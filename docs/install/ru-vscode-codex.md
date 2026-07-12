---
id: 'agents.docs.install.ru-vscode-codex'
title: 'VS Code Codex Install Guide'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
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

# Установка WebDev Agent Kit для VS Code Codex

Этот архив является compatibility alias канонического Codex target. Скачайте
стабильный или версионный файл из одного GitHub Release:

```text
webdev-agent-kit-vs-code-codex.tar.gz
webdev-agent-kit-vs-code-codex-v0.4.0.tar.gz
```

Сверьте SHA-256 выбранного файла с `SHA256SUMS`. Распакуйте архив из корня
frontend-проекта: он сам создаёт `.agents/`.

Проверьте `.agents/AGENTS.md`, `.agents/skills/` и
`.agents/.codex-plugin/plugin.json`. Не распаковывайте архив внутри `.agents/`,
иначе появится `.agents/.agents/`.

Если root `AGENTS.md` отсутствует, после осознанного подтверждения добавьте
минимальный указатель на `.agents/AGENTS.md`. Существующий root-файл нельзя
заменять.

Перезапустите Codex extension, откройте сессию из корня проекта и запустите:

```text
адаптируйся
```

Если нужные tool capabilities доступны, агент использует их. Если capability
отсутствует, агент использует fallback и честно указывает ограничения.
