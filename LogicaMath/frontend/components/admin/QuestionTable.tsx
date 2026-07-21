import React from 'react';
import { 
  Plus, Trash2, Edit, BookOpen, Search, 
  ChevronLeft, ChevronRight, Settings
} from 'lucide-react';

interface QuestionTableProps {
  questions: any[];
  loadingQuestions: boolean;
  onOpenAddModal: () => void;
  onOpenEditModal: (q: any) => void;
  onDeleteQuestion: (id: number) => void;
  questionsPerPage: number;
  setQuestionsPerPage: (n: number) => void;
  currentPage: number;
  setCurrentPage: (n: number) => void;
  searchQuery: string;
  setSearchQuery: (s: string) => void;
}

export const QuestionTable: React.FC<QuestionTableProps> = ({
  questions,
  loadingQuestions,
  onOpenAddModal,
  onOpenEditModal,
  onDeleteQuestion,
  questionsPerPage,
  setQuestionsPerPage,
  currentPage,
  setCurrentPage,
  searchQuery,
  setSearchQuery
}) => {
  // Filter questions by search query
  const filteredQuestions = questions.filter(q => 
    q.enunciado.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Pagination calculations
  const totalPages = Math.ceil(filteredQuestions.length / questionsPerPage);
  const indexOfLastQuestion = currentPage * questionsPerPage;
  const indexOfFirstQuestion = indexOfLastQuestion - questionsPerPage;
  const paginatedQuestions = filteredQuestions.slice(indexOfFirstQuestion, indexOfLastQuestion);

  return (
    <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 rounded-[2.2rem] shadow-2xl p-6 flex flex-col gap-5">
      <div className="flex flex-col md:flex-row justify-between md:items-center gap-4 border-b border-slate-200 dark:border-white/5 pb-4">
        <h4 className="text-base font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest flex items-center gap-2">
          <Settings size={16} className="text-blue-400" /> Banco de Preguntas del Nivel
        </h4>
        
        <button
          onClick={onOpenAddModal}
          className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-sm font-black flex items-center gap-1.5 shadow-md shadow-blue-900/10 active:scale-95 transition-all cursor-pointer"
        >
          <Plus size={14} />
          Agregar Pregunta
        </button>
      </div>

      {/* Filter and Pagination controls bar */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 bg-white/80 dark:bg-slate-950/40 p-4 rounded-2xl border border-slate-200 dark:border-white/5">
        {/* Search input */}
        <div className="relative w-full sm:w-80">
          <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Buscar pregunta por enunciado..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setCurrentPage(1);
            }}
            className="w-full bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl py-2.5 pl-10 pr-4 text-xs font-bold placeholder-slate-500 text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50 transition-colors"
          />
        </div>

        {/* Questions per page dropdown */}
        <div className="flex items-center gap-2 self-end sm:self-center">
          <label className="text-xs font-bold text-slate-500 dark:text-slate-400">Mostrar:</label>
          <select
            value={questionsPerPage}
            onChange={(e) => {
              setQuestionsPerPage(parseInt(e.target.value));
              setCurrentPage(1);
            }}
            className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl px-3 py-2 text-xs font-bold text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50 cursor-pointer"
          >
            <option value={10}>10 preguntas</option>
            <option value={20}>20 preguntas</option>
            <option value={50}>50 preguntas</option>
          </select>
        </div>
      </div>

      {loadingQuestions ? (
        <div className="w-full flex flex-col gap-4 animate-pulse">
          <div className="flex items-center gap-4 border-b border-slate-200 dark:border-white/10 pb-4">
            <div className="h-4 bg-slate-200 dark:bg-white/10 rounded-full w-1/3"></div>
            <div className="h-4 bg-slate-200 dark:bg-white/10 rounded-full w-1/4"></div>
            <div className="h-4 bg-slate-200 dark:bg-white/10 rounded-full w-1/6"></div>
          </div>
          <div className="flex flex-col gap-3">
            {[1, 2, 3, 4, 5].map(i => (
              <div key={i} className="h-16 bg-slate-200 dark:bg-white/10 rounded-xl w-full"></div>
            ))}
          </div>
        </div>
      ) : (
        <div className="overflow-x-auto w-full flex flex-col gap-4">
          {filteredQuestions.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-center border-2 border-dashed border-slate-200 dark:border-white/10 rounded-[2.2rem] bg-slate-50/50 dark:bg-white/5 mx-4">
              <div className="p-4 bg-blue-500/10 rounded-[1.5rem] mb-4">
                <BookOpen size={32} className="text-blue-400" />
              </div>
              <p className="text-base font-black text-slate-600 dark:text-slate-300">
                {searchQuery.trim() !== "" ? "No se encontraron preguntas" : "Banco de Preguntas Vacío"}
              </p>
              <p className="text-sm text-slate-500 font-medium mt-2 max-w-sm">
                {searchQuery.trim() !== "" 
                  ? "Intenta con otra palabra clave en el buscador." 
                  : "No hay preguntas registradas en este nivel. Haz clic en 'Agregar Pregunta' para comenzar a llenar el banco."}
              </p>
            </div>
          ) : (
            <>
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-white/10 text-xs font-black uppercase text-slate-500 dark:text-slate-400">
                    <th className="py-3 px-4">Pregunta / Enunciado</th>
                    <th className="py-3 px-4">Respuesta Correcta</th>
                    <th className="py-3 px-4">Tipo</th>
                    <th className="py-3 px-4 text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {paginatedQuestions.map((q) => (
                    <tr key={q.id} className="border-b border-slate-200 dark:border-white/5 hover:bg-white dark:bg-white/5 transition-colors text-sm">
                      <td className="py-4 px-4 font-semibold max-w-md truncate">{q.enunciado}</td>
                      <td className="py-4 px-4 font-bold text-green-400">{q.respuesta_correcta}</td>
                      <td className="py-4 px-4">
                        <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full font-bold uppercase">
                          {q.tipo_pregunta === 'multiple_opcion' ? 'Opción Múltiple' : 'Numérica'}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-right flex items-center justify-end gap-1">
                        <button
                          onClick={() => onOpenEditModal(q)}
                          className="p-2 hover:bg-slate-200 dark:hover:bg-slate-100 dark:bg-white/10 rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors cursor-pointer"
                        >
                          <Edit size={16} />
                        </button>
                        <button
                          onClick={() => onDeleteQuestion(q.id)}
                          className="p-2 hover:bg-red-500/20 rounded-lg text-slate-500 dark:text-slate-400 hover:text-red-400 transition-colors cursor-pointer"
                        >
                          <Trash2 size={16} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Pagination Controls */}
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-slate-200 dark:border-white/5 pt-4 mt-2">
                <div className="text-xs font-bold text-slate-500">
                  Mostrando {indexOfFirstQuestion + 1} - {Math.min(indexOfLastQuestion, filteredQuestions.length)} de {filteredQuestions.length} preguntas
                </div>
                
                {totalPages > 1 && (
                  <div className="flex items-center gap-1.5">
                    {/* Previous button */}
                    <button
                      onClick={() => setCurrentPage(Math.max(currentPage - 1, 1))}
                      disabled={currentPage === 1}
                      className="p-2 rounded-lg bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white hover:bg-slate-200 dark:hover:bg-slate-100 dark:bg-white/10 disabled:opacity-40 disabled:hover:bg-white dark:bg-white/5 disabled:hover:text-slate-500 dark:text-slate-400 transition-all cursor-pointer"
                    >
                      <ChevronLeft size={14} />
                    </button>

                    {/* Page numbers */}
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
                      const isActive = currentPage === page;
                      return (
                        <button
                          key={page}
                          onClick={() => setCurrentPage(page)}
                          className={`w-8 h-8 rounded-lg text-xs font-black transition-all cursor-pointer ${
                            isActive 
                              ? 'bg-blue-600 text-slate-900 dark:text-white shadow-[0_0_12px_rgba(37,99,235,0.3)]' 
                              : 'bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white hover:bg-slate-200 dark:hover:bg-slate-100 dark:bg-white/10'
                          }`}
                        >
                          {page}
                        </button>
                      );
                    })}

                    {/* Next button */}
                    <button
                      onClick={() => setCurrentPage(Math.min(currentPage + 1, totalPages))}
                      disabled={currentPage === totalPages}
                      className="p-2 rounded-lg bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white hover:bg-slate-200 dark:hover:bg-slate-100 dark:bg-white/10 disabled:opacity-40 disabled:hover:bg-white dark:bg-white/5 disabled:hover:text-slate-500 dark:text-slate-400 transition-all cursor-pointer"
                    >
                      <ChevronRight size={14} />
                    </button>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};
