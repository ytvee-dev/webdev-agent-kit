// Optional OpenCode plugin. Does not activate storage without per-project opt-in.
// SDK reference: https://opencode.ai/docs/sdk/ and https://opencode.ai/docs/plugins/
export const ExperienceRecorder = async ({ client, directory }) => {
  const script = process.env.AGENT_LEARNING_SCRIPT
  if (!script) return {}

  const python = process.env.AGENT_LEARNING_PYTHON || "python"
  const run = async (subcommand, payload) => {
    try {
      const proc = Bun.spawn(
        [python, script, subcommand, "--project", directory],
        { stdin: "pipe", stdout: "pipe", stderr: "ignore" },
      )
      if (payload !== undefined) proc.stdin.write(JSON.stringify(payload))
      proc.stdin.end()
      const output = await new Response(proc.stdout).text()
      const exit = await proc.exited
      return exit === 0 ? JSON.parse(output) : null
    } catch {
      // Recorder failures must never block the user's primary agent.
      return null
    }
  }

  return {
    event: async ({ event }) => {
      if (event.type !== "session.idle") return
      const sessionID = event.properties?.sessionID
      if (!sessionID) return

      const status = await run("status")
      if (!status?.recording) return

      let response
      try {
        response = await client.session.messages({ path: { id: sessionID } })
      } catch {
        return
      }
      const messages = response?.data ?? response
      if (!Array.isArray(messages)) return

      const records = []
      const inline = []
      for (const message of messages) {
        const info = message.info ?? {}
        for (const part of message.parts ?? []) {
          if (!part?.id) continue
          const isText = part.type === "text"
          const isFile = part.type === "file"
          const isTool = part.type === "tool"
          if (!isText && !isFile && !isTool) continue

          const kind = isTool ? "tool" : info.role === "user" ? "user" : "assistant"
          const content = isText
            ? String(part.text ?? "")
            : isTool ? "Tool: " + String(part.tool ?? "unknown") : ""
          const metadata = isFile
            ? [{ name: part.filename ?? "attachment", mime: part.mime ?? "",
                 status: "metadata_only" }]
            : []
          const invoked = isTool && part.tool === "skill"
            ? [part.state?.input?.name].filter((name) => typeof name === "string")
            : []
          records.push({
            client: "opencode",
            session_id: String(sessionID),
            message_id: String(info.id ?? part.id),
            part_id: String(part.id),
            kind,
            content,
            skills: invoked,
            attachments: metadata,
          })
          if (isFile && typeof part.url === "string" &&
              part.url.startsWith("data:") && part.url.length <= 28000000) {
            inline.push({
              client: "opencode",
              session_id: String(sessionID),
              name: part.filename ?? "attachment",
              data_url: part.url,
            })
          }
        }
      }

      // Re-reading on every idle event is safe: the database deduplicates by part ID.
      for (let index = 0; index < records.length; index += 400) {
        await run("capture-batch", records.slice(index, index + 400))
      }
      // Only embedded data: bytes are copied. No arbitrary local path or URL is followed.
      for (const item of inline) {
        await run("attach-data", item)
      }
    },
  }
}
