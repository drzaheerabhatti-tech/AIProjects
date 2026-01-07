# Friction Log (Cohere demos)

> This document captures setup and API friction encountered during development,
> along with resolutions and preventative notes. It is included for transparency
> and future reference.

**Goal:** Record setup and API friction along with fixes, so future work can recover quickly and avoid repeat issues.

---

## 2026-01-07 — Generate API removed (404)

**Symptom**
- Calling `co.generate(...)` fails with:
Generate API was removed on September 15 2025

**Root cause**
- Cohere removed the legacy Generate endpoint in favor of the Chat API.

**Fix**
- Migrated from `co.generate()` to `co.chat()` using the Chat API.

**Prevention**
- Review Cohere quickstarts and deprecation notices before implementing new examples.

---

## 2026-01-07 — SyntaxError while migrating to Chat API

**Symptom**
- Python error:
SyntaxError: invalid syntax. Perhaps you forgot a comma?

near the `messages=[...]` block.

**Root cause**
- List/dictionary syntax error introduced during manual edits.

**Fix**
- Replaced the file with a minimal, known-good Chat API example and re-ran incrementally.

**Prevention**
- Make small edits and execute after each change to catch syntax issues early.

---

## 2026-01-07 — Model `command` removed (404)

**Symptom**
- Error:
NotFoundError: model 'command' was removed on September 15, 2025

**Root cause**
- The `command` model was deprecated and removed; snapshot models must be used instead.

**Fix**
- Updated the example to use a supported snapshot model:
- `command-a-03-2025` (recommended)
- `command-r-08-2024`
- `command-r-plus-08-2024`

**Prevention**
- Verify supported models in the Cohere model catalog before hardcoding model IDs.

---

## 2026-01-07 — VS Code shows “Import cohere could not be resolved” (Pylance)

**Symptom**
- VS Code reports:
Import "cohere" could not be resolved

**Root cause**
- VS Code Python interpreter was not set to the project’s virtual environment.

**Fix**
- VS Code → Command Palette → **Python: Select Interpreter** → select `.venv`.

**Prevention**
- Always select the correct interpreter immediately after creating a virtual environment.

---

## 2026-01-07 — Chat response printed no output

**Symptom**
- Script executed without errors but printed no output.

**Root cause**
- Typo when parsing content blocks (`block.test` instead of `block.text`), causing all blocks to be filtered out.

**Fix**
- Corrected attribute name and added explicit inspection of `response.message.content`.

**Prevention**
- Inspect structured responses (`type()`, `dir()`, raw prints) when parsing SDK objects for the first time.

---

## Key Takeaways

- Modern LLM APIs return **structured responses**, not plain strings.
- API and model lifecycles change frequently; code must adapt.
- Defensive parsing (`hasattr`, type checks) improves robustness.
- Capturing friction reduces future setup and debugging time.
