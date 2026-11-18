# 9. Architecture Decisions

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
