import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from app.routers.ux_feedback import create_ux_feedback, list_ux_feedbacks, update_ux_feedback
from app.schemas import UXFeedbackCreate, UXFeedbackUpdate
from app.models.enums import FeedbackTypeEnum, FeedbackStatusEnum

@pytest.mark.asyncio
async def test_create_ux_feedback_success():
    """Prueba que el registro de feedback de UX se realiza exitosamente en base de datos."""
    # Mock payload
    payload = UXFeedbackCreate(
        fase=4,
        modulo_id=1,
        nivel_id=1,
        pregunta_id="Q123",
        paso_actual=2,
        dom_selector="div.f4-pizza-visualizer",
        viewport="1024x768",
        comentario="Alinear elemento visual",
        tipo=FeedbackTypeEnum.BUG_VISUAL,
        prioridad="alta"
    )
    
    # Mock DB session
    db_mock = AsyncMock()
    
    # Mock current user
    user_mock = {"id": "1", "username": "revisor_test", "role": "ADMIN"}
    
    # Run endpoint logic
    res = await create_ux_feedback(payload=payload, db=db_mock, current_user=user_mock)
    
    # Assertions
    assert res.fase == 4
    assert res.comentario == "Alinear elemento visual"
    assert res.dom_selector == "div.f4-pizza-visualizer"
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_create_ux_feedback_db_error():
    """Prueba que si ocurre un fallo al guardar en base de datos se hace rollback y se eleva un HTTP 500."""
    payload = UXFeedbackCreate(
        fase=4,
        modulo_id=1,
        nivel_id=1,
        dom_selector="div",
        comentario="Error de base de datos"
    )
    
    db_mock = AsyncMock()
    db_mock.commit.side_effect = Exception("DB error connection")
    
    user_mock = {"id": "1", "username": "revisor_test"}
    
    # Verify rollback occurs and HTTPException is raised
    with pytest.raises(HTTPException) as exc_info:
        await create_ux_feedback(payload=payload, db=db_mock, current_user=user_mock)
        
    assert exc_info.value.status_code == 500
    db_mock.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_list_ux_feedbacks():
    """Prueba que el listado de feedbacks funciona y ejecuta la query."""
    db_mock = AsyncMock()
    
    # Mock db.execute to return a list of mock feedbacks
    mock_feedback = MagicMock()
    mock_feedback.id = 1
    mock_feedback.comentario = "Pizza desalineada"
    
    execute_result_mock = MagicMock()
    execute_result_mock.scalars().all.return_value = [mock_feedback]
    db_mock.execute.return_value = execute_result_mock
    
    admin_mock = {"role": "ADMIN"}
    
    # Run query
    res = await list_ux_feedbacks(fase=4, estado=FeedbackStatusEnum.PENDIENTE, db=db_mock, admin_user=admin_mock)
    
    assert len(res) == 1
    assert res[0].comentario == "Pizza desalineada"
    db_mock.execute.assert_called_once()

@pytest.mark.asyncio
async def test_update_ux_feedback_success():
    """Prueba que la actualización de estado y notas se realiza y guarda de forma correcta."""
    db_mock = AsyncMock()
    
    # Mock db.execute to return the target feedback
    mock_feedback = MagicMock()
    mock_feedback.id = 10
    mock_feedback.estado = FeedbackStatusEnum.PENDIENTE
    mock_feedback.desarrollador_notes = None
    
    execute_result_mock = MagicMock()
    execute_result_mock.scalar_one_or_none.return_value = mock_feedback
    db_mock.execute.return_value = execute_result_mock
    
    # Request data
    payload = UXFeedbackUpdate(
        estado=FeedbackStatusEnum.RESUELTO,
        desarrollador_notes="Corregido alineando el estilo en Fase4Styles.css"
    )
    
    admin_mock = {"role": "ADMIN"}
    
    res = await update_ux_feedback(feedback_id=10, payload=payload, db=db_mock, admin_user=admin_mock)
    
    # Assertions
    assert res.estado == FeedbackStatusEnum.RESUELTO
    assert res.desarrollador_notes == "Corregido alineando el estilo en Fase4Styles.css"
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(mock_feedback)

@pytest.mark.asyncio
async def test_upload_feedback_screenshot_success():
    """Prueba la subida de capturas de pantalla exitosa."""
    from fastapi import UploadFile
    from app.routers.ux_feedback import upload_feedback_screenshot_endpoint
    
    # Mock file y contenido
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test_screen.png"
    mock_file.read.return_value = b"fakeimagebytes"
    
    # Mock current user
    user_mock = {"id": "1", "username": "admin_test", "role": "ADMIN"}
    
    with patch("app.routers.ux_feedback.storage_service.upload_feedback_screenshot", new_callable=AsyncMock) as upload_mock:
        upload_mock.return_value = "/evaluador/feedback/screenshots/uuid123.png"
        
        res = await upload_feedback_screenshot_endpoint(file=mock_file, current_user=user_mock)
        
        assert res == {"url": "/evaluador/feedback/screenshots/uuid123.png"}
        upload_mock.assert_called_once_with(b"fakeimagebytes", "test_screen.png")

@pytest.mark.asyncio
async def test_get_feedback_screenshot_local():
    """Prueba la recuperación de una captura de pantalla local."""
    from app.routers.ux_feedback import get_feedback_screenshot
    
    with patch("os.path.exists", return_value=True), \
         patch("app.routers.ux_feedback.FileResponse") as mock_fileresponse:
        
        mock_fileresponse.return_value = "FileResponseObject"
        
        res = await get_feedback_screenshot("uuid123.png")
        
        assert res == "FileResponseObject"
        mock_fileresponse.assert_called_once()

@pytest.mark.asyncio
async def test_create_ux_feedback_multiple_images():
    """Prueba que el registro de feedback con múltiples imágenes se realiza exitosamente."""
    from app.schemas import UXFeedbackImagen
    
    payload = UXFeedbackCreate(
        fase=4,
        modulo_id=1,
        nivel_id=1,
        dom_selector="div",
        comentario="Prueba con dos imágenes",
        tipo=FeedbackTypeEnum.BUG_VISUAL,
        imagenes=[
            UXFeedbackImagen(url="http://url/actual.png", rol="actual"),
            UXFeedbackImagen(url="http://url/referencia.png", rol="referencia")
        ]
    )
    
    db_mock = AsyncMock()
    user_mock = {"id": "1", "username": "revisor_test", "role": "ADMIN"}
    
    res = await create_ux_feedback(payload=payload, db=db_mock, current_user=user_mock)
    
    # La llamada directa omite la validación response_model que aplica FastAPI.
    # Valida aquí la parte anidada sin exigir campos que normalmente completa la BD.
    imagenes = [UXFeedbackImagen.model_validate(imagen) for imagen in res.imagenes]
    assert res.comentario == "Prueba con dos imágenes"
    assert len(imagenes) == 2
    assert imagenes[0].rol == "actual"
    assert imagenes[1].rol == "referencia"
    db_mock.add.assert_called_once()

@pytest.mark.asyncio
async def test_create_ux_feedback_reporter_id():
    """Prueba que el reporter_id se establece a partir del current_user del token."""
    payload = UXFeedbackCreate(
        fase=4,
        modulo_id=1,
        nivel_id=1,
        dom_selector="div",
        comentario="Prueba reporter_id",
        tipo=FeedbackTypeEnum.BUG_VISUAL,
        app_state={"user": {"username": "fake_user", "role": "USER"}} # Intentional fake user in state
    )
    
    db_mock = AsyncMock()
    user_mock = {"id": "revisor_uuid_123", "username": "revisor_real", "role": "ADMIN"}
    
    res = await create_ux_feedback(payload=payload, db=db_mock, current_user=user_mock)
    
    assert res.reporter_id == "revisor_uuid_123"
    db_mock.add.assert_called_once()
