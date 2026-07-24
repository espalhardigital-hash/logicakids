import urllib.request
import json
import sys

BASE_URL = "http://localhost:8000"

def get_auth_token():
    url = f"{BASE_URL}/api/auth/login"
    # Form data for OAuth2 password request
    data = "username=admin%40logicakids.pro&password=admin123".encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
    })
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            token = body.get("access_token")
            print(f"[OK] Authentication Login Token acquired for amilcar@gmail.com")
            return token
    except Exception as e:
        print(f"[FAIL] Login failed: {e}")
        return None

def test_authenticated_dashboard(fase_id, token):
    url = f"{BASE_URL}/api/fase{fase_id}/dashboard"
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Mozilla/5.0'
    })
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            data = json.loads(resp.read().decode('utf-8'))
            modulos_count = len(data.get("modulos", []))
            print(f"[OK] Dashboard Fase {fase_id} (http://localhost:8000/api/fase{fase_id}/dashboard) -> Status {status}, Modulos: {modulos_count}")
            return True
    except Exception as e:
        print(f"[FAIL] Dashboard Fase {fase_id} error: {e}")
        return False

print("=" * 80)
print("VERIFICACIÓN DE AUTENTICACIÓN Y DASHBOARDS (TAREA 2)")
print("=" * 80)

token = get_auth_token()
if token:
    for f in [4, 5, 6, 7]:
        test_authenticated_dashboard(f, token)
else:
    print("No se pudo obtener el token de autenticación.")

print("=" * 80)
