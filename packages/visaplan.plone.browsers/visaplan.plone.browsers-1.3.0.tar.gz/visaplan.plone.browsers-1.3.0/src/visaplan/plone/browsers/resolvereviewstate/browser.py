# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et hls
# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import parent_brains


class IResolveReviewState(Interface):

    def __call__(flatten_public_states):
        """
        flatten_public_states -- alle 'veröffentlicht'-Werte zusammenfassen
        """


class Browser(BrowserView):
    """
    ermittle den ggf. ererbten review-Status des aufrufenden Objekts.

    Um von der Vorgabe abweichende Argumente zu verwenden, den Browser
    erst mit nocall: einer Variablen zuweisen und dann in einem
    Python-Ausdruck aufrufen
    """

    implements(IResolveReviewState)

    def __call__(self, flatten_public_states=True):
        """
        Method resolves the context object's review state to one of the following: private, submitted, accepted, approved, published, visible, restricted.
        If object's review state is 'inherit' the inherited review state is resolved through the hierarchy of parents.
        If the flatten_public_states flag ist set to True the states 'visible' and 'restricted' are mapped to the 'published'-state.
        """
        context = self.context

        # Do parent aquisition with Manager-Role
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:
            # Wenn das Attribut fehlt, unterliegt das Objekt nicht dem
            # Workflow (z. B. ein Container, wie /akademie/vortraege)
            if hasattr(context, 'review_state'):
                review_state = context.review_state

                # Resolve inherited state if the object's review state is 'inherit'
                if review_state == "inherit":
                    parent_brain = context.aq_inner
                    for parent in parent_brains(context, parent_brain):

                        if parent.review_state != "inherit":
                            review_state = parent.review_state
                            break

                    # We are at the portal root object and all parents within the hierarchy had review state 'inherit'.
                    # Set object's review state to 'published'
                    if review_state == "inherit":
                        review_state = "published"

                # Map states 'visible' and 'restricted' to state 'published' if the flatten_public_states-flag is set to True
                if flatten_public_states and review_state in ['visible', 'restricted']:
                    review_state = "published"

                return review_state
            else:
                return ""

        finally:
            sm.setOld()
