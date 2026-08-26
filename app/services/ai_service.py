from groq import Groq
from config import Config


class AIServiceError(Exception):
    """Yapay zeka servisinde bir sorun oldugunda firlatilir."""
    pass


class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "openai/gpt-oss-120b"

    if self.api_key:
        self.client= Groq(api_key=self.api_key)
    else:
        self.client=None

    def _sistem_talimati(self):
        """config.py'deki BUSINESS_CONTEXT'i okur."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanici mesajini Groq'a gonderir, yaniti dondurur.
        gecmis: [{"role": "user"/"assistant", "content": "..."}] formatinda gecmis mesajlar (opsiyonel).
        """

        if not self.api_key:
            return "Demo modu: Su an yapay zeka baglantisi aktif degil. (GROQ_API_KEY tanimli degil)"

        if gecmis is None:
            gecmis = []

        mesajlar = [
            {"role": "system", "content": self._sistem_talimati()}
        ] + gecmis + [
            {"role": "user", "content": mesaj}
        ]

        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": mesajlar
                },
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Yapay zeka servisine ulasilamadi: {str(e)}")
        except (KeyError, IndexError) as e:
            raise AIServiceError(f"Yapay zeka yaniti beklenmeyen formatta: {str(e)}")


# Dosya sonunda tek bir ornek
ai_service = AIService()
