import { describe, it, expect, vi, beforeEach } from 'vitest';
import * as apiHelper from '../../services/apiHelper';

// Mock apiHelper so we can spy on fetchWithTimeout
vi.mock('../../services/apiHelper', () => ({
  fetchWithTimeout: vi.fn(),
}));

import { getFase2Question } from './Fase2Service';

describe('Fase2Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should use fetchWithTimeout for data loading to prevent permanent hangs', async () => {
    const mockResponseData = { id: 1, enunciado: 'Test' };
    
    (apiHelper.fetchWithTimeout as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponseData,
    });

    try {
      await getFase2Question(1, 1);
    } catch (e) {
      // Ignore
    }

    expect(apiHelper.fetchWithTimeout).toHaveBeenCalled();
  });
});
