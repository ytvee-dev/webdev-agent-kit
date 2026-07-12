---
id: 'agents.docs.install.ru-codex'
title: 'Codex Install Guide'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
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

Скачайте стабильный или версионный архив из одного GitHub Release:

```text
webdev-agent-kit-codex.tar.gz
webdev-agent-kit-codex-v0.4.0.tar.gz
```

Сверьте SHA-256 выбранного файла с `SHA256SUMS`. Распакуйте архив из корня
frontend-проекта: архив сам создаёт `.agents/`. Распаковка внутри существующего
`.agents/` ошибочна, потому что создаст `.agents/.agents/`.

Проверьте обязательные пути:

```text
.agents/AGENTS.md
.agents/skills/
.agents/.codex-plugin/plugin.json
```

Если root `AGENTS.md` отсутствует, добавьте минимальный указатель только после
осознанного подтверждения. Существующий файл нельзя заменять; в него нужно
аккуратно добавить совместимую инструкцию:

```md
# AGENTS.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

Откройте новую Codex-сессию из корня проекта и запустите:

```text
адаптируйся
```

MCP/tools используются только если соответствующие capabilities доступны. Если
capability отсутствует, агент должен использовать fallback и честно указать
ограничения.

Не устанавливайте MCP и не меняйте конфиги без явного approval.
