BEGIN TRANSACTION;  /* -*- coding: utf-8 -*- vim: expandtab sw=4 sts=4 si

Verbesserungen gegenüber update-0003.sql:
- für Formatierung durch Datenbank muß der la-Wert ein la_LA-Wert sein
  (de --> de_DE, en zunächst --> en_US, später auch en_GB)
*/
/*
Wenn unitracc_order.dirty gesetzt ist, werden folgende zugeordnete
Datensätze in unitracc_orders_articles neu erzeugt:
   step  5 -- etwaige Rabatte
   step  7 -- Nettosumme
   step 10 -- Mehrwertsteuer
   step 15 -- Gesamtsumme

Für Nettosumme (net_total) und Gesamtsumme (total) werden die entsprechende
Werte durch die Triggerfunktion ... aktualisiert; die Aufsummierung der
Mehrwertsteuerbeträge (es ist möglich, daß Artikel mit unterschiedlichen Sätzen
verarbeitet werden müssen) in vat_total geschieht hier direkt.

 */

------------------------------------------ [ Fremdschlüssel umwandeln ... [
ALTER TABLE "unitracc_orders_calc_step_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_booking_step_texts_la_fkey";
ALTER TABLE "unitracc_discount_group_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_discount_group_texts_la_fkey";
ALTER TABLE "unitracc_orders"
  DROP CONSTRAINT IF EXISTS "unitracc_orders_la_fkey";
ALTER TABLE "unitracc_vat_texts"
  DROP CONSTRAINT IF EXISTS "unitracc_vat_texts_la_fkey";

ALTER TABLE unitracc_language
  ALTER COLUMN la TYPE TEXT;
ALTER TABLE unitracc_language
  ADD CONSTRAINT unitracc_language_la_check_5
  CHECK (length(la) <= 5);

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

UPDATE unitracc_language
  SET la = 'de_DE'
  WHERE la = 'de';
UPDATE unitracc_language
  SET la = 'en_US'
  WHERE la = 'en';
------------------------------------------ ] ... Fremdschlüssel umwandeln ]

------------------------------------------------ [ en_GB unterstützen ... [
INSERT INTO unitracc_language
  (la)
VALUES ('en_GB');

INSERT INTO "unitracc_orders_calc_step_texts"
  (text_id, la, step, step_text)
VALUES
   (72, 'en_GB', 7, 'Net amount'),
  (152, 'en_GB', 15, 'Total amount');

INSERT INTO unitracc_vat_texts
SELECT 'en_GB' AS la,
       text_normal
  FROM unitracc_vat_texts
 WHERE la = 'en_US';

INSERT INTO unitracc_discount_group_texts
SELECT discount_group,
       'en_GB' AS la,
       text_normal,
       text_with_vat,
       text_zero_vat
  FROM unitracc_discount_group_texts
 WHERE la = 'en_US';
-- DELETE FROM unitracc_discount_group_texts WHERE la = 'en_GB';
-- DELETE FROM unitracc_orders_calc_step_texts WHERE la = 'en_GB';
------------------------------------------------ ] ... en_GB unterstützen ]

--------------------- [ de, en temporär ermöglichen ... [
INSERT INTO unitracc_language (la)
VALUES ('de'), ('en');


/*
    TABLE "unitracc_orders_calc_step_texts" CONSTRAINT "unitracc_booking_step_texts_la_fkey" FOREIGN KEY (la) REFERENCES unitracc_language(la)
    TABLE "unitracc_discount_group_texts" CONSTRAINT "unitracc_discount_group_texts_la_fkey" FOREIGN KEY (la) REFERENCES unitracc_language(la)
    TABLE "unitracc_orders" CONSTRAINT "unitracc_orders_la_fkey" FOREIGN KEY (la) REFERENCES unitracc_language(la)
    TABLE "unitracc_vat_texts" CONSTRAINT "unitracc_vat_texts_la_fkey" FOREIGN KEY (la) REFERENCES unitracc_language(la)
*/

CREATE OR REPLACE VIEW articles_calculated_view AS
  -- bei den berechneten Zeilen sind weit weniger Felder interessant:
  SELECT order_id,
         article_id,
         step,          -- Sortierkriterium
         article_title, -- hier keine UIDs
         vat_percent,
         amount_multiplied,
         to_char(vat_percent,                 '990.0%') AS vat_percent_formatted,
         to_char(amount_multiplied, '9,999,999,990.00') AS amount_formatted
    FROM orders_articles_view
   WHERE step > 1
   ORDER BY order_id DESC, -- wie in orders_articles_view
            step,
            article_id;
ALTER TABLE articles_calculated_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_calculated_view
  IS 'nur die berechneten Zeilen (Berechnungsgrundlage: siehe articles_items_view); incl. formatierter Ausgabe der Zahlenwerte';

DROP FUNCTION IF EXISTS recalculate_order(integer);
CREATE OR REPLACE FUNCTION recalculate_order
  (given_order_id integer)
  RETURNS TABLE (  -- wie von Sicht articles_calculated_view
          order_id          integer,
          article_id        integer,
          step              smallint,
          article_title     text,
          vat_percent       numeric,
          amount_multiplied numeric,
          vat_percent_formatted text,
          amount_formattet  text
  ) AS
$BODY$
DECLARE order_row unitracc_orders;
begin
  SELECT *
    INTO order_row
    FROM unitracc_orders o
   WHERE o.order_id = given_order_id;
  IF order_row.la IS NOT NULL THEN
      PERFORM set_config('LC_NUMERIC', order_row.la, true);
  END IF;
  IF order_row.dirty THEN
      RAISE NOTICE 'Neuberechung';
      -- bisherige Werte löschen:
      DELETE FROM unitracc_orders_articles a
       WHERE a.order_id = order_row.order_id
         AND a.step > 1;

      -- (5) etwaige Rabatte
      INSERT INTO unitracc_orders_articles
        (order_id, vat_percent, article_title, amount_multiplied, step)
      SELECT v.order_id,
             v.vat_percent,
             v.article_title,
             v.amount_multiplied,
             v.step  -- 5
        FROM articles_discount_view v
       WHERE v.order_id = order_row.order_id
         AND v.amount_multiplied != 0
         AND v.la = order_row.la;

      -- (7) Nettosumme (hier nur informativ):
      INSERT INTO unitracc_orders_articles
        (order_id, article_title, amount_multiplied, step)
      SELECT a.order_id,
             t.step_text AS article_title,
             sum(a.amount_multiplied) AS amount_multiplied,
             7 as step
        FROM unitracc_orders_articles a
             JOIN unitracc_orders                 o ON o.order_id = a.order_id
             JOIN unitracc_orders_calc_step_texts t ON t.la = o.la
                                                   AND t.step = 7
       WHERE a.order_id = order_row.order_id
         AND a.step < 7  -- Artikel und Rabatte
       GROUP BY a.order_id,
                t.step_text;

      -- (10) Mehrwertsteuer:
      INSERT INTO unitracc_orders_articles
        (order_id, vat_percent, article_title, amount_multiplied, step)
      SELECT v.order_id,
             v.vat_percent,
             v.article_title,
             v.amount_multiplied,
             v.step  -- 10
        FROM articles_vat_view v
       WHERE v.order_id = order_row.order_id;
      WITH t AS (
        SELECT a.order_id,
               sum(a.amount_multiplied) AS amount_multiplied
          FROM unitracc_orders_articles a
         WHERE a.order_id = order_row.order_id
           AND a.step = 10
         GROUP BY a.order_id
      )
      UPDATE unitracc_orders o
         SET vat_total = t.amount_multiplied
        FROM t
       WHERE o.order_id = t.order_id;

       -- (15) Gesamtsumme:
      INSERT INTO unitracc_orders_articles
        (order_id, article_title, amount_multiplied, step)
      SELECT a.order_id,
             t.step_text AS article_title,
             sum(a.amount_multiplied) AS amount_multiplied,
             15 as step
        FROM unitracc_orders_articles a
             JOIN unitracc_orders                 o ON o.order_id = a.order_id
             JOIN unitracc_orders_calc_step_texts t ON t.la = o.la
                                                   AND t.step = 15
       WHERE a.order_id = order_row.order_id
         AND a.step BETWEEN 7 AND 10  -- Nettosumme und Mehrwertsteuer
       GROUP BY a.order_id,
                t.step_text;

      -- dirty-Flag zurücksetzen:
      UPDATE unitracc_orders u
         SET dirty = false
       WHERE u.order_id = order_row.order_id;
  ELSE
      RAISE NOTICE 'Verwende gespeicherte Werte';
  END IF;
  RETURN QUERY
      SELECT *
        FROM articles_calculated_view v
       WHERE v.order_id = order_row.order_id;
end;$BODY$
  LANGUAGE plpgsql VOLATILE;
ALTER FUNCTION recalculate_order(integer)
  OWNER TO "www-data";

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
                WHEN 'de' THEN 'de_DE'
                WHEN 'en' THEN 'en_US'
           ELSE new.la
           END; 
  if TG_OP = 'UPDATE' then
      if new.la != old.la then
          new.dirty = true;
      end if;
  end if;
  return new;
end;$BODY$
  LANGUAGE plpgsql;
ALTER FUNCTION tf_orders_addmissing()
  OWNER TO "www-data";
CREATE TRIGGER tr_orders_addmissing
  BEFORE INSERT OR UPDATE
  ON unitracc_orders
  FOR EACH ROW  -- sonst wäre NEW undefiniert
  EXECUTE PROCEDURE tf_orders_addmissing();


END;
