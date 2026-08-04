import React, { useState, useEffect, useRef } from 'react';
import { getStoredToken } from '../../services/authService';
import { ShieldAlert, CheckCircle, Clock, Trash2, Filter, Code } from 'lucide-react';
import { sanitizeHtml } from '../../services/textService';
import AuthenticatedImage from '../common/AuthenticatedImage';

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/api$/, '');

interface ShadowDOMWrapperProps {
  html: string;
  className?: string;
  style?: React.CSSProperties;
}

const ShadowDOMWrapper: React.FC<ShadowDOMWrapperProps> = ({ html, className, style }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const shadowRootRef = useRef<ShadowRoot | null>(null);

  useEffect(() => {
    if (containerRef.current) {
      if (!shadowRootRef.current) {
        shadowRootRef.current = containerRef.current.attachShadow({ mode: 'open' });
      }
      
      const styleEl = document.createElement('style');
      styleEl.textContent = `
        :host { 
          display: block; 
          max-height: 180px; 
          overflow: auto; 
          width: 100%;
          background: rgba(15, 23, 42, 0.6);
          border-radius: 12px;
          padding: 12px;
          box-sizing: border-box;
        }
        * { 
          box-sizing: border-box; 
          max-width: 100%; 
        }
        body, div, p, span, h1, h2, h3, button { 
          color: #e2e8f0; 
          font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          font-size: 13px; 
          line-height: 1.4;
        }
        img, svg, canvas { 
          max-width: 100% !important; 
          height: auto !important; 
          object-fit: contain; 
        }
        .border-dashed { 
          border-style: dashed !important; 
          border-width: 1.5px !important; 
        }
      `;
      
      shadowRootRef.current.innerHTML = '';
      shadowRootRef.current.appendChild(styleEl);

      const wrapper = document.createElement('div');
      wrapper.style.maxWidth = '100%';
      wrapper.innerHTML = html;
      shadowRootRef.current.appendChild(wrapper);
    }
  }, [html]);

  return <div ref={containerRef} className={className} style={style} />;
};

interface UXFeedback {
  id: number;
  fase: number;
  modulo_id: number;
  nivel_id: number;
  pregunta_id?: string;
  paso_actual?: number;
  dom_selector: string;
  viewport?: string;
  comentario: string;
  tipo: 'bug_visual' | 'texto' | 'propuesta_ux' | 'rendimiento';
  prioridad: 'baja' | 'media' | 'alta' | 'critica';
  estado: 'pendiente' | 'en_desarrollo' | 'resuelto' | 'rechazado';
  desarrollador_notes?: string;
  screenshot_url?: string;
  app_state?: any;
  imagenes?: {url: string; rol: 'actual' | 'referencia'}[];
  fecha_creacion: string;
}

export const UXFeedbackTab: React.FC = () => {
  const [feedbacks, setFeedbacks] = useState<UXFeedback[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filtros
  const [faseFiltro, setFaseFiltro] = useState<string>('');
  const [prioridadFiltro, setPrioridadFiltro] = useState<string>('');
  const [estadoFiltro, setEstadoFiltro] = useState<string>('pendiente');

  // Detalle seleccionado para modal
  const [selectedFeedback, setSelectedFeedback] = useState<UXFeedback | null>(null);
  const [devNotes, setDevNotes] = useState('');
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [copiedSelector, setCopiedSelector] = useState(false);
  const [copiedCmd, setCopiedCmd] = useState(false);

  const fetchFeedbacks = async () => {
    setIsLoading(true);
    setError(null);
    const token = getStoredToken();

    let url = `${API_URL}/evaluador/feedback?`;
    if (faseFiltro) url += `fase=${faseFiltro}&`;
    if (prioridadFiltro) url += `prioridad=${prioridadFiltro}&`;
    if (estadoFiltro) url += `estado=${estadoFiltro}&`;

    try {
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) {
        throw new Error('Error al obtener la lista de feedbacks.');
      }
      const data = await response.json();
      setFeedbacks(data);
    } catch (err: any) {
      setError(err.message || 'Error de conexión');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFeedbacks();
  }, [faseFiltro, prioridadFiltro, estadoFiltro]);

  const handleUpdateStatus = async (id: number, newStatus: string, notes: string) => {
    setUpdatingId(id);
    const token = getStoredToken();

    try {
      const response = await fetch(`${API_URL}/evaluador/feedback/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          estado: newStatus,
          desarrollador_notes: notes.trim()
        })
      });

      if (!response.ok) {
        throw new Error('Error al actualizar el estado del feedback.');
      }

      // Actualizar estado local
      setFeedbacks(prev => 
        prev.map(f => f.id === id ? { ...f, estado: newStatus as any, desarrollador_notes: notes } : f)
      );
      
      if (selectedFeedback && selectedFeedback.id === id) {
        setSelectedFeedback(prev => prev ? { ...prev, estado: newStatus as any, desarrollador_notes: notes } : null);
      }
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setUpdatingId(null);
    }
  };

  const handleDeleteFeedback = async (id: number) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar este reporte de UX de la base de datos?')) return;
    setUpdatingId(id);
    const token = getStoredToken();
    try {
      const response = await fetch(`${API_URL}/evaluador/feedback/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Error al eliminar el reporte.');

      setFeedbacks(prev => prev.filter(f => f.id !== id));
      if (selectedFeedback && selectedFeedback.id === id) {
        setSelectedFeedback(null);
      }
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setUpdatingId(null);
    }
  };

  const getPriorityColor = (p: string) => {
    switch (p) {
      case 'critica': return 'bg-red-500/10 text-red-500 border border-red-500/20';
      case 'alta': return 'bg-orange-500/10 text-orange-500 border border-orange-500/20';
      case 'media': return 'bg-amber-500/10 text-amber-500 border border-amber-500/20';
      default: return 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20';
    }
  };

  const getStatusBadge = (s: string) => {
    switch (s) {
      case 'resuelto': 
        return <span className="flex items-center gap-1.5 text-xs text-emerald-500 bg-emerald-500/10 px-2.5 py-1 rounded-full"><CheckCircle size={12} /> Resuelto</span>;
      case 'en_desarrollo':
        return <span className="flex items-center gap-1.5 text-xs text-blue-400 bg-blue-500/10 px-2.5 py-1 rounded-full"><Clock size={12} /> En Desarrollo</span>;
      case 'rechazado':
        return <span className="flex items-center gap-1.5 text-xs text-slate-400 bg-slate-500/10 px-2.5 py-1 rounded-full">Rechazado</span>;
      default:
        return <span className="flex items-center gap-1.5 text-xs text-amber-400 bg-amber-500/10 px-2.5 py-1 rounded-full"><ShieldAlert size={12} /> Pendiente</span>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white/5 border border-white/5 rounded-2xl p-6 backdrop-blur-xl">
        <div>
          <h2 className="text-xl font-bold text-white">Buzón de Mejorías UX & QA</h2>
          <p className="text-slate-400 text-xs mt-1">Revisa y gestiona las anotaciones visuales y de UX reportadas por el equipo revisor en caliente.</p>
        </div>

        {/* Controles de Filtros */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-300">
            <Filter size={13} className="text-slate-400" />
            <span>Fase:</span>
            <select 
              value={faseFiltro} 
              onChange={(e) => setFaseFiltro(e.target.value)}
              className="bg-transparent border-none text-white outline-none cursor-pointer"
            >
              <option value="" style={{ background: '#1c1d24' }}>Todas</option>
              {[1,2,3,4,5,6,7,8,9].map(f => (
                <option key={f} value={f} style={{ background: '#1c1d24' }}>Fase {f}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-300">
            <span>Prioridad:</span>
            <select 
              value={prioridadFiltro} 
              onChange={(e) => setPrioridadFiltro(e.target.value)}
              className="bg-transparent border-none text-white outline-none cursor-pointer"
            >
              <option value="" style={{ background: '#1c1d24' }}>Todas</option>
              <option value="baja" style={{ background: '#1c1d24' }}>Baja</option>
              <option value="media" style={{ background: '#1c1d24' }}>Media</option>
              <option value="alta" style={{ background: '#1c1d24' }}>Alta</option>
              <option value="critica" style={{ background: '#1c1d24' }}>Crítica</option>
            </select>
          </div>

          <div className="flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-300">
            <span>Estado:</span>
            <select 
              value={estadoFiltro} 
              onChange={(e) => setEstadoFiltro(e.target.value)}
              className="bg-transparent border-none text-white outline-none cursor-pointer"
            >
              <option value="" style={{ background: '#1c1d24' }}>Todos</option>
              <option value="pendiente" style={{ background: '#1c1d24' }}>Pendientes</option>
              <option value="en_desarrollo" style={{ background: '#1c1d24' }}>En Desarrollo</option>
              <option value="resuelto" style={{ background: '#1c1d24' }}>Resueltos</option>
              <option value="rechazado" style={{ background: '#1c1d24' }}>Rechazados</option>
            </select>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-4 rounded-xl text-sm">
          ❌ Error al cargar los feedbacks: {error}
        </div>
      )}

      {isLoading ? (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
        </div>
      ) : feedbacks.length === 0 ? (
        <div className="text-center py-16 bg-white/5 border border-white/5 rounded-2xl">
          <p className="text-slate-400 text-sm">No se encontraron anotaciones de UX con los filtros seleccionados.</p>
        </div>
      ) : (
        <div className="bg-white/5 border border-white/5 rounded-2xl overflow-hidden backdrop-blur-xl">
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left">
              <thead>
                <tr className="border-b border-white/5 text-[11px] font-bold text-slate-400 uppercase tracking-wider bg-white/5">
                  <th className="p-4 pl-6">ID</th>
                  <th className="p-4">Prioridad / Tipo</th>
                  <th className="p-4">Contexto de Pantalla</th>
                  <th className="p-4">Comentario del Revisor</th>
                  <th className="p-4">Selector DOM Clicado</th>
                  <th className="p-4">Estado</th>
                  <th className="p-4 pr-6 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-[13px] text-slate-300">
                {feedbacks.map(f => (
                  <tr key={f.id} className="hover:bg-white/2 transition-colors">
                    <td className="p-4 pl-6 font-mono text-slate-500">#{f.id}</td>
                    <td className="p-4">
                      <div className="flex flex-col gap-1.5">
                        <span className={`text-[10px] px-2 py-0.5 rounded-md font-extrabold uppercase w-fit ${getPriorityColor(f.prioridad)}`}>
                          {f.prioridad}
                        </span>
                        <span className="text-[11px] text-slate-400">
                          {f.tipo === 'bug_visual' ? '🎨 Bug Visual' : f.tipo === 'texto' ? '📝 Copy/Texto' : f.tipo === 'rendimiento' ? '⚡ Rendimiento' : '💡 Propuesta UX'}
                        </span>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="font-medium text-white">Fase {f.fase}</div>
                      <div className="text-[11px] text-slate-400">Módulo {f.modulo_id} • Nivel {f.nivel_id} {f.paso_actual ? `• Paso ${f.paso_actual}` : ''}</div>
                    </td>
                    <td className="p-4 max-w-xs truncate" title={f.comentario}>
                      {f.comentario}
                    </td>
                    <td className="p-4 max-w-xs font-mono text-[11px] text-slate-400 truncate" title={f.dom_selector}>
                      {f.dom_selector}
                    </td>
                    <td className="p-4">{getStatusBadge(f.estado)}</td>
                    <td className="p-4 pr-6 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button 
                          onClick={() => {
                            setSelectedFeedback(f);
                            setDevNotes(f.desarrollador_notes || '');
                          }}
                          className="px-3.5 py-1.5 rounded-lg bg-purple-600/20 text-purple-400 hover:bg-purple-600 hover:text-white transition-colors font-bold text-xs"
                        >
                          Ver Detalle
                        </button>
                        <button 
                          onClick={() => handleDeleteFeedback(f.id)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                          title="Eliminar Reporte"
                        >
                          <Trash2 size={15} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Modal Detalle de Feedback */}
      {selectedFeedback && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex justify-center items-center p-4 z-[100] animate-fadeIn">
          <div className="bg-slate-900 border border-white/10 rounded-3xl w-full max-w-xl p-8 text-slate-200 shadow-2xl animate-slideUp">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="text-lg font-bold text-white">Detalle de Feedback #{selectedFeedback.id}</h3>
                <p className="text-slate-400 text-xs mt-1">Registrado el {new Date(selectedFeedback.fecha_creacion).toLocaleString()}</p>
              </div>
              <button 
                onClick={() => setSelectedFeedback(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-white/5 transition-colors"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/2 p-3.5 border border-white/5 rounded-2xl">
                  <div className="text-[10px] text-slate-400 uppercase font-bold">Ubicación del Bug</div>
                  <div className="text-[13px] text-white mt-1 font-semibold">
                    Fase {selectedFeedback.fase} • M{selectedFeedback.modulo_id} • N{selectedFeedback.nivel_id}
                  </div>
                </div>
                <div className="bg-white/2 p-3.5 border border-white/5 rounded-2xl">
                  <div className="text-[10px] text-slate-400 uppercase font-bold">Tipo y Prioridad</div>
                  <div className="text-[13px] text-white mt-1 font-semibold uppercase">
                    {selectedFeedback.prioridad} • {selectedFeedback.tipo.replace('_', ' ')}
                  </div>
                </div>
              </div>

              <div>
                <div className="text-[10px] text-slate-400 uppercase font-bold mb-1">Comentario del QA</div>
                <div className="bg-white/5 border border-white/5 p-4 rounded-xl text-[13px] leading-relaxed text-white whitespace-pre-wrap">
                  "{selectedFeedback.comentario}"
                </div>
              </div>

              {(selectedFeedback.imagenes && selectedFeedback.imagenes.length > 0) ? (
                <div>
                  <div className="text-[10px] text-slate-400 uppercase font-bold mb-2">Imágenes Adjuntas</div>
                  <div className="grid grid-cols-2 gap-4">
                    {selectedFeedback.imagenes.map((img, idx) => (
                      <div key={idx} className="bg-white/5 border border-white/5 p-2 rounded-xl flex flex-col items-center">
                        <span className="text-[10px] text-slate-400 uppercase font-bold mb-2">{img.rol === 'actual' ? 'Estado Actual' : 'Referencia / Deseado'}</span>
                        <AuthenticatedImage 
                          src={img.url} 
                          alt={img.rol} 
                          className="max-h-64 object-contain rounded-lg border border-white/10 cursor-zoom-in w-full"
                          onClick={() => window.open(img.url, '_blank')}
                          title="Ver en pantalla completa"
                        />
                      </div>
                    ))}
                  </div>
                </div>
              ) : selectedFeedback.screenshot_url ? (
                <div>
                  <div className="text-[10px] text-slate-400 uppercase font-bold mb-1">Captura de Pantalla</div>
                  <div className="bg-white/5 border border-white/5 p-2 rounded-xl flex justify-center">
                    <AuthenticatedImage 
                      src={selectedFeedback.screenshot_url} 
                      alt="Captura de reporte" 
                      className="max-h-64 object-contain rounded-lg border border-white/10 cursor-zoom-in"
                      onClick={() => window.open(selectedFeedback.screenshot_url, '_blank')}
                      title="Ver en pantalla completa"
                    />
                  </div>
                </div>
              ) : null}

              {selectedFeedback.app_state?.element_html && (
                <div>
                  <div className="text-[10px] text-slate-400 uppercase font-bold mb-1">Elemento Seleccionado (Visual - Shadow DOM)</div>
                  <ShadowDOMWrapper 
                    html={selectedFeedback.app_state.element_html}
                    className="bg-white/5 border border-white/5 p-4 rounded-xl max-h-48 overflow-auto pointer-events-none select-none"
                    style={{ background: 'rgba(255,255,255,0.03)' }}
                  />
                </div>
              )}

              <div>
                <div className="text-[10px] text-slate-400 uppercase font-bold mb-1">Selector DOM (Código)</div>
                <div 
                  onClick={() => {
                    navigator.clipboard.writeText(selectedFeedback.dom_selector);
                    setCopiedSelector(true);
                    setTimeout(() => setCopiedSelector(false), 2000);
                  }}
                  className="bg-white/5 border border-white/5 p-3 rounded-xl font-mono text-[11px] text-purple-300 break-all select-all flex items-center justify-between cursor-pointer hover:bg-white/10 transition-colors"
                  title="Clic para copiar selector"
                >
                  <span>{selectedFeedback.dom_selector}</span>
                  <span className="text-[9px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-sans uppercase font-extrabold flex-shrink-0 ml-2">
                    {copiedSelector ? '✓ Copiado' : 'Copiar'}
                  </span>
                </div>
              </div>

              {/* Comando de Resolución de Antigravity */}
              <div>
                <div className="text-[10px] text-blue-400 uppercase font-bold mb-1">Comando Automático Antigravity</div>
                <div 
                  onClick={() => {
                    const cmd = `/opsx-apply resolver feedback UX #${selectedFeedback.id} usando docs/ux_feedback/${selectedFeedback.id}/instruccion.md`;
                    navigator.clipboard.writeText(cmd);
                    setCopiedCmd(true);
                    setTimeout(() => setCopiedCmd(false), 2000);
                  }}
                  className="bg-blue-950/40 border border-blue-900/30 p-3 rounded-xl font-mono text-[11px] text-blue-300 break-all select-all flex items-center justify-between cursor-pointer hover:bg-blue-900/40 transition-colors"
                  title="Clic para copiar comando"
                >
                  <span>/opsx-apply resolver feedback UX #{selectedFeedback.id} usando docs/ux_feedback/{selectedFeedback.id}/instruccion.md</span>
                  <span className="text-[9px] bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded font-sans uppercase font-extrabold flex-shrink-0 ml-2">
                    {copiedCmd ? '✓ Copiado' : 'Copiar'}
                  </span>
                </div>
              </div>

              {/* Actualizar Estado */}
              <div className="border-t border-white/5 pt-4 space-y-3">
                <div className="flex flex-col gap-1.5">
                  <label className="text-[10px] text-slate-400 uppercase font-bold" htmlFor="dev-notes">Notas de Resolución del Desarrollador</label>
                  <textarea
                    id="dev-notes"
                    className="bg-white/5 border border-white/10 rounded-xl p-3 text-[13px] text-white outline-none focus:border-purple-500 resize-none min-h-[75px]"
                    placeholder="Escribe detalles del cambio realizado para resolver este reporte de UX..."
                    value={devNotes}
                    onChange={(e) => setDevNotes(e.target.value)}
                  />
                </div>

                <div className="flex items-center justify-between gap-4 pt-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] text-slate-400">Marcar como:</span>
                    <div className="flex gap-1.5">
                      <button
                        onClick={() => handleUpdateStatus(selectedFeedback.id, 'en_desarrollo', devNotes)}
                        disabled={updatingId !== null}
                        className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${selectedFeedback.estado === 'en_desarrollo' ? 'bg-blue-600 text-white' : 'bg-white/5 text-slate-300 hover:bg-white/10'}`}
                      >
                        En Desarrollo
                      </button>
                      <button
                        onClick={() => handleUpdateStatus(selectedFeedback.id, 'resuelto', devNotes)}
                        disabled={updatingId !== null}
                        className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${selectedFeedback.estado === 'resuelto' ? 'bg-emerald-600 text-white' : 'bg-white/5 text-slate-300 hover:bg-white/10'}`}
                      >
                        Resuelto ✓
                      </button>
                      <button
                        onClick={() => handleUpdateStatus(selectedFeedback.id, 'rechazado', devNotes)}
                        disabled={updatingId !== null}
                        className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${selectedFeedback.estado === 'rechazado' ? 'bg-slate-700 text-white' : 'bg-white/5 text-slate-300 hover:bg-white/10'}`}
                      >
                        Rechazar
                      </button>
                    </div>
                  </div>

                  <button
                    onClick={() => setSelectedFeedback(null)}
                    className="px-4 py-1.5 rounded-lg bg-white/10 hover:bg-white/15 text-white font-bold text-xs transition-colors"
                  >
                    Cerrar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
