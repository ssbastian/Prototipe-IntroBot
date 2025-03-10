# Herramienta para mejorar las habilidades comunicativas en introvertidos sociales🤖


Este es un prototipo chatbot desarrollado con **Rasa** para el proyecto de tesis.

## 📂 Estructura del Proyecto
```
actions/
config.yml
credentials.yml
data/
domain.yml
endpoints.yml
models/
requirements.txt
tests/
```

## 🛠 Instalación y Uso

### 🔹 Requisitos
- Python 3.10
- Rasa Open Source
- Virtualenv (opcional pero recomendado)

## 🔹 Configuración del Entorno Virtual
# Instalar virtualenv si no lo tienes
pip install virtualenv

# Crear un entorno virtual (por ejemplo, llamado 'rasa_env')
python -m venv rasa_env

# Activar el entorno virtual
# En Windows desde la terminal
rasa_env\Scripts\Activate.ps1  
# En macOS/Linux
source rasa_env/bin/activate


## 🔹 Instalación de dependencias
```sh
pip install -r requirements.txt
```

### 🔹 Entrenar el modelo
```sh
rasa train
```

### 🔹 Ejecutar el chatbot
```sh
rasa shell
```

## 📜 Licencia

