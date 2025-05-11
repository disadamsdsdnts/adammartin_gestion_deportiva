# Reglas y Buenas Prácticas del Proyecto

Este documento describe las reglas y buenas prácticas que se siguen en este proyecto Django.

## 1. Estructura del Proyecto
- Organización modular por aplicaciones (baedev/, users/, configuration/, etc.)
- Separación clara de responsabilidades por carpetas (models/, forms/, views/)
- Uso de archivos `__init__.py` para gestionar imports

## 2. Modelos
- Herencia de modelos base:
  - `AuditModel`: Proporciona campos automáticos de auditoría (`created`, `modified`)
  - `SingletonModel`: Para configuraciones globales únicas
- Uso de verbose_name y verbose_name_plural en Meta
- Implementación de `__str__` para representación legible
- Campos con nombres descriptivos en español
- Uso de `on_delete` en ForeignKeys

## 3. Formularios
- Herencia de `ModelForm` para formularios basados en modelos
- Validación personalizada con métodos `clean_*`
- Uso de widgets personalizados (Select2)
- Implementación de `__init__` para personalizar campos
- Traducciones con `gettext` y `gettext_lazy`

## 4. Vistas
- Uso de Class-Based Views (CBV)
- Decoradores para control de acceso (`@login_required`, `@is_global_admin`)
- Implementación de `get_context_data` para datos comunes
- Sistema de breadcrumbs consistente
- Integración con tema Metronic

### 4.1 Estructura Estándar de Vistas por Modelo
Para cada modelo, se deben implementar las siguientes vistas genéricas:

1. **ListView** (Listar registros):
```python
@method_decorator([is_global_admin], name='dispatch')
class ModelListView(ListView):
    template_name = 'app/ModelList.html'
    model = Model
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['page_title'] = _('Título')
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Sección'), 'url': reverse('app:model_list')},
        ]
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('app:model_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        return context
```

2. **DetailView** (Ver detalle):
```python
@method_decorator([is_global_admin], name='dispatch')
class ModelDetailView(DetailView):
    template_name = 'app/ModelDetail.html'
    model = Model
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['page_title'] = f"{_('Objeto')} : {self.object.name}"
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Sección'), 'url': reverse('app:model_list')},
            {'title': self.object.name}
        ]
        return context
```

3. **CreateView** (Crear nuevo):
```python
@method_decorator([is_global_admin], name='dispatch')
class ModelCreateView(CreateView):
    template_name = 'app/ModelCreate.html'
    model = Model
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['page_title'] = _('Nuevo Objeto')
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Sección'), 'url': reverse('app:model_list')},
            {'title': _('Nuevo'), 'url': reverse('app:model_create')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Objeto creado correctamente')
        )
        return reverse_lazy('app:model_list')
```

4. **UpdateView** (Editar):
```python
@method_decorator([is_global_admin], name='dispatch')
class ModelUpdateView(UpdateView):
    template_name = 'app/ModelUpdate.html'
    model = Model
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['page_title'] = _('Editar Objeto')
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Sección'), 'url': reverse('app:model_list')},
            {'title': _('Editar')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Objeto modificado correctamente')
        )
        return reverse_lazy('app:model_detail', kwargs={'pk': self.object.pk})
```

5. **DeleteView** (Eliminar):
```python
@method_decorator([is_global_admin], name='dispatch')
class ModelDeleteView(DeleteView):
    model = Model
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['page_title'] = _("Eliminar Objeto")
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Sección'), 'url': reverse('app:model_list')},
            {'title': _('Eliminar')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Objeto eliminado correctamente')
        )
        return reverse_lazy('app:model_list')
```

### 4.2 Características Comunes en las Vistas
- Uso de decoradores de permisos (`@method_decorator`)
- Implementación consistente de `get_context_data`
- Sistema de mensajes flash para feedback al usuario
- Breadcrumbs para navegación
- Integración con el tema Metronic (KTLayout)
- Traducciones con gettext
- URLs reversibles usando `reverse` y `reverse_lazy`
- Nombres de plantillas consistentes siguiendo el patrón `app/ModelAction.html`

## 5. Seguridad
- Validación de contraseñas
- Protección CSRF
- Decoradores de caché y seguridad
- Manejo de permisos y grupos

## 6. Internacionalización
- Uso consistente de `gettext` y `gettext_lazy`
- Mensajes de error traducibles
- Etiquetas de campos traducibles

## 7. Frontend
- Integración con tema Metronic
- Uso de Select2 para mejorar UI
- Clases CSS consistentes
- Sistema de breadcrumbs

## 8. Convenciones de Código
- Nombres de clases en CamelCase
- Nombres de archivos descriptivos y en snake_case
- Documentación de clases y métodos importantes
- Organización consistente de imports

## 9. Gestión de Usuarios
- Sistema personalizado de autenticación
- Manejo de contraseñas y recuperación
- Perfiles de usuario extensibles
- Sistema de grupos y permisos

## 10. Configuración
- Uso de SingletonModel para configuración global
- Separación de configuración por ambientes
- Gestión de variables de entorno

## 11. Buenas Prácticas Adicionales
- Uso de `super()` en herencias
- Manejo de mensajes flash
- URLs nombradas y reversibles
- Validaciones personalizadas
- Campos con help_text descriptivos

## 12. Testing
- Presencia de `pytest.ini` indica uso de pytest
- Estructura preparada para testing

## 13. Gestión de Dependencias
- Uso de requirements/ para diferentes entornos
- Docker compose para desarrollo

Estas reglas y prácticas hacen que el proyecto sea mantenible, escalable y siga los estándares de Django, mientras mantiene una estructura clara y organizada.
