---
id: 'agents.docs.install.ru-cursor'
title: 'Установка WebDev Agent Kit для Cursor'
doc_type: 'user-guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/cursor'
parent:
    - '[[README|WebDev Agent Kit README]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
depends_on: []
---

# Установка WebDev Agent Kit для Cursor

## Что скачать

Скачайте последний архив:

```text
webdev-agent-kit-cursor.tar.gz
```

## Куда распаковать

Распакуйте архив в `.agents/` внутри frontend-проекта.

## Native pointer

Создайте root `AGENTS.md`:

```md
# AGENTS.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

Cursor rules должны оставаться короткими и ссылаться на тот же canonical policy.

## MCP

Cursor должен использовать уже настроенные MCP tools, если они доступны в текущей сессии.

Если capability отсутствует, агент использует fallback и сообщает снижение уверенности или заблокированные проверки.

MCP setup выполняется только после явного approval и проверки официального источника.

## Адаптация

```text
адаптируйся
```

Агент должен определить Cursor target, проверить root pointer, записать local-only `project/client-profile.md` и `project/mcp-profile.md`, не менять app source и не менять README или docs проекта без отдельного согласования.

## Проверка

```text
Проверь Cursor установку, AGENTS.md pointer и MCP capabilities. Не меняй конфиги без approval.
```
