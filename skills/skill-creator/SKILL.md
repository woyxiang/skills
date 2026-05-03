---
name: skill-creator
description: 'Create new skills for AI agents. Use when: (1) User asks to create a skill for a language, tool, or framework, (2) A new skill needs to be bootstrapped from scratch, (3) An existing skill needs a new capability (doc, script, agent), (4) You need to understand the skill authoring workflow'
---

# Skill Creator

Builds structured skills for AI agents following a consistent pattern.

## Core Principle

A skill is a **bundled, routing-based knowledge system**. The agent doesn't navigate a folder tree — it follows routes from a single entry point. Dead content is worse than no content: every file must be registered in the routing table or it won't be found.

## Lifecycle

Every new skill follows this path:

```
1. Bootstrap    → Create repo structure, write SKILL.md skeleton
2. Add docs     → Create *.md reference docs, register in SKILL.md routing
3. Add scripts  → Create tools under scripts/, reference from docs (optional)
4. Add agents   → Create specialized agents under agents/ (optional)
5. Validate     → Run structure tests
```

Not every skill needs scripts or agents. Start with docs only.

## Bootstrap a New Skill

### Step 1 — Define the Skill

Answer these before writing any code:

| Question | Example |
| --- | --- |
| What is the name? | `python`, `terraform`, `docker` |
| What triggers it? | File extensions, keywords, file patterns |
| What do users want to do? | Write code, debug, manage config |
| What scripts are needed? | Search, validation, code generation |
| What agents are needed? | verify, lint, build |

### Step 2 — Create Directory Structure

```
skills/<name>/
├── SKILL.md           # Entry point (required)
├── *.md               # Reference docs (at least basics.md)
├── agents/            # Specialized agents (optional)
├── scripts/           # Tool scripts (optional)
├── data/              # Embedded indexes (optional)
└── examples/          # Runnable examples (optional)
```

**Important**: The `skills/<name>/` directory is the bundle. Everything outside it is development infrastructure.

### Step 3 — Write SKILL.md

SKILL.md must have:

- `---` frontmatter with `name` and `description`
- Detection section (what triggers this skill)
- Routing table (which doc to read for what task)
- Dependencies list
- Script usage (if any scripts exist)

### Step 4 — Add Reference Docs

For each doc:
1. Create `skills/<name>/<topic>.md`
2. Start with a cross-reference line
3. Lead with patterns, not prose
4. Add entry to SKILL.md routing table

### Step 5 — Add Scripts (optional)

Scripts go in `scripts/`. Requirements:

| Requirement | Reason |
|---|---|
| Python 3.10+ | Matches toolchain baseline |
| `argparse` with `--help` | Agents need to call them |
| `--json` for structured output | Agents parse machine output better |
| Exit 0 on success, non-zero on failure | Script exit codes are meaningful |
| Data embedded in `data/` | Offline, deterministic |

### Step 6 — Validate

Run the structure validator:
```bash
python tests/test_structure.py
```

Every `.md` file must be registered in SKILL.md routing table.

## SKILL.md Template

~~~markdown
---
name: <name>
description: 'One-line description. Use when: (1) trigger conditions, (2) file patterns, (3) user intent'
---

# <Name>

## Detection

What activates this skill?

**File patterns:** `*.ext`, `*.config`
**Keywords:** `import`, `function`, `task`
**Commands:** `build`, `deploy`, `init`

## Routing

| When you need to... | Read |
|---|---|
| Get started | [basics.md](basics.md) |
| Configure | [config.md](config.md) |
| Common tasks | [tasks.md](tasks.md) |

## Dependencies

Required tools and how to install them.

## Script Usage (optional)

```bash
python scripts/search.py "query"
```

## Examples (optional)

| Example | Description |
|---|---|
| [example.ext](examples/example.ext) | ... |
~~~

## Writing Reference Docs (*.md)

Rules for `.md` files inside `skills/<name>/`:

1. **First line**: Cross-reference to sibling docs
2. **Lead with pattern, not explanation**: Show code first, explain after
3. **Tables over prose**: Agents parse structure better
4. **Code blocks use correct fencing**: ` ```<lang> ` for code, ` ```bash ` for shell
5. **Code examples should compile**: If snippet, say so

## Writing Agents

When a task needs a specialized agent, create `agents/<name>-<task>.md`:

```markdown
---
name: <name>-<task>
description: 'What this agent does. Use when: trigger conditions'
model: claude-sonnet-4-6
---

You are a <task> agent for <name>. [Detailed system prompt...]
```

## Script Path Management

When scripts live inside `skills/<name>/scripts/`:

```python
from pathlib import Path

base_dir = Path(__file__).parent.parent  # → skills/<name>
data_dir = base_dir / "data"
# For upstream docs at repo root:
upstream_dir = base_dir.parent / "references" / "docs"
```

Use `parent.parent` (not `parent.parent.parent`). Rule: scripts are at `skills/<name>/scripts/`.

## Building Search Indexes from Upstream Docs

If upstream docs are HTML, you can parse them to build a search index:

### extract-api.py Pattern

1. **Scan for keyword files** — glob pattern depends on naming convention
2. **Parse HTML structure** — find predictable sections (title, syntax, params, examples)
3. **Handle complex names** — some keywords have special characters `(Print | ?)`, must be looked up exactly
4. **Build api.json** with: name, category, syntax, description, parameters, examples, see_also

### BM25 Index

```python
K1 = 1.5   # term frequency saturation
B = 0.75   # document length normalization
WEIGHTS = {'name': 3.0, 'syntax': 2.0, 'description': 1.0}
```

Field weights: `name` at 3x because exact matches should rank highest.

### Search Script Interface

```bash
python scripts/search.py "query" --top 5      # ranked search
python scripts/search.py --name "keyword"    # exact lookup
python scripts/search.py "query" --json       # structured output
```

### Encoding Safety

Windows console may use GBK. Always clean text output:

```python
def clean_text(text: str) -> str:
    return text.replace('\xa0', ' ').replace('​', '')
```

## Detection Patterns by Type

| Type | Detection Markers |
|---|---|
| Compiled language | File extensions, block endings (`End Function`), metacommands (`$Dynamic`) |
| Interpreted / Script | Shebang (`#!/...`), REPL commands |
| Config / Infrastructure | File patterns (`*.tf`, `*.yaml`), resource types |

Do not assume shebang — many compiled languages don't have it.

## Routing Table Enforcement

**Every new file MUST be registered in SKILL.md's routing table.**

A doc not in the routing table is invisible to agents. Test `tests/test_structure.py` enforces this.

Pattern:
- New `.md` doc → add row in routing table
- New script → document in "Script Usage"
- New agent → document which docs reference it

## Commit Style

Imperative mood, lowercase, no period. Scope prefix.

```
skill: bootstrap <name> structure
docs: add basics.md and config.md
scripts: add search with embedded index
agent: add <name>-verify agent
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| SKILL.md missing frontmatter | Must start with `--- name: ... ---` |
| Doc not in routing table | Add entry before finishing doc |
| Script paths use `parent.parent.parent` | Scripts are at `skills/<name>/scripts/`, use `parent.parent` |
| Forgetting `--json` flag | Agents parse structured output better |
| Forgetting encoding clean | Windows GBK + UTF-8 content = broken output |