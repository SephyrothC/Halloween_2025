
import qrcode
import os
import json

# Remplacez par l'IP de votre Raspberry Pi
RASPBERRY_PI_IP = "192.168.1.97"  # À MODIFIER AVEC L'IP DE VOTRE RASPBERRY PI
BASE_URL = f"http://{RASPBERRY_PI_IP}:5000/quiz/"

# Charger les questions et leurs UUID
with open("data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Créer le dossier pour les QR codes
os.makedirs("qr_codes", exist_ok=True)

print("🎃 Génération des QR codes pour Halloween Quiz 2025 👻\n")
print(f"URL de base : {BASE_URL}\n")

for uuid, qdata in questions.items():
    url = f"{BASE_URL}{uuid}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"qr_codes/question_{uuid}.png"
    img.save(filename)
    print(f"✅ QR Code généré : {filename} -> {url}")

print(f"\n🎉 {len(questions)} QR codes générés avec succès dans le dossier 'qr_codes/'")
print("\n📌 Instructions :")
print("1. Imprimez les QR codes")
print("2. Découpez-les ou plastifiez-les")
print("3. Cachez-les dans votre appartement")
print("4. Que la chasse commence ! 🎃\n")
