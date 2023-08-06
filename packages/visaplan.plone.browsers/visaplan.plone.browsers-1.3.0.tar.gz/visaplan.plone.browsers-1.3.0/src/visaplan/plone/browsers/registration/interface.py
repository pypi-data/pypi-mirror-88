# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
# visaplan:
from visaplan.plone.base import Interface


class IRegistrationBrowser(Interface):

    def set():
        """ """

    def validateUserName():
        """ """

    def lock():
        """ """

    def unlock():
        """
        kein wirkliches "Entsperren", eher eine Aktivierung;
        ist bei Anbindung an andere Plattformen (wie z. B. W3L) allerdings
        wichtig!
        """

    def getMailFrom():
        """
        Ermittle die Absender-Adresse für Mails von der Benutzerregistrierung
        (Mailversand und -footer).
        Eine subportalspezifische Festlegung hat Vorrang;
        Beschriftung in configure_registration: "E-Mail From".
        """

    def getMailSiteAdmin():
        """
        Ermittle die BCC-Adresse für Mails von der Benutzerregistrierung
        (Mailversand an neue Benutzer).
        Eine subportalspezifische Festlegung hat Vorrang;
        Beschriftung in configure_registration: "E-Mail Site Administration".
        """

    def getPortalID():
        """ """

    def getPortalTitle():
        """ """

    def getPortalDescription():
        """ """

    def getPortalDomains():
        """ """

    def setConfigure():
        """ """
