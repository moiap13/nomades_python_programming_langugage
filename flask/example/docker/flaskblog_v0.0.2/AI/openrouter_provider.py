from openai import OpenAI

from .aiprovider import AIProvider

class OpenRouterProvider(AIProvider):
    def __init__(self, api_key: str, model_name: str = "openrouter/free"):
        self.api_key = api_key
        self.model_name = model_name
        # OpenRouter utilise une API compatible OpenAI
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    def generate_text(self, prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Erreur lors de la génération : {str(e)}"

    def get_model_info(self) -> dict:
        return {
            "provider": "OpenRouter",
            "model": self.model_name,
            "type": "Cloud (Free tier)"
        }