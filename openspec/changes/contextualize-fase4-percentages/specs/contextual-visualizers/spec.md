## ADDED Requirements

### Requirement: Render Contextual Percentage Bar
The system SHALL provide a frontend visualizer capable of rendering 1D percentage bars based on real-world themes.

#### Scenario: Rendering a battery theme
- **WHEN** a question is loaded with `tipo_visual: 'contextual_bar'` and `theme: 'battery'`
- **THEN** the system renders a battery-shaped progress bar filled to the specified percentage, displaying the remaining or total time.

#### Scenario: Rendering a download theme
- **WHEN** a question is loaded with `tipo_visual: 'contextual_bar'` and `theme: 'download'`
- **THEN** the system renders a digital download progress bar.

### Requirement: Explicit Equation Display
The system SHALL display the mathematical relationship explicitly for contextual questions.

#### Scenario: Displaying the formula box
- **WHEN** the `ContextualPercentageVisualizer` is rendered
- **THEN** a formula box displaying `X% de Y = [ ? ]` (or similar format) is rendered below the visualizer to map the scenario to the abstract math.
