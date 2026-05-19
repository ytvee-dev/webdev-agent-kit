---
id: 'agents.readme'
title: 'webdev-assistant'
doc_type: 'readme'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/readme'
    - 'docs/onboarding'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
depends_on:
    []
---

# webdev-assistant

`webdev-assistant` - это общий набор инструкций, проектных overlays и навыков
для работы OpenAI Codex с React, Next.js, TypeScript, CSS Modules и
документацией самого набора.

Эта документация описывает именно использование набора через официальный
OpenAI Codex IDE extension в VS Code. Она не является инструкцией для Cursor,
Roo, Cline, Claude Code, Copilot, Continue или других агентных систем. Другие
инструменты могут читать Markdown-файлы, но routing skills,
`agents/openai.yaml`, implicit invocation, MCP/connectors и рабочие соглашения
здесь рассчитаны на Codex.

Официальные справочные страницы:

- Codex IDE extension: <https://developers.openai.com/codex/ide>
- Codex IDE settings: <https://developers.openai.com/codex/ide/settings>
- Codex skills: <https://developers.openai.com/codex/skills>
- `AGENTS.md` discovery: <https://developers.openai.com/codex/guides/agents-md>

## Модель подключения

В принимающем проекте этот набор подключается как вложенный checkout
`.agents/`:

```text
host-project/
├─ AGENTS.md
├─ .agents/
│  ├─ AGENTS.md
│  ├─ SUMMARY.md
│  ├─ README.md
│  ├─ common/
│  ├─ skills/
│  ├─ project/
│  └─ .gitignore
└─ src/...
```

Корневой `AGENTS.md` принимающего проекта должен быть стабильным указателем на
`.agents/AGENTS.md`. Он не должен копировать содержимое `.agents/AGENTS.md`.

`.agents/` одновременно является локальным checkout репозитория
`git@github.com:ytvee-dev/webdev-assistant.git`. Внутри upstream-репозитория
эти же файлы лежат в корне, но в принимающем проекте они доступны через
`.agents/<path>`.

## Архитектура `.agents/`

### `AGENTS.md`

Главная политика набора. В ней закреплены:

- модель вложенного bundle;
- порядок чтения;
- общие правила работы;
- правила публикации upstream;
- карта навыков;
- список общих документов;
- список локальных project overlays.

Это канонический publishable policy file. Если правило в README и
`.agents/AGENTS.md` расходится, реализацию нужно привести к `.agents/AGENTS.md`,
а README обновить.

### `SUMMARY.md`

Навигационная карта набора. Она отвечает на вопросы:

- какие common docs существуют;
- какие project overlays ожидаются;
- какие skills есть;
- какой общий порядок чтения;
- какие пути publishable, а какие local-only;
- какие skill chains выбирать для типовых задач.

README может объяснять назначение этих частей, но актуальный список skills и
overlays должен сверяться с `SUMMARY.md`.

### `common/**`

Общие publishable правила, которые можно переносить между принимающими
проектами:

- `common/approved-patterns.md` - общие разрешенные паттерны реализации;
- `common/anti-patterns.md` - общие запрещенные направления;
- `common/documentation-maintenance.md` - правила изменения документации,
  слоев и sync-контракта.

В `common/**` нельзя помещать факты конкретного проекта: реальные пути
приложения, версии зависимостей, локальные исключения, локальные команды,
локальные токены или архитектурные детали конкретного продукта.

### `project/**`

Локальный контекст принимающего проекта. Этот каталог нужен, чтобы Codex не
сканировал весь репозиторий заново перед каждой задачей.

Ожидаемые overlays:

- `project/stack-profile.md` - стек, runtime, tooling, state-management;
- `project/architecture-map.md` - маршруты, shared code, client/server zones;
- `project/styling-profile.md` - styling system, tokens, conventions;
- `project/verification-profile.md` - команды проверки и порядок запуска;
- `project/approved-patterns.md` - локальные разрешенные паттерны;
- `project/anti-patterns.md` - локальные анти-паттерны и исключения;
- `project/figma-profile.md` - правила design-to-code;
- `project/react/path-index.md` - lookup index для React/client работы;
- `project/next/path-index.md` - lookup index для Next.js App Router.

`project/**` всегда local-only. Его нельзя публиковать upstream.

### `skills/**`

Переиспользуемые workflows для Codex. Skill - это папка с обязательным
`SKILL.md` и дополнительными ресурсами:

```text
skills/<skill-name>/
├─ SKILL.md
├─ agents/openai.yaml
├─ references/
├─ scripts/
└─ assets/
```

`SKILL.md` должен описывать, когда skill включается, что прочитать, какой
workflow выполнить и как проверить результат. Подробные чеклисты, варианты,
таблицы и справочные материалы выносятся в `references/`. Скрипты добавляются
только для повторяемой или хрупкой работы, где нужен детерминированный
инструмент.

### `.gitignore`

Защищает local-only paths и служебный шум во вложенном checkout. В частности,
`project/**` и старые helper trees вроде `upstream/**` не должны попадать в
публикацию.

## Obsidian Graph

Каталог `.agents/` можно открыть как Obsidian vault. Все Markdown-документы в
этом дереве имеют YAML frontmatter с `id`, `title`, `doc_type`, `layer`,
`publishable`, `local_only`, `tags` и связями `parent`, `related`,
`depends_on`.

Frontmatter - это metadata для routing, поиска, навигации и graph view. Агент
должен читать рабочие правила и workflow в body документа. Frontmatter не
заменяет `Reference map`, не содержит скрытых инструкций и не требует читать
все связанные документы без причины.

Связи записываются как Obsidian wikilinks относительно root `.agents`, например
`[[skills/webapp-task-protocol/SKILL|Webapp Task Protocol]]`. Для одноименных
файлов вроде `anti-patterns.md` и `path-index.md` используются полные пути,
чтобы graph не смешивал разные документы.

Локальные настройки vault в `.obsidian/**` не публикуются upstream и должны
оставаться local-only.

## Как Codex читает инструкции

Codex собирает инструкции слоями:

1. Глобальные инструкции пользователя из Codex home.
2. Project-level `AGENTS.md` от корня workspace вниз к текущей директории.
3. Более близкие инструкции имеют приоритет над более дальними.
4. Repo-local skills подбираются отдельно по имени, описанию и user intent.

В этом проекте порядок для агента такой:

1. Прочитать корневой `AGENTS.md`.
2. Перейти к `.agents/AGENTS.md`.
3. Прочитать `.agents/SUMMARY.md`.
4. Выбрать relevant skill по prompt и repo context.
5. Прочитать нужные `common/**`, `project/**`, references и affected source
   files.

Пользователь не обязан явно писать `$skill-name`. Если prompt совпадает с
описанием skill, Codex должен выбрать skill сам.

## Что должно быть настроено в VS Code

Минимальная рабочая конфигурация:

1. Установлен официальный OpenAI Codex IDE extension из Visual Studio Code
   Marketplace.
2. Пользователь вошел через ChatGPT account или API key.
3. В VS Code открыт корень принимающего проекта, где есть корневой `AGENTS.md`
   и каталог `.agents/`.
4. `.agents/skills/**` находится внутри workspace, чтобы Codex мог обнаружить
   repo-scoped skills.
5. В проекте сохранена структура `.agents/AGENTS.md`, `.agents/SUMMARY.md`,
   `.agents/common/**`, `.agents/skills/**`, `.agents/project/**`.
6. Shell доступен для search, git state, diff, formatting и verification
   commands.

Дополнительные возможности:

- GitHub connector нужен для `webdev-assistant-sync publish-up`, потому что PR
  должен создаваться через connector.
- Figma capability нужна для задач с Figma URL и design implementation.
- Filesystem MCP желателен для чтения файлов и структуры каталогов; правила
  набора предпочитают MCP file reads, когда инструмент доступен.
- WSL нужен только если проект и tooling живут в WSL. В этом случае Codex в VS
  Code должен запускаться в той же среде, где находятся зависимости и команды
  проекта.

Модель, approvals, sandbox и некоторые настройки Codex управляются настройками
Codex/IDE extension и конфигурацией Codex, а не файлами этого bundle. README
фиксирует только требования, которые важны для корректного чтения `.agents`.

## Навыки

### `webapp-task-protocol`

Базовый routing skill для React/Next.js задач. Используется для feature,
refactor, bugfix, review, audit и design implementation.

Что делает:

- классифицирует задачу;
- определяет project type: `frontend-only` или `fullstack`;
- выбирает skill chain;
- требует inspect -> plan -> implement -> verify;
- направляет агента к path indexes и overlays до широкого поиска.

### `nextjs-app-router`

Используется для App Router routes, layouts, metadata, dynamic segments,
loading/error states и server/client boundaries.

Ключевые правила:

- держать route special files тонкими;
- выбирать server/client boundary осознанно;
- не импортировать server-only логику в client code;
- учитывать metadata, canonical, robots, sitemap и route-level UX states;
- после structural route changes проверять, нужны ли updates в
  `.agents/project/next/path-index.md`.

### `react-component-workflow`

Используется для компонентов, props/state flow, hooks, rendering logic,
client UI и reusable behavior.

Ключевые правила:

- делать компоненты небольшими и сфокусированными;
- держать data flow явным;
- хранить state на минимальном нужном уровне;
- использовать effects только для настоящих side effects;
- учитывать reactive identity context/store/custom hooks;
- добавлять `redux-state-workflow`, если затронут shared state.

### `redux-state-workflow`

Используется для Redux, Redux Toolkit, selectors, typed hooks, providers и
store-like shared state.

Ключевые правила:

- сначала доказать, что state действительно shared;
- не добавлять Redux в проект, где его нет, без архитектурного решения;
- держать shared state serializable и минимальным;
- не использовать Redux как transport/fetch/business layer;
- предпочитать узкие selectors и stable references.

### `frontend-typescript-rules`

Используется при TypeScript refactors, exported APIs, public helpers,
components и safe narrowing.

Ключевые правила:

- сохранять strict typing;
- не использовать `any` и `@ts-ignore`;
- использовать `import type` для type-only imports;
- переиспользовать существующие schemas/helpers/types;
- добавлять explicit return types для exported functions, когда это повышает
  ясность.

### `boundary-input-validation`

Используется для untrusted input: user input, route params, search params,
external data, files и public entry points.

Ключевые правила:

- валидировать на boundary;
- не размазывать fallback coercion downstream;
- сначала искать существующие helpers/dependencies;
- не добавлять validation library без явного approval.

### `frontend-review-and-fix`

Используется после реализации или когда пользователь просит review/follow-up
fixes.

Ключевые правила:

- сначала искать bugs, regressions, лишние abstraction и risk;
- запускать verification из `.agents/project/verification-profile.md`;
- проверять, нужны ли updates в `.agents/project/**`;
- для security/SEO поверхностей рекомендовать профильный audit.

### `project-context-adapter`

Используется, когда изменились факты проекта или path indexes устарели.

Что обновляет:

- `stack-profile.md`;
- `architecture-map.md`;
- `styling-profile.md`;
- `verification-profile.md`;
- `approved-patterns.md`;
- `anti-patterns.md`;
- `figma-profile.md`;
- `react/path-index.md`;
- `next/path-index.md`.

Этот skill редактирует только `.agents/project/**`.

### `project-onboarding-adapter`

Используется для первичной адаптации `webdev-assistant` в новом проекте:
`адаптируйся`, `адаптируй проект`, `подключи .agents`,
`обнови контекст проекта`, `initialize Codex project context`.

Skill работает только в Plan Mode. Если пользователь вызывает его в обычном
режиме, агент должен коротко ответить:

```text
Этот навык работает только в Plan Mode. Включите Plan Mode и повторите: "адаптируйся".
```

В Plan Mode skill не меняет файлы. Он анализирует host project, проверяет
root `AGENTS.md`, планирует заполнение `.agents/project/**`, сверяет пути в
`.agents` docs и skills, затем выдает decision-complete план адаптации.
Выполнение начинается отдельным запросом после выхода из Plan Mode.

Отличие от `project-context-adapter`: `project-onboarding-adapter` отвечает за
первичное подключение проекта, root pointer и полный path/rules audit, а
`project-context-adapter` обновляет уже существующие overlays после drift или
изменений в коде.

### `agent-rules-skill-author`

Используется для `AGENTS.md`, `.agents/common/**`, `.agents/project/**`,
`.agents/skills/**`, skill authoring и agent policy.

Ключевые правила:

- сначала выбрать слой: repo policy, common docs, project overlay или skill;
- не смешивать reusable policy и project facts;
- при создании skills сначала извлекать workflow из чата, repo docs, task
  traces и user corrections, а не писать skill с нуля по догадке;
- делать и trigger evals, и 2-3 realistic workflow evals, а не ограничиваться
  только frontmatter;
- при создании skills определить trigger surface, should/should-not prompts,
  output shape, source-backed workflow и validation gates;
- исправлять skill по reusable причинам, а не подгонять его под один prompt;
- держать `SKILL.md` lean, details выносить в `references/`;
- синхронизировать `agents/openai.yaml` с intent skill.

### `readme-maintainer`

Используется для аудита и поддержки `.agents/README.md`.

После текущего обновления его задача - держать README подробным, точным и
структурированным, если README является пользовательским справочником по
bundle. Он не должен превращать README в маркетинговый текст или склад
локальных project facts.

### `webdev-assistant-sync`

Используется для `sync-down`, `publish-up` и fallback branch push в upstream
`git@github.com:ytvee-dev/webdev-assistant.git`.

Ключевые правила:

- git publication commands выполнять только внутри `.agents`;
- не публиковать `project/**`, `upstream/**` и host-project files;
- коммитить publishable docs на local `.agents/main`;
- не пушить local `main` напрямую;
- перед publication branch делать `pull --rebase origin main`;
- создавать ветку `[fix|feat]-[description]`;
- открывать PR через GitHub connector;
- возвращать checkout на `main`.

### `technical-seo-app`

Используется для metadata, canonical URLs, robots, sitemap, crawlability,
Open Graph и structured data.

По умолчанию это audit-first skill: сначала report, затем fixes только если
пользователь явно попросил применить изменения.

### `frontend-security-inspector`

Используется для secrets, auth/session, public entry points, unsafe data,
environment exposure и client/server boundary risks.

По умолчанию это audit-first skill: сначала structured findings report, затем
remediation только по отдельному запросу.

### `screenshot-design-inspector`

Используется, когда design implementation начинается со screenshots или когда
Figma access недоступен.

Извлекает typography, spacing, colors, hierarchy, breakpoints и confidence
level. Screenshot-derived values считаются менее надежными, чем Figma data.

### `architecture-from-spec`

Используется, когда пользователь дает specification, technical assignment или
large refactor brief и хочет architecture guidance.

Сначала извлекает требования, затем предлагает recommended architecture path и
ограниченные alternatives без выдумывания недостающих constraints.

## Основные цепочки навыков

### Feature / refactor / bugfix

```text
webapp-task-protocol
-> nextjs-app-router и/или react-component-workflow
-> redux-state-workflow, если затронут shared state
-> frontend-typescript-rules, если затронуты типы
-> boundary-input-validation, если есть boundary input
-> frontend-review-and-fix
-> project-context-adapter, если изменился project context
```

### Review

```text
webapp-task-protocol
-> frontend-review-and-fix
```

Review начинается с findings: bugs, regressions, risks, missing tests. Summary
идет после findings.

### SEO

```text
technical-seo-app
```

Если пользователь просит только проверить, skill не применяет fixes. Если
пользователь просит применить, после report можно переходить к implementation.

### Security

```text
frontend-security-inspector
```

Security work начинается с structured report: severity, affected area, evidence,
remediation, follow-up verification.

### Design / Figma

```text
Figma capability
-> nextjs-app-router и/или react-component-workflow
-> screenshot-design-inspector, если Figma недоступна
```

Figma URL или design implementation request сначала идет через Figma capability.
Screenshots - fallback, не основной источник.

### Agent rules / skills / docs

```text
agent-rules-skill-author
-> readme-maintainer, если меняется README или user-facing workflow
-> webdev-assistant-sync, если нужен sync-down или publish-up
```

### Project onboarding

```text
project-onboarding-adapter
-> project-context-adapter, когда пользователь позже попросит выполнить план
-> agent-rules-skill-author, если plan audit нашел drift в reusable bundle docs
```

Этот workflow доступен только в Plan Mode. В обычном режиме агент не должен
читать весь проект или начинать адаптацию.

### Bundle sync / publication

```text
webdev-assistant-sync
```

Этот skill обслуживает nested `.agents` checkout и upstream PR workflow. Host
repo root не используется для upstream publication commands.

## Правила и запреты

### Общие запреты

- Не взаимодействовать с production systems, production data или live production
  environments.
- Не устанавливать packages и не менять shared tokens без явного approval.
- Не добавлять архитектуру, API contracts или behavior, которых нет в prompt или
  repo facts.
- Не делать unrelated refactors.
- Не дублировать существующие helpers/components/selectors/modules до поиска
  текущих решений.
- Не добавлять comments без запроса или реальной safety need.
- Не писать feature tests без явного запроса, если repo convention этого не
  требует.

### React / Next.js

- Не использовать `useEffect` для логики, которая может быть render-time,
  memoized или event-handler logic.
- Не использовать `useCallback` по умолчанию.
- Не использовать `void someFunc()`.
- Не использовать `let isCancelled = false`; prefer `AbortController`.
- Не строить JSX в `renderSomething` variables, если component extraction
  яснее.
- Не импортировать server-only modules в client code.
- Не fetch own route handlers из server-side code, если есть direct module
  call.

### TypeScript

- Не использовать `any`.
- Не использовать `@ts-ignore`, кроме явно обоснованных крайних случаев.
- Не делать unsafe double casts.
- Не клонировать параллельные types, если есть shared types/schemas/helpers.

### State management

- Не переносить local-only UI state в Redux/context/store без shared ownership.
- Не использовать Redux как transport layer или место тяжелой business logic.
- Не подписываться на broad store/context objects, если нужен узкий selector.
- Не возвращать fresh objects/arrays из non-memoized selectors без stability
  strategy.

### Documentation / `.agents`

- Не публиковать `.agents/project/**`.
- Не публиковать `upstream/**`.
- Не зеркалить `.agents/AGENTS.md` в host-root `AGENTS.md`.
- Не менять host-root `README.md`, если пользователь явно не попросил.
- Не добавлять `README.md`, `CHANGELOG.md`, `QUICK_REFERENCE.md` внутрь skill
  packages.
- Не смешивать host-project facts с reusable skills и common docs.
- Не удалять graph frontmatter из `.agents/**/*.md`; для `SKILL.md` не менять
  порядок первых полей `name` и `description`.
- Не помещать binding workflow-инструкции во frontmatter. Смысловые правила
  должны оставаться в body документа.

## Publishable и local-only paths

Publishable paths внутри checkout root `.agents/`:

```text
AGENTS.md
SUMMARY.md
common/**
skills/**
README.md
.gitignore
```

Local-only paths:

```text
project/**
upstream/**
.obsidian/**
application source code
tests
configs
build outputs
host-project files
```

Если файл не входит в publishable list, его нельзя включать в upstream PR.

## Sync-down и publish-up

### `sync-down`

Используется, чтобы подтянуть shared bundle из upstream в текущий принимающий
проект.

Основные правила:

- работать только во вложенном `.agents`;
- не трогать `project/**`;
- не менять host-root pointer без причины;
- после sync проверить Markdown и relevant docs.

### `publish-up`

Используется, чтобы опубликовать generic bundle changes upstream.

Порядок:

1. Убедиться, что `.agents/.git` существует.
2. Проверить remote `git@github.com:ytvee-dev/webdev-assistant.git`.
3. Проверить, что `origin/main` существует.
4. Проверить working tree и unmerged paths.
5. Работать на local `.agents/main`.
6. Stage only publishable paths.
7. Commit на local `main` с `fix(docs): ...` или `feat(docs): ...`.
8. Проверить, что eligible publishable changes не остались unstaged/staged.
9. `pull --rebase origin main`.
10. Создать ветку `[fix|feat]-[description]`.
11. Push branch.
12. Создать PR через GitHub connector.
13. Вернуть локальный checkout на `main`.

Local `.agents/main` напрямую не пушится.

## Неявные правила, которые агент слушает

### Skill selection prompt-driven

Пользователь не обязан писать `$skill-name`. Codex должен сам выбрать skill по
prompt, frontmatter `description`, repo context и touched area.

Явный вызов полезен, когда нужно снять неопределенность:

```text
$webapp-task-protocol реализуй feature ...
$technical-seo-app проверь metadata ...
$frontend-security-inspector проведи security audit ...
$agent-rules-skill-author создай skill ...
$project-onboarding-adapter адаптируйся ...
$webdev-assistant-sync publish-up ...
```

### Indexes before broad search

Если существуют path indexes, агент сначала читает их:

- route/layout/metadata work -> `.agents/project/next/path-index.md`;
- component/hooks/client UI work -> `.agents/project/react/path-index.md`;
- stack facts -> `.agents/project/stack-profile.md`;
- architecture/data flow -> `.agents/project/architecture-map.md`;
- styling -> `.agents/project/styling-profile.md`;
- verification -> `.agents/project/verification-profile.md`.

Широкий repo search используется после targeted docs и indexes.

### Project overlays refresh

Если реализация изменила routes, components, helpers, styling tokens,
verification commands или project structure, агент должен проверить, нужно ли
обновить `.agents/project/**`. Пользователь не обязан просить это отдельно.

### Audit skills report-first

SEO и security skills сначала дают report. Они не должны автоматически
применять изменения, если пользователь попросил только проверить.

### Figma first, screenshots fallback

Если prompt содержит Figma URL или design implementation request, сначала
используется Figma capability. Если Figma недоступна, агент просит screenshots
и подключает `screenshot-design-inspector`.

### Official docs for changing external behavior

Если задача зависит от текущего поведения OpenAI, Next.js, Vercel, GitHub,
Figma или другой внешней системы, агент должен свериться с официальной
документацией или configured docs MCP, а не полагаться на память.

## Как управлять skills

### Когда создавать новый skill

Новый skill нужен, если у задачи есть:

- отдельный trigger surface;
- отдельный reusable workflow;
- повторяемые constraints;
- набор references/scripts/assets, который будет использоваться многократно.

Новый skill не нужен, если достаточно:

- уточнить trigger существующего skill;
- добавить missing rule;
- обновить reference;
- добавить project-specific fact в `.agents/project/**`;
- добавить reusable rule в `.agents/common/**`.

### Что писать в `SKILL.md`

Frontmatter:

```yaml
---
name: skill-name
description: Use when ...
---
```

Правила:

- `name` - lowercase hyphen-case;
- `description` - основной trigger surface;
- в `description` должны быть user intent, verbs, artifacts и граница
  применения;
- `description` должна быть плотной и front-loaded, потому что участвует в
  initial skills list budget Codex;
- для trigger quality нужны realistic should-trigger и near-miss
  should-not-trigger prompts;
- после `description` должны идти graph metadata fields и связи с owning docs,
  references/assets и related workflows;
- body должен быть procedural: purpose, context, workflow, rules, validation,
  reference map;
- body не должен переобъяснять весь домен.

### Что писать в `references/`

`references/` подходит для:

- длинных checklist;
- detailed examples;
- variants;
- schemas/API notes;
- source-backed guidance;
- quality rubrics.

Reference должен быть связан из `SKILL.md`, иначе агент может о нем не узнать.

### Когда добавлять `scripts/`

`scripts/` нужен, когда workflow:

- повторяемый;
- хрупкий;
- требует deterministic output;
- часто переписывается вручную;
- удобнее проверяется командой.

Если одни и те же workflow evals стабильно приводят к одинаковой helper work,
это аргумент за `scripts/`. Если выгода не повторяется, лучше оставить skill
instruction-only.

Скрипты должны быть неинтерактивными, давать понятные ошибки и иметь понятный
интерфейс запуска.

### Когда добавлять `assets/`

`assets/` нужен для шаблонов и ресурсов, которые агент использует в output:

- starter files;
- templates;
- images/icons/fonts;
- structured boilerplate.

Инструкции, которые агент должен читать, не должны жить только в `assets/`.

### Что писать в `agents/openai.yaml`

Фактический формат в этом bundle:

```yaml
interface:
  display_name: 'Human Readable Skill Name'
  short_description: 'Short workflow description'
  default_prompt: 'Use $skill-name to ...'
policy:
  allow_implicit_invocation: true
```

`allow_implicit_invocation: true` означает, что skill может включаться по user
intent без явного `$skill-name`. Если поставить `false`, skill остается доступен
для явного вызова, но не должен выбираться автоматически.

`agents/openai.yaml` нужно обновлять вместе с `SKILL.md`, если меняется trigger,
scope или default prompt.

## Maintenance checklist

### Перед изменением кода

1. Прочитать root `AGENTS.md`.
2. Прочитать `.agents/AGENTS.md`.
3. Прочитать `.agents/SUMMARY.md`.
4. Выбрать relevant skill.
5. Прочитать relevant common docs и project overlays.
6. Прочитать affected source/config files.
7. Сделать минимальную scoped правку.
8. Запустить relevant verification.
9. Проверить, нужны ли updates в `.agents/project/**`.

### Перед изменением `.agents` docs

1. Выбрать слой: `AGENTS.md`, `common/**`, `project/**`, `skills/**`,
   `README.md`.
2. Проверить соседние rules и skill chains.
3. Не смешивать reusable docs и project facts.
4. Обновить cross-links и `SUMMARY.md`, если изменилась структура или routing.
5. Обновить README, если изменились user-facing workflow, paths, skill list или
   publication rules.
6. Обновить graph frontmatter и Obsidian wikilinks для changed Markdown files.
7. Проверить, что frontmatter не содержит workflow вместо body-инструкций.
8. Запустить Markdown/Prettier check.

### Перед публикацией upstream

1. Работать только внутри `.agents`.
2. Убедиться, что `project/**` не staged.
3. Commit publishable docs на local `main`.
4. Не пушить local `main`.
5. Rebase на `origin/main`.
6. Создать `fix-*` или `feat-*` branch.
7. Push branch.
8. Создать PR через GitHub connector.
9. Вернуться на local `main`.

## Как поддерживать этот README

README должен быть подробным техническим справочником по bundle, если он
отвечает на вопросы:

- что такое `.agents`;
- какие правила и skills есть;
- как Codex выбирает инструкции;
- что настроить в VS Code;
- какие paths publishable/local-only;
- как делать sync и publication;
- какие запреты важно знать до работы.

README не должен содержать:

- host-project facts;
- маркетинговый текст;
- историю изменений;
- дословную копию всех references;
- инструкции для не-Codex агентных систем;
- публикацию local-only paths.

Если меняются skill list, routing, sync/publication policy, canonical path,
README должен обновляться в той же задаче.
