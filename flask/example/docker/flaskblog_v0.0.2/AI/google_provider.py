from google import genai

from .aiprovider import AIProvider

class GoogleAIProvider(AIProvider):
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Erreur lors de la génération : {str(e)}"

    def get_model_info(self) -> dict:
        return {
            "provider": "Google Generative AI",
            "model": self.model_name,
            "type": "Cloud (Free tier)"
        }

    @staticmethod
    def list_available_models(api_key: str) -> list:
        """Liste les modèles Gemini disponibles pour la clé API."""
        try:
            client = genai.Client(api_key=api_key)
            return [m.name for m in client.models.list()]
        except Exception as e:
            return [f"Erreur : {e}"]