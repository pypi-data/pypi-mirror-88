BEGIN;
ALTER TABLE unitracc_orders
  ADD COLUMN paypal_id text;
ALTER TABLE unitracc_orders
  ADD COLUMN paypal_allowed boolean DEFAULT true;
ALTER TABLE unitracc_orders
  ADD COLUMN currency character varying(10);
END;
