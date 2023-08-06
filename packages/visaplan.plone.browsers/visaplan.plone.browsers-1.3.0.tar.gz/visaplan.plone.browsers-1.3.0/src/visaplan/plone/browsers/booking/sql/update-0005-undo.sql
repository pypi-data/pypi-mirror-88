BEGIN TRANSACTION;  /* -*- coding: utf-8 -*- vim: expandtab sw=4 sts=4 si
zu --> update-0005.sql
*/
DROP VIEW IF EXISTS orders_view;
DROP VIEW IF EXISTS orders_articles_view;
DROP VIEW IF EXISTS access_settlement_modes_user_view;
DROP VIEW IF EXISTS access_settlement_modes_raw_view;

ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_has_access_settlement_mode;
ALTER TABLE unitracc_orders
  DROP CONSTRAINT IF EXISTS unitracc_orders_access_settlement_mode_fkey;
ALTER TABLE unitracc_orders
  DROP COLUMN access_settlement_mode;
DROP TABLE unitracc_access_settlement_mode;

-- Wiederherstellung der Fassung aus update-0003.sql:
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

END;
