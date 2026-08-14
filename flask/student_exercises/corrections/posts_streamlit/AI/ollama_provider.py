import ollama

from .aiprovider import AIProvider

class OllamaProvider(AIProvider):
    def __init__(
        self,
        model_name: str = "llama3.1:8b",
        host: str = "http://host.docker.internal:11434",
    ):
        self.model_name = model_name
        self.client = ollama.Client(host=host)

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
            )
            return response["response"]
        except Exception as e:
            return f"Erreur lors de la génération : {str(e)}"

    def get_model_info(self) -> dict:
        return {
            "provider": "Ollama",
            "model": self.model_name,
            "type": "Ollama sur le serveur hôte",
            "host": self.client._client.base_url,
        }

    def list_local_models(self) -> list:
        """Liste les modèles disponibles sur l'Ollama du serveur hôte."""
        try:
            response = self.client.list()
            return [m["model"] for m in response["models"]]
        except Exception:
            return []