# PARSING Domain – User Story Bundles

## Domain Overview

**Domain:** PARSING
**Architecture component:** Parser
**Responsibility:** Recognize ASCII digit glyphs and assemble nine-digit account numbers.

**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-2, FR-3)
- `architecture/05-building-block-view.md`, Section 5.2 (Parser component)
- `architecture/02-constraints.md`, Section 2.1 (TC-2, TC-3)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Testability conventions)

---

## PARSING-STORY-001 – Recognise ASCII Digits and Assemble Account Numbers

**Domain:** PARSING
**Story ID:** PARSING-STORY-001
**Title:** Recognise ASCII digits and assemble account numbers
**Priority:** CORE
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-2, FR-3)
- `architecture/04-solution-strategy.md`, Section 4.2 (Parser responsibility)
- `architecture/05-building-block-view.md`, Section 5.2 (Parser component, dependency rules)
- `architecture/06-runtime-view.md`, Section 6.1 (Steps 3–4, Scenario 1)
- `architecture/08-crosscutting-concepts.md`, Sections 8.2, 8.3
- `architecture/10-quality-requirements.md`, QS-01, QS-05

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to recognize ASCII digit representations and assemble them into a nine-digit account number,
**SO THAT** my account numbers can be processed and validated automatically.

---

### Acceptance Scenarios

### SCENARIO 1: Recognise a valid account entry
**Scenario ID:** PARSING-STORY-001-S001
**GIVEN** an account entry containing nine recognisable ASCII digit glyphs arranged in three rows of 27 characters each
**WHEN** the Parser processes the entry
**THEN** it returns a nine-character string containing the corresponding decimal digits in their original order

### SCENARIO 2: Preserve leading zeros
**Scenario ID:** PARSING-STORY-001-S002
**GIVEN** an account entry representing an account number that begins with one or more zeros
**WHEN** the Parser processes the entry
**THEN** the returned account string contains exactly nine characters and preserves all leading zeros

### SCENARIO 3: Recognise all ten supported digits
**Scenario ID:** PARSING-STORY-001-S003
**GIVEN** correctly formed ASCII representations of each digit 0 through 9 placed individually in a valid four-line account entry
**WHEN** each representation is processed by the Parser
**THEN** every glyph is mapped to its corresponding decimal digit without error

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3).

---

### Backend Stories

#### PARSING-BE-001.1 – Implement ASCII glyph-to-digit mapping

**Story ID:** PARSING-BE-001.1
**Parent story:** PARSING-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Parser responsibility)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (placeholder convention)
- `architecture/10-quality-requirements.md`, QS-01

**AS A** BankOCR developer,
**I WANT** the Parser to map each standard 3×3 ASCII glyph to its decimal digit,
**SO THAT** account entries can be converted into decimal strings for downstream validation.

#### Acceptance Scenarios

### SCENARIO 1: Map a single recognised glyph to its digit
**Scenario ID:** PARSING-BE-001.1-S001
**GIVEN** a valid 3×3 ASCII glyph representing one of the digits 0 through 9
**WHEN** the Parser compares the glyph against the supported digit patterns
**THEN** it returns the correct single decimal character for that digit

### SCENARIO 2: Map all nine glyphs in a complete entry
**Scenario ID:** PARSING-BE-001.1-S002
**GIVEN** a complete four-line account entry containing nine recognisable glyphs
**WHEN** the Parser processes the entire entry
**THEN** it returns exactly nine decimal characters in the same left-to-right order as the glyphs appear in the entry

### SCENARIO 3: Preserve leading zeros in the returned string
**Scenario ID:** PARSING-BE-001.1-S003
**GIVEN** an account entry whose leftmost glyph represents the digit zero
**WHEN** the Parser converts the glyphs to an account string
**THEN** the first character of the returned nine-character string is `'0'` and no digit is dropped or shifted

---

### Infrastructure Stories

#### PARSING-INFRA-001.1 – Execute Parser tests in Docker container using pytest

**Story ID:** PARSING-INFRA-001.1
**Parent story:** PARSING-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5) – Note: TC-5 specifies `unittest` but Docker uses `pytest`
- `architecture/05-building-block-view.md`, Section 5.2 (Dependency rules: Parser has no file-system dependency)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Parser testability convention)
- `architecture/10-quality-requirements.md`, QS-05, QS-07
- Dockerfile (local Docker-based environment established in Module 4)
- CI workflow (`.github/workflows/ci.yml`)

**AS A** BankOCR developer,
**I WANT** the Parser to be exercisable in complete isolation within a Docker container using `pytest`,
**SO THAT** digit recognition defects are pinpointed immediately in the local Docker-based test environment.

> **Note:** This story reflects the local Docker-based environment established in Module 4. TC-5 specifies `unittest`, but the Docker setup uses `pytest` for testing. `pytest` is a test dependency, not a runtime dependency, so it does not violate TC-3 (standard library only for runtime).
>
> **QS-07 clarification:** The original QS-7 requirement specifies that tests should run with no external dependencies on a machine with only Python ≥ 3.12. The Module 4 Docker/pytest setup introduces `pytest` as a third-party test dependency, which creates a discrepancy with the original QS-7 requirement. `pytest` is a test-only dependency and does not affect runtime execution, but it does mean the full test suite cannot run with zero external dependencies as originally specified in QS-7.

#### Acceptance Scenarios

### SCENARIO 1: Build Docker image for Parser testing
**Scenario ID:** PARSING-INFRA-001.1-S001
**GIVEN** the BankOCR source code with its Dockerfile and test dependencies configuration
**WHEN** the Docker image is built with `docker build -t kata-tests .`
**THEN** the build completes successfully, installing Python 3.12 and test dependencies including pytest

### SCENARIO 2: Execute Parser tests inside Docker container
**Scenario ID:** PARSING-INFRA-001.1-S002
**GIVEN** the built Docker image containing the BankOCR source and test suite
**WHEN** tests are executed with `docker run --rm kata-tests` (default CMD runs pytest)
**THEN** the Parser tests run inside the container with no external file system dependencies and produce test results

### SCENARIO 3: Pass raw multi-line string directly to Parser without file I/O
**Scenario ID:** PARSING-INFRA-001.1-S003
**GIVEN** a pytest test case that constructs a valid four-line account entry as a Python string literal
**WHEN** that string is passed directly to the Parser inside the Docker container
**THEN** the Parser returns the expected nine-character account string and no file is read from or written to the file system

### SCENARIO 4: Parser tests require no file fixtures when running in Docker
**Scenario ID:** PARSING-INFRA-001.1-S004
**GIVEN** the full Parser test suite executed inside Docker
**WHEN** the test suite runs
**THEN** no test creates, reads, or deletes a file on the host file system, and no temporary directory is mounted or required

---

#### PARSING-INFRA-001.2 – Deploy the Parser as part of the single-file CLI application in Docker environment

**Story ID:** PARSING-INFRA-001.2
**Parent story:** PARSING-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3)
- `architecture/04-solution-strategy.md`, Section 4.1 (single CLI application)
- `architecture/07-deployment-view.md`, Sections 7.1, 7.2, 7.3 – Note: Deployment view doesn't mention Docker
- `architecture/10-quality-requirements.md`, QS-10, QS-11
- Dockerfile (local Docker-based environment)

**AS A** BankOCR developer,
**I WANT** the Parser to be packaged as part of the single Python CLI application within a Docker container,
**SO THAT** the application can be invoked through Docker on any machine with Docker installed, without requiring Python ≥ 3.12 on the host.

#### Acceptance Scenarios

### SCENARIO 1: Docker image contains the complete application with Parser
**Scenario ID:** PARSING-INFRA-001.2-S001
**GIVEN** the built Docker image `kata-tests`
**WHEN** the image layers are inspected
**THEN** the image contains the Parser module and all application source code, ready for execution inside the container

### SCENARIO 2: Parser imports only standard-library modules
**Scenario ID:** PARSING-INFRA-001.2-S002
**GIVEN** the Parser module source file inside the Docker container
**WHEN** the import statements are inspected
**THEN** every imported module belongs to the Python standard library and no third-party runtime package is referenced (TC-3)

### SCENARIO 3: Application runs on Python 3.12 inside Docker
**Scenario ID:** PARSING-INFRA-001.2-S003
**GIVEN** a Docker container running the built image with Python 3.12
**WHEN** the application CLI is invoked inside the container
**THEN** the application runs to completion without a `SyntaxError` or version-compatibility error (TC-1)

### SCENARIO 4: Docker image builds successfully for development testing
**Scenario ID:** PARSING-INFRA-001.2-S004
**GIVEN** the CI workflow configuration (`.github/workflows/ci.yml`)
**WHEN** the workflow executes `docker build -t kata-tests .`
**THEN** the build completes successfully, creating a runnable Docker image that includes the Parser

### SCENARIO 5: Application runs without Docker installation (original CLI requirement)
**Scenario ID:** PARSING-INFRA-001.2-S005
**GIVEN** a machine with Python ≥ 3.12 and the BankOCR source files present on the local file system
**WHEN** the CLI is invoked from the command line with a valid input file path
**THEN** the application starts and the Parser executes without requiring `pip install` or any build step (preserves QS-11)

---

#### PARSING-INFRA-001.3 – Confirm that the Parser operates on in-memory strings with no file-based data handling in Docker

**Story ID:** PARSING-INFRA-001.3
**Parent story:** PARSING-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Parser has no file-system dependency; ADR-002)
- `architecture/08-crosscutting-concepts.md`, Section 8.2 (Separation of I/O from logic)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)
- Dockerfile (local Docker-based environment)

**AS A** BankOCR developer,
**I WANT** the Parser to receive account entries as in-memory string arguments and return account strings as return values within the Docker container, with no direct file access,
**SO THAT** the Parser can be tested and reused without any dependency on the file system, consistent with ADR-002.

> **Note:** File I/O for account entries is owned exclusively by the Processor (ADR-002, `architecture/05-building-block-view.md`, Section 5.2). This story confirms the Parser's compliance with that boundary in the Docker environment; it does not assign file-handling responsibilities to the Parser.

#### Acceptance Scenarios

### SCENARIO 1: Parser accepts a string argument, not a file path, in Docker container
**Scenario ID:** PARSING-INFRA-001.3-S001
**GIVEN** the Parser's public interface inside the Docker container
**WHEN** it is called with a four-line string representing one account entry
**THEN** it processes the string in memory and returns a nine-character string without opening any file or accessing host file system

### SCENARIO 2: Parser produces no file-system side effects in Docker
**Scenario ID:** PARSING-INFRA-001.3-S002
**GIVEN** an invocation of the Parser with a valid four-line account entry string inside Docker
**WHEN** the Parser runs to completion
**THEN** no file is created, modified, or deleted on the container's file system or host file system as a side effect

### SCENARIO 3: Parser behavior is consistent regardless of container file paths
**Scenario ID:** PARSING-INFRA-001.3-S003
**GIVEN** two Docker containers running the same image but with different mounted volumes or working directories
**WHEN** the Parser is called with identical account entry string content in both containers
**THEN** both calls return the identical nine-character account string, confirming no dependency on container file paths or mounted volumes

---

#### PARSING-INFRA-001.4 – Confirm event inapplicability and define observability via pytest results and Docker exit codes

**Story ID:** PARSING-INFRA-001.4
**Parent story:** PARSING-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/10-quality-requirements.md`, QS-07
- `architecture/11-risks-and-technical-debt.md`, DEBT-03
- Dockerfile (local Docker-based environment)
- CI workflow (`.github/workflows/ci.yml`)

**AS A** BankOCR developer,
**I WANT** the system to report Parser test outcomes through `pytest` results and Docker container exit codes rather than through event infrastructure,
**SO THAT** errors in digit recognition are visible in the Docker-based test environment without introducing monitoring services that the architecture does not approve.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the PARSING domain. This story documents that determination explicitly and specifies the observability mechanism that applies in the Docker environment.
>
> **QS-07 clarification:** The original QS-7 requirement specifies that tests should run with no external dependencies on a machine with only Python ≥ 3.12. The Module 4 Docker/pytest setup introduces `pytest` as a third-party test dependency, which creates a discrepancy with the original QS-7 requirement. `pytest` is a test-only dependency and does not affect runtime execution, but it does mean the full test suite cannot run with zero external dependencies as originally specified in QS-7.

#### Acceptance Scenarios

### SCENARIO 1: pytest reports Parser test pass or fail in Docker
**Scenario ID:** PARSING-INFRA-001.4-S001
**GIVEN** the Parser tests are executed inside Docker with `docker run --rm kata-tests`
**WHEN** one or more Parser tests fail
**THEN** pytest prints a FAIL or ERROR result for each failing test to stdout, and the Docker container exits with a non-zero exit code

### SCENARIO 2: CI workflow captures test results from Docker
**Scenario ID:** PARSING-INFRA-001.4-S002
**GIVEN** the CI workflow configuration (`.github/workflows/ci.yml`)
**WHEN** the workflow executes `docker run --rm kata-tests`
**THEN** the workflow step captures the pytest output and fails if any tests fail, providing observability through GitHub Actions

### SCENARIO 3: No event infrastructure is present in the Parser module in Docker
**Scenario ID:** PARSING-INFRA-001.4-S003
**GIVEN** the Parser module source code inside the Docker container
**WHEN** the source is inspected for imports or calls to message queues, event buses, logging frameworks, or external monitoring services
**THEN** no such imports or calls are present; the Parser contains only pure glyph-recognition logic and standard-library imports

### SCENARIO 4: Docker container exit code reflects test suite success
**Scenario ID:** PARSING-INFRA-001.4-S004
**GIVEN** a Docker container running the full test suite with `docker run --rm kata-tests`
**WHEN** all tests in the suite (including Parser tests) pass
**THEN** the container exits with exit code 0; when any test fails, it exits with a non-zero code

### SCENARIO 5: Application exits with code 0 after successful digit recognition
**Scenario ID:** PARSING-INFRA-001.4-S005
**GIVEN** a well-formed input file containing valid account entries
**WHEN** the BankOCR CLI application processes the file and completes digit recognition through the Parser
**THEN** the application process exits with exit code 0

---

### DDD Analysis

**Bounded context:** PARSING — the logical responsibility boundary within the BankOCR CLI that owns glyph recognition and account string assembly.

**Conceptual domain elements** (requirements-analysis concepts; they do not prescribe specific implementation class names):

| Element | Type | Description |
|---------|------|-------------|
| `AsciiDigitGlyph` | Value object | A 3×3 character grid representing one decimal digit. Immutable; equality is defined by character content, not identity. |
| `AccountString` | Value object | The nine-character string produced by parsing one account entry. Each position holds a decimal digit character or a placeholder. Immutable. |
| `AccountEntry` | Aggregate root | One account entry as received from the Processor: four lines comprising nine ordered `AsciiDigitGlyph` instances. The Parser's unit of work. |

**Relationship to existing architecture:** These concepts map onto the Parser component described in `architecture/05-building-block-view.md`, Section 5.2. The Parser component is the implementation boundary; `AccountEntry`, `AsciiDigitGlyph`, and `AccountString` are domain vocabulary for reasoning about its behaviour. The architecture does not mandate separate classes for each; the mapping is an implementation decision.

**Component boundaries respected:** The Parser has no dependency on the Validator, Processor, or file system (ADR-002). The `AccountString` value object it produces is handed to the Processor, which passes it to the Validator. The PARSING bounded context ends at that handoff.

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-2 – Recognise ASCII digit glyphs | PARSING-STORY-001, PARSING-BE-001.1, PARSING-BE-001.1-S001 |
| FR-3 – Assemble nine-digit account numbers | PARSING-STORY-001, PARSING-BE-001.1, PARSING-BE-001.1-S002 |
| TC-1 – Python ≥ 3.12 | PARSING-INFRA-001.1-S001, PARSING-INFRA-001.2-S003 |
| TC-2 – Four-line entry format | PARSING-STORY-001-S001, PARSING-BE-001.1-S002, PARSING-INFRA-001.3-S001 |
| TC-3 – Standard library only | PARSING-INFRA-001.2-S002 |
| TC-5 – unittest | Note: Docker uses pytest, not unittest (PARSING-INFRA-001.1) |
| ADR-001 – Single CLI, no external services | PARSING-INFRA-001.4-S003 |
| ADR-002 – File I/O confined to Processor | PARSING-INFRA-001.3-S001, PARSING-INFRA-001.3-S002, PARSING-INFRA-001.3-S003 |
| Dockerfile – Local Docker environment | PARSING-INFRA-001.1-S001, PARSING-INFRA-001.1-S002, PARSING-INFRA-001.2-S001, PARSING-INFRA-001.2-S004 |
| CI workflow – GitHub Actions | PARSING-INFRA-001.2-S004, PARSING-INFRA-001.4-S002 |
| QS-01 – Digit recognition accuracy | PARSING-STORY-001-S003, PARSING-BE-001.1-S001 |
| QS-05 – Parser tested without file I/O | PARSING-INFRA-001.1-S003, PARSING-INFRA-001.1-S004, PARSING-INFRA-001.3-S001 |
| QS-07 – Test suite runs with no external dependencies | PARSING-INFRA-001.4-S001, PARSING-INFRA-001.4-S002 – Note: `pytest` is a third-party test dependency, creating a discrepancy with the original QS-7 requirement for dependency-free testing |
| QS-10 – No unjustified dependencies | PARSING-INFRA-001.2-S002 |
| QS-11 – Single command invocation | PARSING-INFRA-001.2-S001, PARSING-INFRA-001.2-S005 |
| DEBT-03 – No structured logging | PARSING-INFRA-001.4-S003 |
| RISK-01 – Glyph pattern coverage | PARSING-STORY-001-S003, PARSING-BE-001.1-S001 |

---

**Bundle status:** Approved

---

## PARSING-STORY-002 – Handle Unrecognised Glyphs with a Placeholder

**Domain:** PARSING
**Story ID:** PARSING-STORY-002
**Title:** Handle unrecognised glyphs with a placeholder
**Priority:** Supporting
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Parser component, dependency rules)
- `architecture/06-runtime-view.md`, Section 6.2 (ILL path: Parser returns string with placeholder)
- `architecture/06-runtime-view.md`, Section 6.3 (runtime invariant: Parser returns exactly one nine-character string)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (placeholder convention, no exception raised)
- `architecture/10-quality-requirements.md`, QS-02, QS-05
- `architecture/12-glossary.md` (Placeholder definition)

---

### Scope distinction

This story covers the Parser's behaviour when one or more glyphs in an account entry cannot be matched to a known digit pattern. PARSING-STORY-001 covers the happy path where all nine glyphs are recognised. Together they span the Parser's complete `AccountString` production responsibility.

The Parser's sole obligation when it encounters an unrecognised glyph is to insert a placeholder character at that position and return a nine-character string. It does not raise an exception, return a special object, perform a checksum calculation, or assign VALID, ERR, or ILL status. Status determination belongs exclusively to the Validator (VALIDATION domain, `architecture/05-building-block-view.md`, Section 5.2).

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to handle account entries containing unrecognisable digit glyphs without crashing,
**SO THAT** every entry in my input file still produces a result, and entries with damaged or malformed glyphs are identifiable in the output.

---

### Acceptance Scenarios

### SCENARIO 1: Return a nine-character string with a placeholder at each unrecognised position
**Scenario ID:** PARSING-STORY-002-S001
**GIVEN** an account entry in which one or more 3×3 glyph positions do not match any of the ten known digit patterns
**WHEN** the Parser processes the entry
**THEN** it returns a nine-character string in which each unrecognised position contains a placeholder character and each recognised position contains the correct decimal digit

### SCENARIO 2: Return exactly nine characters regardless of how many glyphs are unrecognised
**Scenario ID:** PARSING-STORY-002-S002
**GIVEN** an account entry in which any number of positions (from one to nine) contain unrecognised glyphs
**WHEN** the Parser processes the entry
**THEN** the returned string contains exactly nine characters, one per glyph position, with no positions dropped or added

### SCENARIO 3: Do not raise an exception for an unrecognised glyph
**Scenario ID:** PARSING-STORY-002-S003
**GIVEN** an account entry containing at least one glyph that matches no known digit pattern
**WHEN** the Parser processes the entry
**THEN** it completes normally and returns a nine-character string; no exception is raised and no error object is returned

### SCENARIO 4: Recognised glyphs in a mixed entry are mapped correctly
**Scenario ID:** PARSING-STORY-002-S004
**GIVEN** an account entry in which some positions contain recognisable glyphs and others contain unrecognisable glyphs
**WHEN** the Parser processes the entry
**THEN** every recognisable position is mapped to its correct decimal digit and every unrecognisable position receives a placeholder character, with no digit shifted from its original position

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3).

---

### Backend Stories

#### PARSING-BE-002.1 – Insert a placeholder character for each unrecognised 3×3 glyph

**Story ID:** PARSING-BE-002.1
**Parent story:** PARSING-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Parser responsibility)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (placeholder convention: insert character, do not raise exception)
- `architecture/12-glossary.md` (Placeholder: non-digit character inserted at unrecognised position)

**AS A** BankOCR developer,
**I WANT** the Parser to insert a placeholder character (conventionally `?`) at every position where the 3×3 glyph cannot be matched to any of the ten known digit patterns,
**SO THAT** the returned `AccountString` faithfully records which positions were unrecognisable, enabling the Validator to detect and classify the entry as ILL.

#### Acceptance Scenarios

### SCENARIO 1: Insert a placeholder at the position of a single unrecognised glyph
**Scenario ID:** PARSING-BE-002.1-S001
**GIVEN** a four-line account entry in which exactly one of the nine 3×3 glyph positions does not match any known digit pattern
**WHEN** the Parser processes the entry
**THEN** the returned nine-character string contains a placeholder character at that position and correct decimal digits at all other positions

### SCENARIO 2: Insert placeholders at all unrecognised positions in a multi-unrecognised entry
**Scenario ID:** PARSING-BE-002.1-S002
**GIVEN** a four-line account entry in which more than one glyph position does not match any known digit pattern
**WHEN** the Parser processes the entry
**THEN** the returned string contains a placeholder character at each unrecognised position and correct decimal digits at all recognised positions

### SCENARIO 3: Do not alter recognised positions when placeholders are inserted elsewhere
**Scenario ID:** PARSING-BE-002.1-S003
**GIVEN** a four-line account entry containing a mix of recognisable and unrecognisable glyphs
**WHEN** the Parser processes the entry
**THEN** every recognised glyph is mapped to its correct decimal digit without being shifted, replaced by a placeholder, or otherwise altered

---

#### PARSING-BE-002.2 – Always return a nine-character AccountString with no exception for unrecognised glyphs

**Story ID:** PARSING-BE-002.2
**Parent story:** PARSING-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Parser returns a nine-character account string)
- `architecture/06-runtime-view.md`, Section 6.3 (runtime invariant: Parser called once per entry, returns exactly one nine-character string)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (Parser does not raise an exception or return a special object for unrecognised glyphs)

**AS A** BankOCR developer,
**I WANT** the Parser to return a nine-character `AccountString` for every account entry it receives, even when one or more glyphs are unrecognised,
**SO THAT** the pipeline invariant is maintained and the Processor can always pass the result to the Validator without special-case handling.

#### Acceptance Scenarios

### SCENARIO 1: Return exactly nine characters for an entry with one unrecognised glyph
**Scenario ID:** PARSING-BE-002.2-S001
**GIVEN** a four-line account entry containing exactly one unrecognised glyph
**WHEN** the Parser processes the entry
**THEN** the return value is a string of exactly nine characters

### SCENARIO 2: Return exactly nine characters for an entry where all nine glyphs are unrecognised
**Scenario ID:** PARSING-BE-002.2-S002
**GIVEN** a four-line account entry in which all nine glyph positions contain patterns that match none of the ten known digits
**WHEN** the Parser processes the entry
**THEN** the return value is a string of exactly nine placeholder characters

### SCENARIO 3: No exception is raised and no special object is returned for any unrecognised glyph
**Scenario ID:** PARSING-BE-002.2-S003
**GIVEN** a four-line account entry containing one or more unrecognised glyphs
**WHEN** the Parser processes the entry
**THEN** the call returns normally with a nine-character string; no exception propagates to the caller and no non-string return value is produced

---

### Infrastructure Stories

#### PARSING-INFRA-002.1 – Test placeholder insertion in isolation using unittest

**Story ID:** PARSING-INFRA-002.1
**Parent story:** PARSING-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Dependency rules: Parser has no file-system dependency)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Parser testability convention)
- `architecture/10-quality-requirements.md`, QS-02, QS-05, QS-07

**AS A** BankOCR developer,
**I WANT** the Parser's placeholder insertion behaviour to be covered by `unittest` tests that pass malformed account entry strings directly to the Parser,
**SO THAT** unrecognised glyph handling is verified in isolation without file fixtures or external tools.

#### Acceptance Scenarios

### SCENARIO 1: Test confirms placeholder appears at each unrecognised position
**Scenario ID:** PARSING-INFRA-002.1-S001
**GIVEN** a `unittest` test case that constructs a four-line account entry string containing one or more unrecognised glyph patterns
**WHEN** the string is passed directly to the Parser
**THEN** the test asserts that the returned string contains a placeholder character at each unrecognised position and the correct digit at each recognised position

### SCENARIO 2: Test confirms the returned string is always nine characters
**Scenario ID:** PARSING-INFRA-002.1-S002
**GIVEN** a `unittest` test case that passes account entry strings with varying numbers of unrecognised glyphs (one, several, and all nine)
**WHEN** each string is passed directly to the Parser
**THEN** the test asserts that every returned string has a length of exactly nine characters

### SCENARIO 3: Placeholder insertion tests require no file fixtures
**Scenario ID:** PARSING-INFRA-002.1-S003
**GIVEN** the full set of `unittest` tests for PARSING-STORY-002
**WHEN** the suite is executed
**THEN** no test creates, reads, or deletes a file on disk, and no temporary directory is required

---

#### PARSING-INFRA-002.2 – Confirm that placeholder insertion introduces no file I/O or status determination

**Story ID:** PARSING-INFRA-002.2
**Parent story:** PARSING-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Parser has no dependency on Validator, Processor, or file system)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (Parser does not assign ILL status), Section 8.2 (Separation of I/O from logic)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)

**AS A** BankOCR developer,
**I WANT** the Parser's placeholder insertion logic to operate entirely on in-memory strings, with no file access and no assignment of VALID, ERR, or ILL status,
**SO THAT** the boundary between PARSING and VALIDATION remains clean and each component remains independently testable.

> **Note:** The placeholder character signals an unrecognised glyph to the Validator. Status assignment (ILL) is performed exclusively by the Validator after it receives the `AccountString` from the Processor. The Parser has no knowledge of VALID, ERR, or ILL.

#### Acceptance Scenarios

### SCENARIO 1: Parser produces no file-system side effects when inserting placeholders
**Scenario ID:** PARSING-INFRA-002.2-S001
**GIVEN** an invocation of the Parser with a four-line account entry string containing unrecognised glyphs
**WHEN** the Parser runs to completion
**THEN** no file is created, modified, or deleted on the file system as a side effect

### SCENARIO 2: Parser does not assign or return a validation status
**Scenario ID:** PARSING-INFRA-002.2-S002
**GIVEN** the Parser module source code
**WHEN** the return-value logic is inspected
**THEN** the Parser returns only a nine-character string; it never returns or assigns the values `VALID`, `ERR`, or `ILL`

### SCENARIO 3: Parser makes no call to the Validator when processing an entry with unrecognised glyphs
**Scenario ID:** PARSING-INFRA-002.2-S003
**GIVEN** the Parser module source code
**WHEN** the logic for handling unrecognised glyphs is inspected
**THEN** no call to the Validator or any checksum function is present; placeholder insertion is the Parser's complete response to an unrecognised glyph

---

#### PARSING-INFRA-002.3 – Confirm event inapplicability and define observability for unrecognised glyph handling

**Story ID:** PARSING-INFRA-002.3
**Parent story:** PARSING-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/10-quality-requirements.md`, QS-07
- `architecture/11-risks-and-technical-debt.md`, RISK-01, DEBT-03

**AS A** BankOCR developer,
**I WANT** unrecognised glyph occurrences to be observable through `unittest` test results and the downstream ` ILL` annotation in the output file, rather than through event infrastructure,
**SO THAT** glyph recognition gaps are detectable without introducing monitoring services that the architecture does not approve.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the PARSING domain. The presence of a placeholder in the `AccountString` is the signal that propagates the unrecognised-glyph condition to the Validator and ultimately to the output file annotation.

#### Acceptance Scenarios

### SCENARIO 1: unittest test suite surfaces any missing or incorrect placeholder logic
**Scenario ID:** PARSING-INFRA-002.3-S001
**GIVEN** the Parser unit tests for PARSING-STORY-002 are executed with `python -m unittest`
**WHEN** the placeholder insertion logic is incorrect or absent
**THEN** one or more tests fail and the runner exits with a non-zero exit code, surfacing the defect

### SCENARIO 2: An unrecognised glyph produces a visible ILL annotation in the output file
**Scenario ID:** PARSING-INFRA-002.3-S002
**GIVEN** the CLI is invoked with an input file containing an account entry with at least one unrecognised glyph
**WHEN** the full pipeline runs to completion
**THEN** the corresponding result line in the output file is suffixed with ` ILL`, confirming the placeholder propagated correctly through the Validator to the Processor

### SCENARIO 3: No event infrastructure is present in the Parser module for unrecognised glyph handling
**Scenario ID:** PARSING-INFRA-002.3-S003
**GIVEN** the Parser module source code
**WHEN** the unrecognised-glyph handling logic is inspected
**THEN** no message queue, event bus, logging call, or external monitoring service is invoked; the Parser inserts a placeholder character and returns the nine-character string with no other side effects

---

### DDD Analysis

**Bounded context:** PARSING — same bounded context as PARSING-STORY-001. This story extends the Parser's behaviour to cover the case where glyph recognition fails.

**Conceptual domain elements relevant to this story** (extending the elements defined in PARSING-STORY-001):

| Element | Type | Description |
|---------|------|-------------|
| `AsciiDigitGlyph` | Value object | As defined in PARSING-STORY-001. This story adds the case where a 3×3 character grid does not match any of the ten known patterns; it is then classified as an unrecognised glyph. |
| `Placeholder` | Value object | A single non-digit character (conventionally `?`) placed in an `AccountString` at the position of an unrecognised `AsciiDigitGlyph`. Immutable. Its presence in the `AccountString` is the signal that causes the Validator to return `ILL`. |
| `AccountString` | Value object | As defined in PARSING-STORY-001. This story adds the constraint that it may contain `Placeholder` characters at any position where glyph recognition failed, while still being exactly nine characters long. |
| `AccountEntry` | Aggregate root | As defined in PARSING-STORY-001. This story adds the case where one or more of its nine glyph positions is unrecognised. |

**Domain rules enforced by the Parser for this story:**
1. For every glyph position in an `AccountEntry`, the Parser attempts to match the 3×3 character grid against the ten known digit patterns.
2. If a match is found, the corresponding decimal digit character is placed at that position in the `AccountString`.
3. If no match is found, a `Placeholder` character is placed at that position instead.
4. The `AccountString` is always exactly nine characters long regardless of how many positions contain `Placeholder` values.
5. The Parser never raises an exception, returns a non-string value, or assigns a validation status for an unrecognised glyph.

**Boundary with VALIDATION domain:** The `Placeholder` character in the `AccountString` is the only signal passed across the PARSING → PROCESSING → VALIDATION boundary. The Validator detects it and returns `ILL`; the Parser has no knowledge of that outcome. This clean separation is enforced by the architecture (ch. 5.2, ADR-002, ch. 8.1).

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-5 – Mark illegible accounts as ILL (Parser's role: insert placeholder) | PARSING-STORY-002, PARSING-BE-002.1, PARSING-BE-002.1-S001, PARSING-BE-002.1-S002 |
| TC-1 – Python ≥ 3.12 | PARSING-INFRA-002.1-S001 |
| TC-3 – Standard library only | PARSING-INFRA-002.1-S001 |
| TC-5 – unittest | PARSING-INFRA-002.1-S001, PARSING-INFRA-002.3-S001 |
| ADR-001 – Single CLI, no external services | PARSING-INFRA-002.3-S003 |
| ADR-002 – File I/O confined to Processor | PARSING-INFRA-002.2-S001 |
| QS-02 – Unrecognised glyph handling | PARSING-STORY-002-S001, PARSING-STORY-002-S003, PARSING-BE-002.1-S001, PARSING-INFRA-002.1-S001 |
| QS-05 – Parser tested without file I/O | PARSING-INFRA-002.1-S003, PARSING-INFRA-002.2-S001 |
| QS-07 – Test suite runs with no external dependencies | PARSING-INFRA-002.1-S001, PARSING-INFRA-002.3-S001 |
| ch. 6.2 – ILL path: Parser returns string with placeholder | PARSING-STORY-002-S001, PARSING-BE-002.1-S001, PARSING-INFRA-002.3-S002 |
| ch. 6.3 – Parser returns exactly one nine-character string | PARSING-STORY-002-S002, PARSING-BE-002.2-S001, PARSING-BE-002.2-S002 |
| ch. 8.1 – Placeholder convention; no exception raised | PARSING-STORY-002-S003, PARSING-BE-002.1-S001, PARSING-BE-002.2-S003, PARSING-INFRA-002.2-S002, PARSING-INFRA-002.2-S003 |
| ch. 8.2 – Separation of I/O from logic | PARSING-INFRA-002.2-S001 |
| RISK-01 – Glyph pattern coverage | PARSING-STORY-002-S004, PARSING-BE-002.1-S003, PARSING-INFRA-002.3-S001 |
| DEBT-03 – No structured logging | PARSING-INFRA-002.3-S003 |

---

**Bundle status:** Approved
