import React from 'react';

const GameScreen = React.lazy(() => import('./fase1/GameScreen'));

export interface PlayRouteWrapperProps {
  category: string;
  difficulty: string;
  currentUser: any;
  adminConfig: any;
  modularConfigs: any;
  isEvaluatorMode: boolean;
  handleEndGame: any;
  navigate: any;
}

export const PlayRouteWrapper: React.FC<PlayRouteWrapperProps> = ({
  category,
  difficulty,
  currentUser,
  adminConfig,
  modularConfigs,
  isEvaluatorMode,
  handleEndGame,
  navigate
}) => {
  const categoryToModId: Record<string, number> = {
    'addition': 1,
    'subtraction': 2,
    'multiplication': 3,
    'division': 4,
    'challenge': 5
  };
  const difficultyToLevelId: Record<string, number> = {
    'easy': 1,
    'easy_medium': 2,
    'medium': 3,
    'medium_hard': 4,
    'hard': 5,
    'random_tables': 6
  };
  const modId = categoryToModId[category] || 1;
  const levelId = difficultyToLevelId[difficulty] || 3;
  const computedSeccion = modId * 100 + levelId;

  return (
    <React.Suspense fallback={<div className="p-8 text-center text-white">Cargando juego...</div>}>
      <GameScreen
        category={category as any}
        difficulty={difficulty as any}
        userSettings={currentUser?.settings}
        adminConfig={adminConfig}
        modularConfigs={modularConfigs}
        faseId={currentUser?.fase_actual_id || 1}
        seccion={computedSeccion}
        isEvaluatorMode={isEvaluatorMode}
        onEndGame={handleEndGame}
        onExit={() => navigate(currentUser ? '/map' : '/welcome')}
      />
    </React.Suspense>
  );
};
