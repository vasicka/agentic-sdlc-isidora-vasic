# 1. Introduction and Goals

## 1.1 Requirements Overview

BankOCR is a Python 3 command-line application that solves the [Bank OCR kata](https://codingdojo.org/kata/BankOCR/). It reads plain-text files containing ASCII representations of bank account numbers, recognises the individual digits, validates the nine-digit numbers against a checksum rule, and writes the results to output.

### Functional requirements

| ID | Requirement |
|----|-------------|
| FR-1 | Read an input file whose lines encode digits as 3-row × 3-column ASCII glyphs. Each entry occupies four lines (three glyph rows plus one blank separator). |
| FR-2 | Parse each glyph and map it to the corresponding decimal digit (0–9). |
| FR-3 | Assemble nine consecutive glyphs into a nine-digit account number. |
| FR-4 | Validate each account number using the checksum rule: `d9 + 2·d8 + 3·d7 + … + 9·d1 ≡ 0 (mod 11)`. |
| FR-5 | Mark an account number as illegible (`ILL`) when one or more glyphs cannot be matched to a known digit. |
| FR-6 | Mark a syntactically valid but checksum-failing account number as erroneous (`ERR`). |
| FR-7 | Write one result line per account number to an output file, appending `ERR` or `ILL` where applicable and leaving the line bare for valid numbers. |

### Out of scope

- Web or network interfaces.
- Database storage.
- External framework dependencies beyond Python's standard library.

These boundaries are established by ADR-001.

---

## 1.2 Quality Goals

The following quality goals drive the architecture. They are ordered by priority.

| Priority | Quality attribute | Scenario |
|----------|------------------|----------|
| 1 | **Correctness** | Every digit, checksum calculation, and status tag (`ERR`, `ILL`) must match the kata specification exactly. A wrong result is a silent data-integrity failure. |
| 2 | **Testability** | Each component (Parser, Validator, Processor) must be exercisable in isolation with `unittest` and without file I/O, so defects are pinpointed quickly. |
| 3 | **Maintainability** | A developer unfamiliar with the codebase should be able to locate, understand, and change a component without touching the others. Clear interfaces and explicit error handling are required. |
| 4 | **Simplicity** | The solution must not introduce dependencies, infrastructure, or design patterns that are not justified by an explicit requirement. |

---

## 1.3 Stakeholders

| Stakeholder | Role | Primary interest |
|-------------|------|-----------------|
| Developer | Implements and maintains the system | Clear component boundaries, testable design, readable code |
| Instructor / Reviewer | Evaluates the kata solution | Correctness, adherence to kata rules, clean architecture |
| User | Submits ASCII account number files and receives validation results | Correct recognition and validation of every account number |
