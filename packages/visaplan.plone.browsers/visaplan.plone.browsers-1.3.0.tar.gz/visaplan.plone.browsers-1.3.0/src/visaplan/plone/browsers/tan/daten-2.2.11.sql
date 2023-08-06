-- Daten für den Browser unitracc@@tan -*- coding: utf-8 -*- vim: et ic sw=4 sts=4 ts=4 si
-- Voraussetzung: schema.sql

INSERT INTO tan_status
        (name, description)
 VALUES ('new', 'Die TAN wurde frisch erzeugt und noch nicht vergeben'),
        ('reserved', 'Die TAN ist schon vergeben, aber noch nicht eingelöst'),
        ('used', 'Die TAN wurde eingelöst'),
        ('expired', 'Das Ablaufdatum ist verstrichen, und die TAN kann nicht mehr eingelöst werden'),
        ('deleted', 'Die TAN wurde "gelöscht"; ihr Eintrag ist aber noch vorhanden, um ihre Historie nachvollziehen zu können.');


