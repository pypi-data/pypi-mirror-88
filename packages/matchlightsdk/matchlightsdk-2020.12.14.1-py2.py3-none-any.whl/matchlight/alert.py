"""An interface for creating and retrieving alerts in Matchlight."""
from __future__ import absolute_import

import datetime

import matchlight.error

__all__ = (
    'Alert',
    'AlertMethods',
)


class Alert(object):
    """Represents an alert."""

    # def __init__(self, id, number, type, url, url_metadata, ctime, mtime, seen, archived, upload_token, details):
    def __init__(self):
        """Initializes a new alert."""
        print('Welcome to alerts')


class AlertMethods(object):
    """An Alert is a notification that is triggered anytime Terbium finds a sourced, timestamp-based, group of matches for Assets on the open web, dark web, social, and mobile.
      What constitutes an alert varies among asset types.
      Returns a list of all alerts belonging to an account.
      If there are no alerts, an empty array is returned.
      Response content will depend on the alert type.
    """

    def __init__(self, ml_connection):  # noqa: D205,D400
        """Initializes an alerts interface with the given Matchlight
        connection.

            :param :class `~.Connection` ml_connection: A Matchlight connection instance.

        """
        self.conn = ml_connection

    def list_alerts(self, status=None, initiatedFrom=None, initiatedTo=None, publishedFrom=None,
                    publishedTo=None, updatedFrom=None, updatedTo=None, limit=None, offset=None, tags=None):
        """Get all alerts in the given project.

                  :param str status:
                          - unvetted: Returns alerts that haven't been triaged by a memeber of the analyst team.
                          - published: Returns alerts that have been triaged and esclated by a memeber of the analyst team.
                          - irrelevant: Returns alerts that have been triaged by a memeber of the analyst team and determined to be irrelevant.
                          - falsePositive: Returns alerts that have been triaged by a memeber of the analyst team and determined to be false positive.
                          - customerNotInterested: Returns alerts that have been triaged by a memeber of the analyst team and the customer wasn't interested.
                          - autoDissmissed: Returns alerts where all assets have been deleted.
                  :param datetime initiatedFrom: Returns alerts initiated from our system equal to or from this date forward.
                  :param datetime initiatedTo: Returns alerts initiated from our system equal to or up to this date.
                  :param datetime publishedFrom: Returns alerts published from an analyst equal to or from this date forward.
                  :param datetime publishedTo: Returns alerts published from an analyst equal to or up to this date.
                  :param datetime updatedFrom: Returns alerts updated from an analyst equal to or from this date forward.
                  :param datetime updatedTo: Returns alerts updated from an analyst equal to or up to this date.
                  :param str limit: The no of alerts to pull.
                  :param str offset: offset of the alerts list.
                  :param str tags: The alert tags.
                  :return:
                     returns :class:`~.Json` Created record with metadata.

                  >>> ml.alerts.list_alerts(status, initiatedFrom='2020-11-04 20:08:11', initiatedTo='2020-11-05 20:08:11')
                  >>> ml.alerts.list_alerts(status, publishedFrom='2020-11-04 20:08:11', publishedTo='2020-11-05 20:08:11')
                  >>> ml.alerts.list_alerts(status, updatedFrom='2020-11-04 20:08:11', updatedTo='2020-11-05 20:08:11')

                  >>> API_ENDPOINT_PATH = "/v3/public/alert/"


                  **Example Response Payload**::

                    {
                       "body":[
                          {
                             "accountId":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                             "accountName":"PublicApi",
                             "alerts":[
                                {
                                   "id":"2697d5e1-2dd7-45a5-a96a-87ba64ad1e9b",
                                   "friendlyId":"20001411650",
                                   "status":"Unvetted",
                                   "url":"http://ea5faa5po25cf7fb.onion/projects/tor/wiki/doc/GAEuploader?version=24",
                                   "siteName":"None",
                                   "source":"Dark Web",
                                   "sourceDetails":"None",
                                   "takedownStatus":"None",
                                   "riskScore":41,
                                   "severity":"Moderate",
                                   "threatType":[

                                   ],
                                   "analysis":"",
                                   "recommendedActions":"None",
                                   "assets":[
                                      {
                                         "assetId":"eca5b698-4210-4470-b281-bc1fc0360e7d",
                                         "customId":"eca5b69842104470",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"public api text",
                                         "tags":"publicapi, public_keyword",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"public api text",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"b066509b-fe9e-4b07-8473-cc5fc0a83296",
                                                  "metaData":[
                                                     [
                                                        "public",
                                                        1
                                                     ],
                                                     [
                                                        "test",
                                                        4
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"ce4d6f74-f34c-4073-87d2-15da43a3f440",
                                         "customId":"ce4d6f74f34c4073",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"public api text2",
                                         "tags":"publicapi, public_keyword, api_public_test",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"adc1d837-a291-462f-a552-f05cc36433f8",
                                                  "metaData":[
                                                     [
                                                        "public",
                                                        1
                                                     ],
                                                     [
                                                        "test",
                                                        4
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"8cc83617-dd86-4ed1-866b-072546530a00",
                                         "customId":"8cc83617dd864ed1",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"public api text",
                                         "tags":"publicapi, public_keyword",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"public api text",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"fc66f24c-836c-4259-90c6-595d3d113c11",
                                                  "metaData":[
                                                     [
                                                        "public",
                                                        1
                                                     ],
                                                     [
                                                        "test",
                                                        4
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"88322dcf-f4f1-4b44-88ce-a1b8a96f9e84",
                                         "customId":"88322dcff4f14b44",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"public api text",
                                         "tags":"publicapi, public_keyword",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"public api text",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"f618a676-af73-4646-b39e-646d15164fd7",
                                                  "metaData":[
                                                     [
                                                        "test",
                                                        4
                                                     ],
                                                     [
                                                        "public",
                                                        1
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"b3afd082-2297-4cdb-8f0e-6699a94eb1e3",
                                         "customId":"b3afd08222974cdb",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"",
                                         "tags":"publicapi, public_keyword, api_public_test",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"None",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"2e8a4cdf-3174-4f5b-8d65-c70c0e9d697c",
                                                  "metaData":[
                                                     [
                                                        "test",
                                                        4
                                                     ],
                                                     [
                                                        "public",
                                                        1
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"3d5b0f62-a7fa-4cf4-a6c8-79bdff069fb3",
                                         "customId":"3d5b0f62a7fa4cf4",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"public api text2",
                                         "tags":"publicapi, public_keyword, api_public_test",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"public api text",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"33f7bb2d-0eab-450c-818b-b76b201db616",
                                                  "metaData":[
                                                     [
                                                        "public",
                                                        1
                                                     ],
                                                     [
                                                        "test",
                                                        4
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"f4517627-9bc4-49d7-8a4e-a7b69d140c5e",
                                         "customId":"f45176279bc449d7",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"",
                                         "tags":"publicapi, public_keyword, api_public_test",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"205ddaca-2300-4bd9-bf26-b0c9b87670ca",
                                                  "metaData":[
                                                     [
                                                        "public",
                                                        1
                                                     ],
                                                     [
                                                        "test",
                                                        4
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"0a8fe218-7708-4844-870b-cb35f4d6e905",
                                         "customId":"0a8fe21877084844",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"None",
                                         "tags":"publicapi, public_keyword, api_public_test",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"205ddaca-2300-4bd9-bf26-b0c9b87670ca",
                                                  "metaData":[
                                                     [
                                                        "public",
                                                        1
                                                     ],
                                                     [
                                                        "test",
                                                        4
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"0a8fe218-7708-4844-870b-cb35f4d6e905",
                                         "customId":"0a8fe21877084844",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"None",
                                         "tags":"publicapi, public_keyword, api_public_test",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"None",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"d8da18fb-66d2-429a-8fde-98efa1914068",
                                                  "metaData":[
                                                     [
                                                        "test",
                                                        4
                                                     ],
                                                     [
                                                        "public",
                                                        1
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"7c4ac913-9751-4d1d-88aa-048c502ebff0",
                                         "customId":"7c4ac91397514d1d",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"",
                                         "tags":"publicapi, public_keyword",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"666fc463-c667-4520-8d07-d2df3295f7e3",
                                                  "metaData":[
                                                     [
                                                        "test",
                                                        4
                                                     ],
                                                     [
                                                        "public",
                                                        1
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"e14bf853-2e25-4e0b-84d5-72bc7531e6a8",
                                         "customId":"e14bf8532e254e0b",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"public api text2",
                                         "tags":"publicapi, public_keyword, api_public_test",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"public api text",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"244b6927-d13f-4b50-987b-6e764a18cf29",
                                                  "metaData":[
                                                     [
                                                        "test",
                                                        4
                                                     ],
                                                     [
                                                        "public",
                                                        1
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"71965583-9659-42fb-af86-ff019a18d7ed",
                                         "customId":"71965583965942fb",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"None",
                                         "tags":"publicapi, public_keyword, api_public_test",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"None",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"bc25bbb1-783f-46d4-b050-6d2f9afaa743",
                                                  "metaData":[
                                                     [
                                                        "test",
                                                        4
                                                     ],
                                                     [
                                                        "public",
                                                        1
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      },
                                      {
                                         "assetId":"adff987c-6f3f-4c48-aa6e-04d6368c06c7",
                                         "customId":"adff987c6f3f4c48",
                                         "assetType":"Keywords",
                                         "methodType":"Plaintext",
                                         "assetDetails":"public api text",
                                         "tags":"publicapi, public_keyword",
                                         "fields":[
                                            {
                                               "name":"Keyword",
                                               "fieldDetail":"public api text",
                                               "term":"Public|APi|test",
                                               "matches":{
                                                  "matchId":"967fb0e5-6fa2-4c85-b818-0bb3929c24b6",
                                                  "metaData":[
                                                     [
                                                        "test",
                                                        4
                                                     ],
                                                     [
                                                        "public",
                                                        1
                                                     ]
                                                  ]
                                               }
                                            }
                                         ]
                                      }
                                   ],
                                   "createdAt":"2020-12-07T16:25:07.687928",
                                   "updatedAt":"2020-12-07T16:25:07.687928",
                                   "publishedAt":"None",
                                   "attachments":[

                                   ]
                                }
                             ]
                          }
                       ],
                       "errors":[

                       ],
                       "totalResults":1688
                  }


        """
        status = status if status else None
        path = "/v3/public/alert/"

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

    def alerts_count(self, status=None, initiatedFrom=None, initiatedTo=None, publishedFrom=None,
                     publishedTo=None, updatedFrom=None, updatedTo=None, tags=None):
        """Returns a count of all alerts belonging to an account.

                :param str status:
                      - unvetted: Returns a count of alerts that haven't been triaged by a memeber of the analyst team.
                      - published: Returns a count of alerts that have been triaged and esclated by a memeber of the analyst team.
                      - irrelevant: Returns a count of alerts that have been triaged by a memeber of the analyst team and determined to be irrelevant.
                      - falsePositive: Returns a count of alerts that have been triaged by a memeber of the analyst team and determined to be false positive.
                      - customerNotInterested: Returns a count of alerts that have been triaged by a memeber of the analyst team and the customer wasn't interested.
                      - autoDissmissed: Returns a count of alerts where all assets have been deleted
                :param datetime initiatedFrom: Returns a count of alerts initiated from our system equal to or from this date forward.
                :param datetime initiatedTo: Returns a count of alerts initiated from our system equal to or up to this date.
                :param datetime publishedFrom: Returns a count of alerts published from an analyst equal to or from this date forward.
                :param datetime publishedTo: Returns a count of alerts published from an analyst equal to or up to this date.
                :param datetime updatedFrom: Returns a count of alerts updated from an analyst equal to or from this date forward.
                :param datetime updatedTo: Returns a count of alerts updated from an analyst equal to or up to this date.
                :param str tags: The alert tags.
                :return:
                  returns :class:`~.Json` Created record with metadata.

                >>> ml.alerts.alerts_count(status, initiatedFrom='2020-11-04 20:08:11', initiatedTo='2020-11-05 20:08:11')
                >>> ml.alerts.alerts_count(status, publishedFrom='2020-11-04 20:08:11', publishedTo='2020-11-05 20:08:11')
                >>> ml.alerts.alerts_count(status, updatedFrom='2020-11-04 20:08:11', updatedTo='2020-11-05 20:08:11')

                >>> API_ENDPOINT_PATH = "/v3/public/alert/count"


                **Example Response Payload**::

                    {
                      count': 1719
                    }

        """
        status = status if status else None
        path = "/v3/public/alert/count"

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

    def list_tags(self, tag_type=None):
        """Get all alerts in the given project.

            :param str tag_type: The name of the document (not fingerprinted).

            :return: returns :class:`Json` object

            >>> ml.alerts.list_tags(tag_type="['unvetted']")

            >>> API_ENDPOINT_PATH = "/v3/public/tags/unique"

            **Example Response**::

                {
                   "body":[
                      "_",
                      "api_public_test",
                      "c",
                      "chennai_doc",
                      "chennaiipl",
                      "d",
                      "e",
                      "emppiie",
                      "foods_od_india",
                      "ipaddress",
                      "jiopublic",
                      "k",
                      "m",
                      "mumbaiipl",
                      "n",
                      "o",
                      "publicapi",
                      "public_domain",
                      "public_keyword",
                      "publict_test_api1",
                      "s",
                      "sdk_test",
                      "sdk_test_document",
                      "sdk_test_source_code",
                      "srhipl",
                      "t",
                      "u"
                   ],
                   "errors":[

                   ],
                   "totalResults":1
                }
        """

        path = "/v3/public/tags/unique"
        response = self.conn.public_request(
            path,
            params={
                'for': tag_type
            },
            method='GET',
        )
        return response

    def get_details(self, alert_id):
        """Returns details of an alert by the given alert ID.

            :param str alert_id: The alert identifier.

            :return: Returns :obj:`dict`: map of the alert details.
            >>> ml.alerts.get_details("e762fffc-442b-4fae-b822-c87ba99c7388")

            >>> API_ENDPOINT_PATH = "/alert/patient_id/details"
        """

        if isinstance(alert_id, Alert):
            alert_id = alert_id.id

        try:
            response = self.conn.request('/alert/{}/details'.format(alert_id))
            return response.json()
        except matchlight.error.APIError as err:
            if err.args[0] == 404:
                return
            else:
                raise
