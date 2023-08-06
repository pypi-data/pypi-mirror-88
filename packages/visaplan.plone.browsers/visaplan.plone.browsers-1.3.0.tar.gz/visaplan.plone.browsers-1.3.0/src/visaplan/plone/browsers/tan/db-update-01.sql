-- Änderungen relativ zu schema-2.2.11.sql und daten-2.2.11.sql vom 20.2.2014

-- Spalte mit Sortierschlüssel ergänzen:
BEGIN TRANSACTION;
ALTER TABLE tan_status
  ADD COLUMN sortkey integer;
UPDATE tan_status SET sortkey = 1 WHERE name = 'new';
UPDATE tan_status SET sortkey = 2 WHERE name = 'reserved';
UPDATE tan_status SET sortkey = 3 WHERE name = 'used';
UPDATE tan_status SET sortkey = 4 WHERE name = 'expired';
UPDATE tan_status SET sortkey = 5 WHERE name = 'deleted';
ALTER TABLE tan_status
  ALTER COLUMN sortkey SET NOT NULL;
ALTER TABLE tan_status
  ADD CONSTRAINT tan_status_sortkey UNIQUE (sortkey);
COMMENT ON COLUMN tan_status.sortkey IS 'nur zum Sortieren, nicht zum Zugriff';
COMMIT;

-- Beschreibungsspalte ergänzen:
BEGIN TRANSACTION;
ALTER TABLE tan
  ADD COLUMN additional_info character varying(50);
ALTER TABLE tan_history
  ADD COLUMN additional_info character varying(50);
COMMENT ON COLUMN tan_history.additional_info IS
  'Z. B. die E-Mail-Adresse, an die versandt wurde, der Name der Firma, etc.';
COMMENT ON COLUMN tan.additional_info IS
  'Entspricht dem letzten (bzw. letzten nicht-leeren?) Wert in der Historie dieser TAN';
COMMIT;

-- Hoppla - Beschreibungsspalte für tan_changeset, nicht für tan_history:
BEGIN TRANSACTION;
ALTER TABLE tan_changeset
  ADD COLUMN additional_info character varying(50);
COMMENT ON COLUMN tan_changeset.additional_info IS
  'Z. B. die E-Mail-Adresse, an die versandt wurde, der Name der Firma, etc.';
ALTER TABLE tan_history
 DROP COLUMN additional_info;
COMMIT;

-- keine zwei Statusfelder in tan_history; status_hint --> additional_info:
BEGIN TRANSACTION;
ALTER TABLE tan_history
 DROP COLUMN status_old;
ALTER TABLE tan_history
 RENAME COLUMN status_new TO status;
ALTER TABLE tan_history
 DROP COLUMN status_hint;
COMMIT;

-- eine View zum Sammeln aller aktuellen Informationen zu einer TAN;
-- es wird nur der jeweils letzte Änderungssatz aufgeführt.
BEGIN TRANSACTION;
DROP VIEW IF EXISTS tan_view;
CREATE OR REPLACE VIEW tan_view AS
SELECT t.tan, t.status, t.group_id, t.duration_days,
       t.owner_id, 
       TO_CHAR(t.expiration_date, 'DD.MM.YYYY') as expiration_date,
       t.additional_info,
       c.user_id changed_by,
       MAX(h.changeset) changeset,
       TO_CHAR(MAX(c.date), 'YYYY-MM-DD FMHH24:MI:SS') as last_changed_date
  FROM tan t
  JOIN tan_history h ON t.tan = h.tan
  JOIN tan_changeset c ON h.changeset = c.id
 GROUP BY t.tan, t.status, t.group_id, t.duration_days,
       t.owner_id, t.expiration_date, t.additional_info,
       c.user_id
 ORDER BY tan ASC;
COMMIT;

-- wie tan_view, aber ohne Gruppierung nach Änderungssatz
BEGIN TRANSACTION;
DROP VIEW IF EXISTS tan_view_all;
CREATE OR REPLACE VIEW tan_view_all AS
SELECT t.tan, t.status, t.group_id, t.duration_days,
       t.owner_id, 
       TO_CHAR(t.expiration_date, 'DD.MM.YYYY') as expiration_date,
       t.additional_info,
       h.changeset,
       c.user_id changed_by,
       TO_CHAR(c.date, 'YYYY-MM-DD FMHH24:MI:SS') as last_changed_date
  FROM tan t
  JOIN tan_history h ON t.tan = h.tan
  JOIN tan_changeset c ON h.changeset = c.id
 ORDER BY h.changeset DESC;
ALTER VIEW public.tan_view_all OWNER TO "www-data";
COMMIT;

-- View für die Historie einer einzelnen TAN
BEGIN TRANSACTION;
DROP VIEW IF EXISTS tan_history_view;
CREATE OR REPLACE VIEW tan_history_view AS
SELECT c.id as changeset,
       t.tan,
       h.status,
       h.owner_id,
       c.user_id changed_by,
       TO_CHAR(c.date, 'YYYY-MM-DD FMHH24:MI:SS') as last_changed_date,
       c.additional_info
  FROM tan_changeset c
  JOIN tan_history h ON c.id = h.changeset
  JOIN tan t ON h.tan = t.tan
 ORDER BY changeset DESC;
COMMIT;

-- für (globale) "Letzte Änderungen"
BEGIN TRANSACTION;
DROP VIEW IF EXISTS tan_changesets_view;
CREATE OR REPLACE VIEW tan_changesets_view AS
SELECT c.id changeset,
       c.user_id,
       TO_CHAR(c.date, 'YYYY-MM-DD FMHH24:MI:SS') as last_changed_date,
       t.group_id,
       Count(t.tan) tan_quantity
  FROM tan_changeset c
  JOIN tan_history h ON h.changeset = c.id
  JOIN tan t ON h.tan = t.tan
 GROUP BY t.group_id, c.id
 ORDER BY changeset DESC, group_id ASC;
COMMIT;

BEGIN TRANSACTION;
-- Sortierte Liste der Statuswerte
CREATE OR REPLACE VIEW tan_status_view AS
SELECT name from tan_status
 ORDER BY sortkey;

-- Statuswerte mit Statistik über Verwendung
CREATE OR REPLACE VIEW tan_status_summary_view AS
SELECT s.name AS status,
       Max(s.description) AS description,
       Count(t.tan) AS quantity
  FROM tan_status s
  LEFT JOIN tan t
       ON s.name = t.status
 GROUP BY s.name, s.sortkey
 ORDER BY s.sortkey;

-- Kandidaten zum Ablaufen
CREATE OR REPLACE VIEW tan_expire_candidates_view AS
SELECT tan, status, expiration_date
  FROM tan
 WHERE expiration_date <= current_date
   AND status in ('new', 'reserved');
COMMIT;

-- Reparatur: Korrektur der unter einem anderen Benutzer erzeugten Views
-- (aufzurufen durch diesen Benutzer)
BEGIN TRANSACTION;
ALTER VIEW public.tan_changeset_view OWNER TO "www-data";
ALTER VIEW public.tan_changesets_view OWNER TO "www-data";
ALTER VIEW public.tan_expire_candidates_view OWNER TO "www-data";
ALTER VIEW public.tan_history_view OWNER TO "www-data";
ALTER VIEW public.tan_status_summary_view OWNER TO "www-data";
ALTER VIEW public.tan_status_view OWNER TO "www-data";
ALTER VIEW public.tan_view OWNER TO "www-data";
COMMIT;

BEGIN TRANSACTION;
DROP VIEW IF EXISTS tan_groups_with_tans_view;
CREATE OR REPLACE VIEW tan_groups_with_tans_view AS
SELECT DISTINCT group_id
  FROM tan
 ORDER BY group_id;
ALTER VIEW public.tan_groups_with_tans_view OWNER TO "www-data";
COMMIT;

-- bis hierhin integriert in schema.sql
