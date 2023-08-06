
import requests
import json
import time
import os
import logging
from enum import Enum
from urllib.parse import quote

log = logging.getLogger(__name__)

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)


class Status(Enum):
    FINISHED = 'finished'
    STARTED = 'started'
    CORRECTED = 'corrected'


class Client():

    def __init__(self, apikey):
        self.fahrzeugschein = ""
        self.status = "started"
        self.session = ""
        self.endpoint = os.environ.get("REGISTRATION_RECOGNITION_ENDPOINT",
                                       "https://api.mmmint.ai/fahrzeugschein")
        self.api_version = os.environ.get("REGISTRATION_RECOGNITION_VERSION", "v1")
        self.base_url = "{}/{}".format(self.endpoint, self.api_version)
        if not apikey:
            raise UnauthorizedException()
        self.api_key = apikey

    def new_fahrzeugschein(self, fahrzeugschein_path):
        self.fahrzeugschein_path = fahrzeugschein_path

        url = '{}/fahrzeugschein?access_token={}'.format(self.base_url, self.api_key)
        log.info(url)

        with open(self.fahrzeugschein_path, 'rb') as f:
            r = requests.post(url, files={'file': f})
        return self._handle_response(r)

    def new_fahrzeugschein_url(self, fahrzeugschein_url):
        self.fahrzeugschein_url = quote(fahrzeugschein_url, safe='')
        url = '{}/fahrzeugschein/url?image_url={}&access_token={}'.format(
            self.base_url, self.fahrzeugschein_url, self.api_key)
        log.info(url)
        r = requests.post(url)
        return self._handle_response(r)

    def get_fahrzeugschein_status(self, session_id=''):
        session_id = self._handle_empty_session(session_id)
        url = '{}/fahrzeugschein/status/{}?access_token={}'.format(
            self.base_url, session_id, self.api_key)
        log.info(url)
        r = requests.get(url)
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            log.info(response_dict)
            self.status = response_dict["status"]
            return self.status
        elif r.status_code != 200:
            self._handle_not_authenticated(r)
            self._handle_other(r)

    def get_fahrzeugschein(self):
        url = '{}/fahrzeugschein/{}?access_token={}'.format(
            self.base_url, self.session, self.api_key)
        log.info(url)
        r = requests.get(url)
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            log.info(response_dict)
            self.fahrzeugschein = response_dict
            return self.fahrzeugschein
        elif r.status_code != 200:
            self._handle_not_authenticated(r)
            self._handle_other(r)

    def edit_fahrzeugschein(self):
        data = json.dumps(self.fahrzeugschein)
        log.info(data)

        url = '{}/fahrzeugschein/{}?access_token={}'.format(
            self.base_url, self.session, self.api_key)
        log.info(url)
        r = requests.put(url, data=data)

        if r.status_code == 200:
            response_dict = json.loads(r.text)
            log.info(response_dict)
            self.fahrzeugschein = response_dict
            return self.fahrzeugschein
        elif r.status_code != 200:
            self._handle_not_authenticated(r)
            self._handle_other(r)

    def get_sessions(self):
        url = '{}/session?access_token={}'.format(
            self.base_url, self.api_key)
        log.info(url)
        r = requests.get(url)
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            log.info(response_dict)
            self.sessions = response_dict
            return self.sessions
        elif r.status_code != 200:
            self._handle_not_authenticated(r)
            self._handle_other(r)

    def is_finished(self, session_id):
        session_id = self._handle_empty_session(session_id)
        self.get_fahrzeugschein_status(session_id)

    def get_sessions_finished(self):
        sessions = self.get_sessions()
        finished_sessions = []
        for sess in sessions:
            if Status.FINISHED.value == sess["status"]:
                finished_sessions.append(sess)
        return finished_sessions

    def get_detection_bounding_boxes(self, session_id=""):
        session_id = self._handle_empty_session(session_id)
        url = '{}/detection/boundingboxes/{}?access_token={}'.format(
            self.base_url, session_id, self.api_key)
        log.info(url)
        r = requests.get(url)
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            log.info(response_dict)
            self.boundingboxes = response_dict
            return self.boundingboxes
        elif r.status_code != 200:
            self._handle_not_authenticated(r)
            self._handle_other(r)

    def get_detection_image(self, session_id=''):
        session_id = self._handle_empty_session(session_id)
        url = '{}/detection/image/{}?access_token={}'.format(
            self.base_url, session_id, self.api_key)
        log.info(url)
        r = requests.get(url)
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            log.info(response_dict)
            self.image = response_dict
            return self.image
        elif r.status_code != 200:
            self._handle_not_authenticated(r)
            self._handle_other(r)

    def get_detection_cropped_image(self, session_id=''):

        session_id = self._handle_empty_session(session_id)

        url = '{}/detection/croppedimage/{}?access_token={}'.format(
            self.base_url, session_id, self.api_key)
        log.info(url)
        r = requests.get(url)
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            log.info(response_dict)
            self.cropped_images = response_dict
            return self.cropped_images
        elif r.status_code != 200:
            self._handle_not_authenticated(r)
            self._handle_other(r)

    def _handle_response(self, r):
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            log.info(response_dict)

            self.status = response_dict["status"]
            self.session = response_dict["session_id"]
            return self.status, self.session
        elif r.status_code != 200:
            self._handle_not_authenticated(r)
            self._handle_other(r)

    def _handle_not_authenticated(self, r):
        if r.status_code == 403:
            log.error("Not authenticated")
            raise UnauthorizedException(self.api_key, r)

    def _handle_other(self, r):
        log.warning(r.reason)

    def _handle_empty_session(self, session_id):
        if not session_id:
            session_id = self.session

        if not session_id:
            raise NoSessionException()

        return session_id


class NoSessionException(Exception):
    def __init__(self, message="No session: Please provide a session_id"):
        super().__init__(self.message)


class UnauthorizedException(Exception):
    def __init__(self, api_key="", request="", message="Unauthorized: Please provide API_KEY"):
        self.api_key = api_key
        self.request = request
        self.message = message
        super().__init__(self.message)
