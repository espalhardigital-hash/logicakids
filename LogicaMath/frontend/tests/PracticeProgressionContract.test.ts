import { describe, expect, it } from 'vitest';

import {
  PRACTICE_REQUIRED_CORRECT_ANSWERS,
  calculateProgressPercentage,
} from '../components/common/progression';

describe('practice progression contract', () => {
  it('uses 10 correct answers as the single practice goal', () => {
    expect(PRACTICE_REQUIRED_CORRECT_ANSWERS).toBe(10);
  });

  it.each([
    [0, 0],
    [9, 90],
    [10, 100],
    [11, 100],
  ])('maps %i correct answers to %i%% without exceeding 100', (correct, expected) => {
    expect(calculateProgressPercentage(correct, PRACTICE_REQUIRED_CORRECT_ANSWERS)).toBe(expected);
  });
});
