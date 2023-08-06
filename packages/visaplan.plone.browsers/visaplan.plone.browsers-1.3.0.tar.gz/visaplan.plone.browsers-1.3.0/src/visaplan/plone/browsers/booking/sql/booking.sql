-- unitracc@@booking -*- coding: utf-8 -*- äöü vim: et ic sw=4 sts=4 ts=4 si

COMMENT ON COLUMN unitracc_booking_states.id IS 'Numerische ID';
COMMENT ON COLUMN unitracc_booking_states.booking_state IS 'Symbolischer Name';
-- Zugriff auf Status über textuellen Namen unterstützen
-- (ALTER TABLE wird fehlschlagen, wenn die Datenbank gerade verwendet wird -
-- und leider hängen ...)
ALTER TABLE unitracc_booking_states
  ADD UNIQUE (booking_state);

CREATE OR REPLACE VIEW bookings_view AS
SELECT o.id, o.ordernr,
       s.booking_state,
       pt.payment_type,
       o.userid, o.firstname, o.lastname, o.company,
       o.date_booked
 FROM unitracc_orders o
 JOIN unitracc_booking_states s ON o.booking_states_id = s.id
 JOIN unitracc_payment_types pt ON o.payment_type_id = pt.id
ORDER BY o.id DESC;

ALTER TABLE bookings_view
  OWNER TO "www-data";
COMMENT ON VIEW bookings_view
  IS 'Sicht zum schnelleren Überblick über vorhandene Buchungen';

CREATE OR REPLACE VIEW booking_states_summary_view AS
SELECT s.id, s.booking_state,
       count(o.id) Anzahl,
       max(o.date_booked) date_booked
  FROM unitracc_booking_states s
  JOIN unitracc_orders o on o.booking_states_id = s.id
 GROUP BY s.id
 ORDER BY date_booked DESC;

ALTER TABLE booking_states_summary_view
  OWNER TO "www-data";
COMMENT ON VIEW booking_states_summary_view
  IS 'Vorhandene Buchungen nach Zahlungs-/Buchungsstatus';

