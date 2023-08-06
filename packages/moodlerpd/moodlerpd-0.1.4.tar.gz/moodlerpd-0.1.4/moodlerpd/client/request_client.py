import json
import urllib
from urllib.parse import quote
import requests
import logging


class RequestClient:
    """
    Encapsulates the recurring logic for sending out requests to the
    Moodle-System.
    """

    stdHeader = {
        'User-Agent': (
                'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPIS26.48-43-2; wv) AppleWebKit/537.36'
                + ' (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 MoodleMobile'
        ),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def __init__(
            self,
            moodle_domain: str,
            moodle_path: str = '/',
            token: str = '',
            skip_cert_verify: bool = False,
            log_responses_to: str = None,
    ):
        self.token = token
        self.moodle_domain = moodle_domain
        self.moodle_path = moodle_path

        self.verify = not skip_cert_verify
        self.url_base = 'https://' + moodle_domain + moodle_path

        self.log_responses_to = log_responses_to
        self.log_responses = False

        if log_responses_to is not None:
            self.log_responses = True
            with open(self.log_responses_to, 'w') as response_log_file:
                response_log_file.write('JSON Log:\n\n')

        logging.getLogger("requests").setLevel(logging.WARNING)

    def post(self, function: str, data: {str: str} = None) -> object:
        """
        Sends a POST request to the REST endpoint of the Moodle system
        @param function: The Web service function to be called.
        @param data: The optional data is added to the POST body.
        @return: The JSON response returned by the Moodle system, already
        checked for errors.
        """

        if self.token is None:
            raise ValueError('The required Token is not set!')

        data_urlencoded = self._get_post_data(function, self.token, data)
        url = self._get_post_url(self.url_base, function)

        response = requests.post(url, data=data_urlencoded, headers=self.stdHeader, verify=self.verify)

        json_result = self._initial_parse(response)
        if self.log_responses and function not in ['tool_mobile_get_autologin_key']:
            with open(self.log_responses_to, 'a') as response_log_file:
                response_log_file.write('URL: {}\n'.format(response.url))
                response_log_file.write('Function: {}\n\n'.format(function))
                response_log_file.write('Data: {}\n\n'.format(data))
                response_log_file.write(json.dumps(json_result, indent=4, ensure_ascii=False))
                response_log_file.write('\n\n\n')

        return json_result

    @staticmethod
    def _get_post_url(url_base: str, function: str) -> str:
        """
        Generates an URL for a REST-POST request
        @params: The necessary parameters for a REST URL
        @return: A formatted URL
        """
        return '%swebservice/rest/server.php?moodlewsrestformat=json&wsfunction=%s' % (url_base, function)

    @staticmethod
    def _get_post_data(function: str, token: str, data_obj: str) -> str:
        """
        Generates the data for a REST-POST request
        @params: The necessary parameters for a REST URL
        @return: A URL-encoded data string
        """
        data = {'moodlewssettingfilter': 'true', 'moodlewssettingfileurl': 'true'}

        if data_obj is not None:
            data.update(data_obj)

        data.update({'wsfunction': function, 'wstoken': token})

        return RequestClient.recursive_url_encode(data)

    @staticmethod
    def recursive_url_encode(data):
        """URL-encode a multidimensional dictionary.
        @param data: the data to be encoded
        @returns: the url encoded data
        """

        def recursion(data_list, base=None):
            if base is None:
                base = []
            pairs = []

            for key, value in data_list.items():
                new_base = base + [key]
                if hasattr(value, 'values'):
                    pairs += recursion(value, new_base)
                else:
                    if len(new_base) > 1:
                        first = urllib.parse.quote(new_base.pop(0))
                        rest = map(lambda x: urllib.parse.quote(x), new_base)
                        new_pair = '%s[%s]=%s' % (first, ']['.join(rest), urllib.parse.quote(str(value)))
                    else:
                        new_pair = '%s=%s' % (urllib.parse.quote(str(key)), urllib.parse.quote(str(value)))

                    pairs.append(new_pair)
            return pairs

        return '&'.join(recursion(data))

    @staticmethod
    def _check_response_code(response):
        # Normally Moodle answer with response 200
        if response.status_code != 200:
            raise RuntimeError(
                'An Unexpected Error happened on side of the Moodle System!'
                + (' Status-Code: %s' % str(response.status_code))
                + ('\nHeader: %s' % response.headers)
                + ('\nResponse: %s' % response.text)
            )

    def _initial_parse(self, response) -> object:
        """
        The first time parsing the result of a REST request.
        It is checked for known errors.
        @param response: The JSON response of the Moodle system
        @return: The parsed JSON object
        """

        self._check_response_code(response)

        # Try to parse the JSON
        try:
            response_extracted = response.json()
        except Exception as error:
            raise RuntimeError(
                'An Unexpected Error occurred while trying'
                + ' to parse the json response! Moodle'
                + ' response: %s.\nError: %s' % (response, error)
            )
        # Check for known errors
        if 'error' in response_extracted:
            error = response_extracted.get('error', '')
            errorcode = response_extracted.get('errorcode', '')
            stacktrace = response_extracted.get('stacktrace', '')
            debuginfo = response_extracted.get('debuginfo', '')
            reproductionlink = response_extracted.get('reproductionlink', '')

            raise RequestRejectedError(
                'The Moodle System rejected the Request.'
                + (' Details: %s (Errorcode: %s, ' % (error, errorcode))
                + ('Stacktrace: %s, Debuginfo: %s, Reproductionlink: %s)' % (stacktrace, debuginfo, reproductionlink))
            )

        if 'exception' in response_extracted:
            exception = response_extracted.get('exception', '')
            errorcode = response_extracted.get('errorcode', '')
            message = response_extracted.get('message', '')

            raise RequestRejectedError(
                'The Moodle System rejected the Request.'
                + ' Details: %s (Errorcode: %s, Message: %s)' % (exception, errorcode, message)
            )

        return response_extracted


class RequestRejectedError(Exception):
    """An Exception which gets thrown if the Moodle-System answered with an
    Error to our Request"""

    pass
