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

```shell
cp data_app/credentials.json stocks_api/credentials.json && cd stocks_api && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/stocks_api:1.0.0 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/stocks_api:1.0.0 && \
cd .. && rm stocks_api/credentials.json
```

```shell
cp data_app/credentials.json stocks_worker/credentials.json && cd stocks_worker && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/stocks_worker:1.0.1 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/stocks_worker:1.0.1 && \
cd .. && rm stocks_worker/credentials.json
```

```shell
cp data_app/credentials.json order/credentials.json && cd order && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/order:1.0.2 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/order:1.0.2 && \
cd .. && rm order/credentials.json
```

```shell
cp data_app/credentials.json stores/credentials.json && cd stores && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/stores:1.0.0 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/stores:1.0.0 && \
cd .. && rm stores/credentials.json
```

```shell
cp data_app/credentials.json product/credentials.json && cd product && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/product:1.0.0 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/product:1.0.0 && \
cd .. && rm product/credentials.json
```

```shell
cp data_app/credentials.json seller/credentials.json && cd seller && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/seller:1.0.0 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/seller:1.0.0 && \
cd .. && rm seller/credentials.json
```

```shell
cp data_app/credentials.json user_session_manager/credentials.json && cd user_session_manager && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/user_session_manager:1.0.1 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/user_session_manager:1.0.1 && \
cd .. && rm user_session_manager/credentials.json
```

```shell
cp data_app/credentials.json client/credentials.json && cd client && \
docker build -t us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/client:1.0.1 . && \
docker push us-central1-docker.pkg.dev/proyectofinalmiso2025/repositorio-proyecto-final1/client:1.0.1 && \
cd .. && rm client/credentials.json
```
