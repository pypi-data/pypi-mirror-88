-- zur Korrektur des Encodings -*- coding: utf-8 -*- äöü
-- zum manuellen Aufruf, falls nötig
update tan_status set description = 'Die TAN ist schon vergeben, aber noch nicht eingelöst' where name = 'reserved';
update tan_status set description = 'Die TAN wurde eingelöst' where name = 'used';
update tan_status set description = 'Das Ablaufdatum ist verstrichen, und die TAN kann nicht mehr eingelöst werden' where name = 'expired';
update tan_status set description = 'Die TAN wurde "gelöscht"; ihr Eintrag ist aber noch vorhanden, um ihre Historie nachvollziehen zu können.' where name = 'deleted';
