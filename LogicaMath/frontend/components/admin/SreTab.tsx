import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, AlertTriangle, RefreshCw, Server, Shield, Cpu, Activity, ListChecks, Play, History, Sparkles } from 'lucide-react';

interface Task {
  id: string;
  nombre: string;
  descripcion: string;
  completado: boolean;
}

interface StageData {
  descripcion: string;
  tareas: Task[];
}

interface SreProgress {
  [stageName: string]: StageData;
}

interface HistoryItem {
  filename: string;
  generated_at?: string;
  environment?: string;
  summary?: {
    total_tests: number;
    passed: number;
    failed: number;
    duration_seconds: number;
  };
  note?: string;
}

const SRE_ENDPOINT = import.meta.env.VITE_SRE_ENDPOINT ?? 'http://localhost:9323/progreso_sre.json';
const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/api$/, '');

const METRIC_EXPLANATIONS: Record<string, { title: string; desc: string }> = {
  generated_at: {
    title: "Fecha de Generación",
    desc: "Indica la fecha y hora exacta en que se ejecutó el pipeline de pruebas y se generaron los resultados de calidad.",
  },
  environment: {
    title: "Entorno de Ejecución",
    desc: "Especifica el servidor o entorno (local, dev, prod) donde se corrieron las verificaciones de calidad.",
  },
  version: {
    title: "Versión de la App",
    desc: "El identificador o tag de la versión de software compilada y validada en esta ejecución.",
  },
  summary: {
    title: "Resumen de Métricas",
    desc: "Consolida los resultados globales: número total de pruebas unitarias/E2E ejecutadas, aprobadas, fallidas y duración.",
  },
  suites: {
    title: "Suites de Pruebas",
    desc: "Colecciones de pruebas automatizadas agrupadas por componentes de software analizados.",
  },
  note: {
    title: "Notas e Indicaciones",
    desc: "Información contextual relevante generada de forma automática por el ejecutor de pruebas.",
  },
  build: {
    title: "Fase de Construcción (Build)",
    desc: "Compilación de código, análisis estático (linter) y auditoría rápida de seguridad de dependencias.",
  },
  test: {
    title: "Fase de Pruebas (Test)",
    desc: "Ejecución de pruebas unitarias, de carga/rendimiento, y de regresión visual y funcional (Playwright).",
  },
  deploy: {
    title: "Fase de Despliegue (Deploy)",
    desc: "Publicación en el entorno destino, validación de latencia y pruebas de rollback de contenedores.",
  },
  monitor: {
    title: "Fase de Monitoreo (Monitor)",
    desc: "Supervisión continua en tiempo real del uso de CPU/memoria y análisis automático de tasas de error.",
  },
};

const getAuthHeaders = (): Record<string, string> => {
  const token = localStorage.getItem('auth_token');
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

const SreTab: React.FC = () => {
  const [data, setData] = useState<SreProgress | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isFallback, setIsFallback] = useState<boolean>(false);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [showHistory, setShowHistory] = useState<boolean>(false);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_URL}/admin/sre/history`, {
        headers: getAuthHeaders()
      });
      if (res.ok) {
        const histData = await res.json();
        setHistory(histData);
      }
    } catch {
      // Omitir silently si falla histórico
    }
  };

  const fetchSreData = async () => {
    setLoading(true);
    setError(null);
    setIsFallback(false);
    
    // Intento 1: Servidor de reportes Nginx estático (puerto 9323)
    try {
      const response = await fetch(SRE_ENDPOINT);
      if (response.ok) {
        const jsonData = await response.json();
        setData(jsonData);
        setLoading(false);
        fetchHistory();
        return;
      }
    } catch {
      // Ignorar para intentar fallback backend
    }

    // Intento 2 (Fallback Resiliente): API Backend FastAPI
    try {
      const fallbackUrl = `${API_URL}/admin/sre/status`;
      const fallbackRes = await fetch(fallbackUrl, {
        headers: getAuthHeaders()
      });

      if (fallbackRes.ok) {
        const fallbackJson = await fallbackRes.json();
        setData(fallbackJson);
        setIsFallback(true);
        setError(null);
        fetchHistory();
        return;
      }
      throw new Error(`El backend FastAPI respondió con código HTTP ${fallbackRes.status}`);
    } catch (fallbackErr: any) {
      console.error(fallbackErr);
      setError(fallbackErr.message || 'Error al conectar con la API de reportes');
    } finally {
      setLoading(false);
    }
  };

  const runSreVerification = async () => {
    setIsRefreshing(true);
    try {
      const res = await fetch(`${API_URL}/admin/sre/refresh`, {
        method: 'POST',
        headers: getAuthHeaders()
      });
      if (!res.ok) {
        throw new Error(`Error en el servidor API (${res.status})`);
      }
      const resData = await res.json();
      if (resData.report) {
        setData(resData.report);
        setIsFallback(false);
        setError(null);
        fetchHistory();
      }
    } catch (err: any) {
      alert(`No se pudo ejecutar la verificación SRE: ${err.message}`);
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    fetchSreData();
  }, []);

  const getStageIcon = (stage: string) => {
    switch (stage.toLowerCase()) {
      // Stages
      case 'build': return <Cpu className="text-[#007AFF]" size={20} />;
      case 'test': return <Activity className="text-[#10b981]" size={20} />;
      case 'deploy': return <Server className="text-[#8b5cf6]" size={20} />;
      case 'monitor': return <Shield className="text-[#f59e0b]" size={20} />;
      // Metadata
      case 'generated_at': return <Activity className="text-[#8b5cf6]" size={20} />;
      case 'environment': return <Server className="text-[#10b981]" size={20} />;
      case 'version': return <Cpu className="text-[#f59e0b]" size={20} />;
      case 'summary': return <ListChecks className="text-[#007AFF]" size={20} />;
      case 'suites': return <Shield className="text-[#6366f1]" size={20} />;
      case 'note': return <AlertTriangle className="text-amber-500" size={20} />;
      default: return <ListChecks className="text-slate-400" size={20} />;
    }
  };

  const renderMetadataValue = (key: string, value: any) => {
    if (value === null || value === undefined) return null;

    switch (key.toLowerCase()) {
      case 'generated_at': {
        const date = new Date(value);
        return (
          <div className="p-3 rounded-xl bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 font-mono text-[11px] text-slate-800 dark:text-slate-200">
            {isNaN(date.getTime()) ? String(value) : date.toLocaleString('es-ES', { timeZoneName: 'short' })}
          </div>
        );
      }
      case 'environment': {
        const isLocal = String(value).toLowerCase() === 'local';
        return (
          <div className="flex items-center gap-2">
            <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${isLocal ? 'bg-green-500/15 text-green-500 font-mono' : 'bg-[#007AFF]/15 text-[#007AFF] font-mono'}`}>
              {String(value).toUpperCase()}
            </span>
          </div>
        );
      }
      case 'version': {
        return (
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 font-mono text-xs font-semibold text-[#007AFF]">
              v{String(value)}
            </span>
          </div>
        );
      }
      case 'summary': {
        if (typeof value !== 'object') return String(value);
        const { total_tests, passed, failed, skipped, duration_seconds } = value;
        return (
          <div className="grid grid-cols-2 gap-2.5">
            <div className="p-2.5 rounded-xl bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 flex flex-col">
              <span className="text-[10px] text-slate-400 font-bold uppercase">Total Tests</span>
              <span className="text-lg font-bold text-slate-800 dark:text-slate-200">{total_tests ?? 0}</span>
            </div>
            <div className="p-2.5 rounded-xl bg-green-500/5 border border-green-500/10 flex flex-col">
              <span className="text-[10px] text-green-500 font-bold uppercase">Aprobadas</span>
              <span className="text-lg font-bold text-green-500">{passed ?? 0}</span>
            </div>
            <div className="p-2.5 rounded-xl bg-red-500/5 border border-red-500/10 flex flex-col">
              <span className="text-[10px] text-red-500 font-bold uppercase">Fallidas</span>
              <span className="text-lg font-bold text-red-500">{failed ?? 0}</span>
            </div>
            <div className="p-2.5 rounded-xl bg-amber-500/5 border border-amber-500/10 flex flex-col">
              <span className="text-[10px] text-amber-500 font-bold uppercase">Duración</span>
              <span className="text-lg font-bold text-amber-500">{(duration_seconds ?? 0).toFixed(1)}s</span>
            </div>
          </div>
        );
      }
      case 'suites': {
        const suitesList = Array.isArray(value) ? value : [];
        if (suitesList.length === 0) {
          return (
            <div className="p-3 rounded-xl bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-slate-450 text-xs italic text-center text-slate-400">
              Ninguna suite de pruebas registrada
            </div>
          );
        }
        return (
          <div className="space-y-1 max-h-40 overflow-y-auto pr-1">
            {suitesList.map((suite: any, idx: number) => (
              <div key={idx} className="p-2 rounded-lg bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-[11px] text-slate-800 dark:text-slate-200 flex justify-between">
                <span>{suite.name || `Suite ${idx + 1}`}</span>
                <span className="text-green-500 font-semibold">{suite.passed ? 'OK' : 'FAIL'}</span>
              </div>
            ))}
          </div>
        );
      }
      case 'note': {
        return (
          <div className="p-3 rounded-xl bg-amber-500/5 dark:bg-amber-500/5 border border-amber-500/10 text-[11.5px] text-slate-600 dark:text-slate-350 leading-relaxed italic">
            "{String(value)}"
          </div>
        );
      }
      default:
        return typeof value === 'object' ? JSON.stringify(value) : String(value);
    }
  };

  // Calculate totals
  let totalTasks = 0;
  let completedTasks = 0;
  let isMetadataJson = false;
  let testSummary: any = null;

  if (data) {
    if (data.summary && typeof data.summary === 'object' && !('tareas' in data.summary)) {
      isMetadataJson = true;
      testSummary = data.summary;
      totalTasks = testSummary.total_tests ?? 0;
      completedTasks = testSummary.passed ?? 0;
    } else {
      Object.keys(data).forEach(stage => {
        const stageTasks = Array.isArray(data[stage]?.tareas) ? data[stage].tareas : [];
        totalTasks += stageTasks.length;
        completedTasks += stageTasks.filter((t: any) => t.completado).length;
      });
    }
  }
  const overallPercent = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
              <Shield className="text-[#007AFF]" /> Principios ENG / SRE & Calidad
            </h2>
            {isFallback && (
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-amber-500/15 text-amber-500 border border-amber-500/20 font-mono flex items-center gap-1">
                <Sparkles size={11} /> MODO FALLBACK (BACKEND API)
              </span>
            )}
          </div>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Monitoreo en tiempo real del ciclo de vida y compuertas de calidad ("production-grade or nothing").
          </p>
        </div>
        
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={runSreVerification}
            disabled={isRefreshing}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#007AFF] hover:bg-[#0062cc] text-white text-xs font-bold transition-all shadow-md shadow-blue-500/20 disabled:opacity-50"
          >
            <Play size={13} className={isRefreshing ? 'animate-spin' : ''} />
            {isRefreshing ? 'Ejecutando...' : 'Ejecutar Verificación SRE'}
          </button>
          
          <button
            onClick={() => setShowHistory(!showHistory)}
            className={`flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold border transition-all ${
              showHistory 
                ? 'bg-slate-800 border-slate-700 text-white' 
                : 'bg-slate-100 dark:bg-white/5 border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-white/10'
            }`}
          >
            <History size={14} />
            Histórico ({history.length})
          </button>

          <button
            onClick={fetchSreData}
            className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-100 dark:bg-white/5 hover:bg-slate-200 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300 text-xs font-semibold transition-colors border border-slate-200 dark:border-white/10"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            Sincronizar
          </button>
        </div>
      </div>

      {/* Histórico Panel */}
      {showHistory && (
        <motion.div 
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="glass-card p-5 border border-slate-700/50 space-y-3"
        >
          <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2">
            <History size={16} className="text-[#007AFF]" /> Registro de Verificaciones de Calidad Pasadas
          </h3>
          {history.length === 0 ? (
            <p className="text-slate-400 text-xs italic">No hay ejecuciones guardadas en el histórico todavía.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-60 overflow-y-auto pr-1">
              {history.map((h, i) => (
                <div key={i} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs flex justify-between items-center">
                  <div className="space-y-1">
                    <span className="font-mono font-bold text-blue-400 block">
                      {h.generated_at ? new Date(h.generated_at).toLocaleString('es-ES') : h.filename}
                    </span>
                    <span className="text-[10.5px] text-slate-400 block">{h.note || 'Verificación SRE'}</span>
                  </div>
                  {h.summary && (
                    <div className="text-right font-mono">
                      <span className="px-2 py-0.5 rounded bg-green-500/10 text-green-400 font-bold block">
                        {h.summary.passed}/{h.summary.total_tests} OK
                      </span>
                      <span className="text-[10px] text-slate-400 block mt-0.5">
                        {h.summary.duration_seconds?.toFixed(1)}s
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center py-20 gap-3">
          <div className="w-8 h-8 border-4 border-[#007AFF] border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-500 text-sm">Cargando métricas de calidad...</p>
        </div>
      )}

      {error && (
        <div className="glass-card p-6 flex flex-col items-center justify-center text-center gap-4 border border-red-500/20">
          <AlertTriangle className="text-red-500" size={44} />
          <div className="max-w-lg space-y-2">
            <h3 className="font-bold text-lg text-red-500">Servidor de Reportes Desconectado</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              No se pudo obtener el reporte de calidad desde <code className="text-[#007AFF] font-mono px-1 py-0.5 bg-slate-800 rounded">{SRE_ENDPOINT}</code>.
            </p>
            
            <div className="text-left bg-slate-950/80 p-3 rounded-xl border border-slate-800 font-mono text-[11px] text-slate-300 space-y-1.5 mt-3">
              <div className="text-amber-400 font-bold flex items-center gap-1.5">
                <span>🔍 Diagnóstico y Solución de Terreno:</span>
              </div>
              <ul className="list-disc list-inside space-y-1 text-slate-400 text-[10.5px]">
                <li><strong>Contenedor Docker:</strong> Levantar el servicio en local: <code className="text-green-400">docker compose -f Datos_localhost/docker-compose.local.yml up -d test-reports</code></li>
                <li><strong>CORS:</strong> Asegurar que <code className="text-blue-400">nginx-reports.conf</code> incluya <code className="text-blue-400">Access-Control-Allow-Origin: *</code></li>
                <li><strong>Archivo de datos:</strong> Confirmar que exista <code className="text-purple-400">Datos_localhost/resultados/progreso_sre.json</code></li>
              </ul>
              {error && (
                <div className="pt-2 text-red-400 border-t border-slate-800/80 text-[10px] break-all">
                  Detalle: {error}
                </div>
              )}
            </div>
          </div>
          <button
            onClick={fetchSreData}
            className="px-5 py-2.5 bg-[#007AFF] hover:bg-[#0062cc] text-white rounded-xl text-xs font-bold transition-all shadow-lg shadow-blue-500/20 flex items-center gap-2"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            Reintentar Conexión
          </button>
        </div>
      )}

      {data && !loading && !error && (
        <>
          {/* Overall Progress Panel */}
          <div className="glass-card p-6 space-y-4">
            <div className="flex justify-between items-center">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                  {isMetadataJson ? 'Tasa de Éxito de Pruebas E2E' : 'Progreso del Pipeline'}
                </span>
                <h3 className="text-3xl font-extrabold mt-1 text-[#007AFF] dark:text-[#3b82f6]">
                  {overallPercent}% <span className="text-sm font-medium text-slate-500 dark:text-slate-400">
                    {isMetadataJson 
                      ? `(${completedTasks} de ${totalTasks} Pruebas E2E aprobadas)` 
                      : `(${completedTasks} de ${totalTasks} Checkpoints aprobados)`
                    }
                  </span>
                </h3>
              </div>
            </div>
            <div className="w-full bg-slate-200 dark:bg-slate-800 h-2.5 rounded-full overflow-hidden">
              <motion.div 
                className="bg-gradient-to-r from-[#007AFF] to-[#00c6ff] h-full rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${overallPercent}%` }}
                transition={{ duration: 0.5, ease: 'easeOut' }}
              />
            </div>
          </div>

          {/* Grid of Stages */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.keys(data).map((stage) => {
              const stageData = data[stage];
              const stageTasks = Array.isArray(data[stage]?.tareas) ? data[stage].tareas : [];
              const completedStage = stageTasks.filter((t: any) => t.completado).length;
              const stagePercent = stageTasks.length > 0 ? Math.round((completedStage / stageTasks.length) * 100) : 0;
              const expl = METRIC_EXPLANATIONS[stage.toLowerCase()];

              return (
                <div key={stage} className="glass-card p-5 flex flex-col gap-4">
                  <div className="flex justify-between items-center">
                    <div className="relative group flex items-center gap-2.5">
                      {getStageIcon(stage)}
                      <h4 className="font-bold text-base text-slate-900 dark:text-white cursor-help border-b border-dashed border-slate-400/40">
                        {stage}
                      </h4>
                      {/* Premium Tooltip */}
                      <div className="absolute left-0 bottom-full mb-2 hidden group-hover:flex flex-col w-72 p-3 bg-slate-950/95 dark:bg-slate-900/95 text-slate-100 text-xs rounded-xl shadow-2xl border border-slate-800/80 dark:border-slate-800 backdrop-blur-lg z-[100] pointer-events-none transition-all duration-200">
                        <div className="font-bold text-[#007AFF] mb-1">
                          {expl?.title || stage}
                        </div>
                        <div className="text-slate-300 dark:text-slate-400 leading-relaxed">
                          {expl?.desc || 'Métrica o etapa de calidad del pipeline.'}
                        </div>
                        {/* Tooltip arrow */}
                        <div className="absolute top-full left-4 w-2 h-2 bg-slate-950 dark:bg-slate-900 border-r border-b border-slate-800/80 dark:border-slate-800 transform rotate-45 -translate-y-1"></div>
                      </div>
                    </div>
                    {stageTasks.length > 0 && (
                      <span className="text-xs font-bold px-2 py-1 rounded bg-[#007AFF]/10 text-[#007AFF]">
                        {stagePercent}%
                      </span>
                    )}
                  </div>
                  
                  <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                    {stageData.descripcion || expl?.desc || 'Mapeo de métricas y compuertas de calidad.'}
                  </p>

                  {stageTasks.length > 0 && (
                    <div className="w-full bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div 
                        className="bg-[#007AFF] h-full rounded-full" 
                        style={{ width: `${stagePercent}%` }}
                      />
                    </div>
                  )}

                  {stageTasks.length > 0 ? (
                    <div className="space-y-2.5 mt-2">
                      {stageTasks.map((task) => (
                        <div 
                          key={task.id} 
                          className={`flex gap-3 p-3 rounded-xl border border-transparent transition-colors ${
                            task.completado 
                              ? 'bg-green-500/5 dark:bg-green-500/5 hover:bg-green-500/10' 
                              : 'bg-amber-500/5 dark:bg-amber-500/5 hover:bg-amber-500/10'
                          }`}
                        >
                          <div className={`mt-0.5 flex-shrink-0`}>
                            {task.completado ? (
                              <CheckCircle2 className="text-[#10b981]" size={16} />
                            ) : (
                              <AlertTriangle className="text-amber-500" size={16} />
                            )}
                          </div>
                          <div className="flex flex-col gap-0.5">
                            <span className={`text-xs font-semibold ${task.completado ? 'text-slate-800 dark:text-slate-200' : 'text-slate-500 dark:text-slate-400'}`}>
                              {task.nombre}
                            </span>
                            <span className="text-[10.5px] text-slate-500 dark:text-slate-400 leading-tight">
                              {task.descripcion}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="mt-1">
                      {renderMetadataValue(stage, stageData)}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
};

export default SreTab;
