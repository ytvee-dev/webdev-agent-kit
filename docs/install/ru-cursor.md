---
id: 'agents.docs.install.ru-cursor'
title: 'Cursor Install Guide'
doc_type: 'user-guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/cursor'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
depends_on: []
---

# Установка WebDev Agent Kit для Cursor

Скачайте архив:

```text
webdev-agent-kit-cursor.tar.gz
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

Если нужные tool capabilities доступны, агент использует их. Если capability отсутствует, агент использует fallback и честно указывает ограничения.
