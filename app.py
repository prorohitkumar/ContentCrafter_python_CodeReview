from flask import Flask, jsonify, request, send_file
import requests
import json
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# Initializing the App and Gemini API
working_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open(config_file_path))
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]


class RolePlayCreator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="
            + self.api_key
        )


rolePlayCreator_service = RolePlayCreator(api_key=GOOGLE_API_KEY)


# Define a route for user story generation


# @app.route("/generate-user-story", methods=["POST"])
# def generate_user_story():
#     # Extract request data
#     data = request.get_json()

#     # Extract required fields from request body
#     application_type = data.get("application_type")
#     feature = data.get("feature")
#     feature_for = data.get("feature_for")
#     user_role = data.get("user_role")

#     print(feature)

#     # Constructing the prompt
#     promptt = (
#         f"List all possible user stories for a {application_type} product {feature} feature for {feature_for} development used by {user_role}. "
#         "Each user story should be accompanied by criteria that define when the story is considered complete, including both functional and non-functional requirements.\n"
#         "Return your response in an array of JSON objects. Each object will have 'userStory' key.\n"
#         "Below is the example structure that you should return your response: \n"
#         """[
#               {{
#                 "userStory": "As a product administrator, I want to able to verify if a
#                  user has registered a specific product using a guest user account, so that I can provide support
#                  if needed",
#               }},
#               {{
#                 "userStory": "As a product administrator, I want to able to view the registration details of a specific product registered by a guest user,
#                   so that I can track warranty information and usage history",
#               }}
#             ]"""
#     )

#     try:
#         headers = {"Content-Type": "application/json"}
#         generation_config = {
#             "temperature": 1.0,
#             "topK": 1,
#             "topP": 1,
#             "maxOutputTokens": 2048,
#             "stopSequences": [],
#         }

#         request_body = {
#             "contents": [{"parts": [{"text": promptt}]}],
#             "generationConfig": generation_config,
#         }

#         response = requests.post(
#             rolePlayCreator_service.base_url, json=request_body, headers=headers
#         )
#         response.raise_for_status()
#         response_data = response.json()
#         rolePlayExercise = [
#             candidate["content"]["parts"][0]["text"]
#             for candidate in response_data["candidates"]
#         ]
#         print(rolePlayExercise)
#         generated_questions = []
#         for candidate in response_data["candidates"]:
#             question_answer_pairs = json.loads(candidate["content"]["parts"][0]["text"])
#             for pair in question_answer_pairs:
#                 generated_questions.append(
#                     {
#                         "user story": pair["userStory"],
#                     }
#                 )

#         print("\n\n\n\n", generated_questions)

#         return jsonify(generated_questions)

#     except Exception as e:
#         print("Service Exception:", str(e))
#         raise Exception("Error in getting response from Gemini API")

#     # return jsonify({'user_story': user_story})


@app.route("/generate-user-story", methods=["POST"])
def generate_user_story():
    # Extract request data
    data = request.get_json()

    # Extract required fields from request body
    application_type = data.get("application_type")
    feature = data.get("feature")
    feature_for = data.get("feature_for")
    user_role = data.get("user_role", "")

    # Constructing the prompt dynamically based on presence of user_role
    if user_role:
        promptt = (
            f"List all possible user stories for a {application_type} product {feature} feature for {feature_for} development used by {user_role}. "
            "Each user story should be accompanied by criteria that define when the story is considered complete, including both functional and non-functional requirements.\n"
            "Return your response in an array of JSON objects. Each object will have 'userStory' key.\n"
            "Below is the example structure that you should return your response: \n"
            """[
                  {{
                    "userStory": "As a product administrator, I want to able to verify if a
                     user has registered a specific product using a guest user account, so that I can provide support
                     if needed",
                  }},
                  {{
                    "userStory": "As a product administrator, I want to able to view the registration details of a specific product registered by a guest user,
                      so that I can track warranty information and usage history",
                  }}
                ]"""
        )
    else:
        promptt = (
            f"List all possible user stories for a {application_type} product {feature} feature for {feature_for} development. "
            "Each user story should be accompanied by criteria that define when the story is considered complete, including both functional and non-functional requirements.\n"
            "Return your response in an array of JSON objects. Each object will have 'userStory' key.\n"
            "Below is the example structure that you should return your response: \n"
            """[
                  {{
                    "userStory": "As a product administrator, I want to able to verify if a
                     user has registered a specific product using a guest user account, so that I can provide support
                     if needed",
                  }},
                  {{
                    "userStory": "As a product administrator, I want to able to view the registration details of a specific product registered by a guest user,
                      so that I can track warranty information and usage history",
                  }}
                ]"""
        )

    try:
        headers = {"Content-Type": "application/json"}
        generation_config = {
            "temperature": 1.0,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 2048,
            "stopSequences": [],
        }

        request_body = {
            "contents": [{"parts": [{"text": promptt}]}],
            "generationConfig": generation_config,
        }

        response = requests.post(
            rolePlayCreator_service.base_url, json=request_body, headers=headers
        )
        response.raise_for_status()
        response_data = response.json()

        generated_questions = []
        for candidate in response_data["candidates"]:
            question_answer_pairs = json.loads(candidate["content"]["parts"][0]["text"])
            for pair in question_answer_pairs:
                generated_questions.append(
                    {
                        "user story": pair["userStory"],
                    }
                )

        return jsonify(generated_questions)

    except Exception as e:
        print("Service Exception:", str(e))
        raise Exception("Error in getting response from Gemini API")

    # return jsonify({'user_story': user_story})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
