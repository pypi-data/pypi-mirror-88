# Python compatibility:
from __future__ import absolute_import

import six

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IMyUnitracc(Interface):

    def canViewMyAcademy():
        """ """

    def getCourseData():
        """ """


class Browser(BrowserView):

    implements(IMyUnitracc)

    def _getGroupCourseDataMapping(self):
        course_group_data_mapping = {
                'group_dwa_zks_course':
                                        ['5ebede414186cbcebb81b669284b43b4',
                                         'a5c2d771c11c1e61e74c2def618be0a8',
                                         'c146572a5a4cde15a2aa92cefb54f822',
                                         '5ee7a8002b6e6257153e1215864233cc',
                                         '893ee641d5c34d406a1c677e2d952b18',
                                         '1622ba5b45c8b66d566c17f6c47a713c',
                                         '6330fe9ed3814f02661952c59a8cf05a'],
                'group_utility_tunnelling_course':
                                        ['7650c7e12af14ad8617514e1342285de'],
                'group_39e5d82b713c892e090d6257640a804d':  # Grabenloser Leitungsbau
                                        ['dc0cc85e9fbe8ba37eb3595ab43d4e93'],
        }

        return course_group_data_mapping

    def canViewMyAcademy(self):
        """
        Checks if current user can view myAcademy-section.
        @return true, if user can view myAcademy-/Course-section, false otherwise
        """
        context = self.context
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        for group_id in six.iterkeys(self._getGroupCourseDataMapping()):
            if group_id in member.getGroups():
                return True

    def getCourseData(self):
        """
        Gets all courses, which are meant for the current user
        @return List of UIDs for the course objects
        """
        context = self.context
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        group_course_data_mapping = self._getGroupCourseDataMapping()
        data = []

        for group_id in six.iterkeys(group_course_data_mapping):
            if group_id in member.getGroups():
                for course_uid in group_course_data_mapping[group_id]:
                    data.append(course_uid)

        return set(data)

    def getCourseIcon(self):
        """ """
