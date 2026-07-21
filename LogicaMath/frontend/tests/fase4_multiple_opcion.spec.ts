import { test, expect } from '@playwright/test';

test.describe('Fase 4 Multiple Opcion Redesign', () => {

  test.beforeEach(async ({ page }) => {
    // Forward console logs
    page.on('console', msg => console.log(`[Browser Console] ${msg.text()}`));

    // Navigate and mock auth like in other tests
    await page.addInitScript(() => {
      window.localStorage.setItem('auth_user', JSON.stringify({
        id: 1,
        username: 'AdminTest',
        role: 'ADMIN',
        unlocked_level: 100
      }));
      window.localStorage.setItem('auth_token', 'mock-token');
    });
    await page.route('**/users/me*', route => route.fulfill({ json: { id: 1, username: 'AdminTest', role: 'ADMIN' } }));
    await page.route('**/pedagogy/config/*', route => route.fulfill({ json: {} }));
    await page.route('**/admin/settings', route => route.fulfill({ json: {} }));
    await page.route('**/admin/configuracion*', route => route.fulfill({ json: [] }));
  });

  test('Should allow selecting an option and clicking confirm, then auto-advance on incorrect in challenge mode', async ({ page }) => {
    // Mock the dashboard to show mixed challenge available
    await page.route('**/fase4/dashboard', async route => {
      const json = {
        alumno_nombre: "AdminTest",
        puntos_totales: 120,
        desafio_mixto_disponible: true,
        desafio_mixto_estado: "en_progreso",
        modulos: []
      };
      await route.fulfill({ json });
    });

    // Mock the question to be a multiple_opcion
    await page.route('**/fase4/modulo/*/nivel/*/pregunta*', async route => {
      const json = {
        id: 101,
        enunciado: "Test Question",
        tipo_pregunta: "multiple_opcion",
        dificultad: "basico",
        respuesta_correcta: "B",
        alternativas: [
          { id: 1, texto: "A" },
          { id: 2, texto: "B" }, // correct
          { id: 3, texto: "C" }
        ],
        tiempo_limite_segundos: 60,
        tiene_cronometro: true,
        cantidad_requerida: 10,
        aciertos_acumulados: 0,
        intentos_totales: 0,
        porcentaje_actual: 0
      };
      await route.fulfill({ json });
    });

    // Mock the answer submission (Incorrect)
    await page.route('**/fase4/responder', async route => {
      const json = {
        es_correcta: false,
        aciertos_acumulados: 0,
        intentos_totales: 1,
        porcentaje_actual: 0,
        respuesta_correcta: "B",
        early_exit: false
      };
      await route.fulfill({ json });
    });

    // 1. Navigate to map first to establish authenticated session
    await page.goto('/map');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);
    
    // 2. Navigate to Welcome Screen of Fase 4
    await page.goto('/welcome-fase4');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);

    // 3. Click "Iniciar Desafío" (Desafío Mixto) which sets moduloId = 99, nivelId = 99
    const challengeButton = page.getByRole('button', { name: /Iniciar Desafío/i });
    await expect(challengeButton).toBeVisible();
    await challengeButton.click();
    
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);
    
    // Check if splash screen is visible and click start
    try {
      const startButton = page.getByRole('button', { name: /comenzar/i });
      if (await startButton.isVisible()) {
        await startButton.click();
      }
    } catch (e) {
      // ignore
    }

    // Wait for alternatives to render
    await page.waitForSelector('text="A"');
    
    // Verify CONFIRMAR is disabled initially
    const confirmBtn = page.getByRole('button', { name: /confirmar/i });
    await expect(confirmBtn).toBeDisabled();

    // Select incorrect alternative "A"
    await page.getByRole('button', { name: "A", exact: true }).click();
    
    // CONFIRMAR should be enabled now
    await expect(confirmBtn).toBeEnabled();

    // Click CONFIRMAR
    await confirmBtn.click();

    // Verify auto-advance happens (we check if a GET request to /pregunta is made for the next question)
    const requestPromise = page.waitForRequest(request => request.url().includes('/pregunta') && request.method() === 'GET');
    await requestPromise;
  });

  test('Should call /pregunta with reload=true on initial mount', async ({ page }) => {
    // Mock the dashboard to show mixed challenge available
    await page.route('**/fase4/dashboard', async route => {
      const json = {
        alumno_nombre: "AdminTest",
        puntos_totales: 120,
        desafio_mixto_disponible: true,
        desafio_mixto_estado: "en_progreso",
        modulos: []
      };
      await route.fulfill({ json });
    });

    // Capture the first GET request to /pregunta and verify it has reload=true
    let hasReloadTrue = false;
    await page.route('**/fase4/modulo/*/nivel/*/pregunta*', async route => {
      const url = route.request().url();
      if (url.includes('reload=true')) {
        hasReloadTrue = true;
      }
      const json = {
        id: 101,
        enunciado: "Initial Question",
        tipo_pregunta: "multiple_opcion",
        dificultad: "basico",
        respuesta_correcta: "B",
        alternativas: [
          { id: 1, texto: "A" },
          { id: 2, texto: "B" }
        ],
        tiempo_limite_segundos: 60,
        tiene_cronometro: true,
        cantidad_requerida: 10,
        aciertos_acumulados: 0,
        intentos_totales: 0,
        porcentaje_actual: 0
      };
      await route.fulfill({ json });
    });

    // 1. Navigate to map and then welcome phase 4
    await page.goto('/map');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);
    await page.goto('/welcome-fase4');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);

    // 2. Click "Iniciar Desafío"
    const challengeButton = page.getByRole('button', { name: /Iniciar Desafío/i });
    await challengeButton.click();
    await page.waitForLoadState('domcontentloaded');
    
    // Check if splash screen is visible and click start
    try {
      const startButton = page.getByRole('button', { name: /comenzar/i });
      if (await startButton.isVisible()) {
        await startButton.click();
      }
    } catch (e) {}

    // Wait for alternatives to render (ensures the question load finished)
    await page.waitForSelector('text="A"');

    // Expect that the request had reload=true
    expect(hasReloadTrue).toBe(true);
  });
});
