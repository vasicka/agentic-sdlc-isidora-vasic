# VALIDATION Domain – User Story Bundles

## Domain Overview

**Domain:** VALIDATION
**Architecture component:** Validator
**Responsibility:** Receive a nine-character account string, apply the mod-11 checksum, and return exactly one status: VALID, ERR, or ILL.

**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-4, FR-5, FR-6)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator component, dependency rules)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (error handling and result classification)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)

---

## VALIDATION-STORY-001 – Validate Account Numbers with Mod-11 Checksum

**Domain:** VALIDATION
**Story ID:** VALIDATION-STORY-001
**Title:** Validate account numbers with mod-11 checksum
**Priority:** CORE
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-4, FR-5, FR-6)
- `architecture/04-solution-strategy.md`, Section 4.2 (Validator responsibility)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator component, dependency rules)
- `architecture/06-runtime-view.md`, Section 6.1 (Steps 5–6), Section 6.2 (ERR and ILL paths), Section 6.3 (runtime invariants)
- `architecture/08-crosscutting-concepts.md`, Sections 8.1, 8.2, 8.3
- `architecture/10-quality-requirements.md`, QS-02, QS-03, QS-06

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to validate each nine-digit account number against the mod-11 checksum rule and determine whether it is valid, erroneous, or illegible,
**SO THAT** I receive an accurate and unambiguous status for every account number in my input file.

---

### Acceptance Scenarios

### SCENARIO 1: Return VALID for a nine-digit account number that passes mod-11
**Scenario ID:** VALIDATION-STORY-001-S001
**GIVEN** a nine-character account string in which every character is a decimal digit (0–9) and the value of `(d9 + 2·d8 + 3·d7 + 4·d6 + 5·d5 + 6·d4 + 7·d3 + 8·d2 + 9·d1) mod 11` equals 0
**WHEN** the Validator processes the string
**THEN** it returns the status `VALID`

### SCENARIO 2: Return ERR for a nine-digit account number that fails mod-11
**Scenario ID:** VALIDATION-STORY-001-S002
**GIVEN** a nine-character account string in which every character is a decimal digit (0–9) and the mod-11 checksum result is not 0
**WHEN** the Validator processes the string
**THEN** it returns the status `ERR`

### SCENARIO 3: Return ILL when the account string contains a placeholder character
**Scenario ID:** VALIDATION-STORY-001-S003
**GIVEN** a nine-character account string in which one or more positions contain a placeholder character inserted by the Parser for an unrecognised glyph
**WHEN** the Validator processes the string
**THEN** it returns the status `ILL` without performing a checksum calculation

### SCENARIO 4: Return exactly one status for every input string
**Scenario ID:** VALIDATION-STORY-001-S004
**GIVEN** any nine-character account string passed to the Validator
**WHEN** the Validator processes it
**THEN** it returns exactly one of `VALID`, `ERR`, or `ILL`, and no account string is left without a status

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3). The Validator is an internal component with no user-facing interface of its own.

---

### Backend Stories

#### VALIDATION-BE-001.1 – Implement mod-11 checksum calculation

**Story ID:** VALIDATION-BE-001.1
**Parent story:** VALIDATION-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-4)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator responsibility)
- `architecture/06-runtime-view.md`, Section 6.1 (Steps 5–6)
- `architecture/10-quality-requirements.md`, QS-03

**AS A** BankOCR developer,
**I WANT** the Validator to compute `(d9 + 2·d8 + 3·d7 + 4·d6 + 5·d5 + 6·d4 + 7·d3 + 8·d2 + 9·d1) mod 11` for any nine-digit account string,
**SO THAT** the system can determine whether an account number is arithmetically valid according to the kata specification.

#### Acceptance Scenarios

### SCENARIO 1: Compute a checksum that equals zero and return VALID
**Scenario ID:** VALIDATION-BE-001.1-S001
**GIVEN** a nine-character string of decimal digits whose weighted sum `(d9 + 2·d8 + … + 9·d1)` is divisible by 11
**WHEN** the Validator applies the checksum formula
**THEN** it returns `VALID`

### SCENARIO 2: Compute a checksum that is non-zero and return ERR
**Scenario ID:** VALIDATION-BE-001.1-S002
**GIVEN** a nine-character string of decimal digits whose weighted sum is not divisible by 11
**WHEN** the Validator applies the checksum formula
**THEN** it returns `ERR`

### SCENARIO 3: Apply the correct positional weights
**Scenario ID:** VALIDATION-BE-001.1-S003
**GIVEN** a known nine-digit account number whose expected checksum result can be verified by manual calculation against the kata specification
**WHEN** the Validator computes the checksum
**THEN** the result agrees with the manually verified expected value, confirming that position d1 carries weight 9 and position d9 carries weight 1

---

#### VALIDATION-BE-001.2 – Detect placeholder characters and return ILL without checksum calculation

**Story ID:** VALIDATION-BE-001.2
**Parent story:** VALIDATION-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator responsibility)
- `architecture/06-runtime-view.md`, Section 6.2 (ILL path)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (placeholder convention, ILL classification rule)
- `architecture/10-quality-requirements.md`, QS-02

**AS A** BankOCR developer,
**I WANT** the Validator to detect placeholder characters in the account string and return `ILL` immediately without attempting a checksum calculation,
**SO THAT** entries containing unrecognised glyphs are classified correctly and no arithmetic is performed on non-digit input.

#### Acceptance Scenarios

### SCENARIO 1: Return ILL for a string with one placeholder
**Scenario ID:** VALIDATION-BE-001.2-S001
**GIVEN** a nine-character account string in which exactly one position contains a placeholder character
**WHEN** the Validator inspects the string
**THEN** it returns `ILL` without computing the weighted sum

### SCENARIO 2: Return ILL for a string with multiple placeholders
**Scenario ID:** VALIDATION-BE-001.2-S002
**GIVEN** a nine-character account string in which more than one position contains a placeholder character
**WHEN** the Validator inspects the string
**THEN** it returns `ILL` without computing the weighted sum

### SCENARIO 3: Do not return ILL for a string with no placeholders
**Scenario ID:** VALIDATION-BE-001.2-S003
**GIVEN** a nine-character account string in which every position contains a decimal digit (0–9) and no placeholder is present
**WHEN** the Validator inspects the string
**THEN** it does not return `ILL`; it proceeds to the checksum calculation and returns either `VALID` or `ERR`

---

### Infrastructure Stories

#### VALIDATION-INFRA-001.1 – Execute Validator tests in Docker container using pytest

**Story ID:** VALIDATION-INFRA-001.1
**Parent story:** VALIDATION-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5) – Note: TC-5 specifies `unittest` but Docker uses `pytest`
- `architecture/05-building-block-view.md`, Section 5.2 (Dependency rules: Validator has no file-system dependency)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Validator testability convention)
- `architecture/10-quality-requirements.md`, QS-06, QS-07
- Dockerfile (local Docker-based environment established in Module 4)
- CI workflow (`.github/workflows/ci.yml`)

**AS A** BankOCR developer,
**I WANT** the Validator to be exercisable in complete isolation within a Docker container using `pytest`, by passing nine-character strings directly with no file-system dependencies,
**SO THAT** checksum and ILL-detection defects are pinpointed immediately in the local Docker-based test environment.

> **Note:** This story reflects the local Docker-based environment established in Module 4. TC-5 specifies `unittest`, but the Docker setup uses `pytest` for testing. `pytest` is a test dependency, not a runtime dependency, so it does not violate TC-3 (standard library only for runtime).
>
> **QS-07 clarification:** The original QS-7 requirement specifies that tests should run with no external dependencies on a machine with only Python ≥ 3.12. The Module 4 Docker/pytest setup introduces `pytest` as a third-party test dependency, which creates a discrepancy with the original QS-7 requirement. `pytest` is a test-only dependency and does not affect runtime execution, but it does mean the full test suite cannot run with zero external dependencies as originally specified in QS-7.

#### Acceptance Scenarios

### SCENARIO 1: Build Docker image for Validator testing
**Scenario ID:** VALIDATION-INFRA-001.1-S001
**GIVEN** the BankOCR source code with its Dockerfile and test dependencies configuration
**WHEN** the Docker image is built with `docker build -t kata-tests .`
**THEN** the build completes successfully, installing Python 3.12 and test dependencies including pytest

### SCENARIO 2: Execute Validator tests inside Docker container
**Scenario ID:** VALIDATION-INFRA-001.1-S002
**GIVEN** the built Docker image containing the BankOCR source and test suite
**WHEN** tests are executed with `docker run --rm kata-tests` (default CMD runs pytest)
**THEN** the Validator tests run inside the container with no external file system dependencies and produce test results

### SCENARIO 3: Pass a nine-character string directly to the Validator without file I/O
**Scenario ID:** VALIDATION-INFRA-001.1-S003
**GIVEN** a pytest test case that constructs a nine-character account string as a Python string literal
**WHEN** that string is passed directly to the Validator inside the Docker container
**THEN** the Validator returns one of `VALID`, `ERR`, or `ILL`, and no file is read from or written to the file system

### SCENARIO 4: Validator tests require no file fixtures when running in Docker
**Scenario ID:** VALIDATION-INFRA-001.1-S004
**GIVEN** the full Validator test suite executed inside Docker
**WHEN** the test suite runs
**THEN** no test creates, reads, or deletes a file on the host file system, and no temporary directory is mounted or required

---

#### VALIDATION-INFRA-001.2 – Deploy the Validator as part of the single-file CLI application in Docker environment

**Story ID:** VALIDATION-INFRA-001.2
**Parent story:** VALIDATION-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3)
- `architecture/04-solution-strategy.md`, Section 4.1 (single CLI application)
- `architecture/07-deployment-view.md`, Sections 7.1, 7.2, 7.3 – Note: Deployment view doesn't mention Docker
- `architecture/10-quality-requirements.md`, QS-10, QS-11
- Dockerfile (local Docker-based environment)

**AS A** BankOCR developer,
**I WANT** the Validator to be packaged as part of the single Python CLI application within a Docker container,
**SO THAT** the application can be invoked through Docker on any machine with Docker installed, without requiring Python ≥ 3.12 on the host.

#### Acceptance Scenarios

### SCENARIO 1: Docker image contains the complete application with Validator
**Scenario ID:** VALIDATION-INFRA-001.2-S001
**GIVEN** the built Docker image `kata-tests`
**WHEN** the image layers are inspected
**THEN** the image contains the Validator module and all application source code, ready for execution inside the container

### SCENARIO 2: Validator imports only standard-library modules
**Scenario ID:** VALIDATION-INFRA-001.2-S002
**GIVEN** the Validator module source file inside the Docker container
**WHEN** the import statements are inspected
**THEN** every imported module belongs to the Python standard library and no third-party runtime package is referenced (TC-3)

### SCENARIO 3: Application runs on Python 3.12 inside Docker
**Scenario ID:** VALIDATION-INFRA-001.2-S003
**GIVEN** a Docker container running the built image with Python 3.12
**WHEN** the application CLI is invoked inside the container
**THEN** the application runs to completion without a `SyntaxError` or version-compatibility error (TC-1)

### SCENARIO 4: Docker image builds successfully for development testing
**Scenario ID:** VALIDATION-INFRA-001.2-S004
**GIVEN** the CI workflow configuration (`.github/workflows/ci.yml`)
**WHEN** the workflow executes `docker build -t kata-tests .`
**THEN** the build completes successfully, creating a runnable Docker image that includes the Validator

### SCENARIO 5: Application runs without Docker installation (original CLI requirement)
**Scenario ID:** VALIDATION-INFRA-001.2-S005
**GIVEN** a machine with Python ≥ 3.12 and the BankOCR source files present on the local file system
**WHEN** the CLI is invoked from the command line with a valid input file path
**THEN** the application starts and the Validator executes without requiring `pip install` or any build step (preserves QS-11)

---

#### VALIDATION-INFRA-001.3 – Confirm that the Validator operates on in-memory strings with no file-based data handling in Docker

**Story ID:** VALIDATION-INFRA-001.3
**Parent story:** VALIDATION-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Validator has no file-system dependency)
- `architecture/08-crosscutting-concepts.md`, Section 8.2 (Separation of I/O from logic)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)
- Dockerfile (local Docker-based environment)

**AS A** BankOCR developer,
**I WANT** the Validator to receive account strings as in-memory string arguments and return status values as return values within the Docker container, with no direct file access,
**SO THAT** the Validator can be tested and reused without any dependency on the file system, consistent with ADR-002.

> **Note:** File I/O is owned exclusively by the Processor (ADR-002, `architecture/05-building-block-view.md`, Section 5.2). This story confirms the Validator's compliance with that boundary in the Docker environment; it does not assign file-handling responsibilities to the Validator.

#### Acceptance Scenarios

### SCENARIO 1: Validator accepts a string argument, not a file path, in Docker container
**Scenario ID:** VALIDATION-INFRA-001.3-S001
**GIVEN** the Validator's public interface inside the Docker container
**WHEN** it is called with a nine-character account string
**THEN** it processes the string in memory and returns one of `VALID`, `ERR`, or `ILL` without opening any file or accessing host file system

### SCENARIO 2: Validator produces no file-system side effects in Docker
**Scenario ID:** VALIDATION-INFRA-001.3-S002
**GIVEN** an invocation of the Validator with a valid nine-character account string inside Docker
**WHEN** the Validator runs to completion
**THEN** no file is created, modified, or deleted on the container's file system or host file system as a side effect

### SCENARIO 3: Validator behavior is consistent regardless of container file paths
**Scenario ID:** VALIDATION-INFRA-001.3-S003
**GIVEN** two Docker containers running the same image but with different mounted volumes or working directories
**WHEN** the Validator is called with identical nine-character account string content in both containers
**THEN** both calls return the identical status value, confirming no dependency on container file paths or mounted volumes

---

#### VALIDATION-INFRA-001.4 – Confirm event inapplicability and define observability via pytest results and Docker exit codes

**Story ID:** VALIDATION-INFRA-001.4
**Parent story:** VALIDATION-STORY-001
**Priority:** CORE
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/10-quality-requirements.md`, QS-07
- `architecture/11-risks-and-technical-debt.md`, DEBT-03
- Dockerfile (local Docker-based environment)
- CI workflow (`.github/workflows/ci.yml`)

**AS A** BankOCR developer,
**I WANT** the system to report Validator test outcomes through `pytest` results and Docker container exit codes rather than through event infrastructure,
**SO THAT** errors in checksum logic or ILL detection are visible in the Docker-based test environment without introducing monitoring services that the architecture does not approve.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the VALIDATION domain. This story documents that determination explicitly and specifies the observability mechanism that applies in the Docker environment.
>
> **QS-07 clarification:** The original QS-7 requirement specifies that tests should run with no external dependencies on a machine with only Python ≥ 3.12. The Module 4 Docker/pytest setup introduces `pytest` as a third-party test dependency, which creates a discrepancy with the original QS-7 requirement. `pytest` is a test-only dependency and does not affect runtime execution, but it does mean the full test suite cannot run with zero external dependencies as originally specified in QS-7.

#### Acceptance Scenarios

### SCENARIO 1: pytest reports Validator test pass or fail in Docker
**Scenario ID:** VALIDATION-INFRA-001.4-S001
**GIVEN** the Validator tests are executed inside Docker with `docker run --rm kata-tests`
**WHEN** one or more Validator tests fail
**THEN** pytest prints a FAIL or ERROR result for each failing test to stdout, and the Docker container exits with a non-zero exit code

### SCENARIO 2: CI workflow captures test results from Docker
**Scenario ID:** VALIDATION-INFRA-001.4-S002
**GIVEN** the CI workflow configuration (`.github/workflows/ci.yml`)
**WHEN** the workflow executes `docker run --rm kata-tests`
**THEN** the workflow step captures the pytest output and fails if any tests fail, providing observability through GitHub Actions

### SCENARIO 3: No event infrastructure is present in the Validator module in Docker
**Scenario ID:** VALIDATION-INFRA-001.4-S003
**GIVEN** the Validator module source code inside the Docker container
**WHEN** the source is inspected for imports or calls to message queues, event buses, logging frameworks, or external monitoring services
**THEN** no such imports or calls are present; the Validator contains only checksum logic, placeholder detection, and standard-library imports

### SCENARIO 4: Docker container exit code reflects test suite success
**Scenario ID:** VALIDATION-INFRA-001.4-S004
**GIVEN** a Docker container running the full test suite with `docker run --rm kata-tests`
**WHEN** all tests in the suite (including Validator tests) pass
**THEN** the container exits with exit code 0; when any test fails, it exits with a non-zero code

### SCENARIO 5: Application exits with code 0 after successful validation of VALID, ERR, and ILL outcomes
**Scenario ID:** VALIDATION-INFRA-001.4-S005
**GIVEN** a well-formed input file containing account entries that produce VALID, ERR, and ILL outcomes after validation
**WHEN** the BankOCR CLI application processes the file and completes validation through the Validator for all entries
**THEN** the application process exits with exit code 0, regardless of the mix of VALID, ERR, and ILL statuses returned

---

### DDD Analysis

**Bounded context:** VALIDATION — the logical responsibility boundary within the BankOCR CLI that owns checksum calculation, placeholder detection, and status determination.

**Conceptual domain elements** (requirements-analysis concepts; they do not prescribe specific implementation class names):

| Element | Type | Description |
|---------|------|-------------|
| `AccountString` | Value object | The nine-character string received from the Processor (originally produced by the Parser). Each position holds a decimal digit (0–9) or a placeholder. Immutable; consumed but not modified by the Validator. |
| `ValidationStatus` | Value object | The result of Validator processing: one of exactly three values — `VALID`, `ERR`, or `ILL`. Immutable; passed back to the Processor for output formatting. |
| `ChecksumRule` | Domain service | The stateless computation `(d9 + 2·d8 + 3·d7 + … + 9·d1) mod 11`. Applied only when no placeholder is present in the `AccountString`. Not an entity; it holds no state. |

**Domain rules enforced by the Validator:**
1. If any placeholder is present in the `AccountString`, return `ILL` immediately — no checksum calculation.
2. If no placeholder is present and the checksum equals 0, return `VALID`.
3. If no placeholder is present and the checksum is non-zero, return `ERR`.
4. These three outcomes are mutually exclusive and exhaustive; every input string produces exactly one.

**Relationship to existing architecture:** These concepts map onto the Validator component described in `architecture/05-building-block-view.md`, Section 5.2. `AccountString` is a shared value object that crosses the PARSING/VALIDATION context boundary — the Parser produces it, the Processor passes it, and the Validator consumes it. The architecture does not mandate separate classes for each domain element; the mapping is an implementation decision.

**Component boundaries respected:** The Validator has no dependency on the Parser, Processor, or file system (ADR-002, ch. 5.2). It receives a string and returns a status; it neither reads files nor calls any other component. The VALIDATION bounded context begins at that string handoff and ends when `ValidationStatus` is returned to the Processor.

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-4 – Validate using mod-11 checksum | VALIDATION-STORY-001, VALIDATION-BE-001.1, VALIDATION-BE-001.1-S001, VALIDATION-BE-001.1-S002, VALIDATION-BE-001.1-S003 |
| FR-5 – Mark illegible accounts as ILL | VALIDATION-STORY-001-S003, VALIDATION-BE-001.2, VALIDATION-BE-001.2-S001, VALIDATION-BE-001.2-S002 |
| FR-6 – Mark checksum-failing accounts as ERR | VALIDATION-STORY-001-S002, VALIDATION-BE-001.1-S002 |
| TC-1 – Python ≥ 3.12 | VALIDATION-INFRA-001.1-S001, VALIDATION-INFRA-001.2-S003 |
| TC-3 – Standard library only | VALIDATION-INFRA-001.2-S002 |
| TC-5 – unittest | Note: Docker uses pytest, not unittest (VALIDATION-INFRA-001.1) |
| ADR-001 – Single CLI, no external services | VALIDATION-INFRA-001.4-S003 |
| ADR-002 – File I/O confined to Processor | VALIDATION-INFRA-001.3-S001, VALIDATION-INFRA-001.3-S002, VALIDATION-INFRA-001.3-S003 |
| Dockerfile – Local Docker environment | VALIDATION-INFRA-001.1-S001, VALIDATION-INFRA-001.1-S002, VALIDATION-INFRA-001.2-S001, VALIDATION-INFRA-001.2-S004 |
| CI workflow – GitHub Actions | VALIDATION-INFRA-001.2-S004, VALIDATION-INFRA-001.4-S002 |
| QS-02 – Unrecognised glyph handling | VALIDATION-STORY-001-S003, VALIDATION-BE-001.2-S001, VALIDATION-BE-001.2-S002 |
| QS-03 – Checksum validation correctness | VALIDATION-STORY-001-S001, VALIDATION-STORY-001-S002, VALIDATION-BE-001.1-S001, VALIDATION-BE-001.1-S002, VALIDATION-BE-001.1-S003 |
| QS-06 – Validator tested without file I/O | VALIDATION-INFRA-001.1-S003, VALIDATION-INFRA-001.1-S004, VALIDATION-INFRA-001.3-S001 |
| QS-07 – Test suite runs with no external dependencies | VALIDATION-INFRA-001.4-S001, VALIDATION-INFRA-001.4-S002 – Note: `pytest` is a third-party test dependency, creating a discrepancy with the original QS-7 requirement for dependency-free testing |
| QS-10 – No unjustified dependencies | VALIDATION-INFRA-001.2-S002 |
| QS-11 – Single command invocation | VALIDATION-INFRA-001.2-S001, VALIDATION-INFRA-001.2-S005 |
| DEBT-03 – No structured logging | VALIDATION-INFRA-001.4-S003 |
| ch. 8.1 – Error handling and result classification | VALIDATION-STORY-001-S004, VALIDATION-BE-001.2-S003 |
| ch. 6.3 – Runtime invariant: Validator called once per string | VALIDATION-STORY-001-S004 |

---

**Bundle status:** Approved

---

## VALIDATION-STORY-002 – Mark Checksum-Failing Accounts as ERR

**Domain:** VALIDATION
**Story ID:** VALIDATION-STORY-002
**Title:** Mark checksum-failing accounts as ERR
**Priority:** Supporting
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-6)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator component, dependency rules)
- `architecture/06-runtime-view.md`, Section 6.2 (ERR path), Section 6.3 (runtime invariants)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (result classification: ERR branch)
- `architecture/10-quality-requirements.md`, QS-03

---

### Scope distinction

VALIDATION-STORY-001 establishes the general three-branch algorithm — placeholder present → ILL; checksum = 0 → VALID; checksum ≠ 0 → ERR — and verifies the formula is applied with the correct positional weights. This story focuses specifically on the ERR branch: the conditions that trigger it, that it fires only when all nine positions are decimal digits and the weighted sum is not divisible by 11, and that the Validator's responsibility ends at returning `ERR`. Appending ` ERR` to the output line is the Processor's responsibility (PROCESSING-BE-002.2) and is not covered here.

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to identify account numbers that contain only recognisable digits but fail the checksum rule,
**SO THAT** I can distinguish syntactically well-formed but arithmetically invalid account numbers from both valid ones and those with unreadable digits.

---

### Acceptance Scenarios

### SCENARIO 1: Return ERR for a fully-digit string whose checksum is non-zero
**Scenario ID:** VALIDATION-STORY-002-S001
**GIVEN** a nine-character account string in which every position contains a decimal digit (0–9) and the value of `(d9 + 2·d8 + 3·d7 + 4·d6 + 5·d5 + 6·d4 + 7·d3 + 8·d2 + 9·d1) mod 11` is not equal to 0
**WHEN** the Validator processes the string
**THEN** it returns the status `ERR`

### SCENARIO 2: Do not return ERR when the checksum passes
**Scenario ID:** VALIDATION-STORY-002-S002
**GIVEN** a nine-character account string in which every position contains a decimal digit and the mod-11 checksum equals 0
**WHEN** the Validator processes the string
**THEN** it returns `VALID` and not `ERR`

### SCENARIO 3: Do not return ERR when the string contains a placeholder
**Scenario ID:** VALIDATION-STORY-002-S003
**GIVEN** a nine-character account string in which one or more positions contain a placeholder character
**WHEN** the Validator processes the string
**THEN** it returns `ILL` and not `ERR`, confirming that the placeholder check takes precedence over the checksum

### SCENARIO 4: ERR is returned regardless of which digit position causes the checksum to fail
**Scenario ID:** VALIDATION-STORY-002-S004
**GIVEN** multiple nine-character all-digit account strings, each with a different single-digit position altered so that the mod-11 checksum fails
**WHEN** the Validator processes each string
**THEN** it returns `ERR` for every such string, confirming that no digit position is exempt from the checksum rule

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3). The Validator is an internal component with no user-facing interface of its own.

---

### Backend Stories

#### VALIDATION-BE-002.1 – Return ERR exclusively for all-digit strings with a non-zero mod-11 result

**Story ID:** VALIDATION-BE-002.1
**Parent story:** VALIDATION-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-6)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator responsibility)
- `architecture/06-runtime-view.md`, Section 6.2 (ERR path: all glyphs recognised, checksum fails)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (ERR branch of result classification)
- `architecture/10-quality-requirements.md`, QS-03

**AS A** BankOCR developer,
**I WANT** the Validator to return `ERR` if and only if the `AccountString` contains nine decimal digits and the mod-11 weighted sum is not divisible by 11,
**SO THAT** the ERR classification is applied precisely — neither suppressed for strings that should fail nor triggered for strings that should be VALID or ILL.

#### Acceptance Scenarios

### SCENARIO 1: Return ERR for a known checksum-failing string
**Scenario ID:** VALIDATION-BE-002.1-S001
**GIVEN** a nine-character all-digit account string whose mod-11 weighted sum can be manually verified to be non-zero
**WHEN** the Validator applies the checksum formula
**THEN** it returns `ERR`

### SCENARIO 2: Do not return ERR for the same string with the check digit corrected to pass
**Scenario ID:** VALIDATION-BE-002.1-S002
**GIVEN** a nine-character all-digit account string derived from the string in S001 by adjusting the check digit so the mod-11 sum equals 0
**WHEN** the Validator applies the checksum formula
**THEN** it returns `VALID` and not `ERR`, confirming the boundary between ERR and VALID is correctly placed

### SCENARIO 3: Do not return ERR for a string containing a placeholder
**Scenario ID:** VALIDATION-BE-002.1-S003
**GIVEN** a nine-character account string in which one position contains a placeholder character and the remaining eight positions are decimal digits
**WHEN** the Validator inspects the string
**THEN** it returns `ILL` without reaching the checksum step, confirming placeholder detection takes precedence over ERR classification

---

#### VALIDATION-BE-002.2 – Confirm that the Validator does not format or annotate output lines

**Story ID:** VALIDATION-BE-002.2
**Parent story:** VALIDATION-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Processor writes annotated result lines; Validator returns a status value only)
- `architecture/06-runtime-view.md`, Section 6.2 (ERR path comparison table: Validator output is `ERR`; result line annotation ` ERR` is applied by the Processor)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (result classification table: Validator returns status, Processor writes annotation)
- `architecture/09-architecture-decisions.md`, ADR-002

**AS A** BankOCR developer,
**I WANT** the Validator to return the string `ERR` as a status value and leave all output line formatting to the Processor,
**SO THAT** the Validator's responsibility remains limited to classification and the output format can change without touching the Validator.

#### Acceptance Scenarios

### SCENARIO 1: Validator return value for a checksum-failing string is the bare status token ERR
**Scenario ID:** VALIDATION-BE-002.2-S001
**GIVEN** a nine-character all-digit account string that fails the mod-11 checksum
**WHEN** the Validator processes the string
**THEN** the return value is the string `ERR` with no leading space, no account number prefix, and no surrounding punctuation

### SCENARIO 2: Validator makes no call to any file-writing or output-formatting function
**Scenario ID:** VALIDATION-BE-002.2-S002
**GIVEN** the Validator module source code
**WHEN** the logic for returning `ERR` is inspected
**THEN** no file-open, file-write, string-concatenation with an account number, or output-formatting call is present; the Validator only returns the status token

### SCENARIO 3: Processor is solely responsible for appending the ERR annotation to the result line
**Scenario ID:** VALIDATION-BE-002.2-S003
**GIVEN** the Processor receives `ERR` from the Validator for a given account string
**WHEN** the Processor formats the result line
**THEN** it produces a line containing the nine-character account string followed by ` ERR`; this formatting occurs in the Processor, not in the Validator (confirmed by PROCESSING-BE-002.2)

---

### Infrastructure Stories

#### VALIDATION-INFRA-002.1 – Test ERR classification in isolation using unittest

**Story ID:** VALIDATION-INFRA-002.1
**Parent story:** VALIDATION-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Dependency rules: Validator has no file-system dependency)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Validator testability convention)
- `architecture/10-quality-requirements.md`, QS-03, QS-06, QS-07

**AS A** BankOCR developer,
**I WANT** the Validator's ERR classification to be covered by `unittest` tests that pass known checksum-failing nine-character strings directly to the Validator,
**SO THAT** the boundary between ERR, VALID, and ILL outcomes is verified automatically without file fixtures or external tools.

#### Acceptance Scenarios

### SCENARIO 1: Test confirms ERR for a known checksum-failing string
**Scenario ID:** VALIDATION-INFRA-002.1-S001
**GIVEN** a `unittest` test case that constructs a nine-character all-digit string whose mod-11 checksum is known to be non-zero
**WHEN** the string is passed directly to the Validator
**THEN** the test asserts that the return value is `ERR`

### SCENARIO 2: Test confirms VALID for the corrected version of the same string
**Scenario ID:** VALIDATION-INFRA-002.1-S002
**GIVEN** a `unittest` test case that constructs the checksum-passing counterpart of the string used in S001
**WHEN** the string is passed directly to the Validator
**THEN** the test asserts that the return value is `VALID` and not `ERR`, verifying the ERR/VALID boundary

### SCENARIO 3: ERR classification tests require no file fixtures
**Scenario ID:** VALIDATION-INFRA-002.1-S003
**GIVEN** the full set of `unittest` tests for VALIDATION-STORY-002
**WHEN** the suite is executed
**THEN** no test creates, reads, or deletes a file on disk, and no temporary directory is required

---

#### VALIDATION-INFRA-002.2 – Confirm that ERR classification introduces no file I/O or output formatting

**Story ID:** VALIDATION-INFRA-002.2
**Parent story:** VALIDATION-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Validator has no file-system dependency)
- `architecture/08-crosscutting-concepts.md`, Section 8.2 (Separation of I/O from logic)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)

**AS A** BankOCR developer,
**I WANT** the Validator's ERR classification logic to operate entirely on in-memory strings, with no file access and no output line formatting,
**SO THAT** the Validator remains independently testable and the output format remains the Processor's sole responsibility.

#### Acceptance Scenarios

### SCENARIO 1: Validator produces no file-system side effects when returning ERR
**Scenario ID:** VALIDATION-INFRA-002.2-S001
**GIVEN** an invocation of the Validator with a nine-character all-digit string that fails the mod-11 checksum
**WHEN** the Validator runs to completion and returns `ERR`
**THEN** no file is created, modified, or deleted on the file system as a side effect

### SCENARIO 2: Validator return value contains only the status token with no formatting
**Scenario ID:** VALIDATION-INFRA-002.2-S002
**GIVEN** an invocation of the Validator with a checksum-failing all-digit string
**WHEN** the Validator returns
**THEN** the return value is exactly the three-character string `ERR` with no surrounding whitespace, no account number prefix, and no newline character

### SCENARIO 3: Validator makes no call to any Processor or file-writing function when returning ERR
**Scenario ID:** VALIDATION-INFRA-002.2-S003
**GIVEN** the Validator module source code
**WHEN** the ERR return path is inspected
**THEN** no import or call to the Processor, file system, or any output-formatting function is present; the return statement yields only the status token

---

#### VALIDATION-INFRA-002.3 – Confirm event inapplicability and define observability for ERR classification

**Story ID:** VALIDATION-INFRA-002.3
**Parent story:** VALIDATION-STORY-002
**Priority:** Supporting
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/10-quality-requirements.md`, QS-03, QS-07
- `architecture/11-risks-and-technical-debt.md`, DEBT-03

**AS A** BankOCR developer,
**I WANT** ERR classification outcomes to be observable through `unittest` test results and the downstream ` ERR` annotation in the output file, rather than through event infrastructure,
**SO THAT** checksum failures are detectable without introducing monitoring services that the architecture does not approve.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the VALIDATION domain. The `ERR` status token returned by the Validator is the signal that propagates the checksum-failure condition to the Processor, which writes the ` ERR` annotation to the output file.

#### Acceptance Scenarios

### SCENARIO 1: unittest test suite surfaces any incorrect ERR classification logic
**Scenario ID:** VALIDATION-INFRA-002.3-S001
**GIVEN** the Validator unit tests for VALIDATION-STORY-002 are executed with `python -m unittest`
**WHEN** the ERR classification logic is incorrect — for example, returning `VALID` for a string that should be `ERR`
**THEN** one or more tests fail and the runner exits with a non-zero exit code, surfacing the defect

### SCENARIO 2: A checksum-failing account number produces a visible ERR annotation in the output file
**Scenario ID:** VALIDATION-INFRA-002.3-S002
**GIVEN** the CLI is invoked with an input file containing an account entry whose nine glyphs are all recognisable but whose mod-11 checksum fails
**WHEN** the full pipeline runs to completion
**THEN** the corresponding result line in the output file is suffixed with ` ERR`, confirming the `ERR` status propagated correctly from the Validator through the Processor

### SCENARIO 3: No event infrastructure is present in the Validator module for ERR classification
**Scenario ID:** VALIDATION-INFRA-002.3-S003
**GIVEN** the Validator module source code
**WHEN** the ERR classification logic is inspected
**THEN** no message queue, event bus, logging call, or external monitoring service is invoked; the Validator returns `ERR` and no other side effect occurs

---

### DDD Analysis

**Bounded context:** VALIDATION — same bounded context as VALIDATION-STORY-001. This story focuses on the ERR branch of the Validator's classification logic.

**Conceptual domain elements relevant to this story** (subset of elements defined in VALIDATION-STORY-001):

| Element | Type | Description |
|---------|------|-------------|
| `AccountString` | Value object | As defined in VALIDATION-STORY-001. This story constrains the input to the ERR path: a nine-character string containing only decimal digits (0–9) with no placeholder characters. |
| `ValidationStatus` | Value object | As defined in VALIDATION-STORY-001. This story focuses on the `ERR` variant: the value returned when the `ChecksumRule` applied to an all-digit `AccountString` yields a non-zero result. |
| `ChecksumRule` | Domain service | As defined in VALIDATION-STORY-001. This story establishes the precise trigger for `ERR`: the weighted sum `(d9 + 2·d8 + … + 9·d1) mod 11` is computed and found to be non-zero. |

**Domain rules specific to this story:**
1. The ERR path is entered only when the `AccountString` contains no placeholder characters (rule 1 of VALIDATION-STORY-001 dispatches placeholder strings to ILL before the checksum is computed).
2. Within the ERR path, the `ChecksumRule` is applied to all nine digit characters.
3. If the result is non-zero, the Validator returns `ERR` as the `ValidationStatus`.
4. The Validator's responsibility ends at returning the `ERR` token; no output line is formatted and no file is written (ADR-002, ch. 5.2).
5. The ` ERR` annotation in the output file is produced by the Processor (PROCESSING-BE-002.2), not by the Validator.

**Relationship to VALIDATION-STORY-001:** VALIDATION-STORY-001 defines the algorithm and proves it is correctly implemented. This story defines the user-visible outcome of the ERR branch and reinforces the boundary between the Validator (returns a status token) and the Processor (formats the output line). The two stories together provide complete coverage of the ERR classification requirement (FR-6).

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-6 – Mark checksum-failing accounts as ERR | VALIDATION-STORY-002, VALIDATION-BE-002.1, VALIDATION-BE-002.1-S001, VALIDATION-BE-002.1-S002 |
| TC-1 – Python ≥ 3.12 | VALIDATION-INFRA-002.1-S001 |
| TC-3 – Standard library only | VALIDATION-INFRA-002.1-S001 |
| TC-5 – unittest | VALIDATION-INFRA-002.1-S001, VALIDATION-INFRA-002.3-S001 |
| ADR-001 – Single CLI, no external services | VALIDATION-INFRA-002.3-S003 |
| ADR-002 – File I/O confined to Processor | VALIDATION-BE-002.2-S002, VALIDATION-INFRA-002.2-S001, VALIDATION-INFRA-002.2-S003 |
| QS-03 – Checksum validation correctness | VALIDATION-STORY-002-S001, VALIDATION-STORY-002-S004, VALIDATION-BE-002.1-S001, VALIDATION-BE-002.1-S002, VALIDATION-INFRA-002.3-S001 |
| QS-06 – Validator tested without file I/O | VALIDATION-INFRA-002.1-S003, VALIDATION-INFRA-002.2-S001 |
| QS-07 – Test suite runs with no external dependencies | VALIDATION-INFRA-002.1-S001, VALIDATION-INFRA-002.3-S001 |
| ch. 6.2 – ERR path: all glyphs recognised, checksum fails | VALIDATION-STORY-002-S001, VALIDATION-BE-002.1-S001, VALIDATION-INFRA-002.3-S002 |
| ch. 6.3 – Validator called once per string, returns exactly one status | VALIDATION-STORY-002-S001, VALIDATION-STORY-002-S003 |
| ch. 8.1 – ERR branch of result classification; placeholder check takes precedence | VALIDATION-STORY-002-S003, VALIDATION-BE-002.1-S003, VALIDATION-BE-002.2-S001 |
| ch. 8.2 – Separation of I/O from logic | VALIDATION-INFRA-002.2-S001, VALIDATION-INFRA-002.2-S003 |
| DEBT-03 – No structured logging | VALIDATION-INFRA-002.3-S003 |
| PROCESSING-BE-002.2 – Processor formats ` ERR` annotation (cross-reference) | VALIDATION-BE-002.2-S003, VALIDATION-INFRA-002.3-S002 |

---

**Bundle status:** Approved

---

## VALIDATION-STORY-003 – Mark Accounts with Unrecognised Glyphs as ILL

**Domain:** VALIDATION
**Story ID:** VALIDATION-STORY-003
**Title:** Mark accounts with unrecognised glyphs as ILL
**Priority:** Supporting
**Status:** Approved
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator component, dependency rules)
- `architecture/06-runtime-view.md`, Section 6.2 (ILL path), Section 6.3 (runtime invariants)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (placeholder convention: ILL classification, checksum skipped)
- `architecture/10-quality-requirements.md`, QS-02, QS-06
- `architecture/12-glossary.md` (ILL, Placeholder definitions)

---

### Scope distinction

VALIDATION-STORY-001 establishes the general three-branch algorithm — placeholder present → ILL; checksum = 0 → VALID; checksum ≠ 0 → ERR — and proves that the presence of any placeholder suppresses the checksum calculation. VALIDATION-STORY-002 covers the ERR branch for all-digit strings. This story focuses specifically on the ILL branch: the conditions that trigger it, that it fires for any number of placeholders from one to nine, that the checksum is never computed when a placeholder is present, and that the Validator's responsibility ends at returning `ILL`. Appending ` ILL` to the output line is the Processor's responsibility (PROCESSING-BE-002.2) and is not covered here.

The placeholder character is inserted by the Parser (PARSING-STORY-002). This story covers detection and classification by the Validator; it does not revisit how the placeholder was produced.

---

### Original User Story

**AS A** BankOCR user,
**I WANT** the application to identify account entries that contain one or more unreadable digit glyphs and mark them as illegible,
**SO THAT** I can distinguish entries that could not be read from those that were read but failed the checksum.

---

### Acceptance Scenarios

### SCENARIO 1: Return ILL for a string containing one placeholder
**Scenario ID:** VALIDATION-STORY-003-S001
**GIVEN** a nine-character account string in which exactly one position contains a placeholder character and the remaining eight positions contain decimal digits
**WHEN** the Validator processes the string
**THEN** it returns the status `ILL`

### SCENARIO 2: Return ILL for a string containing multiple placeholders
**Scenario ID:** VALIDATION-STORY-003-S002
**GIVEN** a nine-character account string in which more than one position contains a placeholder character
**WHEN** the Validator processes the string
**THEN** it returns the status `ILL`

### SCENARIO 3: Do not return ILL for an all-digit string
**Scenario ID:** VALIDATION-STORY-003-S003
**GIVEN** a nine-character account string in which every position contains a decimal digit (0–9) and no placeholder is present
**WHEN** the Validator processes the string
**THEN** it does not return `ILL`; it proceeds to the checksum calculation and returns either `VALID` or `ERR`

### SCENARIO 4: Return ILL without performing the checksum calculation
**Scenario ID:** VALIDATION-STORY-003-S004
**GIVEN** a nine-character account string containing at least one placeholder character
**WHEN** the Validator processes the string
**THEN** it returns `ILL` before computing any weighted sum, confirming that placeholder detection takes precedence over the checksum

---

### Frontend Stories

**Not applicable.**

BankOCR is a command-line application without a graphical frontend. All user interaction occurs through plain-text input and output files on the local file system (ADR-001, `architecture/03-context-and-scope.md`, Section 3.3). The Validator is an internal component with no user-facing interface of its own.

---

### Backend Stories

#### VALIDATION-BE-003.1 – Inspect the AccountString for placeholder characters before the checksum step

**Story ID:** VALIDATION-BE-003.1
**Parent story:** VALIDATION-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator responsibility)
- `architecture/06-runtime-view.md`, Section 6.2 (ILL path: Validator detects placeholder, skips checksum)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (placeholder present → ILL; checksum skipped)
- `architecture/10-quality-requirements.md`, QS-02

**AS A** BankOCR developer,
**I WANT** the Validator to scan the `AccountString` for placeholder characters as the first step of its classification logic, before any checksum arithmetic,
**SO THAT** entries with unrecognised glyphs are classified as ILL immediately and no arithmetic is performed on non-digit input.

#### Acceptance Scenarios

### SCENARIO 1: Placeholder detected in the first position triggers ILL without checksum
**Scenario ID:** VALIDATION-BE-003.1-S001
**GIVEN** a nine-character account string in which the first position contains a placeholder character
**WHEN** the Validator processes the string
**THEN** it returns `ILL` without computing the weighted sum for any position

### SCENARIO 2: Placeholder detected in the last position triggers ILL without checksum
**Scenario ID:** VALIDATION-BE-003.1-S002
**GIVEN** a nine-character account string in which the ninth position contains a placeholder character
**WHEN** the Validator processes the string
**THEN** it returns `ILL` without computing the weighted sum for any position

### SCENARIO 3: Absence of any placeholder allows the checksum step to proceed
**Scenario ID:** VALIDATION-BE-003.1-S003
**GIVEN** a nine-character account string in which every position contains a decimal digit
**WHEN** the Validator inspects the string for placeholders
**THEN** it finds none and proceeds to the checksum calculation, returning either `VALID` or `ERR`

---

#### VALIDATION-BE-003.2 – Return ILL for any number of placeholder positions from one to nine

**Story ID:** VALIDATION-BE-003.2
**Parent story:** VALIDATION-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/01-introduction-and-goals.md`, Section 1.1 (FR-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Validator responsibility)
- `architecture/06-runtime-view.md`, Section 6.2 (ILL path)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (one or more unrecognised glyphs → ILL)

**AS A** BankOCR developer,
**I WANT** the Validator to return `ILL` regardless of how many positions in the `AccountString` contain placeholder characters,
**SO THAT** every partially or fully illegible entry is correctly classified without special-casing for the number of unrecognised glyphs.

#### Acceptance Scenarios

### SCENARIO 1: Return ILL for a string with exactly one placeholder
**Scenario ID:** VALIDATION-BE-003.2-S001
**GIVEN** a nine-character account string containing exactly one placeholder character
**WHEN** the Validator processes the string
**THEN** it returns `ILL`

### SCENARIO 2: Return ILL for a string with all nine positions as placeholders
**Scenario ID:** VALIDATION-BE-003.2-S002
**GIVEN** a nine-character account string in which all nine positions contain placeholder characters
**WHEN** the Validator processes the string
**THEN** it returns `ILL`

### SCENARIO 3: Return ILL for a string with an intermediate number of placeholders
**Scenario ID:** VALIDATION-BE-003.2-S003
**GIVEN** a nine-character account string in which four positions contain placeholder characters and five positions contain decimal digits
**WHEN** the Validator processes the string
**THEN** it returns `ILL`, confirming there is no threshold below which ILL is suppressed

---

#### VALIDATION-BE-003.3 – Confirm that the Validator does not format or annotate output lines for ILL entries

**Story ID:** VALIDATION-BE-003.3
**Parent story:** VALIDATION-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Processor writes annotated result lines; Validator returns a status value only)
- `architecture/06-runtime-view.md`, Section 6.2 (ILL path comparison table: Validator output is `ILL`; result line annotation ` ILL` is applied by the Processor)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (result classification table)
- `architecture/09-architecture-decisions.md`, ADR-002

**AS A** BankOCR developer,
**I WANT** the Validator to return the string `ILL` as a status value and leave all output line formatting to the Processor,
**SO THAT** the Validator's responsibility remains limited to classification and the output format can change without touching the Validator.

#### Acceptance Scenarios

### SCENARIO 1: Validator return value for a placeholder-containing string is the bare status token ILL
**Scenario ID:** VALIDATION-BE-003.3-S001
**GIVEN** a nine-character account string containing at least one placeholder character
**WHEN** the Validator processes the string
**THEN** the return value is the string `ILL` with no leading space, no account string prefix, and no surrounding punctuation

### SCENARIO 2: Validator makes no call to any file-writing or output-formatting function
**Scenario ID:** VALIDATION-BE-003.3-S002
**GIVEN** the Validator module source code
**WHEN** the logic for returning `ILL` is inspected
**THEN** no file-open, file-write, string-concatenation with an account string, or output-formatting call is present; the Validator only returns the status token

### SCENARIO 3: Processor is solely responsible for appending the ILL annotation to the result line
**Scenario ID:** VALIDATION-BE-003.3-S003
**GIVEN** the Processor receives `ILL` from the Validator for a given account string
**WHEN** the Processor formats the result line
**THEN** it produces a line containing the nine-character account string followed by ` ILL`; this formatting occurs in the Processor, not in the Validator (confirmed by PROCESSING-BE-002.2)

---

### Infrastructure Stories

#### VALIDATION-INFRA-003.1 – Test ILL classification in isolation using unittest

**Story ID:** VALIDATION-INFRA-003.1
**Parent story:** VALIDATION-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/02-constraints.md`, Section 2.1 (TC-1, TC-3, TC-5)
- `architecture/05-building-block-view.md`, Section 5.2 (Dependency rules: Validator has no file-system dependency)
- `architecture/08-crosscutting-concepts.md`, Section 8.3 (Validator testability convention)
- `architecture/10-quality-requirements.md`, QS-02, QS-06, QS-07

**AS A** BankOCR developer,
**I WANT** the Validator's ILL classification to be covered by `unittest` tests that pass account strings containing placeholder characters directly to the Validator,
**SO THAT** the boundary between ILL, VALID, and ERR outcomes is verified automatically without file fixtures or external tools.

#### Acceptance Scenarios

### SCENARIO 1: Test confirms ILL for a string with one placeholder
**Scenario ID:** VALIDATION-INFRA-003.1-S001
**GIVEN** a `unittest` test case that constructs a nine-character string containing exactly one placeholder character
**WHEN** the string is passed directly to the Validator
**THEN** the test asserts that the return value is `ILL`

### SCENARIO 2: Test confirms ILL for a string where all nine positions are placeholders
**Scenario ID:** VALIDATION-INFRA-003.1-S002
**GIVEN** a `unittest` test case that constructs a nine-character string consisting entirely of placeholder characters
**WHEN** the string is passed directly to the Validator
**THEN** the test asserts that the return value is `ILL`

### SCENARIO 3: ILL classification tests require no file fixtures
**Scenario ID:** VALIDATION-INFRA-003.1-S003
**GIVEN** the full set of `unittest` tests for VALIDATION-STORY-003
**WHEN** the suite is executed
**THEN** no test creates, reads, or deletes a file on disk, and no temporary directory is required

---

#### VALIDATION-INFRA-003.2 – Confirm that ILL classification introduces no file I/O, no checksum calculation, and no output formatting

**Story ID:** VALIDATION-INFRA-003.2
**Parent story:** VALIDATION-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/05-building-block-view.md`, Section 5.2 (Validator has no file-system dependency)
- `architecture/08-crosscutting-concepts.md`, Section 8.1 (checksum skipped when placeholder present), Section 8.2 (Separation of I/O from logic)
- `architecture/09-architecture-decisions.md`, ADR-002 (File I/O confined to Processor)

**AS A** BankOCR developer,
**I WANT** the Validator's ILL classification logic to operate entirely on in-memory strings, with no file access, no checksum arithmetic, and no output line formatting,
**SO THAT** the Validator remains independently testable, the checksum is never applied to non-digit input, and the output format remains the Processor's sole responsibility.

#### Acceptance Scenarios

### SCENARIO 1: Validator produces no file-system side effects when returning ILL
**Scenario ID:** VALIDATION-INFRA-003.2-S001
**GIVEN** an invocation of the Validator with a nine-character string containing at least one placeholder
**WHEN** the Validator runs to completion and returns `ILL`
**THEN** no file is created, modified, or deleted on the file system as a side effect

### SCENARIO 2: Validator return value contains only the status token with no formatting
**Scenario ID:** VALIDATION-INFRA-003.2-S002
**GIVEN** an invocation of the Validator with a string containing at least one placeholder character
**WHEN** the Validator returns
**THEN** the return value is exactly the three-character string `ILL` with no surrounding whitespace, no account string prefix, and no newline character

### SCENARIO 3: No checksum arithmetic is performed when the ILL path is taken
**Scenario ID:** VALIDATION-INFRA-003.2-S003
**GIVEN** the Validator module source code
**WHEN** the ILL return path is inspected
**THEN** the placeholder check appears before any multiplication or modulo operation; no weighted sum is computed on a string that contains a placeholder

---

#### VALIDATION-INFRA-003.3 – Confirm event inapplicability and define observability for ILL classification

**Story ID:** VALIDATION-INFRA-003.3
**Parent story:** VALIDATION-STORY-003
**Priority:** Supporting
**Architecture references:**
- `architecture/03-context-and-scope.md`, Section 3.3 (no network interfaces, message queues, or external services)
- `architecture/09-architecture-decisions.md`, ADR-001 (no event infrastructure)
- `architecture/10-quality-requirements.md`, QS-02, QS-07
- `architecture/11-risks-and-technical-debt.md`, DEBT-03

**AS A** BankOCR developer,
**I WANT** ILL classification outcomes to be observable through `unittest` test results and the downstream ` ILL` annotation in the output file, rather than through event infrastructure,
**SO THAT** illegible entry detection is verifiable without introducing monitoring services that the architecture does not approve.

> **Event infrastructure:** BankOCR has no message queues, event buses, pub/sub topics, or distributed tracing (ADR-001, Section 3.3). Event-driven infrastructure is not applicable to the VALIDATION domain. The `ILL` status token returned by the Validator is the signal that propagates the illegible-entry condition to the Processor, which writes the ` ILL` annotation to the output file.

#### Acceptance Scenarios

### SCENARIO 1: unittest test suite surfaces any incorrect ILL classification logic
**Scenario ID:** VALIDATION-INFRA-003.3-S001
**GIVEN** the Validator unit tests for VALIDATION-STORY-003 are executed with `python -m unittest`
**WHEN** the ILL classification logic is incorrect — for example, returning `ERR` or `VALID` for a string that contains a placeholder
**THEN** one or more tests fail and the runner exits with a non-zero exit code, surfacing the defect

### SCENARIO 2: An entry with an unrecognised glyph produces a visible ILL annotation in the output file
**Scenario ID:** VALIDATION-INFRA-003.3-S002
**GIVEN** the CLI is invoked with an input file containing an account entry in which one or more glyphs were unrecognised by the Parser (producing a placeholder in the account string)
**WHEN** the full pipeline runs to completion
**THEN** the corresponding result line in the output file is suffixed with ` ILL`, confirming the `ILL` status propagated correctly from the Validator through the Processor

### SCENARIO 3: No event infrastructure is present in the Validator module for ILL classification
**Scenario ID:** VALIDATION-INFRA-003.3-S003
**GIVEN** the Validator module source code
**WHEN** the ILL classification logic is inspected
**THEN** no message queue, event bus, logging call, or external monitoring service is invoked; the Validator returns `ILL` and no other side effect occurs

---

### DDD Analysis

**Bounded context:** VALIDATION — same bounded context as VALIDATION-STORY-001 and VALIDATION-STORY-002. This story focuses on the ILL branch of the Validator's classification logic.

**Conceptual domain elements relevant to this story** (subset of elements defined in VALIDATION-STORY-001):

| Element | Type | Description |
|---------|------|-------------|
| `AccountString` | Value object | As defined in VALIDATION-STORY-001. This story constrains the input to the ILL path: a nine-character string in which one or more positions contain a placeholder character produced by the Parser (PARSING-STORY-002). |
| `ValidationStatus` | Value object | As defined in VALIDATION-STORY-001. This story focuses on the `ILL` variant: the value returned when the placeholder inspection step finds at least one non-digit position. |
| `ChecksumRule` | Domain service | As defined in VALIDATION-STORY-001. This story establishes that `ChecksumRule` is not invoked on the ILL path; placeholder detection is a gate that must be passed before `ChecksumRule` is applied. |

**Domain rules specific to this story:**
1. Placeholder inspection is performed before any checksum arithmetic; it is the first step of the Validator's classification logic (ch. 8.1).
2. If one or more placeholder characters are found anywhere in the `AccountString`, the Validator returns `ILL` immediately without computing the weighted sum.
3. `ILL` is returned regardless of the number of placeholder positions — one placeholder and nine placeholders both produce `ILL`.
4. The Validator's responsibility ends at returning the `ILL` token; no output line is formatted and no file is written (ADR-002, ch. 5.2).
5. The ` ILL` annotation in the output file is produced by the Processor (PROCESSING-BE-002.2), not by the Validator.

**Relationship to VALIDATION-STORY-001 and VALIDATION-STORY-002:**
- VALIDATION-STORY-001 establishes the algorithm and proves placeholder detection suppresses the checksum. This story establishes the user-visible outcome of the ILL branch and reinforces the Validator/Processor boundary.
- VALIDATION-STORY-002 covers the ERR branch (all digits, non-zero checksum). ILL and ERR are mutually exclusive: ILL fires when any placeholder is present; ERR fires only when no placeholder is present (ch. 8.1 rules 1 and 3).

**Cross-domain signal:** The placeholder character in the `AccountString` is produced by the Parser (PARSING domain, PARSING-STORY-002) and detected by the Validator (VALIDATION domain, this story). It is the only mechanism by which the PARSING domain communicates an unrecognised glyph to the VALIDATION domain. The Processor passes the string between them without interpreting it (PROCESSING domain, PROCESSING-BE-002.1).

---

### Traceability

| Source | Story / Sub-story / Scenario |
|--------|------------------------------|
| FR-5 – Mark illegible accounts as ILL (Validator's role: detect placeholder, return ILL) | VALIDATION-STORY-003, VALIDATION-BE-003.1, VALIDATION-BE-003.1-S001, VALIDATION-BE-003.1-S002, VALIDATION-BE-003.2, VALIDATION-BE-003.2-S001, VALIDATION-BE-003.2-S002 |
| TC-1 – Python ≥ 3.12 | VALIDATION-INFRA-003.1-S001 |
| TC-3 – Standard library only | VALIDATION-INFRA-003.1-S001 |
| TC-5 – unittest | VALIDATION-INFRA-003.1-S001, VALIDATION-INFRA-003.3-S001 |
| ADR-001 – Single CLI, no external services | VALIDATION-INFRA-003.3-S003 |
| ADR-002 – File I/O confined to Processor | VALIDATION-BE-003.3-S002, VALIDATION-INFRA-003.2-S001, VALIDATION-INFRA-003.2-S003 |
| QS-02 – Unrecognised glyph handling | VALIDATION-STORY-003-S001, VALIDATION-STORY-003-S004, VALIDATION-BE-003.1-S001, VALIDATION-INFRA-003.3-S001 |
| QS-06 – Validator tested without file I/O | VALIDATION-INFRA-003.1-S003, VALIDATION-INFRA-003.2-S001 |
| QS-07 – Test suite runs with no external dependencies | VALIDATION-INFRA-003.1-S001, VALIDATION-INFRA-003.3-S001 |
| ch. 6.2 – ILL path: Validator detects placeholder, returns ILL, skips checksum | VALIDATION-STORY-003-S004, VALIDATION-BE-003.1-S001, VALIDATION-BE-003.1-S002, VALIDATION-INFRA-003.3-S002 |
| ch. 6.3 – Validator called once per string, returns exactly one status | VALIDATION-STORY-003-S001, VALIDATION-STORY-003-S002 |
| ch. 8.1 – Placeholder present → ILL; checksum skipped; result classification table | VALIDATION-STORY-003-S003, VALIDATION-STORY-003-S004, VALIDATION-BE-003.1-S003, VALIDATION-BE-003.2-S003, VALIDATION-BE-003.3-S001, VALIDATION-INFRA-003.2-S003 |
| ch. 8.2 – Separation of I/O from logic | VALIDATION-INFRA-003.2-S001, VALIDATION-INFRA-003.2-S003 |
| DEBT-03 – No structured logging | VALIDATION-INFRA-003.3-S003 |
| PARSING-STORY-002 – Parser inserts placeholder (cross-reference) | VALIDATION-STORY-003-S001, VALIDATION-BE-003.1-S001 |
| PROCESSING-BE-002.2 – Processor formats ` ILL` annotation (cross-reference) | VALIDATION-BE-003.3-S003, VALIDATION-INFRA-003.3-S002 |

---

**Bundle status:** Approved
