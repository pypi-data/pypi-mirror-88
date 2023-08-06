BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü vim: expandtab

-- Zu #393: Beim Fortsetzen von Kursen vom Schreibtisch aus stets den Plattformmodus verwenden
-- siehe ../../../../../../../visaplan.plone.elearning/src/visaplan/plone/elearning/coursestatistics/sql/schema.sql

-- Die Sicht muß tatsächlich gelöscht werden; ansonsten gab es (mit PostgreSQL 9.3) einen Fehler bei der Änderung
-- des Typs von page_view_type, und die Änderung war unwirksam
-- (wobei die weiteren Änderungen -- die Kommentare -- durchaus ausgeführt wurden!)
DROP VIEW course_statistics_overview;
CREATE OR REPLACE VIEW course_statistics_overview AS
SELECT usc.user_uid,
       usc.course_uid,
       usc.course_page_count,
       lpv.rid,
       lpv.last_view_date,
       lpv.pages_viewed,
       lpv.max_page_nr,
       ps2.page_uid        AS max_page_uid,
       CASE
         WHEN lpv.pages_viewed >= usc.course_page_count
              THEN '100'::text
         WHEN usc.course_page_count > 0
              THEN to_char(100.0 * lpv.pages_viewed::numeric / usc.course_page_count::numeric, '990.99'::text)
         ELSE '0'::text
       END                 AS percent,
       ps1.page_number     AS last_viewed_page_nr,
       ps1.page_uid        AS last_viewed_page_uid,
       'course_view'::text AS page_view_type,  -- #393 (konstanter Wert statt ps1.page_view_type)
       usc.id              AS user_and_course_id
  FROM unitracc_statistic_course usc
  LEFT JOIN last_page_view_date lpv
       ON usc.id = lpv.rid
  LEFT JOIN unitracc_page_statistic_course ps1
       ON lpv.last_view_date = ps1.page_view_date
  LEFT JOIN unitracc_page_statistic_course ps2
       ON usc.id = ps2.rid AND ps2.page_number = lpv.max_page_nr;

COMMENT ON COLUMN course_statistics_overview.percent
IS 'Prozentsatz der besuchten Seiten; wg. Verwendung für Styleangabe leider stets mit Dezimal*punkt*';

COMMENT ON COLUMN course_statistics_overview.page_view_type
IS '#393: vom Schreibtisch aus wird stets die Plattformansicht angesteuert (per Ajax-Navigation)';

END;
