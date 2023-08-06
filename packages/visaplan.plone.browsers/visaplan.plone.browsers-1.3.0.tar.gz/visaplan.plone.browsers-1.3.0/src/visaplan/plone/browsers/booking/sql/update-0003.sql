BEGIN TRANSACTION;  /* -*- coding: utf-8 -*- vim: expandtab sw=4 sts=4 si
Bereinigung doppelter Buchungsdatensätze in der Datenbank,
und Etablierung eines Indexes!
(https://stackoverflow.com/a/9260906/1051649)

Außerdem:
- statt  payment_type_id (int)
  direkt payment_type (text) setzen
  (erübrigt zukünftig JOINs)
- statt  booking_states_id (int)
  direkt booking_state (text) setzen
  (erübrigt zukünftig JOINs)
- beide neuen Felder werden über Trigger gefüllt, sodaß
  der Programmcode peu à peu aktualisiert werden kann
  (es ist *nicht* nötig, beide Werte anzugeben!)
*/

--------------------------- [ Konsolidierung von unitracc_orders ... [
------------------------ [ unitracc_orders: Primärschlüssel ... [
DELETE FROM  unitracc_orders o1
       USING unitracc_orders o2
 WHERE     o1.id = o2.id
       -- Systemspalte ctid:
       AND o1.ctid < o2.ctid
       -- Datenspalten:
       AND o1.ordernr = o2.ordernr
       AND o1.userid = o2.userid
       AND o1.sessionid = o2.sessionid
       AND o1.payment_type_id = o2.payment_type_id
       AND o1.booking_states_id = o2.booking_states_id
       AND o1.ip = o2.ip
       AND o1.date_booked = o2.date_booked
       AND o1.date_payed = o2.date_payed
       AND (o1.firstname = o2.firstname
            OR (o1.firstname IS NULL AND o2.firstname IS NULL))
       AND (o1.lastname = o2.lastname
            OR (o1.lastname IS NULL AND o2.lastname IS NULL))
       AND (o1.company = o2.company
            OR (o1.company IS NULL AND o2.company IS NULL))
       AND (o1.street = o2.street
            OR (o1.street IS NULL AND o2.street IS NULL))
       AND (o1.zip = o2.zip
            OR (o1.zip IS NULL AND o2.zip IS NULL))
       AND (o1.city = o2.city
            OR (o1.city IS NULL AND o2.city IS NULL))
       AND (o1.country = o2.country
            OR (o1.country IS NULL AND o2.country IS NULL))
       AND (o1.additional_info = o2.additional_info
            OR (o1.additional_info IS NULL AND o2.additional_info IS NULL))
       AND (o1.paypal_id = o2.paypal_id
            OR (o1.paypal_id IS NULL AND o2.paypal_id IS NULL))
       AND (o1.paypal_allowed = o2.paypal_allowed
            OR (o1.paypal_allowed IS NULL AND o2.paypal_allowed IS NULL))
       AND (o1.currency = o2.currency
            OR (o1.currency IS NULL AND o2.currency IS NULL))
 RETURNING o1.id, o1.ctid, o1.ordernr, o1.userid, o1.payment_type_id, o1.booking_states_id, o1.date_payed, o1.date_booked;

-- hier zur Sicherstellung der Eindeutigkeit;
-- weiter unten wird die Primärschlüsselspalte umbenannt:
/*
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_id_pkey PRIMARY KEY (id);
*/
------------------------ ] ... unitracc_orders: Primärschlüssel ]

------------------- [ Dokumentationsspalte für Hilfstabelle ... [
ALTER TABLE unitracc_booking_states
  DROP COLUMN IF EXISTS state_description;
ALTER TABLE unitracc_booking_states
  ADD COLUMN state_description TEXT;
UPDATE unitracc_booking_states
  SET state_description = 'Neuer Auftrag, noch nicht abgeschickt und noch ohne Buchungsnummer'
  WHERE booking_state = 'new';
UPDATE unitracc_booking_states
  SET state_description = 'Auftrag abgeschickt (vermutlich Zahlungsart Vorkasse)'
  WHERE booking_state = 'paying';
UPDATE unitracc_booking_states
  SET state_description = 'Probleme bei der Zahlung; noch nicht abgeschlossen (vermutlich nur bei Paypal-Zahlungen)'
  WHERE booking_state = 'pending';
UPDATE unitracc_booking_states
  SET state_description = 'Die Zahlung ist eingegangen'
  WHERE booking_state = 'accepted';
UPDATE unitracc_booking_states
  SET state_description = 'Die Zahlung ist fehlgeschlagen (Paypal-Status Denied, Failed oder Voided)'
  WHERE booking_state = 'declined';
UPDATE unitracc_booking_states
  SET state_description = 'Bearbeitungszeit überschritten (Paypal)'
  WHERE booking_state = 'timeout';
UPDATE unitracc_booking_states
  SET state_description = 'Unbekannter Status (Paypal)'
  WHERE booking_state = 'unknown';
------------------- ] ... Dokumentationsspalte für Hilfstabelle ]


------------------- [ Hilfstabellen vor Änderungen schützen ... [
CREATE OR REPLACE FUNCTION tf_disallow_changes()
  RETURNS trigger AS
$BODY$begin
  RAISE EXCEPTION 'Trigger %: Table % must not be changed', TG_NAME, TG_TABLE_NAME;
end;$BODY$
  LANGUAGE plpgsql;
ALTER FUNCTION tf_disallow_changes()
  OWNER TO "www-data";

-- "INSTEAD OF" ist für Tabellen nicht erlaubt:
CREATE TRIGGER tr_disallow_changes
  BEFORE INSERT OR UPDATE OR DELETE
  ON unitracc_booking_states
  EXECUTE PROCEDURE tf_disallow_changes();
COMMENT ON TABLE unitracc_booking_states
  IS 'Achtung - Änderungen werden derzeit durch Trigger verhindert;
die aktuellen Zeilen finden sich wieder in tf_orders_addmissing.
Nach Eliminierung von unitracc_orders.booking_states_id kann diese Restriktion aufgehoben werden.';
CREATE TRIGGER tr_disallow_changes
  BEFORE INSERT OR UPDATE OR DELETE
  ON unitracc_payment_types
  EXECUTE PROCEDURE tf_disallow_changes();
COMMENT ON TABLE unitracc_payment_types
  IS 'Achtung - Änderungen werden derzeit durch Trigger verhindert;
die aktuellen Zeilen finden sich wieder in tf_orders_addmissing.
Nach Eliminierung von unitracc_orders.payment_type_id kann diese Restriktion aufgehoben werden.';
------------------- ] ... Hilfstabellen vor Änderungen schützen ]

----------------------------------------- [ numerische --> Textfelder ... [
ALTER TABLE unitracc_orders
  ADD COLUMN booking_state TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_booking_state_fkey FOREIGN KEY (booking_state)
      REFERENCES unitracc_booking_states (booking_state) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;
COMMENT ON COLUMN unitracc_orders.booking_states_id
  IS 'veraltend; siehe --> booking_state und --> tf_orders_addmissing';

ALTER TABLE unitracc_orders
  ADD COLUMN payment_type TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_payment_type_fkey FOREIGN KEY (payment_type)
      REFERENCES unitracc_payment_types (payment_type) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;
COMMENT ON COLUMN unitracc_orders.payment_type_id
  IS 'veraltend; siehe --> payment_type und --> tf_orders_addmissing';

/* überflüssiger Constraint, ehemals aus update-0002.sql:
 */
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_la_check_2;

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

-- Werte für neue Felder per Trigger erzeugen:
UPDATE unitracc_orders
  SET booking_states_id = booking_states_id;
ALTER TABLE unitracc_orders
  ALTER COLUMN payment_type SET NOT NULL;
ALTER TABLE unitracc_orders
  ALTER COLUMN booking_state SET NOT NULL;

--------------- [ numerische --> Textfelder: alte Felder löschen ... [
--------- [ numerische --> Textfelder: alte Sichten löschen ... [
DROP FUNCTION IF EXISTS recalculate_order(integer);
DROP VIEW IF EXISTS user_bookings_view;
DROP VIEW IF EXISTS latest_paypal_record_view;
DROP VIEW IF EXISTS booking_states_summary_view;
DROP VIEW IF EXISTS bookings_view;
DROP VIEW IF EXISTS articles_items_view;
DROP VIEW IF EXISTS articles_calculated_view;
DROP VIEW IF EXISTS orders_articles_view;
DROP VIEW IF EXISTS orders_view;
DROP VIEW IF EXISTS articles_discount_view;
DROP VIEW IF EXISTS articles_discount_inner_view;
DROP VIEW IF EXISTS articles_discount_counting_view;
DROP VIEW IF EXISTS articles_vat_view;


/*

psql:Products/unitracc/browser/booking/sql/update-0003.sql:242: ERROR:  cannot drop table unitracc_orders column booking_states_id because other objects depend on it
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
*/


--------- ] ... numerische --> Textfelder: alte Sichten löschen ]

---------- [ bei dieser Gelegenheit: Indexfelder umbenennen ... [
-------------------- [ Fremdschlüssel temporär löschen ... [
-------------------- ] ... Fremdschlüssel temporär löschen ]

------------------------ [ Umbenennung der Indexfelder ... [
ALTER TABLE unitracc_orders
  RENAME COLUMN id TO order_id;


ALTER TABLE unitracc_orders_articles
  DROP CONSTRAINT IF EXISTS unitracc_orders_articles_pkey;
ALTER TABLE unitracc_orders_articles
  RENAME COLUMN id TO article_id;
ALTER TABLE unitracc_orders_articles
  RENAME COLUMN orderid TO order_id;


DELETE FROM  unitracc_orders o1
       USING unitracc_orders o2
 WHERE     o1.order_id = o2.order_id
       -- Systemspalte ctid:
       AND o1.ctid < o2.ctid
       -- Datenspalten:
       AND o1.ordernr = o2.ordernr
       AND o1.userid = o2.userid
       AND o1.sessionid = o2.sessionid
       AND o1.payment_type = o2.payment_type
       AND o1.booking_state = o2.booking_state
       AND o1.ip = o2.ip
       AND o1.date_booked = o2.date_booked
       AND o1.date_payed = o2.date_payed
       AND (o1.firstname = o2.firstname
            OR (o1.firstname IS NULL AND o2.firstname IS NULL))
       AND (o1.lastname = o2.lastname
            OR (o1.lastname IS NULL AND o2.lastname IS NULL))
       AND (o1.company = o2.company
            OR (o1.company IS NULL AND o2.company IS NULL))
       AND (o1.street = o2.street
            OR (o1.street IS NULL AND o2.street IS NULL))
       AND (o1.zip = o2.zip
            OR (o1.zip IS NULL AND o2.zip IS NULL))
       AND (o1.city = o2.city
            OR (o1.city IS NULL AND o2.city IS NULL))
       AND (o1.country = o2.country
            OR (o1.country IS NULL AND o2.country IS NULL))
       AND (o1.additional_info = o2.additional_info
            OR (o1.additional_info IS NULL AND o2.additional_info IS NULL))
       AND (o1.paypal_id = o2.paypal_id
            OR (o1.paypal_id IS NULL AND o2.paypal_id IS NULL))
       AND (o1.paypal_allowed = o2.paypal_allowed
            OR (o1.paypal_allowed IS NULL AND o2.paypal_allowed IS NULL))
       AND (o1.currency = o2.currency
            OR (o1.currency IS NULL AND o2.currency IS NULL))
 RETURNING o1.order_id, o1.ctid, o1.ordernr, o1.userid, o1.payment_type, o1.booking_state, o1.date_payed, o1.date_booked;


ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_id_pkey PRIMARY KEY (order_id);
ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_pkey PRIMARY KEY (article_id);
/* Es fehlt Datensatz Nr. 93 ...
*/
INSERT INTO unitracc_orders (order_id, userid, sessionid, ip, booking_state)
  VALUES (93, '<unknown>', '<unknown>', '0.0.0.0', 'unknown');

ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_order_id_fkey FOREIGN KEY (order_id)
      REFERENCES unitracc_orders (order_id)
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE unitracc_orders_paypal
  RENAME COLUMN id TO paypal_order_id;
-- Constraint: unitracc_orders_paypal_pkey
-- ALTER TABLE unitracc_orders_paypal DROP CONSTRAINT unitracc_orders_paypal_pkey;
ALTER TABLE unitracc_orders_paypal
  ADD CONSTRAINT unitracc_orders_paypal_pkey PRIMARY KEY(paypal_order_id);


/*
unitracc_booking_states, unitracc_payment_types:
vorerst nur eingehende Fremdschlüssel ändern
*/
------------------------ ] ... Umbenennung der Indexfelder ]

-------------------- [ Fremdschlüssel wiederherstellen ... [
-------------------- ] ... Fremdschlüssel wiederherstellen ]
---------- ] ... bei dieser Gelegenheit: Indexfelder umbenennen ]

------------------------------- [ Löschung der alten Felder ... [
-- Trigger und Funktion nach getaner Tat löschen:
DROP TRIGGER IF EXISTS tr_orders_addmissing
  ON unitracc_orders;
DROP FUNCTION IF EXISTS tf_orders_addmissing();

ALTER TABLE unitracc_orders
  DROP COLUMN IF EXISTS booking_states_id;
ALTER TABLE unitracc_orders
  DROP COLUMN IF EXISTS payment_type_id;
------------------------------- ] ... Löschung der alten Felder ]

-------------- [ Sichten mit neuen Feldern wiederherstellen ... [
CREATE OR REPLACE VIEW user_bookings_view AS 
 SELECT o.order_id,
        o.ordernr,
        o.userid,
        o.sessionid,
        o.payment_type,
        o.booking_state,
        o.booking_state AS payment_status,  -- historisch bedingt
        o.date_booked,
        o.date_payed,
        g.group_id_,
        g.start,
        g.ends,
        o.additional_info,
        to_char(g.start::timestamp with time zone, 'DD.MM.YYYY'::text) AS start_ddmmyyyy,
        to_char(g.ends::timestamp with time zone, 'DD.MM.YYYY'::text) AS ends_ddmmyyyy
   FROM unitracc_orders o
        LEFT JOIN unitracc_orders_articles  a ON a.order_id = o.order_id
        LEFT JOIN unitracc_groupmemberships g ON g.order_id = o.order_id
  ORDER BY o.order_id DESC;
ALTER TABLE user_bookings_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW booking_states_summary_view AS 
 SELECT 
    s.booking_state,
    count(o.order_id) AS anzahl,
    max(o.date_booked) AS date_booked
   FROM unitracc_booking_states s
        JOIN unitracc_orders o ON o.booking_state = s.booking_state
  GROUP BY s.booking_state
  ORDER BY max(o.date_booked) DESC;
ALTER TABLE booking_states_summary_view
  OWNER TO "www-data";
COMMENT ON VIEW booking_states_summary_view
  IS 'Vorhandene Buchungen nach Zahlungs-/Buchungsstatus';


-- View: latest_paypal_record_view
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
        p.memo,
        p.paypal_order_id
   FROM unitracc_orders_paypal p
   JOIN unitracc_orders o ON p.unitracc_orders_id = o.order_id
  WHERE p."timestamp" IS NOT NULL
  ORDER BY p."timestamp" DESC;
ALTER TABLE latest_paypal_record_view
  OWNER TO "www-data";

-- wird ergänzt in --> update-0005.sql:
CREATE OR REPLACE VIEW orders_articles_view AS
  SELECT 
         o.order_id,
         o.ordernr,
         o.userid,
         o.sessionid,
         o.payment_type,
         o.booking_state,
         o.date_booked,
         o.date_payed,
         a.article_uid,
         a.article_title,
         a.article_id,
         a.step,
         a.amount,
         a.amount_multiplied,
         a.group_id,
         g.start,
         g.ends,
         -- get_backend_bookings: "real_start"
         to_char(g.start, 'DD.MM.YYYY') AS start_ddmmyyyy,
         -- get_backend_bookings: "real_end"
         to_char(g.ends,  'DD.MM.YYYY') AS  ends_ddmmyyyy,
         a.duration,
         a.quantity,
         a.vat_percent,
         o.la,
         a.discount_group,
         -- get_backend_bookings: 
         to_char(a.start, 'DD.MM.YYYY') AS start_wanted
    FROM unitracc_orders o
         LEFT JOIN unitracc_orders_articles  a ON a.order_id = o.order_id
         LEFT JOIN unitracc_groupmemberships g ON g.order_id = o.order_id
                                              AND g.group_id_ = a.group_id
    ORDER BY o.order_id   DESC,
             a.article_id ASC;
ALTER TABLE orders_articles_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW articles_items_view AS
  SELECT *
    FROM orders_articles_view
   WHERE step = 1
   ORDER BY order_id DESC, -- wie in orders_articles_view
            article_id;
ALTER TABLE articles_items_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_items_view
  IS 'nur die bestellten Artikel selbst (die Berechnungsgrundlage); siehe auch articles_calculated_view';

CREATE OR REPLACE VIEW articles_calculated_view AS
  -- bei den berechneten Zeilen sind weit weniger Felder interessant:
  SELECT order_id,
         article_id,
         step,          -- Sortierkriterium
         article_title, -- hier keine UIDs
         vat_percent,
         amount_multiplied
    FROM orders_articles_view
   WHERE step > 1
   ORDER BY order_id DESC, -- wie in orders_articles_view
            step,
            article_id;
ALTER TABLE articles_calculated_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_calculated_view
  IS 'nur die berechneten Zeilen (Berechnungsgrundlage: siehe articles_items_view)';

CREATE OR REPLACE VIEW bookings_view AS
 SELECT o.order_id,
    o.ordernr,
    o.booking_state,
    o.payment_type,
    o.userid,
    o.firstname,
    o.lastname,
    o.company,
    o.date_booked
   FROM unitracc_orders o
  ORDER BY o.order_id DESC;
ALTER TABLE bookings_view
  OWNER TO "www-data";
COMMENT ON VIEW bookings_view
  IS 'Sicht zum schnelleren Überblick über vorhandene Buchungen';

-- wird ergänzt in --> update-0005.sql:
CREATE OR REPLACE VIEW orders_view AS
 SELECT o.order_id,
        o.ordernr,
        o.userid,
        o.sessionid,
        o.payment_type,
        o.booking_state AS payment_status,
        o.booking_state,
        o.date_booked,
        o.date_payed,
        o.additional_info,
        -- neu ab März 2018:
        o.la,
        CASE
            WHEN o.booking_state IN ('new', 'pending', 'paying') THEN
                'new'
            WHEN o.booking_state IN ('declined', 'timeout') THEN
                'failed'
            WHEN o.booking_state IN ('accepted') THEN
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
  ORDER BY o.order_id DESC;
ALTER TABLE orders_view
  OWNER TO "www-data";



CREATE OR REPLACE VIEW articles_discount_counting_view AS
  WITH t as (
    SELECT a.order_id,
       sum(a.quantity) AS quantity_per_group,
       vat_percent,
       discount_group
      FROM unitracc_orders_articles a
     WHERE step = 1
     GROUP BY a.order_id,
              a.discount_group,
              a.vat_percent
  )
  SELECT t.order_id,
         sum(quantity_per_group) quantity_per_group,
         count(vat_percent) AS vat_percentages_per_group,
         discount_group
    FROM t
   GROUP BY t.order_id,
            t.discount_group;
ALTER TABLE articles_discount_counting_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_discount_counting_view
  IS 'Hilfs-Sicht für articles_discount_view:
Da es theoretisch möglich ist, daß Artikel derselben Rabattgruppe unterschiedliche Mehrwertsteuersätze haben
(zumindest ist es im System möglich, den MwSt-Satz (VAT) pro Objekt anzugeben),
die Anzahl sich aber unabhängig von solchen Unterschieden berechnet,
muß diese Anzahl vorab ermittelt werden.';

CREATE OR REPLACE VIEW articles_discount_inner_view AS
 SELECT a.order_id,
        cv.quantity_per_group,
        CASE
            WHEN cv.quantity_per_group >= 10 THEN
                10
            WHEN cv.quantity_per_group >= 5 THEN
                5
            WHEN cv.quantity_per_group >= 3 THEN
                3
            ELSE NULL
        END AS discount_quorum,
        CASE
            WHEN cv.quantity_per_group >= 10 THEN
                30
            WHEN cv.quantity_per_group >= 5 THEN
                20
            WHEN cv.quantity_per_group >= 3 THEN
                10
            ELSE NULL
        END AS discount_percent,
        cv.vat_percentages_per_group,
        max(a.article_id) AS article_id,
        max(a.article_title::TEXT) AS article_title,
        a.vat_percent,
        sum(a.quantity * a.amount) AS amount,
        a.discount_group
   FROM articles_discount_counting_view cv
        LEFT JOIN unitracc_orders_articles a ON cv.order_id = a.order_id
                                            AND cv.discount_group = a.discount_group
  WHERE a.step = 1
  GROUP BY a.order_id,
           a.discount_group,
           a.vat_percent,
           cv.quantity_per_group,
           cv.vat_percentages_per_group;

ALTER TABLE articles_discount_inner_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_discount_inner_view
  IS 'Hilfs-Sicht für articles_discount_view:
Bereitstellung der Daten';


----------------------------------- [ articles_discount_view ... [
CREATE OR REPLACE VIEW articles_discount_view AS
 WITH t AS (
 SELECT iv.order_id,
        gt.la, -- Sprachkürzel
        iv.discount_quorum,
        iv.discount_percent,
        iv.discount_group,
        iv.vat_percentages_per_group,
        iv.vat_percent,
        CASE
            WHEN vat_percentages_per_group = 1 THEN
                format(gt.text_normal, discount_percent, discount_quorum)
            WHEN vat_percent IS NULL or vat_percent = 0 THEN
                format(gt.text_zero_vat, discount_percent, discount_quorum)
            ELSE
                format(gt.text_with_vat, discount_percent, discount_quorum, vat_percent)
        END AS article_title,
        iv.amount
   FROM articles_discount_inner_view iv
        join unitracc_discount_group_texts gt ON iv.discount_group = gt.discount_group
  )
  SELECT *,
        CAST(t.discount_percent / -100.0 * t.amount AS NUMERIC(10, 2)) AS amount_multiplied,
        5 AS step
    FROM t
  ORDER BY discount_group DESC,  -- enterprise vor course
           vat_percent;
ALTER TABLE articles_discount_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_discount_view
  IS 'Ausgabe der Rabatte, in Abhängigkeit von der numerischen Buchungsnummer (order_id) und der Ausgabesprache';
COMMENT ON COLUMN articles_discount_view.la
  IS 'Bei Verwendung dieser Sicht als Berechnungsgrundlage ist unbedingt nach "la" zu filtern!';
----------------------------------- ] ... articles_discount_view ]

----------------------------------- [ articles_vat_view ... [
CREATE OR REPLACE VIEW articles_vat_view AS
  WITH t1 AS (
    SELECT order_id,
           amount_multiplied,
           vat_percent
      FROM unitracc_orders_articles
     WHERE step = 1 OR step = 5
    ), t2 AS (
    SELECT order_id,
           sum(amount_multiplied) AS amount_multiplied,
           vat_percent
      FROM t1
     GROUP BY order_id, vat_percent
    )
  SELECT DISTINCT
         t2.order_id,
         CAST(t2.amount_multiplied * t2.vat_percent / 100.0 AS NUMERIC(10, 2)) AS amount_multiplied,
         t2.vat_percent,
         format(vt.text_normal, t2.vat_percent) AS article_title,
         10 AS step
    FROM t2
         JOIN unitracc_orders    uo ON t2.order_id = uo.order_id
         JOIN unitracc_vat_texts vt ON uo.la = vt.la
   ORDER BY t2.vat_percent;
ALTER TABLE articles_vat_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_vat_view
  IS 'Ausgabe der Mehrwertsteuer, in Abhängigkeit von der numerischen Buchungsnummer (order_id)';
----------------------------------- ] ... articles_vat_view ]

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
  (given_order_id integer)
  RETURNS TABLE (  -- wie von Sicht articles_calculated_view
          order_id          integer,
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
    FROM unitracc_orders o
   WHERE o.order_id = given_order_id;
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


-- (zurückgesetzt auf false wird das Feld
--  derzeit in Anwendungscode)
CREATE OR REPLACE FUNCTION tf_articles_dirty()
  RETURNS trigger AS
$BODY$begin
  if TG_OP = 'DELETE' then
    if old.step = 1 then
      UPDATE unitracc_orders
        SET dirty = true
        WHERE order_id = old.order_id;
    end if;
  else
      if new.step = 1 then
            UPDATE unitracc_orders
              SET dirty = true
              WHERE order_id = new.order_id;
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
                WHERE order_id = new.order_id;
          else
              -- vat_total wird in der Funktion recalculate_order
              -- direkt gesetzt
              if new.step = 15 then  -- Gesamtsumme
                  UPDATE unitracc_orders
                    SET total = new.amount_multiplied
                    WHERE order_id = new.order_id;
              end if;
          end if;
      end if;
  end if;
  return new;
end;$BODY$
  LANGUAGE plpgsql;
ALTER FUNCTION tf_articles_dirty()
  OWNER TO "www-data";




-------------- ] ... Sichten mit neuen Feldern wiederherstellen ]

--------------- ] ... numerische --> Textfelder: alte Felder löschen ]


-- Sichten ohne die nicht mehr zu verwendenden id-Felder:
CREATE VIEW payment_types_view AS
  SELECT payment_type,
         active
    FROM unitracc_payment_types
   ORDER BY id;
CREATE VIEW booking_states_view AS
  SELECT booking_state,
         state_description
    FROM unitracc_booking_states
   ORDER BY id;
----------------------------------------- ] ... numerische --> Textfelder ]

/* Test:
INSERT INTO unitracc_orders
(userid, sessionid, payment_type_id, ip)
VALUES ('therp', 'session123', 1, '0.0.0.0')
RETURNING *;
*/

--------------------------- ] ... Konsolidierung von unitracc_orders ]

END;
