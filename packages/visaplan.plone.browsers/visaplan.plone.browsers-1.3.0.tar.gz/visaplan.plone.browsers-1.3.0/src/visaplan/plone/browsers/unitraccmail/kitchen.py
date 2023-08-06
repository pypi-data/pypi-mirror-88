# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
"""\
unitracc@@unitraccmail:kitchen - Hier wird Suppe verarbeitet ...

Operationen auf HTML-Textkörpern von Mails, z.B. um sie in text/plain zu
konvertieren
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves.urllib.parse import parse_qs, urlparse

# Standard library:
from codecs import BOM_UTF8
# für Doctests:
from os.path import dirname, isabs, join, normpath
from string import whitespace

# 3rd party:
from bs4 import BeautifulSoup, Comment

# visaplan:
from visaplan.kitchen.spoons import contents_stripped2
from visaplan.tools.html import (
    BLOCK_ELEMENT_NAMES,
    EMPTY_ELEMENT_NAMES,
    collapse_whitespace,
    entity,
    )
from visaplan.tools.sequences import sequence_slide

# Logging / Debugging:
from visaplan.tools.debug import pp

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"

__all__ = ['html2plain',
           ]

# ------------------------------------------------------ [ Daten ... [
LINESEP = '\r\n'  # In Mails: immer, oder?
TEXTWIDTH = 79    # reicht für Unitracc-Mail-Footer
HORIZONTAL_ROW = '-' * 72  # übliche Maximalbreite für Mails
# Siehe auch --> HANDLER:
IGNORED_ELEMENTS = set(EMPTY_ELEMENT_NAMES)
IGNORED_ELEMENTS.difference_update(set(['img', 'br']))
IGNORED_ELEMENTS.update(['head'])
print(IGNORED_ELEMENTS)
# ------------------------------------------------------ ] ... Daten ]


def html2plain(html=None, template=None, context=None, subject=None,
               **kwargs):
    """
    Konvertiere HTML-Text in einfachen Text, der für einfache Text-Mails
    verwendet werden kann.

    html - Wenn angegeben, der fertige HTML-Text (z. B., um ihn *auch* in
           HTML-Form zu verwenden)
      oder
    template - ein aufzurufendes Template-Objekt
    context - der Kontext (für Template-Aufruf benötigt)
    **kwargs - Argumente für den Template-Aufruf

    >>> html = _testtext('registration.html')
    >>> expected = _testtext('registration.txt')
    >>> converted = html2plain(html)
    >>> from difflib import context_diff
    >>> u''.join(list(context_diff(expected, converted)))
    u''
    >>> converted == expected
    True
    """
    if html is None:
        assert template is not None, (
                'kein fertiger HTMl-Text: Template benoetigt! (%r)'
                % (locals(),))
        assert context is not None, (
                'kein fertiger HTMl-Text: Kontext benoetigt! (%r)'
                % (locals(),))
        html = _getTemplate(context, template_id)(**kwargs)
    soup = BeautifulSoup(collapse_whitespace(html, False))
    res = []
    for elem in soup.children:
        name = elem.name
        f = HANDLER[name]
        f(elem, res)
    resolve_blanks(res)
    return u''.join(res)


# -------------------------------- [ Elementbehandlung ... [
# ------------------------------- [ generisch ... [
def _handle__block(elem, thelist):
    """
    Generische Behandlung von Blockelementen

    Für die Behandlung von Blockelementen (p, div) gilt:
    - Leerraum am Anfang und Ende wird ignoriert
    - leere Blockelemente werden ignoriert
    """
    sublist = []
    # print '--- handle_block(%r, %s)' % (elem.name, elem)
    for child in contents_stripped2(elem):
        HANDLER[child.name](child, sublist)
    if sublist:
        if thelist and thelist[-1] != LINESEP:
            thelist.append(LINESEP)
        thelist.extend(sublist)
        thelist.append(LINESEP)
        return True
    return False

def _handle__text(elem, thelist):
    s = elem.string
    if s:
        thelist.append(s)

def _handle__ignore(elem, thelist):
    pass
# ------------------------------- ] ... generisch ]


HANDLER = {None: _handle__text,
           }
for name in ('div',
             'html', 'body',
             ):
    HANDLER[name] = _handle__block
for name in IGNORED_ELEMENTS:
    HANDLER[name] = _handle__ignore

# -------------------------- [ Einzelelemente ... [
def _handle_p(elem, thelist):
    if _handle__block(elem, thelist):
        thelist.append(LINESEP)
HANDLER['p'] = _handle_p

# für Überschriften: wenigstens schonmal eine Leerzeile dahinter
for name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6',
             ):
    HANDLER[name] = _handle_p

def _handle_span(elem, thelist):
    for child in elem.children:
        HANDLER[child.name](child, thelist)
HANDLER['span'] = _handle_span

def _handle_a(elem, thelist):
    url = elem.attrs.get('href')
    if url:
        thelist.extend([None, url, None])
    else:
        _handle_span(elem, thelist)
HANDLER['a'] = _handle_a

# -------------------------- [ Tabellen ... [
def _handle_table(elem, thelist):
    """
    Verarbeite eine einfache Tabelle:
    - iteriere über die Zeilen
    - stelle fest, wie breit die erste Spalte ist
    - schreibe die Inhalte der ersten und der zweiten Spalte jeweils
      linksbündig untereinander

    Die Funktionalität ist wie folgt eingeschränkt:
    - Es werden nur Tabellen mit zwei Spalten unterstützt
    - Die Zelleninhalte werden als so kurz angenommen, daß sich um
      Zeilenumbrüche nicht gekümmert werden muß
    """
    rows = []
    for child in elem.children:
        name = child.name
        if name == 'tr':
            _handle_tr_(child, rows)
        elif name in ('thead', 'tbody', 'tfoot'):
            for grandchild in child.children:
                _handle_tr_(grandchild, rows)
    maxl = max(len(row[0]) for row in rows)
    mask = '%%-%ds %%s' % maxl
    tmp = []
    for row in rows:
        if not row[1:]:
            row.append('')
        tmp.append((mask % tuple(row[:2])).rstrip())
    if not tmp:
        return
    tmp.append('')
    if thelist:
        thelist.append(LINESEP)
    thelist.append(LINESEP.join(tmp))


def _handle_tr_(elem, rowlist):
    """
    tr-Elemente werden speziell behandelt: sie werden nicht in die globale
    Liste geschrieben, sondern es wird pro Zelle ein String erzeugt und einer
    Liste von Zellen angefügt.

    ACHTUNG: Es wird erwartet, daß jede Zeile zwei Zellen hat!
    """
    cells = []
    for child in elem.children:
        name = child.name
        if name in ('td', 'th'):
            tmpl = []
            HANDLER[name](child, tmpl)
            cells.append(''.join(tmpl).strip())
    if cells:
        rowlist.append(cells)


def _handle_td(elem, thelist):
    for child in contents_stripped2(elem):
        HANDLER[child.name](child, thelist)
    resolve_blanks(thelist)


HANDLER['table'] = _handle_table
HANDLER['td'] = _handle_td
HANDLER['th'] = _handle_td
# -------------------------- ] ... Tabellen ]

# ----------------- [ Ersetzte Elemente ... [
def _handle_br(elem, thelist):
    thelist.append(LINESEP)
HANDLER['br'] = _handle_br

def _handle_hr(elem, thelist):
    thelist.extend([LINESEP, HORIZONTAL_ROW, LINESEP])
HANDLER['hr'] = _handle_hr

def _handle_img(elem, thelist):
    alttext = elem.attrs.get(alt)
    if alttext:
        alttext = collapse_whitespace(alttext, preserve_edge=False)
    else:
        return
    thelist.append(alttext or None)
HANDLER['img'] = _handle_img

# ----------------- ] ... Ersetzte Elemente ]
# -------------------------- ] ... Einzelelemente ]
# -------------------------------- ] ... Elementbehandlung ]

# ---------------------------------- [ Hilfsfunktionen ... [
def resolve_blanks(lst):
    """
    Behandle die Null-Werte in der Liste lst:
    - das vorige Element mit Leerraum aufhört
      oder das nächste damit anfängt: entfernen
    - andernfalls durch ein Leerzeichen ersetzen
    """
    while True:
        done = True
        idx = 0
        delinquents = set([])
        for (prev, current, next) in sequence_slide(lst):
            if current is None:
                if (startswith_whitespace(next) or
                    endswith_whitespace(prev)
                    ):
                    delinquents.add(idx)
                else:
                    lst[idx] = ' '
            elif current == LINESEP:
                if (prev, next) == (LINESEP, LINESEP):
                    delinquents.add(idx)
                """
                elif startswith_whitespace(next, False):
                    lst[idx+1] = lst[idx+1].lstrip()
                """
            elif (current == ' '
                  and next == LINESEP
                  # and (prev, next) == (LINESEP, LINESEP)
                  ):
                delinquents.add(idx)
                done = False
            idx += 1
        if delinquents:
            delinquents = reversed(sorted(delinquents))
            for idx in delinquents:
                del lst[idx]
        if done:
            break


def startswith_whitespace(s, if_none=False):
    if s is None:
        return if_none
    if not s:
        return False
    return s[0] in whitespace


def endswith_whitespace(s, if_none=False):
    if s is None:
        return if_none
    if not s:
        return False
    return s[-1] in whitespace
# ---------------------------------- ] ... Hilfsfunktionen ]


# ----------------------------------------- [ Test-Unterstützung ... [
def _getTemplate(context, template_id):
    return context.unrestrictedTraverse(template_id)


def _testtext(fn, coding='utf-8'):
    r"""
    Gib den Inhalt der angegebenen Testdatei zurück

    >>> _testtext('registration.html')[:20]
    u'<html><body>\r\n\r\n<div'
    """
    filename = normpath(fn)
    if not isabs(filename):
        filename = join(dirname(__file__),
                        'testdata',
                        filename)
    with open(filename, 'rb') as fo:
        txt = fo.read()
        if txt.startswith(BOM_UTF8):
            coding = 'utf-8'
            txt = txt[len(BOM_UTF8):]
        if coding:
            return txt.decode(coding)  # nur für Doctests
        return txt
# ----------------------------------------- ] ... Test-Unterstützung ]


# ------------------------------------ [ Debugging-Unterstützung ... [
def tell():
    dic = {}
    gipsnich = ('GIPS', 'NICH', None)
    for key in ('elem', 'name', 'f'):
        val = globals().get(key, gipsnich)
        if val != gipsnich:
            dic[key] = val
    if dic:
        pp(dic)
        return True
    return False
# ------------------------------------ ] ... Debugging-Unterstützung ]
if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
