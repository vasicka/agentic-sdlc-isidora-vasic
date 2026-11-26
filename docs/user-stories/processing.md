# PROCESSING Domain – User Story Bundles

## Domain Overview

**Domain:** PROCESSING
**Architecture component:** Processor
**Responsibility:** Read the input file, split it into account entries, coordinate the Parser and Validator for each entry, and write one annotated result line per entry to the output file.

**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-1, FR-7)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor component, dependency rules)
- `architecture/08-crosscutting-concepts.md`, Sections 8.1, 8.2, 8.4 (error handling, I/O separation, input format)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)

---

## PROCESSING-STORY-002 – Coordinate Parse-Validate-Record Pipeline per Entry

**Domain:** PROCESSING
**Story ID:** PROCESSING-STORY-002
**Title:** Coordinate parse-validate-record pipeline per entry
**Priority:** CORE
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-1, FR-7)
- `architecture/04-solution-strategy.md`, Section 4.2 (Processor responsibility), Section 4.3 (processing strategy)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor component, dependency rules)
- `architecture/06-runtime-view.md`, Section 6.1 (full valid-path sequence), Section 6.2 (ERR and ILL paths), Section 6.3 (runtime invariants)
- `architecture/08-crosscutting-concepts.md`, Sections 8.1, 8.2, 8.4
- `architecture/09-architecture-decisions.md`, ADR-002
- `architecture/10-quality-requirements.md`, QS-04, QS-07, QS-08, QS-09

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to process every account entry in my input file through the full parse-validate-record pipeline,
**SO THAT** every account number receives exactly one correctly annotated result line in the output file.

---

### Acceptance Scenarios

### SCENARIO 1: Produce a bare result line for a valid account entry
**Scenario ID:** PROCESSING-STORY-002-S001
**GIVEN** an input file containing one account entry whose nine glyphs are all recognisable and whose mod-11 checksum passes
**WHEN** the Processor runs the pipeline for that entry
**THEN** the output file contains exactly one line consisting of the nine-digit account number with no annotation

### SCENARIO 2: Produce an ERR-annotated result line for a checksum-failing entry
**Scenario ID:** PROCESSING-STORY-002-S002
**GIVEN** an input file containing one account entry whose nine glyphs are all recognisable but whose mod-11 checksum fails
**WHEN** the Processor runs the pipeline for that entry
**THEN** the output file contains exactly one line consisting of the nine-digit account number suffixed with ` ERR`

### SCENARIO 3: Produce an ILL-annotated result line for an entry with an unrecognised glyph
**Scenario ID:** PROCESSING-STORY-002-S003
**GIVEN** an input file containing one account entry in which one or more glyphs cannot be matched to a known digit pattern
**WHEN** the Processor runs the pipeline for that entry
**THEN** the output file contains exactly one line consisting of the account string (with placeholder characters in unrecognised positions) suffixed with ` ILL`

### SCENARIO 4: Produce one result line per entry with no entries dropped
**Scenario ID:** PROCESSING-STORY-002-S004
**GIVEN** an input file containing multiple account entries of mixed validity (VALID, ERR, and ILL)
**WHEN** the Processor runs the pipeline for the entire file
**THEN** the output file contains exactly one result line for each input entry, in the same order, and no entry is omitted or duplicated

### SCENARIO 5: Call Parser and Validator exactly once per entry
**Scenario ID:** PROCESSING-STORY-002-S005
**GIVEN** an input file containing N account entries
**WHEN** the Processor processes the file
**THEN** the Parser is called exactly N times and the Validator is called exactly N times, once each per entry

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3). The Processor has no user-facing interface beyond the CLI entry point, which is covered by PROCESSING-STORY-005.

---

### Backend Stories

#### PROCESSING-BE-002.1 – Implement the per-entry parse-validate-record loop

**Story ID:** PROCESSING-BE-002.1
**Parent story:** PROCESSING-STORY-002
**Priority:** CORE
**Architecture references:**
- `architecture/04-solution-strategy.md`, Section 4.3 (sequential single-pass processing strategy)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor depends on Parser and Validator; Parser and Validator are independent of each other)
- `architecture/06-runtime-view.md`, Section 6.1 (Steps 3–7), Section 6.3 (runtime invariants)

**AS A** BankOCR developer,
**I WANT** the Processor to iterate over each account entry in sequence, pass it to the Parser, pass the resulting account string to the Validator, and record the annotated result,
**SO THAT** every entry in the input file is processed in a single pass with no entries skipped or processed more than once.

#### Acceptance Scenarios

### SCENARIO 1: Pass each entry to the Parser and receive an account string
**Scenario ID:** PROCESSING-BE-002.1-S001
**GIVEN** a pre-sliced four-line account entry held in memory
**WHEN** the Processor passes the entry to the Parser
**THEN** the Processor receives a nine-character account string as the return value and does not read the file again for that entry

### SCENARIO 2: Pass each account string to the Validator and receive a status
**Scenario ID:** PROCESSING-BE-002.1-S002
**GIVEN** a nine-character account string returned by the Parser
**WHEN** the Processor passes the string to the Validator
**THEN** the Processor receives exactly one of `VALID`, `ERR`, or `ILL` as the return value

### SCENARIO 3: Record one result line per entry in order
**Scenario ID:** PROCESSING-BE-002.1-S003
**GIVEN** a sequence of account entries processed one at a time
**WHEN** the Processor receives the Validator status for each entry
**THEN** it appends exactly one correctly annotated result line to the output for that entry before moving to the next entry, preserving input order

---

#### PROCESSING-BE-002.2 – Apply correct output annotation based on Validator status

**Story ID:** PROCESSING-BE-002.2
**Parent story:** PROCESSING-STORY-002
**Priority:** CORE
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-7)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor writes annotated result lines)
- `architecture/06-runtime-view.md`, Section 6.2 (ERR and ILL path comparison table)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (result classification table)
- `architecture/10-quality-requirements.md`, QS-04

**AS A** BankOCR developer,
**I WANT** the Processor to format each result line by appending ` ERR` or ` ILL` when the Validator returns those statuses, and no suffix when the Validator returns `VALID`,
**SO THAT** the output file matches the kata-specified annotation format exactly.

#### Acceptance Scenarios

### SCENARIO 1: Write a bare account number for VALID status
**Scenario ID:** PROCESSING-BE-002.2-S001
**GIVEN** the Validator returns `VALID` for an account string
**WHEN** the Processor formats the result line
**THEN** the result line contains the nine-character account string with no suffix and no trailing space

### SCENARIO 2: Write an ERR-suffixed line for ERR status
**Scenario ID:** PROCESSING-BE-002.2-S002
**GIVEN** the Validator returns `ERR` for an account string
**WHEN** the Processor formats the result line
**THEN** the result line contains the nine-character account string followed by exactly ` ERR` (one space then the three characters E, R, R)

### SCENARIO 3: Write an ILL-suffixed line for ILL status
**Scenario ID:** PROCESSING-BE-002.2-S003
**GIVEN** the Validator returns `ILL` for an account string
**WHEN** the Processor formats the result line
**THEN** the result line contains the nine-character account string followed by exactly ` ILL` (one space then the three characters I, L, L)

---

### Infrastructure Stories

#### PROCESSING-INFRA-002.1 – Test the Processor pipeline coordination in Docker using pytest with temporary files

**Story ID:** PROCESSING-INFRA-002.1
**Parent story:** PROCESSING-STORY-002
**Priority:** CORE
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5) – Note: TC-5 specifies `unittest` but Docker uses `pytest`
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Processor tests may use temporary files)
- `architecture/10-quality-requirements.md`, QS-07
- `architecture/11-risks-and-technical-debt.md`, RISK-03 (no integration test covers the full pipeline end-to-end)
- Dockerfile (local Docker-based environment established in Module 4)
- CI workflow (`.github/workflows/ci.yml`)

**AS A** BankOCR developer,
**I WANT** the Processor's pipeline coordination logic to be covered by at least one end-to-end `pytest` test that exercises a real input file and asserts on the content of the resulting output file within a Docker container,
**SO THAT** integration defects in the Processor's coordination logic and output formatting are detected automatically in the Docker-based test environment.

> **Mitigation of RISK-03:** The architecture identifies (`architecture/11-risks-and-technical-debt.md`, RISK-03) that isolated unit tests alone do not detect errors in the Processor's coordination or output formatting. This sub-story directly addresses that risk by requiring at least one end-to-end test with file I/O, as permitted by the testability convention in `architecture/08-crosscutting-concepts.md`, Section 8.3.
>
> **QS-07 clarification:** The original QS-7 requirement specifies that tests should run with no external dependencies on a machine with only Python ≥ 3.12. The Module 4 Docker/pytest setup introduces `pytest` as a third-party test dependency, which creates a discrepancy with the original QS-7 requirement. `pytest` is a test-only dependency and does not affect runtime execution, but it does mean the full test suite cannot run with zero external dependencies as originally specified in QS-7.

#### Acceptance Scenarios

### SCENARIO 1: Build Docker image for end-to-end testing
**Scenario ID:** PROCESSING-INFRA-002.1-S001
**GIVEN** the BankOCR source code with its Dockerfile and test dependencies configuration
**WHEN** the Docker image is built with `docker build -t kata-tests .`
**THEN** the build completes successfully, installing Python 3.12 and test dependencies including pytest for end-to-end testing

### SCENARIO 2: End-to-end test reads a real input file and asserts on output file content in Docker
**Scenario ID:** PROCESSING-INFRA-002.1-S002
**GIVEN** a pytest test case that creates a temporary input file containing at least one valid, one ERR, and one ILL account entry inside Docker
**WHEN** the Processor is invoked with that file within the Docker container
**THEN** the test reads the resulting output file and asserts that each result line carries the correct annotation, confirming the full pipeline executed correctly

### SCENARIO 3: End-to-end test cleans up temporary files after execution in Docker
**Scenario ID:** PROCESSING-INFRA-002.1-S003
**GIVEN** an end-to-end Processor test that creates temporary input and output files inside Docker
**WHEN** the test completes, whether passing or failing
**THEN** both temporary files are removed from the container's file system, leaving no test artefacts on disk

### SCENARIO 4: End-to-end test runs with pytest in Docker container
**Scenario ID:** PROCESSING-INFRA-002.1-S004
**GIVEN** the built Docker image containing the BankOCR source and test suite
**WHEN** end-to-end Processor tests are executed with `docker run --rm kata-tests` (default CMD runs pytest)
**THEN** the tests run inside the container and produce results without requiring external dependencies

---

#### PROCESSING-INFRA-002.2 – Deploy the Processor as the entry point of the single-file CLI application in Docker environment

**Story ID:** PROCESSING-INFRA-002.2
**Parent story:** PROCESSING-STORY-002
**Priority:** CORE
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3)
- `architecture/04-solution-strategy.md`, Section 4.1 (single CLI application; Processor coordinates the pipeline)
- `architecture/07-deployment-view.md`, Sections 7.1, 7.2, 7.3 – Note: Deployment view doesn't mention Docker
- `architecture/10-quality-requirements.md`, QS-10, QS-11
- Dockerfile (local Docker-based environment)

**AS A** BankOCR developer,
**I WANT** the Processor to serve as the coordination entry point of the single Python CLI application within a Docker container,
**SO THAT** the full parse-validate-record pipeline can be invoked through Docker on any machine with Docker installed, without requiring Python ≥ 3.12 on the host.

#### Acceptance Scenarios

### SCENARIO 1: Docker image contains the complete application with Processor as entry point
**Scenario ID:** PROCESSING-INFRA-002.2-S001
**GIVEN** the built Docker image `kata-tests`
**WHEN** the image layers are inspected
**THEN** the image contains the Processor module and all application source code, with Processor as the pipeline coordination entry point

### SCENARIO 2: Processor imports only standard-library modules
**Scenario ID:** PROCESSING-INFRA-002.2-S002
**GIVEN** the Processor module source file inside the Docker container
**WHEN** the import statements are inspected
**THEN** every imported module belongs to the Python standard library or to other BankOCR source modules; no third-party runtime package is referenced (TC-3)

### SCENARIO 3: Application runs on Python 3.12 inside Docker
**Scenario ID:** PROCESSING-INFRA-002.2-S003
**GIVEN** a Docker container running the built image with Python 3.12
**WHEN** the application CLI is invoked inside the container
**THEN** the application runs to completion without a `SyntaxError` or version-compatibility error (TC-1)

### SCENARIO 4: Docker image builds successfully for development testing
**Scenario ID:** PROCESSING-INFRA-002.2-S004
**GIVEN** the CI workflow configuration (`.github/workflows/ci.yml`)
**WHEN** the workflow executes `docker build -t kata-tests .`
**THEN** the build completes successfully, creating a runnable Docker image that includes the Processor as the pipeline coordinator

### SCENARIO 5: Full pipeline executes from a single CLI invocation without Docker (original requirement)
**Scenario ID:** PROCESSING-INFRA-002.2-S005
**GIVEN** a machine with Python ≥ 3.12 and the BankOCR source files present on the local file system
**WHEN** the CLI is invoked with a valid input file path
**THEN** the Processor runs the complete parse-validate-record pipeline for every entry in the file and writes the output file, without requiring `pip install` or any build step (preserves QS-11)

---

#### PROCESSING-INFRA-002.3 – Confirm that the Processor exclusively owns all file-based data handling in Docker

**Story ID:** PROCESSING-INFRA-002.3
**Parent story:** PROCESSING-STORY-002
**Priority:** CORE
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Processor depends on file system; Parser and Validator do not)
- `architecture/08-crosscutting-concepts.md`, Section 8.2 (Separation of I/O from logic), Section 8.4 (input format handling)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)
- Dockerfile (local Docker-based environment)

**AS A** BankOCR developer,
**I WANT** the Processor to be the only component that reads from or writes to the file system within a Docker container, passing pre-sliced string entries to the Parser and nine-character strings to the Validator,
**SO THAT** the file I/O boundary established by ADR-002 is enforced by design in the Docker environment and Parser and Validator remain independently testable with plain string inputs.

#### Acceptance Scenarios

### SCENARIO 1: Processor reads the input file and passes string entries to the Parser in Docker
**Scenario ID:** PROCESSING-INFRA-002.3-S001
**GIVEN** the Processor is processing an input file inside a Docker container
**WHEN** it calls the Parser for each account entry
**THEN** it passes a four-line string argument and does not pass a file path or file handle; the Parser opens no file

### SCENARIO 2: Processor passes account strings to the Validator with no file involvement in Docker
**Scenario ID:** PROCESSING-INFRA-002.3-S002
**GIVEN** the Processor has received a nine-character account string from the Parser inside Docker
**WHEN** it calls the Validator
**THEN** it passes the string as an argument and does not pass a file path or file handle; the Validator opens no file

### SCENARIO 3: Parser and Validator produce no file-system side effects during pipeline execution in Docker
**Scenario ID:** PROCESSING-INFRA-002.3-S003
**GIVEN** the Processor runs the full pipeline for a file containing multiple entries inside Docker
**WHEN** the pipeline completes
**THEN** the only files created or modified on the container's file system are the output file written by the Processor; no file is created or modified by the Parser or Validator

---

#### PROCESSING-INFRA-002.4 – Confirm event inapplicability and define observability via Docker test results and application exit codes

**Story ID:** PROCESSING-INFRA-002.4
**Parent story:** PROCESSING-STORY-002
**Priority:** CORE
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/10-quality-requirements.md`, QS-07
- `architecture/11-risks-and-technical-debt.md`, DEBT-03, RISK-03
- Dockerfile (local Docker-based environment)
- CI workflow (`.github/workflows/ci.yml`)

**AS A** BankOCR developer,
**I WANT** the system to report Processor test outcomes through `pytest` results in Docker and application-level exit codes for CLI execution, rather than through event infrastructure,
**SO THAT** pipeline coordination defects are observable in the Docker test environment and application failures are visible to users, without introducing monitoring services that the architecture does not approve.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the PROCESSING domain. This story documents that determination explicitly and specifies the observability mechanisms that apply in the Docker environment and for CLI execution.
>
> **QS-07 clarification:** The original QS-7 requirement specifies that tests should run with no external dependencies on a machine with only Python ≥ 3.12. The Module 4 Docker/pytest setup introduces `pytest` as a third-party test dependency, which creates a discrepancy with the original QS-7 requirement. `pytest` is a test-only dependency and does not affect runtime execution, but it does mean the full test suite cannot run with zero external dependencies as originally specified in QS-7.

#### Acceptance Scenarios

### SCENARIO 1: pytest reports Processor test pass or fail in Docker
**Scenario ID:** PROCESSING-INFRA-002.4-S001
**GIVEN** the Processor unit and integration tests are executed inside Docker with `docker run --rm kata-tests`
**WHEN** one or more Processor tests fail
**THEN** pytest prints a FAIL or ERROR result for each failing test to stdout, and the Docker container exits with a non-zero exit code

### SCENARIO 2: Application exits with code 0 on successful pipeline completion (original requirement)
**Scenario ID:** PROCESSING-INFRA-002.4-S002
**GIVEN** the CLI is invoked with a well-formed input file (with or without Docker)
**WHEN** the Processor completes the full parse-validate-record pipeline for every entry and writes the output file without an unhandled exception
**THEN** the process exits with exit code 0, regardless of whether running in Docker or directly on Python

### SCENARIO 3: No event infrastructure is present in the Processor module in Docker
**Scenario ID:** PROCESSING-INFRA-002.4-S003
**GIVEN** the Processor module source code inside the Docker container
**WHEN** the source is inspected for imports or calls to message queues, event buses, logging frameworks, or external monitoring services
**THEN** no such imports or calls are present; the Processor contains only file I/O, pipeline coordination logic, and standard-library imports

### SCENARIO 4: Docker container exit code reflects test suite success
**Scenario ID:** PROCESSING-INFRA-002.4-S004
**GIVEN** a Docker container running the full test suite with `docker run --rm kata-tests`
**WHEN** all tests in the suite (including Processor tests) pass
**THEN** the container exits with exit code 0; when any test fails, it exits with a non-zero code

### SCENARIO 5: CI workflow captures Processor test results from Docker
**Scenario ID:** PROCESSING-INFRA-002.4-S005
**GIVEN** the CI workflow configuration (`.github/workflows/ci.yml`)
**WHEN** the workflow executes `docker run --rm kata-tests`
**THEN** the workflow step captures the pytest output and fails if any Processor tests fail, providing observability through GitHub Actions

---

### DDD Analysis

**Bounded context:** PROCESSING — the logical responsibility boundary within the BankOCR CLI that owns file I/O, entry-level pipeline coordination, and result recording. This is the only bounded context with direct file-system access.

**Conceptual domain elements** (requirements-analysis concepts; they do not prescribe specific implementation class names):

| Element | Type | Description |
|---------|------|-------------|
| `ProcessingRun` | Aggregate root | One complete execution: an input file path, the ordered sequence of entries it contains, the results produced for each, and the output file path. Represents the top-level unit of work owned by the Processor. |
| `AccountEntry` | Entity (within ProcessingRun) | One four-line ASCII account entry extracted from the input file. Identified by its position (index) within the input file. Passed to the Parser as a string; not persisted. |
| `ResultLine` | Value object | The formatted output string for one account entry: the nine-character account string optionally suffixed with ` ERR` or ` ILL`. Determined by the Validator's status and the Processor's formatting logic. Immutable once produced. |
| `InputFilePath` | Value object | The path to the plain-text input file supplied by the user. Validated by the Processor before reading (see ch. 8.4, RISK-02). |
| `OutputFilePath` | Value object | The path to the plain-text output file written by the Processor on completion. |

**Domain rules enforced by the Processor:**
1. The input file is read and split into entries before any parsing or validation begins.
2. The Parser is called exactly once per `AccountEntry`; the Validator is called exactly once per returned account string (ch. 6.3 invariants).
3. Every `AccountEntry` produces exactly one `ResultLine`; no entry is dropped or processed more than once (ch. 6.3, ch. 8.1).
4. `ResultLine` formatting is determined solely by the Validator's status: no suffix for `VALID`, ` ERR` for `ERR`, ` ILL` for `ILL`.
5. The Processor is the only component that opens, reads, or writes files; it passes strings to Parser and Validator (ADR-002).

**Shared value objects across bounded context boundaries:**
- `AccountEntry` as a four-line string is produced by the Processor and consumed by the Parser (crosses PROCESSING → PARSING boundary).
- `AccountString` (nine-character string) is produced by the Parser and passed by the Processor to the Validator (crosses PARSING → VALIDATION boundary).
- `ValidationStatus` is produced by the Validator and consumed by the Processor to format `ResultLine` (crosses VALIDATION → PROCESSING boundary).

These crossings are string-valued handoffs, not object references, consistent with the architecture's component boundary rules (ch. 5.2, ADR-002).

**Relationship to existing architecture:** These concepts map onto the Processor component described in `architecture/05-building-block-view.md`, Section 5.2, and the runtime sequence in `architecture/06-runtime-view.md`. The architecture does not mandate separate classes for each domain element; the mapping is an implementation decision.

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-1 – Read input file and split into four-line entries | PROCESSING-STORY-002, PROCESSING-BE-002.1, PROCESSING-BE-002.1-S001, PROCESSING-INFRA-002.3-S001 |
| FR-7 – Write one annotated result line per entry | PROCESSING-STORY-002, PROCESSING-BE-002.2, PROCESSING-BE-002.2-S001, PROCESSING-BE-002.2-S002, PROCESSING-BE-002.2-S003, PROCESSING-STORY-002-S004 |
| TC-1 – Python ≥ 3.12 | PROCESSING-INFRA-002.2-S003 |
| TC-3 – Standard library only | PROCESSING-INFRA-002.2-S002 |
| TC-4 – Plain-text files | PROCESSING-INFRA-002.3-S001, PROCESSING-INFRA-002.3-S002, PROCESSING-INFRA-002.3-S003 |
| TC-5 – unittest | Note: Docker uses pytest, not unittest (PROCESSING-INFRA-002.1) |
| ADR-001 – Single CLI, no external services | PROCESSING-INFRA-002.4-S003 |
| ADR-002 – File I/O confined to Processor | PROCESSING-INFRA-002.3-S001, PROCESSING-INFRA-002.3-S002, PROCESSING-INFRA-002.3-S003 |
| Dockerfile – Local Docker environment | PROCESSING-INFRA-002.1-S001, PROCESSING-INFRA-002.1-S004, PROCESSING-INFRA-002.2-S001, PROCESSING-INFRA-002.2-S004 |
| CI workflow – GitHub Actions | PROCESSING-INFRA-002.2-S004, PROCESSING-INFRA-002.4-S005 |
| QS-04 – Output annotation accuracy | PROCESSING-STORY-002-S001, PROCESSING-STORY-002-S002, PROCESSING-STORY-002-S003, PROCESSING-BE-002.2-S001, PROCESSING-BE-002.2-S002, PROCESSING-BE-002.2-S003 |
| QS-07 – Test suite runs with no external dependencies | PROCESSING-INFRA-002.4-S001, PROCESSING-INFRA-002.4-S005 – Note: `pytest` is a third-party test dependency, creating a discrepancy with the original QS-7 requirement for dependency-free testing |
| QS-08 – Changing digit recognition does not affect validation | PROCESSING-INFRA-002.3-S001 |
| QS-09 – Changing output format does not affect parsing or validation | PROCESSING-BE-002.2-S001, PROCESSING-BE-002.2-S002, PROCESSING-BE-002.2-S003 |
| QS-10 – No unjustified dependencies | PROCESSING-INFRA-002.2-S002 |
| QS-11 – Single command invocation | PROCESSING-INFRA-002.2-S001, PROCESSING-INFRA-002.2-S005, PROCESSING-INFRA-002.4-S002 |
| ch. 6.3 – Runtime invariants (Parser and Validator called once per entry) | PROCESSING-STORY-002-S005, PROCESSING-BE-002.1-S001, PROCESSING-BE-002.1-S002 |
| ch. 8.1 – No entry silently dropped | PROCESSING-STORY-002-S004, PROCESSING-BE-002.1-S003 |
| ch. 8.4 – Input format handling owned by Processor | PROCESSING-INFRA-002.3-S001 |
| RISK-03 – No integration test covers full pipeline end-to-end | PROCESSING-INFRA-002.1-S002, PROCESSING-INFRA-002.1-S003 |
| DEBT-03 – No structured logging | PROCESSING-INFRA-002.4-S003 |

---

**Bundle status:** Approved

---

## PROCESSING-STORY-001 – Read Input File and Split into Account Entries

**Domain:** PROCESSING
**Story ID:** PROCESSING-STORY-001
**Title:** Read input file and split into account entries
**Priority:** Supporting
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-1)
- `architecture/02-constraints.md`, Section 2.1 (TC-2, TC-4)
- `architecture/04-solution-strategy.md`, Section 4.3 (processing strategy, step 1)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor component, dependency rules)
- `architecture/06-runtime-view.md`, Section 6.1 (Steps 1–2), Section 6.3 (runtime invariants)
- `architecture/08-crosscutting-concepts.md`, Sections 8.2, 8.4 (I/O separation, input format handling)
- `architecture/09-architecture-decisions.md`, ADR-002
- `architecture/10-quality-requirements.md`, QS-11
- `architecture/11-risks-and-technical-debt.md`, RISK-02, DEBT-01

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to read my plain-text input file and correctly identify each account entry within it,
**SO THAT** every account number in the file is available for parsing and validation.

---

### Acceptance Scenarios

### SCENARIO 1: Read a file containing one account entry and produce one four-line entry string
**Scenario ID:** PROCESSING-STORY-001-S001
**GIVEN** a plain-text input file containing exactly four lines (three glyph rows of 27 characters each followed by one blank line)
**WHEN** the Processor reads and splits the file
**THEN** it produces exactly one four-line entry string ready to be passed to the Parser

### SCENARIO 2: Read a file containing multiple account entries and produce one entry string per entry
**Scenario ID:** PROCESSING-STORY-001-S002
**GIVEN** a plain-text input file containing N groups of four lines, each group consisting of three glyph rows followed by one blank line
**WHEN** the Processor reads and splits the file
**THEN** it produces exactly N four-line entry strings in the same order as they appear in the file

### SCENARIO 3: Preserve the exact line content of each entry without alteration
**Scenario ID:** PROCESSING-STORY-001-S003
**GIVEN** a plain-text input file whose entries each contain specific ASCII glyph patterns
**WHEN** the Processor splits the file into entries
**THEN** each resulting entry string contains the exact three glyph rows from the input file, with no characters added, removed, or reordered

### SCENARIO 4: Report a clear error for a file whose line count is not a multiple of four
**Scenario ID:** PROCESSING-STORY-001-S004
**GIVEN** a plain-text input file whose total number of lines is not a multiple of four
**WHEN** the Processor attempts to read and split the file
**THEN** it reports a diagnostic message identifying the format error and does not pass any malformed entry to the Parser

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3).

---

### Backend Stories

#### PROCESSING-BE-001.1 – Implement plain-text input file reading

**Story ID:** PROCESSING-BE-001.1
**Parent story:** PROCESSING-STORY-001
**Priority:** Supporting
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-1)
- `architecture/02-constraints.md`, Section 2.1 (TC-4)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor owns file system access)
- `architecture/06-runtime-view.md`, Section 6.1 (Steps 1–2)
- `architecture/09-architecture-decisions.md`, ADR-002

**AS A** BankOCR developer,
**I WANT** the Processor to open and read the plain-text input file from the local file system using only standard-library file I/O,
**SO THAT** the full content of the file is available in memory for entry splitting before any parsing begins.

#### Acceptance Scenarios

### SCENARIO 1: Read all lines from a valid input file into memory
**Scenario ID:** PROCESSING-BE-001.1-S001
**GIVEN** a plain-text input file present on the local file system
**WHEN** the Processor opens and reads the file
**THEN** all lines are loaded into memory and the file handle is closed on completion

### SCENARIO 2: Handle a missing input file with a clear diagnostic
**Scenario ID:** PROCESSING-BE-001.1-S002
**GIVEN** an input file path supplied to the Processor that does not correspond to an existing file
**WHEN** the Processor attempts to open the file
**THEN** it reports a diagnostic message identifying the missing file and does not proceed to entry splitting or parsing

### SCENARIO 3: Read the file without altering its content
**Scenario ID:** PROCESSING-BE-001.1-S003
**GIVEN** a plain-text input file with known content
**WHEN** the Processor reads the file
**THEN** the lines held in memory exactly match the original file content, with no characters added, removed, or modified

---

#### PROCESSING-BE-001.2 – Split file lines into four-line account entry strings

**Story ID:** PROCESSING-BE-001.2
**Parent story:** PROCESSING-STORY-001
**Priority:** Supporting
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-1)
- `architecture/02-constraints.md`, Section 2.1 (TC-2)
- `architecture/04-solution-strategy.md`, Section 4.3 (processing strategy, step 1)
- `architecture/08-crosscutting-concepts.md`, Section 8.4 (input format handling; Parser assumes pre-sliced entry)

**AS A** BankOCR developer,
**I WANT** the Processor to group the file's lines into consecutive four-line blocks and represent each block as a single string argument,
**SO THAT** the Parser receives one correctly bounded account entry per call, exactly as the architecture requires.

#### Acceptance Scenarios

### SCENARIO 1: Group N×4 lines into N four-line entry strings
**Scenario ID:** PROCESSING-BE-001.2-S001
**GIVEN** a list of lines read from a valid input file whose length is a multiple of four
**WHEN** the Processor applies the entry-splitting logic
**THEN** it produces a list of N strings each containing exactly four lines (three glyph rows and one blank line), in input order

### SCENARIO 2: Each entry string spans lines 4k+1 through 4k+4 for entry k
**Scenario ID:** PROCESSING-BE-001.2-S002
**GIVEN** a valid input file containing at least two account entries
**WHEN** the Processor splits the file into entries
**THEN** the first entry contains lines 1–4, the second entry contains lines 5–8, and each subsequent entry follows the same four-line stride with no lines shared between entries

### SCENARIO 3: Reject a file whose line count is not a multiple of four before splitting
**Scenario ID:** PROCESSING-BE-001.2-S003
**GIVEN** a list of lines whose total count is not a multiple of four
**WHEN** the Processor applies the entry-splitting logic
**THEN** it reports a diagnostic message and returns no entry strings, preventing any malformed data from reaching the Parser

---

### Infrastructure Stories

#### PROCESSING-INFRA-001.1 – Test input file reading and entry splitting using unittest with temporary files

**Story ID:** PROCESSING-INFRA-001.1
**Parent story:** PROCESSING-STORY-001
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Processor tests may use temporary files)
- `architecture/10-quality-requirements.md`, QS-07
- `architecture/11-risks-and-technical-debt.md`, RISK-02, DEBT-01

**AS A** BankOCR developer,
**I WANT** the Processor's file-reading and entry-splitting logic to be covered by `unittest` tests that use temporary input files,
**SO THAT** format-error handling and correct entry boundaries are verified automatically.

#### Acceptance Scenarios

### SCENARIO 1: Test correctly splits a temporary file into the expected number of entries
**Scenario ID:** PROCESSING-INFRA-001.1-S001
**GIVEN** a `unittest` test case that creates a temporary input file containing a known number of well-formed account entries
**WHEN** the Processor's splitting logic is exercised against that file
**THEN** the test asserts that the number and content of returned entry strings match the expected values

### SCENARIO 2: Test verifies that a malformed file produces a diagnostic and no entries
**Scenario ID:** PROCESSING-INFRA-001.1-S002
**GIVEN** a `unittest` test case that creates a temporary input file whose line count is not a multiple of four
**WHEN** the Processor's splitting logic is exercised against that file
**THEN** the test asserts that a diagnostic is reported and no entry strings are returned

### SCENARIO 3: Temporary files are cleaned up after each test
**Scenario ID:** PROCESSING-INFRA-001.1-S003
**GIVEN** a `unittest` test case that creates a temporary input file
**WHEN** the test completes, whether passing or failing
**THEN** the temporary file is removed from the file system, leaving no test artefacts on disk

---

#### PROCESSING-INFRA-001.2 – Confirm plain-text file as the sole data storage mechanism for input

**Story ID:** PROCESSING-INFRA-001.2
**Parent story:** PROCESSING-STORY-001
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-4)
- `architecture/03-context-and-scope.md`, Section 3.3 (plain-text file input channel)
- `architecture/09-architecture-decisions.md`, ADR-001 (no database or binary format)

**AS A** BankOCR developer,
**I WANT** the Processor to read account entry data exclusively from a plain-text file on the local file system, with no database, binary format, or network source involved,
**SO THAT** the input data handling remains consistent with the approved architecture and requires no additional infrastructure.

#### Acceptance Scenarios

### SCENARIO 1: Input is read from a plain-text file, not a database or network source
**Scenario ID:** PROCESSING-INFRA-001.2-S001
**GIVEN** the Processor module source code
**WHEN** the input-reading logic is inspected
**THEN** it reads from a local file path using standard file I/O; no database connection, network socket, or binary deserialisation is present (TC-4, ADR-001)

### SCENARIO 2: Input file is opened in text mode, not binary mode
**Scenario ID:** PROCESSING-INFRA-001.2-S002
**GIVEN** the Processor opens the input file
**WHEN** the file open call is inspected
**THEN** the file is opened in text mode so that lines are read as strings, consistent with the plain-text format specified in TC-4

### SCENARIO 3: No in-memory data persists between separate CLI invocations
**Scenario ID:** PROCESSING-INFRA-001.2-S003
**GIVEN** the CLI is invoked twice in sequence with different input files
**WHEN** each invocation completes
**THEN** the data read during the first invocation is not accessible during the second; each run starts from a clean state with no shared in-memory storage

---

#### PROCESSING-INFRA-001.3 – Confirm event inapplicability and define observability for file reading errors

**Story ID:** PROCESSING-INFRA-001.3
**Parent story:** PROCESSING-STORY-001
**Priority:** Supporting
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/10-quality-requirements.md`, QS-07
- `architecture/11-risks-and-technical-debt.md`, RISK-02, DEBT-01, DEBT-03

**AS A** BankOCR developer,
**I WANT** file-reading errors and format violations to be reported as diagnostic messages to stderr and reflected in a non-zero exit code, rather than through event infrastructure,
**SO THAT** input file problems are immediately visible to the user without introducing monitoring services that the architecture does not approve.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the PROCESSING domain. This story documents that determination explicitly and specifies the observability mechanism that applies instead.

#### Acceptance Scenarios

### SCENARIO 1: Missing input file produces a diagnostic message and non-zero exit code
**Scenario ID:** PROCESSING-INFRA-001.3-S001
**GIVEN** the CLI is invoked with a path to a file that does not exist
**WHEN** the Processor attempts to open the file
**THEN** a diagnostic message identifying the missing file is written to stderr and the process exits with a non-zero exit code

### SCENARIO 2: Malformed input file produces a diagnostic message and non-zero exit code
**Scenario ID:** PROCESSING-INFRA-001.3-S002
**GIVEN** the CLI is invoked with a path to a file whose line count is not a multiple of four
**WHEN** the Processor reads and attempts to split the file
**THEN** a diagnostic message identifying the format error is written to stderr and the process exits with a non-zero exit code

### SCENARIO 3: No event infrastructure is used to report file-reading errors
**Scenario ID:** PROCESSING-INFRA-001.3-S003
**GIVEN** the Processor module source code
**WHEN** the error-reporting logic for file-reading and format failures is inspected
**THEN** errors are reported using standard output streams (stderr) and exit codes only; no message queue, event bus, or external monitoring service is called

---

### DDD Analysis

**Bounded context:** PROCESSING — same bounded context as PROCESSING-STORY-002. This story focuses on the file-reading and entry-splitting responsibilities of the Processor, which precede the pipeline coordination covered by PROCESSING-STORY-002.

**Conceptual domain elements relevant to this story** (subset of the PROCESSING bounded context elements defined in PROCESSING-STORY-002):

| Element | Type | Description |
|---------|------|-------------|
| `ProcessingRun` | Aggregate root | One complete execution. This story covers its initialisation: locating the input file, reading its lines, and producing the ordered `AccountEntry` sequence that the pipeline loop will consume. |
| `InputFilePath` | Value object | The path to the plain-text input file supplied by the user. Validated by the Processor: the file must exist and its line count must be a multiple of four (TC-2, ch. 8.4, RISK-02). |
| `AccountEntry` | Entity (within ProcessingRun) | One four-line ASCII account entry produced by splitting the input file. Identified by its zero-based position within the file. This story is responsible for producing the ordered sequence of `AccountEntry` strings; PROCESSING-STORY-002 is responsible for processing each one. |

**Domain rules enforced at this stage:**
1. The input file must be present and readable before any splitting is attempted.
2. The file's total line count must be a multiple of four; a non-conforming file is rejected with a diagnostic before any `AccountEntry` is produced (TC-2, ch. 8.4).
3. Each `AccountEntry` spans exactly four consecutive lines starting from position 4k (zero-based) for entry k; no line belongs to more than one entry.
4. The order of `AccountEntry` strings produced by splitting must match the order in which their corresponding entries appear in the input file.

**Relationship to PROCESSING-STORY-002:** The entry sequence produced by this story is the input consumed by the pipeline loop in PROCESSING-STORY-002. These two stories together cover the full Processor responsibility defined in `architecture/05-building-block-view.md`, Section 5.2.

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-1 – Read input file and split into four-line entries | PROCESSING-STORY-001, PROCESSING-BE-001.1, PROCESSING-BE-001.1-S001, PROCESSING-BE-001.2, PROCESSING-BE-001.2-S001, PROCESSING-BE-001.2-S002 |
| TC-2 – Four-line entry format | PROCESSING-STORY-001-S001, PROCESSING-STORY-001-S002, PROCESSING-BE-001.2-S001, PROCESSING-BE-001.2-S002, PROCESSING-BE-001.2-S003 |
| TC-4 – Plain-text files | PROCESSING-BE-001.1-S001, PROCESSING-INFRA-001.2-S001, PROCESSING-INFRA-001.2-S002 |
| TC-1 – Python ≥ 3.12 | PROCESSING-INFRA-001.1-S001 |
| TC-3 – Standard library only | PROCESSING-INFRA-001.1-S001 |
| TC-5 – unittest | PROCESSING-INFRA-001.1-S001, PROCESSING-INFRA-001.3-S001 |
| ADR-001 – Single CLI, no database or external services | PROCESSING-INFRA-001.2-S001, PROCESSING-INFRA-001.3-S003 |
| ADR-002 – File I/O confined to Processor | PROCESSING-BE-001.1-S001, PROCESSING-BE-001.1-S003 |
| QS-07 – Test suite runs with no external dependencies | PROCESSING-INFRA-001.1-S001 |
| QS-11 – Single command invocation | PROCESSING-BE-001.1-S002, PROCESSING-INFRA-001.3-S001 |
| ch. 6.1 – Runtime steps 1–2 (Processor reads and splits file) | PROCESSING-STORY-001-S001, PROCESSING-STORY-001-S002, PROCESSING-BE-001.1-S001, PROCESSING-BE-001.2-S001 |
| ch. 8.4 – Input format handling owned by Processor | PROCESSING-STORY-001-S004, PROCESSING-BE-001.2-S003, PROCESSING-INFRA-001.3-S002 |
| RISK-02 – Input file format validation not yet implemented | PROCESSING-STORY-001-S004, PROCESSING-BE-001.2-S003, PROCESSING-INFRA-001.1-S002, PROCESSING-INFRA-001.3-S002 |
| DEBT-01 – Input file validation logic and tests are pending | PROCESSING-STORY-001-S004, PROCESSING-BE-001.2-S003, PROCESSING-INFRA-001.1-S002 |
| DEBT-03 – No structured logging | PROCESSING-INFRA-001.3-S003 |

---

**Bundle status:** Approved

---

## PROCESSING-STORY-003 – Write Annotated Results File

**Domain:** PROCESSING
**Story ID:** PROCESSING-STORY-003
**Title:** Write annotated results file
**Priority:** Supporting
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-7)
- `architecture/02-constraints.md`, Section 2.1 (TC-4)
- `architecture/03-context-and-scope.md`, Section 3.3 (output file channel)
- `architecture/04-solution-strategy.md`, Section 4.3 (processing strategy, step 3: Record)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor writes results file)
- `architecture/06-runtime-view.md`, Section 6.1 (Step 8), Section 6.3 (runtime invariants)
- `architecture/08-crosscutting-concepts.md`, Sections 8.1, 8.2
- `architecture/09-architecture-decisions.md`, ADR-002
- `architecture/10-quality-requirements.md`, QS-04, QS-09

---

### Scope distinction

This story covers the **file-writing** responsibility of the Processor: opening the output file, writing the complete ordered sequence of result lines to it, and closing it. The **content** of each individual result line (which suffix to append based on Validator status) was specified in PROCESSING-BE-002.2 as part of PROCESSING-STORY-002. These two stories together cover the full output side of the Processor's responsibility (FR-7).

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to write every result line to a plain-text output file in the same order as the input entries,
**SO THAT** I can read the validation results for all my account numbers from a single file after the application completes.

---

### Acceptance Scenarios

### SCENARIO 1: Write one result line per entry to the output file
**Scenario ID:** PROCESSING-STORY-003-S001
**GIVEN** an input file containing N account entries that have been processed through the pipeline
**WHEN** the Processor writes the results file
**THEN** the output file contains exactly N lines, one per input entry, with no lines added or omitted

### SCENARIO 2: Write result lines in the same order as the input entries
**Scenario ID:** PROCESSING-STORY-003-S002
**GIVEN** an input file containing multiple account entries in a known order
**WHEN** the Processor writes the results file
**THEN** the result lines appear in the output file in the same left-to-right, top-to-bottom order as the corresponding entries in the input file

### SCENARIO 3: Output file is a readable plain-text file on the local file system after the run
**Scenario ID:** PROCESSING-STORY-003-S003
**GIVEN** the Processor has completed processing all entries
**WHEN** the output file is opened with any plain-text reader
**THEN** every result line is present and readable, and the file contains no binary or non-printable characters beyond standard line endings

### SCENARIO 4: Output file contains correct annotations matching each entry's pipeline result
**Scenario ID:** PROCESSING-STORY-003-S004
**GIVEN** an input file containing a mix of VALID, ERR, and ILL account entries
**WHEN** the Processor writes the results file
**THEN** each result line carries exactly the annotation determined by the Validator for that entry: no suffix for VALID, ` ERR` for ERR, and ` ILL` for ILL

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3). The output file is the sole delivery channel for results to the user.

---

### Backend Stories

#### PROCESSING-BE-003.1 – Write the complete ordered sequence of result lines to the output file

**Story ID:** PROCESSING-BE-003.1
**Parent story:** PROCESSING-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-7)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor writes results file)
- `architecture/06-runtime-view.md`, Section 6.1 (Step 8: Processor writes completed results file), Section 6.3 (every entry produces exactly one output line)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (no entry silently dropped)

**AS A** BankOCR developer,
**I WANT** the Processor to open the output file, write each result line in input order, and close the file on completion,
**SO THAT** the output file is a complete and consistent record of every account entry's pipeline result.

#### Acceptance Scenarios

### SCENARIO 1: Open the output file, write all result lines, and close the file
**Scenario ID:** PROCESSING-BE-003.1-S001
**GIVEN** a sequence of N result lines produced by the pipeline
**WHEN** the Processor writes the results file
**THEN** it opens the output file, writes all N lines in order, and closes the file handle on completion without leaving it open

### SCENARIO 2: Write result lines in the order the pipeline produced them
**Scenario ID:** PROCESSING-BE-003.1-S002
**GIVEN** a sequence of result lines produced in the same order as the input entries
**WHEN** the Processor writes those lines to the output file
**THEN** the first line in the output file corresponds to the first input entry, the second to the second, and so on for all N entries

### SCENARIO 3: Every result line is written; none are omitted
**Scenario ID:** PROCESSING-BE-003.1-S003
**GIVEN** a pipeline that produced N result lines for N input entries
**WHEN** the Processor writes the results file
**THEN** the output file contains exactly N lines and no entry's result is absent

---

#### PROCESSING-BE-003.2 – Use plain-text format and standard line endings for the output file

**Story ID:** PROCESSING-BE-003.2
**Parent story:** PROCESSING-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-4)
- `architecture/03-context-and-scope.md`, Section 3.3 (output file: plain text)
- `architecture/09-architecture-decisions.md`, ADR-001 (no database or binary format)

**AS A** BankOCR developer,
**I WANT** the Processor to write the output file as a plain-text file using standard line endings,
**SO THAT** the results file is readable by any text editor or downstream tool without requiring a special format or encoding.

#### Acceptance Scenarios

### SCENARIO 1: Output file is written in text mode with standard line endings
**Scenario ID:** PROCESSING-BE-003.2-S001
**GIVEN** the Processor writes the output file
**WHEN** the file open call is inspected
**THEN** the file is opened in text mode so that each result line is terminated by the platform's standard line ending, consistent with TC-4

### SCENARIO 2: Output file contains only printable ASCII characters and line endings
**Scenario ID:** PROCESSING-BE-003.2-S002
**GIVEN** the Processor has written the output file for a run containing VALID, ERR, and ILL entries
**WHEN** the output file is read back
**THEN** every character in the file is either a printable ASCII character (digit, space, or annotation letter) or a standard line ending; no binary or control characters are present

### SCENARIO 3: Output file uses no binary serialisation or database format
**Scenario ID:** PROCESSING-BE-003.2-S003
**GIVEN** the Processor module source code
**WHEN** the output-writing logic is inspected
**THEN** it uses standard-library text file I/O only; no binary serialisation, database write, or third-party format library is used (TC-4, ADR-001)

---

### Infrastructure Stories

#### PROCESSING-INFRA-003.1 – Test output file writing using unittest with temporary files

**Story ID:** PROCESSING-INFRA-003.1
**Parent story:** PROCESSING-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Processor tests may use temporary files)
- `architecture/10-quality-requirements.md`, QS-07

**AS A** BankOCR developer,
**I WANT** the Processor's output file writing to be covered by `unittest` tests that read back a temporary output file and assert on its content,
**SO THAT** ordering, completeness, and annotation correctness of the output file are verified automatically.

#### Acceptance Scenarios

### SCENARIO 1: Test asserts that output file contains correct number of lines in correct order
**Scenario ID:** PROCESSING-INFRA-003.1-S001
**GIVEN** a `unittest` test case that runs the Processor against a temporary input file with a known number of entries
**WHEN** the Processor writes the output file
**THEN** the test reads the output file and asserts that it contains exactly the expected number of lines in the expected order

### SCENARIO 2: Test asserts correct annotations for VALID, ERR, and ILL entries
**Scenario ID:** PROCESSING-INFRA-003.1-S002
**GIVEN** a `unittest` test case whose temporary input file contains at least one VALID, one ERR, and one ILL account entry
**WHEN** the Processor writes the output file
**THEN** the test asserts that each result line carries the correct annotation: no suffix, ` ERR`, or ` ILL` respectively

### SCENARIO 3: Temporary output files are cleaned up after each test
**Scenario ID:** PROCESSING-INFRA-003.1-S003
**GIVEN** a `unittest` test case that causes the Processor to write a temporary output file
**WHEN** the test completes, whether passing or failing
**THEN** the temporary output file is removed from the file system, leaving no test artefacts on disk

---

#### PROCESSING-INFRA-003.2 – Confirm plain-text file as the sole output data storage mechanism

**Story ID:** PROCESSING-INFRA-003.2
**Parent story:** PROCESSING-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-4)
- `architecture/03-context-and-scope.md`, Section 3.3 (output file channel)
- `architecture/09-architecture-decisions.md`, ADR-001 (no database or binary format), ADR-002 (file I/O confined to Processor)

**AS A** BankOCR developer,
**I WANT** the Processor to write account results exclusively to a plain-text file on the local file system, with no database, binary format, or network destination involved,
**SO THAT** the output data handling remains consistent with the approved architecture and requires no additional infrastructure.

#### Acceptance Scenarios

### SCENARIO 1: Results are written to a plain-text file, not a database or network destination
**Scenario ID:** PROCESSING-INFRA-003.2-S001
**GIVEN** the Processor module source code
**WHEN** the output-writing logic is inspected
**THEN** it writes to a local file path using standard text file I/O; no database connection, network socket, or binary serialisation is present (TC-4, ADR-001)

### SCENARIO 2: Only the Processor writes the output file
**Scenario ID:** PROCESSING-INFRA-003.2-S002
**GIVEN** the full pipeline execution for a valid input file
**WHEN** all file-write operations on the output file path are traced
**THEN** every write originates from the Processor; the Parser and Validator make no write calls to the output file (ADR-002)

### SCENARIO 3: No result data persists between separate CLI invocations
**Scenario ID:** PROCESSING-INFRA-003.2-S003
**GIVEN** the CLI is invoked twice in sequence with different input files and different output file paths
**WHEN** each invocation completes
**THEN** each output file contains only the results from its corresponding invocation; no result data from one run appears in the other run's output file

---

#### PROCESSING-INFRA-003.3 – Confirm event inapplicability and define observability for output file writing

**Story ID:** PROCESSING-INFRA-003.3
**Parent story:** PROCESSING-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/10-quality-requirements.md`, QS-04, QS-07
- `architecture/11-risks-and-technical-debt.md`, DEBT-03

**AS A** BankOCR developer,
**I WANT** output file write failures to be reported as diagnostic messages to stderr with a non-zero exit code, and successful writes to be confirmed by exit code 0, rather than through event infrastructure,
**SO THAT** output file problems are immediately visible to the user without introducing monitoring services that the architecture does not approve.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the PROCESSING domain. This story documents that determination explicitly and specifies the observability mechanism that applies instead.

#### Acceptance Scenarios

### SCENARIO 1: Successful output file write results in exit code 0
**Scenario ID:** PROCESSING-INFRA-003.3-S001
**GIVEN** the CLI is invoked with a valid input file and a writable output file path
**WHEN** the Processor writes all result lines and closes the output file without error
**THEN** the process exits with exit code 0

### SCENARIO 2: Output file write failure produces a diagnostic message and non-zero exit code
**Scenario ID:** PROCESSING-INFRA-003.3-S002
**GIVEN** the CLI is invoked with a valid input file but an output file path that cannot be written (for example, a path in a non-existent directory)
**WHEN** the Processor attempts to open or write the output file
**THEN** a diagnostic message identifying the write failure is written to stderr and the process exits with a non-zero exit code

### SCENARIO 3: No event infrastructure is used to report output file write status
**Scenario ID:** PROCESSING-INFRA-003.3-S003
**GIVEN** the Processor module source code
**WHEN** the output-writing and error-reporting logic is inspected
**THEN** write status is communicated using exit codes and stderr only; no message queue, event bus, or external monitoring service is called

---

### DDD Analysis

**Bounded context:** PROCESSING — same bounded context as PROCESSING-STORY-001 and PROCESSING-STORY-002. This story focuses on the output file writing responsibility of the Processor, which follows the pipeline coordination covered by PROCESSING-STORY-002.

**Conceptual domain elements relevant to this story** (subset of the PROCESSING bounded context elements defined in PROCESSING-STORY-002):

| Element | Type | Description |
|---------|------|-------------|
| `ProcessingRun` | Aggregate root | One complete execution. This story covers its finalisation: writing the ordered sequence of `ResultLine` values to the output file and closing it. |
| `ResultLine` | Value object | The formatted output string for one account entry, produced during pipeline coordination (PROCESSING-STORY-002). Immutable once produced. This story is responsible for persisting the full ordered sequence of `ResultLine` values to the output file. |
| `OutputFilePath` | Value object | The path to the plain-text output file written by the Processor on completion. Validated before writing: the path must be writable. |

**Domain rules enforced at this stage:**
1. The output file is written only after the full pipeline has been run for all entries; partial writes mid-pipeline are not performed.
2. Every `ResultLine` in the sequence is written to the output file; none are dropped (ch. 8.1, ch. 6.3).
3. `ResultLine` values are written in the same order they were produced, which matches input entry order.
4. The output file is a plain-text file; no binary or database format is used (TC-4, ADR-001).
5. Only the Processor writes the output file (ADR-002).

**Relationship to PROCESSING-STORY-002:** PROCESSING-STORY-002 covers pipeline coordination and result line formatting (how each `ResultLine` string is constructed). This story covers output file writing (how the complete sequence of `ResultLine` strings is persisted to disk). Together with PROCESSING-STORY-001 (input file reading) they span the full Processor responsibility defined in `architecture/05-building-block-view.md`, Section 5.2.

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-7 – Write one annotated result line per entry to the output file | PROCESSING-STORY-003, PROCESSING-BE-003.1, PROCESSING-BE-003.1-S001, PROCESSING-BE-003.1-S002, PROCESSING-BE-003.1-S003 |
| TC-4 – Plain-text files | PROCESSING-BE-003.2-S001, PROCESSING-BE-003.2-S002, PROCESSING-BE-003.2-S003, PROCESSING-INFRA-003.2-S001 |
| TC-1 – Python ≥ 3.12 | PROCESSING-INFRA-003.1-S001 |
| TC-3 – Standard library only | PROCESSING-INFRA-003.1-S001 |
| TC-5 – unittest | PROCESSING-INFRA-003.1-S001, PROCESSING-INFRA-003.3-S001 |
| ADR-001 – Single CLI, no database or external services | PROCESSING-BE-003.2-S003, PROCESSING-INFRA-003.2-S001, PROCESSING-INFRA-003.3-S003 |
| ADR-002 – File I/O confined to Processor | PROCESSING-INFRA-003.2-S002 |
| QS-04 – Output annotation accuracy | PROCESSING-STORY-003-S004, PROCESSING-INFRA-003.1-S002 |
| QS-07 – Test suite runs with no external dependencies | PROCESSING-INFRA-003.1-S001 |
| QS-09 – Changing output format does not affect parsing or validation | PROCESSING-BE-003.1-S001, PROCESSING-BE-003.2-S001 |
| ch. 6.1 – Step 8: Processor writes completed results file | PROCESSING-STORY-003-S001, PROCESSING-STORY-003-S002, PROCESSING-BE-003.1-S001 |
| ch. 6.3 – Every entry produces exactly one output line | PROCESSING-STORY-003-S001, PROCESSING-BE-003.1-S003 |
| ch. 8.1 – No entry silently dropped | PROCESSING-STORY-003-S001, PROCESSING-BE-003.1-S003 |
| ch. 8.2 – Separation of I/O from logic | PROCESSING-INFRA-003.2-S002 |
| DEBT-03 – No structured logging | PROCESSING-INFRA-003.3-S003 |

---

**Bundle status:** Approved

---

## PROCESSING-STORY-005 – Invoke the Application via a Single CLI Command

**Domain:** PROCESSING
**Story ID:** PROCESSING-STORY-005
**Title:** Invoke the application via a single CLI command
**Priority:** Supporting
**Status:** Approved
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3)
- `architecture/04-solution-strategy.md`, Section 4.1 (single CLI application, no server or network interface)
- `architecture/05-building-block-view.md`, Section 5.1 (BankOCR CLI container), Section 5.2 (Processor coordinates execution; Parser and Validator have no CLI dependency)
- `architecture/07-deployment-view.md`, Sections 7.1, 7.2, 7.3
- `architecture/10-quality-requirements.md`, QS-10, QS-11

---

### Scope distinction

PROCESSING-STORY-001 covers reading and splitting the input file inside the Processor. PROCESSING-STORY-002 covers the per-entry pipeline loop. PROCESSING-STORY-003 covers writing the output file. This story covers the outermost shell: how the user invokes the application from the command line, how CLI arguments are parsed and validated, how the Processor is started from the entry point, and what the user sees when the invocation itself is incorrect. It does not revisit what happens inside the Processor once it starts.

---

### Original User Story

**AS A** BankOCR user,
**I WANT** to run the entire application with a single command that accepts the input and output file paths as arguments,
**SO THAT** I can process any account number file on any machine that has Python ≥ 3.12 installed, without installing packages, running a build, or editing a configuration file.

---

### Acceptance Scenarios

### SCENARIO 1: Application processes an input file and writes results when invoked with valid arguments
**Scenario ID:** PROCESSING-STORY-005-S001
**GIVEN** a machine with Python ≥ 3.12 and the BankOCR source present, an existing well-formed input file at a known path, and a writable output path
**WHEN** the CLI is invoked with the input file path and the output file path as arguments
**THEN** the application runs the full pipeline to completion, writes the results file, and exits with code 0

### SCENARIO 2: Application runs without any build step or package installation
**Scenario ID:** PROCESSING-STORY-005-S002
**GIVEN** a machine with Python ≥ 3.12 and the BankOCR source files present, and no third-party packages installed
**WHEN** the CLI is invoked
**THEN** the application starts and runs to completion without requiring `pip install`, a Makefile target, a compiled artefact, or any configuration file

### SCENARIO 3: Invoking with no arguments produces a usage diagnostic and a non-zero exit code
**Scenario ID:** PROCESSING-STORY-005-S003
**GIVEN** the CLI is invoked with no arguments
**WHEN** the entry point processes the command line
**THEN** a usage or help message is written to stderr, the application exits with a non-zero exit code, and no input file is read

### SCENARIO 4: Invoking with a missing required argument produces a usage diagnostic and a non-zero exit code
**Scenario ID:** PROCESSING-STORY-005-S004
**GIVEN** the CLI is invoked with only one of the two required file path arguments
**WHEN** the entry point processes the command line
**THEN** a diagnostic message identifying the missing argument is written to stderr and the application exits with a non-zero exit code

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. The CLI itself is the user-facing interface; it accepts file paths as arguments and communicates errors through stderr and exit codes. There is no web interface, GUI, or interactive prompt (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3).

---

### Backend Stories

#### PROCESSING-BE-005.1 – Implement CLI argument parsing for input and output file paths

**Story ID:** PROCESSING-BE-005.1
**Parent story:** PROCESSING-STORY-005
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-3: standard library only)
- `architecture/07-deployment-view.md`, Section 7.1 (input file path supplied at invocation; output file path collected at invocation)
- `architecture/07-deployment-view.md`, Section 7.2 (step 3: invoke CLI with path to input file; step 4: collect output file from path specified at invocation)
- `architecture/10-quality-requirements.md`, QS-11

**AS A** BankOCR developer,
**I WANT** the CLI entry point to parse the input file path and output file path from the command-line arguments using the Python standard library,
**SO THAT** the user can specify both paths at invocation and the Processor receives them without hard-coded defaults.

#### Acceptance Scenarios

### SCENARIO 1: Parse a valid invocation and pass both paths to the Processor
**Scenario ID:** PROCESSING-BE-005.1-S001
**GIVEN** the CLI is invoked with a valid input file path as the first argument and a valid output file path as the second argument
**WHEN** the entry point parses the command line
**THEN** it extracts both paths correctly and passes them to the Processor without modification

### SCENARIO 2: Reject an invocation with no arguments and report the required usage
**Scenario ID:** PROCESSING-BE-005.1-S002
**GIVEN** the CLI is invoked with no arguments
**WHEN** the entry point parses the command line
**THEN** it writes a message describing the required arguments to stderr and exits with a non-zero exit code without calling the Processor

### SCENARIO 3: Use only standard-library modules for argument parsing
**Scenario ID:** PROCESSING-BE-005.1-S003
**GIVEN** the CLI entry point source code
**WHEN** the argument-parsing logic is inspected
**THEN** it uses only Python standard-library modules (such as `argparse` or `sys.argv`); no third-party argument-parsing library is imported (TC-3)

---

#### PROCESSING-BE-005.2 – Start the Processor from the CLI entry point and propagate its exit code

**Story ID:** PROCESSING-BE-005.2
**Parent story:** PROCESSING-STORY-005
**Priority:** Supporting
**Architecture references:**
- `architecture/04-solution-strategy.md`, Section 4.1 (Processor coordinates the pipeline)
- `architecture/05-building-block-view.md`, Section 5.1 (BankOCR CLI container entry point), Section 5.2 (Processor dependency rules: Parser and Validator have no CLI dependency)
- `architecture/07-deployment-view.md`, Section 7.2

**AS A** BankOCR developer,
**I WANT** the CLI entry point to call the Processor with the parsed file paths and exit with the Processor's result code,
**SO THAT** the shell receives a machine-readable signal of success or failure and the Parser and Validator remain unaware of the CLI layer.

#### Acceptance Scenarios

### SCENARIO 1: Successful pipeline run exits with code 0
**Scenario ID:** PROCESSING-BE-005.2-S001
**GIVEN** the CLI is invoked with valid arguments pointing to an existing input file and a writable output path
**WHEN** the Processor completes the full pipeline without an unhandled exception
**THEN** the CLI entry point exits with code 0

### SCENARIO 2: Pipeline failure exits with a non-zero code
**Scenario ID:** PROCESSING-BE-005.2-S002
**GIVEN** the CLI is invoked with valid argument syntax but an input file that cannot be read (for example, the file does not exist)
**WHEN** the Processor encounters the error
**THEN** the CLI entry point exits with a non-zero exit code, confirming the error is propagated from the Processor to the shell

### SCENARIO 3: Parser and Validator are not imported or called by the CLI entry point directly
**Scenario ID:** PROCESSING-BE-005.2-S003
**GIVEN** the CLI entry point source code
**WHEN** its imports and function calls are inspected
**THEN** it imports and calls only the Processor (or a top-level coordination function); it does not import or call the Parser or Validator directly, preserving the dependency rules of ch. 5.2

---

### Infrastructure Stories

#### PROCESSING-INFRA-005.1 – Test CLI argument handling using unittest

**Story ID:** PROCESSING-INFRA-005.1
**Parent story:** PROCESSING-STORY-005
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Processor tests may use temporary files)
- `architecture/10-quality-requirements.md`, QS-07, QS-11

**AS A** BankOCR developer,
**I WANT** the CLI argument-parsing and entry-point logic to be covered by `unittest` tests that simulate command-line invocations,
**SO THAT** correct argument handling, usage diagnostics, and exit codes are verified automatically.

#### Acceptance Scenarios

### SCENARIO 1: Test confirms correct paths are extracted from a valid invocation
**Scenario ID:** PROCESSING-INFRA-005.1-S001
**GIVEN** a `unittest` test case that simulates a valid CLI invocation by supplying an input path and an output path
**WHEN** the entry point's argument-parsing logic is exercised
**THEN** the test asserts that both paths are extracted correctly and no error is raised

### SCENARIO 2: Test confirms a diagnostic and non-zero exit for a no-argument invocation
**Scenario ID:** PROCESSING-INFRA-005.1-S002
**GIVEN** a `unittest` test case that simulates a CLI invocation with no arguments
**WHEN** the entry point's argument-parsing logic is exercised
**THEN** the test asserts that a non-zero exit code is produced and a diagnostic message is present in stderr

### SCENARIO 3: CLI tests run with no third-party dependencies
**Scenario ID:** PROCESSING-INFRA-005.1-S003
**GIVEN** a machine with Python ≥ 3.12 and the BankOCR source present, with no third-party packages installed
**WHEN** the CLI unit tests are executed with `python -m unittest`
**THEN** the tests run to completion without an `ImportError` or missing-dependency error

---

#### PROCESSING-INFRA-005.2 – Confirm deployment: source-only distribution, no build step, Python ≥ 3.12

**Story ID:** PROCESSING-INFRA-005.2
**Parent story:** PROCESSING-STORY-005
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3)
- `architecture/07-deployment-view.md`, Sections 7.1, 7.2, 7.3
- `architecture/10-quality-requirements.md`, QS-10, QS-11

**AS A** BankOCR developer,
**I WANT** the application to be deployable by placing its source files on a machine with Python ≥ 3.12 and invoking the CLI directly, with no packaging, compilation, or installation step,
**SO THAT** the deployment process matches the simplicity requirement of the architecture and no additional tooling is needed.

#### Acceptance Scenarios

### SCENARIO 1: Application runs on Python 3.12 with source files only
**Scenario ID:** PROCESSING-INFRA-005.2-S001
**GIVEN** a machine with Python 3.12 installed and the BankOCR source files present on the local file system
**WHEN** the CLI is invoked with valid arguments
**THEN** the application runs to completion without a `SyntaxError`, version-compatibility error, or missing-module error (TC-1)

### SCENARIO 2: No wheel, egg, compiled extension, or configuration file is required
**Scenario ID:** PROCESSING-INFRA-005.2-S002
**GIVEN** the BankOCR source directory
**WHEN** its contents are inspected
**THEN** running the CLI requires no `.whl`, `.egg`, `.pyc` pre-compilation, `setup.cfg`, or external configuration file beyond the Python source files themselves

### SCENARIO 3: All runtime imports resolve to the Python standard library or other BankOCR source modules
**Scenario ID:** PROCESSING-INFRA-005.2-S003
**GIVEN** the CLI entry point and all modules it imports transitively
**WHEN** every import statement is inspected
**THEN** each resolves to either a Python standard-library module or another BankOCR source file; no third-party package is required at runtime (TC-3)

---

#### PROCESSING-INFRA-005.3 – Confirm plain-text files as the sole I/O channel and event inapplicability

**Story ID:** PROCESSING-INFRA-005.3
**Parent story:** PROCESSING-STORY-005
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-4)
- `architecture/03-context-and-scope.md`, Section 3.3 (input and output channels: plain-text files; no network interfaces)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure, no web interface)
- `architecture/11-risks-and-technical-debt.md`, DEBT-03

**AS A** BankOCR developer,
**I WANT** the CLI to accept file paths as its sole I/O arguments and communicate errors through stderr and exit codes only, with no event infrastructure involved,
**SO THAT** the application's interaction model remains consistent with the approved architecture and requires no additional runtime services.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the CLI layer. This story documents that determination and specifies that all user-facing communication uses stderr, stdout, file paths, and exit codes.

#### Acceptance Scenarios

### SCENARIO 1: CLI accepts only file paths as arguments; no URLs, ports, or connection strings
**Scenario ID:** PROCESSING-INFRA-005.3-S001
**GIVEN** the CLI entry point source code
**WHEN** the argument definitions are inspected
**THEN** the only accepted arguments are file system paths (input file and output file); no network address, port number, database connection string, or message-queue URL is accepted

### SCENARIO 2: All user-facing communication uses stderr, stdout, and exit codes
**Scenario ID:** PROCESSING-INFRA-005.3-S002
**GIVEN** the CLI entry point and its invocation under both success and error conditions
**WHEN** all output channels are observed
**THEN** diagnostic messages are written to stderr, any informational output to stdout, and results to the output file; no external service, socket, or message queue is written to

### SCENARIO 3: No event infrastructure is present in the CLI entry point module
**Scenario ID:** PROCESSING-INFRA-005.3-S003
**GIVEN** the CLI entry point source code
**WHEN** all imports and function calls are inspected
**THEN** no message queue client, event bus, logging framework, or external monitoring service is imported or called; the entry point contains only argument parsing, Processor invocation, and exit-code propagation

---

### DDD Analysis

**Bounded context:** PROCESSING — same bounded context as the other PROCESSING stories. This story covers the CLI layer that is the outermost boundary of the `ProcessingRun` aggregate: it is responsible for accepting user input (file paths from the command line), validating the invocation, constructing the parameters needed to start a `ProcessingRun`, and delegating to the Processor.

**Conceptual domain elements relevant to this story** (extending and referencing elements defined in earlier PROCESSING stories):

| Element | Type | Description |
|---------|------|-------------|
| `CliInvocation` | Value object | The parsed result of a single command-line call: an `InputFilePath` and an `OutputFilePath` extracted from `sys.argv`. Valid only when both paths are present; invalid otherwise. Immutable once parsed. |
| `InputFilePath` | Value object | As defined in PROCESSING-STORY-001. This story adds the constraint that it must be supplied by the user at the command line; there is no default value. |
| `OutputFilePath` | Value object | As defined in PROCESSING-STORY-003. This story adds the constraint that it must be supplied by the user at the command line; there is no default value. |
| `ProcessingRun` | Aggregate root | As defined in PROCESSING-STORY-002. This story covers the initiation of a `ProcessingRun`: the CLI entry point creates one by passing a valid `CliInvocation` to the Processor. |

**Domain rules enforced at this stage:**
1. A `CliInvocation` is valid only when both `InputFilePath` and `OutputFilePath` are present; a missing argument is an invocation error, not a file error.
2. An invalid `CliInvocation` is rejected before the Processor is called; no file I/O is attempted on behalf of an invalid invocation.
3. The CLI entry point calls the Processor and no other component; it does not call the Parser or Validator directly (ch. 5.2 dependency rules).
4. The exit code returned to the shell is the Processor's outcome: 0 for success, non-zero for any failure.
5. All user-facing communication from the CLI layer uses stderr (diagnostics), stdout (informational), and plain-text output file (results); no network or event channel is used.

**Relationship to other PROCESSING stories:** PROCESSING-STORY-001, PROCESSING-STORY-002, and PROCESSING-STORY-003 cover the internal Processor responsibilities once a valid invocation has been received. This story covers the boundary at which the user's command-line input enters the system and is translated into a `ProcessingRun`. Together, the four stories span the complete PROCESSING domain responsibility defined in `architecture/05-building-block-view.md`, Section 5.2.

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| TC-1 – Python ≥ 3.12 | PROCESSING-STORY-005-S002, PROCESSING-INFRA-005.2-S001 |
| TC-3 – Standard library only | PROCESSING-BE-005.1-S003, PROCESSING-INFRA-005.1-S003, PROCESSING-INFRA-005.2-S003 |
| TC-4 – Plain-text files | PROCESSING-INFRA-005.3-S001, PROCESSING-INFRA-005.3-S002 |
| ADR-001 – Single CLI, no web interface or event infrastructure | PROCESSING-STORY-005-S002, PROCESSING-INFRA-005.3-S003 |
| ADR-002 – File I/O confined to Processor | PROCESSING-BE-005.2-S003 |
| ch. 5.1 – BankOCR CLI container | PROCESSING-STORY-005-S001, PROCESSING-BE-005.2-S001 |
| ch. 5.2 – Dependency rules: Parser and Validator have no CLI dependency | PROCESSING-BE-005.2-S003, PROCESSING-INFRA-005.3-S003 |
| ch. 7.1 – Deployment topology: CLI invoked with input file path | PROCESSING-STORY-005-S001, PROCESSING-BE-005.1-S001 |
| ch. 7.2 – Deployment steps: invoke CLI, collect output from specified path | PROCESSING-STORY-005-S001, PROCESSING-STORY-005-S002, PROCESSING-BE-005.2-S001 |
| ch. 7.3 – Deployment constraints: Python ≥ 3.12, local execution, no packages | PROCESSING-STORY-005-S002, PROCESSING-INFRA-005.2-S001, PROCESSING-INFRA-005.2-S002, PROCESSING-INFRA-005.2-S003 |
| QS-07 – Test suite runs with no external dependencies | PROCESSING-INFRA-005.1-S003 |
| QS-10 – No unjustified dependencies | PROCESSING-BE-005.1-S003, PROCESSING-INFRA-005.2-S003 |
| QS-11 – Application runs with a single command | PROCESSING-STORY-005-S001, PROCESSING-STORY-005-S002, PROCESSING-BE-005.1-S001, PROCESSING-BE-005.2-S001, PROCESSING-INFRA-005.2-S001 |
| DEBT-03 – No structured logging | PROCESSING-INFRA-005.3-S003 |

---

**Bundle status:** Approved

---

## PROCESSING-STORY-004 – Handle Malformed Input File with a Diagnostic

**Domain:** PROCESSING
**Story ID:** PROCESSING-STORY-004
**Title:** Handle malformed input file with a diagnostic
**Priority:** Supporting
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-1 implicit validation)
- `architecture/04-solution-strategy.md`, Section 4.3 (processing strategy, step 1 validation)
- `architecture/05-building-block-view.md`, Section 5.2 (Processor component, dependency rules)
- `architecture/08-crosscutting-concepts.md`, Section 8.4 (input format handling owned by Processor)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)
- `architecture/10-quality-requirements.md`, QS-04 (correctness), QS-07 (testability)
- `architecture/11-risks-and-technical-debt.md`, RISK-02, DEBT-01 (input file format validation pending)

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to detect when my input file does not follow the four-line entry format and report a clear diagnostic message,
**SO THAT** I can correct the file format before attempting to process it further.

---

### Acceptance Scenarios

### SCENARIO 1: Detect file with non-multiple-of-four line count and report diagnostic
**Scenario ID:** PROCESSING-STORY-004-S001
**GIVEN** a plain-text input file whose total number of lines is not a multiple of four (e.g., 13 lines)
**WHEN** the Processor attempts to read and split the file
**THEN** it reports a clear diagnostic message identifying the format error and exits without writing an output file or calling the Parser

### SCENARIO 2: Detect missing blank line after a three-line glyph block
**Scenario ID:** PROCESSING-STORY-004-S002
**GIVEN** a plain-text input file where a three-line glyph row is not immediately followed by a blank line (e.g., two consecutive glyph rows)
**WHEN** the Processor attempts to split the file into entries
**THEN** it reports a diagnostic message indicating the location of the missing blank separator and does not pass malformed data to the Parser

### SCENARIO 3: Distinguish format errors from CLI argument errors
**Scenario ID:** PROCESSING-STORY-004-S003
**GIVEN** a malformed input file (e.g., wrong number of lines) supplied to the CLI with correct argument syntax
**WHEN** the Processor validates the file format
**THEN** the diagnostic message clearly describes a file format problem, not an argument parsing problem, and distinguishes this from a missing file or permission error

### SCENARIO 4: Fail-fast on malformed input before processing any entries
**Scenario ID:** PROCESSING-STORY-004-S004
**GIVEN** a malformed input file containing some valid entries before the malformed section
**WHEN** the Processor validates the file format
**THEN** it reports the diagnostic and stops before attempting to parse or validate any entries, even those that would have been valid

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3). Format validation diagnostics are reported via stderr and exit codes.

---

### Backend Stories

#### PROCESSING-BE-004.1 – Validate input file format before entry splitting

**Story ID:** PROCESSING-BE-004.1
**Parent story:** PROCESSING-STORY-004
**Priority:** Supporting
**Architecture references:**
- `architecture/08-crosscutting-concepts.md`, Section 8.4 (Processor owns input format validation)
- `architecture/11-risks-and-technical-debt.md`, RISK-02, DEBT-01 (validation logic pending)
- `architecture/04-solution-strategy.md`, Section 4.3 (validation step before parsing)

**AS A** BankOCR developer,
**I WANT** the Processor to validate the input file's conformance to the four-line entry format before attempting to split it into entries,
**SO THAT** malformed files are rejected early and do not produce misleading or partial output.

#### Acceptance Scenarios

### SCENARIO 1: Validate total line count is a multiple of four
**Scenario ID:** PROCESSING-BE-004.1-S001
**GIVEN** the lines read from an input file
**WHEN** the Processor validates the format
**THEN** if the line count is not a multiple of four, it reports a diagnostic and returns no entries; otherwise, it proceeds to entry splitting

### SCENARIO 2: Validate every fourth line is empty (blank separator)
**Scenario ID:** PROCESSING-BE-004.1-S002
**GIVEN** the lines read from an input file with line count a multiple of four
**WHEN** the Processor validates the format
**THEN** it checks that lines 4, 8, 12, … (every fourth line) are empty; if any is non-empty, it reports a diagnostic and returns no entries

### SCENARIO 3: Do not proceed to splitting when format validation fails
**Scenario ID:** PROCESSING-BE-004.1-S003
**GIVEN** an input file that fails format validation (e.g., wrong line count or missing blank line)
**WHEN** the Processor runs its validation logic
**THEN** it returns an error result without creating any entry strings or calling the entry splitting logic

---

#### PROCESSING-BE-004.2 – Generate clear diagnostic messages for format errors

**Story ID:** PROCESSING-BE-004.2
**Parent story:** PROCESSING-STORY-004
**Priority:** Supporting
**Architecture references:**
- `architecture/08-crosscutting-concepts.md`, Section 8.4 (clear error reporting)
- `architecture/10-quality-requirements.md`, QS-04 (correctness)
- `architecture/11-risks-and-technical-debt.md`, RISK-02 (impact: misleading output without diagnostics)

**AS A** BankOCR developer,
**I WANT** the Processor to produce human-readable diagnostic messages that clearly identify the nature and location of format errors,
**SO THAT** users can understand what is wrong with their input file and fix it.

#### Acceptance Scenarios

### SCENARIO 1: Report line count error with total and expected count
**Scenario ID:** PROCESSING-BE-004.2-S001
**GIVEN** an input file with N lines where N is not a multiple of four
**WHEN** the Processor detects the format error
**THEN** it writes a diagnostic to stderr that includes the actual line count (N) and the required multiple-of-four constraint

### SCENARIO 2: Report blank line error with line number and content
**Scenario ID:** PROCESSING-BE-004.2-S002
**GIVEN** an input file where line L (which should be blank) contains non-whitespace characters
**WHEN** the Processor detects the format error
**THEN** it writes a diagnostic to stderr that identifies line number L and shows the unexpected content

### SCENARIO 3: Distinguish format errors from other file errors
**Scenario ID:** PROCESSING-BE-004.2-S003
**GIVEN** multiple possible error conditions (missing file, permission denied, format error)
**WHEN** the Processor reports an error
**THEN** the diagnostic message clearly indicates whether the problem is a missing file, a permission issue, or a format violation, using distinct wording for each case

---

### Infrastructure Stories

#### PROCESSING-INFRA-004.1 – Test malformed input file handling with unittest

**Story ID:** PROCESSING-INFRA-004.1
**Parent story:** PROCESSING-STORY-004
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-5: unittest)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Processor tests may use temporary files)
- `architecture/10-quality-requirements.md`, QS-07 (testability)
- `architecture/11-risks-and-technical-debt.md`, RISK-02 (mitigation: dedicated Processor tests)

**AS A** BankOCR developer,
**I WANT** the Processor's format validation logic to be covered by `unittest` tests that create temporary malformed input files and assert on the resulting diagnostics,
**SO THAT** format error handling is verified automatically and regressions are prevented.

#### Acceptance Scenarios

### SCENARIO 1: Test detects non-multiple-of-four line count error
**Scenario ID:** PROCESSING-INFRA-004.1-S001
**GIVEN** a `unittest` test case that creates a temporary input file with a line count not a multiple of four
**WHEN** the Processor's validation logic is exercised against that file
**THEN** the test asserts that a diagnostic is written to stderr and no entries are produced

### SCENARIO 2: Test detects missing blank separator line
**Scenario ID:** PROCESSING-INFRA-004.1-S002
**GIVEN** a `unittest` test case that creates a temporary input file where a fourth line contains text instead of being blank
**WHEN** the Processor's validation logic is exercised against that file
**THEN** the test asserts that a diagnostic is written to stderr identifying the problematic line and no entries are produced

### SCENARIO 3: Temporary malformed files are cleaned up after test
**Scenario ID:** PROCESSING-INFRA-004.1-S003
**GIVEN** a `unittest` test case that creates a temporary malformed input file
**WHEN** the test completes, whether passing or failing
**THEN** the temporary file is removed from the file system, leaving no test artefacts on disk

---

#### PROCESSING-INFRA-004.2 – Ensure diagnostic reporting uses standard I/O channels, not event infrastructure

**Story ID:** PROCESSING-INFRA-004.2
**Parent story:** PROCESSING-STORY-004
**Priority:** Supporting
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/11-risks-and-technical-debt.md`, DEBT-03 (no structured logging)

**AS A** BankOCR developer,
**I WANT** format validation diagnostics to be written to stderr with appropriate exit codes, without using message queues, logging frameworks, or external monitoring services,
**SO THAT** the error reporting remains consistent with the approved architecture and requires no additional runtime infrastructure.

#### Acceptance Scenarios

### SCENARIO 1: Format error diagnostics are written to stderr
**Scenario ID:** PROCESSING-INFRA-004.2-S001
**GIVEN** the Processor detects a malformed input file
**WHEN** it reports the diagnostic
**THEN** the message is written to the standard error stream (sys.stderr), not to stdout, a log file, or an external service

### SCENARIO 2: Application exits with non-zero code on format error
**Scenario ID:** PROCESSING-INFRA-004.2-S002
**GIVEN** the CLI is invoked with a malformed input file
**WHEN** the Processor detects the format violation
**THEN** the application exits with a non-zero exit code (e.g., 1) to signal failure to the calling shell

### SCENARIO 3: No event infrastructure is used for format error reporting
**Scenario ID:** PROCESSING-INFRA-004.2-S003
**GIVEN** the Processor's format validation logic source code
**WHEN** the diagnostic reporting code is inspected
**THEN** no message queue, event bus, logging framework, or external monitoring service is called; only sys.stderr.write and sys.exit are used

---

#### PROCESSING-INFRA-004.3 – Distinguish format validation from other validation concerns

**Story ID:** PROCESSING-INFRA-004.3
**Parent story:** PROCESSING-STORY-004
**Priority:** Supporting
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (component responsibilities)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (ERR and ILL classification vs format errors)
- `architecture/09-architecture-decisions.md`, ADR-002 (Processor owns format validation; Parser owns glyph recognition; Validator owns checksum)

**AS A** BankOCR developer,
**I WANT** format validation (four-line structure) to remain distinct from glyph recognition (Parser) and checksum validation (Validator), with clear ownership boundaries,
**SO THAT** each component's responsibilities remain aligned with the architecture and format errors do not bleed into the ERR/ILL classification system.

#### Acceptance Scenarios

### SCENARIO 1: Format validation occurs before Parser is called
**Scenario ID:** PROCESSING-INFRA-004.3-S001
**GIVEN** an input file with a format error
**WHEN** the Processor executes its validation logic
**THEN** the error is caught and reported before the Parser receives any entry string; the Parser is never called

### SCENARIO 2: Format errors are not represented as ERR or ILL statuses
**Scenario ID:** PROCESSING-INFRA-004.3-S002
**GIVEN** a malformed input file
**WHEN** the Processor handles the error
**THEN** it does not produce an output file with ERR or ILL annotations; those statuses are reserved for entries that pass format validation but fail glyph recognition or checksum

### SCENARIO 3: Parser and Validator have no format validation responsibilities
**Scenario ID:** PROCESSING-INFRA-004.3-S003
**GIVEN** the Parser and Validator source code
**WHEN** their function signatures and documentation are inspected
**THEN** they assume valid four-line entry format and nine-character account strings respectively; they contain no logic for validating file structure or line counts

---

### DDD Analysis

**Bounded context:** PROCESSING — same bounded context as the other PROCESSING stories. This story covers the validation of the external file format before the system can begin processing entries within the `ProcessingRun` aggregate.

**Conceptual domain elements relevant to this story** (extending and referencing elements defined in earlier PROCESSING stories):

| Element | Type | Description |
|---------|------|-------------|
| `InputFormat` | Value object | The structural requirements of an input file: total line count must be a multiple of four; every fourth line must be blank. This is a validation rule applied by the Processor before any processing begins. |
| `FormatDiagnostic` | Value object | A human-readable error message describing a violation of `InputFormat`. Includes the nature of the violation (wrong line count, missing blank line), location (line number), and possibly the offending content. |
| `InputFilePath` | Value object | As defined in PROCESSING-STORY-001. This story adds that the file must not only exist and be readable but must also satisfy `InputFormat`. |
| `ProcessingRun` | Aggregate root | As defined in PROCESSING-STORY-002. This story adds that a `ProcessingRun` can only be initiated with a file that passes `InputFormat` validation; a malformed file prevents the creation of a valid `ProcessingRun`. |

**Domain rules enforced by this story:**
1. An `InputFilePath` must reference a file that satisfies `InputFormat`; otherwise, it is considered invalid for processing.
2. `InputFormat` validation is performed by the Processor before any entry splitting occurs (fail-fast principle).
3. A format violation results in a `FormatDiagnostic` being reported via stderr and the process exiting with a non-zero code.
4. Format validation is distinct from glyph recognition (Parser) and checksum validation (Validator); format errors are not represented as ERR or ILL statuses.
5. The responsibility for `InputFormat` validation belongs exclusively to the Processor (aligned with ADR-002, ch. 8.4).

**Relationship to other PROCESSING stories:**
- PROCESSING-STORY-001 covers reading and splitting valid input files; this story covers rejecting invalid ones.
- PROCESSING-STORY-002 assumes valid entries are available; this story ensures that assumption holds.
- PROCESSING-STORY-005 (CLI invocation) may pass a malformed file; this story handles the detection and reporting at the Processor boundary.

Together, these stories ensure the Processor fulfills its complete responsibility for input handling defined in `architecture/05-building-block-view.md`, Section 5.2.

**Shared value objects across bounded context boundaries:** None specific to this story. Format validation occurs entirely within the PROCESSING bounded context before any cross-boundary handoffs to PARSING or VALIDATION.

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-1 – Read input file and split into entries (implicit validation) | PROCESSING-STORY-004, PROCESSING-BE-004.1, PROCESSING-BE-004.1-S001, PROCESSING-BE-004.1-S002 |
| TC-5 – unittest | PROCESSING-INFRA-004.1-S001, PROCESSING-INFRA-004.1-S002 |
| ADR-002 – File I/O confined to Processor | PROCESSING-INFRA-004.3-S001, PROCESSING-INFRA-004.3-S003 |
| ch. 8.4 – Input format handling owned by Processor | PROCESSING-STORY-004-S001, PROCESSING-STORY-004-S002, PROCESSING-BE-004.1-S001, PROCESSING-BE-004.1-S002 |
| QS-04 – Output annotation accuracy (corollary: format errors reported clearly) | PROCESSING-STORY-004-S003, PROCESSING-BE-004.2-S003 |
| QS-07 – Test suite runs with no external dependencies | PROCESSING-INFRA-004.1-S001, PROCESSING-INFRA-004.1-S002 |
| RISK-02 – Input file format validation logic is not yet implemented | PROCESSING-STORY-004, PROCESSING-BE-004.1, PROCESSING-INFRA-004.1 |
| DEBT-01 – Input file validation logic and tests pending | PROCESSING-STORY-004, PROCESSING-BE-004.1, PROCESSING-BE-004.2, PROCESSING-INFRA-004.1 |
| ch. 6.3 – Runtime invariants (format validation before processing) | PROCESSING-STORY-004-S004, PROCESSING-BE-004.1-S003, PROCESSING-INFRA-004.3-S001 |

---

**Bundle status:** Approved
