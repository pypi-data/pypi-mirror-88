-- Schema-Update für Unitracc
BEGIN;

DROP VIEW tan_view;
DROP VIEW tan_view_all;

-- View: tan_view_inner

CREATE VIEW tan_view_inner AS
 SELECT t.tan,
        t.status,
        t.group_id,
        t.duration_days,
        t.owner_id,
        t.expiration_date,
        t.additional_info,
        h.changeset,
        c.user_id AS changed_by,
        c.date AS changed_date
   FROM tan t
   JOIN tan_history h ON t.tan = h.tan
   JOIN tan_changeset c ON h.changeset = c.id
  ORDER BY h.changeset DESC, t.tan ASC;
COMMENT ON VIEW tan_view_inner IS
  'Basis-Sicht auf TANs, nur mit JOINs; ohne Änderungsdatum';

ALTER TABLE tan_view_inner
  OWNER TO "www-data";


CREATE VIEW tan_view_grouped AS
 SELECT DISTINCT
        tan,
        status,
        group_id,
        duration_days,
        owner_id,
        expiration_date,
        additional_info,
        max(changeset) AS changeset
   FROM tan_view_inner
  GROUP BY tan,
        status,
        group_id,
        duration_days,
        owner_id,
        expiration_date,
        additional_info;
COMMENT ON VIEW tan_view_grouped IS
  'Gruppierte Sicht auf TANs, jeweils mit der letzten Änderung; ohne Änderungsdatum';

ALTER TABLE tan_view_grouped
  OWNER TO "www-data";


-- View: tan_view

CREATE VIEW tan_view AS
 SELECT DISTINCT
        tan,
        status,
        group_id,
        duration_days,
        owner_id,
        to_char(expiration_date::timestamp with time zone,
                'DD.MM.YYYY'::text) AS expiration_date,
        v.additional_info,
        changeset,
        c.user_id AS changed_by,
        to_char(c.date,
                'YYYY-MM-DD FMHH24:MI:SS'::text) AS last_changed_date
   FROM tan_view_grouped v
   JOIN tan_changeset c on v.changeset = c.id
  GROUP BY tan,
        status,
        group_id,
        duration_days,
        owner_id,
        expiration_date,
        v.additional_info,
        changeset,
        changed_by,
        last_changed_date;
COMMENT ON VIEW tan_view IS
  'Alle TANs mit den jeweiligen letzten Änderungen, auf der Basis von tan_view_grouped';

ALTER TABLE tan_view
  OWNER TO "www-data";

-- View: tan_view_all


CREATE VIEW tan_view_all AS
 SELECT DISTINCT
        tan,
        status,
        group_id,
        duration_days,
        owner_id,
        to_char(expiration_date::timestamp with time zone,
                'DD.MM.YYYY'::text) AS expiration_date,
        v.additional_info,
        changeset,
        changed_by,
        to_char(c.date,
                'YYYY-MM-DD FMHH24:MI:SS'::text) AS last_changed_date
   FROM tan_view_inner v
   JOIN tan_changeset c on v.changeset = c.id;
COMMENT ON VIEW tan_view_all IS
  'Alle TANs mit *allen* Änderungssätzen, auf der Basis von tan_view_inner';

ALTER TABLE tan_view_all
  OWNER TO "www-data";


-- View: tan_history_view: obsolet?

COMMIT;

