# Trabajo de Final de Ciclo

## Introducción

El presente proyecto tiene como finalidad el desarrollo de una aplicación web para la **gestión de un equipo de fútbol**, abarcando todos los elementos clave de su día a día: la administración de jugadores, equipos contrarios, temporadas, resultados y estadísticas relevantes como tarjetas. El proyecto busca combinar el desarrollo técnico con una proyección práctica y económica, haciendo uso de herramientas actuales y orientadas al despliegue y la escalabilidad.

## Documentos del proyecto
- [Trabajo del proyecto](https://docs.google.com/document/d/1e52IDNOS9UoQX5oOJPwAVAHNHViP8_pzB9Sro8Vgf3s/edit?tab=t.0#heading=h.cqcld96sqn3p)

## Descripción general de la aplicación

La aplicación está pensada para ser utilizada por **clubes deportivos, entrenadores o gestores de equipos**, permitiéndoles registrar y gestionar toda la información relativa a su equipo de forma centralizada y accesible desde cualquier dispositivo.

Entre sus funcionalidades destacan:

- Gestión de **temporadas** y equipos.
- Registro de **jugadores** y sus estadísticas.
- Control de **partidos jugados**, resultados, equipos contrarios y sanciones (tarjetas).
- Posibilidad de obtener informes o historiales por temporada o jugador.

## Tecnologías utilizadas

Para el desarrollo de la aplicación se empleará **Django**, uno de los frameworks más robustos y utilizados en el desarrollo web con Python. La aplicación estará completamente **dockerizada**, lo cual permitirá su fácil transporte, despliegue y escalabilidad.

La base de datos será **PostgreSQL**, contenida en un contenedor Docker separado, y la aplicación se diseñará visualmente con **Tailwind CSS**, complementado con el sistema de componentes **Frostbite**. Para la creación de prototipos visuales y flujos de navegación se empleará **Figma**.

## Aspecto económico y despliegue

Como parte de la viabilidad del proyecto, se utilizará **Coolify**, una plataforma moderna de despliegue continuo en la nube. Esto permitirá ofrecer el proyecto como **servicio SaaS (Software as a Service)**, posibilitando su comercialización como herramienta para clubes deportivos de cualquier tamaño. De esta manera, se podrá vender o alquilar la aplicación a distintos clientes sin necesidad de realizar instalaciones manuales.

## Relación con los módulos del ciclo formativo

- **0483. Sistemas informáticos:** Uso de Docker y configuración de entornos de desarrollo virtualizados para la aplicación.
- **0484. Bases de datos:** Modelado y gestión de la base de datos PostgreSQL, así como la relación entre entidades (jugadores, partidos, equipos, etc.).
- **0485. Programación:** Implementación de la lógica de negocio con Django, controladores, validaciones y estructuras de datos.
- **0373. Lenguajes de marcas y sistemas de gestión de información:** Uso de HTML, JSON y plantillas en Django; estructuras de datos intercambiables.
- **0487. Entornos de desarrollo:** Uso de herramientas como Docker, Visual Studio Code y Git para gestionar el ciclo de vida del software.
- **0612. Desarrollo web en entorno cliente:** Aplicación de Tailwind CSS, manipulación de formularios y validaciones del lado del cliente.
- **0613. Desarrollo web en entorno servidor:** Desarrollo con Django, arquitectura MVC, APIs REST y tratamiento del backend.
- **0614. Despliegue de aplicaciones web:** Dockerización completa del entorno, despliegue automatizado con Coolify y posible integración con servicios en la nube.
- **0615. Diseño de interfaces WEB:** Maquetación responsiva y visual con Tailwind y Frostbite, prototipos realizados en Figma.
