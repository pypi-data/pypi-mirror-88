# -*- coding: utf-8 -*- äöü
"""
Datenmodul für unitracc@@booking

Manche Daten sind nicht hier definiert, sondern im Utility-Modul ./utils.py,
um dessen Testbarkeit mit Doctests nicht zu beeinträchtigen.
"""

# Python compatibility:
from __future__ import absolute_import

REQUIRED_USER_FIELDS = ["street", "zip", "city",
                        "country", "payment_type",  # Payment method
                        ]
REQUIRED_FIELDS = ["user", "article",
                   ] + REQUIRED_USER_FIELDS

# TODO: evtl. datumsabhängig in Datenbank ablegen
VAT_PERCENTAGE = 0.19
DD_MM_YYYY = "%d.%m.%Y"
ACTIVE_VALUES = (1,         # False: Frontend
                 (1, 2),    # True: Backend
                 )
# Buchungsstatus (Tabelle unitracc_booking_states):
BS_NEW = 1      # bei Bestellung per Vorkasse
BS_PAYING = 2   # ?
BS_PENDING = 3
BS_ACCEPTED = 4
BS_DECLINED = 5
BS_TIMEOUT = 6
BS_UNKNOWN = 99

# Zahlungsart / payment type:
PT_PREPAYMENT = 1
PT_PAYPAL = 2

# ---------------------------------------------------------- [ Paypal ... [
# vollständige Übersicht: siehe <https://developer.paypal.com/docs/classic/api/currency_codes/>
PAYPAL_KNOWN_CURRENCYCODES = [
        'EUR',
        'USD',
        ]
# https://developer.paypal.com/webapps/developer/docs/classic/ipn/integration-guide/IPNandPDTVariables/#id091EB04C0HS__id0913D0E0UQU
PAYPAL2NUMERIC_STATUS = {
        'Pending':      BS_PENDING,
        'Completed':    BS_ACCEPTED,
        # 'Processed':  BS_ACCEPTED,    # prakt. Unterschied zu Completed?
        'Denied':       BS_DECLINED,
        'Failed':       BS_DECLINED,
        'Voided':       BS_DECLINED,
        'Expired':      BS_TIMEOUT,
        # bisher nicht vorgesehen:
        # 'Created':    0,              # Pending? Completed?
        # 'Refunded':   0,
        # 'Reversed':   0,              # --> reason_code
        # 'Canceled_Reversal':  0,
        }
# seit März 2018: direkt textuell angeben
PAYPAL2UNITRACC_STATUS = {
        'Pending':      'pending',
        'Completed':    'accepted',
        # 'Processed':  'accepted',    # prakt. Unterschied zu Completed?
        'Denied':       'declined',
        'Failed':       'declined',
        'Voided':       'declined',
        'Expired':      'timeout',
        # bisher nicht vorgesehen:
        # 'Created':    0,              # Pending? Completed?
        # 'Refunded':   0,
        # 'Reversed':   0,              # --> reason_code
        # 'Canceled_Reversal':  0,
        }
# alte (Zahlen-) in neue Werte umwandeln:
OLD2NEW_STATUS = {
	BS_NEW:	        'new',
	BS_PAYING:	'paying',
	BS_PENDING:	'pending',
	BS_ACCEPTED:	'accepted',
	BS_DECLINED:	'declined',
	BS_TIMEOUT:	'timeout',
	BS_UNKNOWN:	'unknown',
        }
tmp = []
for num, booking_state in OLD2NEW_STATUS.items():
    if num >= BS_ACCEPTED:
        tmp.append(booking_state)
ACCEPTED_OR_BETTER = frozenset(tmp)
del tmp

PAYPAL_PAYMENT_STATES = {
    'Canceled_Reversal':
                 'A reversal has been canceled. For example, '
                 'you won a dispute with the customer, and the funds '
                 'for the transaction that was reversed '
                 'have been returned to you.',
    'Completed': 'The payment has been completed, '
                 'and the funds have been added successfully '
                 'to your account balance.',
    'Created':   'A German ELV payment is made using Express Checkout.',
    'Denied':    'The payment was denied. This happens only '
                 'if the payment was previously pending '
                 'because of one of the reasons listed for the pending_reason '
                 'variable or the Fraud_Management_Filters_x variable.',
    'Expired':   'This authorization has expired and cannot be captured.',
    'Failed':    "The payment has failed. This happens only if the payment "
                 "was made from your customer's bank account.",
    'Pending':   'The payment is pending. See pending_reason for more information.',
    'Refunded':  'You refunded the payment.',
    'Reversed':  'A payment was reversed due to a chargeback or '
                 'other type of reversal. '
                 'The funds have been removed from your account balance '
                 'and returned to the buyer. The reason for the reversal '
                 'is specified in the ReasonCode element.',
    'Processed': 'A payment has been accepted.',
    'Voided':    'This authorization has been voided.',
    }
# ---------------------------------------------------------- ] ... Paypal ]

AUTHOR_BRAIN_TO_DB = {
        'getBusinessCompany': 'company',
        'getFirstname': 'firstname',
        'getLastname': 'lastname',
        'getBusinessCity': 'city',
        'getBusinessZip': 'zip',
        'getBusinessStreet': 'street',
        'getBusinessCountry': 'country',
        }
# finde angegebenen Auftrag nur ohne Bestellerangaben:
UNTOUCHED_ORDER_WHERE = ' AND '.join([
    'WHERE order_id = %(order_id)s',
    ] + ["(%s is NULL OR TRIM(%s) = '')" % (field, field)
         for field in ['additional_info'] +
                      list(AUTHOR_BRAIN_TO_DB.values())
         ])
# print UNTOUCHED_ORDER_WHERE

DEFAULT_CURRENCY_CODE = 'EUR'


# visaplan:
# ----------------------------------------------[ für den Parser ... [
from visaplan.tools.minifuncs import translate_dummy as _

#            (Markierung mit ""-Präfix funktioniert nicht zuverlässig)
USER_MAIL_SUBJECT = {
        'normal':   _('Your order no. %(ordernr)s'
                      ' (%(subportal)s)'),
        'thankyou': _('Thank you for '
                      'your order no. %(ordernr)s'
                      ' (%(subportal)s)'),
        # ordernr nicht benötigt:
        'failed':   _('Failed order'
                      ' (%(subportal)s)'),
        }

TIMEOUT_MSGID = _("The time limit for the ordering process has been "
                  "exceeded. Please repeat the order process.")

del _  # ---------------------------------------] ... für den Parser ]
