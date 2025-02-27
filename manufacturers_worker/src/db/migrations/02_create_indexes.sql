-- Create additional indexes and constraints for performance

-- Create individual indexes on nombre and nit for faster lookups
CREATE INDEX IF NOT EXISTS idx_manufacturers_nombre ON manufacturers(nombre);
CREATE INDEX IF NOT EXISTS idx_manufacturers_nit ON manufacturers(nit);

-- Create index for batch lookup in errors table
CREATE INDEX IF NOT EXISTS idx_errors_batch ON errors(batch_number);

-- Comment: These indexes will improve query performance when looking up manufacturers
-- by name or NIT, and when filtering errors by batch number