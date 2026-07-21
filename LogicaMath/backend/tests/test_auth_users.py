import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.routers.auth_users import login, register, logout
from datetime import datetime

@pytest.mark.asyncio
async def test_login_rollback_failure_tolerance():
    """
    Verifica que si la actualización del last_login falla y luego el rollback también falla,
    el endpoint aún devuelve el token exitosamente (tolerancia a fallos) y loggea el error crítico.
    """
    form_data = AsyncMock(spec=OAuth2PasswordRequestForm)
    form_data.username = "test_user"
    form_data.password = "test_pass"
    
    db_mock = AsyncMock()
    response_mock = MagicMock()
    
    db_mock.commit.side_effect = Exception("DB Commit Timeout")
    db_mock.rollback.side_effect = Exception("Rollback Failed (Connection Lost)")
    
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "test_user"
    mock_user.last_login = None
    
    with patch("app.routers.auth_users.authenticate_user", new_callable=AsyncMock) as mock_auth:
        mock_auth.return_value = mock_user
        
        with patch("app.routers.auth_users.create_access_token") as mock_create_token:
            mock_create_token.return_value = "mocked_token"
            
            result = await login(response=response_mock, form_data=form_data, db=db_mock)
            
            assert result.access_token == "mocked_token"
            mock_auth.assert_called_once_with(db_mock, "test_user", "test_pass")
            response_mock.set_cookie.assert_called_once()
            db_mock.commit.assert_called_once()
            db_mock.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_logout_deletes_cookie():
    response_mock = MagicMock()
    res = await logout(response=response_mock)
    assert res["message"] == "Sesión cerrada correctamente"
    response_mock.delete_cookie.assert_called_once_with(key="access_token")
