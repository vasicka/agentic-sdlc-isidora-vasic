# 2. Architecture Constraints

Constraints are conditions the architecture must satisfy regardless of design preference. They are separated here from architectural decisions, which are deliberate choices made within those constraints and documented in [ADR-001](./09-architecture-decisions.md).

---

## 2.1 Technical Constraints

### Externally imposed

These constraints come from outside the project's design process and cannot be changed without altering the project setup or kata specification.

| ID | Constraint | Source |
|----|-----------|--------|
| TC-1 | The application must be implemented in **Python 3** (≥ 3.12). | `pyproject.toml` |
| TC-2 | The input file format is fixed: each account entry occupies exactly **four lines** (three glyph rows of 27 characters each, followed by one blank line). | Kata specification |

### Accepted project decisions

These are technology choices made in ADR-001. They are not externally imposed and could be revisited through a new ADR.

| ID | Constraint | Source |
|----|-----------|--------|
| TC-3 | Only **Python's standard library** may be used as a runtime dependency. No third-party packages are permitted. | ADR-001 |
| TC-4 | Input and output must use **plain-text files**. No database or binary format is involved. | ADR-001 |
| TC-5 | Tests must be written using Python's built-in **`unittest`** framework. No external test runner is required. | ADR-001 |

---

## 2.2 Organisational Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| OC-1 | The system solves the **Bank OCR kata** as defined at [codingdojo.org/kata/BankOCR](https://codingdojo.org/kata/BankOCR/). Requirements must not be extended beyond the kata scope without explicit approval. | Project context |
| OC-2 | Architecture documentation must follow the **arc42** structure and use the **C4 model** with PlantUML for diagrams. | Project conventions |
| OC-3 | Architectural decisions must be recorded as **ADRs** in `architecture/09-architecture-decisions.md` and must not be overwritten once accepted. | Project conventions |

---

## 2.3 Architectural Decisions Distinct from Constraints

The following are deliberate design choices made within the constraints above. They are not externally imposed and could have been decided differently. They are recorded in ADR-001 and listed here for clarity.

| Decision | Rationale (summary) |
|----------|---------------------|
| Modular structure with three components: Parser, Validator, Processor | Separates concerns and enables independent unit testing |
| Single deployable unit (CLI application) | The problem scope does not justify splitting into separate processes or services |
| No web interface or distributed processing | Outside kata scope; would add unjustified complexity |
