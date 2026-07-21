## ADDED Requirements

### Requirement: Differentiate Questions by Level
The Phase 5 question generation logic SHALL generate distinct question templates and parameters based on the module's difficulty level (`lvl_id`).

#### Scenario: Module 1 Level 1 (Discovery)
- **WHEN** the generator generates a question for M1-N1
- **THEN** it generates a perimeter counting question using a visual grid.

#### Scenario: Module 1 Level 3 (Fluency)
- **WHEN** the generator generates a question for M1-N3
- **THEN** it generates a perimeter unit conversion question without a grid.

### Requirement: Deduplicate Distractor Alternatives
The system MUST ensure that all alternative answers generated for a multiple-choice question are unique and none of them overlap with the correct answer.

#### Scenario: Generating Area Question Distractors
- **WHEN** the generator creates distractors for an area question (e.g. `a=4, b=4`, correct answer `16`)
- **THEN** it verifies that distractors like `2*(a+b)` do not result in `16`, generating a distinct fallback distractor instead.

### Requirement: Expand Template Variety
The system SHALL support at least 3 distinct wording templates per module-level combination to prevent monotony in repetitive practice sessions.

#### Scenario: Practicing the Same Level
- **WHEN** a user plays 10 questions in the same module and level
- **THEN** they experience a variety of phrasing styles (e.g., "calculate the total perimeter", "how much fence is needed", "how many steps to walk around").
