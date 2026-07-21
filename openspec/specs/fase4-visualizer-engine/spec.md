# Spec: Fase 4 Visualizer Engine

## Purpose
Centralización y estandarización del motor de visualizadores interactivos y estáticos de la Fase 4.

## Requirements

### Requirement: Centralized Rendering of Visualizers
The `Fase4VisualizerEngine` component SHALL render the correct SVG/interactive representation based on the `datos_numericos.tipo_visual` prop of a given question.

#### Scenario: Renders Pizza Visualizer
- **WHEN** the question visual type is "pizza"
- **THEN** it renders the `PizzaFractionVisualizer` component with the provided interactive props

#### Scenario: Renders Beaker Visualizer
- **WHEN** the question visual type is "beaker"
- **THEN** it renders the `BeakerVisualizer` component
