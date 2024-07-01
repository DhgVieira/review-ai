# Apache License
# Version 2.0, January 2004
# Author: Eugene Tkachenko

import os
from openai import OpenAI
from ai.ai_bot import AiBot
import requests


class ChatGPT(AiBot):

    def __init__(self, token, model):
        self.__chat_gpt_model = model
        self.__client = OpenAI(api_key=token)

    def ai_request_diffs(self, code, diffs):
        stream = self.__client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": AiBot.build_ask_text(code=code, diffs=diffs),
                }
            ],
            model=self.__chat_gpt_model,
            stream=True,
        )
        content = []
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content.append(chunk.choices[0].delta.content)
        return " ".join(content)

    def request_to_generative(self, code, diffs):

        headers = {
            "Content-Type": "application/json",
            "cookie": "_hjSessionUser_3270469=eyJpZCI6IjY0NzQxNmEyLTcxYWUtNTQ3ZC1iOTU4LTQwNDBjZTllNWNjZiIsImNyZWF0ZWQiOjE3MTUwMDUzMjMyNTksImV4aXN0aW5nIjp0cnVlfQ==; GCP_IAP_UID=117266882697102200152; _hjSessionUser_1373410=eyJpZCI6ImZkYTc1ODJhLWNiNGMtNWYwZC1iZGJmLWU4MDI2M2FhZDE0ZCIsImNyZWF0ZWQiOjE3MTUwMTM3MTA4NzUsImV4aXN0aW5nIjp0cnVlfQ==; _hjDonePolls=1018484; _ga_49RZ1MSG13=GS1.2.1716405944.2.0.1716405944.0.0.0; _hjSessionUser_1668499=eyJpZCI6IjQxMTA1NmI2LWMwYmUtNWY5OC04NDUyLWFiY2VjZDQ2ZmFhNiIsImNyZWF0ZWQiOjE3MTY5MjMzODQzMDgsImV4aXN0aW5nIjp0cnVlfQ==; _csrf=4rn3K3dk9suS-LQwD7gSSBar; _clck=r6w82y%7C2%7Cfmq%7C0%7C1589; _hjSessionUser_783944=eyJpZCI6IjUxNTJmN2ViLTg0MzktNWI0Ny05YTA2LWNmYTI5OWEzZTIyNSIsImNyZWF0ZWQiOjE3MTg3NDA1MDkzODIsImV4aXN0aW5nIjp0cnVlfQ==; amp_7e504c=_mV4Wfl57dk4hqz70HIZEx.ZGl2aWVpcmE=..1i0mhgrk2.1i0mhi2ok.a3.0.a3; mp_ad031834cbd83ea4aa0a9633182023c2_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18f59b4d136ea6-0e926947a445cd-1b525637-16a7f0-18f59b4d136ea6%22%2C%22%24device_id%22%3A%20%2218f59b4d136ea6-0e926947a445cd-1b525637-16a7f0-18f59b4d136ea6%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%22%24os%22%3A%20%22Mac%20OS%20X%22%2C%22%24browser%22%3A%20%22Chrome%22%2C%22%24browser_version%22%3A%20125%2C%22User%20Logged%22%3A%20%22divieira%22%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; _ga=GA1.1.1631103844.1715196973; _hjShownFeedbackMessage=true; _hjSessionUser_3383051=eyJpZCI6ImRhOTk1MDdhLTM3M2MtNWQ5Ni1iZWM4LWQ0MDEzYjAzNjFiNCIsImNyZWF0ZWQiOjE3MTk1MTg5NjUwNjQsImV4aXN0aW5nIjp0cnVlfQ==; session_id=divieira-b8eab209-356f-4182-958e-50397ecaf5dc; user_activity_last_session=3_hours; _hjSession_3383051=eyJpZCI6IjVkMDM2ODc4LTY3YWYtNDgyYy1hNDc5LWQyNTA3ZjE4ZjdkZiIsImMiOjE3MTk1OTYxMjM2MzksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ga_Z13X7Z78XM=GS1.1.1719596124.5.1.1719597587.0.0.0",
            "x-fury-user": "divieira",
            "x-csrf-token": "EhhwhpOx-_EVfCdtnjMz_swE2efvJwMaLnYI"
        }

        messages = [
            {
                "role": "user",
                "content": AiBot.build_ask_text(code=code, diffs=diffs),
            }
        ]
        body = {
            "messages": messages,
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 3000,

        }

        response = requests.post("https://generative-ai.adminml.com/api/genai/openai/chat", json=body, headers=headers)
        json_response = []
        if response.status_code == 200 or response.status_code == 201:
            json_response = response.json()

        content = []
        for chunk in json_response['messages']:
            if chunk['content']:
                content.append(chunk['content'])
        return " ".join(content)
