---
id: 'agents.docs.install.ru-codex'
title: 'Codex Install Guide'
doc_type: 'user-guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/codex'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
depends_on: []
---

# Установка WebDev Agent Kit для Codex

Скачайте архив:

```text
webdev-agent-kit-codex.tar.gz
```

Распакуйте архив в `.agents/` внутри frontend-проекта.

Создайте root `AGENTS.md`:

```md
# AGENTS.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

После установки запустите:

```text
адаптируйся
```

MCP/tools используются только если соответствующие capabilities доступны. Если capability отсутствует, агент должен использовать fallback и честно указать ограничения.

Не устанавливайте MCP и не меняйте конфиги без явного approval.
