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
        return self._sistem_talimati_metni()

    def _sistem_talimati_metni(self):
        temel_metin = current_app.config['BUSINESS_CONTEXT']
        turkce_hatirlatma = (
            "\n\nÇOK ÖNEMLİ: Yanıtını KESİNLİKLE ve SADECE Türkçe ver. "
            "İngilizce tek kelime bile kullanma."
        )
        return temel_metin + turkce_hatirlatma

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

            for oge in data.get("output", []):
                if oge.get("type") == "message":
                    for icerik in oge.get("content", []):
                        if icerik.get("type") == "output_text":
                            return icerik.get("text", "")

            raise AIServiceError("Yapay zekâ yanıtı beklenmeyen formatta.")

        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Yapay zekâ servisine ulaşılamadı: {str(e)}")
        except (KeyError, IndexError) as e:
            raise AIServiceError(f"Yapay zekâ yanıtı beklenmeyen formatta: {str(e)}")


# Dosya sonunda tek bir örnek
ai_service = AIService()