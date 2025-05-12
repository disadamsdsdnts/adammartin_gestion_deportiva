Despliegue de FutGOAL
============

Necesitaremos tener instalado tanto Docker como Docker Compose, que es un orquestador de contenedores de Docker

El fichero que tendremos que cargar será el fichero dev.yml, ese fichero está compuesto por

- Contenedor principal django
- Contenedor de base de datos postgres

# Entorno dev

Apartado para mostrar toda la información del desarrollo en modo dev.

## Generación de entorno DEV

### Creación de imágenes base

Tanto el contenedor de Django como las réplicas, necesitan de una imagen base que será la primera que tendremos que crear. Para ello navegaremos al directorio **compose/djangobase** y ejecutaremos la creación de la imagen base con el comando:

`docker build --no-cache -f dockerfiles/Dockerfile.dev -t 'adammartin/django_base:latest' .`

Esto nos creará la imagen 'adammartin/django_base:latest' que si os fijáis es la imagen de base del DockerFile de Django: `FROM adammartin/django_base:latest`

### Creación de las imágenes del stack

Una vez ya tenemos la imagen base, volvemos al directorio principal y ya podemos construir las imágenes del stack. Desde el directorio raiz:

`docker-compose -f dev.yml build`

### Creación de las tablas del sistema
> **Nota:** Este comando no es necesario si la base de datos ya está creada y tiene todas las tablas. Pero no hay peligro de nada si se ejecuta durante estos pasos.

Una vez con las imágenes realizadas, ya podremos lanzar el comando migrate para crear las tablas de la base de datos con:

`docker-compose -f dev.yml run --rm django python manage.py migrate`

## Ejecución del entorno DEV
### Arrancar el stack

Ya tendremos todo listo para arrancar el stack. Lo arrancamos con:

`docker-compose -f dev.yml run --rm --service-ports django`
`docker-compose -f dev.yml up -d`  Esto es para arrancarlo en segundo plano

### Parar el stack

`docker-compose -f dev.yml down`

El contenedor de Django tiene el puerto 8000 puenteado por lo que ya podremos entrar desde nuestro navegador en <http://localhost:8000>


# Funcionalidades de un solo uso

## Creación de usuario administrador

Una vez creadas las tablas, creemos nuestro primer usuario administrador

`docker-compose -f dev.yml run --rm django python manage.py createsuperuser`

Ahí nos pedirá usuario, email contraseña etc...

## Creación de la instancia Configuration

`docker-compose -f dev.yml run --rm django python manage.py shell_plus`

Configuration.objects.create(app_name="Baedev")

exit()

# Paquetes utilizados
## Paquetes base
- **psycopg2:**
  - Adaptador de base de datos para PostgreSQL.
  - [Documentación en PyPi](https://pypi.org/project/psycopg2/)
- **Django-environ:**
  - Paquete de Python que te permite usar la [metodología de 12 factores](https://www.12factor.net/es/) en aplicaciones de Django.
  - [Documentación oficial](https://django-environ.readthedocs.io/en/latest/)
- **Crispy Forms:**
  - Permite modificar y darle estilos a los formularios de Django de forma fácil y sin modificar la lógica interna de Django.
  - [Documentación oficial](https://django-crispy-forms.readthedocs.io/en/latest/)
- **Crispy Forms - Bootstrap 4:**
  - Estilos base usados para Metronic para darle estilos a los formularios.
- **Django Extensions:**
  - Añade comandos de administración, nuevos campos a la base de datos, extensiones de admin y mucho más.
  - [Documentación oficial](https://django-extensions.readthedocs.io/en/latest/)

## Paquetes de Desarrollo
- **Django Debug Toolbar:**
  - Barra lateral para mostrar en el el front-end o back-end para mostrar una lista de paneles de información para encontrar errores, fallos de rendimiento, entre otros.
  - [Documentación oficial](https://django-debug-toolbar.readthedocs.io/en/latest/)
- **ipdb:**
  - Conecta y da acceso al [IPython](https://ipython.org/) debugger para para poder hacer breakpoints, syntax highlighting, tracebacks, etc...
  - [Documentación en PyPi](https://pypi.org/project/ipdb/)

## Paquetes de Producción
- **Celery:**
  - Cola de tareas distribuida para administrar la ejecución de procesos de forma cómoda.
  - [Documentación oficial](https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html#using-celery-with-django)
- **WhiteNoise:**
  - Genera una unidad independiente de estáticos fácilmente que puede ser servida desde NGINX, Amazon S3 o cualquier servicio externo.
  - [Documentación oficial](https://whitenoise.readthedocs.io/en/stable/django.html)

# Datos importantes
- **Administración:** /admin
    - Para iniciar sesión, se utiliza el correo y no el username (a diferencia de lo que dice el panel)
