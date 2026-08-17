from abc import ABC, abstractmethod

class AIProvider(ABC):
    """
    Classe abstraite : interface commune aux différents fournisseurs d'IA.
    Tous les fournisseurs (Google, Ollama, OpenRouter, Groq) hériteront de cette classe.
    """

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Génère du texte à partir d'un prompt donné."""
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """Retourne les informations sur le fournisseur et le modèle utilisé."""
        pass