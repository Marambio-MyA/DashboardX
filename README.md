# Sistema de Gestión de Productos

Sistema de gestión de productos desarrollado con Django.

## Requisitos

- Python 3.8 o superior
- Django 5.0 o superior
- PostgreSQL (opcional, se puede usar SQLite para desarrollo)

## Instalación

1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
cd [nombre-del-directorio]
```

2. Crear un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
   - Para SQLite (desarrollo): No se requiere configuración adicional
   - Para PostgreSQL: Configurar en `tienda/settings.py`

5. Aplicar migraciones:
```bash
python manage.py migrate
```

6. Crear un superusuario (opcional):
```bash
python manage.py createsuperuser
```

7. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

- `productos/`: Aplicación principal
  - `models.py`: Modelos de datos
  - `views.py`: Vistas de la aplicación
  - `forms.py`: Formularios
  - `templates/`: Plantillas HTML
- `tienda/`: Configuración del proyecto
  - `settings.py`: Configuración general
  - `urls.py`: URLs principales

## Características

- Gestión CRUD de productos
- Validación de datos
- Interfaz responsive con Bootstrap
- Mensajes de éxito/error 