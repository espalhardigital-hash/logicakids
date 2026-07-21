---
name: github-repository-management
description: Guía y procedimientos para configurar el remoto, gestionar credenciales y realizar commits y pushes en el nuevo repositorio privado de GitHub (https://github.com/espalhardigital-hash/logicakids.git).
---

# Habilidad: Gestión de Repositorio y Commits en GitHub

Esta habilidad documenta las credenciales, configuración de remotos y los procedimientos exactos para realizar commits y sincronizar cambios en el nuevo repositorio privado de GitHub de **LogicaKids**.

---

## 1. Datos del Repositorio Privado

* **Organización / Propietario**: `espalhardigital-hash`
* **Nombre del Repositorio**: `logicakids`
* **URL Remota (HTTPS)**: `https://github.com/espalhardigital-hash/logicakids.git`
* **Visibilidad**: Privado
* **Rama Principal**: `main`
* **Rama de Desarrollo**: `desarrollo`

---

## 2. Reglas de Seguridad y Autorización (Agente AI)

> [!IMPORTANT]
> **Reglas de Git para el Agente:**
> 1. El agente **NUNCA** ejecutará automáticamente comandos que alteren o actualicen el repositorio en GitHub (como `git commit` o `git push`) sin que el usuario lo haya solicitado de forma expresa y explícita en la conversación.
> 2. Al realizar updates o pushes, siempre verificar el remoto objetivo (`origin`) y confirmar la rama de destino (`main` o `desarrollo`).

---

## 3. Guía de Inicio Rápidos y Comandos

### A. Inicialización desde Cero (Repositorio Nuevo)
Si se requiere inicializar un repositorio local completamente nuevo y vincularlo:

```powershell
echo "# logicakids" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/espalhardigital-hash/logicakids.git
git push -u origin main
```

### B. Vincular o Reemplazar Remoto en Proyecto Existente
Para actualizar el repositorio existente al nuevo repositorio privado:

```powershell
# 1. Verificar el remoto actual
git remote -v

# 2. Reconfigurar la URL del remoto 'origin' (o agregarlo si no existe)
git remote set-url origin https://github.com/espalhardigital-hash/logicakids.git

# 3. Asegurar nombre de la rama principal
git branch -M main

# 4. Enviar los cambios iniciales y vincular la rama
git push -u origin main
```

### C. Flujo Habitual de Commits y Pushes

1. **Verificar estado de archivos en cambio:**
   ```powershell
   git status
   ```

2. **Añadir archivos al stage:**
   ```powershell
   git add .
   ```

3. **Crear commit con un mensaje descriptivo:**
   ```powershell
   git commit -m "feat: descripción de los cambios realizados"
   ```

4. **Hacer push al repositorio remoto:**
   - Para la rama principal `main`:
     ```powershell
     git push origin main
     ```
   - Para la rama de desarrollo `desarrollo`:
     ```powershell
     git push origin desarrollo
     ```

---

## 4. Credenciales y Autenticación de GitHub

En Windows (PowerShell), la autenticación con GitHub se realiza a través de:

1. **Git Credential Manager (GCM)**:
   Al ejecutar el primer `git push`, Windows solicitará el inicio de sesión web o un **Personal Access Token (PAT)** de GitHub.
   
2. **Personal Access Token (PAT)**:
   - Si se utiliza un Token Personal en lugar de contraseña, se requiere el permiso `repo` (Full control of private repositories).
   - En caso de configurar la URL con token empotrado (para automatizaciones autorizadas en scripts locales):
     ```powershell
     https://<TOKEN>@github.com/espalhardigital-hash/logicakids.git
     ```
   > [!CAUTION]
   > Nunca incluir tokens de acceso directamente en archivos de código expuestos ni commits. Mantenerlos exclusivamente en la bóveda de credenciales local de Windows o archivos `.env.local` fuera del control de versiones.
