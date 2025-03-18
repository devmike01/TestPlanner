import json
import os

from google import genai
from google.genai.types import GenerateContentResponse

from secrets import Secrets


class GeminiPrompts:
    test_maker = """
You are an expert in analyzing Django views and generating structured test plans. Your task is to examine the conditions, validations, and business logic in the given Django views and use them to create a comprehensive test plan.

given: {views}

1. Identify all conditional checks, error handling, and validation logic present in the Django view functions or class-based views.
2. Map each check to a **test case** specifying:
   - The field being validated (e.g., email, password, username).
   - The possible valid and invalid inputs.
   - The expected outputs for each case.
3. Structure the test plan using the following JSON format:

{schema}

Generate the test plan in JSON format, ensuring **all edge cases** are covered based on the Django view logic.

    """


# .strip('json')
def ai_json(data):
    return json.loads(json.dumps(json.loads(data.replace('```', '').replace('json', '').strip()), indent=2))


class AjalaAi:

    def __init__(self):
        self.client = genai.Client(api_key=Secrets.GEMINI_KEY)

    def _using_model(self, contents: str):
        return self.client.models.generate_content(
            model="gemini-2.0-flash", contents=contents
        )

    def _schema(self, json_path: str = "schema.json"):  # /Users/admin/PycharmProjects/testmaker/schema.json
        # remove {os.getcwd()}/utils/ to test locally
        with open(f'{os.getcwd()}/{json_path}') as f:
            d = json.load(f)
            return json.dumps(d)

    def write_test_sheet(self, views: str):
        return ai_json(self._using_model(GeminiPrompts
                                         .test_maker.format(views=views,
                                                            schema=self._schema('schema.json'))).text)
