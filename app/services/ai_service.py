import os
from openai import OpenAI
from config import Config


class AIServiceError(Exception):
    """Yapay zeka servisinde bir sorun olduğunda fırlatılır."""
    pass


class AIService:

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "openai/gpt-oss-20b"

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        else:
            self.client = None

    def _sistem_talimati(self):
        """config.py'deki BUSINESS_CONTEXT'i okur."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanıcı mesajını Groq üzerinden GPT-OSS modeline gönderir.

        gecmis:
        [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
        """

        if not self.api_key or self.client is None:
            return (
                "Demo modu: Şu an yapay zeka bağlantısı aktif değil. "
                "(GROQ_API_KEY tanımlı değil)"
            )

        if gecmis is None:
            gecmis = []

        # Sistem talimatı + konuşma geçmişi + yeni kullanıcı mesajı
        input_mesajlari = [
            {
                "role": "system",
                "content": self._sistem_talimati()
            }
        ]

        input_mesajlari.extend(gecmis)

        input_mesajlari.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        try:
            response = self.client.responses.create(
                model=self.model,
                input=input_mesajlari
            )

            return response.output_text

        except Exception as e:
            raise AIServiceError(
                f"Yapay zeka servisinde hata oluştu: {str(e)}"
            )


# Dosya sonunda tek bir örnek
ai_service = AIService()


# Dosya sonunda tek bir ornek
ai_service = AIService()
