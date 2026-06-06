from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from contextlib import asynccontextmanager
from datetime import datetime
import os

# Create FastAPI app
app = FastAPI(title="RythuMitra")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Models
class FarmerQuery(BaseModel):
    phone_number: str
    message: str

# Response generator function (with all your Telugu content)
def get_farming_response(message):
    message = message.lower()
    
    # CHILLI - 15+ Suggestions
    if "chilli" in message or "మిరప" in message:
        return """🌶️ **మిరప పంట - 15+ సంపూర్ణ సలహాలు** 🌶️
════════════════════════════════════

🐛 **పురుగులు (Pests) - 6 రకాలు:**

1. **తెల్ల దోమ (Thrips):** Fipronil 5% SC - 1.0 ml/L
2. **మిరపకాయ పురుగు:** Emamectin Benzoate - 0.4 gm/L
3. **ఆకు తొలుచు పురుగు:** Chlorantraniliprole - 0.3 ml/L
4. **సాలీడు పురుగు:** Propargite 57% EC - 1.5 ml/L
5. **పిండి పురుగు:** Buprofezin 25% SC - 1.5 ml/L
6. **తొండ పురుగు:** Novaluron 10% EC - 0.75 ml/L

🍄 **వ్యాధులు (Diseases) - 5 రకాలు:**
7. తెల్ల బూజు: Sulfur 80% WP - 2.0 gm/L
8. ఆకు మచ్చ: Carbendazim 50% WP - 1.0 gm/L
9. వేరు తెగులు: Carbendazim + Trichoderma
10. కొమ్మ చివరి తెగులు: Difenoconazole - 1.0 ml/L
11. ఆకు ముడత వైరస్: Imidacloprid - 0.3 ml/L

🌱 **సేంద్రియ ఎంపికలు:**
12. వేప నూనె: 5 ml/L + సబ్బు
13. వెల్లుల్లి స్ప్రే: 100 gm/L
14. పంచగవ్యం: 30 ml/L
15. NSKE 5%: 50 gm వేప గింజలు/L

💡 **సాగు చిట్కాలు:**
• విత్తనాలు: తేజ, ఇందమ్-5
• నాట్ల దూరం: 45 cm x 45 cm
• ఎరువులు: N:P:K = 120:60:40 kg/ఎకరా
• డ్రిప్ ఇరిగేషన్ - 60% నీరు ఆదా
• మందు పిచికారీ చేసిన 14-21 రోజుల తర్వాతే కోత

🌾 రైతుమిత్ర - మీ విశ్వసనీయ వ్యవసాయ స్నేహితుడు"""

    # COTTON - 15+ Suggestions
    elif "cotton" in message or "ప్రత్తి" in message:
        return """🌿 **ప్రత్తి పంట - 15+ సంపూర్ణ సలహాలు** 🌿
════════════════════════════════════

🐛 **పురుగులు (Pests) - 7 రకాలు:**

1. పత్తి పురుగు: Spinosad 45% SC - 0.5 ml/L
2. పిండి పురుగు: Buprofezin 25% SC - 1.5 ml/L
3. పొగాకు తొండ: Chlorantraniliprole - 0.3 ml/L
4. సాలీడు పురుగు: Abamectin 1.9% EC - 0.4 ml/L
5. తెల్ల దోమ: Imidacloprid - 0.3 ml/L
6. ఆకు తొలుచు పురుగు: Cartap Hydrochloride - 0.8 gm/L
7. బూడిద పురుగు: Thiamethoxam - 0.2 gm/L

🍄 **వ్యాధులు (Diseases) - 5 రకాలు:**
8. వేరు తెగులు: Trichoderma viride - 2.5 kg/ఎకరా
9. ఆకు మచ్చ: Hexaconazole 5% SC - 1.0 ml/L
10. ఆకు ముడత వైరస్: Imidacloprid + Oil
11. కొమ్మ తెగులు: Carbendazim 50% WP - 1.0 gm/L
12. ఆకు ఎర్రబారు: Magnesium Sulphate - 10 gm/L

🧪 **సూక్ష్మ పోషకాలు:**
13. జింక్: Zinc Sulphate 25 kg/ఎకరా
14. బోరాన్: Borax 10 kg/ఎకరా
15. మెగ్నీషియం: Mg Sulphate 15 kg/ఎకరా

💡 **సాగు చిట్కాలు:**
• Bt Cotton: MECH-162, RCH-659
• నాట్ల దూరం: 90 cm x 60 cm
• ఎరువులు: N:P:K = 120:60:60 kg/ఎకరా
• డ్రిప్ ఇరిగేషన్ - 80% నీరు ఆదా
• పూత దశలో మందు పిచికారీ చేయవద్దు

🌾 రైతుమిత్ర - మీ స్మార్ట్ వ్యవసాయ స్నేహితుడు"""

    # PADDY - 15+ Suggestions
    elif "paddy" in message or "వరి" in message:
        return """🌾 **వరి పంట - 15+ సంపూర్ణ సలహాలు** 🌾
════════════════════════════════════

🐛 **పురుగులు (Pests) - 6 రకాలు:**

1. కాండం తొలుచు పురుగు: Chlorantraniliprole - 0.4 ml/L
2. ఆకు మంట: Tricyclazole 75% WP - 0.6 gm/L
3. ఆకు తొలుచు పురుగు: Chlorantraniliprole - 0.3 ml/L
4. గోనె పురుగు: Fipronil 5% SC - 1.0 ml/L
5. తామర పురుగు: Acephate 75% SP - 1.0 gm/L
6. కాండం తెగులు: Chlorpyriphos - 2.0 ml/L

🍄 **వ్యాధులు (Diseases) - 6 రకాలు:**
7. కాండం తెగులు: Hexaconazole 5% SC - 1.0 ml/L
8. కొమ్మ తెగులు: Carbendazim 50% WP - 1.0 gm/L
9. కంకి తెగులు: Propiconazole 25% EC - 1.0 ml/L
10. ఆకు మచ్చ: Edifenphos 50% EC - 1.0 ml/L
11. ఆకు బూడిద: Validamycin 3% L - 2.0 ml/L
12. నాటు విరుగుడు: Streptocycline - 0.5 gm/L

🌱 **సేంద్రియ ఎంపికలు:**
13. వేప ఆకుల కషాయం: 200 gm/L
14. వేప నూనె: 5 ml/L + సబ్బు
15. పంచగవ్యం: 30 ml/L

💡 **సాగు చిట్కాలు:**
• రకాలు: BPT 5204, MTU 1010
• నాట్ల దూరం: 15 cm x 10 cm
• ఎరువులు: N:P:K = 120:60:40 kg/ఎకరా
• AWD నీటి పద్ధతి
• మందు కలిపిన 21-25 రోజుల తర్వాతే కోత

🌾 రైతుమిత్ర - మీ విశ్వసనీయ వ్యవసాయ స్నేహితుడు"""

    # TOMATO
    elif "tomato" in message or "టమోటా" in message:
        return """🍅 **టమోటా పంట - 15+ సంపూర్ణ సలహాలు** 🍅
════════════════════════════════════

🐛 **పురుగులు (Pests):**
1. ఆకు మైనర్: Cyantraniliprole - 0.3 ml/L
2. కాయ పురుగు: Emamectin Benzoate - 0.4 gm/L
3. తెల్ల దోమ: Imidacloprid - 0.3 ml/L
4. సాలీడు పురుగు: Propargite - 1.5 ml/L
5. పిండి పురుగు: Buprofezin - 1.5 ml/L
6. తొండ పురుగు: Chlorantraniliprole - 0.3 ml/L

🍄 **వ్యాధులు:**
7. ఆకు మచ్చ: Chlorothalonil - 2.0 gm/L
8. వేరు తెగులు: Carbendazim - 1.0 gm/L
9. ఆకు తెగులు: Metalaxyl + Mancozeb
10. కాయ తెగులు: Carbendazim - 1.0 gm/L
11. ఆకు ముడత: Imidacloprid + Oil
12. కాండం తెగులు: Hexaconazole - 1.0 ml/L

🌱 **సేంద్రియ:**
13. వేప నూనె: 5 ml/L
14. వెల్లుల్లి స్ప్రే: 100 gm/L
15. పంచగవ్యం: 30 ml/L

💡 **సాగు చిట్కాలు:**
• రకాలు: Pusa Ruby, Arka Vikas
• నాట్ల దూరం: 60 cm x 45 cm
• స్టేకింగ్ తప్పనిసరి
• డ్రిప్ ఇరిగేషన్

🌾 రైతుమిత్ర - మీ విశ్వసనీయ వ్యవసాయ స్నేహితుడు"""

    elif "help" in message or "menu" in message:
        return """🌾 **రైతుమిత్ర సహాయ మెనూ**
══════════════════════════════

అందుబాటులో ఉన్న పంటలు:
1️⃣ వరి - "వరి" లేదా "paddy" టైప్ చేయండి
2️⃣ ప్రత్తి - "ప్రత్తి" లేదా "cotton" టైప్ చేయండి
3️⃣ మిరప - "మిరప" లేదా "chilli" టైప్ చేయండి
4️⃣ టమోటా - "టమోటా" లేదా "tomato" టైప్ చేయండి

మీ పంట పేరు టైప్ చేసి 15+ సూచనలను పొందండి!"""
    
    else:
        return """🌾 **రైతుమిత్రకు స్వాగతం!**
══════════════════════════════

అందుబాటులో ఉన్న పంటలు:
🌾 వరి (paddy)
🌿 ప్రత్తి (cotton)
🌶️ మిరప (chilli)
🍅 టమోటా (tomato)

మీ పంట పేరు టైప్ చేయండి!
ఉదా: "మిరప" లేదా "chilli"

సహాయం కోసం "help" టైప్ చేయండి"""

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "crops_count": 4,
        "pesticides_count": 20,
        "queries_count": 0
    })

@app.post("/api/whatsapp")
async def whatsapp_webhook(query: FarmerQuery):
    response = get_farming_response(query.message)
    return {
        "success": True,
        "message": response,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/crops")
async def get_crops():
    return {"crops": [
        {"id": 1, "name": "Paddy", "name_te": "వరి"},
        {"id": 2, "name": "Cotton", "name_te": "ప్రత్తి"},
        {"id": 3, "name": "Chilli", "name_te": "మిరప"},
        {"id": 4, "name": "Tomato", "name_te": "టమోటా"}
    ]}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RythuMitra", "version": "2.0.0"}

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)