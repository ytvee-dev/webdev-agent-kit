// Optional, experimental OpenCode adapter. Manually copy into .opencode/plugins/.
// Set AGENT_LEARNING_SCRIPT to an absolute path to the shipped learning.py.
// No raw image bytes are copied. File parts remain metadata-only until explicit import.
export const ExperienceRecorder = async ({ client, directory }) => {
  const script = process.env.AGENT_LEARNING_SCRIPT
  if (!script) return {}

  async function command(commandName, event) {
    try {
      const proc = Bun.spawn(
        ["python", script, commandName, "--project", directory],
        { stdin: "pipe", stdout: "pipe", stderr: "ignore" },
      )
      if (event !== undefined) proc.stdin.write(JSON.stringify(event))
      proc.stdin.end()
      const output = await new Response(proc.stdout).text()
      await proc.exited
      return JSON.parse(output)
    } catch {
      return null // The recorder is best-effort and must never block OpenCode.
    }
  }

  return {
    event: async ({ event }) => {
      if (event.type !== "session.idle") return
      const status = await command("status")
      if (!status?.recording) return

      const sessionID = event.properties?.sessionID
      if (!sessionID) return
      let messages
      try {
        const response = await client.session.messages({ path: { id: sessionID } })
        messages = response.data ?? response
      } catch {
        return
      }
      if (!Array.isArray(messages)) return

      for (const message of messages) {
        const info = message.info ?? {}
        for (const part of message.parts ?? []) {
          if (!part?.id) continue
          const isText = part.type === "text"
          const isFile = part.type === "file"
          const isTool = part.type === "tool"
          if (!isText && !isFile && !isTool) continue
          const kind = isTool ? "tool" : info.role === "user" ? "user" : "assistant"
          const canonical = {
            client: "opencode",
            session_id: String(sessionID),
            message_id: String(info.id ?? part.id),
            part_id: String(part.id),
            kind,
            content: isText ? String(part.text ?? "") : isTool ? String(part.tool ?? "tool") : "",
            attachments: isFile ? [{ name: part.filename ?? "attachment",
                                      mime: part.mime ?? "application/octet-stream" }] : [],
          }
          await command("capture", canonical)
        }
      }
    },
  }
}
