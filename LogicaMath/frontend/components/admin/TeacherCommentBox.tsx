import React, { useState } from 'react';
import { MessageSquare, Send, Loader2 } from 'lucide-react';
import { saveTeacherFeedback } from '../../services/storageService';

interface TeacherCommentBoxProps {
  faseId: number;
  seccionId: number;
  preguntaId?: number | null;
  tipo: 'pregunta' | 'teoria' | 'interactivo';
  showToast: (message: string, type: 'success' | 'error') => void;
}

export const TeacherCommentBox: React.FC<TeacherCommentBoxProps> = ({
  faseId,
  seccionId,
  preguntaId = null,
  tipo,
  showToast
}) => {
  const [comentario, setComentario] = useState('');
  const [sending, setSending] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!comentario.trim()) {
      showToast('Por favor, escribe un comentario antes de enviar.', 'error');
      return;
    }

    setSending(true);
    try {
      await saveTeacherFeedback({
        fase_id: faseId,
        seccion_id: seccionId,
        pregunta_id: preguntaId,
        tipo,
        comentario: comentario.trim()
      });
      showToast('¡Comentario de retroalimentación guardado con éxito!', 'success');
      setComentario('');
    } catch (error: any) {
      console.error(error);
      showToast(error.message || 'Error al guardar el comentario.', 'error');
    } finally {
      setSending(false);
    }
  };

  const getTipoLabel = () => {
    switch (tipo) {
      case 'pregunta': return 'esta Pregunta';
      case 'teoria': return 'esta Sección Teórica';
      case 'interactivo': return 'este Ejercicio Interactivo';
      default: return 'este Contenido';
    }
  };

  return (
    <div className="w-full bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-4 flex flex-col gap-3 shadow-xl">
      <div className="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-wider">
        <MessageSquare size={14} className="text-purple-400" />
        <span>Comentarios y Ajustes del Docente</span>
      </div>
      
      <p className="text-[11px] text-slate-500 leading-relaxed font-medium">
        ¿Notas algún error o tienes sugerencias para <strong>{getTipoLabel()}</strong>? Escríbelo abajo. Un proceso automático de IA revisará este comentario para realizar las correcciones y actualizar las imágenes si es necesario.
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <textarea
          rows={3}
          value={comentario}
          onChange={(e) => setComentario(e.target.value)}
          placeholder={`Escribe aquí tus comentarios sobre ${getTipoLabel()}... (ej. "La figura del reloj no tiene las manecillas correctas", "Reescribir el enunciado para usar 1/2 en vez de 2/4")`}
          className="w-full bg-slate-950/40 border border-white/5 rounded-xl p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500/50 resize-none font-medium"
          disabled={sending}
        />
        <button
          type="submit"
          disabled={sending || !comentario.trim()}
          className="self-end px-4 py-2 bg-purple-600 hover:bg-purple-500 disabled:opacity-40 disabled:hover:bg-purple-600 text-[11px] font-black text-white rounded-lg flex items-center gap-1.5 active:scale-95 transition-all cursor-pointer shadow-md shadow-purple-900/20"
        >
          {sending ? (
            <>
              <Loader2 size={12} className="animate-spin" />
              Guardando...
            </>
          ) : (
            <>
              <Send size={12} />
              Enviar Retroalimentación
            </>
          )}
        </button>
      </form>
    </div>
  );
};
