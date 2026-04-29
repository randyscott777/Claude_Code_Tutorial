---
description: Find unreferenced Python code (functions, classes, imports, variables) using vulture
argument-hint: "[path]  (optional; defaults to repo root)"
---

Find dead code in the Python project.

**Scope:** `$ARGUMENTS` if provided, otherwise the repo root.

## Steps

1. Check that `vulture` is installed (`python -m vulture --version`). If it isn't, tell the user and offer to install it with `pip install vulture` — wait for confirmation before installing.
2. Run vulture on the scope with these exclusions, combining them into a single `--exclude` argument:
   - `*/migrations/*`
   - `*/__pycache__/*`
   - `*/.venv/*,*/venv/*`
   - `*/node_modules/*`
   - `*/tests/*,*/test_*.py`
   - `*/buildozer.spec,*/build/*,*/dist/*`
   - Use `--min-confidence 80` to cut noise.

   Example: `python -m vulture <scope> --exclude "*/migrations/*,*/__pycache__/*,*/.venv/*,*/venv/*,*/node_modules/*,*/tests/*,*/test_*.py,*/build/*,*/dist/*" --min-confidence 80`

3. Parse the output and group findings by category: unused functions, unused classes, unused imports, unused variables, unreachable code. Present as a compact table with `file:line` references.

4. For each finding, apply judgment before suggesting removal:
   - **Django views / URL handlers**: referenced by string in `urls.py`, not by import — do NOT flag as dead.
   - **Click commands / Flask routes**: registered via decorators — do NOT flag as dead.
   - **`__init__.py` re-exports**: may be intentional public API — flag but don't auto-remove.
   - **Test fixtures, `conftest.py`**: framework-loaded — skip.
   - **Dunder methods** (`__str__`, `__repr__`, etc.): called implicitly — skip.

5. Report findings as a prioritized list:
   - **Safe to remove** (high confidence, no framework hooks)
   - **Review first** (medium confidence or framework-adjacent)
   - **Ignore** (false positives, with one-line reason)

6. Ask the user which group (or specific items) to remove. **Do not delete anything without explicit confirmation** — per project convention, delete operations always require a prompt.

7. After removal, run `python -m py_compile` on each touched file to catch syntax errors, and run `python menu.py --help` or the affected app's entry point if one exists to smoke-test.

## Notes
- If `vulture` reports many low-confidence hits, suggest tightening `--min-confidence` rather than wading through noise.
- For non-Python projects or mixed-language trees, tell the user this command only covers Python and suggest a language-specific tool.
