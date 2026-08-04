from flask import Blueprint, request, jsonify, render_template
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

# Iki blueprint: biri sayfalar icin, biri API icin
pages_bp = Blueprint('pages', __name__)
api_bp = Blueprint('api', __name__)


# ---- Sayfa rotalari ----

@pages_bp.route('/')
def anasayfa():
    return render_template('index.html')


@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ---- API rotalari ----

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    data = request.get_json()

    if not data or 'mesaj' not in data:
        return jsonify({"basari": False, "hata": "Mesaj alani zorunlu"}), 400

    try:
        cevap = ai_service.yanit_uret(data['mesaj'], data.get('gecmis'))
        return jsonify({"basari": True, "cevap": cevap}), 200

    except AIServiceError as e:
        return jsonify({"basari": False, "hata": str(e)}), 503


@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    data = request.get_json()

    if not data or 'isim' not in data or 'telefon' not in data:
        return jsonify({"basari": False, "hata": "Isim ve telefon zorunlu"}), 400

    lead_ekle(
        isim=data['isim'],
        telefon=data['telefon'],
        mesaj=data.get('mesaj'),
        koleksiyon=data.get('koleksiyon')
    )
    return jsonify({"basari": True}), 201


@api_bp.route('/leads', methods=['GET'])
def leadleri_getir():
    return jsonify({"basari": True, "leadler": tum_leadler()}), 200