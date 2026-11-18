# 11. Risks and Technical Debt

This chapter identifies known risks and areas of technical debt in the current BankOCR architecture. Risks are conditions that could prevent the system from meeting its quality goals. Technical debt is work that has been deferred and that will cost more to address the longer it remains.

Each item carries a priority based on its likelihood and impact on the quality goals established in Chapter 1.

---

## 11.1 Risks

### RISK-01: Glyph pattern coverage is not explicitly validated at startup

| Field | Detail |
|-------|--------|
| **Description** | The Parser relies on a static mapping of 3×3 glyph patterns to digits. If the mapping is incomplete or contains a transcription error, the Parser will silently return a placeholder for a valid digit, producing `ILL` results for well-formed input. |
| **Quality goal affected** | Correctness (priority 1) |
| **Likelihood** | Low — the digit set is fixed (0–9) and small |
| **Impact** | High — a single missing pattern causes all entries containing that digit to be misclassified |
| **Mitigation** | Unit tests (QS-01) must cover all ten digits in all nine positions. A startup assertion or test fixture that verifies all ten patterns are present would surface this error immediately. |

### RISK-02: Input file format validation logic is not yet implemented

| Field | Detail |
|-------|--------|
| **Description** | Chapter 8 (section 8.4) establishes that the Processor is architecturally responsible for validating the input file format and handling format errors before passing entries to the Parser. This requirement is defined, but the specific validation logic and its tests have not yet been implemented. If a file with an incorrect number of lines, missing blank separators, or trailing content is processed before this is in place, the Processor may silently produce malformed entries. |
| **Quality goal affected** | Correctness (priority 1) |
| **Likelihood** | Low — input files are User-supplied and the format is well-defined |
| **Impact** | Medium — a malformed file could produce incorrect or misleading output rather than a clear error |
| **Mitigation** | Implement the validation logic already required by Chapter 8, section 8.4: check that the file length is a multiple of four lines and report a clear error if not. Cover this with dedicated Processor tests. |

### RISK-03: No integration test covers the full pipeline end-to-end with a file

| Field | Detail |
|-------|--------|
| **Description** | The testability design (ADR-002, QS-05, QS-06) focuses on isolating Parser and Validator from file I/O. If no test exercises the Processor reading a real input file and writing a real output file, errors in the Processor's coordination logic or output formatting could go undetected until runtime. |
| **Quality goal affected** | Correctness (priority 1), Testability (priority 2) |
| **Likelihood** | Medium — Processor logic is the least covered by the isolated unit test approach |
| **Impact** | Medium — integration defects in the Processor would only appear during manual testing or in production use |
| **Mitigation** | At least one end-to-end test should exercise the Processor with a temporary input file and assert on the content of the resulting output file (QS-07). |

---

## 11.2 Technical Debt

### DEBT-01: Input file validation logic and tests are pending implementation

| Field | Detail |
|-------|--------|
| **Description** | The architectural responsibility for input file format validation is already assigned to the Processor in Chapter 8 (section 8.4). What remains is the implementation of that validation logic and its corresponding tests. Until this is done, the Processor fulfils its coordination role but not its format-error-handling role. |
| **Impact** | A malformed input file may produce misleading output rather than a diagnostic message |
| **Effort to address** | Low — adding a line-count check and a clear error message is a small, localised change to the Processor |
| **Recommended action** | Implement and test input validation in the Processor before the system is used with untrusted input files |

### DEBT-02: Local execution only; no path to other input sources

| Field | Detail |
|-------|--------|
| **Description** | ADR-001 and ADR-002 deliberately scope the system to local file I/O. This is appropriate for the kata but means that reading from stdin, a network stream, or a string buffer requires a Processor change rather than a configuration option. |
| **Impact** | Low for the current scope; would become a constraint if the system were extended |
| **Effort to address** | Medium — the Parser and Validator are already decoupled from file I/O (ADR-002), so only the Processor would need to change; the effort is proportionate to the new input source |
| **Recommended action** | No action required within the current kata scope. If the input source changes, record a new ADR before modifying the Processor. |

### DEBT-03: No structured logging or diagnostics

| Field | Detail |
|-------|--------|
| **Description** | The current architecture does not specify how the application reports progress, errors, or unexpected conditions to the operator. Any error reporting is left to implementation convention. |
| **Impact** | Debugging a silent failure (e.g. RISK-01, RISK-02) requires inspecting source code rather than reading a log |
| **Effort to address** | Low — Python's standard `logging` module requires no external dependency (TC-3) and can be added to the Processor without touching Parser or Validator |
| **Recommended action** | Adopt a minimal logging convention in the Processor for startup, per-file processing, and error conditions before the system processes files in an unattended context |

---

## 11.3 Summary

| ID | Type | Priority | Quality goal affected | Status |
|----|------|----------|-----------------------|--------|
| RISK-01 | Risk | High | Correctness | Mitigated by unit tests (QS-01); no code change required beyond comprehensive test coverage |
| RISK-02 | Risk | Medium | Correctness | Open; addressed by DEBT-01 |
| RISK-03 | Risk | Medium | Correctness, Testability | Open; mitigated by adding an end-to-end Processor test |
| DEBT-01 | Technical debt | Medium | Correctness | Open; low effort to address in the Processor |
| DEBT-02 | Technical debt | Low | Maintainability | Accepted for current scope; revisit if input source changes |
| DEBT-03 | Technical debt | Low | Maintainability | Open; low effort using standard `logging` |
