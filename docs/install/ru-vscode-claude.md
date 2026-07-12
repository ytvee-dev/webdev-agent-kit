---
id: 'agents.docs.install.ru-vscode-claude'
title: 'VS Code Claude Install Guide'
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

# Установка WebDev Agent Kit для VS Code Claude

VS Code Claude использует тот же нативный plugin contract, что Claude Code CLI.
Скачайте стабильный или версионный alias из одного GitHub Release:

```text
webdev-agent-kit-vs-code-claude.tar.gz
webdev-agent-kit-vs-code-claude-v0.4.0.tar.gz
```

Сверьте SHA-256 выбранного файла с `SHA256SUMS`. Для постоянного личного
подключения распакуйте архив из `~/.claude/skills/`. Проверьте:

```text
~/.claude/skills/webdev-agent-kit/.claude-plugin/plugin.json
~/.claude/skills/webdev-agent-kit/skills/
```

Перезапустите Claude Code extension. В prompt box выполните `/plugins` и
убедитесь, что `webdev-agent-kit@skills-dir` доступен. VS Code extension и CLI
используют одну plugin system; отдельной копии runtime для VS Code нет.

Не копируйте plugin skills в `.agents/skills`.

Если проект отдельно использует `.agents/AGENTS.md`, предложите импортировать эту политику одной строкой в root `CLAUDE.md`:

```text
@.agents/AGENTS.md
```

Создавать или менять существующий `CLAUDE.md` можно только после явного согласия
пользователя; установка plugin сама такого согласия не даёт.

После установки запустите:

```text
адаптируйся
```

Если нужные tool capabilities доступны, агент использует их. Если capability
отсутствует, агент использует fallback и честно указывает ограничения.
