# Proyecto_Seminario_Back

## Herramientas que utiliza el proyecto

- Python 3.10.12 como lenguaje de programacion 

- FastAPI 0.101.1 Como Framework para backend

- PostgresSQL Como lenguage de base de datos

- PngAdmin Como gestor de base de datos 

- Docker y Docker-Compose para armar los contenedores del proyecto

## Estructura de carpetas

- Toda la aplicacion se encuantra dentro de la carpeta app

- La carpeta controlers contiene los archivos donde se expondran los endpoint del backend

- La carpeta models contiene los archivos con las clases que representan los objetos con los que se trabajara

- La carpeta services contiene los archivos con los distintos servicios que expone el backend

## Requisitos Previos

- Tener instalado VScode

- Tener Instalado Docker y Docker-Compose

- Instalar la extension de VScode "Dev Container"

## Levantar el proyecto y comenzar a desarrollar

- En la carpeta del proyecto correr el comando 
`docker-compose build (para docker compose v1)`

`docker compose build (para docker compose v2)`

- Una vez terminado de construir los contenedores correr el comando
`docker-compose up (para docker compose v1)`

`docker compose up (para docker compose v2)`

- Una vez el proyecto este corriendo abrir una ventana remota en VScode

- Seleccionar la opcion attanch to running container

- Seleccionar el contenedor `proyecto_seminario_back-fastapi-1`

- Una vez este la ventana abierta asegurarse de que se instalen las extenciones de python y pylance y luego recargar la ventana

- Ya esta listo para comenzar a desarrollar 

## Manejo de ramas del proyecto

- La rama `master` representa el sistema deployado, no hacer cambios en ella

- La rama `develop` tiene todos los cambios ya terminados pero que no estan deployados

- Para iniciar el desarrollo de una nueva funcion crear una rama desde `develop`

- Para seguimiento el nombre de la rama debe ser `SI-XX-(una breve descripcion de la tarea)`

- SI-XX es la Key que se encuentra en cada card de trelo

- Antes de empezar a desarrollar correr todos los tests y notificar si alguno fallo

## Migraciones de la DB
- Al iniciar el proyecto ya no se genera la DB automaticamente se tiene que correr el comando (dentro del contenedor)

- `python -m alembic upgrade head`

- Para agregar una nueva tabla a la DB importar el modelo correspondiente en el archivo `migrations/env.py:19`

- En el caso de haber hecho un cambio en una tabla o luego de haber creado una

- Correr el comando ` python -m alembic revision --autogenerate -m "Aca un comentario sobre de que fue la migracion" `

- Ejecutar la migracion `python -m alembic upgrade head`

- IMPORTANTE!!!!!!!!!!!!!!!!! Si se creo una migracion afuera del contenedor dar permisos al archivo de migracion

- En el caso de Linux `sudo chown -R usuario:usuario *` correr afuera del contenedor
