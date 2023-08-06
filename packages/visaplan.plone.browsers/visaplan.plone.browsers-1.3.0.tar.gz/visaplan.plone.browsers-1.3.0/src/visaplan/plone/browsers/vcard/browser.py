# Python compatibility:
from __future__ import absolute_import

from six import string_types as six_string_types

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IVCard(Interface):

    def get():
        """ """


class Browser(BrowserView):

    implements(IVCard)

    def wrap(self, value):
        s = ''
        # When generating a content line, lines longer than 75
        # characters SHOULD be folded according to the folding
        # described in http://www.faqs.org/rfcs/rfc2426.html
        while value:
            s += value[:75] + "\r\n "
            value = value[75:]
        # remove last CRLF and space
        s = s[:-3]
        return s

    def addValue(self, key, value):
        context = self.context
        # helper method to skip empty values, escape commas and
        # semicolons and format line breaks. See
        # http://www.faqs.org/rfcs/rfc2426.html

        # A formatted text line break in a text value type MUST be
        # represented as the character sequence backslash (ASCII decimal 92)
        # followed by a Latin small letter n (ASCII decimal 110) or a Latin
        # capital letter N (ASCII decimal 78), that is "\n" or "\N".
        if not value:
            return

        if 'ENCODING=b' in key:
            # join lines so that we can rewrap them
            value = value.replace('\n', '')
        else:
            if isinstance(value, six_string_types):
                value = [value]

            l = []
            for v in value:
                if not v:
                    v = ''
                v = v.replace(",", "\,")
                v = v.replace(";", "\;")
                v = v.replace("\r\n", "\\n")
                v = v.replace("\n", "\\n")
                l.append(v)
            value = ";".join(l)

        value = "%s:%s" % (key, value)
        if len(value) > 75:
            value = self.wrap(value)

        self.vcard.append(value)

    def get(self):
        """ """
        context = self.context

        self.vcard = [
            "BEGIN:VCARD",
            "VERSION:3.0",
        ]
        self.addValue("FN", str(context.combinedContactName()))

        self.addValue("ADR;TYPE=postal", (
                        "",
                        "",  # extended address not in default schema
                        context.getContactStreet(),
                        context.getContactCity(),
                        '',
                        context.getContactZip(),
                        ''
                        )
                )

        self.addValue("TEL;TYPE=work,voice", str(context.getContactPhone()))
        self.addValue("TEL;TYPE=work,fax", str(context.getContactFax()))
        self.addValue("EMAIL;TYPE=internet", str(context.getContactEmail()))

        organisation = context.getContactCompany()
        if organisation:
            self.addValue("ORG", str(organisation))

        self.addValue("URL", context.absolute_url())

        self.vcard.append("END:VCARD")

        RESPONSE = context.REQUEST.RESPONSE
        RESPONSE.setHeader('Content-Type', 'text/x-vcard; charset=utf-8')
        RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.vcf"' % context.getId())
        return "\r\n".join(self.vcard)
