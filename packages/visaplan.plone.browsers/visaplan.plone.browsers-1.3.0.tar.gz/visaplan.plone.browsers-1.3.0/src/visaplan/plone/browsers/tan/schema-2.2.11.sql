-- Tabellen für den Browser unitracc@@tan -*- coding: utf-8 -*- vim: et ic sw=4 sts=4 ts=4 si

-- Statuswerte
-- Table: tan_status

-- DROP TABLE tan_status;

CREATE TABLE tan_status
(
  name character varying(10) NOT NULL,    -- engl. Kurzbezeichnung des Status
  description text,
  CONSTRAINT tan_status_pkey PRIMARY KEY (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tan_status
  OWNER TO "www-data";
COMMENT ON COLUMN tan_status.name IS 'engl. Kurzbezeichnung des Status';


-- Transaktionsnummern
-- Table: tan

-- DROP TABLE tan;

CREATE TABLE tan
(
  tan_stem integer NOT NULL,        -- TAN ohne Prüfziffern
  tan integer,                      -- TAN mit Prüfziffern
  status character varying(10) NOT NULL,   -- Fremdschlüssel zu tan_status.name
  group_id character varying(50)    -- Gruppen-ID; enthält oft nach dem Präfix group_ die UID eines Objekts
                 NOT NULL,
  duration_days integer DEFAULT 31, -- Gültigkeitsdauer (der vermittelten Zuweisung) in Tagen
  owner_id character varying(50),   -- Benutzer-ID des Benutzers, für den die TAN eingelöst wurde
  expiration_date date NOT NULL,    -- Tag, ab dem die TAN nicht mehr eingelöst werden kann
  CONSTRAINT tan_pkey PRIMARY KEY (tan_stem),
  CONSTRAINT tan_unique UNIQUE (tan),
  CONSTRAINT tan_status_fkey FOREIGN KEY (status)
      REFERENCES tan_status (name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tan
  OWNER TO "www-data";
COMMENT ON COLUMN tan.tan_stem IS 'TAN ohne Prüfziffern';
COMMENT ON COLUMN tan.tan IS 'TAN mit Prüfziffern';
COMMENT ON COLUMN tan.status IS 'Fremdschlüssel zu tan_status.name';
COMMENT ON COLUMN tan.group_id IS 'Gruppen-ID; enthält oft nach dem Präfix group_ die UID eines Objekts';
COMMENT ON COLUMN tan.duration_days IS 'Gültigkeitsdauer (der vermittelten Zuweisung) in Tagen';
COMMENT ON COLUMN tan.owner_id IS 'Benutzer-ID des Benutzers, für den die TAN eingelöst wurde';
COMMENT ON COLUMN tan.expiration_date IS 'Tag, ab dem die TAN nicht mehr eingelöst werden kann';


-- Änderungsverfolgung: pro "Transaktion"
-- Table: tan_changeset

-- DROP TABLE tan_changeset;

CREATE TABLE tan_changeset
(
  id serial NOT NULL,
  user_id character varying(50) NOT NULL, -- ID des ausführenden Benutzers
  date timestamp without time zone NOT NULL DEFAULT now(),
  CONSTRAINT tan_changes_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tan_changeset
  OWNER TO "www-data";
COMMENT ON TABLE tan_changeset
  IS 'Faßt Änderungen zusammen, die in einer (Plone-) Transaktion getätigt werden';
COMMENT ON COLUMN tan_changeset.user_id IS 'ID des ausführenden Benutzers';



-- Änderungsverfolgung: pro Transaktionsnummer (TAN)
-- Table: tan_history

-- DROP TABLE tan_history;

CREATE TABLE tan_history
(
  id serial NOT NULL,
  tan integer NOT NULL,             -- Fremdschlüssel zur Tabelle tan
  changeset integer NOT NULL,       -- Fremdschlüssel zur Tabelle tan_changeset
  status_old character varying (10),               -- Fremdschlüssel zur Tabelle tan_status
  status_new character varying (10) NOT NULL,      -- Fremdschlüssel zur Tabelle tan_status
  status_hint text,                 -- Hinweistext, z. B. die Mail-Adresse, für die die TAN erzeugt wurde
  owner_id character varying(50),   -- Bei Einlösung die ID des zugewiesenen Benutzers
  CONSTRAINT tan_history_pkey PRIMARY KEY (id),
  CONSTRAINT tan_history_fkey_changeset FOREIGN KEY (changeset)
      REFERENCES tan_changeset (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT tan_history_fkey_new_status FOREIGN KEY (status_new)
      REFERENCES tan_status (name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT tan_history_fkey_old_status FOREIGN KEY (status_old)
      REFERENCES tan_status (name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT tan_history_fkey_tan FOREIGN KEY (tan)
      REFERENCES tan (tan) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT tan_history_unique UNIQUE (changeset, tan)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tan_history
  OWNER TO "www-data";
COMMENT ON TABLE tan_history
  IS 'Änderungsverlauf für Transaktionsnummern';
COMMENT ON COLUMN tan_history.tan IS 'Fremdschlüssel zur Tabelle tan';
COMMENT ON COLUMN tan_history.status_old IS 'Fremdschlüssel zur Tabelle tan_status';
COMMENT ON COLUMN tan_history.status_new IS 'Fremdschlüssel zur Tabelle tan_status';
COMMENT ON COLUMN tan_history.status_hint IS 'Hinweistext, z. B. die Mail-Adresse, für die die TAN erzeugt wurde';
COMMENT ON COLUMN tan_history.owner_id IS 'Bei Einlösung die ID des zugewiesenen Benutzers';
COMMENT ON COLUMN tan_history.changeset IS 'Fremdschlüssel zur Tabelle tan_changeset';


-- Funktionen
-- Function: get_random_number(integer, integer)

-- DROP FUNCTION get_random_number(integer, integer);

CREATE OR REPLACE FUNCTION get_random_number(integer, integer)
  RETURNS integer AS
$BODY$
DECLARE
    start_int ALIAS FOR $1;
    end_int ALIAS FOR $2;
BEGIN
    RETURN trunc(random() * (end_int-start_int) + start_int);
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION get_random_number(integer, integer)
  OWNER TO "www-data";

-- Function: get_check_digits(integer)

-- DROP FUNCTION get_check_digits(integer);

CREATE OR REPLACE FUNCTION get_check_digits(stem integer)
  RETURNS smallint AS
$BODY$declare
  sum int := 0;
  x int;
  digit int;
  primes int[] := array [17, 13, 11, 7, 5, 3, 2];
begin
  foreach x in array primes
  loop
    digit := stem % 10;
    stem := stem / 10;
    sum := sum + digit * x;
  end loop;
  return 99 - (sum % 100);
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION get_check_digits(integer)
  OWNER TO "www-data";

-- Function: tf_create_tan()

-- DROP FUNCTION tf_create_tan();

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
  new.status := 'new';
  return new;
end if;
end;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tf_create_tan()
  OWNER TO "www-data";

-- Trigger: tan_create_trigger on tan

-- DROP TRIGGER tan_create_trigger ON tan;

CREATE TRIGGER tan_create_trigger
  BEFORE INSERT
  ON tan
  FOR EACH ROW
  EXECUTE PROCEDURE tf_create_tan();


-- Trigger-Funktionen: http://www.postgresql.org/docs/9.1/static/plpgsql-trigger.html
