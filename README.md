# proyectoFinal1Grupo11_2025

## Builder Images

```shell
cp data_app/credentials.json manufacture_api/credentials.json && cd manufacture_api && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/manufacture_api:1.0.5 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/manufacture_api:1.0.5 && \
cd .. && rm manufacture_api/credentials.json
```

```shell
cp data_app/credentials.json manufacturers_worker/credentials.json && cd manufacturers_worker && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/manufacturers_worker:1.0.5 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/manufacturers_worker:1.0.5 && \
cd .. && rm manufacturers_worker/credentials.json
```

```shell
cp data_app/credentials.json document_manager/credentials.json && cd document_manager && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/document_manager:1.0.5 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/document_manager:1.0.5 && \
cd .. && rm document_manager/credentials.json
```

```shell
cp data_app/credentials.json massive_worker/credentials.json && cd massive_worker && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/massive_worker:1.0.9 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/massive_worker:1.0.9 && \
cd .. && rm massive_worker/credentials.json
```
