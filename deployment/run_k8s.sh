#!/bin/bash

echo "Start Run K8s\n"

kubectl apply -f secrets.yaml

kubectl apply -f k8s-base-layer-deployment.yaml

kubectl apply -f k8s-ingress-deployment.yaml

echo "End Run K8s\n"