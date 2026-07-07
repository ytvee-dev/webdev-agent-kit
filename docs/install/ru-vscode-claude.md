---
id: 'agents.docs.install.ru-vscode-claude'
title: 'Установка WebDev Agent Kit для VS Code Claude'
doc_type: 'user-guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/vscode-claude'
parent:
    - '[[README|WebDev Agent Kit README]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
depends_on: []
---

# Установка WebDev Agent Kit для VS Code Claude

## Что скачать

```text
webdev-agent-kit-vs-code-claude.tar.gz
```

## Куда распаковать

Распакуйте архив в `.agents/` внутри frontend-проекта.

## Native pointer

Создайте root `CLAUDE.md`:

```md
# CLAUDE.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

## MCP

Если нужный MCP или native tool доступен, агент использует его. Если capability отсутствует, агент использует fallback и сообщает ограничения.

Не устанавливайте MCP и не меняйте клиентский конфиг без явного approval.

## Адаптация

```text
адаптируйся
```

Агент должен определить editor Claude surface, проверить pointer, записать `project/client-profile.md` и `project/mcp-profile.md`, ничего не устанавливать и не менять документацию проекта без approval.
