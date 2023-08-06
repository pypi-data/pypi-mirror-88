# *-* coding:utf-8 *-*

from dotenv import load_dotenv
import os
import requests
import logging
logging.basicConfig(level=logging.INFO)

# Documentation : how to implement Google Analytics on Flask: https://cloud.google.com/appengine/docs/flexible/python/integrating-with-analytics

# Definition of the terms: https://support.google.com/analytics/answer/1033068?hl=en

# Environment variables are defined in app.yaml.
import sys
sys.path.append(os.path.join(os.getcwd()))
logging.info(f' {os.path.join(os.getcwd())}')
logging.info('before')
load_dotenv(verbose=True)
logging.info('after')
GA_TRACKING_ID = os.environ["COM_GOOGLE_ANALYTICS_TRACKING_ID"]


class GoogleAnalytics():
    def __init__(self):
        pass

    def track_event(self, category, action, label=None, value=0, ua=None):
        data = {
            "v": "1",  # API Version.
            "tid": GA_TRACKING_ID,  # Tracking ID / Property ID.
            # Anonymous Client Identifier. Ideally, this should be a UUID that
            # is associated with particular user, device, or browser instance.
            "cid": "000000",  # client id, unique identifier to generate in the future
            "t": "event",  # Event hit type.
            "ec": category,  # Event category.
            "ea": action,  # Event action.
            "el": label,  # Event label.
            "ev": value,  # Event value, must be an integer
            "ua": ua,  # User Agent
        }

        logging.debug(f"Google analytics - tracked event: {data}")

        try:
            # See documentation : https://developers.google.com/analytics/devguides/collection/protocol/v1/reference
            response = requests.post(
                "https://www.google-analytics.com/collect", data=data)

            # If the request fails, this will raise a RequestException. Depending
            # on your application's needs, this may be a non-error and can be caught
            # by the caller.
            response.raise_for_status()
        except Exception as e:
            logging.exception(
                f"Exception: Set an event in Google Analytics: {e}")
