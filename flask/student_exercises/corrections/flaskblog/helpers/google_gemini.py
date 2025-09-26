from google import genai
from google.genai import types


class GeminiAssistantService:
    """
    Service module for handling Gemini API interactions.
    """

    def __init__(
        self, api_key: str, sys_prompt: str = None, model_name: str = "gemini-2.5-flash"
    ):
        self.model_name = model_name
        self.sys_prompt = sys_prompt or ""
        self.client = genai.Client(api_key=api_key)

    def basic_chat(self, prompt: str, temperature: float = 0.1) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=self.sys_prompt,
                temperature=temperature,
            ),
            contents=prompt,
        )
        return response.text

    def model_info(self) -> str:
        model = self.client.models.get(model=self.model_name)
        return f"Model name: {model.name}, Description: {model.description}"
