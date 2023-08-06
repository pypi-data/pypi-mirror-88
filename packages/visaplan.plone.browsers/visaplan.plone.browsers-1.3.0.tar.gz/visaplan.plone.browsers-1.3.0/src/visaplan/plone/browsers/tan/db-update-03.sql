-- Änderungen relativ zu schema-2.2.13.sql und db-update-02.sql vom 24.3.2014

-- für (globale) "Letzte Änderungen"
BEGIN TRANSACTION;
DROP VIEW IF EXISTS tan_changesets_view;
CREATE OR REPLACE VIEW tan_changesets_view AS
SELECT c.id changeset,
       c.user_id as changed_by,
       TO_CHAR(c.date, 'YYYY-MM-DD FMHH24:MI:SS') as last_changed_date,
       t.group_id,
       Count(t.tan) tan_quantity
  FROM tan_changeset c
  JOIN tan_history h ON h.changeset = c.id
  JOIN tan t ON h.tan = t.tan
 GROUP BY t.group_id, c.id
 ORDER BY changeset DESC, group_id ASC;
COMMIT;
ALTER VIEW public.tan_changesets_view OWNER TO "www-data";

BEGIN TRANSACTION;
DROP VIEW IF EXISTS tan_view;
CREATE OR REPLACE VIEW tan_view AS
SELECT DISTINCT
       t.tan, t.status, t.group_id, t.duration_days,
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
 ORDER BY changeset DESC;
COMMIT;
ALTER VIEW public.tan_view OWNER TO "www-data";

ALTER TABLE public.unitracc_booking_states OWNER TO "www-data";
ALTER TABLE public.unitracc_coursestatistics OWNER TO "www-data";
ALTER TABLE public.unitracc_orders OWNER TO "www-data";
ALTER TABLE public.unitracc_orders_articles OWNER TO "www-data";
ALTER TABLE public.unitracc_orders_paypal OWNER TO "www-data";
ALTER TABLE public.unitracc_payment_types OWNER TO "www-data";

-- 28.04.2014: übergebenen Wert für status berücksichtigen
CREATE OR REPLACE FUNCTION tf_create_tan()
  RETURNS trigger AS
$BODY$begin
if TG_OP = 'INSERT' then
  new.tan_stem := get_random_number(1000000, 9999999);
  if new.tan_stem < 1000000 then
    raise exception 'TAN-Basiswert zu klein (%s)', new.tan_stem;
  end if;
  if new.tan_stem > 9999999 then
    raise exception 'TAN-Basiswert zu groß (%s)', new.tan_stem;
  end if;
  new.tan := new.tan_stem * 100 + get_check_digits(new.tan_stem);
  if new.status is NULL then
    new.status := 'new';
  end if;
  return new;
end if;
end;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tf_create_tan()
  OWNER TO "www-data";

