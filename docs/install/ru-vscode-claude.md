---
id: 'agents.docs.install.ru-vscode-claude'
title: 'VS Code Claude Install Guide'
doc_type: 'user-guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'docs/install'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
depends_on: []
---

# Установка WebDev Agent Kit для VS Code Claude

Скачайте архив:

```text
webdev-agent-kit-vs-code-claude.tar.gz
```

Распакуйте каталог `webdev-agent-kit/` вне проекта и подключите его через нативный Claude Code plugin flow, доступный в текущей интеграции VS Code. В plugin root должны находиться `.claude-plugin/plugin.json` и `skills/`.

Не копируйте plugin skills в `.agents/skills`.

Если проект отдельно использует `.agents/AGENTS.md`, предложите импортировать эту политику одной строкой в root `CLAUDE.md`:

```text
@.agents/AGENTS.md
```

Создавать или менять существующий `CLAUDE.md` можно только после явного согласия пользователя.

После установки запустите:

```text
адаптируйся
```

Если нужные tool capabilities доступны, агент использует их. Если capability отсутствует, агент использует fallback и честно указывает ограничения.
