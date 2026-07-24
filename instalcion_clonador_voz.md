Aquí tienes la versión en un **único bloque de código continuo**. Puedes usar el botón de **"Copiar"** (en la esquina superior derecha del bloque) y pegarlo directamente dentro de tu archivo `README_INSTALACION.md` en la raíz de tu proyecto:

```markdown
# Guía de Instalación y Configuración - GPT-SoVITS (Windows)

Documento de referencia para la instalación limpia del entorno de desarrollo de **GPT-SoVITS** con aceleración por GPU NVIDIA en Windows 11.

---

## 📋 Requisitos Previos

* **Sistema Operativo:** Windows 10/11 (64-bit).
* **GPU:** NVIDIA GeForce con soporte CUDA (ej. GTX 1660 / 6 GB VRAM o superior).
* **Controladores NVIDIA:** Actualizados (soportando CUDA 11.8+).
* **Python:** Versión **3.10.x** (Obligatorio; versiones superiores como 3.14 no son compatibles con las dependencias compiladas de PyTorch).

---

## 🛠️ Paso a Paso de la Instalación

### 1. Preparar Python 3.10 en el Sistema
Si tienes varias versiones de Python instaladas, descarga e instala silenciosamente la versión 3.10 desde la consola:

```cmd
curl -o python-3.10.11.exe [https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)
python-3.10.11.exe /quiet InstallAllUsers=1 PrependPath=1

```

### 2. Crear y Activar el Entorno Virtual (`venv`)

Navega hasta la carpeta del proyecto y crea el entorno aislado usando el ejecutable de Python 3.10:

```cmd
cd D:\Antigravity\Clonador-voz\GPT-SoVITS
py -3.10 -m venv venv
venv\Scripts\activate

```

*Verifica que en la terminal aparezca el prefijo `(venv)` y responda `Python 3.10.11` al ejecutar `python --version`.*

---

### 3. Instalar PyTorch con Aceleración CUDA

Instala la versión de PyTorch específica compilada para soporte GPU (CUDA 11.8):

```cmd
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu118](https://download.pytorch.org/whl/cu118)

```

---

### 4. Resolver Dependencias Precompiladas (Windows Workaround)

En Windows, librerías como `pyopenjtalk` requieren un compilador de C++ si no se usa una versión precompilada. Para evitar instalar Visual Studio C++, se instala la versión preconstruida:

```cmd
pip install pyopenjtalk-prebuilt

```

---

### 5. Instalar las Librerías y Requerimientos del Proyecto

Instala los paquetes principales y herramientas de utilidad para el monitoreo de hardware:

```cmd
pip install scipy tensorboard librosa numba pytorch-lightning gradio ffmpeg-python onnxruntime-gpu funasr cn2an pypinyin psutil

```

---

## 🧪 Verificación del Hardware (GPU NVIDIA)

Antes de iniciar la aplicación, valida que PyTorch esté detectando la GPU correctamente ejecutando este comando rápido:

```cmd
python -c "import torch; print('¿CUDA activo?:', torch.cuda.is_available()); print('GPU en uso:', torch.cuda.get_device_name(0))"

```

*Salida esperada:*

> `¿CUDA activo?: True`
> `GPU en uso: NVIDIA GeForce GTX 1660` (o el nombre de tu tarjeta)

---

## 🚀 Ejecución de la Aplicación

Con el entorno virtual activado (`venv`), lanza la interfaz web con:

```cmd
python webui.py

```

Abre tu navegador web e ingresa a la dirección local que aparece en la consola (por defecto: `http://127.0.0.1:9874`).

---

## 📌 Mantenimiento y Reinicio Posterior

Para volver a abrir el proyecto en sesiones futuras:

1. Abre la terminal en la carpeta del proyecto.
2. Activa el entorno virtual: `venv\Scripts\activate`
3. Ejecuta la interfaz: `python webui.py`

```

```