-- Create schema for manufacturer worker application
CREATE SCHEMA IF NOT EXISTS manufacturers

-- Create tables for manufacturer worker application

-- Create manufacturers table
CREATE TABLE IF NOT EXISTS manufacturers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(255) NOT NULL,
    nit VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    codigo_pais VARCHAR(2) NOT NULL,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_nombre_nit UNIQUE (nombre, nit)
);

-- Create errors table to track validation and processing errors
CREATE TABLE IF NOT EXISTS errors (
    id SERIAL PRIMARY KEY,
    transaction_id UUID NOT NULL,
    batch_number INTEGER NOT NULL,
    line_number INTEGER NOT NULL,
    description TEXT NOT NULL,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on transaction_id to improve error lookup performance
CREATE INDEX IF NOT EXISTS idx_errors_transaction_id ON errors(transaction_id);