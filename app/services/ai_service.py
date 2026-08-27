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

    def yanit_uret(self, mesaj, gecmis=None):

        if not self.api_key or self.client is None:
            return "Şu anda yapay zeka bağlantım aktif değil."

        if gecmis is None:
            gecmis = []

        try:

            # Önceki konuşmaları hazırla
            input_mesajlari = []

            for mesaj_item in gecmis:
                input_mesajlari.append({
                    "role": mesaj_item["role"],
                    "content": mesaj_item["content"]
                })

            # Yeni kullanıcı mesajı
            input_mesajlari.append({
                "role": "user",
                "content": mesaj
            })
            
            response = self.client.responses.create(
                model=self.model,

                # MARKA TALİMATI BURADA
                instructions=Config.BUSINESS_CONTEXT,

                # KULLANICI MESAJLARI BURADA
                input=input_mesajlari,

                reasoning={
                    "effort": "low"
                }
            )

            return response.output_text.strip()

        except Exception as e:
            raise AIServiceError(
                f"Yapay zeka servisinde hata oluştu: {str(e)}"
            )


ai_service = AIService()