## 🔧 Listado de tareas específicas en Django

### 📁 1. Inicialización del proyecto
- [ ] Crear entorno virtual con `venv` (opcional en Docker).
- [ ] Crear proyecto con `django-admin startproject gestion_futbol`.
- [ ] Crear aplicación principal con `python manage.py startapp core`.
- [ ] Configurar `settings.py`:
  - Añadir apps instaladas.
  - Configurar base de datos PostgreSQL.
  - Configurar `STATICFILES_DIRS` y `TEMPLATES`.

### 🧩 2. Definición del modelo de datos
- [ ] Crear modelos en `models.py`:
  - `Equipo`
  - `Jugador`
  - `Temporada`
  - `Partido`
  - `Resultado`
  - `Tarjeta`
- [ ] Crear relaciones entre modelos (`ForeignKey`, `ManyToMany`, etc.).
- [ ] Crear `__str__()` para cada modelo.
- [ ] Ejecutar `makemigrations` y `migrate`.

### 🔐 3. Configuración del panel de administración
- [ ] Registrar todos los modelos en `admin.py`.
- [ ] Personalizar el `admin` con `list_display`, `search_fields`, `list_filter`, etc.
- [ ] Crear superusuario con `createsuperuser`.

### 🌐 4. Rutas y vistas
- [ ] Crear archivo `urls.py` en la app si no existe.
- [ ] Registrar rutas en el `urls.py` del proyecto.
- [ ] Crear vistas con funciones o clases (`ListView`, `CreateView`, etc.).
- [ ] Asociar cada vista con su correspondiente URL.

### 📝 5. Plantillas y formularios
- [ ] Crear estructura de carpetas `templates/core/`.
- [ ] Crear `base.html` y extenderlo en otras plantillas.
- [ ] Crear formularios con `ModelForm`.
- [ ] Renderizar formularios en plantillas con `form.as_p` o personalizado.

### ✅ 6. Validaciones y lógica de negocio
- [ ] Añadir validaciones personalizadas en `forms.py` o en los modelos (`clean()`).
- [ ] Añadir lógica específica (e.g., no permitir partidos en fechas duplicadas).
- [ ] Calcular estadísticas (tarjetas acumuladas, partidos jugados, etc.).

### 🔄 7. Paginación, filtros y mejoras de UX
- [ ] Implementar paginación con `Paginator`.
- [ ] Añadir filtros por temporada, jugador, etc.
- [ ] Mejorar navegación con enlaces contextuales y breadcrumbs.

### 🔧 8. Tests y control de calidad
- [ ] Crear tests unitarios para modelos y vistas.
- [ ] Usar `pytest` o `unittest` integrado.
- [ ] Validar que no haya errores en consola y que el flujo esté completo.
