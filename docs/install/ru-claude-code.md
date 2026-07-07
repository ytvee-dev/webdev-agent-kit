---
id: 'agents.docs.install.ru-claude-code'
title: 'Установка WebDev Agent Kit для Claude Code'
doc_type: 'user-guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/claude-code'
parent:
    - '[[README|WebDev Agent Kit README]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
depends_on: []
---

# Установка WebDev Agent Kit для Claude Code

## Что скачать

Скачайте последний архив:

```text
webdev-agent-kit-claude-code.tar.gz
```

из GitHub Releases.

## Куда распаковать

В корне frontend-проекта создайте каталог `.agents/` и распакуйте содержимое архива туда.

## Native pointer

Для Claude Code создайте маленький `CLAUDE.md` в корне проекта:

```md
# CLAUDE.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

Не дублируйте полный policy в `CLAUDE.md`.

## Skills

Claude-compatible target содержит portable `skills/**/SKILL.md`. Если ваша установка Claude Code ожидает skills в отдельном каталоге, используйте содержимое `.agents/skills/**` как source и не копируйте Codex-only `agents/openai.yaml`.

## MCP

Skillpack использует доступные MCP-серверы или native tools, если они уже настроены в Claude Code.

Если capability отсутствует, агент должен работать через разрешенный fallback и явно указать, что заблокировано.

Установка MCP выполняется только после отдельного approval и проверки официального источника.

## Custom instructions

Короткий bootstrap:

```text
Use the repository CLAUDE.md. If it points to WebDev Agent Kit, follow `.agents/AGENTS.md`. Do not read or edit the host project README.md unless the user explicitly asks for documentation work and approves the scope.
```

## Адаптация

После установки попросите:

```text
адаптируйся
```

Агент должен:

- определить Claude Code как client surface;
- создать или обновить `project/client-profile.md`;
- создать или обновить `project/mcp-profile.md`;
- не менять исходный код приложения;
- не менять README или docs проекта без отдельного согласования.

## Проверка

```text
Проверь установку Claude Code target, CLAUDE.md pointer и MCP capability profile. Ничего не устанавливай.
```
