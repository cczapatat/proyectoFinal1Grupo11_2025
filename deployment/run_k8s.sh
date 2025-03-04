#!/bin/bash

echo "Inicio Run K8s\n"

kubectl apply -f secrets.yaml

kubectl apply -f k8s-base-layer-deployment.yaml

kubectl apply -f k8s-ingress-deloyment.yaml

echo "Fin Run K8s\n"