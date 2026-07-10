---
id: 'agents.docs.install.index'
title: 'Installation Guides'
doc_type: 'user-guide-index'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
parent:
    - '[[CHANGELOG|WebDev Agent Kit Changelog]]'
related:
    - '[[docs/install/ru-codex|Codex Install Guide]]'
    - '[[docs/install/ru-claude-code|Claude Code Install Guide]]'
    - '[[docs/install/ru-cursor|Cursor Install Guide]]'
    - '[[docs/install/ru-vscode-codex|VS Code Codex Install Guide]]'
    - '[[docs/install/ru-vscode-claude|VS Code Claude Install Guide]]'
depends_on: []
---

# Installation Guides

Выберите архив для фактического клиента. Версионный архив содержит тег релиза,
например `webdev-agent-kit-codex-v0.3.0.tar.gz`; стабильное имя без версии содержит
те же байты. Перед распаковкой сверьте SHA-256 файла с `SHA256SUMS` из того же
GitHub Release.

| Клиент | Архив | Куда распаковывать | Нативная точка входа |
| --- | --- | --- | --- |
| Codex | `webdev-agent-kit-codex.tar.gz` | Из корня проекта | `.agents/AGENTS.md` и `.agents/skills/` |
| Claude Code | `webdev-agent-kit-claude-code.tar.gz` | В каталог plugins/skills вне проекта | `webdev-agent-kit/.claude-plugin/plugin.json` |
| Cursor | `webdev-agent-kit-cursor.tar.gz` | Из корня проекта | `.cursor/rules/webdev-agent-kit.mdc` |
| VS Code Codex | `webdev-agent-kit-vs-code-codex.tar.gz` | Из корня проекта | Контракт Codex |
| VS Code Claude | `webdev-agent-kit-vs-code-claude.tar.gz` | В каталог plugins/skills вне проекта | Контракт Claude Code |

- [Codex](ru-codex.md)
- [Claude Code](ru-claude-code.md)
- [Cursor](ru-cursor.md)
- [VS Code Codex](ru-vscode-codex.md)
- [VS Code Claude](ru-vscode-claude.md)

Codex и Cursor архивы сами создают `.agents/`; не распаковывайте их внутри уже
существующего `.agents/`. Claude Code использует нативный plugin root и не должен
копироваться в `.agents/skills`.

Это пользовательские инструкции установки, а не runtime policy и не источник
истины для структуры артефактов. Структуру определяют `bundle-manifest.json`,
сборщик и валидаторы архивов.
