# Para generar la imagen custom

docker build --no-cache -f dockerfiles/Dockerfile.dev -t 'adammartin/django_base:latest' .

# Para añadir a los Dockerfiles y que cojan la imagen base

FROM adammartin/django_base:latest

# Para generar la imagen custom

docker build --no-cache -f dockerfiles/Dockerfile.prod -t 'adammartin/django_ ase:latest' .

# Para añadir a los Dockerfiles y que cojan la imagen base

FROM adammartin/django_base:latest

pass cRsuD20r0zVI
