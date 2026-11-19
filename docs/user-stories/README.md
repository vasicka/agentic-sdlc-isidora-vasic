# BankOCR – User Stories

## 1. Overview

This document contains the prioritized user story backlog for the BankOCR application.

The requirements are derived from the approved arc42 architecture documentation in the `architecture/` directory.

BankOCR is a Python 3 command-line application that reads ASCII representations of bank account numbers, recognizes digits, validates account numbers using the mod-11 checksum, and writes results to a text file.

## 2. Domains and Bounded Contexts

The following logical domains are derived from the BankOCR architecture.

| Domain | Component | Responsibility |
|--------|-----------|----------------|
| PARSING | Parser | Recognizes ASCII digits and assembles nine-digit account numbers. |
| VALIDATION | Validator | Validates account numbers and determines VALID, ERR, or ILL status. |
| PROCESSING | Processor | Reads input files, coordinates parsing and validation, and writes output files. |

These domains represent logical responsibility boundaries within a single CLI application, not independently deployed services.

## 3. Prioritized User Story Backlog

| Story ID | Title | Domain | Priority | Status |
|----------|-------|--------|----------|--------|
| PARSING-STORY-001 | Recognise ASCII digits and assemble account numbers | PARSING | **CORE** | Approved |
| VALIDATION-STORY-001 | Validate account numbers with mod-11 checksum | VALIDATION | **CORE** | Approved |
| PROCESSING-STORY-002 | Coordinate parse-validate-record pipeline per entry | PROCESSING | **CORE** | Approved |
| PROCESSING-STORY-001 | Read input file and split into account entries | PROCESSING | Supporting | Approved |
| PROCESSING-STORY-003 | Write annotated results file | PROCESSING | Supporting | Approved |
| PARSING-STORY-002 | Handle unrecognised glyphs with a placeholder | PARSING | Supporting | Approved |
| VALIDATION-STORY-002 | Mark checksum-failing accounts as ERR | VALIDATION | Supporting | Approved |
| VALIDATION-STORY-003 | Mark accounts with unrecognised glyphs as ILL | VALIDATION | Supporting | Approved |
| PROCESSING-STORY-005 | Invoke the application via a single CLI command | PROCESSING | Supporting | Approved |
| PROCESSING-STORY-004 | Handle malformed input file with a diagnostic | PROCESSING | Supporting | Approved |

## 4. Pareto Analysis

### Candidate evaluation

Each story was evaluated against four criteria: MVP necessity, dependency foundation, user-visible value, and architectural coverage.

| Story ID | MVP necessity | Dependency foundation | User-visible value | Architecture coverage |
|----------|---------------|-----------------------|--------------------|----------------------|
| PARSING-STORY-001 | High | High | High | FR-2, FR-3 |
| PARSING-STORY-002 | High | High | High | FR-5 |
| VALIDATION-STORY-001 | High | High | High | FR-4 |
| VALIDATION-STORY-002 | High | Medium | High | FR-6 |
| VALIDATION-STORY-003 | High | Medium | High | FR-5 |
| PROCESSING-STORY-001 | High | High | High | FR-1 |
| PROCESSING-STORY-002 | High | High | High | FR-1, FR-7 |
| PROCESSING-STORY-003 | High | Medium | High | FR-7 |
| PROCESSING-STORY-004 | Low | Low | Medium | RISK-02, ch. 8.4 |
| PROCESSING-STORY-005 | Medium | Low | High | QS-11, ch. 7 |

### Impact ranking and CORE selection

Stories ranked by impact (highest first):

1. **PARSING-STORY-001** — the entire pipeline starts here; digit recognition is a dependency of every downstream component
2. **VALIDATION-STORY-001** — the mod-11 logic is the core correctness requirement of the kata
3. **PROCESSING-STORY-002** — the pipeline coordinator; it connects Parser and Validator into a working end-to-end system

**CORE story count: 3 out of 10 (30%)**

A strict 20% selection would yield 2 stories, which cannot produce a runnable pipeline path. 3 stories is the minimum set that enables a demonstrably working system end-to-end (Parse → Validate → Record). The 10% deviation from 20% is justified by the small backlog size and the indivisibility of the core pipeline. The remaining 7 stories cover essential error paths, CLI invocation, output formatting, and input validation; they are Supporting, not optional.

This analysis does not claim that 3 stories mathematically deliver 80% of business value. It identifies the 3 stories whose absence would render the application non-functional.

## 5. Architecture Traceability

| Domain | Architecture Reference | Functional Requirements |
|--------|------------------------|-------------------------|
| PARSING | `architecture/05-building-block-view.md`, Section 5.2 | FR-2, FR-3, FR-5 |
| VALIDATION | `architecture/05-building-block-view.md`, Section 5.2 | FR-4, FR-5, FR-6 |
| PROCESSING | `architecture/05-building-block-view.md`, Section 5.2 | FR-1, FR-7 |

Functional requirements are defined in `architecture/01-introduction-and-goals.md`, Section 1.1.
Technical constraints are defined in `architecture/02-constraints.md`.
Quality scenarios are defined in `architecture/10-quality-requirements.md`.
Risks and technical debt are defined in `architecture/11-risks-and-technical-debt.md`.

## 6. Story Bundle Progress

User story bundles are stored in separate domain files:

- `parsing.md` — PARSING domain
- `validation.md` — VALIDATION domain
- `processing.md` — PROCESSING domain

Each bundle includes a parent user story, testable acceptance scenarios, and applicable BE and INFRA sub-stories.

FE stories are not applicable. BankOCR has no graphical frontend; all user interaction is through plain-text files on the local file system.

INFRA requirements are confined to: CLI deployment and execution, plain-text file I/O, event applicability, and observability via exit codes and test results. No web interfaces, containers, databases, message brokers, or external services are introduced.

## 7. Approval Status and CORE Progress

| Metric | Value |
|--------|-------|
| Total stories | 10 |
| CORE stories | 3 |
| CORE percentage | 30% |
| CORE bundles completed | 3 |
| CORE bundles remaining | 0 |
| Supporting bundles completed | 7 |
| Supporting bundles remaining | 0 |

| Bundle | Status |
|--------|--------|
| PARSING-STORY-001 | Approved |
| VALIDATION-STORY-001 | Approved |
| PROCESSING-STORY-002 | Approved |
| PROCESSING-STORY-001 | Approved |
| PROCESSING-STORY-003 | Approved |
| PARSING-STORY-002 | Approved |
| VALIDATION-STORY-002 | Approved |
| VALIDATION-STORY-003 | Approved |
| PROCESSING-STORY-005 | Approved |
| PROCESSING-STORY-004 | Approved |
