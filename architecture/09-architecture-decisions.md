# 9. Architecture Decisions

This chapter records the architectural decisions made for BankOCR as Architecture Decision Records (ADRs). Each ADR documents the context, the decision taken, the rationale, and the consequences.

ADRs are append-only. An accepted ADR is never overwritten; superseded decisions are marked accordingly and a new ADR records the replacement (OC-3).

---

## ADR-001: Technology Choices for BankOCR

### Status
Accepted

### Context
The BankOCR system needs to read account numbers represented as ASCII characters, recognize digits, validate account numbers using a checksum, and generate processing results.

The solution should be simple, maintainable, and easy to test. The architecture should also support future extensions.

### Decision
The following technology and architecture choices have been made:

- **Programming language:** Python 3.
- **Framework:** No external framework is required; Python's standard library will be used.
- **Architecture:** A modular application with three main components:
  - Parser – converts ASCII representations into digits.
  - Validator – verifies account numbers using checksum rules.
  - Processor – coordinates processing and generates results.
- **Data storage:** Input and output will use plain-text files. No database is required.
- **Testing:** Python's built-in `unittest` framework will be used.
- **Diagrams:** PlantUML with the C4 model will be used to document the architecture.

### Rationale
Python provides readable syntax and built-in support for text processing, making it suitable for BankOCR.

A modular architecture separates responsibilities and allows individual components to be tested independently.

Using plain-text files avoids unnecessary database complexity.

### Consequences
**Positive:**
- Simple implementation and maintenance.
- Easy testing of individual components.
- Minimal external dependencies.
- Clear separation of responsibilities.

**Negative:**
- The system is initially designed for local execution.
- Additional development would be required to support a web interface or distributed processing.

---

## ADR-002: File I/O Confined to the Processor

### Status
Accepted

### Context
BankOCR has three internal components: Parser, Validator, and Processor. An early design question is which component or components should be responsible for reading the input file and writing the output file.

Placing file I/O in the Parser or Validator would couple those components to the file system, making them harder to test in isolation and harder to reuse if the input source ever changed (e.g. reading from a string buffer in tests).

### Decision
File I/O is confined exclusively to the Processor. The Parser receives a pre-sliced four-line account entry as a string argument and returns a nine-character account string. The Validator receives a nine-character account string and returns a status value. Neither the Parser nor the Validator reads from or writes to the file system directly.

### Rationale
Isolating file I/O in the Processor means the Parser and Validator can be tested by passing string literals directly, with no file fixtures, temporary directories, or mock objects. This is the simplest way to satisfy the testability quality goal (Chapter 1, priority 2) while keeping each component's responsibility focused.

It also means that if the input source changes in the future (e.g. reading from stdin or a string buffer), only the Processor needs to change.

### Consequences
**Positive:**
- Parser and Validator are independently testable with plain string inputs.
- The file I/O boundary is explicit and enforced by component design.
- Changes to input or output format are localised to the Processor.

**Negative:**
- The Processor carries more responsibility than the other two components, as it owns coordination, file reading, entry slicing, and file writing.
