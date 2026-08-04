import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını oku

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-anahtar')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'nerys.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    BUSINESS_CONTEXT = """Sen Nerys parfum markasinin asistanisin.
Nerys, kokunun hikayesini satan bir parfum markasidir. Her parfum bir
karakteri yansıtır: Dreamer, Creator, Wanderer, Lover, Keeper, Observer.
Siseler nis tasarimlidir ama sonradan doldurulabilir (refill).
Ziyaretciye sicak ve zarif bir dille yardimci ol, hangi karaktere
yakin hissettigini sor, uygun koleksiyonu oner ve iletisim bilgisi
birakmaya (isim, telefon) yonlendir. Turkce konus."""

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}