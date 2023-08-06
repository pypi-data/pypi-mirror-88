BEGIN TRANSACTION;  /* -*- coding: utf-8 -*- vim: expandtab sw=4 sts=4 si
*/

------------------------------- [ neue Sichten löschen ... [
DROP FUNCTION IF EXISTS recalculate_order(integer);
DROP VIEW IF EXISTS user_bookings_view;
DROP VIEW IF EXISTS latest_paypal_record_view;
DROP VIEW IF EXISTS booking_states_summary_view;
DROP VIEW IF EXISTS bookings_view;
DROP VIEW IF EXISTS booking_states_view;
DROP VIEW IF EXISTS payment_types_view;
DROP VIEW IF EXISTS articles_calculated_view;
DROP VIEW IF EXISTS articles_items_view;
DROP VIEW IF EXISTS orders_articles_view;
DROP VIEW IF EXISTS orders_view;

------------------------------- ] ... neue Sichten löschen ]

ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_id_pkey;

DROP TRIGGER IF EXISTS tr_orders_addmissing
  ON unitracc_orders;
--------------------------- [ Schutz der Hilfstabellen ... [
DROP TRIGGER IF EXISTS tr_disallow_changes
  ON unitracc_booking_states;
DROP TRIGGER IF EXISTS tr_disallow_changes
  ON unitracc_payment_types;

DROP FUNCTION IF EXISTS tf_disallow_changes();
DROP FUNCTION IF EXISTS tf_orders_addmissing();
--------------------------- ] ... Schutz der Hilfstabellen ]

------------------------ [ zurück zu den alten Feldern ... [
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_booking_state_fkey;

ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_payment_type_fkey;

ALTER TABLE unitracc_orders
  RENAME COLUMN order_id TO id;
ALTER TABLE unitracc_orders_articles
  DROP CONSTRAINT unitracc_orders_articles_order_id_fkey;
-- jetzt kann der Ergänzungsdatensatz aus unitracc_orders
-- wieder gelöscht werden:
DELETE FROM unitracc_orders
  WHERE id = 93 AND userid = '<unknown>';
ALTER TABLE unitracc_orders_articles
  RENAME COLUMN article_id TO id;
ALTER TABLE unitracc_orders_articles
  RENAME COLUMN order_id TO orderid;

ALTER TABLE unitracc_orders_paypal
  DROP CONSTRAINT unitracc_orders_paypal_pkey;
ALTER TABLE unitracc_orders_paypal
  RENAME COLUMN paypal_order_id TO id;

ALTER TABLE unitracc_orders
  ADD COLUMN booking_states_id integer;
ALTER TABLE unitracc_orders
  ADD COLUMN payment_type_id integer;

ALTER TABLE unitracc_booking_states
  DROP COLUMN state_description IF EXISTS;
--------- [ alte Felder per Trigger wiederbelegen ... [
CREATE OR REPLACE FUNCTION tf_orders_addmissing()
  RETURNS trigger AS
$BODY$begin
  if new.booking_states_id IS NULL then
    new.booking_states_id := CASE new.booking_state
                            WHEN 'new' THEN 1
                            WHEN 'paying' THEN 2
                            WHEN 'pending' THEN 3
                            WHEN 'accepted' THEN 4
                            WHEN 'declined' THEN 5
                            WHEN 'timeout' THEN 6
                            WHEN 'unknown' THEN 99
                          END;
  end if;
  if new.payment_type_id IS NULL then
    new.payment_type_id := CASE new.payment_type
                            WHEN 'prepayment' THEN 1
                            WHEN 'paypal' THEN 2
                          END;
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

UPDATE unitracc_orders
  SET booking_state = booking_state;
--------- ] ... alte Felder per Trigger wiederbelegen ]

ALTER TABLE unitracc_orders ALTER COLUMN booking_states_id SET NOT NULL;
ALTER TABLE unitracc_orders ALTER COLUMN booking_states_id SET DEFAULT 1;
ALTER TABLE unitracc_orders ALTER COLUMN payment_type_id SET NOT NULL;

DROP TRIGGER tr_orders_addmissing ON unitracc_orders;
DROP FUNCTION tf_orders_addmissing();
ALTER TABLE unitracc_orders DROP COLUMN booking_state;
ALTER TABLE unitracc_orders DROP COLUMN payment_type;

------------------------ ] ... zurück zu den alten Feldern ]

---------------------- [ alte Sichten wiederherstellen ... [
CREATE OR REPLACE VIEW booking_states_summary_view AS 
 SELECT s.id,
    s.booking_state,
    count(o.id) AS anzahl,
    max(o.date_booked) AS date_booked
   FROM unitracc_booking_states s
     JOIN unitracc_orders o ON o.booking_states_id = s.id
  GROUP BY s.id
  ORDER BY max(o.date_booked) DESC;
ALTER TABLE booking_states_summary_view
  OWNER TO "www-data";
COMMENT ON VIEW booking_states_summary_view
  IS 'Vorhandene Buchungen nach Zahlungs-/Buchungsstatus';

CREATE OR REPLACE VIEW user_bookings_view AS 
 SELECT o.id AS orderid,
    o.ordernr,
    o.userid,
    o.sessionid,
    p.payment_type,
    s.booking_state AS payment_status,
    o.date_booked,
    o.date_payed,
    g.group_id_,
    g.start,
    g.ends,
    o.additional_info,
    o.payment_type_id,
    o.booking_states_id,
    to_char(g.start::timestamp with time zone, 'DD.MM.YYYY'::text) AS start_ddmmyyyy,
    to_char(g.ends::timestamp with time zone, 'DD.MM.YYYY'::text) AS ends_ddmmyyyy
   FROM unitracc_orders o
     LEFT JOIN unitracc_orders_articles a ON a.orderid = o.id
     LEFT JOIN unitracc_payment_types p ON o.payment_type_id = p.id
     LEFT JOIN unitracc_booking_states s ON o.booking_states_id = s.id
     LEFT JOIN unitracc_groupmemberships g ON g.order_id = o.id
  ORDER BY o.id DESC;
ALTER TABLE user_bookings_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW latest_paypal_record_view AS 
 SELECT p.unitracc_orders_id,
        p.payment_status,
        p.pending_reason,
        p.reason_code, 
        p.payer_id,
        p.payer_email,
        p.payer_status,
        p.address_name,
        o.userid, 
        o.ordernr,
        p."timestamp",
        p.memo
   FROM unitracc_orders_paypal p
   JOIN unitracc_orders o ON p.unitracc_orders_id = o.id
  WHERE p."timestamp" IS NOT NULL
  ORDER BY p."timestamp" DESC;
ALTER TABLE latest_paypal_record_view
  OWNER TO "www-data";

DROP VIEW IF EXISTS orders_articles_view;
CREATE OR REPLACE VIEW orders_articles_view AS
 SELECT DISTINCT o.id AS orderid,
    o.ordernr,
    o.userid,
    o.sessionid,
    p.payment_type,
    s.booking_state,
    o.date_booked,
    o.date_payed,
    a.article_uid,
    a.article_title,
    a.id AS article_id,
    a.step,
    a.amount,
    a.amount_multiplied,
    a.group_id,
    g.start,
    g.ends,
    to_char(g.start::timestamp with time zone, 'DD.MM.YYYY'::text) AS start_ddmmyyyy,
    to_char(g.ends::timestamp with time zone, 'DD.MM.YYYY'::text) AS ends_ddmmyyyy,
    a.duration,
    a.quantity,
    a.vat_percent,
    o.la,
    a.discount_group,
    to_char(a.start, 'DD.MM.YYYY'::text) AS start_wanted,
    o.firstname,
    o.lastname,
    o.company,
    o.street,
    o.zip,
    o.city,
    o.country,
    o.additional_info,
    o.ip
   FROM unitracc_orders o
     LEFT JOIN unitracc_orders_articles a ON a.orderid = o.id
     LEFT JOIN unitracc_payment_types p ON o.payment_type_id = p.id
     LEFT JOIN unitracc_booking_states s ON o.booking_states_id = s.id
     LEFT JOIN unitracc_groupmemberships g ON g.order_id = o.id AND g.group_id_::text = a.group_id
  ORDER BY o.id DESC, a.id;
ALTER TABLE orders_articles_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW articles_calculated_view AS
  -- bei den berechneten Zeilen sind weit weniger Felder interessant:
  SELECT orderid,
         article_id,
         step,          -- Sortierkriterium
         article_title, -- hier keine UIDs
         vat_percent,
         amount_multiplied
    FROM orders_articles_view
   WHERE step > 1
   ORDER BY orderid DESC, -- wie in orders_articles_view
            step,
            article_id;
ALTER TABLE articles_calculated_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_calculated_view
  IS 'nur die berechneten Zeilen (Berechnungsgrundlage: siehe articles_items_view)';
---------------------- ] ... alte Sichten wiederherstellen ]


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
CREATE OR REPLACE FUNCTION recalculate_order
  (order_id integer)
  RETURNS TABLE (  -- wie von Sicht articles_calculated_view
          orderid           integer,
          article_id        integer,
          step              smallint,
          article_title     text,
          vat_percent       numeric,
          amount_multiplied numeric
  ) AS
$BODY$
DECLARE order_row unitracc_orders;
begin
  SELECT *
    INTO order_row
    FROM unitracc_orders
   WHERE id = order_id;
  IF order_row.dirty THEN
      RAISE NOTICE 'Neuberechung';
      -- bisherige Werte löschen:
      DELETE FROM unitracc_orders_articles a
       WHERE a.orderid = order_row.id
         AND a.step > 1;

      -- (5) etwaige Rabatte
      INSERT INTO unitracc_orders_articles
        (orderid, vat_percent, article_title, amount_multiplied, step)
      SELECT v.orderid,
             v.vat_percent,
             v.article_title,
             v.amount_multiplied,
             v.step  -- 5
        FROM articles_discount_view v
       WHERE v.orderid = order_row.id
         AND v.amount_multiplied != 0
         AND v.la = order_row.la;

      -- (7) Nettosumme (hier nur informativ):
      INSERT INTO unitracc_orders_articles
        (orderid, article_title, amount_multiplied, step)
      SELECT a.orderid,
             t.step_text AS article_title,
             sum(a.amount_multiplied) AS amount_multiplied,
             7 as step
        FROM unitracc_orders_articles a
             JOIN unitracc_orders                 o ON o.id = a.orderid
             JOIN unitracc_orders_calc_step_texts t ON t.la = o.la
                                                   AND t.step = 7
       WHERE a.orderid = order_row.id
         AND a.step < 7  -- Artikel und Rabatte
       GROUP BY a.orderid,
                t.step_text;

      -- (10) Mehrwertsteuer:
      INSERT INTO unitracc_orders_articles
        (orderid, vat_percent, article_title, amount_multiplied, step)
      SELECT v.orderid,
             v.vat_percent,
             v.article_title,
             v.amount_multiplied,
             v.step  -- 10
        FROM articles_vat_view v
       WHERE v.orderid = order_row.id;
      WITH t AS (
        SELECT a.orderid,
               sum(a.amount_multiplied) AS amount_multiplied
          FROM unitracc_orders_articles a
         WHERE a.orderid = order_row.id
           AND a.step = 10
         GROUP BY a.orderid
      )
      UPDATE unitracc_orders o
         SET vat_total = t.amount_multiplied
        FROM t
       WHERE o.id = t.orderid;

       -- (15) Gesamtsumme:
      INSERT INTO unitracc_orders_articles
        (orderid, article_title, amount_multiplied, step)
      SELECT a.orderid,
             t.step_text AS article_title,
             sum(a.amount_multiplied) AS amount_multiplied,
             15 as step
        FROM unitracc_orders_articles a
             JOIN unitracc_orders                 o ON o.id = a.orderid
             JOIN unitracc_orders_calc_step_texts t ON t.la = o.la
                                                   AND t.step = 15
       WHERE a.orderid = order_row.id
         AND a.step BETWEEN 7 AND 10  -- Nettosumme und Mehrwertsteuer
       GROUP BY a.orderid,
                t.step_text;

      -- dirty-Flag zurücksetzen:
      UPDATE unitracc_orders
         SET dirty = false
       WHERE id = order_row.id;
  ELSE
      RAISE NOTICE 'Verwende gespeicherte Werte';
  END IF;
  RETURN QUERY
      SELECT *
        FROM articles_calculated_view v
       WHERE v.orderid = order_row.id;
end;$BODY$
  LANGUAGE plpgsql VOLATILE;

CREATE OR REPLACE VIEW bookings_view AS
 SELECT o.id,
        o.ordernr,
        s.booking_state,
        t.payment_type,
        o.userid,
        o.firstname,
        o.lastname,
        o.company,
        o.date_booked
   FROM unitracc_orders o
        JOIN unitracc_booking_states s ON o.booking_states_id = s.id
        JOIN unitracc_payment_types  t ON o.payment_type_id = t.id
  ORDER BY o.id DESC;
ALTER TABLE bookings_view
  OWNER TO "www-data";
COMMENT ON VIEW bookings_view
  IS 'Sicht zum schnelleren Überblick über vorhandene Buchungen';

CREATE OR REPLACE VIEW articles_items_view AS
  SELECT *
    FROM orders_articles_view
   WHERE step = 1
   ORDER BY orderid DESC, -- wie in orders_articles_view
            article_id;
ALTER TABLE articles_items_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_items_view
  IS 'nur die bestellten Artikel selbst (die Berechnungsgrundlage); siehe auch articles_calculated_view';

CREATE OR REPLACE VIEW articles_calculated_view AS
  -- bei den berechneten Zeilen sind weit weniger Felder interessant:
  SELECT orderid,
         article_id,
         step,          -- Sortierkriterium
         article_title, -- hier keine UIDs
         vat_percent,
         amount_multiplied
    FROM orders_articles_view
   WHERE step > 1
   ORDER BY orderid DESC, -- wie in orders_articles_view
            step,
            article_id;
ALTER TABLE articles_calculated_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_calculated_view
  IS 'nur die berechneten Zeilen (Berechnungsgrundlage: siehe articles_items_view)';


CREATE OR REPLACE VIEW orders_view AS
 SELECT o.id orderid,
        o.ordernr,
        o.userid,
        o.sessionid,
        o.payment_type_id,
        p.payment_type,
        o.booking_states_id,
        s.booking_state AS payment_status,
        o.date_booked,
        o.date_payed,
        o.additional_info,
        -- neu ab März 2018:
        o.la,
        CASE
            WHEN s.booking_state IN ('new', 'pending', 'paying') THEN
                'new'
            WHEN s.booking_state IN ('declined', 'timeout') THEN
                'failed'
            WHEN s.booking_state IN ('accepted') THEN
                'paid'
            ELSE
                'other'
        END AS payment_status_category,
        o.dirty,
        -- wenn dirty, bedürfen die folgenden drei der Aktualisierung:
        o.net_total,
        o.vat_total,
        o.total,
        -- sonstiges:
        o.paypal_allowed,
        o.company,
        o.street,
        o.zip,
        o.city,
        o.country,
        o.firstname,
        o.lastname,
        o.ip,
        o.currency
   FROM unitracc_orders o
        LEFT JOIN unitracc_payment_types  p ON o.payment_type_id = p.id
        LEFT JOIN unitracc_booking_states s ON o.booking_states_id = s.id
  ORDER BY o.id DESC;
ALTER TABLE orders_view
  OWNER TO "www-data";


-- (zurückgesetzt auf false wird das Feld
--  derzeit in Anwendungscode)
CREATE OR REPLACE FUNCTION tf_articles_dirty()
  RETURNS trigger AS
$BODY$begin
  if TG_OP = 'DELETE' then
    if old.step = 1 then
      UPDATE unitracc_orders
        SET dirty = true
        WHERE id = old.orderid;
    end if;
  else
      if new.step = 1 then
            UPDATE unitracc_orders
              SET dirty = true
              WHERE id = new.orderid;
/* automatische Generierung der Gruppen-ID funktioniert noch nicht:
          if new.article_uid is not null and
             (new.group_id = '<auto>'
              or (TG_OP = 'INSERT' and new.group_id IS NULL)
              or (TG_OP = 'UPDATE' and new.group_id IS NULL
                                   and old.group_id IS NULL)
              )
          then
              new.group_id := CASE
                                  WHEN  new.discount_group = 'course' THEN
                                      'group_' || new.article_uid || '_learner'
                                  ELSE NULL
                              END;
          end if;
*/
      else
          if new.step = 7 then  -- Nettosumme
              UPDATE unitracc_orders
                SET net_total = new.amount_multiplied
                WHERE id = new.orderid;
          else
              -- vat_total wird in der Funktion recalculate_order
              -- direkt gesetzt
              if new.step = 15 then  -- Gesamtsumme
                  UPDATE unitracc_orders
                    SET total = new.amount_multiplied
                    WHERE id = new.orderid;
              end if;
          end if;
      end if;
  end if;
  return new;
end;$BODY$
  LANGUAGE plpgsql;
ALTER FUNCTION tf_articles_dirty()
  OWNER TO "www-data";


END;
