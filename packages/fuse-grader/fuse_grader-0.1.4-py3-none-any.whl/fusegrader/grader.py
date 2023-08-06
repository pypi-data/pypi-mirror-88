import json
import sys

import numpy as np
import requests


# source: https://github.com/mpld3/mpld3/issues/434#issuecomment-340255689
# fix for the NumPy array is not JSON serializable
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj: object) -> None:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Grader:
    """Student side grader class
    ...

    Attributes
    ----------
    submission_url : str
        API url to fetch data

    assignmentKey : str
        test-case filename

    details : dict
        Contains data to be validated with test case functions


    Methods
    -------
    add_details(variable_key_vale)
        Saves assignemnt result on the details variable

    submit("email","token")
        Send email and session token along with
        student assignment result in parts variableW
        and filename of test case in assignmentKey variable
    """

    def __init__(self, assignmentKey: str, submission_url: str) -> None:
        self.submission_url = submission_url
        self.assignmentKey = assignmentKey
        self.details: dict = {}

    def add_details(self, variable_key_vale: dict) -> None:
        assert isinstance(variable_key_vale, dict)
        key_of_function = list(variable_key_vale.keys())[0]
        key_of_function_val = list(variable_key_vale.values())[0]
        assert key_of_function_val is not None
        assert isinstance(key_of_function, str)
        try:
            self.details[key_of_function] = key_of_function_val
        except Exception:
            print("Invalid function name value passed")

    def submit(self, email: str, token: str) -> dict:
        submission = {
            "assignmentKey": self.assignmentKey,
            "student_email": email,
            "secret": token,
            "parts": [self.details],
        }
        try:
            request = requests.post(
                self.submission_url,
                data=json.dumps(submission, cls=NumpyEncoder),
                headers={"content-type": "application/json"},
            )

            # get response form api
            response = request.json()
            return response["data"]

        except Exception:
            return {"err": "No live server found!"}
