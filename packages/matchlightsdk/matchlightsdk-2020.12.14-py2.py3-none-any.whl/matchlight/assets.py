"""An interface for creating and retrieving PII records in Matchlight."""
from __future__ import absolute_import

import io
import json

import six

import matchlight.error
import matchlight.utils
from pylibfp import (
    fingerprint,
    fingerprints_pii_address_variants,
    fingerprints_pii_city_state_zip_variants,
    fingerprints_pii_credit_card,
    fingerprints_pii_email_address,
    fingerprints_pii_iban,
    fingerprints_pii_medicare_id,
    fingerprints_pii_name_variants,
    fingerprints_pii_passport,
    fingerprints_pii_phone_number,
    fingerprints_pii_ssn,
    MODE_CODE,
    OPTIONS_TILED,
)

__all__ = (
    'Asset',
    'AssetMethods',
)

MAX_DOCUMENT_FINGERPRINTS = 840


class Asset(object):
    """Represents a personal information record."""

    # def __init__(self, id, name, description, ctime=None, mtime=None, metadata=None):
    def __init__(self):
        """Initializes a new personal information record. """
        print("hello")
    #     if metadata is None:
    #         metadata = {}
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.ctime = ctime
    #     self.mtime = mtime
    #     self.metadata = metadata
    #
    # @classmethod
    # def from_mapping(cls, mapping):
    #     """Creates a new project instance from the given mapping."""
    #     return cls(
    #         id=mapping['id'],
    #         name=mapping['name'],
    #         description=mapping['description'],
    #         ctime=mapping['ctime'],
    #         mtime=mapping['mtime'],
    #         metadata=mapping['metadata'],
    #     )
    #
    # @property
    # def user_provided_id(self):
    #     """:obj:`int`: The user provided record identifier."""
    #     return self.metadata.get('user_record_id', None)
    #
    # @property
    # def details(self):
    #     """:obj:`dict`: Returns the feed details as a mapping."""
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'description': self.description,
    #         'ctime': self.ctime,
    #         'mtime': self.mtime,
    #         'metadata': self.metadata,
    #     }
    #
    # def __repr__(self):  # pragma: no cover
    #     return '<Record(name="{}", id="{}")>'.format(self.name, self.id)


class AssetMethods(object):
    """Provides methods for interfacing with the records API. """

    def __init__(self, ml_connection):  # noqa: D205,D400
        """Initializes a records interface with the given Matchlight
        connection.

            :param :class:`~.Connection` ml_connection: A Matchlight connection instance.

        """
        self.conn = ml_connection

    def add_document(self, account_id, custom_id, asset_detail, tags,
                     content, match_score_threshold=70, offline=False):
        """Creates a new document record in the given project.

            :param str account_id: Account ID.
            :param str custom_id: Custom ID of the document.
            :param str asset_detail: Asset_detail of the document.
            :param str tags: Tag of the document.
            :param str match_score_threshold: minimum matching score of the document.
            :param str content:  The text of the document to be fingerprinted.
            :param bool offline: Run in "offline mode". Nodata is sent to the Matchlight server. Returns a dictionary of values instead of a :class:`~.Report` instance.
            :return:
                returns :class:`~.Json`: Created Json with metadata.


            **Example Request Payload**::

                    {
                       "account_id":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                       "custom_id":"sdk_test_document",
                       "asset_detail":"sdk_test_document",
                       "type":"document",
                       "metadata":{
                          "fingerprinting_tool_name":"Python SDK",
                          "fingerprinting_tool_version":"unknown"
                       },
                       "fields":[
                          {
                             "type":"document",
                             "variants":[
                                [
                                   "049688c8f2428313",
                                   "04be7d9e80fdfa7c",
                                   "06c6a7c0fc6c70b7",
                                   "07b0ac51afbf089e",
                                   "0851c847d2587ff9",
                                   "08733f4a281611bb",
                                   "10ad57aea0d3787b",
                                   "15c8e157ab706e92",
                                   "16cddcfd2bf633f6",
                                   "18d4b88471b4927a",
                                   "18e175195f980a77",
                                   "1bf435cf4c0b912c",
                                   "1c1c3e3ffb9553c0",
                                   "2413ea3c70947f0e",
                                   "270cba42925c2c88",
                                   "2a427823ab8c1454",
                                   "2cd2b504f6936356",
                                   "2ff2f9df0f2ef1b6",
                                   "30e7c829c36d92af",
                                   "33a44f1c8c9f03f3",
                                   "354ff044026bdefd",
                                   "3ba14168f8555362",
                                   "3d0fc2c4daa69b92",
                                   "3ecf8a6d2de0f30f",
                                   "479bf8e9b8c3de2b",
                                   "4c23aab273b8b202",
                                   "4c35632f00e06fe7",
                                   "4d09334303ec564a",
                                   "52272b1ef7580667",
                                   "53ae8ccde40ff3c6",
                                   "540c2722c8476cbe",
                                   "54ee17d7ee091c30",
                                   "58537327169683c5",
                                   "5b5557456f77529f",
                                   "6317c43363c86d17",
                                   "6801ef9d934be938",
                                   "689ba48dece15aa6",
                                   "698693cfa1454723",
                                   "6b8ca3e0c397b0da",
                                   "6e079efa1648a05b",
                                   "6e1924b5357eb264",
                                   "705214961ac7ea70",
                                   "7270315316267534",
                                   "72c1de4177b21a1c",
                                   "72d7fab2e1fbe274",
                                   "77c10cb455cc0f39",
                                   "7f363486b8b2e418",
                                   "830a10da13a322ca",
                                   "845447608db9018a",
                                   "89ea12964f491107",
                                   "8a7c8b986ac06702",
                                   "93a0f3ed9a311988",
                                   "946433583be02349",
                                   "9525300fd7829886",
                                   "97fd7f5eacd8ba60",
                                   "98c81edd1b28a06c",
                                   "9bad899617b690a2",
                                   "9f9e399902223856",
                                   "a55bc1bae181b366",
                                   "a8686918198ff616",
                                   "a8daa87fb3c9ab68",
                                   "af5d553e1b38e04a",
                                   "bbbdce62e57a3b61",
                                   "bbfc1a1d1fddcf05",
                                   "c90a7a2a68a01217",
                                   "ccad3236df8f32f0",
                                   "ce256e3ea8742b33",
                                   "d425308fc2291b9e",
                                   "d589432213820ead",
                                   "d73c30501f0ba189",
                                   "d7df7bbe9511c209",
                                   "d7f47da9932b4ae7",
                                   "dac59d4d3f8a35c1",
                                   "e11e3efe751cfbfb",
                                   "e248371f50a328f0",
                                   "ed9287c1b6470f6f",
                                   "edb18cc8dbb55796",
                                   "f432aeb74d374dca",
                                   "f49f8fc49fbfff10",
                                   "f75019e789a3b5e2",
                                   "f7e04ae93a7d580c",
                                   "fbaee0d65df3f836",
                                   "fd1ace2b02aacc70"
                                ]
                             ],
                             "field_detail":"sdk_test_document"
                          }
                       ],
                       "tags":[
                          "sdk_test_document"
                       ],
                       "match_score_threshold":70
                    }



            **Example Response Payload**::

                    {
                      "body":"74496a75-6eaa-460e-8055-937b7eab4af2",
                      "errors":[],
                      "totalResults":1
                    }

        """

        result_json = fingerprint(content, flags=OPTIONS_TILED)
        result = json.loads(result_json)
        fingerprints = result['data']['fingerprints']

        data = {
            'account_id': account_id,
            'custom_id': custom_id,
            'asset_detail': asset_detail,
            'type': "document",
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        fields = dict()
        fields['type'] = 'document'
        fields['variants'] = [fingerprints]
        fields['field_detail'] = asset_detail

        data['fields'] = [fields]

        if tags is not None:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = tags
        if match_score_threshold is not None:
            data['match_score_threshold'] = match_score_threshold

        if offline:
            return data
        else:
            return self.add_document_from_fingerprints(data)

    def add_document_from_fingerprints(self, fingerprint_data):
        """Add a document record from fingerprinted data generated by the :class:`~/.Record.add_pii` in offline mode.

          :param dict fingerprint_data: The output of :class:`~/.Assets.add_document(offline=True)
          :return: returns :class:`Json` object

          >>> API_ENDPOINT_PATH = '/v3/public/asset/'

          **Example Request Payload**::

                    {
                       "account_id":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                       "custom_id":"sdk_test_document",
                       "asset_detail":"sdk_test_document",
                       "type":"document",
                       "metadata":{
                          "fingerprinting_tool_name":"Python SDK",
                          "fingerprinting_tool_version":"unknown"
                       },
                       "fields":[
                          {
                             "type":"document",
                             "variants":[
                                [
                                   "049688c8f2428313",
                                   "04be7d9e80fdfa7c",
                                   "06c6a7c0fc6c70b7",
                                   "07b0ac51afbf089e",
                                   "0851c847d2587ff9",
                                   "08733f4a281611bb",
                                   "10ad57aea0d3787b",
                                   "15c8e157ab706e92",
                                   "16cddcfd2bf633f6",
                                   "18d4b88471b4927a",
                                   "18e175195f980a77",
                                   "1bf435cf4c0b912c",
                                   "1c1c3e3ffb9553c0",
                                   "2413ea3c70947f0e",
                                   "270cba42925c2c88",
                                   "2a427823ab8c1454",
                                   "2cd2b504f6936356",
                                   "2ff2f9df0f2ef1b6",
                                   "30e7c829c36d92af",
                                   "33a44f1c8c9f03f3",
                                   "354ff044026bdefd",
                                   "3ba14168f8555362",
                                   "3d0fc2c4daa69b92",
                                   "3ecf8a6d2de0f30f",
                                   "479bf8e9b8c3de2b",
                                   "4c23aab273b8b202",
                                   "4c35632f00e06fe7",
                                   "4d09334303ec564a",
                                   "52272b1ef7580667",
                                   "53ae8ccde40ff3c6",
                                   "540c2722c8476cbe",
                                   "54ee17d7ee091c30",
                                   "58537327169683c5",
                                   "5b5557456f77529f",
                                   "6317c43363c86d17",
                                   "6801ef9d934be938",
                                   "689ba48dece15aa6",
                                   "698693cfa1454723",
                                   "6b8ca3e0c397b0da",
                                   "6e079efa1648a05b",
                                   "6e1924b5357eb264",
                                   "705214961ac7ea70",
                                   "7270315316267534",
                                   "72c1de4177b21a1c",
                                   "72d7fab2e1fbe274",
                                   "77c10cb455cc0f39",
                                   "7f363486b8b2e418",
                                   "830a10da13a322ca",
                                   "845447608db9018a",
                                   "89ea12964f491107",
                                   "8a7c8b986ac06702",
                                   "93a0f3ed9a311988",
                                   "946433583be02349",
                                   "9525300fd7829886",
                                   "97fd7f5eacd8ba60",
                                   "98c81edd1b28a06c",
                                   "9bad899617b690a2",
                                   "9f9e399902223856",
                                   "a55bc1bae181b366",
                                   "a8686918198ff616",
                                   "a8daa87fb3c9ab68",
                                   "af5d553e1b38e04a",
                                   "bbbdce62e57a3b61",
                                   "bbfc1a1d1fddcf05",
                                   "c90a7a2a68a01217",
                                   "ccad3236df8f32f0",
                                   "ce256e3ea8742b33",
                                   "d425308fc2291b9e",
                                   "d589432213820ead",
                                   "d73c30501f0ba189",
                                   "d7df7bbe9511c209",
                                   "d7f47da9932b4ae7",
                                   "dac59d4d3f8a35c1",
                                   "e11e3efe751cfbfb",
                                   "e248371f50a328f0",
                                   "ed9287c1b6470f6f",
                                   "edb18cc8dbb55796",
                                   "f432aeb74d374dca",
                                   "f49f8fc49fbfff10",
                                   "f75019e789a3b5e2",
                                   "f7e04ae93a7d580c",
                                   "fbaee0d65df3f836",
                                   "fd1ace2b02aacc70"
                                ]
                             ],
                             "field_detail":"sdk_test_document"
                          }
                       ],
                       "tags":[
                          "sdk_test_document"
                       ],
                       "notes":"",
                       "score":70
                    }



          **Example Response Payload**::

                    {
                      "body":"74496a75-6eaa-460e-8055-937b7eab4af2",
                      "errors":[],
                      "totalResults":1
                    }

        """
        path = '/v3/public/asset/'
        response = self.conn.request(
            path,
            data=json.dumps(fingerprint_data)
        )
        return response.json()

    def add_pii(self, account_id, custom_id, tags, pii_type, email, first_name=None,
                middle_name=None, last_name=None, ssn=None, street_address=None, city=None, state_province=None,
                zip_postal_code=None, phone=None, credit_card=None, medicare_id=None, passport=None, iban=None,
                offline=False):
        """Creates a new PII record in the given project.

            :param str account_id: Account ID.
            :param str custom_id: A custom ID of the asset.
            :param list tags: tags for PII.
            :param str  pii_type: PII Type.
            :param str pii_type: PII Type.
            :param str email: An email address.
            :param str first_name: First Name Defaults to :obj:`NoneType`.
            :param str middle_name: Middle Name Defaults to :obj:`NoneType`.
            :param str last_name:  Last name Defaults to :obj:`NoneType`.
            :param str ssn: SSN Defaults to :obj:`NoneType`.
            :param str street_address: Address Defaults to :obj:`NoneType`.
            :param str city: City Defaults to :obj:`NoneType`.
            :param str state_province: State Defaults to :obj:`NoneType`.
            :param int  zip_postal_code: zip_postal_code Defaults to :obj:`NoneType`.
            :param str phone: Phone Defaults to :obj:`NoneType`.
            :param str credit_card: Credit card Defaults to :obj:`NoneType`.
            :param str medicare_id: Medicate ID Defaults to :obj:`NoneType`.
            :param str passport: Passport Defaults to :obj:`NoneType`.
            :param str iban: IBAN Defaults to :obj:`NoneType`.
            :param bool offline: offline Run in "offline mode". No data is sent to the Matchlight server. Returns dictionary of values instead of a :class:`~.Json` instance.
            :return:
                returns :class:`~.Json`: Created Json with metadata.

            **Example Request Payload**::

                    {
                       "account_id":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                       "custom_id":"sdk_test",
                       "asset_detail":"employee_pii",
                       "type":"employee_pii",
                       "tags":[
                          "sdk_test"
                       ],
                       "fields":[
                          {
                             "field_detail":"name_fingerprints",
                             "type":"name",
                             "variants":[
                                [
                                   "445b63dd1c27e5e0",
                                   "5b0d82bd4fa62cff",
                                   "96ef10ea6ed1e24f"
                                ],
                                [
                                   "534f4bf243710747",
                                   "cb33787f061202b8",
                                   "d2abd30ffc5a59e6"
                                ],
                                [
                                   "8cb3ba54829a0cf3",
                                   "c7abb3ca00ee1c4e",
                                   "d0b58abfb66b396e"
                                ],
                                [
                                   "98a060802d12a74e",
                                   "c0bcd0583f02eac0",
                                   "d2abd30ffc5a59e6"
                                ],
                                [
                                   "8cb3ba54829a0cf3",
                                   "c0bcd0583f02eac0",
                                   "c7abb3ca00ee1c4e"
                                ],
                                [
                                   "01220cc0d1f441fa",
                                   "24a069c9b3619f47",
                                   "d2abd30ffc5a59e6"
                                ],
                                [
                                   "15726536a1af6e33",
                                   "8cb3ba54829a0cf3",
                                   "c7abb3ca00ee1c4e"
                                ]
                             ]
                          },
                          {
                             "field_detail":"email_fingerprints",
                             "type":"email",
                             "variants":[
                                [
                                   "446f53bc7885490d"
                                ],
                                [
                                   "1bc0e0207c505930"
                                ]
                             ]
                          },
                          {
                             "field_detail":"ssn_fingerprints",
                             "type":"ssn",
                             "variants":[
                                [
                                   "6870332d558b1b19"
                                ]
                             ]
                          },
                          {
                             "field_detail":"street_address_fingerprints",
                             "type":"address",
                             "variants":[
                                [
                                   "8af8a7ee69be06a2",
                                   "9dff1185a0d275d1",
                                   "cfe75fd6855237b4"
                                ],
                                [
                                   "1709f58fcb0b21f4",
                                   "27c2df40e8863a96",
                                   "8af8a7ee69be06a2"
                                ],
                                [
                                   "21c61e5688c7db0e",
                                   "49b7c77feb4e375e",
                                   "8af8a7ee69be06a2"
                                ],
                                [
                                   "407c83ef7ba61c1e",
                                   "60ccfbc6af6dfc8f",
                                   "8af8a7ee69be06a2"
                                ],
                                [
                                   "65b19cda6771470f",
                                   "8af8a7ee69be06a2",
                                   "b3482aecc6661d52"
                                ],
                                [
                                   "45cb705fed73f400",
                                   "8af8a7ee69be06a2",
                                   "9dff1185a0d275d1"
                                ],
                                [
                                   "407c83ef7ba61c1e",
                                   "8af8a7ee69be06a2",
                                   "971c548dad1c6408"
                                ],
                                [
                                   "8af8a7ee69be06a2",
                                   "971c548dad1c6408",
                                   "fdc4e83d02e1f5cb"
                                ],
                                [
                                   "62935ea5317fb53b",
                                   "7bd4d6350eca79a0",
                                   "8af8a7ee69be06a2"
                                ],
                                [
                                   "85527d5ff1975d67",
                                   "8af8a7ee69be06a2",
                                   "b3482aecc6661d52"
                                ],
                                [
                                   "3475d3556e9f3fa1",
                                   "8af8a7ee69be06a2",
                                   "90ee3afef5069ce5"
                                ],
                                [
                                   "21c61e5688c7db0e",
                                   "8af8a7ee69be06a2",
                                   "fc45680581e82656"
                                ]
                             ]
                          },
                          {
                             "field_detail":"city_state_zip_fingerprints",
                             "type":"region",
                             "variants":[
                                [
                                   "b364f0ab8867203a",
                                   "ebf2b257d3dcc722"
                                ],
                                [
                                   "07197d34f21a74fa",
                                   "485f7eaa670bfe99"
                                ],
                                [
                                   "b364f0ab8867203a",
                                   "c00279d1dfc137a4",
                                   "d978beceaee3f135",
                                   "f302fa53bc6c1c06"
                                ],
                                [
                                   "42b34a271aebb143",
                                   "485f7eaa670bfe99",
                                   "4860e3d32453e50c",
                                   "6d898134bea3cd8a"
                                ]
                             ]
                          },
                          {
                             "field_detail":"phone_fingerprints",
                             "type":"phone",
                             "variants":[
                                [
                                   "7428b2f77cfc1743"
                                ]
                             ]
                          },
                          {
                             "field_detail":"credit_card_fingerprints",
                             "type":"credit_card",
                             "variants":[
                                [
                                   "4e2af5c2d6ea48fb"
                                ]
                             ]
                          },
                          {
                             "field_detail":"medicare_fingerprints",
                             "type":"medicare_id",
                             "variants":[
                                [
                                   "8e5fd73a05a2ff36"
                                ]
                             ]
                          },
                          {
                             "field_detail":"passport_fingerprints",
                             "type":"passport",
                             "variants":[
                                [
                                   "4fe56b36ca016874"
                                ]
                             ]
                          },
                          {
                             "field_detail":"iban_fingerprints",
                             "type":"iban",
                             "variants":[
                                [
                                   "286529dc0958ffaa",
                                   "d407149b5696bef3"
                                ],
                                [
                                   "286529dc0958ffaa",
                                   "403f647df970960a"
                                ]
                             ]
                          }
                       ]
                    }



            **Example Response Payload**::

                    {
                      "body":"b34ad06e-7d27-496b-9047-8ce64734705a",
                      "errors":[],
                      "totalResults":1
                    }

       """

        if account_id is None:
            raise matchlight.error.SDKError(
                'Provide valid account id')

        if first_name is not None and last_name is None:
            raise matchlight.error.SDKError(
                'Fingerprinter Failed: the last_name argument is required '
                'along with the first_name argument.'
            )

        if first_name is None and last_name is not None:
            raise matchlight.error.SDKError(
                'Fingerprinter Failed: the first_name argument is required '
                'along with the last_name argument.'
            )

        data = {
            "account_id": account_id,
            "custom_id": custom_id,
        }

        if pii_type:
            data['type'] = pii_type
            # TODO change to asset_detail
            data["asset_detail"] = pii_type

        if tags:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = [tags]

        fields_list = list()
        if any((first_name, middle_name, last_name)):
            name_fingerprints = fingerprints_pii_name_variants(
                first_name or '', middle_name or None, last_name or '')
            field = dict()
            field['field_detail'] = 'name_fingerprints'
            field['type'] = 'name'
            field['variants'] = name_fingerprints

            fields_list.append(field)

        if email:
            email_fingerprints = fingerprints_pii_email_address(email)
            field = dict()
            field['field_detail'] = 'email_fingerprints'
            field['type'] = 'email'
            field['variants'] = email_fingerprints

            fields_list.append(field)

        if ssn:
            ssn_fingerprints = [fingerprints_pii_ssn(ssn)]
            field = dict()
            field['field_detail'] = 'ssn_fingerprints'
            field['type'] = 'ssn'
            field['variants'] = ssn_fingerprints

            fields_list.append(field)

        if street_address:
            address_fingerprints = fingerprints_pii_address_variants(street_address)
            field = dict()
            field['field_detail'] = 'street_address_fingerprints'
            field['type'] = 'address'
            field['variants'] = address_fingerprints

            fields_list.append(field)

        if any((city, state_province, zip_postal_code)):
            csz_fingerprints = fingerprints_pii_city_state_zip_variants(
                *[six.text_type(text) if text is not None else ''
                  for text in (city, state_province, zip_postal_code)])
            field = dict()
            field['field_detail'] = 'city_state_zip_fingerprints'
            field['type'] = 'region'
            field['variants'] = csz_fingerprints

            fields_list.append(field)

        if phone:
            phone_fingerprints = fingerprints_pii_phone_number(phone)
            field = dict()
            field['field_detail'] = 'phone_fingerprints'
            field['type'] = 'phone'
            field['variants'] = [phone_fingerprints]

            fields_list.append(field)

        if credit_card:
            cc_fingerprints = fingerprints_pii_credit_card(credit_card)
            field = dict()
            field['field_detail'] = 'credit_card_fingerprints'
            field['type'] = 'credit_card'
            field['variants'] = [cc_fingerprints]

            fields_list.append(field)

        if medicare_id:
            medicare_id_fingerprints = fingerprints_pii_medicare_id(
                medicare_id
            )
            field = dict()
            field['field_detail'] = 'medicare_fingerprints'
            field['type'] = 'medicare_id'
            field['variants'] = [medicare_id_fingerprints]

            fields_list.append(field)

        if passport:
            passport_fingerprints = fingerprints_pii_passport(passport)
            field = dict()
            field['field_detail'] = 'passport_fingerprints'
            field['type'] = 'passport'
            field['variants'] = [passport_fingerprints]

            fields_list.append(field)

        if iban:
            iban_fingerprints = fingerprints_pii_iban(iban)
            field = dict()
            field['field_detail'] = 'iban_fingerprints'
            field['type'] = 'iban'
            field['variants'] = iban_fingerprints

            fields_list.append(field)

        data['fields'] = fields_list

        if offline:
            return data
        else:
            return self.add_pii_from_fingerprints(data)

    def add_pii_from_fingerprints(self, fingerprint_data):
        """Add a PII record from fingerprinted data generated by the :class:`~/.Assets.add_pii` in offline mode.

           :param dict fingerprint_data: The output of :class:`~/.Assets.add_pii(offline=True)`
           :returns: the `Json` object

           >>> API_ENDPOINT_PATH = '/v3/public/asset/'

           **Example Request Payload**::

                    {
                       "account_id":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                       "custom_id":"sdk_test",
                       "asset_detail":"employee_pii",
                       "type":"employee_pii",
                       "tags":[
                          "sdk_test"
                       ],
                       "fields":[
                          {
                             "field_detail":"name_fingerprints",
                             "type":"name",
                             "variants":[
                                [
                                   "445b63dd1c27e5e0",
                                   "5b0d82bd4fa62cff",
                                   "96ef10ea6ed1e24f"
                                ],
                                [
                                   "534f4bf243710747",
                                   "cb33787f061202b8",
                                   "d2abd30ffc5a59e6"
                                ],
                                [
                                   "8cb3ba54829a0cf3",
                                   "c7abb3ca00ee1c4e",
                                   "d0b58abfb66b396e"
                                ],
                                [
                                   "98a060802d12a74e",
                                   "c0bcd0583f02eac0",
                                   "d2abd30ffc5a59e6"
                                ],
                                [
                                   "8cb3ba54829a0cf3",
                                   "c0bcd0583f02eac0",
                                   "c7abb3ca00ee1c4e"
                                ],
                                [
                                   "01220cc0d1f441fa",
                                   "24a069c9b3619f47",
                                   "d2abd30ffc5a59e6"
                                ],
                                [
                                   "15726536a1af6e33",
                                   "8cb3ba54829a0cf3",
                                   "c7abb3ca00ee1c4e"
                                ]
                             ]
                          },
                          {
                             "field_detail":"email_fingerprints",
                             "type":"email",
                             "variants":[
                                [
                                   "446f53bc7885490d"
                                ],
                                [
                                   "1bc0e0207c505930"
                                ]
                             ]
                          },
                          {
                             "field_detail":"ssn_fingerprints",
                             "type":"ssn",
                             "variants":[
                                [
                                   "6870332d558b1b19"
                                ]
                             ]
                          },
                          {
                             "field_detail":"street_address_fingerprints",
                             "type":"address",
                             "variants":[
                                [
                                   "8af8a7ee69be06a2",
                                   "9dff1185a0d275d1",
                                   "cfe75fd6855237b4"
                                ],
                                [
                                   "1709f58fcb0b21f4",
                                   "27c2df40e8863a96",
                                   "8af8a7ee69be06a2"
                                ],
                                [
                                   "21c61e5688c7db0e",
                                   "49b7c77feb4e375e",
                                   "8af8a7ee69be06a2"
                                ],
                                [
                                   "407c83ef7ba61c1e",
                                   "60ccfbc6af6dfc8f",
                                   "8af8a7ee69be06a2"
                                ],
                                [
                                   "65b19cda6771470f",
                                   "8af8a7ee69be06a2",
                                   "b3482aecc6661d52"
                                ],
                                [
                                   "45cb705fed73f400",
                                   "8af8a7ee69be06a2",
                                   "9dff1185a0d275d1"
                                ],
                                [
                                   "407c83ef7ba61c1e",
                                   "8af8a7ee69be06a2",
                                   "971c548dad1c6408"
                                ],
                                [
                                   "8af8a7ee69be06a2",
                                   "971c548dad1c6408",
                                   "fdc4e83d02e1f5cb"
                                ],
                                [
                                   "62935ea5317fb53b",
                                   "7bd4d6350eca79a0",
                                   "8af8a7ee69be06a2"
                                ],
                                [
                                   "85527d5ff1975d67",
                                   "8af8a7ee69be06a2",
                                   "b3482aecc6661d52"
                                ],
                                [
                                   "3475d3556e9f3fa1",
                                   "8af8a7ee69be06a2",
                                   "90ee3afef5069ce5"
                                ],
                                [
                                   "21c61e5688c7db0e",
                                   "8af8a7ee69be06a2",
                                   "fc45680581e82656"
                                ]
                             ]
                          },
                          {
                             "field_detail":"city_state_zip_fingerprints",
                             "type":"region",
                             "variants":[
                                [
                                   "b364f0ab8867203a",
                                   "ebf2b257d3dcc722"
                                ],
                                [
                                   "07197d34f21a74fa",
                                   "485f7eaa670bfe99"
                                ],
                                [
                                   "b364f0ab8867203a",
                                   "c00279d1dfc137a4",
                                   "d978beceaee3f135",
                                   "f302fa53bc6c1c06"
                                ],
                                [
                                   "42b34a271aebb143",
                                   "485f7eaa670bfe99",
                                   "4860e3d32453e50c",
                                   "6d898134bea3cd8a"
                                ]
                             ]
                          },
                          {
                             "field_detail":"phone_fingerprints",
                             "type":"phone",
                             "variants":[
                                [
                                   "7428b2f77cfc1743"
                                ]
                             ]
                          },
                          {
                             "field_detail":"credit_card_fingerprints",
                             "type":"credit_card",
                             "variants":[
                                [
                                   "4e2af5c2d6ea48fb"
                                ]
                             ]
                          },
                          {
                             "field_detail":"medicare_fingerprints",
                             "type":"medicare_id",
                             "variants":[
                                [
                                   "8e5fd73a05a2ff36"
                                ]
                             ]
                          },
                          {
                             "field_detail":"passport_fingerprints",
                             "type":"passport",
                             "variants":[
                                [
                                   "4fe56b36ca016874"
                                ]
                             ]
                          },
                          {
                             "field_detail":"iban_fingerprints",
                             "type":"iban",
                             "variants":[
                                [
                                   "286529dc0958ffaa",
                                   "d407149b5696bef3"
                                ],
                                [
                                   "286529dc0958ffaa",
                                   "403f647df970960a"
                                ]
                             ]
                          }
                       ]
                    }



           **Example Response Payload**::

                    {
                      "body":"b34ad06e-7d27-496b-9047-8ce64734705a",
                      "errors":[],
                      "totalResults":1
                    }

        """
        path = '/v3/public/asset/'
        response = self.conn.request(
            path,
            data=json.dumps(fingerprint_data)
        )
        return response.json

    def add_plain_text(self, account_id, asset_type, asset_detail=str(), customer_request_term=str(),
                       monitoring_term=str(), data_science_term=str(), tags=list()):
        """Creates a new PII record in the given project.

            :param str account_id: Project account id.
            :param str asset_type: A custom ID of the asset.
            :param str asset_detail: asset detail
            :param str customer_request_term: customer_request_term
            :param str monitoring_term: monitoring_term
            :param str data_science_term: description data science term
            :param str tags: An email address.
            :return:
               returns :class:`~.Json`: Created Json with metadata.

            >>> API_ENDPOINT_PATH = '/v3/public/asset?unsafe=true'

            **Example Request Payload**::

                    {
                               "account_id":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                               "type":"keyword",
                               "asset_detail":"public api text",
                               "tags":[
                                  "publicapi",
                                  "public_keyword"
                               ],
                               "fields":[
                                  {
                                     "field_detail":"",
                                     "type":"keyword",
                                     "status":"approved",
                                     "terms":[
                                        {
                                           "type":"customer_request",
                                           "term":""
                                        },
                                        {
                                           "type":"regex",
                                           "term":"Public|APi|test"
                                        },
                                        {
                                           "type":"data_science",
                                           "term":"public api"
                                        }
                                     ]
                                  }
                               ]
                     }


            **Example Response Payload**::

                    {
                      "body":"b34ad06e-7d27-496b-9047-8ce64734705a",
                      "errors":[],
                      "totalResults":1
                    }

        """
        if account_id is None:
            raise matchlight.error.SDKError(
                'Provide valid account id')
        data = {
            "account_id": account_id,
            "type": asset_type,
            "asset_detail": asset_detail,
            "tags": tags
        }

        fields = dict()
        fields['field_detail'] = customer_request_term
        fields['type'] = asset_type
        fields['status'] = 'approved'

        terms = list()
        terms.append({"type": "customer_request", "term": customer_request_term})
        terms.append({"type": "regex", "term": monitoring_term})
        terms.append({"type": "data_science", "term": data_science_term})

        fields['terms'] = terms
        data['fields'] = [fields]

        path = '/v3/public/asset?unsafe=true'
        print(data)
        response = self.conn.request(
            path,
            data=json.dumps(data)
        )
        return response.json

    def add_source_code(self, account_id, custom_id, asset_detail, tags, code_path,
                        match_score_threshold=70, offline=False):
        """Creates a new source code record in the given project.

           :param str account_id: Account ID.
           :param str custom_id: Custom Id.
           :param str  asset_detail:  Label.
           :param str tags: Tag of source code.
           :param str code_path: Source Code path.
           :param int match_score_threshold: Run in "offline mode". No data is sent to the Matchlight server
           :param bool offline: Run in "offline mode". No data is sent to the Matchlight server.

           :return:
               returns :class:`~.Json` Created record with metadata.

           **Example Request Payload**::

                    {
                       "account_id":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                       "customId":"sdk_test_source_code",
                       "asset_detail":"sdk_test_source_code",
                       "type":"source_code",
                       "metadata":{
                          "fingerprinting_tool_name":"Python SDK",
                          "fingerprinting_tool_version":"unknown",
                          "min_score":"0"
                       },
                       "fields":[
                          {
                             "type":"sourceCode",
                             "variants":[
                                [
                                   "01385745fac13d2d",
                                   "038c0ef8952a1392",
                                   "0ccef1a0979b9d28",
                                   "1b84f5dea567442a",
                                   "2d8d3c60844fad2c",
                                   "2e7135784118cc28",
                                   "3123f225adec87de",
                                   "4c638f6b53b24bce",
                                   "4fe693c64944ffb7",
                                   "53bb2a9c50374625",
                                   "5f167b61b14e1cbf",
                                   "63d73fac669a6140",
                                   "6d55be881af3e46d",
                                   "6d9264822564daba",
                                   "702a627e0c78ae91",
                                   "74ee96b1fbdcd0ad",
                                   "7ca227b625af3941",
                                   "8915943f0bc7896b",
                                   "8ecdf1499000a283",
                                   "94f09856d4bf1227",
                                   "9539c44bb26184d2",
                                   "a049c40dd93aa6af",
                                   "aa6943967b8f89c3",
                                   "be7b0ff501c58e6b",
                                   "c28bbe77e0d2dcce",
                                   "c42224b1c4a27d42",
                                   "d8696ac755d29c2f",
                                   "dae67c8151fd70bd",
                                   "ed108495de4220c4",
                                   "fb308c97e2976867",
                                   "ff0f4d8a9f473747"
                                ]
                             ],
                             "field_detail":"sdk_test_source_code"
                          }
                       ],
                       "tags":[
                          "sdk_test_source_code"
                       ]
                    }


           **Example Response Payload**::

                    {
                      "body":"7d3623bf-aa00-41bf-bb63-7b5d79f85c40",
                      "errors":[],
                      "totalResults":1
                    }

        """
        with io.open(code_path, 'r', encoding='utf-8') as document:
            content = document.read()

        if len(content) > MAX_DOCUMENT_FINGERPRINTS:
            raise matchlight.error.SDKError(
                'Fingerprinter Failed: the maximum length of a Source Code '
                'record is 840 characters.'
            )

        result_json = fingerprint(content, flags=OPTIONS_TILED, mode=MODE_CODE)
        result = json.loads(result_json)
        fingerprints = result['data']['fingerprints']

        data = {
            'account_id': account_id,
            'customId': custom_id,
            'asset_detail': asset_detail,
            'type': "source_code",
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        fields = dict()
        fields['type'] = 'sourceCode'
        fields['variants'] = [fingerprints]
        fields['field_detail'] = asset_detail

        data['fields'] = [fields]
        if tags is not None:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = [tags]
        if match_score_threshold is not None:
            data['metadata']['min_score'] = str(match_score_threshold)
        if offline:
            return data
        else:
            return self.add_source_code_from_fingerprints(data)

    def add_source_code_from_fingerprints(self, fingerprint_data):
        """Add a source code record from fingerprinted data generated by the :class:`~/.Assets.add_source_code` in offline mode.

        :param dict fingerprint_data: The output of :class:`~/.Assets.add_source_code(offline=True)`

        >>> API_ENDPOINT_PATH = "/v3/public/asset/"

        **Example Request Payload**::

                    {
                       "account_id":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                       "customId":"sdk_test_source_code",
                       "asset_detail":"sdk_test_source_code",
                       "type":"source_code",
                       "metadata":{
                          "fingerprinting_tool_name":"Python SDK",
                          "fingerprinting_tool_version":"unknown",
                          "min_score":"0"
                       },
                       "fields":[
                          {
                             "type":"sourceCode",
                             "variants":[
                                [
                                   "01385745fac13d2d",
                                   "038c0ef8952a1392",
                                   "0ccef1a0979b9d28",
                                   "1b84f5dea567442a",
                                   "2d8d3c60844fad2c",
                                   "2e7135784118cc28",
                                   "3123f225adec87de",
                                   "4c638f6b53b24bce",
                                   "4fe693c64944ffb7",
                                   "53bb2a9c50374625",
                                   "5f167b61b14e1cbf",
                                   "63d73fac669a6140",
                                   "6d55be881af3e46d",
                                   "6d9264822564daba",
                                   "702a627e0c78ae91",
                                   "74ee96b1fbdcd0ad",
                                   "7ca227b625af3941",
                                   "8915943f0bc7896b",
                                   "8ecdf1499000a283",
                                   "94f09856d4bf1227",
                                   "9539c44bb26184d2",
                                   "a049c40dd93aa6af",
                                   "aa6943967b8f89c3",
                                   "be7b0ff501c58e6b",
                                   "c28bbe77e0d2dcce",
                                   "c42224b1c4a27d42",
                                   "d8696ac755d29c2f",
                                   "dae67c8151fd70bd",
                                   "ed108495de4220c4",
                                   "fb308c97e2976867",
                                   "ff0f4d8a9f473747"
                                ]
                             ],
                             "field_detail":"sdk_test_source_code"
                          }
                       ],
                       "tags":[
                          "sdk_test_source_code"
                       ]
                    }



        **Example Response Payload**::

                    {
                      "body":"7d3623bf-aa00-41bf-bb63-7b5d79f85c40",
                      "errors":[],
                      "totalResults":1
                    }

        """
        path = '/v3/public/asset/'
        response = self.conn.request(
            path,
            data=json.dumps(fingerprint_data)
        )
        return response.json()

    def delete_asset(self, asset_id):
        """Delete a fingerprinted record.

            :param str asset_id: The Asset object or identifier to be deleted.
            :return: returns :obj:`NoneType`
            >>> API_ENDPOINT_PATH = "/v3/public/asset/delete/asset_id"

            **Response Payload**::

               {
                       "body": None,
                       "errors":[
                       ],
                       "totalResults":1
               }

        """
        self.conn.public_request('/v3/public/asset/delete/{}'.format(asset_id), method="DELETE")

    def list_assets(self, status=None, createdFrom=None, createdTo=None, updatedFrom=None,
                    updatedTo=None, limit=None, offset=None, tags=None):
        """Get all alerts in the given project.

             :param str status:
                      - approved: Returns active assets we are currently monitoring for.
                      - deleted: Returns deleted assets we are no longer monitoring for.
             :param datetime createdFrom: Returns assets created equal to or from this date forward.
             :param datetime createdTo: Returns assets created equal to or up to this date.
             :param datetime updatedFrom: Returns assets updated equal to or from this date forward.
             :param datetime updatedTo: Returns assets updated equal to or up to this date.
             :param str limit: The no of alerts to pull.
             :param str offset: offset of the alerts list.
             :param str tags: The alert tags
             :return:
                    returns :class:`~.Json` Created json with metadata.

             >>> ml.alerts.list_assets(status, initiatedFrom='2020-11-04 20:08:11', initiatedTo='2020-11-05 20:08:11')
             >>> ml.alerts.list_assets(status, updatedFrom='2020-11-04 20:08:11', updatedTo='2020-11-05 20:08:11')

             >>> API_ENDPOINT_PATH = "/v3/public/asset/"


             **Example Response Payload**::

                {
                       "body":{
                          "accountId":"73c489e8-4df5-49f6-a3ed-6e544df59809",
                          "accountName":"PublicApi",
                          "assets":[
                             {
                                "id":"a58a7255-0542-423b-b928-f447648f915d",
                                "customId":"a58a72550542423b",
                                "assetType":"Keywords",
                                "assetDetails":"pub",
                                "methodType":"Plaintext",
                                "fields":[
                                   {
                                      "name":"Keyword",
                                      "fieldDetail":"None",
                                      "term":"Public|APi|test"
                                   }
                                ],
                                "tags":[
                                   "publicapi",
                                   "public_keyword",
                                   "api_public_test"
                                ],
                                "deletedAt":"None",
                                "createdAt":"2020-12-08T15:24:40.393797",
                                "updatedAt":"2020-12-08T15:24:40.393797"
                             }
                          ]
                       },
                       "errors":[

                       ],
                       "totalResults":109
                }
        """
        statuses = status if status else None
        path = "/v3/public/asset/"

        response = self.conn.public_request(
            path,
            params={
                'status': statuses,
                'tags': tags,
                'createdFrom': createdFrom,
                'createdTo': createdTo,
                'updatedFrom': updatedFrom,
                'updatedTo': updatedTo,
                'limit': limit,
                'offset': offset,
            },
            method='GET',
        )

        return response

    def assets_count(self, status=None, createdFrom=None, createdTo=None, updatedFrom=None,
                     updatedTo=None, tags=None):
        """Returns a count of all assets belonging to an account. If there are no assets, an empty array is returned.

              :param str status:
                       - approved: Returns a count of active assets we are currently monitoring for.
                       - deleted: Returns a count of deleted assets we are no longer monitoring for.
              :param datetime createdFrom: Returns a count of assets created equal to or from this date forward.
              :param datetime createdTo: Returns a count of assets created equal to or up to this date.
              :param datetime updatedFrom: Returns a count of assets updated equal to or from this date forward.
              :param datetime updatedTo: Returns a count of assets updated equal to or up to this date.
              :param str tags: The alert tags.
              :return:
                    returns :class:`~.Json` Created json with metadata.

              >>> ml.alerts.list_assets(status, initiatedFrom='2020-11-04 20:08:11', initiatedTo='2020-11-05 20:08:11')
              >>> ml.alerts.list_assets(status, updatedFrom='2020-11-04 20:08:11', updatedTo='2020-11-05 20:08:11')

              >>> API_ENDPOINT_PATH = "/v3/public/asset/count"

              **Example Response Payload**::

                    {
                       "count": 109
                    }

        """

        statuses = status if status else None
        path = "/v3/public/asset/count"

        response = self.conn.public_request(
            path,
            params={
                'status': statuses,
                'tags': tags,
                'createdFrom': createdFrom,
                'createdTo': createdTo,
                'updatedFrom': updatedFrom,
                'updatedTo': updatedTo,
            },
            method='GET',
        )

        return response
