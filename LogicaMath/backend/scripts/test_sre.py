import asyncio
import sys

async def main():
    print("==========================================")
    print("🔍 VERIFICACIÓN DE TERRENO BACKEND SRE")
    print("==========================================")
    
    from app.admin.router import get_sre_status, refresh_sre_status, get_sre_history
    from app.db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        admin_mock = {"sub": "admin_test", "email": "test@logicakids.local"}

        status = await get_sre_status(db=db)
        print("1. GET /admin/sre/status OK:", status["summary"])
        print("   -> Generado a:", status["generated_at"])
        print("   -> Es Fallback:", status.get("is_fallback", False))

        refreshed = await refresh_sre_status(db=db, admin_user=admin_mock)
        print("2. POST /admin/sre/refresh OK:", refreshed["status"])
        print("   -> Mensaje:", refreshed["message"])

        history = await get_sre_history(admin_user=admin_mock)
        print("3. GET /admin/sre/history OK: Total elementos =", len(history))
        if history:
            print("   -> Último registro:", history[0]["filename"])

    print("==========================================")
    print("🎉 PRUEBA COMPLETADA EXITOSAMENTE")
    print("==========================================")

if __name__ == "__main__":
    asyncio.run(main())
