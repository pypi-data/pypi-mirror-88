#!/bin/python3

__author__ = "Manoj Kumar Arram"

import matchlight as ml

ml = ml.Matchlight(access_key="d30417b47b0a45ba9966321eaca234c2", secret_key="19f6d9c97f834338be4a0685ad7e9442")


def get_alerts(limit, status):
    return ml.alerts.list_alerts(limit=limit, status=status)


def get_alerts_count(status=['unvetted']):
    return ml.alerts.alerts_count(status=status)


def get_matches(limit, status):
    return ml.matches.list_matches(status=status, limit=limit)


def get_match_count(status=['published']):
    return ml.matches.match_count(status=status)


def get_assets(limit=2):
    return ml.assets.list_assets(limit=limit)


def get_asset_count():
    return ml.assets.assets_count()


def get_tags(tag_type):
    return ml.alerts.list_tags(tag_type=tag_type)
