# 10. Quality Requirements

Chapter 1 established four quality goals in priority order: correctness, testability, maintainability, and simplicity. This chapter refines each goal into concrete quality scenarios that make the requirement measurable and verifiable. The scenarios follow the arc42 quality scenario structure: stimulus, context, response, and response measure.

---

## 10.1 Quality Tree

```
BankOCR Quality
├── Correctness (priority 1)
│   ├── Digit recognition accuracy
│   ├── Checksum calculation correctness
│   └── Output annotation accuracy (ERR / ILL)
├── Testability (priority 2)
│   ├── Component isolation
│   └── No external test dependencies
├── Maintainability (priority 3)
│   ├── Localised change impact
│   └── Readable component interfaces
└── Simplicity (priority 4)
    ├── Minimal dependencies
    └── No unjustified complexity
```

---

## 10.2 Correctness Scenarios

### QS-01: Digit recognition accuracy

| Field | Detail |
|-------|--------|
| **Stimulus** | The Parser receives a four-line ASCII entry containing a known digit glyph in each of the nine positions |
| **Context** | Normal operation; all glyphs conform to the kata-specified 3×3 patterns |
| **Response** | The Parser returns a nine-character string in which each character matches the correct decimal digit |
| **Response measure** | All ten digit glyphs (0–9) are recognised correctly in every position; no recognised glyph is mapped to the wrong digit |

### QS-02: Unrecognised glyph handling

| Field | Detail |
|-------|--------|
| **Stimulus** | The Parser receives an entry containing one or more glyphs that do not match any known 3×3 pattern |
| **Context** | Input contains a malformed or damaged glyph |
| **Response** | The Parser inserts a placeholder character for each unrecognised glyph; the Validator returns `ILL`; the Processor writes the result line with ` ILL` |
| **Response measure** | No unrecognised glyph is silently mapped to a digit; the output line is annotated with ` ILL` without exception or crash |

### QS-03: Checksum validation correctness

| Field | Detail |
|-------|--------|
| **Stimulus** | The Validator receives a nine-character account string where all digits are recognised |
| **Context** | Normal operation |
| **Response** | The Validator applies `(d9 + 2·d8 + … + 9·d1) mod 11`; returns `VALID` if the result is 0, `ERR` otherwise |
| **Response measure** | The Validator agrees with a manual checksum calculation for every test case derived from the kata specification |

### QS-04: Output annotation accuracy

| Field | Detail |
|-------|--------|
| **Stimulus** | The Processor processes a file containing a mix of valid, ERR, and ILL account entries |
| **Context** | Normal operation |
| **Response** | Each output line carries exactly the correct annotation: no suffix for `VALID`, ` ERR` for checksum failures, ` ILL` for illegible entries |
| **Response measure** | Zero incorrectly annotated lines; zero entries omitted from the output file |

---

## 10.3 Testability Scenarios

### QS-05: Parser tested without file I/O

| Field | Detail |
|-------|--------|
| **Stimulus** | A developer writes a unit test for the Parser |
| **Context** | Development environment; `unittest` only |
| **Response** | The test passes a multi-line string directly to the Parser and asserts on the returned account string; no file is created or read |
| **Response measure** | The test requires zero file fixtures, zero mock objects, and zero external dependencies |

### QS-06: Validator tested without file I/O

| Field | Detail |
|-------|--------|
| **Stimulus** | A developer writes a unit test for the Validator |
| **Context** | Development environment; `unittest` only |
| **Response** | The test passes a nine-character string directly to the Validator and asserts on the returned status |
| **Response measure** | The test requires zero file fixtures, zero mock objects, and zero external dependencies |

### QS-07: Full test suite runs with no external dependencies

| Field | Detail |
|-------|--------|
| **Stimulus** | A developer runs the full test suite on a machine with Python ≥ 3.12 and no additional packages installed |
| **Context** | CI or local development |
| **Response** | All tests execute and produce a pass or fail result |
| **Response measure** | No `ImportError`, no missing dependency, no network call required to complete the suite |

---

## 10.4 Maintainability Scenarios

### QS-08: Changing digit recognition does not affect validation

| Field | Detail |
|-------|--------|
| **Stimulus** | A developer modifies the Parser's glyph-to-digit mapping (e.g. to support an additional character set) |
| **Context** | The Validator and Processor are unchanged |
| **Response** | The Validator and Processor require no code changes; only Parser source and Parser tests are affected |
| **Response measure** | Zero changes required outside the Parser module and its tests |

### QS-09: Changing output format does not affect parsing or validation

| Field | Detail |
|-------|--------|
| **Stimulus** | A developer changes how result lines are formatted in the output file (e.g. different annotation tokens) |
| **Context** | The Parser and Validator are unchanged |
| **Response** | Only the Processor's output-writing logic and its tests require changes |
| **Response measure** | Zero changes required outside the Processor module and its tests |

---

## 10.5 Simplicity Scenarios

### QS-10: No unjustified dependencies introduced

| Field | Detail |
|-------|--------|
| **Stimulus** | A developer adds a new feature or fixes a defect |
| **Context** | Normal development |
| **Response** | The change uses only the Python standard library; no third-party package is added |
| **Response measure** | `pyproject.toml` contains no runtime dependencies beyond Python itself; `pip install` is not required to run the application |

### QS-11: Application runs with a single command

| Field | Detail |
|-------|--------|
| **Stimulus** | A User wants to process an account file on a machine with Python ≥ 3.12 installed |
| **Context** | The application source is present on the file system |
| **Response** | The User invokes the CLI with the input file path; the application runs to completion and writes the results file |
| **Response measure** | No build step, no package installation, and no configuration file is required before the first run |
