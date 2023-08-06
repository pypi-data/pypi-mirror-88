"""An interface for creating and retrieving alerts in Matchlight."""
from __future__ import absolute_import

import datetime

__all__ = (
    'Matches',
    'MatchMethods',
)


class Matches(object):
    """Represents an Matches."""

    def __init__(self):
        """Initializes a new alert."""
        print("welcome matches")


class MatchMethods(object):
    """A Match is a notification that is triggered anytime Terbium finds a single field under monitoring found while crawling the open web, dark web, social, and mobile.
       What constitutes a match varies among asset types.
       Returns a list of all matches belonging to an account.
       If there are no matches, an empty array is returned.
       Response content will depend on the match type.
    """

    def __init__(self, ml_connection):  # noqa: D205,D400
        """Initializes an alerts interface with the given Matchlight
        connection.

        Args:
            ml_connection (:class:`~.Connection`): A Matchlight
                connection instance.

        """

        self.conn = ml_connection

    def list_matches(self, status=None, initiatedFrom=None, initiatedTo=None, publishedFrom=None,
                     publishedTo=None, updatedFrom=None, updatedTo=None, limit=None, offset=None, tags=None):
        """Get all alerts Count in the given project.

                :param str status:
                        - unvetted: Returns matches that haven't been triaged by a memeber of the analyst team.
                        - published: Returns matches that have been triaged and escalated by a memeber of the analyst team.
                        - irrelevant: Returns matches that have been triaged by a memeber of the analyst team and determined to be irrelevant.
                        - falsePositive: Returns matches that have been triaged by a memeber of the analyst team and determined to be false positive.
                        - customerNotInterested: Returns matches that have been triaged by a memeber of the analyst team and the customer wasn't interested.
                        - autoDissmissed: Returns matches where all assets have been deleted

                :param str initiatedFrom: Returns matches initiated from our system equal to or from this date forward.
                :param str initiatedTo: Returns matches initiated from our system equal to or up to this date.

                :param str publishedFrom: Reutrns matches published from an analyst equal to or from this date forward.
                :param bool publishedTo: Returns matches published from an analyst equal to or up to this date.

                :param str updatedFrom: Returns matches updated from an analyst equal to or from this date forward.

                :param datetime updatedTo: Returns matches updated from an analyst equal to or up to this date.

                :param str tags: The alert tags.
                :param str limit: The no of alerts to pull.
                :param str offset: offset of the alerts list.

                :return:
                     returns :class:`Response` object

                >>> ml.matches.list_matches(status='unvetted')
                >>> API_ENDPOINT_PATH = "/v3/public/match/"

                **Example Request Payload**::

                    {
                      "start_date": 1474243200,
                      "end_date": 1474329600
                    }


                **Example Response Payload**::

                    {
                      "start_date": 1474243200,
                      "end_date": 1474329600
                    }

                """

        status = status if status else None
        path = "/v3/public/match/"

        response = self.conn.public_request(
            path,
            params={
                'status': status,
                'tags': tags,
                'initiatedFrom': initiatedFrom,
                'initiatedTo': initiatedTo,
                'publishedFrom': publishedFrom,
                'publishedTo': publishedTo,
                'updatedFrom': updatedFrom,
                'updatedTo': updatedTo,
                'limit': limit,
                'offset': offset,
            },
            method='GET',
        )

        return response

    def match_count(self, status=None, initiatedFrom=None, initiatedTo=None, publishedFrom=None,
                    publishedTo=None, updatedFrom=None, updatedTo=None, tags=None):
        """Returns a count of all matches belonging to an account.

               :param str status:
                      - unvetted: Returns a count of matches that haven't been triaged by a memeber of the analyst team.
                      - published: Returns a count of matches that have been triaged and esclated by a memeber of the analyst team.
                      - irrelevant: Returns a count of matches that have been triaged by a memeber of the analyst team and determined to be irrelevant.
                      - falsePositive: Returns a count of matches that have been triaged by a memeber of the analyst team and determined to be false positive.
                      - customerNotInterested: Returns a count of matches that have been triaged by a memeber of the analyst team and the customer wasn't interested.
                      - autoDissmissed: Returns a count of matches where all assets have been deleted.
               :param str initiatedFrom: Returns a count of matches initiated from our system equal to or from this date forward.
               :param str initiatedTo: Returns a count of matches initiated from our system equal to or up to this date.
               :param str publishedFrom: Returns a count of matches published from an analyst equal to or from this date forward.
               :param bool  publishedTo: Returns a count of matches published from an analyst equal to or up to this date.
               :param str updatedFrom: Returns a count of matches updated from an analyst equal to or from this date forward.
               :param str updatedTo: Returns a count of matches updated from an analyst equal to or up to this date.
               :param str tags: The alert tags.
               :return:
                    returns :class:`~.Json` Created record with metadata.


               >>> ml.matches.match_count(status='unvetted')
               >>> API_ENDPOINT_PATH = "/v3/public/match/count"


               **Example Request Payload**::

                    {
                      "start_date": 1474243200,
                      "end_date": 1474329600
                    }


               **Example Response Payload**::

                    {
                      "start_date": 1474243200,
                      "end_date": 1474329600
                    }
               """

        status = status if status else None
        path = "/v3/public/match/count"

        response = self.conn.public_request(
            path,
            params={
                'status': status,
                'initiatedFrom': initiatedFrom,
                'initiatedTo': initiatedTo,
                'publishedFrom': publishedFrom,
                'publishedTo': publishedTo,
                'updatedFrom': updatedFrom,
                'updatedTo': updatedTo,
                'tags': tags,
            },
            method='GET',
        )

        return response
