---
id: 'agents.docs.install.ru-codex'
title: 'Установка WebDev Agent Kit для Codex'
doc_type: 'user-guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/codex'
parent:
    - '[[README|WebDev Agent Kit README]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
depends_on: []
---

# Установка WebDev Agent Kit для Codex

## Что скачать

Скачайте последний архив:

```text
webdev-agent-kit-codex.tar.gz
```

из GitHub Releases.

## Куда распаковать

В корне frontend-проекта создайте каталог `.agents/` и распакуйте содержимое архива туда.

Итоговая форма:

```text
your-project/
├── AGENTS.md
└── .agents/
    ├── AGENTS.md
    ├── common/
    ├── skills/
    ├── templates/
    └── tool-capabilities-manifest.json
```

## Root pointer

Для Codex создайте маленький `AGENTS.md` в корне проекта:

```md
# AGENTS.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

Не копируйте полный `.agents/AGENTS.md` в корень проекта.

## MCP

Skillpack использует MCP-серверы и native tools, заявленные в capability model, когда они доступны в текущей Codex-сессии.

Рекомендуемый frontend-набор:

```text
project_files
current_library_docs
web_platform_docs
rendered_visual_evidence
```

Если нужный MCP-сервер недоступен, агент должен использовать разрешенный fallback и честно указать, какие проверки стали менее надежными или заблокированы.

Не устанавливайте и не включайте MCP-серверы без явного согласия пользователя и проверки официального источника.

## Custom instructions

В системных инструкциях Codex достаточно короткого bootstrap:

```text
Use the repository AGENTS.md. If the repository installs WebDev Agent Kit, follow `.agents/AGENTS.md`. Do not read or edit the host project README.md unless the user explicitly asks for documentation work and approves the scope.
```

## Адаптация

После установки попросите агента:

```text
адаптируйся
```

Ожидаемый результат:

- агент определяет клиент и стек;
- создает или обновляет local-only `project/client-profile.md`;
- создает или обновляет local-only `project/mcp-profile.md`;
- не меняет исходный код приложения;
- не меняет README или docs проекта без отдельного согласования.

## Проверка

Попросите агента сообщить:

```text
Проверь, что WebDev Agent Kit установлен, AGENTS.md указывает на .agents/AGENTS.md, MCP capabilities определены, но ничего не устанавливай.
```
