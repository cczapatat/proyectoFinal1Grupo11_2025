FROM node:18.20.8 AS builder

ENV NG_CLI_ANALYTICS=false
ENV NG_CACHE=false

WORKDIR /app

# Configurar variables de entorno para optimizar memoria
ENV NODE_OPTIONS="--max-old-space-size=4096" \
    NPM_CONFIG_UPDATE_NOTIFIER=false \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_AUDIT=false \
    NPM_CONFIG_LOGLEVEL=error \
    NODE_ENV=production

# Copiar solo los archivos necesarios para la instalación
COPY package*.json ./

# Instalar dependencias con límites de memoria
RUN npm ci --quiet --no-optional --no-fund --no-audit --unsafe-perm=true --max-old-space-size=2048

# Copiar el resto de archivos y construir con límites de memoria
COPY . .
RUN NG_CACHE=false npx --max-old-space-size=2048 --max-workers=2 ng build --configuration production --no-progress --verbose --build-optimizer=false --named-chunks=false --source-map=false

# Etapa de producción
FROM --platform=linux/amd64 node:18.20.8-slim

# Configurar variables de entorno para npm en producción
ENV NPM_CONFIG_UPDATE_NOTIFIER=false \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_AUDIT=false \
    NPM_CONFIG_LOGLEVEL=error \
    NODE_ENV=production

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist/web-smartstock ./dist/web-smartstock
COPY --from=builder /app/server.js ./

EXPOSE 5000
CMD ["node", "server.js"]