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

Распакуйте архив в `.agents/` внутри frontend-проекта.

Создайте root `CLAUDE.md`, который указывает на `.agents/AGENTS.md`.

После установки запустите:

```text
адаптируйся
```

Если нужные tool capabilities доступны, агент использует их. Если capability отсутствует, агент использует fallback и честно указывает ограничения.
