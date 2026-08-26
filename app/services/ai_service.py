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
        """config.py içerisindeki Nerys marka bilgisini alır."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanıcı mesajını Groq API üzerinden GPT-OSS modeline gönderir
        ve Nerys marka asistanının yanıtını döndürür.

        gecmis:
        [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
        formatında önceki konuşma mesajlarını içerir.
        """

        # API anahtarı yoksa demo mesajı göster
        if not self.api_key or self.client is None:
            return (
                "Demo modu: Şu an yapay zeka bağlantısı aktif değil. "
                "(GROQ_API_KEY tanımlı değil)"
            )

        # Konuşma geçmişi gönderilmediyse boş liste oluştur
        if gecmis is None:
            gecmis = []

        # Sistem mesajı + geçmiş konuşmalar + yeni kullanıcı mesajı
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
            # Groq'un OpenAI uyumlu Responses API'si
            response = self.client.responses.create(
                model=self.model,
                input=input_mesajlari
            )

            # Modelin oluşturduğu metin yanıtını döndür
            return response.output_text

        except Exception as e:
            raise AIServiceError(
                f"Yapay zeka servisinde hata oluştu: {str(e)}"
            )


# Uygulama içerisinde kullanılacak tek AIService örneği
ai_service = AIService()
