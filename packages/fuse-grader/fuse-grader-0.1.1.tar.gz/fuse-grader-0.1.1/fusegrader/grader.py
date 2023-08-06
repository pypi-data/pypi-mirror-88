import requests
import json
import numpy as np

# source: https://github.com/mpld3/mpld3/issues/434#issuecomment-340255689
# fix for the NumPy array is not JSON serializable
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Grader:
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    submission_page : str
        API url to fetch data
    assignment_key : str
        test-case filename
    details : dict
        Contains data to be validated with test case functions


    Methods
    -------
    add_details(variable_key_vale)
        Saves assignemnt result on the details variable
    submit("email","token")
        Send email and session token along with
        student assignment result in parts variable
        and filename of test case in assignment_key variable
    """

    def __init__(self, assignment_key, submission_url):
        self.submission_page = submission_url
        self.assignment_key = assignment_key
        self.details = {}

    def add_details(self, variable_key_vale):
        assert isinstance(variable_key_vale, dict)
        key_of_function = list(variable_key_vale.keys())[0]
        key_of_function_val = list(variable_key_vale.values())[0]
        assert key_of_function_val is not None
        assert isinstance(key_of_function, str)
        try:
            self.details[key_of_function] = key_of_function_val
        except:
            print("Invalid function name value passed")

    def submit(self, email, token):
        submission = {
            "assignmentKey": self.assignment_key,
            "submitterEmail": email,
            "secret": token,
            "parts": [self.details],
        }
        try:
            request = requests.post(
                self.submission_page, data=json.dumps(submission, cls=NumpyEncoder)
            )
            ## get response form api
            response = request.json()
            if request.status_code == 200:
                print("Status Code: ", request.status_code)
                print(response)
            else:
                print(response)
        except:
            print("NO live Server found")
