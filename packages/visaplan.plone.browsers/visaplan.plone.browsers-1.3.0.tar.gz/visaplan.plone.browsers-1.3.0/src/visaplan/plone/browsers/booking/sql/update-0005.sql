BEGIN TRANSACTION;  /* -*- coding: utf-8 -*- vim: expandtab sw=4 sts=4 si
Weiterentwicklung des Buchungssystems:

- Erledigungsart:
  Wenn mehr als ein Zugang pro Kurs gebucht wird, oder beim Bildungspaket,
  kann die Erledigung nicht durch simple Freischaltung des Buchenden nach
  Zahlungseingang erfolgen; stattdessen müssen Zugangscodes versandt werden.
  Der Versand kann per E-Mail oder Papierpost erfolgen.

Temporäre Änderungen:
- Die Modifikation bestimmter Tabellen kann wieder erlaubt werden,
  der die Umstellung auf die Verwendung von Kürzeln anstelle der numerischen IDs abgeschlossen ist
  (kein Undo vorgesehen)

Siehe auch --> update-0005-undo.sql
*/

-- auch --> update-0003-undo.sql:
DROP TRIGGER IF EXISTS tr_disallow_changes
  ON unitracc_payment_types;

------------------------- [ access_settlement_mode ... [
------------------------------ [ neue Tabelle ... [
CREATE TABLE unitracc_access_settlement_mode (
  mode_key TEXT NOT NULL,
  mode_description TEXT NOT NULL,
  mode_order SERIAL NOT NULL,
  mode_enabled BOOLEAN NOT NULL DEFAULT true,
  CONSTRAINT unitracc_access_settlement_mode_pkey PRIMARY KEY (mode_key),
  CONSTRAINT unitracc_access_settlement_mode_unique_description UNIQUE (mode_description)
  )
WITH (
  OIDS=FALSE
);
ALTER TABLE unitracc_access_settlement_mode
  OWNER TO "www-data";
COMMENT ON TABLE unitracc_access_settlement_mode
  IS 'Erledigungsarten für Berechtigungszuweisung

Bei Buchung eines Bildungspakets (für 15 Mitarbeiter) z. B. ist es nicht möglich,
dies durch Aktivierung eines einzelnen Benutzers zu erledigen; stattdessen muß eine
entsprechende Anzahl von Zugangscodes versandt werden.  Die entsprechende Sicherstellung,
daß Unternehmenspakete nicht ''immediate'' erledigt werden, ist derzeit Aufgabe des
Programmcodes und wird *nicht* durch das Feld "mode_enabled" geleistet.';
-- Bei Spaltenbeschreibungen sind feste Zeilenumbrüche ungünstig:
COMMENT ON COLUMN unitracc_access_settlement_mode.mode_key
  IS 'Zur Ausgabe einer lokalisierten Beschreibung wird das Präfix "access_settlement_mode_" vorangestellt.';
COMMENT ON COLUMN unitracc_access_settlement_mode.mode_description
  IS 'Nur zur Dokumentation; zur Ausgabe einer Beschreibung für den Benutzer siehe --> mode_key.';
COMMENT ON COLUMN unitracc_access_settlement_mode.mode_enabled
  IS 'Nur zur generellen Deaktivierung (dann für neue Aufträge nicht mehr auswählbar); weitergehende Funktionen müssen derzeit durch Programmcode erledigt werden.';

INSERT INTO unitracc_access_settlement_mode
  (mode_order, mode_key, mode_description)
VALUES
  (1, 'immediate', 'Der Zugang wird nach Buchung der Zahlung direkt durch das Buchungssystem gewährt; ' ||
                   'nur möglich bei Anzahl=1 bei allen Posten, und nicht bei Unternehmenspaketen'),
  (2, 'tans_email', 'Es werden Zugangscodes (TANs) ausgefertigt und per E-Mail versendet'),
  (3, 'tans_postal', 'Es werden Zugangscodes (TANs) ausgefertigt und per Briefpost versendet');

------------- [ Sicht für Administration ... [
CREATE OR REPLACE VIEW access_settlement_modes_raw_view AS
  SELECT mode_key,
         'access_settlement_mode_' || mode_key AS access_settlement_mode_msgid,
         'access_settlement_mode_' || mode_key || '_description' AS access_settlement_mode_description_msgid,
         mode_enabled
    FROM unitracc_access_settlement_mode
   ORDER BY mode_order ASC,
            mode_key ASC;
ALTER TABLE access_settlement_modes_raw_view
  OWNER TO "www-data";
------------- ] ... Sicht für Administration ]

-------------------- [ Sicht für Auswahl ... [
CREATE OR REPLACE VIEW access_settlement_modes_user_view AS
  SELECT mode_key,
         access_settlement_mode_msgid,
         access_settlement_mode_description_msgid
    FROM access_settlement_modes_raw_view
   WHERE mode_enabled;
ALTER TABLE access_settlement_modes_user_view
  OWNER TO "www-data";
-------------------- ] ... Sicht für Auswahl ]
------------------------------ ] ... neue Tabelle ]

---------------------- [ neuer Fremdschlüssel ... [
ALTER TABLE unitracc_orders
  ADD COLUMN access_settlement_mode TEXT DEFAULT 'immediate';
-- die neue Spalte ist nun für vorhandene Aufträge korrekt gefüllt
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_access_settlement_mode_fkey
      FOREIGN KEY (access_settlement_mode)
      REFERENCES unitracc_access_settlement_mode (mode_key)
      ON UPDATE NO ACTION ON DELETE NO ACTION;
-- für neue Aufträge muß dies explizit gewählt werden:
ALTER TABLE unitracc_orders
  ALTER COLUMN access_settlement_mode DROP DEFAULT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_has_access_settlement_mode
  CHECK (booking_state = 'new' OR access_settlement_mode IS NOT NULL);
---------------------- ] ... neuer Fremdschlüssel ]

-------------------------- [ Sichten anpassen ... [
CREATE OR REPLACE VIEW orders_articles_view AS
  SELECT o.order_id,
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
         to_char(a.start, 'DD.MM.YYYY') AS start_wanted,
         -- Erledigungssart, ab April 2018:
         o.access_settlement_mode,
         s.access_settlement_mode_msgid
    FROM unitracc_orders o
         LEFT JOIN unitracc_orders_articles  a ON a.order_id = o.order_id
         LEFT JOIN unitracc_groupmemberships g ON g.order_id = o.order_id
                                              AND g.group_id_ = a.group_id
         LEFT JOIN access_settlement_modes_raw_view s ON s.mode_key = o.access_settlement_mode
    ORDER BY o.order_id   DESC,
             a.article_id ASC;
ALTER TABLE orders_articles_view
  OWNER TO "www-data";

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
        o.currency,
        -- Erledigungssart, ab April 2018:
        o.access_settlement_mode,
        s.access_settlement_mode_msgid  -- generisch um Präfix ergänzt
   FROM unitracc_orders o
        LEFT JOIN access_settlement_modes_raw_view s ON s.mode_key = o.access_settlement_mode
  ORDER BY o.order_id DESC;
ALTER TABLE orders_view
  OWNER TO "www-data";

-------------------------- ] ... Sichten anpassen ]
------------------------- ] ... access_settlement_mode ]


END;
