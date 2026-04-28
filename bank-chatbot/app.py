"""Wifak Bank — Internal Assistant (Rule-based)

English-first application with an optional language selector (EN/FR/AR).

Run:
  pip install -r requirements.txt
  python app.py

Then open:
  http://127.0.0.1:5000

This app is intentionally simple: no database, no external AI APIs.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Tuple

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)  # templates/ and static/ are alongside this file


SUPPORTED_LANGS = {"en", "fr", "ar"}


def _now_str() -> str:
    """Human-friendly timestamp (24h)."""

    return datetime.now().strftime("%H:%M")


def _normalize(text: str) -> str:
    """Normalize user input for regex matching."""

    return (text or "").strip().lower()


def _pick(lang: str, en: str, fr: str | None = None, ar: str | None = None) -> str:
    """Pick a localized string; defaults to English."""

    if lang == "fr" and fr:
        return fr
    if lang == "ar" and ar:
        return ar
    return en


def generate_response(message: str, lang: str = "en") -> Tuple[str, str]:
    """Rule-based chatbot (regex + if/elif).

    Returns:
      (response_text, category)

    Formatting conventions used by the frontend:
      - **bold** will be rendered as <strong>
      - Lines starting with • or - are rendered as list items
    """

    lang = (lang or "en").strip().lower()
    if lang not in SUPPORTED_LANGS:
        lang = "en"

    raw = (message or "").strip()
    msg = _normalize(raw)

    if not raw:
        return (
            _pick(
                lang,
                "I didn't receive a message. Please type your question.\n"
                "• Example: **How do I request annual leave?**\n"
                "• Example: **How do I reset my password?**",
                "Je n’ai pas reçu de message. Merci d’écrire votre question.\n"
                "• Exemple: **Comment demander un congé annuel ?**\n"
                "• Exemple: **Comment réinitialiser mon mot de passe ?**",
                "لم تصلني رسالة. من فضلك اكتب سؤالك.\n"
                "• مثال: **كيف أطلب إجازة سنوية؟**\n"
                "• مثال: **كيف أعيد تعيين كلمة المرور؟**",
            ),
            "input",
        )

    # 1) Greetings
    if re.search(r"\b(hi|hello|hey|bonjour|salut)\b", msg) or re.search(
        r"(salam|assalam|as-salam|السلام|مرحبا)", raw, re.IGNORECASE
    ):
        return (
            _pick(
                lang,
                "Hello and welcome to **Wifak Bank**. I'm your internal assistant.\n"
                "• Onboarding and first-day guidance\n"
                "• Leave policy and absences\n"
                "• IT support (VPN, email, password)\n"
                "• Payroll (payslips, salary transfers)\n"
                "• Compliance & KYC\n\n"
                "Ask your question, or choose a topic on the left.",
                "Bonjour et bienvenue chez **Wifak Bank**. Je suis votre assistant interne.\n"
                "• Onboarding et premier jour\n"
                "• Congés et absences\n"
                "• Support IT (VPN, email, mot de passe)\n"
                "• Paie (bulletins, virements)\n"
                "• Compliance & KYC\n\n"
                "Posez votre question ou choisissez un thème à gauche.",
                "مرحبًا بك في **بنك الوفاق**. أنا مساعدك الداخلي.\n"
                "• الاندماج الوظيفي واليوم الأول\n"
                "• الإجازات والغيابات\n"
                "• دعم تقنية المعلومات (VPN، البريد، كلمة المرور)\n"
                "• الرواتب (كشوفات وتحويلات)\n"
                "• الامتثال و KYC\n\n"
                "اطرح سؤالك أو اختر موضوعًا من القائمة.",
            ),
            "greetings",
        )

    # 2) Onboarding
    if re.search(
        r"\b(onboarding|orientation|first\s*day|badge|access|it\s*setup|setup|welcome|new\s*joiner)\b",
        msg,
    ):
        return (
            _pick(
                lang,
                "**Onboarding checklist (Day 1 → Week 1)**:\n"
                "• **Badge & access**: collect your badge and confirm physical access (site, floor, office).\n"
                "• **IT setup**: email account, VPN, intranet access, MFA/Authenticator, Teams/Outlook.\n"
                "• **Equipment**: laptop, charger, peripherals; verify encryption and security baseline.\n"
                "• **Orientation**: meet your team, understand org structure, key contacts (HR, IT, Compliance).\n"
                "• **Security**: password policy, data classification, clean-desk guidance.\n\n"
                "Tell me your department (e.g., branch, HQ, IT) and I'll tailor the checklist.",
                "**Checklist onboarding (jour 1 → semaine 1)**:\n"
                "• **Badge & accès**: récupérer le badge et vérifier les accès physiques.\n"
                "• **IT setup**: email, VPN, intranet, MFA, Teams/Outlook.\n"
                "• **Matériel**: laptop et périphériques; vérifier le chiffrement et la sécurité.\n"
                "• **Orientation**: équipe, organigramme, contacts clés (RH, IT, Compliance).\n"
                "• **Sécurité**: politiques mots de passe, classification des données, clean desk.\n\n"
                "Indiquez votre service et j’adapte la checklist.",
                "**قائمة الاندماج (اليوم الأول → الأسبوع الأول)**:\n"
                "• **البطاقة والدخول**: استلام البطاقة وتأكيد صلاحيات الدخول.\n"
                "• **إعداد IT**: البريد، VPN، الإنترانت، MFA.\n"
                "• **المعدات**: الحاسوب والملحقات؛ التحقق من التشفير.\n"
                "• **التعريف**: لقاء الفريق وجهات الاتصال (HR/IT/Compliance).\n"
                "• **الأمن**: سياسة كلمة المرور وتصنيف البيانات.\n\n"
                "اذكر القسم لأخصص القائمة.",
            ),
            "onboarding",
        )

    # 3) Leave policy
    if re.search(r"\b(leave|vacation|holiday|sick|annual|absence|congé|conges|maladie)\b", msg):
        return (
            _pick(
                lang,
                "**Leave & absences (internal overview)**:\n"
                "• **Request**: submit via the HR tool (or your manager approval flow) with dates and details if required.\n"
                "• **Approval**: your manager validates based on planning and business continuity.\n"
                "• **Sick leave**: inform your manager promptly; provide documentation per HR policy.\n"
                "• **Balance**: check your remaining balance before confirming travel/commitments.\n"
                "• **Handover**: set an out-of-office message and delegate ownership if needed.\n\n"
                "Tell me the leave type (annual/sick/exceptional) and I'll guide the exact steps.",
                "**Congés & absences (résumé interne)**:\n"
                "• **Demande**: via outil RH (ou circuit manager) avec dates.\n"
                "• **Validation**: selon planning et continuité.\n"
                "• **Maladie**: informer rapidement + justificatif selon RH.\n"
                "• **Solde**: vérifier le solde avant confirmation.\n"
                "• **Passation**: message d’absence + délégation.\n\n"
                "Précisez le type de congé et je détaille la procédure.",
                "**الإجازات والغياب (ملخص)**:\n"
                "• **الطلب**: عبر نظام الموارد البشرية أو مسار المدير.\n"
                "• **الموافقة**: حسب التخطيط واستمرارية العمل.\n"
                "• **المرضية**: إخطار المدير وتقديم الوثائق حسب السياسة.\n"
                "• **الرصيد**: تحقق من الرصيد قبل التأكيد.\n"
                "• **التسليم**: رسالة خارج المكتب وتفويض المهام.\n\n"
                "اذكر نوع الإجازة لأعطيك الخطوات الدقيقة.",
            ),
            "leave",
        )

    # 4) IT Support
    if re.search(
        r"\b(it|support|helpdesk|password|vpn|email|mail|outlook|laptop|pc|login|mfa|authenticator|mot\s*de\s*passe|connexion)\b",
        msg,
    ):
        return (
            _pick(
                lang,
                "**IT Support — quick troubleshooting**:\n"
                "• **Password**: use self-service reset if enabled; otherwise open a Helpdesk ticket.\n"
                "• **VPN**: confirm internet, credentials, MFA; restart the VPN client; try another network.\n"
                "• **Email/Outlook**: check password/MFA, mailbox quota, profile; test webmail if available.\n"
                "• **Laptop issues**: reboot, updates, storage; for hardware incidents, ticket + asset tag.\n"
                "• **App access**: include the app name, exact error text, timestamp, and (if allowed) a screenshot.\n\n"
                "Share the exact error message and I'll guide you step-by-step.",
                "**Support IT — dépannage rapide**:\n"
                "• **Mot de passe**: SSPR si disponible, sinon ticket Helpdesk.\n"
                "• **VPN**: internet, identifiants, MFA; redémarrer le client; tester autre réseau.\n"
                "• **Email/Outlook**: quota, profil; tester webmail si disponible.\n"
                "• **Laptop**: redémarrage, mises à jour, stockage; incident matériel: ticket + asset tag.\n"
                "• **Accès appli**: nom appli, erreur exacte, heure, capture si autorisée.\n\n"
                "Donnez le message d’erreur exact et je vous guide.",
                "**دعم IT — خطوات سريعة**:\n"
                "• **كلمة المرور**: إعادة تعيين ذاتي إن توفر، وإلا تذكرة للدعم.\n"
                "• **VPN**: تحقق من الإنترنت وMFA ثم أعد تشغيل البرنامج.\n"
                "• **البريد**: تحقق من MFA والملف الشخصي والـquota.\n"
                "• **الحاسوب**: إعادة تشغيل وتحديثات؛ للأعطال: تذكرة + رقم الجهاز.\n\n"
                "أرسل نص الخطأ وسأرشدك خطوة بخطوة.",
            ),
            "it_support",
        )

    # 5) Payroll
    if re.search(r"\b(payroll|salary|payslip|transfer|payment|paie|bulletin|virement)\b", msg):
        return (
            _pick(
                lang,
                "**Payroll — payslips and transfers**:\n"
                "• **Payslip**: available via the HR/Payroll portal according to the monthly schedule.\n"
                "• **Delayed transfer**: verify bank details (IBAN), value date, and public holidays/weekends.\n"
                "• **IBAN change**: update through HR with supporting documents before payroll cut-off.\n"
                "• **Questions**: deductions and taxes are best reviewed with HR/Payroll line-by-line.\n\n"
                "Tell me the month and the issue (payslip, transfer delay, IBAN) and I'll narrow it down.",
                "**Paie — bulletins et virements**:\n"
                "• **Bulletin**: via portail RH/Paie selon calendrier.\n"
                "• **Retard**: vérifier IBAN, date de valeur, jours fériés/week-end.\n"
                "• **Changement IBAN**: mise à jour RH avant clôture.\n\n"
                "Indiquez le mois et le sujet pour une réponse ciblée.",
                "**الرواتب**:\n"
                "• **كشف الراتب**: عبر بوابة الموارد البشرية وفق الجدول الشهري.\n"
                "• **تأخر التحويل**: تحقق من IBAN وتاريخ القيمة والعطل.\n"
                "• **تغيير IBAN**: تحديث عبر HR قبل إغلاق الرواتب.\n\n"
                "اذكر الشهر والمشكلة لأحدد الإجابة.",
            ),
            "payroll",
        )

    # 6) Compliance & KYC
    if re.search(
        r"\b(compliance|kyc|aml|audit|regulation|policy|procedure|conformité|procédure|règlementation)\b",
        msg,
    ):
        return (
            _pick(
                lang,
                "**Compliance & KYC (AML/CFT) — operational reminder**:\n"
                "• **KYC**: identify/verify the customer, understand purpose, assess risk, keep records updated.\n"
                "• **Monitoring**: look for unusual patterns (amounts, frequency, geography, structuring).\n"
                "• **Evidence**: retain documentation and decision rationale for audit readiness.\n"
                "• **Escalation**: follow the internal process (Compliance/MLRO). Do not tip-off the customer.\n\n"
                "Tell me if this is an individual or a company case, and which product (account, credit, etc.).",
                "**Compliance & KYC (AML/CFT)**:\n"
                "• **KYC**: identifier, vérifier, comprendre l’objectif, évaluer le risque, tenir à jour.\n"
                "• **Surveillance**: opérations inhabituelles (montants, fréquence, pays, structuration).\n"
                "• **Preuves**: conserver la documentation pour audit.\n"
                "• **Escalade**: procédure interne (Compliance/MLRO) sans alerter le client.\n\n"
                "Précisez particulier/entreprise et le produit.",
                "**الامتثال و KYC (AML/CFT)**:\n"
                "• **KYC**: التحقق من الهوية وفهم الغرض وتقييم المخاطر وتحديث الملف.\n"
                "• **المراقبة**: أنماط غير معتادة (مبالغ/تكرار/بلدان).\n"
                "• **التوثيق**: احتفظ بالأدلة لجهوزية التدقيق.\n"
                "• **التصعيد**: وفق الإجراء الداخلي دون تنبيه العميل.\n\n"
                "هل الحالة فرد أم شركة؟ وما هو المنتج؟",
            ),
            "compliance",
        )

    # 7) Credit & Loans
    if re.search(
        r"\b(credit|loan|financing|financement|rate|simulation|installment|mensualité|murabaha|mourabaha)\b",
        msg,
    ):
        return (
            _pick(
                lang,
                "**Credit / financing — key points**:\n"
                "• **Eligibility**: income stability, debt ratio, history, and guarantees (if applicable).\n"
                "• **Documents (typical)**: ID, proof of income, statements, employment letter, quotation/asset info.\n"
                "• **Internal flow**: assessment → decision → contract → disbursement → monitoring.\n"
                "• **Compliance**: KYC plus clear economic rationale for the financing.\n"
                "• **Islamic finance**: some products (e.g., **Murabaha**) are structured as sale/markup rather than interest.\n\n"
                "Are you looking for documents, internal steps, or product explanation?",
                "**Crédit / financement**:\n"
                "• Éligibilité, pièces, étapes internes (étude → décision → signature → déblocage).\n"
                "• KYC + justification économique.\n"
                "• Mourabaha: structure vente/marge plutôt qu’intérêt.\n\n"
                "Souhaitez-vous documents, étapes, ou explication produit ?",
                "**التمويل/القروض**:\n"
                "• الأهلية والوثائق والخطوات الداخلية.\n"
                "• الالتزام بـKYC وتبرير اقتصادي.\n"
                "• المرابحة: بيع بهامش معلوم بدل فائدة.\n\n"
                "هل تريد الوثائق أم الخطوات أم شرح المنتج؟",
            ),
            "credit",
        )

    # 8) Account opening
    if re.search(r"\b(account|opening|client|customer|iban|rib|compte|ouverture)\b", msg):
        return (
            _pick(
                lang,
                "**Account opening (internal overview)**:\n"
                "• **KYC collection**: identity, address, activity, beneficial owner (companies), supporting docs.\n"
                "• **Risk approach**: apply the risk matrix (profile, country, activity, sanctions/PEP checks).\n"
                "• **Quality controls**: duplicates, completeness, consistency, document validity.\n"
                "• **Creation**: create in system, generate IBAN/RIB, sign account terms.\n"
                "• **Activation**: issue channels/means of payment according to permissions.\n\n"
                "Tell me if it's an individual or a company, and I'll list the typical documents.",
                "**Ouverture de compte (résumé interne)**:\n"
                "• Collecte KYC, scoring risque, contrôles qualité, création, activation.\n\n"
                "Particulier ou entreprise ?",
                "**فتح حساب (ملخص)**:\n"
                "• جمع KYC وتقييم المخاطر والتحقق ثم الإنشاء والتفعيل.\n\n"
                "هل هو فرد أم شركة؟",
            ),
            "account_opening",
        )

    # 9) Islamic finance terms
    if re.search(r"\b(ijara|ijāra|ijarah|murabaha|mourabaha|wakala|wakāla|sukuk|takaful)\b", msg):
        return (
            _pick(
                lang,
                "**Islamic finance — quick definitions**:\n"
                "• **Murabaha**: the bank purchases an asset and resells it to the customer with a disclosed margin.\n"
                "• **Ijara**: leasing/rental of an asset; sometimes with an ownership transfer option.\n"
                "• **Wakala**: agency/mandate — the customer appoints the bank to act/invest under agreed terms.\n"
                "• **Sukuk**: asset-backed certificates linked to assets/projects (Sharia-compliant structure).\n"
                "• **Takaful**: cooperative insurance based on mutual assistance.\n\n"
                "If you tell me the product (auto, home, SME), I can explain a typical structure.",
                "**Finance islamique — définitions rapides**:\n"
                "• Mourabaha, Ijara, Wakala, Sukuk, Takaful (résumé).\n\n"
                "Dites-moi le produit et je précise la structure.",
                "**مصطلحات المالية الإسلامية**:\n"
                "• المرابحة، الإجارة، الوكالة، الصكوك، التكافل (تعريفات سريعة).\n\n"
                "اذكر المنتج لأشرح الهيكلة.",
            ),
            "islamic_finance",
        )

    # Fallback
    return (
        _pick(
            lang,
            "I'm not fully sure about this one.\n"
            "• Rephrase with a keyword (e.g., **VPN**, **annual leave**, **payslip**, **KYC**)\n"
            "• Or use a quick topic on the left.\n\n"
            "Received: **{}**".format(raw),
            "Je ne suis pas certain de la réponse.\n"
            "• Reformulez avec un mot-clé (ex: **VPN**, **congé annuel**, **bulletin de paie**, **KYC**)\n"
            "• Ou utilisez un thème à gauche.\n\n"
            "Texte reçu: **{}**".format(raw),
            "لست متأكدًا من الإجابة.\n"
            "• أعد الصياغة بكلمة مفتاحية (VPN، إجازة سنوية، كشف راتب، KYC)\n"
            "• أو استخدم المواضيع السريعة.\n\n"
            "تم الاستلام: **{}**".format(raw),
        ),
        "fallback",
    )


@app.get("/")
def index():
    return render_template("index.html", now=_now_str())


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}

    message = str(payload.get("message", ""))
    lang = str(payload.get("lang", "en"))

    response_text, category = generate_response(message, lang=lang)
    return jsonify({"response": response_text, "category": category})


if __name__ == "__main__":
    # For internal usage / dev. In production, use a WSGI server.
    app.run(host="127.0.0.1", port=5000, debug=True)
