## 1. UI Redesign

- [x] 1.1 Add `selectedAltId` state to `Fase4GameScreen.tsx`.
- [x] 1.2 Update `multiple_opcion` alternative buttons to set `selectedAltId` instead of calling `handleSubmit` directly.
- [x] 1.3 Add a "Confirmar" / "Continuar" / "Intentar de nuevo" button specifically for `multiple_opcion` questions, mirroring the Phase 2 design.

## 2. Logic Update

- [x] 2.1 Update `handleSubmit` in `Fase4GameScreen.tsx` to handle submission when `selectedAltId` is set, mapping the ID to the alternative's text.
- [x] 2.2 Ensure the confirmation button calls `handleSubmit` and properly transitions the UI state.
- [x] 2.3 Ensure 1.5s auto-advance is present for challenge mode incorrect answers.

## 3. Testing

- [x] 3.1 Create and run an automated test (Playwright) to verify the new confirmation flow and auto-advance in Fase 4 multiple choice questions.

## 4. Version Control (GitHub)

- [x] 4.1 Check status of git repository.
- [x] 4.2 Commit the changes to `Fase4GameScreen.tsx` with a descriptive message in the `desarrollo` branch.
- [x] 4.3 Update the repository using `git push` (after explicit approval if needed).

## 5. Deployment

- [x] 5.1 Re-deploy the local containers using `docker compose -f docs/Pruebas_y_Test_Unitario/docker-compose.local.yml up -d --build`.
- [x] 5.2 Deploy to VPS (desarrollo): *Skipped per rule "Modo de Pruebas Locales (100% Local) — ACTIVO".*
- [x] 5.3 Deploy to VPS (produccion): *Skipped per rule "Modo de Pruebas Locales (100% Local) — ACTIVO".*
- [x] 5.4 Check logs of both deployed containers to verify stability. *Skipped for VPS.*
