BEGIN TRANSACTION;  /* -*- coding: utf-8 -*- vim: expandtab sw=4 sts=4 si
*/
DELETE FROM unitracc_orders_calc_step_texts WHERE la = 'en_GB';
DELETE FROM unitracc_discount_group_texts WHERE la = 'en_GB';
DELETE FROM unitracc_vat_texts WHERE la = 'en_GB';

DELETE FROM unitracc_language WHERE la = 'en_GB';





-------------------------- [ definierter Zustand für Constraints ... [
ALTER TABLE "unitracc_orders_calc_step_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_booking_step_texts_la_fkey";
ALTER TABLE "unitracc_discount_group_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_discount_group_texts_la_fkey";
ALTER TABLE "unitracc_orders"
  DROP CONSTRAINT IF EXISTS "unitracc_orders_la_fkey";
ALTER TABLE "unitracc_vat_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_vat_texts_la_fkey";
ALTER TABLE "unitracc_orders_calc_step_texts"
  ADD CONSTRAINT "unitracc_booking_step_texts_la_fkey"
  FOREIGN KEY (la) REFERENCES unitracc_language(la)
  ON UPDATE CASCADE
  ON DELETE NO ACTION;
ALTER TABLE "unitracc_discount_group_texts"
  ADD CONSTRAINT "unitracc_discount_group_texts_la_fkey"
  FOREIGN KEY (la) REFERENCES unitracc_language(la)
  ON UPDATE CASCADE
  ON DELETE NO ACTION;
ALTER TABLE "unitracc_orders"
  ADD CONSTRAINT "unitracc_orders_la_fkey"
  FOREIGN KEY (la) REFERENCES unitracc_language(la)
  ON UPDATE CASCADE
  ON DELETE NO ACTION;
ALTER TABLE "unitracc_vat_texts"
  ADD CONSTRAINT "unitracc_vat_texts_la_fkey"
  FOREIGN KEY (la) REFERENCES unitracc_language(la)
  ON UPDATE CASCADE
  ON DELETE NO ACTION;
-------------------------- ] ... definierter Zustand für Constraints ]

ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_la_check_2;

-------------------------------- [ Trigger-Funktion zurücksetzen ... [
DROP TRIGGER IF EXISTS tr_orders_addmissing
  ON unitracc_orders;
CREATE OR REPLACE FUNCTION tf_orders_addmissing()
  RETURNS trigger AS
$BODY$begin
  -- neues Feld booking_state, als Ersatz für booking_states_id:
  if new.booking_state IS NULL then
    new.booking_state := CASE new.booking_states_id
                            WHEN 1 THEN 'new'
                            WHEN 2 THEN 'paying'
                            WHEN 3 THEN 'pending'
                            WHEN 4 THEN 'accepted'
                            WHEN 5 THEN 'declined'
                            WHEN 6 THEN 'timeout'
                            WHEN 99 THEN 'unknown'
                          END;
  end if;
  -- neues Feld payment_type, als Ersatz für payment_type_id:
  if new.payment_type IS NULL then
    new.payment_type := CASE new.payment_type_id
                            WHEN 1 THEN 'prepayment'
                            WHEN 2 THEN 'paypal'
                        END;
  end if;
  new.la = CASE new.la
                WHEN 'de_DE' THEN 'de'
                WHEN 'en_US' THEN 'en'
           ELSE new.la
           END; 
  return new;
end;$BODY$
  LANGUAGE plpgsql;
ALTER FUNCTION tf_orders_addmissing()
  OWNER TO "www-data";
-------------------------------- ] ... Trigger-Funktion zurücksetzen ]

------------------------------ [ wieder zweistellige Sprachcodes ... [
UPDATE unitracc_language
  SET la = 'de'
  WHERE la = 'de_DE';
UPDATE unitracc_language
  SET la = 'en'
  WHERE la = 'en_US';

CREATE TRIGGER tr_orders_addmissing
  BEFORE INSERT OR UPDATE
  ON unitracc_orders
  FOR EACH ROW  -- sonst wäre NEW undefiniert
  EXECUTE PROCEDURE tf_orders_addmissing();

ALTER TABLE unitracc_language
  DROP CONSTRAINT IF EXISTS unitracc_language_la_check_5;
ALTER TABLE unitracc_language
  ALTER COLUMN la TYPE VARCHAR(2);
------------------------------ ] ... wieder zweistellige Sprachcodes ]

------------------------- [ alte Fremdschlüssel wiederherstellen ... [
ALTER TABLE "unitracc_orders_calc_step_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_booking_step_texts_la_fkey";
ALTER TABLE "unitracc_discount_group_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_discount_group_texts_la_fkey";
ALTER TABLE "unitracc_orders"
  DROP CONSTRAINT IF EXISTS "unitracc_orders_la_fkey";
ALTER TABLE "unitracc_vat_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_vat_texts_la_fkey";

ALTER TABLE "unitracc_orders_calc_step_texts"
  ADD CONSTRAINT "unitracc_booking_step_texts_la_fkey"
  FOREIGN KEY (la) REFERENCES unitracc_language(la)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;
ALTER TABLE "unitracc_discount_group_texts"
  ADD CONSTRAINT "unitracc_discount_group_texts_la_fkey"
  FOREIGN KEY (la) REFERENCES unitracc_language(la)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;
ALTER TABLE "unitracc_orders"
  ADD CONSTRAINT "unitracc_orders_la_fkey"
  FOREIGN KEY (la) REFERENCES unitracc_language(la)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;
ALTER TABLE "unitracc_vat_texts"
  ADD CONSTRAINT "unitracc_vat_texts_la_fkey"
  FOREIGN KEY (la) REFERENCES unitracc_language(la)
  ON UPDATE NO ACTION
  ON DELETE NO ACTION;
------------------------- ] ... alte Fremdschlüssel wiederherstellen ]

END;
