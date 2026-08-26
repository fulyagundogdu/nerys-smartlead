import requests
from flask import current_app


class AIServiceError(Exception):
    """Yapay zekâ servisinde bir sorun olduğunda fırlatılır."""
    pass


class AIService:
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/responses"
        self.model = "openai/gpt-oss-20b"

    def _sistem_talimati(self):
        """config.py'deki BUSINESS_CONTEXT'i okur."""
        return current_app.config['BUSINESS_CONTEXT']

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanıcı mesajını Groq'a gönderir, yanıtı döndürür.
        """
        api_key = current_app.config['GROQ_API_KEY']

        if not api_key:
            return "Demo modu: Şu an yapay zekâ bağlantısı aktif değil. (GROQ_API_KEY tanımlı değil)"

        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "instructions": self._sistem_talimati(),
                    "input": mesaj
                },
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            return data["output"][0]["content"][0]["text"]

        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Yapay zekâ servisine ulaşılamadı: {str(e)}")
        except (KeyError, IndexError) as e:
            raise AIServiceError(f"Yapay zekâ yanıtı beklenmeyen formatta: {str(e)}")


# Dosya sonunda tek bir örnek
<<<<<<< HEAD
ai_service = AIService()
=======
ai_service = AIService()
>>>>>>> f122c8745ab048fdba590f647240a71bb603b8b0
