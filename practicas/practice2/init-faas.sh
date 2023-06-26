#!/bin/bash

# Assuming minikube is already running (Windows terminal) and Docker is running (Docker Desktop)
# All the following commands are executed in Git Bash (Windows terminal)

# Custom limits and timeouts for OpenFaaS. These values are set to avoid timeouts when deploying large functions, such as SAM-Segmentation with CPU.
export TIMEOUT=10m
export HARD_TIMEOUT=10m2s

# INSTALL ARKADE AND OPENFAAS CLI.
# Additional flags are set to avoid timeouts when deploying large functions, such as SAM-Segmentation with CPU.
curl -sLS https://get.arkade.dev | sh
arkade install openfaas \
    --set gateway.upstreamTimeout=$TIMEOUT \
    --set gateway.writeTimeout=$HARD_TIMEOUT \
    --set gateway.readTimeout=$HARD_TIMEOUT \
    --set faasnetes.writeTimeout=$HARD_TIMEOUT \
    --set faasnetes.readTimeout=$HARD_TIMEOUT \
    --set queueWorker.ackWait=$TIMEOUT
curl -SLsf https://cli.openfaas.com | sh

# FORWARD PORTS. For whatever reason, this order doesn't always work and need to be executed manually.
kubectl rollout status -n openfaas deploy/gateway
kubectl port-forward -n openfaas svc/gateway 8080:8080 &

# LOGIN TO OPENFAAS
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o  jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
echo -n $PASSWORD | faas-cli login --username admin --password-stdin

# LOGIN TO DOCKER HUB IN ORDER TO BE ABLE TO BUILD AND DEPLOY MY OWN FUNCTIONS AS DOCKER CONTAINERS (assuming docker's password variable is set). Only during development.
# echo -n $DOCKER_PASSWORD | docker login --username modejota --password-stdin

# DEPLOY FUNCTIONS
faas-cli store deploy face-detect-pigo
faas-cli store deploy face-detect-opencv
faas-cli deploy -f basic-face-detection.yml
faas-cli deploy -f cnn-face-detection.yml
faas-cli deploy -f sam-segmentation.yml
faas-cli deploy -f sam-segmentation-light.yml