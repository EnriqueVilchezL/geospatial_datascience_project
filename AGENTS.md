# AGENTS.md

## Setup commands
- Install deps: `uv sync`
- Start dev server: `uv run src/app.py`
- add depencies to project: `uvx add <package-name>`

## Development
- lint and check after changes: `uvx ruff format .` and `uvx ruff check --fix .` 
- type check: `uvx pyrefly check .` 

## Code style
- dry, clean, solid. Type hints always using modern syntax (e.g. list[int], not List[int])
- trailing commas always for readability
- named parameters for functions with more than 1 parameter
- prefer match-case instead of if elses when it makes sense and it is cleaner, that includes type checking.