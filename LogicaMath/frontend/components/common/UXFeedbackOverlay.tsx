import React, { useState, useEffect, useRef } from 'react';
import html2canvas from 'html2canvas';
import { getStoredToken, getStoredUser } from '../../services/authService';
import { sanitizeHtml } from '../../services/textService';
import './UXFeedbackOverlay.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Helper recursivo para calcular el selector CSS único de un elemento
export function getUniqueSelector(el: HTMLElement): string {
  if (el.getAttribute('data-testid')) {
    return `[data-testid="${el.getAttribute('data-testid')}"]`;
  }
  if (el.getAttribute('data-component')) {
    return `[data-component="${el.getAttribute('data-component')}"]`;
  }
  if (el.id) return `#${el.id}`;
  if (el === document.body) return 'body';

  // Si se cliquea en un tag de texto interno o icono, intentar subir al contenedor semántico de UI
  let target: HTMLElement = el;
  const leafTags = ['span', 'p', 'strong', 'b', 'em', 'code', 'svg', 'path', 'g', 'i', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'label', 'img'];
  
  if (leafTags.includes(target.tagName.toLowerCase()) && target.parentElement && target.parentElement !== document.body) {
    let currentParent: HTMLElement | null = target.parentElement;
    while (currentParent && currentParent !== document.body) {
      if (
        currentParent.getAttribute('data-component') ||
        currentParent.getAttribute('data-testid') ||
        currentParent.id ||
        Array.from(currentParent.classList).some(c => 
          c.startsWith('f1-') || c.startsWith('f2-') || c.startsWith('f3-') || 
          c.startsWith('f4-') || c.startsWith('f5-') || c.startsWith('f6-') || 
          c.startsWith('f7-') || c.startsWith('f8-') || c.startsWith('f9-') || 
          c.includes('modal') || c.includes('card') || c.includes('theory') ||
          c.includes('visualizer') || c.includes('screen') || c.includes('container')
        )
      ) {
        target = currentParent;
        break;
      }
      currentParent = currentParent.parentElement;
    }
  }

  if (target.getAttribute('data-component')) {
    return `[data-component="${target.getAttribute('data-component')}"]`;
  }
  if (target.getAttribute('data-testid')) {
    return `[data-testid="${target.getAttribute('data-testid')}"]`;
  }
  if (target.id) return `#${target.id}`;

  const path: string[] = [];
  let current: HTMLElement | null = target;

  while (current && current !== document.body && current.parentElement) {
    if (current.getAttribute('data-component')) {
      path.unshift(`[data-component="${current.getAttribute('data-component')}"]`);
      break;
    }
    if (current.getAttribute('data-testid')) {
      path.unshift(`[data-testid="${current.getAttribute('data-testid')}"]`);
      break;
    }
    if (current.id) {
      path.unshift(`#${current.id}`);
      break;
    }

    const tagName = current.tagName.toLowerCase();
    const parent = current.parentElement;
    const children = Array.from(parent.children);
    const index = children.indexOf(current) + 1;

    // Clases relevantes ampliadas para el dominio de LógicaKids y UI general
    const classes = Array.from(current.classList)
      .filter(c => 
        c.startsWith('f1-') || 
        c.startsWith('f2-') || 
        c.startsWith('f3-') || 
        c.startsWith('f4-') || 
        c.startsWith('f5-') || 
        c.startsWith('f6-') || 
        c.startsWith('f7-') || 
        c.startsWith('f8-') || 
        c.startsWith('f9-') || 
        c.includes('visualizer') || 
        c.includes('screen') || 
        c.includes('card') || 
        c.includes('btn') || 
        c.includes('button') || 
        c.includes('wrapper') ||
        c.includes('modal') ||
        c.includes('dialog') ||
        c.includes('theory') ||
        c.includes('container') ||
        c.includes('header') ||
        c.includes('box') ||
        c.includes('grid') ||
        c.includes('flex')
      )
      .map(c => `.${c}`)
      .join('');

    let selector = tagName + classes;
    if (children.length > 1 && !classes) {
      selector += `:nth-child(${index})`;
    }

    path.unshift(selector);
    current = parent;
  }

  if (target !== el) {
    const leafTag = el.tagName.toLowerCase();
    const firstClass = el.className && typeof el.className === 'string' && el.className.trim() ? `.${el.className.trim().split(/\s+/)[0]}` : '';
    return `${path.join(' > ')} > ${leafTag}${firstClass}`;
  }

  return path.join(' > ');
}

interface UXFeedbackOverlayProps {
  children: React.ReactNode;
  fase: number;
  moduloId: number;
  nivelId: number;
  preguntaId?: string;
  pasoActual?: number;
  isAdmin?: boolean;
}

export const UXFeedbackOverlay: React.FC<UXFeedbackOverlayProps> = ({
  children,
  fase,
  moduloId,
  nivelId,
  preguntaId = '',
  pasoActual = 1,
  isAdmin: isAdminProp
}) => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [isInspecting, setIsInspecting] = useState(false);
  const [hoveredElement, setHoveredElement] = useState<HTMLElement | null>(null);
  const [highlightStyle, setHighlightStyle] = useState<React.CSSProperties>({});
  
  // Estados del Modal
  const [showModal, setShowModal] = useState(false);
  const [selectedSelector, setSelectedSelector] = useState('');
  const [comentario, setComentario] = useState('');
  const [tipo, setTipo] = useState('bug_visual');
  const [prioridad, setPrioridad] = useState('media');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [alertMsg, setAlertMsg] = useState<{ text: string; type: 'success' | 'error' | 'info' } | null>(null);
  const [selectedElementHtml, setSelectedElementHtml] = useState('');
  const [screenshotUrl, setScreenshotUrl] = useState('');
  const [isUploadingScreenshot, setIsUploadingScreenshot] = useState(false);
  const [isCapturingScreen, setIsCapturingScreen] = useState(false);

  // Verificar rol del usuario al montar o al cambiar la propiedad isAdminProp
  useEffect(() => {
    if (isAdminProp !== undefined) {
      setIsAdmin(isAdminProp);
      return;
    }
    const user = getStoredUser();
    if (user && user.role === 'ADMIN') {
      setIsAdmin(true);
    }
  }, [isAdminProp]);

  // Manejar el efecto visual de hover del inspector
  useEffect(() => {
    if (!isInspecting) {
      setHoveredElement(null);
      return;
    }

    const handleMouseMove = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target || target.closest('.ux-inspector-trigger') || target.closest('.ux-feedback-card')) {
        setHoveredElement(null);
        return;
      }
      setHoveredElement(target);
      
      const rect = target.getBoundingClientRect();
      setHighlightStyle({
        top: `${rect.top + window.scrollY}px`,
        left: `${rect.left + window.scrollX}px`,
        width: `${rect.width}px`,
        height: `${rect.height}px`,
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, [isInspecting]);

  // Intercept clics en fase de captura cuando el inspector está activo
  useEffect(() => {
    if (!isInspecting) return;

    const handleCaptureClick = async (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      // No interceptar clics sobre la UI del inspector flotante
      if (target.closest('.ux-inspector-trigger')) return;

      e.preventDefault();
      e.stopPropagation();

      const selector = getUniqueSelector(target);
      setSelectedSelector(selector);
      setSelectedElementHtml(target.outerHTML);
      setIsInspecting(false);
      setHoveredElement(null);
      setIsCapturingScreen(true);

      try {
        const canvas = await html2canvas(document.body, {
          useCORS: true,
          logging: false,
          scrollX: 0,
          scrollY: 0,
          windowWidth: document.documentElement.clientWidth,
          windowHeight: document.documentElement.clientHeight,
          ignoreElements: (el) => 
            el.classList.contains('ux-inspector-trigger') || 
            el.classList.contains('ux-hover-highlight') ||
            el.classList.contains('ux-feedback-modal-overlay')
        });

        canvas.toBlob(async (blob) => {
          if (blob) {
            const file = new File([blob], `auto-screenshot-${Date.now()}.png`, { type: 'image/png' });
            await handleUploadImage(file);
          }
          setIsCapturingScreen(false);
          setShowModal(true);
        }, 'image/png');
      } catch (err) {
        console.error('Error en captura html2canvas:', err);
        setIsCapturingScreen(false);
        setShowModal(true);
      }
    };

    window.addEventListener('click', handleCaptureClick, true);
    return () => {
      window.removeEventListener('click', handleCaptureClick, true);
    };
  }, [isInspecting]);

  const handleUploadImage = async (file: File) => {
    if (!file) return;
    setIsUploadingScreenshot(true);
    const token = getStoredToken();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/evaluador/feedback/upload-screenshot`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Error al subir la captura de pantalla.');
      }

      const data = await response.json();
      // Si la URL devuelta es local, asegurarnos de que use la URL absoluta del Backend API
      let finalUrl = data.url;
      if (finalUrl.startsWith('/')) {
        finalUrl = `${API_URL}${finalUrl}`;
      }
      setScreenshotUrl(finalUrl);
    } catch (err: any) {
      alert(`Error al subir imagen: ${err.message}`);
    } finally {
      setIsUploadingScreenshot(false);
    }
  };

  useEffect(() => {
    if (!showModal) return;

    const handlePaste = (e: ClipboardEvent) => {
      const items = e.clipboardData?.items;
      if (!items) return;

      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const blob = items[i].getAsFile();
          if (blob) {
            const file = new File([blob], 'screenshot.png', { type: blob.type });
            handleUploadImage(file);
            e.preventDefault();
            break;
          }
        }
      }
    };

    window.addEventListener('paste', handlePaste);
    return () => {
      window.removeEventListener('paste', handlePaste);
    };
  }, [showModal]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!comentario.trim()) return;

    setIsSubmitting(true);
    const token = getStoredToken();

    const currentUser = getStoredUser();

    const payload = {
      fase,
      modulo_id: moduloId,
      nivel_id: nivelId,
      pregunta_id: preguntaId,
      paso_actual: pasoActual,
      dom_selector: selectedSelector,
      viewport: `${window.innerWidth}x${window.innerHeight}`,
      comentario: comentario.trim(),
      tipo,
      prioridad,
      screenshot_url: screenshotUrl || null,
      app_state: {
        timestamp: new Date().toISOString(),
        url: window.location.pathname,
        element_html: selectedElementHtml || null,
        fase,
        moduloId,
        nivelId,
        preguntaId,
        pasoActual,
        user: currentUser ? { username: currentUser.username, role: currentUser.role } : null,
        global_state: (window as any).__GAME_STATE__ || null
      }
    };

    try {
      const response = await fetch(`${API_URL}/evaluador/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('Error al registrar feedback en backend.');
      }

      setAlertMsg({ text: '💡 ¡Feedback guardado con éxito!', type: 'success' });
      setComentario('');
      setScreenshotUrl('');
      setSelectedElementHtml('');
      setShowModal(false);
      
      // Auto ocultar alerta tras 3 segundos
      setTimeout(() => setAlertMsg(null), 3500);
    } catch (err: any) {
      setAlertMsg({ text: `❌ Fallo al guardar: ${err.message || err}`, type: 'error' });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isAdmin) {
    return <>{children}</>;
  }

  return (
    <div className={isInspecting ? 'ux-inspector-active' : ''}>
      {children}
      
      {/* Caja de resaltado hover */}
      {isInspecting && hoveredElement && (
        <div className="ux-hover-highlight" style={highlightStyle} />
      )}

      {/* Indicator de Captura de Pantalla en curso */}
      {isCapturingScreen && (
        <div 
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.7)',
            color: '#fff',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 100002,
            gap: '12px',
            backdropFilter: 'blur(4px)'
          }}
        >
          <div style={{ fontSize: '2rem', animation: 'pulse 1s infinite' }}>📸</div>
          <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>Generando captura de pantalla automática...</div>
          <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Por favor espera un segundo</div>
        </div>
      )}

      {/* Alerta flotante */}
      {alertMsg && (
        <div 
          style={{
            position: 'fixed',
            top: '24px',
            right: '24px',
            background: alertMsg.type === 'success' ? '#10b981' : '#ef4444',
            color: '#fff',
            padding: '16px 24px',
            borderRadius: '16px',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.3)',
            zIndex: 100001,
            fontWeight: 800,
            animation: 'slideUp 0.3s ease-out'
          }}
        >
          {alertMsg.text}
        </div>
      )}

      {/* Botón flotante de activación del inspector */}
      <button 
        className={`ux-inspector-trigger ${isInspecting ? 'active' : ''}`}
        title={isInspecting ? 'Cancelar inspección' : 'Reportar Feedback UX (Modo Evaluador)'}
        onClick={() => setIsInspecting(!isInspecting)}
      >
        {isInspecting ? (
          <span style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>×</span>
        ) : (
          <span style={{ fontSize: '1.3rem' }}>💬</span>
        )}
      </button>

      {/* Modal de Feedback */}
      {showModal && (
        <div className="ux-feedback-modal-overlay">
          <div className="ux-feedback-card">
            <div className="ux-feedback-header">
              <span className="ux-feedback-icon">🛠️</span>
              <div>
                <h3 className="ux-feedback-title">Anotación de Mejoría UX</h3>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                  Fase {fase} • Módulo {moduloId} • Nivel {nivelId}
                </span>
              </div>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="ux-feedback-field">
                <label className="ux-feedback-label">Elemento DOM Seleccionado</label>
                <div className="ux-feedback-meta-badge">{selectedSelector}</div>
              </div>

              {selectedElementHtml && (
                <div className="ux-feedback-field">
                  <label className="ux-feedback-label">Elemento Seleccionado (Visual)</label>
                  <div 
                    className="ux-element-html-preview"
                    style={{
                      maxHeight: '150px',
                      overflow: 'auto',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                      borderRadius: '8px',
                      padding: '12px',
                      background: 'rgba(255, 255, 255, 0.05)',
                      pointerEvents: 'none',
                      userSelect: 'none'
                    }}
                    dangerouslySetInnerHTML={{ __html: sanitizeHtml(selectedElementHtml) }}
                  />
                </div>
              )}

              <div className="ux-feedback-field">
                <label className="ux-feedback-label" htmlFor="feedback-tipo">Tipo de Reporte</label>
                <select 
                  id="feedback-tipo"
                  className="ux-feedback-select"
                  value={tipo}
                  onChange={(e) => setTipo(e.target.value)}
                >
                  <option value="bug_visual">Bug Visual / Desalineación</option>
                  <option value="texto">Sugerencia de Texto / Copy</option>
                  <option value="propuesta_ux">Propuesta de UX / Animación</option>
                  <option value="rendimiento">Problema de Rendimiento</option>
                </select>
              </div>

              <div className="ux-feedback-field">
                <label className="ux-feedback-label" htmlFor="feedback-prioridad">Prioridad</label>
                <select 
                  id="feedback-prioridad"
                  className="ux-feedback-select"
                  value={prioridad}
                  onChange={(e) => setPrioridad(e.target.value)}
                >
                  <option value="baja">Baja</option>
                  <option value="media">Media</option>
                  <option value="alta">Alta</option>
                  <option value="critica">Crítica</option>
                </select>
              </div>

              <div className="ux-feedback-field">
                <label className="ux-feedback-label" htmlFor="feedback-comentario">Comentario del Evaluador</label>
                <textarea
                  id="feedback-comentario"
                  className="ux-feedback-textarea"
                  placeholder="Describe detalladamente el problema visual o la mejoría de UX sugerida..."
                  value={comentario}
                  onChange={(e) => setComentario(e.target.value)}
                  required
                />
              </div>

              <div className="ux-feedback-field">
                <label className="ux-feedback-label">Captura de Pantalla (Opcional)</label>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {screenshotUrl ? (
                    <div style={{ position: 'relative', width: 'fit-content' }}>
                      <img 
                        src={screenshotUrl} 
                        alt="Screenshot" 
                        style={{ maxWidth: '100%', maxHeight: '120px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }} 
                      />
                      <button
                        type="button"
                        onClick={() => setScreenshotUrl('')}
                        style={{
                          position: 'absolute',
                          top: '-6px',
                          right: '-6px',
                          background: '#ef4444',
                          color: '#fff',
                          border: 'none',
                          borderRadius: '50%',
                          width: '20px',
                          height: '20px',
                          fontSize: '12px',
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontWeight: 'bold',
                          boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
                        }}
                        title="Quitar imagen"
                      >
                        ×
                      </button>
                    </div>
                  ) : (
                    <div 
                      style={{
                        border: '1px dashed rgba(255,255,255,0.2)',
                        borderRadius: '12px',
                        padding: '16px',
                        textAlign: 'center',
                        background: 'rgba(255,255,255,0.02)',
                        cursor: 'pointer',
                        transition: 'border-color 0.2s',
                      }}
                      onClick={() => document.getElementById('feedback-screenshot-file')?.click()}
                    >
                      <span style={{ fontSize: '1.2rem', display: 'block', marginBottom: '4px' }}>📸</span>
                      <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                        {isUploadingScreenshot ? 'Subiendo imagen...' : 'Selecciona una imagen o pega directamente con Ctrl+V'}
                      </span>
                      <input 
                        type="file" 
                        id="feedback-screenshot-file" 
                        accept="image/*" 
                        style={{ display: 'none' }} 
                        onChange={(e) => {
                          const file = e.target.files?.[0];
                          if (file) handleUploadImage(file);
                        }}
                      />
                    </div>
                  )}
                </div>
              </div>

              <div className="ux-feedback-actions">
                <button 
                  type="button" 
                  className="ux-feedback-btn ux-feedback-btn-cancel"
                  onClick={() => {
                    setShowModal(false);
                    setComentario('');
                  }}
                  disabled={isSubmitting}
                >
                  Cancelar
                </button>
                <button 
                  type="submit" 
                  className="ux-feedback-btn ux-feedback-btn-submit"
                  disabled={isSubmitting || !comentario.trim()}
                >
                  {isSubmitting ? 'Guardando...' : 'Enviar Reporte →'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
