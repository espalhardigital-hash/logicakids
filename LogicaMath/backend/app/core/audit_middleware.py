import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import AsyncSessionLocal
from ..models.audit import AuditLog

class AuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware that intercepts all mutating requests (POST, PUT, PATCH, DELETE)
    to /admin/* endpoints and logs them to the AuditLog table for compliance.
    """
    async def dispatch(self, request: Request, call_next):
        # We only care about /admin paths
        if request.url.path.startswith("/admin") and request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # Capture request body (up to 2000 chars to avoid huge payloads)
            body = b""
            try:
                body = await request.body()
            except Exception:
                pass
            
            payload_summary = body.decode("utf-8", errors="ignore")[:2000] if body else None
            
            # Re-inject the body safely so FastAPI endpoints can read it without hanging
            async def receive():
                return {"type": "http.request", "body": body, "more_body": False}
            request._receive = receive
            
            response = await call_next(request)
            
            auth_header = request.headers.get("Authorization", "")
            admin_id = "UNKNOWN"
            if auth_header.startswith("Bearer "):
                admin_id = "ADMIN_TOKEN_USED"

            try:
                async with AsyncSessionLocal() as session:
                    audit_entry = AuditLog(
                        admin_id=admin_id,
                        action=f"{request.method} {request.url.path}",
                        endpoint=request.url.path,
                        method=request.method,
                        payload_summary=payload_summary,
                        ip_address=request.client.host if request.client else "UNKNOWN"
                    )
                    session.add(audit_entry)
                    await session.commit()
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Error guardando AuditLog en AuditMiddleware: {e}")

            return response
        else:
            return await call_next(request)
