---
id: 'agents.docs.install.ru-claude-code'
title: 'Claude Code Install Guide'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
parent:
    - '[[docs/install/README|Installation Guides]]'
related: []
depends_on: []
---

# Установка WebDev Agent Kit для Claude Code

Скачайте `webdev-agent-kit-claude-code.tar.gz` или версионный
`webdev-agent-kit-claude-code-v0.4.0.tar.gz` из одного GitHub Release и сверьте
SHA-256 с `SHA256SUMS`.

Для постоянного личного подключения распакуйте архив из
`~/.claude/skills/`. Ожидаемый plugin root:

```text
~/.claude/skills/webdev-agent-kit/.claude-plugin/plugin.json
~/.claude/skills/webdev-agent-kit/skills/
```

Claude Code обнаруживает такой skills-directory plugin как
`webdev-agent-kit@skills-dir` при следующем запуске. Для односессионной проверки
распакованного каталога можно использовать:

```text
claude --plugin-dir /absolute/path/to/webdev-agent-kit
```

Проверьте plugin через `claude plugin list` или интерфейс `/plugins`. Флаг
`--plugin-dir` предназначен для локальной проверки и действует только в текущей
сессии.

Не распаковывайте plugin в `.agents/skills`: Claude обнаруживает skills внутри
нативного plugin автоматически.

Если проект отдельно использует общую политику `.agents/AGENTS.md`, предложите добавить в root `CLAUDE.md` ровно одну строку:

```text
@.agents/AGENTS.md
```

Создавать или менять существующий `CLAUDE.md` можно только после явного согласия
пользователя; установка plugin сама такого согласия не даёт.

После перезапуска Claude Code запустите `адаптируйся`.
