---
id: 'agents.docs.install.ru-cursor'
title: 'Cursor Install Guide'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
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

Скачайте стабильный или версионный архив из одного GitHub Release:

```text
webdev-agent-kit-cursor.tar.gz
webdev-agent-kit-cursor-v0.4.0.tar.gz
```

Сверьте SHA-256 выбранного файла с `SHA256SUMS`. Распакуйте архив из корня
frontend-проекта: архив сам создаёт `.agents/` и нативный `.cursor/`.

Проверьте обязательные пути:

```text
.agents/AGENTS.md
.agents/skills/
.cursor/rules/webdev-agent-kit.mdc
```

Не распаковывайте архив внутри `.agents/`: это создаст ошибочный путь
`.agents/.agents/`. Не заменяйте существующие root-инструкции; нативное правило
Cursor уже указывает на общую project policy.

Откройте новую Cursor Agent-сессию из корня проекта и запустите:

```text
адаптируйся
```

Если нужные tool capabilities доступны, агент использует их. Если capability
отсутствует, агент использует fallback и честно указывает ограничения.
