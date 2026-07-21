from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON
from ..db.base import Base
from .enums import FeedbackTypeEnum, FeedbackStatusEnum

class UXFeedback(Base):
    """
    Modelo de base de datos para almacenar el feedback de UI/UX y bugs visuales 
    enviados por el revisor desde el Modo Evaluador.
    """
    __tablename__ = "ux_feedbacks"

    id = Column(Integer, primary_key=True, index=True)

    fase = Column(Integer, nullable=False, index=True)
    modulo_id = Column(Integer, nullable=False, index=True)
    nivel_id = Column(Integer, nullable=False, index=True)
    pregunta_id = Column(String(100), nullable=True, index=True)
    paso_actual = Column(Integer, nullable=True)

    dom_selector = Column(Text, nullable=False)
    viewport = Column(String(50), nullable=True)
    comentario = Column(Text, nullable=False)
    
    tipo = Column(
        Enum(FeedbackTypeEnum, name="ux_feedback_tipo", native_enum=False),
        default=FeedbackTypeEnum.BUG_VISUAL,
        nullable=False,
    )
    
    prioridad = Column(String(20), default="media", nullable=False) # baja, media, alta, critica
    
    app_state = Column(JSON, nullable=True)
    screenshot_url = Column(String(255), nullable=True)
    
    estado = Column(
        Enum(FeedbackStatusEnum, name="ux_feedback_estado", native_enum=False),
        default=FeedbackStatusEnum.PENDIENTE,
        nullable=False,
        index=True
    )
    
    desarrollador_notes = Column("desarrollador_notas", Text, nullable=True)

    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    ultima_modificacion = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self):
        return f"<UXFeedback id={self.id} fase={self.fase} modulo={self.modulo_id} tipo={self.tipo} estado={self.estado}>"
