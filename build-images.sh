#!/bin/bash

# Validar que se proporcione el tag como parámetro
if [ -z "$1" ]; then
    echo "Error: Debe proporcionar un tag como parámetro"
    echo "Uso: ./build-images.sh <tag>"
    exit 1
fi

TAG=$1
REGISTRY="us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1"

# Lista de servicios a construir
services="document_manager manufacture_api manufacturers_worker massive_worker order product seller stocks_api stocks_worker stores user_session_manager"

# Función para construir y publicar imagen
build_and_push() {
    service=$1
    echo "Building $service..."
    
    # Copiar credenciales
    cp data_app/credentials.json $service/credentials.json
    
    # Cambiar al directorio del servicio
    cd $service
    
    # Construir imagen
    docker build -t "$REGISTRY/$service:$TAG" .
    
    # Publicar imagen
    #docker push "$REGISTRY/$service:$TAG"
    
    # Volver al directorio raíz y limpiar credenciales
    cd ..
    rm $service/credentials.json
    
    echo "Completed building $service"
}

# Iterar sobre cada servicio
for service in $services
do
    build_and_push $service
done

echo "All images have been built and pushed with tag: $TAG"
