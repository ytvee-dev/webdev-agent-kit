---
id: 'agents.docs.install.ru-claude-code'
title: 'Claude Code Install Guide'
doc_type: 'user-guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'docs/install'
parent:
    - '[[docs/install/README|Installation Guides]]'
related: []
depends_on: []
---

# Установка

Скачайте `webdev-agent-kit-claude-code.tar.gz` и распакуйте каталог `webdev-agent-kit/` вне проекта. Это корень нативного Claude Code plugin: внутри него должны находиться `.claude-plugin/plugin.json` и `skills/`.

Подключите каталог через нативный plugin flow Claude Code. Для локальной проверки можно запустить:

```text
claude --plugin-dir /absolute/path/to/webdev-agent-kit
```

Не распаковывайте plugin в `.agents/skills`: Claude обнаруживает skills внутри plugin автоматически.

Если проект отдельно использует общую политику `.agents/AGENTS.md`, предложите добавить в root `CLAUDE.md` ровно одну строку:

```text
@.agents/AGENTS.md
```

Создавать или менять существующий `CLAUDE.md` можно только после явного согласия пользователя.

После установки запустите `адаптируйся`.
