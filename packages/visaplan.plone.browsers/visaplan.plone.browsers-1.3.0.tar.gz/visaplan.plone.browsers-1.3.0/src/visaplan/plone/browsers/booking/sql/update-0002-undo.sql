BEGIN TRANSACTION;
/*
Änderungen aus update-0002.sql zurücksetzen
(für Entwicklungszwecke)
*/
DROP FUNCTION IF EXISTS recalculate_order(integer);
DROP VIEW IF EXISTS articles_calculated_view;
DROP VIEW IF EXISTS articles_items_view;
DROP VIEW IF EXISTS articles_discount_view;
DROP VIEW IF EXISTS articles_discount_inner_view;
DROP VIEW IF EXISTS articles_discount_counting_view;
DROP VIEW IF EXISTS articles_vat_view;
DROP VIEW IF EXISTS orders_articles_view;
DROP VIEW IF EXISTS user_bookings_view;
DROP VIEW IF EXISTS orders_view;
DROP VIEW IF EXISTS latest_paypal_record_view;
DROP VIEW IF EXISTS bookings_view;

ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_la_fkey;
ALTER TABLE unitracc_orders_articles
  DROP CONSTRAINT IF EXISTS unitracc_orders_articles_step_fkey;
ALTER TABLE unitracc_orders_articles
  DROP CONSTRAINT IF EXISTS unitracc_orders_articles_discount_group_fkey;

DROP TABLE IF EXISTS unitracc_language CASCADE;
DROP TABLE IF EXISTS unitracc_discount_group CASCADE;
DROP TABLE IF EXISTS unitracc_discount_group_texts CASCADE;
DROP TABLE IF EXISTS unitracc_orders_calc_steps CASCADE;
DROP TABLE IF EXISTS unitracc_orders_calc_step_texts CASCADE;
DROP TABLE IF EXISTS unitracc_vat_texts;

-------------- [ etwaige Testdaten aufräumen ... [
DELETE FROM unitracc_orders_articles
 WHERE article_uid LIKE 'test%';
    -- OR step > 1;
-------------- ] ... etwaige Testdaten aufräumen ]

--------- [ Daten nach neuem Schema abräumen ... [
DELETE FROM unitracc_orders_articles
 WHERE article_uid IS NULL;
--------- ] ... Daten nach neuem Schema abräumen ]

-- verwendet die Felder "step" und "dirty" (siehe unten):
DROP TRIGGER IF EXISTS tr_articles_dirty
  ON unitracc_orders_articles;
DROP FUNCTION IF EXISTS tf_articles_dirty();

ALTER TABLE unitracc_orders
  DROP COLUMN IF EXISTS dirty;
ALTER TABLE unitracc_orders
  DROP COLUMN IF EXISTS la;
ALTER TABLE unitracc_orders_articles
  DROP COLUMN IF EXISTS step;
ALTER TABLE unitracc_orders_articles
  DROP COLUMN IF EXISTS quantity;
ALTER TABLE unitracc_orders_articles
  DROP COLUMN IF EXISTS discount_group;
ALTER TABLE unitracc_orders_articles
  DROP COLUMN IF EXISTS amount_multiplied;
ALTER TABLE unitracc_orders_articles
  DROP COLUMN IF EXISTS vat_percent;
ALTER TABLE unitracc_orders_articles
  DROP COLUMN IF EXISTS group_id;

ALTER TABLE unitracc_orders_articles
  ALTER COLUMN amount DROP NOT NULL;
ALTER TABLE unitracc_orders_articles
  ALTER COLUMN amount DROP DEFAULT;
COMMENT ON COLUMN unitracc_orders_articles.amount
  IS '@@booking, update-0002: SET NOT NULL, DEFAULT 0';

DROP TRIGGER IF EXISTS tr_articles_addmissing
  ON unitracc_orders_articles;
DROP FUNCTION IF EXISTS tf_articles_addmissing();

--------------------------[ Änderung der Spaltentypen revertieren ... [

--------------------- [ text --> zurück zu character varying ... [
ALTER TABLE unitracc_orders
  ALTER COLUMN ordernr TYPE CHARACTER VARYING(50);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_ordernr_check_50;

ALTER TABLE unitracc_orders
  ALTER COLUMN userid TYPE CHARACTER VARYING(50);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_userid_check_50;

ALTER TABLE unitracc_orders
  ALTER COLUMN sessionid TYPE CHARACTER VARYING(150);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_sessionid_check_150;

ALTER TABLE unitracc_orders
  ALTER COLUMN ip TYPE CHARACTER VARYING(15);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_ip_check_15;

ALTER TABLE unitracc_orders
  ALTER COLUMN firstname TYPE CHARACTER VARYING(50);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_firstname_check_50;

ALTER TABLE unitracc_orders
  ALTER COLUMN lastname TYPE CHARACTER VARYING(50);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_lastname_check_50;

ALTER TABLE unitracc_orders
  ALTER COLUMN company TYPE CHARACTER VARYING(150);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_company_check_150;

ALTER TABLE unitracc_orders
  ALTER COLUMN street TYPE CHARACTER VARYING(150);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_street_check_150;

ALTER TABLE unitracc_orders
  ALTER COLUMN zip TYPE CHARACTER VARYING(50);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_zip_check_50;

ALTER TABLE unitracc_orders
  ALTER COLUMN city TYPE CHARACTER VARYING(100);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_city_check_100;

ALTER TABLE unitracc_orders
  ALTER COLUMN country TYPE CHARACTER VARYING(200);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_country_check_200;

ALTER TABLE unitracc_orders
  ALTER COLUMN additional_info TYPE CHARACTER VARYING(50);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_additional_info_check_50;

ALTER TABLE unitracc_orders
  ALTER COLUMN currency TYPE CHARACTER VARYING(10);
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_currency_check_10;

ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_la_check_2;

ALTER TABLE unitracc_orders_articles
  ALTER COLUMN article_uid TYPE CHARACTER VARYING(50);
ALTER TABLE unitracc_orders_articles
  ALTER COLUMN article_uid SET NOT NULL;
ALTER TABLE unitracc_orders_articles
  DROP CONSTRAINT IF EXISTS unitracc_orders_articles_article_uid_check;

ALTER TABLE unitracc_orders_articles
  ALTER COLUMN article_title TYPE CHARACTER VARYING(300);
ALTER TABLE unitracc_orders_articles
  DROP CONSTRAINT IF EXISTS unitracc_orders_articles_article_title_check_300;
--------------------- ] ... text --> zurück zu character varying ]

-------------- [ weitere neue Felder für die Buchungstabelle ... [
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_adminid_check_50;
ALTER TABLE unitracc_orders
   DROP COLUMN IF EXISTS adminid;

------------------------------ [ neue numerische Felder ... [
ALTER TABLE unitracc_orders
  DROP COLUMN IF EXISTS net_total;
ALTER TABLE unitracc_orders
  DROP COLUMN IF EXISTS vat_total;
ALTER TABLE unitracc_orders
  DROP COLUMN IF EXISTS total;
------------------------------ ] ... neue numerische Felder ]

ALTER TABLE unitracc_orders
  ALTER COLUMN payment_type_id DROP DEFAULT;
ALTER TABLE unitracc_orders
  ALTER COLUMN booking_states_id DROP DEFAULT;
-------------- ] ... weitere neue Felder für die Buchungstabelle ]

------------------------ [ Verknüpfung zu u.groupmemberships ... [
-- erster Versuch ...
ALTER TABLE unitracc_orders_articles
  DROP CONSTRAINT IF EXISTS unitracc_orders_articles_orderid_fkey1;
ALTER TABLE unitracc_groupmemberships
  DROP CONSTRAINT IF EXISTS unitracc_groupmemberships_order_id_group_id__key;
-- zweiter Versuch ...
ALTER TABLE unitracc_orders_articles
  DROP CONSTRAINT IF EXISTS unitracc_orders_articles_orderid_groupid__key;
ALTER TABLE unitracc_groupmemberships
  DROP CONSTRAINT IF EXISTS unitracc_groupmemberships_orderid_groupid__key;
-- das neue Feld; auch oben schon gelöscht:
ALTER TABLE unitracc_orders_articles
  DROP COLUMN IF EXISTS group_id;
------------------------ ] ... Verknüpfung zu u.groupmemberships ]

----------------------------------------- [ neue Constraints ... [
ALTER TABLE unitracc_payment_types
  DROP CONSTRAINT IF EXISTS unitracc_payment_types_payment_type__key;
ALTER TABLE unitracc_booking_states
  DROP CONSTRAINT IF EXISTS unitracc_booking_states_booking_state__key;
----------------------------------------- ] ... neue Constraints ]

-------------------- [ gelöschte Sicht wiederherstellen ... [
-- (alte Fassung vor update-0002.sql)
CREATE OR REPLACE VIEW orders_articles_view AS
  SELECT o.id,
         o.ordernr,
         o.userid,
         o.sessionid,
         p.payment_type,
         s.booking_state,
         o.date_booked,
         o.date_payed,
         a.article_uid,
         a.article_title,
         a.amount
    FROM unitracc_orders o
    LEFT JOIN unitracc_orders_articles a ON a.orderid = o.id
    LEFT JOIN unitracc_payment_types p ON o.payment_type_id = p.id
    LEFT JOIN unitracc_booking_states s ON o.booking_states_id = s.id
   ORDER BY o.id DESC;
ALTER TABLE orders_articles_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW user_bookings_view AS
 SELECT o.id,
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
        o.additional_info
   FROM unitracc_orders o
        LEFT JOIN unitracc_orders_articles a ON a.orderid = o.id
        LEFT JOIN unitracc_payment_types p ON o.payment_type_id = p.id
        LEFT JOIN unitracc_booking_states s ON o.booking_states_id = s.id
        LEFT JOIN unitracc_groupmemberships g ON g.order_id = o.id
  ORDER BY o.id DESC;
ALTER TABLE user_bookings_view
  OWNER TO "www-data";

-- (alte Fassung vor update-0002.sql)
CREATE OR REPLACE VIEW orders_view AS
 SELECT o.id,
        o.ordernr,
        o.userid,
        o.sessionid,
        o.payment_type_id,
        p.payment_type,
        o.booking_states_id,
        s.booking_state AS payment_status,
        o.date_booked,
        o.date_payed,
        o.additional_info
   FROM unitracc_orders o
        LEFT JOIN unitracc_payment_types p ON o.payment_type_id = p.id
        LEFT JOIN unitracc_booking_states s ON o.booking_states_id = s.id
  ORDER BY o.id DESC;
ALTER TABLE orders_view
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

CREATE OR REPLACE VIEW bookings_view AS
 SELECT o.id, o.ordernr, s.booking_state, pt.payment_type, o.userid,
    o.firstname, o.lastname, o.company, o.date_booked
   FROM unitracc_orders o
   JOIN unitracc_booking_states s ON o.booking_states_id = s.id
   JOIN unitracc_payment_types pt ON o.payment_type_id = pt.id
  ORDER BY o.id DESC;
ALTER TABLE bookings_view
  OWNER TO "www-data";
COMMENT ON VIEW bookings_view
  IS 'Sicht zum schnelleren Überblick über vorhandene Buchungen';

-------------------- ] ... gelöschte Sicht wiederherstellen ]

--------------------------] ... Änderung der Spaltentypen revertieren ]
END;
