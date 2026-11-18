# 4. Solution Strategy

This chapter explains the key architectural choices that shape BankOCR and how those choices support the quality goals established in Chapter 1.

---

## 4.1 Overall Approach

BankOCR is implemented as a single Python 3 command-line application. There is no server, no network interface, and no database. The application reads an input file, processes every account entry in sequence, and writes a results file. This matches the problem scope exactly and avoids infrastructure complexity that the kata does not require (ADR-001, OC-1).

---

## 4.2 Modular Component Structure

Responsibility is divided across three components that operate in a fixed pipeline:

| Component | Responsibility |
|-----------|---------------|
| **Parser** | Receives a four-line ASCII account entry and converts each 3×3 glyph into a digit character. Produces a nine-character account string, using a placeholder for any glyph it cannot recognise. Has no dependency on file I/O. |
| **Validator** | Receives a nine-character account string from the Parser and applies the mod-11 checksum (`d9 + 2·d8 + … + 9·d1 ≡ 0 mod 11`). Returns a status of `VALID`, `ERR`, or `ILL`. Has no dependency on file I/O. |
| **Processor** | Reads the input file, splits it into individual entries, passes each entry to the Parser, passes each parsed string to the Validator, and writes the annotated results file. |

Each component has a single, well-defined responsibility. The Processor depends on the Parser and Validator, but the Parser and Validator are independent of each other and of file I/O, which keeps them straightforward to test in isolation.

---

## 4.3 Processing Strategy

The application processes account entries one at a time in the order they appear in the input file. For each entry the pipeline is:

1. **Parse** — the Processor passes the four-line entry to the Parser, which maps each glyph to a digit and returns a nine-character string.
2. **Validate** — determine whether the nine-digit string is valid, erroneous, or illegible.
3. **Record** — write one result line to the output file, appending ` ERR` or ` ILL` where applicable.

Sequential, single-pass processing is sufficient for the problem size and keeps the control flow easy to follow and test.

---

## 4.4 Technology Rationale

| Choice | Rationale |
|--------|-----------|
| **Python 3 (≥ 3.12)** | Readable syntax and strong built-in support for text processing make it a natural fit for glyph recognition and string manipulation. |
| **Standard library only** | The problem requires no capabilities beyond what Python provides. Eliminating external dependencies reduces setup friction and removes a category of maintenance risk. |
| **Plain-text files** | The kata specifies a fixed text format. Using files directly — without a database or serialisation layer — is the simplest correct implementation. |
| **`unittest`** | Built into Python, requiring no additional installation. Sufficient for testing each component independently with straightforward arrange-act-assert tests. |

---

## 4.5 How the Strategy Supports the Quality Goals

| Quality goal (Chapter 1) | How the strategy addresses it |
|--------------------------|-------------------------------|
| **Correctness** | The Parser maps each glyph deterministically; the Validator applies the checksum formula exactly as specified. The `ILL` and `ERR` paths are explicit branches, not implicit fallbacks. |
| **Testability** | Parser and Validator have no dependency on file I/O or on each other, so each can be tested with direct inputs and no test fixtures beyond simple strings. |
| **Maintainability** | Each component has one responsibility. Changing digit recognition does not touch validation logic, and changing output formatting does not touch parsing. |
| **Simplicity** | The single-process, file-in/file-out design contains no moving parts beyond what the kata requires. There is nothing to deploy, configure, or operate beyond running the script. |
