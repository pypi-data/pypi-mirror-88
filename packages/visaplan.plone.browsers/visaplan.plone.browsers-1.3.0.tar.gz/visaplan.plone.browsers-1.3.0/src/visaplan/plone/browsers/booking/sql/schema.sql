-- für den Browser unitracc@@booking -*- coding: utf-8 -*- äöü vim: et ic sw=4 sts=4 ts=4 si

-- [ Transaktion für die Änderungen von Unitracc 2.2.17 ... [
BEGIN TRANSACTION;
-- für Methode get_order bzw. evtl. get_orders:
CREATE OR REPLACE VIEW orders_view AS
SELECT o.id,
       o.ordernr,
       o.userid,
       o.sessionid,
       o.payment_type_id,
       p.payment_type,
       o.booking_states_id,
       s.booking_state payment_status,
       o.date_booked,
       o.date_payed,
       o.additional_info
  FROM unitracc_orders o
  LEFT JOIN unitracc_payment_types p
       ON o.payment_type_id = p.id
  LEFT JOIN unitracc_booking_states s
       ON o.booking_states_id = s.id
  ORDER BY o.id DESC;
ALTER VIEW public.orders_view OWNER TO "www-data";


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
  LEFT JOIN unitracc_orders_articles a
       ON a.orderid = o.id
  LEFT JOIN unitracc_payment_types p
       ON o.payment_type_id = p.id
  LEFT JOIN unitracc_booking_states s
       ON o.booking_states_id = s.id
  ORDER BY o.id DESC;
ALTER VIEW public.orders_articles_view OWNER TO "www-data";


CREATE OR REPLACE VIEW user_bookings_view AS
SELECT o.id,
       o.ordernr,
       o.userid,
       o.sessionid,
       -- o.payment_type_id,
       p.payment_type,
       -- o.booking_states_id,
       s.booking_state payment_status,
       o.date_booked,
       o.date_payed,
       g.start,
       g.ends,
       o.additional_info
  FROM unitracc_orders o
  LEFT JOIN unitracc_orders_articles a
       ON a.orderid = o.id
  LEFT JOIN unitracc_payment_types p
       ON o.payment_type_id = p.id
  LEFT JOIN unitracc_booking_states s
       ON o.booking_states_id = s.id
  LEFT JOIN unitracc_groupmemberships g
       ON g.order_id = o.id
  ORDER BY o.id DESC;
ALTER VIEW public.user_bookings_view OWNER TO "www-data";


-- üblicherweise zu filtern nach learner_gid:
CREATE OR REPLACE VIEW current_course_bookings_view AS
SELECT m.courseuid learner_gid,  -- ID der Lerngruppe
       m.groupuid,
       m.start,
       m.ends,
       m.order_id,
       m.id
  FROM unitracc_groupmemberships m
 WHERE NOW() BETWEEN start AND ends;
ALTER VIEW public.current_course_bookings_view OWNER TO "www-data";

ALTER TABLE unitracc_orders_paypal
ADD COLUMN memo varchar(255);

ALTER TABLE unitracc_orders_paypal
ADD COLUMN timestamp TIMESTAMP DEFAULT now();

CREATE OR REPLACE VIEW latest_paypal_record_view AS
SELECT payment_status,
       pending_reason,
       reason_code,
       payer_id,
       payer_email,
       payer_status,
       address_name,
       o.userid,
       o.ordernr,
       p.timestamp,
       p.memo
  FROM unitracc_orders_paypal p
  JOIN unitracc_orders o ON unitracc_orders_id = o.id
 WHERE p.timestamp IS NOT NULL 
 ORDER BY p.timestamp desc;
ALTER VIEW public.latest_paypal_record_view OWNER TO "www-data";

COMMIT;
-- ] ... Transaktion für die Änderungen von Unitracc 2.2.17 ]


/*
BEGIN TRANSACTION;
ALTER TABLE unitracc_orders_paypal
ADD row_nr SERIAL;

CREATE OR REPLACE VIEW latest_paypal_record_view AS
SELECT payment_status,
       pending_reason,
       reason_code,
       payer_id,
       payer_email,
       payer_status,
       address_name,
       o.userid,
       o.ordernr,
       p.timestamp,
       p.memo,
       p.row_nr
  FROM unitracc_orders_paypal p
  JOIN unitracc_orders o ON unitracc_orders_id = o.id
 ORDER BY p.row_nr desc;
ALTER VIEW public.latest_paypal_record_view OWNER TO "www-data";
COMMIT;
*/

BEGIN TRANSACTION;
-- Erst die View korrigieren.
-- Es ist nicht möglich, ein Feld zu löschen;
-- stattdessen muß die Sicht neu erzeugt werden:
DROP VIEW latest_paypal_record_view;
CREATE VIEW latest_paypal_record_view AS
SELECT p.unitracc_orders_id,
       payment_status,
       pending_reason,
       reason_code,
       payer_id,
       payer_email,
       payer_status,
       address_name,
       o.userid,
       o.ordernr,
       p.timestamp,
       p.memo
  FROM unitracc_orders_paypal p
  JOIN unitracc_orders o ON unitracc_orders_id = o.id
 WHERE p.timestamp IS NOT NULL 
 ORDER BY p.timestamp desc;
ALTER VIEW public.latest_paypal_record_view OWNER TO "www-data";

-- Jetzt das obsolete Feld aus der Tabelle löschen:
ALTER TABLE unitracc_orders_paypal
DROP row_nr;
COMMIT;

INSERT INTO unitracc_booking_states (id, booking_state)
VALUES (99, 'unknown');

ALTER TABLE unitracc_orders_articles
ADD UNIQUE (orderid, article_uid);
-- bis hierher enthalten in Version 2.2.18

ALTER TABLE unitracc_payment_types
ADD UNIQUE (payment_type);

DROP VIEW IF EXISTS user_bookings_view;
CREATE OR REPLACE VIEW user_bookings_view AS
SELECT o.id,
       o.ordernr,
       o.userid,
       o.sessionid,
       -- o.payment_type_id,
       p.payment_type,
       -- o.booking_states_id,
       s.booking_state payment_status,
       o.date_booked,
       o.date_payed,
       g.courseuid group_id,
       g.start,
       g.ends,
       o.additional_info
  FROM unitracc_orders o
  LEFT JOIN unitracc_orders_articles a
       ON a.orderid = o.id
  LEFT JOIN unitracc_payment_types p
       ON o.payment_type_id = p.id
  LEFT JOIN unitracc_booking_states s
       ON o.booking_states_id = s.id
  LEFT JOIN unitracc_groupmemberships g
       ON g.order_id = o.id
  ORDER BY o.id DESC;
ALTER VIEW public.user_bookings_view OWNER TO "www-data";

-- obsolet, da Untermenge von orders_view:
DROP VIEW IF EXISTS bookings_view;

COMMENT ON COLUMN unitracc_groupmemberships.courseuid IS 'ID (keine UID!) der Reader-/learner-Gruppe; in user_bookings_view als group_id';
COMMENT ON COLUMN unitracc_groupmemberships.groupuid IS 'ID (keine UID!) des Users oder der (Teilnehmer-) Gruppe, der der Gruppe "courseuid" zugeordnet wird';
COMMENT ON COLUMN user_bookings_view.group_id IS 'Die (schlecht benannte) Spalte unitracc_groupmemberships.courseuid';

