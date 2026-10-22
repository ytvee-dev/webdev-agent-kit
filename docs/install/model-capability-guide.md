---
id: 'agents.docs.install.model-capability-guide'
title: 'Models, Clients And Tool Capabilities'
doc_type: 'guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'installation/models'
    - 'tools/capabilities'
parent:
    - '[[README]]'
related:
    - '[[docs/install/gpt-model-routing]]'
    - '[[docs/install/claude-agents]]'
    - '[[common/tool-capability-model]]'
depends_on: []
---

# Models, Clients And Tool Capabilities

Documentation checked: **2026-10-22**. Recommendations below are WebDev starting
choices informed by provider documentation, not a comparative Kit benchmark or a
guarantee of availability in your account. Check the exact model, client version,
authentication method and workspace controls before configuring a project.

## Contents

- [Choose a model by provider](#choose-a-model-by-provider)
- [Match the capability to its requirements](#match-the-capability-to-its-requirements)
- [Choose the client separately](#choose-the-client-separately)
- [Verify your installation](#verify-your-installation)

## Choose a model by provider

### OpenAI

| Use | Starting choice | Boundary |
| --- | --- | --- |
| Everyday implementation, debugging and tool-driven workflows | GPT-6.1 Sol (`gpt-6.1-sol`) | Use only if exposed by your account/client; retain a verified existing binding otherwise |
| Difficult architecture or multi-step investigation | GPT-6 Astra (`gpt-6-astra`) | Reserve for material reasoning needs and an acceptable usage budget |
| Demanding screenshot/UI judgment and Computer Use | GPT-6 Astra | The client still needs the actual screenshot/action tools |
| Bounded extraction, summaries and repetitive code edits | GPT-6 Luna (`gpt-6-luna`) | Do not infer suitability for critical independent review from low cost |

Start with the client's supported default effort; increase it for a concrete
reasoning need. UI labels and API values differ. Max/Ultra are not universal
settings; Ultra can involve subagents, so check the task's delegation constraints.
These recommendations do not rewrite existing local routing profiles. Older
versioned routing guidance is not proof of current model availability.

Sources: [model selection and availability](https://learn.chatgpt.com/docs/models),
[Computer Use](https://learn.chatgpt.com/docs/computer-use).

### Anthropic

| Use | Starting choice | Boundary |
| --- | --- | --- |
| General agentic coding with quality prioritized | Claude Opus 5.5 | Provider's general starting recommendation; verify client access |
| Routine bounded implementation with latency in mind | Claude Sonnet 5.5 | WebDev starting recommendation, not a measured cost/quality winner |
| Extraction, classification and small known transformations | Claude Haiku 5.5 | Keep acceptance criteria narrow |
| Exceptional reasoning and long-horizon work | Claude Fable 5.1 | Consider when available and ordinary Opus evaluation is insufficient |
| Screenshot analysis | Sonnet 5.5 for bounded inspection; Opus 5.5 for ambiguous flows | Current lineup supports image input, but the client must transmit the image |
| Computer Use through an integrated environment | Opus 5.5 as a starting choice | Match the hosting platform's computer-tool version and execution loop |

Do not copy a provider model ID into another host blindly. Claude 5.5 on the
Claude API and Google Cloud requires `computer_toolset_20260801`; Bedrock has a
different compatibility path. API computer-tool support does not establish that
Claude Code has access to your desktop. Kit Claude roles inherit the selected
model unless an approved, supported binding is configured.

Sources: [model lineup](https://platform.claude.com/docs/en/models/overview),
[vision](https://platform.claude.com/docs/en/build-with-claude/vision),
[computer-tool compatibility](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool),
[Kit Claude roles](claude-agents.md).

### Google

| Use | Starting choice | Boundary |
| --- | --- | --- |
| Complex engineering and long-context reasoning | Gemini 4 Argon (`gemini-4-argon`) | Verify the chosen client's provider adapter and tool support |
| Browser UI action loop | Gemini 3.8 Flash (`gemini-3.8-flash`) | Google's documented Computer Use recommendation; an executor is still required |
| More demanding UI reasoning | Gemini 4 Argon | Supported Computer Use model; not a ready-made desktop connection |
| Low-latency bounded tasks | Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`) | Evaluate the actual task before delegating consequential work |
| Image, PDF, video or audio input analysis | Gemini 4 Argon when the client exposes those inputs | Input support does not imply audio/image generation or live camera access |

Gemini recommendations concern provider capabilities. The Kit does not ship a
native Gemini client target or claim a live-tested Gemini installation. Use a
compatible host and verify its tools. Search grounding must be enabled through
the supported integration; merely selecting Gemini does not enable web search.

Sources: [model catalog](https://ai.google.dev/gemini-api/docs/models),
[Argon input capabilities](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon),
[Computer Use](https://ai.google.dev/gemini-api/docs/computer-use),
[Google Search grounding](https://ai.google.dev/gemini-api/docs/google-search).

### Other providers, gateways and local models

There is no blanket "all tools supported" recommendation for an OpenAI-compatible
endpoint, a free model, or a local model. Check its exact version for tool calling,
image input, structured arguments, context limits and client adapter support.
Use bounded extraction/code tasks first; do not assign visual QA to a text-only
endpoint. A gateway may expose fewer capabilities than the underlying provider.
Account availability and free-tier quotas can change independently of the Kit.

OpenCode supports multiple providers and local models; its own recommendation
list explicitly may not be current. Prefer current provider specifications and
small checks in your installed client. See [OpenCode models](https://opencode.ai/docs/models/).

## Match the capability to its requirements

This table is a practical selection/checklist, not a provider support certificate.

| Capability | What the model needs | What the client/environment needs | Useful verification |
| --- | --- | --- | --- |
| MCP tools | Reliable tool selection and structured arguments; image input for visual responses | Connected server, authenticated identity and permitted tool schema | One scoped read-only call with a real result |
| WebDev capture hooks | No special model: these are local command handlers | Supported lifecycle events, installed Python/bridge, consent, client trust | Observe an actual event from the current session in local capture |
| Browser navigation | Tool use; vision when acting on screenshots | Browser plugin/native browser/approved automation with the required session | Open a harmless page, identify a control and verify resulting state |
| Desktop Computer Use | Visual grounding plus the supported action protocol | Screenshot/click executor, OS permissions and access to the correct machine | Inspect a harmless window; do not infer access from a model name |
| Web search and source verification | Tool use and evidence synthesis | Search/fetch or provider grounding enabled | Retrieve a current source, open it and cite the matching claim |
| Screenshots, Figma and visual QA | Image input and adequate visual reasoning | Actual screenshot/image payload; Figma metadata alone is insufficient | Compare a known element/state; distinguish observed values from estimates |
| PDF/documents, audio and video | The corresponding input modality or an explicit extraction tool | File reader/renderer/transcriber and access to the file | Check a known page or timestamp, including extraction limitations |
| Terminal, edits, builds and tests | Code reasoning and correct tool arguments | Workspace, shell/runtime, dependencies and permissions | Run the relevant existing check; do not equate a code suggestion with execution |
| Subagents and independent review | Adequate role/model for each bounded assignment | Native dispatch, isolated reviewer context, verified bindings and budget | Verify one authorized invocation; configuration alone is insufficient |
| Long-context analysis | Enough context and stable reasoning across evidence | Retrieval, compaction and preserved project constraints | Check that decisive sources survived retrieval/compaction |
| Project memory and manual sync | Evidence extraction and scoped retrieval | Opted-in local storage, valid schema and separately configured sync | Verify project isolation and manual exchange; this does not train model weights |
| Image generation/editing | A dedicated supported image-generation capability | Image tool/provider and artifact output | Inspect the produced image; vision input alone does not imply generation |

Command hooks differ from prompt/agent hooks offered by some clients: the latter
can make model calls. WebDev's capture bridge uses commands, not an LLM inside
the hook. Changing the main model does not repair hook trust or a missing runtime.
See [Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Claude hooks](https://code.claude.com/docs/en/hooks),
[Claude MCP](https://code.claude.com/docs/en/mcp),
[OpenAI image inputs](https://learn.chatgpt.com/docs/image-inputs),
[OpenAI search](https://learn.chatgpt.com/docs/web-search) and
[Claude search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool).

## Choose the client separately

| Client/surface | Practical choice | Important distinction |
| --- | --- | --- |
| Codex in a supported desktop surface | Sol for general work; Astra for difficult visual workflows | Confirm Browser/Computer Use is available in this session and can reach the intended app |
| Codex CLI or IDE extension | Same verified coding model; use exposed tools | OpenAI's built-in Browser is not available here; another browser integration is a separate capability |
| Claude Code | Use the chosen Claude model and the Kit's native plugin | MCP, lifecycle hooks and local roles are client features; API computer-use support is not desktop access |
| Cursor | Choose an explicitly available model for reproducible setup checks | Auto routing is not a stable model identity; inspect actual capability exposure |
| OpenCode | Select a supported provider/model pair and verify the adapter | MCP and plugins need their own setup; the Kit's capture integration remains a preview |

A cloud/browser environment cannot automatically inspect your local desktop or
an application on another machine. A CLI launched by an orchestrator does not
thereby gain a desktop application's session. Verify where each tool actually
runs. When the task explicitly requires native Computer Use, do not silently
substitute DOM automation or treat source inspection as visual verification.

Sources: [OpenAI Browser availability](https://learn.chatgpt.com/docs/browser),
[Cursor models and routing](https://cursor.com/docs/models-and-pricing),
[OpenCode MCP](https://opencode.ai/docs/mcp-servers/),
[Kit integration status](../../skills/agent-self-improvement/assets/integrations/INTEGRATIONS.md).

## Verify your installation

Ask: "Check my WebDev setup and report the model, image inputs, MCP, hooks,
browser, Computer Use, search and subagent capabilities. Do not change setup."
Inspect configured/discovered/permitted/runtime-verified states separately. For
capabilities without a real check, say **unverified**, not **working**.

Run only explicitly authorized, bounded probes. Capture verification itself
requires capture consent. A diagnostic request alone does not enable recording,
install dependencies, launch model canaries or alter trust. Record successful
checks with client/model/version/date in local project profiles; repeat after
relevant drift. See [GPT routing](gpt-model-routing.md) and
[installation diagnostics](../../skills/project-onboarding-adapter/references/installation-diagnostics.md).

For cost comparisons measure the full accepted task: coordinator, children,
retries, review and tool costs. A cheaper token price or larger context window is
not proof of lower total cost or better results. This guide changes no defaults
or model bindings and must be rechecked against provider sources when stale.
