export const PRACTICE_REQUIRED_CORRECT_ANSWERS = 10;

export const calculateProgressPercentage = (
  correctAnswers: number,
  requiredAnswers: number,
): number => {
  if (requiredAnswers <= 0) return 0;
  return Math.min(100, Math.max(0, Math.floor((correctAnswers / requiredAnswers) * 100)));
};
