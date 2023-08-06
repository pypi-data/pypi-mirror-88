#!/bin/python3

__author__ = "Manoj Kumar Arram"

import matchlight as ml
import json
import os

cpath = "/".join(os.path.abspath(os.getcwd()).split('/'))

ml = ml.Matchlight(access_key="d30417b47b0a45ba9966321eaca234c2", secret_key="19f6d9c97f834338be4a0685ad7e9442")
account_id = '73c489e8-4df5-49f6-a3ed-6e544df59809'

pii_path = cpath + "/resources/pii.json"

with open(pii_path, 'r') as f:
    assets = json.loads(f.read())


def pii_online():
    # Online
    try:
        ml.assets.add_pii(account_id=assets.get("account_id"), custom_id=assets.get('custom_id'),
                          tags=assets.get('tags'),
                          pii_type=assets.get("pii_type"),
                          email=assets.get("email"), first_name=assets.get('first_name'),
                          middle_name=assets.get("middle_name"), last_name=assets.get("last_name"),
                          ssn=assets.get("ssn"),
                          street_address=assets.get("street_address"), city=assets.get("city"),
                          state_province=assets.get("state_province"),
                          zip_postal_code=assets.get("zip_postal_code"), phone=assets.get("phone"),
                          credit_card=assets.get("credit_card"),
                          medicare_id=assets.get("medicare_id"), passport=assets.get("passport"),
                          iban=assets.get("iban"), offline=False)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


def pii_offline():
    # Offline
    try:
        res = ml.assets.add_pii(account_id=assets.get("account_id"), custom_id=assets.get('custom_id'),
                                tags=assets.get('tags'),
                                pii_type=assets.get("pii_type"),
                                email=assets.get("email"), first_name=assets.get('first_name'),
                                middle_name=assets.get("middle_name"), last_name=assets.get("last_name"),
                                ssn=assets.get("ssn"),
                                street_address=assets.get("street_address"), city=assets.get("city"),
                                state_province=assets.get("state_province"),
                                zip_postal_code=assets.get("zip_postal_code"), phone=assets.get("phone"),
                                credit_card=assets.get("credit_card"),
                                medicare_id=assets.get("medicare_id"), passport=assets.get("passport"),
                                iban=assets.get("iban"), offline=True)

        f_name = assets.get("account_id") + "_pii.json"
        with open(f_name, "w") as res_file:
            res_file.write(json.dumps(res))
        print("Hurray!! \U0001F973 Generated Offline data and saved to ", f_name)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


def pii_fp_file(data):
    try:
        ml.assets.add_pii_from_fingerprints(data)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


def delete_asset(asset_id):
    try:
        ml.assets.delete_asset(asset_id)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


doc_path = cpath + "/resources/document.json"

with open(doc_path, 'r') as f:
    try:
        documents = json.loads(f.read())
    except Exception as ex:
        print("unable to read document.json ", ex)


def document_online():
    try:
        # Online
        ml.assets.add_document(account_id=documents.get("account_id"), custom_id=documents.get("custom_id"),
                               asset_detail=documents.get("asset_detail"), tags=documents.get("tags"),
                               content=documents.get("content"),
                               match_score_threshold=documents.get("match_score_threshold"),
                               offline=False)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


def document_offline():
    # Offline
    try:
        res = ml.assets.add_document(account_id=documents.get("account_id"), custom_id=documents.get("custom_id"),
                                     asset_detail=documents.get("asset_detail"), tags=documents.get("tags"),
                                     content=documents.get("content"),
                                     match_score_threshold=documents.get("match_score_threshold"),
                                     offline=True)

        f_name = assets.get("account_id") + "_document.json"
        with open(f_name, "w") as res_file:
            res_file.write(json.dumps(res))
        print("Hurray!! \U0001F973 Generated Offline data and saved to ", f_name)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


def document_from_file(data):
    try:
        ml.assets.add_document_from_fingerprints(data)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


source_path = cpath + "/resources/sourcecode.json"

with open(source_path, 'r') as f:
    try:
        sourcecode = json.loads(f.read())
    except Exception as ex:
        print("unable to read source code json ", ex)


def source_code_online():
    # Online
    try:
        ml.assets.add_source_code(account_id=sourcecode.get("account_id"), custom_id=sourcecode.get("custom_id"),
                                  asset_detail=sourcecode.get("asset_detail"), tags=sourcecode.get("tags"),
                                  code_path=sourcecode.get("code_path"),
                                  match_score_threshold=sourcecode.get("match_score_threshold"),
                                  offline=False)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


def source_code_offline():
    # Offline
    try:
        res = ml.assets.add_source_code(account_id=sourcecode.get("account_id"), custom_id=sourcecode.get("custom_id"),
                                        asset_detail=sourcecode.get("asset_detail"), tags=sourcecode.get("tags"),
                                        code_path=sourcecode.get("code_path"),
                                        match_score_threshold=sourcecode.get("match_score_threshold"),
                                        offline=True)

        f_name = assets.get("account_id") + "_source_code.json"
        with open(f_name, "w") as res_file:
            res_file.write(json.dumps(res))
        print("Hurray!! \U0001F973 Generated Offline data and saved to ", f_name)

    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


def source_from_file(data):
    try:
        ml.assets.add_source_code_from_fingerprints(data)
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)


term_path = cpath + "/resources/plaintext.json"

with open(term_path, 'r') as f:
    try:
        terms = json.loads(f.read())
    except Exception as ex:
        print("unable to read source code json ", ex)


# Terms
def add_plain_text():
    try:
        ml.assets.add_plain_text(account_id=terms.get("account_id"), asset_type=terms.get("asset_type"),
                                 asset_detail=terms.get("asset_detail"),
                                 customer_request_term=terms.get("customer_request_term"),
                                 monitoring_term=terms.get("monitoring_term"),
                                 data_science_term=terms.get("data_science_term"), tags=terms.get("tags"))
    except Exception as e:
        print("My Bad \U0001F625 Unable to process your request: ", e)
