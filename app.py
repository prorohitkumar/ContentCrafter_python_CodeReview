from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import json

import logging

# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

CORS(app)

# Initializing the App and Gemini API
working_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open(config_file_path))
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]


class CodeReviewer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + self.api_key

    def generate_review(self, code, description):
        try:
            headers = {'Content-Type': 'application/json'}

            if description == "Fix issues of my code":
                logging.info(f"Fix issue of the code:",{code})
                prompt = (
                    f"Act as a code reviewer. Your responsibility is to read the provided code:\n{code} \n and check "
                    f"for any code related issues. First find out in which language the code is provided,"
                    f"then according to the language of code, you should look for the following, and be extremely "
                    f"vigilant:\n- Syntax errors\n- Logic errors\n- Security vulnerabilities\n- Performance "
                    f"issues\n- Anything else that looks wrong\n\nOnce you find an error, please explain it as "
                    f"clearly as possible along with error name and exact line number of the provided code."
                    f"\nFollow it up with an explanation of the "
                    f"error\nNext, you should provide the corrected code and explain the changes made in the "
                    f"corrected code.\nUse the same format per issue found.If there is no issue in the provided "
                    f"code, response with the message 'The code does not have any error' and don't provide any extra "
                    f"information. If provided code is not related to any coding language, response with the message "
                    f"'Please provide code for reviewing.'")
            elif description == "Optimize my code":
                logging.info(f"Optimizing the code:",{code})
                prompt = (f"Act as a code reviewer. Your responsibility is to read the provided code:\n{code} \n and "
                          "check for any code optimization and best practices of coding. First find out in which "
                          "language the code is provided,"
                          "then according to the language of code, you should look for the optimization and best "
                          "practices of coding after checking of any code related issues. If any error is exist in "
                          "the provided code,"
                          "first solve it after then you should look for the optimization and best practices of "
                          "making code testable."
                          "Once you find an any optimization and best practices of coding in provided code, "
                          "please explain both things,"
                          "What have you changed in code to make it correct and optimized as clearly as possible. "
                          "Next, you should provide the refactored code and explain the changes made in the refactored "
                          "code. If there is no possibility of optimization in the provided code, response with the "
                          "message 'Your code is already optimized' and don't provide any extra information. If "
                          "provided code is not related to any coding language, response with the message 'Please "
                          "provide code for Optimization.'")
            else:
                logging.info(f"Fix the issue if and document the same:",{code})
                prompt = (
                    "Act as a code reviewer.Your responsibility is to read the provided code and Document the "
                    f"code:\n{code}\n."
                    f"If the given code contains any code related issues then solve it."
                    f"Make sure that, the code is documented with the help of comments only.Once you document the "
                    f"code, You should provide the documented code."
                    f"If provided code is not related to any coding language, response with the message 'This "
                    f"code is not valid and therefore cannot be documented.'"

                )

            print(prompt)

            generation_config = {
                'temperature': 0.9,
                'topK': 1,
                'topP': 1,
                'maxOutputTokens': 2048,
                'stopSequences': []
            }

            request_body = {
                'contents': [{'parts': [{'text': prompt}]}],
                'generationConfig': generation_config
            }

            response = requests.post(self.base_url, json=request_body, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            generated_review = [candidate['content']['parts'][0]['text'] for candidate in response_data['candidates']]
            return generated_review

        except Exception as e:
            print("Service Exception:", str(e))
            logging.error(f"Service exception caused while generating response",str(e))
            raise Exception("Error in getting response from Gemini API")

@app.route('/', methods=['GET'])
def hello_world():
    logging.info(f"Testing end points")
    return "Hii"

@app.route('/review_code', methods=['POST'])
def review_code():
    request_data = request.json
    code = request_data.get('code')
    description = request_data.get('description')

    print(code)
    # api_key = "AIzaSyCYutjs2BzQThKnA2q1hDNbZro4Al7N0Dw"
    reviewer = CodeReviewer(api_key=GOOGLE_API_KEY)
    review = reviewer.generate_review(code, description)

    for i, question in enumerate(review, start=1):
        print(f" Review {i}: {question}")

    return jsonify({"review": review})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
