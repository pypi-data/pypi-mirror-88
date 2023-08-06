BEGIN TRANSACTION;  /* -*- coding: utf-8 -*- vim: expandtab sw=4 sts=4 si
Schemaerweiterungen für das Buchungssystem:
- Unterstützung von Rabatten

Übersicht über diese SQL-Datei (gemäß Bereichskommentaren):

- neue Hilfstabellen
  - unterstützte Sprachkürzel
  - Rabattgruppen
  - Texte für Rabatte
  - Verarbeitung von Artikeldaten
- Spaltentypen ändern
  - Sicht orders_articles_view löschen
  - character varying --> text
  - numerischer Datentyp für Geldbeträge
  - gelöschte Sicht wiederherstellen
- weitere neue Felder in Bestandstabellen
- Ermittlung etwaiger Rabatte
  - Hilfs-Sichten für articles_discount_view
    - erreichte Rabattstufe pro Rabattgruppe
    - Anwendung der Rabattstufen je MwSt-Gruppe
  - articles_discount_view
- Berechnung der Mehrwertsteuer
  - articles_vat_view
- Aktualisierung der Bestandsdaten
  - Operationen der Trigger-Funktion tf_articles_addmissing
- Integrität neuer Daten

Entsprechende Aktualisierungen der Bestandsdaten folgen nochmals in update-0003.sql;
Zurücksetzung der Änderungen (zur erneuten Anwendung einer aktualisierten Fassung)
in update-0002-undo.sql


Sichten für unitracc_orders_articles:
 (1) articles_items_view
 (5) articles_discount_view
 (7) articles_netsum_view
(10) articles_vat_view
(15)

*/

-------------------------------------------- [ neue Hilfstabellen ... [
-- (incl. entsprechender neuer Felder der Bestandstabellen)

-------------------------------- [ unterstützte Sprachkürzel ... [
-- Table: unitracc_language

-- DROP TABLE unitracc_language;

CREATE TABLE unitracc_language (
  la character varying(2) NOT NULL, -- Sprachkürzel, z. B. 'de'
  CONSTRAINT unitracc_language_pkey PRIMARY KEY (la)
  -- erstellt implizit einen Index »unitracc_language_pkey«
) WITH (
  OIDS=FALSE
);
ALTER TABLE unitracc_language
  OWNER TO "www-data";
COMMENT ON TABLE unitracc_language
  IS 'Verfügbare Sprachcodes, z. B. für unitracc_discount_group_texts.
';
COMMENT ON COLUMN unitracc_language.la
  IS 'Sprachkürzel, z. B. ''de''';

INSERT INTO unitracc_language (la)
  VALUES ('de'), ('en');

-- Column: la
-- ALTER TABLE unitracc_orders DROP COLUMN la;

ALTER TABLE unitracc_orders ADD COLUMN la character varying(2);
COMMENT ON COLUMN unitracc_orders.la
  IS 'Sprachkürzel (neu ab 2/2018)';

-- Foreign Key: unitracc_orders_la_fkey
-- ALTER TABLE unitracc_orders DROP CONSTRAINT unitracc_orders_la_fkey;

ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_la_fkey FOREIGN KEY (la)
      REFERENCES unitracc_language (la) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;
-------------------------------- ] ... unterstützte Sprachkürzel ]

-------------- [ weitere neue Felder für die Buchungstabelle ... [
ALTER TABLE unitracc_orders
  ADD COLUMN dirty boolean NOT NULL DEFAULT true;
COMMENT ON COLUMN unitracc_orders.dirty
  IS 'Wenn dirty gesetzt (z. B. durch Hinzufügen eines Artikels; siehe Trigger tr_articles_dirty), muß die Berechnung von Rabatten und Mehrwertsteuer etc. wiederholt werden';
-- dadurch wird das Feld für die bisherigen Datensätze auf true gesetzt;
-- für neue Datensätze den Vorgabewert ändern:
ALTER TABLE unitracc_orders
  ALTER COLUMN dirty SET DEFAULT false;

ALTER TABLE unitracc_orders
  ADD COLUMN adminid TEXT;
COMMENT ON COLUMN unitracc_orders.adminid
  IS 'Benutzer-ID des Administrators, wenn Auftrag im Backend angelegt';
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_adminid_check_50
  CHECK (length(adminid) <= 50);

------------------------------ [ neue numerische Felder ... [
-- (noch ohne Vorgabewerte und Constraints)
ALTER TABLE unitracc_orders
  ADD COLUMN net_total NUMERIC(10, 2) NOT NULL DEFAULT 0;
COMMENT ON COLUMN unitracc_orders.net_total
  IS 'Summe der multiplizierten Nettobeträge aus unitracc_orders_articles,
unter Berücksichtigung etwaiger Rabatte';
ALTER TABLE unitracc_orders
  ADD COLUMN vat_total NUMERIC(10, 2) NOT NULL DEFAULT 0;
COMMENT ON COLUMN unitracc_orders.vat_total
  IS 'Summe der Mehrwertsteuerbeträge, die sich aus unterschiedlichen MwSt-Sätzen berechnen können';
ALTER TABLE unitracc_orders
  ADD COLUMN total NUMERIC(10, 2) NOT NULL DEFAULT 0;
COMMENT ON COLUMN unitracc_orders.total
  IS 'Gesamtsumme; Summe von net_total und vat_total (neu ab März 2018)';
------------------------------ ] ... neue numerische Felder ]

ALTER TABLE unitracc_orders
  ALTER COLUMN payment_type_id SET DEFAULT 1; -- 'prepayment'
-- wurde bisher umständlich in Anwendungscode gesetzt:
ALTER TABLE unitracc_orders
  ALTER COLUMN booking_states_id SET DEFAULT 1;  -- 'new'

-- dieses Feld enthält bislang nichts sinnvolles ...
-- (irreversible Aufräumaktion)
UPDATE unitracc_orders
   SET additional_info = NULL
 WHERE trim(additional_info) = ''
    OR (userid = 'david.regesch' and additional_info = 'YYY')
    OR (userid = 'therp' and additional_info = 'Unter dem Dach rechts');

-------------- ] ... weitere neue Felder für die Buchungstabelle ]

-------------------------------------------- [ Rabattgruppen ... [
-- Table: unitracc_discount_group
-- DROP TABLE unitracc_discount_group;

CREATE TABLE unitracc_discount_group (
  key TEXT NOT NULL,
  description TEXT, -- Beschreibungstext der Objekte, die in dieser Rabattgruppe zusammengefaßt werden
  CONSTRAINT unitracc_discount_group_pkey PRIMARY KEY (key)
  -- erstellt implizit einen Index »unitracc_discount_group_pkey«
) WITH (
  OIDS=FALSE
);
ALTER TABLE unitracc_discount_group
  OWNER TO "www-data";
COMMENT ON TABLE unitracc_discount_group
  IS 'Rabattgruppen (neu im Februar 2018): Bestellposten derselben Rabattgruppe werden für die Berechnung der Rabattstufe zusammengefaßt (drei Buchungen desselben Kurses werden genauso behandelt wie drei Einzelbuchungen unterschiedlicher Kurse)
';
COMMENT ON COLUMN unitracc_discount_group.description
  IS 'Beschreibungstext der Objekte, die in dieser Rabattgruppe zusammengefaßt werden';

INSERT INTO unitracc_discount_group (key, description)
VALUES ('course', 'Kursobjekte'),
       ('enterprise', 'Unternehmens-Pakete'),
       ('test', '(für Test-Datensätze)');

-------------------------------------------- ] ... Rabattgruppen ]


---------------------------------------- [ Texte für Rabatte ... [
-- Table: unitracc_discount_group_texts

-- DROP TABLE unitracc_discount_group_texts;

CREATE TABLE unitracc_discount_group_texts (
  discount_group TEXT NOT NULL,
  la TEXT NOT NULL,
  text_normal TEXT, -- Text für den Normalfall, daß für die Rabattgruppe <key> nur ein Mehrwertsteuersatz vorkommt und dieser nicht 0 ist
  text_with_vat TEXT, -- Text für den Fall, daß für die Rabattgruppe <key> mehrere Mehrwertsteuersätze vorkommen und dieser hier nicht 0 ist
  text_zero_vat TEXT, -- Text für den Fall, daß für die Rabattgruppe mehrere Mehrwertsteuersätze vorkommen und dieser hier 0 ist
  CONSTRAINT unitracc_discount_group_texts_pkey PRIMARY KEY (discount_group, la),
  -- erstellt implizit einen Index »unitracc_discount_group_texts_pkey«
  CONSTRAINT unitracc_discount_group_texts_discount_group_fkey FOREIGN KEY (discount_group)
      REFERENCES unitracc_discount_group (key) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT unitracc_discount_group_texts_la_fkey FOREIGN KEY (la)
      REFERENCES unitracc_language (la) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
) WITH (
  OIDS=FALSE
);
ALTER TABLE unitracc_discount_group_texts
  OWNER TO "www-data";
COMMENT ON TABLE unitracc_discount_group_texts
  IS 'Hilfstabelle für Rabattgruppen (neu im Februar 2018): stellt für jede erlaubte Kombination von Rabattgruppe und Sprachkürzel Texte bereit, die mit Hilfe der format-Funktion verarbeitet werden können (siehe die Besschreibungen der text_-Felder)';
COMMENT ON COLUMN unitracc_discount_group_texts.text_normal
  IS 'Text für den Normalfall, daß für die Rabattgruppe <key> nur ein Mehrwertsteuersatz vorkommt und dieser nicht 0 ist';
COMMENT ON COLUMN unitracc_discount_group_texts.text_with_vat
  IS 'Text für den Fall, daß für die Rabattgruppe <key> mehrere Mehrwertsteuersätze vorkommen und dieser hier nicht 0 ist';
COMMENT ON COLUMN unitracc_discount_group_texts.text_zero_vat
  IS 'Text für den Fall, daß für die Rabattgruppe mehrere Mehrwertsteuersätze vorkommen und dieser hier 0 ist';

------------------------------------ ] ... Texte für Rabatte ... [
INSERT INTO unitracc_discount_group_texts
  (discount_group, la,
   text_normal,
   text_with_vat,
   text_zero_vat)
VALUES
  ('course', 'de',
   '%s%% Rabatt für mindestens %s Kursmodule',
   '%s%% Rabatt, mindestens %s Kursmodule (für jene mit %s%% MwSt)',
   '%s%% Rabatt, mindestens %s Kursmodule (für von der MwSt. befreite)'),
  ('enterprise', 'de',
   '%s%% Rabatt für mindestens %s Weiterbildungspakete',
   '%s%% Rabatt, mindestens %s Weiterbildungspakete (für jene mit %s%% MwSt)',
   '%s%% Rabatt, mindestens %s Weiterbildungspakete (für von der MwSt. befreite)'),
  ('test', 'de',
   '%s%% Rabatt für mindestens %s Test-Dingse',
   '%s%% Rabatt, mindestens %s Test-Dingse (für jene mit %s%% MwSt)',
   '%s%% Rabatt, mindestens %s Test-Dingse (für von der MwSt. befreite)'),
  ('course', 'en',
   '%s%% discount for at least %s course modules',
   '%s%% discount, at least %s course modules (for those with %s%% VAT)',
   '%s%% discount, at least %s course modules (for those without VAT)'),
  ('enterprise', 'en',
   '%s%% discount for at least %s enterprise packages',
   '%s%% discount, at least %s enterprise packages (for those with %s%% VAT)',
   '%s%% discount, at least %s enterprise packages (for those without VAT)'),
  ('test', 'en',
   '%s%% discount for at least %s test thingies',
   '%s%% discount, at least %s test thingies (for those with %s%% VAT)',
   '%s%% discount, at least %s test thingies (for those without VAT)');
---------------------------------------- ] ... Texte für Rabatte ]


--------------------------------- [ Texte für Mehrwertsteuer ... [
-- Table: unitracc_vat_texts

-- DROP TABLE unitracc_vat_texts;

CREATE TABLE unitracc_vat_texts (
  la TEXT NOT NULL,
  text_normal TEXT, -- eventuell wird es noch weitere geben
  CONSTRAINT unitracc_vat_texts_pkey PRIMARY KEY (la),
  CONSTRAINT unitracc_vat_texts_la_fkey FOREIGN KEY (la)
      REFERENCES unitracc_language (la) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
) WITH (
  OIDS=FALSE
);
ALTER TABLE unitracc_vat_texts
  OWNER TO "www-data";
COMMENT ON TABLE unitracc_vat_texts
  IS 'Hilfstabelle für Mehrwertsteuer (neu im Februar 2018; für articles_vat_view): stellt für jedes Sprachkürzel den Text zur Angabe der Mehrwertsteuer bereit (analog zu unitracc_discount_group_texts; bislang gibt es hier jedoch nur je einen Text)';

----------------------------- ] ... Texte für Mehrwertsteuer ... [
INSERT INTO unitracc_vat_texts
  (la,
   text_normal)
VALUES
  ('de', '%s%% MwSt.'),
  ('en', '%s%% VAT');
--------------------------------- ] ... Texte für Mehrwertsteuer ]


---------------------------- [ Verarbeitung von Artikeldaten ... [
-- Table: unitracc_orders_calc_steps

-- DROP TABLE unitracc_orders_calc_steps;

CREATE TABLE unitracc_orders_calc_steps (
  id smallint NOT NULL,
  description TEXT NOT NULL, -- reines Beschreibungsfeld
  CONSTRAINT unitracc_orders_calc_steps_pkey PRIMARY KEY (id)
  -- erstellt implizit einen Index »unitracc_orders_calc_steps_pkey«
) WITH (
  OIDS=FALSE
);
ALTER TABLE unitracc_orders_calc_steps
  OWNER TO "www-data";
COMMENT ON TABLE unitracc_orders_calc_steps
  IS 'Schritte bei automatischen Ergänzung berechneter Zeilen in unitracc_orders_articles; siehe Feld "description"';
COMMENT ON COLUMN unitracc_orders_calc_steps.description
  IS 'reines Beschreibungsfeld';

INSERT INTO unitracc_orders_calc_steps
  (id, description)
VALUES (1, 'Explizit in den Einkaufswagen gelegte Artikel'),
       (5, 'Berechnung etwaiger Rabatte'),
       (7, 'Berechnung der Nettosumme, nach Rabatten'),
      (10, 'Berechnung der Steuern'),
      (15, 'Berechnung der Gesamtsumme');

ALTER TABLE unitracc_orders_articles
  ADD COLUMN step smallint NOT NULL DEFAULT 1;
ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_step_fkey FOREIGN KEY (step)
      REFERENCES unitracc_orders_calc_steps (id)
      ON UPDATE NO ACTION ON DELETE NO ACTION;
COMMENT ON COLUMN unitracc_orders_articles.step
  IS '1 für explizit hinzugefügte Artikel; größere Werte für berechnete Zeilen';
---------------------------- ] ... Verarbeitung von Artikeldaten ]

--------------------------- [ Texte für Buchungsverarbeitung ... [

-- Table: unitracc_orders_calc_step_texts

-- DROP TABLE unitracc_orders_calc_step_texts;

CREATE TABLE unitracc_orders_calc_step_texts
(
  text_id serial NOT NULL, -- numerischer Index; nur für Tabellenpflege
  la text NOT NULL, -- Das Sprachkürzel
  step smallint,
  step_text text NOT NULL, -- Die Nutzlast
  CONSTRAINT unitracc_booking_step_texts_pkey PRIMARY KEY (text_id),
  CONSTRAINT unitracc_booking_step_texts_la_fkey FOREIGN KEY (la)
      REFERENCES unitracc_language (la) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT unitracc_booking_step_texts_step_fkey FOREIGN KEY (step)
      REFERENCES unitracc_orders_calc_steps (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT unitracc_orders_calc_step_texts_la_step_key UNIQUE (la, step)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE unitracc_orders_calc_step_texts
  OWNER TO "www-data";
COMMENT ON TABLE unitracc_orders_calc_step_texts
  IS 'Texte für die Generierung der berechneten Zeilen in unitracc_orders_articles';
COMMENT ON COLUMN unitracc_orders_calc_step_texts.text_id IS 'numerischer Index; nur für Tabellenpflege';
COMMENT ON COLUMN unitracc_orders_calc_step_texts.la IS 'Das Sprachkürzel';
COMMENT ON COLUMN unitracc_orders_calc_step_texts.step_text IS 'Die Nutzlast';

----------------------- ] ... Texte für Buchungsverarbeitung ... [

INSERT INTO unitracc_orders_calc_step_texts
  (text_id, la, step, step_text)
VALUES
  (10, 'de',  1, 'XXX Hier gehört der article_title hin! XXX'),
  (11, 'en',  1, 'XXX Please use the article_title! XXX'),
  (50, 'de',  5, 'XXX Bitte Werte aus unitracc_discount_group_texts verwenden! XXX'),
  (51, 'en',  5, 'XXX Please use values from unitracc_discount_group_texts! XXX'),
  (70, 'de',  7, 'Nettosumme'),
  (71, 'en',  7, 'Net amount'),
 (100, 'de', 10, 'XXX Bitte Werte aus unitracc_vat_texts verwenden! XXX'),
 (101, 'en', 10, 'XXX Please use values from unitracc_vat_texts! XXX'),
 (150, 'de', 15, 'Gesamtsumme'),
 (151, 'en', 15, 'Total amount');
--------------------------- ] ... Texte für Buchungsverarbeitung ]


-------------------------------------------- ] ... neue Hilfstabellen ]

------------------------------------------- [ Spaltentypen ändern ... [
DROP VIEW IF EXISTS orders_articles_view;
DROP VIEW IF EXISTS user_bookings_view;
DROP VIEW IF EXISTS orders_view;
DROP VIEW IF EXISTS latest_paypal_record_view;
DROP VIEW IF EXISTS bookings_view;

------------------------------- [ character varying --> text ... [
ALTER TABLE unitracc_orders
  ALTER COLUMN ordernr TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_ordernr_check_50
  CHECK (length(ordernr) <= 50);

ALTER TABLE unitracc_orders
  ALTER COLUMN userid TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_userid_check_50
  CHECK (length(userid) <= 50);

ALTER TABLE unitracc_orders
  ALTER COLUMN sessionid TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_sessionid_check_150
  CHECK (length(sessionid) <= 150);

ALTER TABLE unitracc_orders
  ALTER COLUMN ip TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_ip_check_15
  CHECK (length(ip) <= 15);

ALTER TABLE unitracc_orders
  ALTER COLUMN firstname TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_firstname_check_50
  CHECK (length(firstname) <= 50);

ALTER TABLE unitracc_orders
  ALTER COLUMN lastname TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_lastname_check_50
  CHECK (length(lastname) <= 50);

ALTER TABLE unitracc_orders
  ALTER COLUMN company TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_company_check_150
  CHECK (length(company) <= 150);

ALTER TABLE unitracc_orders
  ALTER COLUMN street TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_street_check_150
  CHECK (length(street) <= 150);

ALTER TABLE unitracc_orders
  ALTER COLUMN zip TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_zip_check_50
  CHECK (length(zip) <= 50);

ALTER TABLE unitracc_orders
  ALTER COLUMN city TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_city_check_100
  CHECK (length(city) <= 100);

ALTER TABLE unitracc_orders
  ALTER COLUMN country TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_country_check_200
  CHECK (length(country) <= 200);

ALTER TABLE unitracc_orders
  ALTER COLUMN additional_info TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_additional_info_check_50
  CHECK (length(additional_info) <= 50);

ALTER TABLE unitracc_orders
  ALTER COLUMN currency TYPE TEXT;
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_currency_check_10
  CHECK (length(currency) <= 10);

ALTER TABLE unitracc_orders
  ALTER COLUMN la TYPE TEXT;
/* nutzlos, und wg. Fremdschlüssels auch überflüssig:
ALTER TABLE unitracc_orders
  ADD CONSTRAINT unitracc_orders_la_check_2
  CHECK (length(la) <= 2);
*/

ALTER TABLE unitracc_orders_articles
  ALTER COLUMN article_uid TYPE TEXT;
ALTER TABLE unitracc_orders_articles
  ALTER COLUMN article_uid DROP NOT NULL;
-- wenn step > 1 ist, haben wir eine berechnete Zeile,
-- und damit keine UID:
ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_article_uid_check
  CHECK (step > 1 OR length(article_uid) <= 50);

ALTER TABLE unitracc_orders_articles
  ALTER COLUMN article_title TYPE TEXT;
ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_article_title_check_300
  CHECK (length(article_title) <= 300);
------------------------------- ] ... character varying --> text ]

ALTER TABLE unitracc_orders_articles
  ADD COLUMN group_id TEXT;
-- Gruppen-IDs wurden bisher zur Verknüpfung im Python-Code zusammengebastelt!
COMMENT ON COLUMN unitracc_orders_articles.group_id
  IS 'zumeist group_..._learner; bei berechneten Zeilen NULL';
UPDATE unitracc_orders_articles
  SET group_id = 'group_' || article_uid || '_learner'
  WHERE group_id IS NULL
    AND article_uid IS NOT NULL;
ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_group_id_check_50
  CHECK (length(group_id) <= 50);

--------------------- [ numerischer Datentyp für Geldbeträge ... [
ALTER TABLE unitracc_orders_articles
  ALTER COLUMN amount
  SET DATA TYPE NUMERIC(10, 2);
ALTER TABLE unitracc_orders_articles
  ALTER COLUMN amount SET NOT NULL;
ALTER TABLE unitracc_orders_articles
  ALTER COLUMN amount SET DEFAULT 0;
COMMENT ON COLUMN unitracc_orders_articles.amount
  IS 'Bei Zeilen mit step > 1 ist ausschließlich amount_multiplied interessant!';
ALTER TABLE unitracc_orders_articles
  ALTER COLUMN vat
  SET DATA TYPE NUMERIC(10, 2);

ALTER TABLE unitracc_orders_articles
  ADD COLUMN amount_multiplied NUMERIC(10, 2);
--------------------- ] ... numerischer Datentyp für Geldbeträge ]


------------------------------------------- ] ... Spaltentypen ändern ]

----------------------- [ weitere neue Felder in Bestandstabellen ... [

-- ALTER TABLE unitracc_orders_articles DROP COLUMN quantity;
ALTER TABLE unitracc_orders_articles
  ADD COLUMN quantity integer NOT NULL DEFAULT 1;

-- Gruppierungsfeld zur Berechnung von Rabatten:
ALTER TABLE unitracc_orders_articles
  ADD COLUMN discount_group TEXT;
ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_discount_group_fkey FOREIGN KEY (discount_group)
      REFERENCES unitracc_discount_group (key)
      ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_unitracc_orders_articles_discount_group_fkey
  ON unitracc_orders_articles(discount_group);


-- vat_percent ersetzt vat;
-- <https://www.postgresql.org/docs/current/static/datatype-numeric.html#DATATYPE-NUMERIC-DECIMAL>:
-- Column: vat_percent

-- ALTER TABLE unitracc_orders_articles DROP COLUMN vat_percent;

ALTER TABLE unitracc_orders_articles
  ADD COLUMN vat_percent NUMERIC(4, 2);
COMMENT ON COLUMN unitracc_orders_articles.vat_percent
  IS 'Mehrwertsteuersatz, zur Gruppierbarkeit';
COMMENT ON COLUMN unitracc_orders_articles.vat
  IS 'Mehrwertsteuerbetrag zu <amount> (ohne etwaige Multiplikation mit <quantity>.

Ist im Begriff, durch <vat_percent> und die separate Darstellung
der berechneten Felder (mit <step>-Werten größer 1; siehe unitracc_orders_calc_steps) abgelöst zu werden';

------------------------ [ Verknüpfung zu u.groupmemberships ... [

-- Diese Datensätze stehen dem UNIQUE-Constraint im Wege:
DELETE FROM unitracc_groupmemberships
 WHERE id IN (505, 506) AND member_id_ = 'therp';

/* erster Versuch ...
ALTER TABLE unitracc_groupmemberships
  ADD CONSTRAINT unitracc_groupmemberships_order_id_group_id__key
  UNIQUE(order_id, group_id_);
ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_orderid_fkey1 FOREIGN KEY (orderid, group_id)
      REFERENCES unitracc_groupmemberships (order_id, group_id_) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

Mit dem FOREIGN-KEY-Constraint wird das nichts; aber UNIQUE könnte etwas bringen:
*/
ALTER TABLE unitracc_orders_articles
  ADD CONSTRAINT unitracc_orders_articles_orderid_groupid__key
  UNIQUE(orderid, group_id);
ALTER TABLE unitracc_groupmemberships
  ADD CONSTRAINT unitracc_groupmemberships_orderid_groupid__key
  UNIQUE(order_id, group_id_);
------------------------ ] ... Verknüpfung zu u.groupmemberships ]



-- Kommentare zu Tabelle unitracc_orders:
COMMENT ON COLUMN unitracc_orders.ordernr
  IS 'Gegenwärtig noch in Python-Code erzeugt :-(';

----------------------- ] ... weitere neue Felder in Bestandstabellen ]

---------------------------------------------- [ neue Constraints ... [
-- perspektivisch die Verwendung der numerischen ID ablösen:
ALTER TABLE unitracc_payment_types
  ADD CONSTRAINT unitracc_payment_types_payment_type__key
  UNIQUE(payment_type);
ALTER TABLE unitracc_booking_states
  ADD CONSTRAINT unitracc_booking_states_booking_state__key
  UNIQUE(booking_state);
---------------------------------------------- ] ... neue Constraints ]

----------------------------------- [ Ermittlung etwaiger Rabatte ... [

----------------- [ Hilfs-Sichten für articles_discount_view ... [

-------------- [ erreichte Rabattstufe pro Rabattgruppe ... [
-- View: articles_discount_counting_view

-- DROP VIEW articles_discount_counting_view;

CREATE OR REPLACE VIEW articles_discount_counting_view AS
  WITH t as (
    SELECT a.orderid,
       sum(a.quantity) AS quantity_per_group,
       vat_percent,
       discount_group
      FROM unitracc_orders_articles a
     WHERE step = 1
     GROUP BY a.orderid,
              a.discount_group,
              a.vat_percent
  )
  SELECT t.orderid,
         sum(quantity_per_group) quantity_per_group,
         count(vat_percent) AS vat_percentages_per_group,
         discount_group
    FROM t
   GROUP BY t.orderid,
            t.discount_group;

ALTER TABLE articles_discount_counting_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_discount_counting_view
  IS 'Hilfs-Sicht für articles_discount_view:
Da es theoretisch möglich ist, daß Artikel derselben Rabattgruppe unterschiedliche Mehrwertsteuersätze haben
(zumindest ist es im System möglich, den MwSt-Satz (VAT) pro Objekt anzugeben),
die Anzahl sich aber unabhängig von solchen Unterschieden berechnet,
muß diese Anzahl vorab ermittelt werden.';

-------------- ] ... erreichte Rabattstufe pro Rabattgruppe ]

----------- [ Anwendung der Rabattstufen je MwSt-Gruppe ... [
-- View: articles_discount_inner_view

-- DROP VIEW articles_discount_inner_view;

CREATE OR REPLACE VIEW articles_discount_inner_view AS
 SELECT a.orderid,
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
        max(a.id) AS article_id,
        max(a.article_title::TEXT) AS article_title,
        a.vat_percent,
        sum(a.quantity * a.amount) AS amount,
        a.discount_group
   FROM articles_discount_counting_view cv
        LEFT JOIN unitracc_orders_articles a ON cv.orderid = a.orderid
                                            AND cv.discount_group = a.discount_group
  WHERE a.step = 1
  GROUP BY a.orderid,
           a.discount_group,
           a.vat_percent,
           cv.quantity_per_group,
           cv.vat_percentages_per_group;

ALTER TABLE articles_discount_inner_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_discount_inner_view
  IS 'Hilfs-Sicht für articles_discount_view:
Bereitstellung der Daten';
----------- ] ... Anwendung der Rabattstufen je MwSt-Gruppe ]
----------------- ] ... Hilfs-Sichten für articles_discount_view ]

------------------------------- ] ... Ermittlung etwaiger Rabatte ... [

----------------------------------- [ articles_discount_view ... [
CREATE OR REPLACE VIEW articles_discount_view AS
 WITH t AS (
 SELECT iv.orderid,
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
  IS 'Ausgabe der Rabatte, in Abhängigkeit von der numerischen Buchungsnummer (orderid) und der Ausgabesprache';
COMMENT ON COLUMN articles_discount_view.la
  IS 'Bei Verwendung dieser Sicht als Berechnungsgrundlage ist unbedingt nach "la" zu filtern!';
----------------------------------- ] ... articles_discount_view ]

----------------------------------- ] ... Ermittlung etwaiger Rabatte ]


-------------------- [ Berechnung der Zwischensumme (vor Steuern) ... [
CREATE OR REPLACE VIEW articles_netsum_view AS
  SELECT a.orderid,
         t.step_text AS article_title,
         sum(a.amount_multiplied) AS amount_multiplied,
         7 as step
    FROM unitracc_orders_articles a
         JOIN unitracc_orders                 o ON o.id = a.orderid
         JOIN unitracc_orders_calc_step_texts t ON t.la = o.la
                                               AND t.step = 7
   WHERE a.step < 7  -- Artikel und Rabatte
   GROUP BY a.orderid,
            t.step_text;
ALTER TABLE articles_netsum_view
  OWNER TO "www-data";


--------------------------------- [ Berechnung der Mehrwertsteuer ... [

----------------------------------- [ articles_vat_view ... [
CREATE OR REPLACE VIEW articles_vat_view AS
  WITH t1 AS (
    SELECT orderid,
           amount_multiplied,
           vat_percent
      FROM unitracc_orders_articles
     WHERE step = 1 OR step = 5
    ), t2 AS (
    SELECT orderid,
           sum(amount_multiplied) AS amount_multiplied,
           vat_percent
      FROM t1
     GROUP BY orderid, vat_percent
    )
  SELECT DISTINCT
         t2.orderid,
         CAST(t2.amount_multiplied * t2.vat_percent / 100.0 AS NUMERIC(10, 2)) AS amount_multiplied,
         t2.vat_percent,
         format(vt.text_normal, t2.vat_percent) AS article_title,
         10 AS step
    FROM t2
         JOIN unitracc_orders    uo ON t2.orderid = uo.id
         JOIN unitracc_vat_texts vt ON uo.la = vt.la
   ORDER BY t2.vat_percent;
ALTER TABLE articles_vat_view
  OWNER TO "www-data";
COMMENT ON VIEW articles_vat_view
  IS 'Ausgabe der Mehrwertsteuer, in Abhängigkeit von der numerischen Buchungsnummer (orderid)';
----------------------------------- ] ... articles_vat_view ]

--------------------------------- ] ... Berechnung der Mehrwertsteuer ]


------------------------------ [ Aktualisierung der Bestandsdaten ... [
-- (vor der Etablierung entsprechender Trigger)

-- [ Operationen der Trigger-Funktion tf_articles_addmissing ... [
UPDATE unitracc_orders_articles
  SET amount_multiplied = quantity * amount
  WHERE amount_multiplied IS NULL;
UPDATE unitracc_orders_articles
  SET vat_percent = vat / amount * 100
  WHERE vat_percent IS NULL AND amount != 0;
-- ] ... Operationen der Trigger-Funktion tf_articles_addmissing ]

------------------------------ ] ... Aktualisierung der Bestandsdaten ]

------------------------- [ gelöschte Sicht wiederherstellen ... [
-- (ergänzte Fassung mit neuen Feldern)
CREATE OR REPLACE VIEW orders_articles_view AS
  SELECT DISTINCT
         o.id orderid,
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
         LEFT JOIN unitracc_orders_articles  a ON a.orderid = o.id
         LEFT JOIN unitracc_payment_types    p ON o.payment_type_id = p.id
         LEFT JOIN unitracc_booking_states   s ON o.booking_states_id = s.id
         LEFT JOIN unitracc_groupmemberships g ON g.order_id = o.id
                                              AND g.group_id_ = a.group_id
    ORDER BY o.id DESC,
             a.id ASC;
ALTER TABLE orders_articles_view
  OWNER TO "www-data";

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
        -- neu ab Februar 2018:
        o.payment_type_id,
        o.booking_states_id,
        to_char(g.start, 'DD.MM.YYYY') AS start_ddmmyyyy,
        to_char(g.ends,  'DD.MM.YYYY') AS  ends_ddmmyyyy
   FROM unitracc_orders o
        LEFT JOIN unitracc_orders_articles  a ON a.orderid = o.id
        LEFT JOIN unitracc_payment_types    p ON o.payment_type_id = p.id
        LEFT JOIN unitracc_booking_states   s ON o.booking_states_id = s.id
        LEFT JOIN unitracc_groupmemberships g ON g.order_id = o.id
  ORDER BY o.id DESC;
ALTER TABLE user_bookings_view
  OWNER TO "www-data";

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
------------------------- ] ... gelöschte Sicht wiederherstellen ]

--------------------------------------------- [ neue Sichten ... [
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
--------------------------------------------- ] ... neue Sichten ]

-------------- [ Neuberechnung der berechneten Artikelfelder ... [
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
-------------- ] ... Neuberechnung der berechneten Artikelfelder ]


---------------------------------------- [ Integrität neuer Daten ... [
-- (Sicherstellung der vorstehenden Änderungen durch Trigger)

CREATE OR REPLACE FUNCTION tf_articles_addmissing()
  RETURNS trigger AS
$BODY$begin
  if new.quantity IS NULL then
    new.quantity := 1;
  end if;
  if (new.amount_multiplied IS NULL
      OR (TG_OP = 'UPDATE' AND
          new.amount_multiplied = old.amount_multiplied AND
          new.amount IS NOT NULL)
      ) then
       new.amount_multiplied := new.quantity * new.amount;
  end if;
  if new.vat_percent IS NULL AND new.vat IS NOT NULL and new.amount != 0 then
    new.vat_percent := new.vat / new.amount * 100;
  end if;
  return new;
end;$BODY$
  LANGUAGE plpgsql;
ALTER FUNCTION tf_articles_addmissing()
  OWNER TO "www-data";
CREATE TRIGGER tr_articles_addmissing
  BEFORE INSERT OR UPDATE
  ON unitracc_orders_articles
  FOR EACH ROW  -- sonst wäre NEW undefiniert
  EXECUTE PROCEDURE tf_articles_addmissing();

----------------- [ unitracc_orders.dirty automatisch setzen ... [
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
CREATE TRIGGER tr_articles_dirty
  AFTER INSERT OR UPDATE OR DELETE
  ON unitracc_orders_articles
  FOR EACH ROW  -- sonst wären NEW und OLD undefiniert
  EXECUTE PROCEDURE tf_articles_dirty();
----------------- ] ... unitracc_orders.dirty automatisch setzen ]

---------------------------------------- ] ... Integrität neuer Daten ]

END;
/* Testdaten:
INSERT INTO unitracc_orders_articles
  (orderid, article_uid, article_title, quantity, amount, discount_group, vat_percent)
VALUES (134, 'testuid1', 'Testkurs 1', 5, 300, 'course', 19)
  RETURNING *;

UPDATE unitracc_orders
  SET la = 'de',
      dirty = true
 WHERE id = 134
 RETURNING id, dirty, net_total, vat_total, total, la;

UPDATE unitracc_orders_articles
  SET discount_group = 'course',
      vat_percent = 19
 WHERE orderid = 134
 RETURNING *;
UPDATE unitracc_orders_articles
  SET group_id = '<auto>'
 WHERE orderid = 134
   AND discount_group = 'course'
   AND group_id IS NULL
 RETURNING *;

SELECT article_id, article_uid, group_id, discount_group
  FROM articles_items_view
 WHERE orderid = 134;

INSERT INTO unitracc_orders_articles
  (orderid, article_uid, article_title, quantity, amount, discount_group, vat_percent)
VALUES (134, 'testuid2', 'Testkurs 2', 2, 250, 'course', 19)
  RETURNING *;
-- Jetzt die Sichten:
SELECT *
  FROM articles_items_view
 WHERE orderid = 134;

SELECT orderid, article_id, userid, article_uid, article_title, amount, quantity, amount_multiplied, group_id
  FROM articles_items_view
 WHERE orderid = 134;

SELECT * from articles_discount_view
 WHERE orderid = 134
    AND la = 'de';
SELECT *
  FROM articles_netsum_view
 WHERE orderid = 134;
SELECT *
  FROM articles_vat_view
 WHERE orderid = 134;
SELECT *
  FROM recalculate_order(134);

-- Debugging für recalculate_order:

SELECT id, dirty, net_total, vat_total, total, la
  FROM unitracc_orders
 WHERE id = 134;

SELECT *
 FROM unitracc_orders_articles
 WHERE orderid = 4;


*/
