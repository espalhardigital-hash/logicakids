## ADDED Requirements

### Requirement: Contextual Percentage Questions Generation
The backend SHALL seed percentage-related questions using real-world contexts instead of exclusively abstract shapes.

#### Scenario: Seeding Phase 4 Module 3
- **WHEN** the backend generates or seeds questions for percentage levels in Phase 4
- **THEN** it must include questions that define `tipo_visual: 'contextual_bar'` and provide contextual text (e.g., minutes of battery, MB downloaded) matching a predefined set of mathematically friendly base numbers (e.g., 100, 200, 400, 500, 600, 1000) and percentages (e.g., 10, 20, 25, 30, 40, 50, 60, 75, 80, 90).
