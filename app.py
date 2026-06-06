from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from contextlib import asynccontextmanager
import sqlite3
import os
from datetime import datetime

# Database setup
DATABASE_PATH = "data/rythumitra.db"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Database connection
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_database():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT,
            name_te TEXT,
            season TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pesticides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            name_te TEXT,
            dilution_ml REAL,
            wait_days INTEGER,
            safety_tips TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmer_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            query TEXT,
            response TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data if empty
    cursor.execute("SELECT COUNT(*) as count FROM crops")
    if cursor.fetchone()['count'] == 0:
        cursor.execute("INSERT INTO crops (name_en, name_te, season) VALUES ('Paddy', 'వరి', 'Kharif')")
        cursor.execute("INSERT INTO crops (name_en, name_te, season) VALUES ('Cotton', 'ప్రత్తి', 'Kharif')")
        cursor.execute("INSERT INTO crops (name_en, name_te, season) VALUES ('Chilli', 'మిరప', 'Rabi')")
        cursor.execute("INSERT INTO crops (name_en, name_te, season) VALUES ('Tomato', 'టమోటా', 'Rabi')")
        cursor.execute("INSERT INTO pesticides (name, name_te, dilution_ml, wait_days) VALUES ('Chlorantraniliprole', 'క్లోరాంట్రానిలిప్రోల్', 0.4, 21)")
        cursor.execute("INSERT INTO pesticides (name, name_te, dilution_ml, wait_days) VALUES ('Tricyclazole', 'ట్రైసైక్లాజోల్', 0.6, 25)")
        cursor.execute("INSERT INTO pesticides (name, name_te, dilution_ml, wait_days) VALUES ('Spinosad', 'స్పైనోసాడ్', 0.5, 21)")
    
    conn.commit()
    conn.close()
    print("✅ డేటాబేస్ సిద్ధమైంది!")

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 రైతుమిత్ర స్టార్ట్ అవుతుంది...")
    init_database()
    print("""
    ════════════════════════════════════════════
    🌾 రైతుమిత్ర - స్మార్ట్ వ్యవసాయ వేదిక
    ════════════════════════════════════════════
    ✅ సర్వర్ రన్నింగ్!
    📍 డ్యాష్ బోర్డు: /dashboard
    💬 వాట్సాప్ API: POST /api/whatsapp
    ════════════════════════════════════════════
    """)
    yield
    print("🛑 సర్వర్ ఆగిపోతుంది...")

# Create FastAPI app
app = FastAPI(title="రైతుమిత్ర", lifespan=lifespan)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Models
class FarmerQuery(BaseModel):
    phone_number: str
    message: str

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Dashboard
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM crops")
    crops_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM pesticides")
    pesticides_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM farmer_queries")
    queries_count = cursor.fetchone()['total']
    conn.close()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "crops_count": crops_count,
        "pesticides_count": pesticides_count,
        "queries_count": queries_count
    })

# WhatsApp webhook with 15+ suggestions in Telugu
@app.post("/api/whatsapp")
async def whatsapp_webhook(query: FarmerQuery):
    message = query.message.lower()
    
    # ============================================
    # CHILLI (మిరప) - 15+ సంపూర్ణ సలహాలు
    # ============================================
    if "chilli" in message or "మిరప" in message or "mirchi" in message:
        response = """🌶️ **మిరప పంట - 15+ సంపూర్ణ సలహాలు** 🌶️
══════════════════════════════════════════════════

🐛 **పురుగులు (Pests) - 6 రకాలు:**

1. **తెల్ల దోమ (Thrips):**
   💊 Chlorfenapyr 10% SC - 1.0 ml/L
   💊 Fipronil 5% SC - 1.0 ml/L
   ⏰ PHI: 14 రోజులు
   🌿 సేంద్రియ: వేప నూనె 5ml/L + సబ్బు

2. **మిరపకాయ పురుగు (Fruit Borer):**
   💊 Emamectin Benzoate 5% SG - 0.4 gm/L
   💊 Spinosad 45% SC - 0.5 ml/L
   💊 Indoxacarb 15.5% SC - 0.5 ml/L
   ⏰ PHI: 10 రోజులు
   🌿 సేంద్రియ: NSKE 5% + ఫెరోమోన్ ట్రాప్స్

3. **ఆకు తొలుచు పురుగు (Leaf Roller):**
   💊 Chlorantraniliprole 18.5% SC - 0.3 ml/L
   💊 Flubendiamide 20% WG - 0.3 gm/L
   ⏰ PHI: 21 రోజులు
   🌿 సేంద్రియ: Bt (Bacillus thuringiensis)

4. **సాలీడు పురుగు (Mites):**
   💊 Propargite 57% EC - 1.5 ml/L
   💊 Fenazaquin 10% EC - 1.5 ml/L
   💊 Abamectin 1.9% EC - 0.4 ml/L
   ⏰ PHI: 14 రోజులు
   🌿 సేంద్రియ: సఫాయిల్ (1 ml/L)

5. **పిండి పురుగు (Mealybug):**
   💊 Buprofezin 25% SC - 1.5 ml/L
   💊 Diafenthiuron 50% WP - 0.8 gm/L
   🌿 సేంద్రియ: వేప నూనె + స్టిక్కర్

6. **తొండ పురుగు (Tobacco Caterpillar):**
   💊 Novaluron 10% EC - 0.75 ml/L
   💊 Lufenuron 5% EC - 1.0 ml/L
   🌿 సేంద్రియ: లైట్ ట్రాప్స్ + Bt

🍄 **వ్యాధులు (Diseases) - 5 రకాలు:**

7. **తెల్ల బూజు (Powdery Mildew):**
   💊 Sulfur 80% WP - 2.0 gm/L
   💊 Hexaconazole 5% SC - 1.0 ml/L
   💊 Tebuconazole 25% EC - 1.0 ml/L
   🌿 సేంద్రియ: బేకింగ్ సోడా (2gm/L) + నూనె

8. **ఆకు మచ్చ (Leaf Spot - Cercospora):**
   💊 Carbendazim 50% WP - 1.0 gm/L
   💊 Mancozeb 75% WP - 2.0 gm/L
   💊 Chlorothalonil 75% WP - 2.0 gm/L

9. **వేరు తెగులు (Root Rot):**
   💊 Carbendazim + Trichoderma
   💊 Tebuconazole 25% EC
   🌿 సేంద్రియ: Pseudomonas fluorescens

10. **కొమ్మ చివరి తెగులు (Die Back):**
    💊 Difenoconazole 25% EC - 1.0 ml/L
    💊 Propiconazole 25% EC - 1.0 ml/L

11. **ఆకు ముడత వైరస్ (Leaf Curl Virus):**
    💊 Imidacloprid 17.8% SL - 0.3 ml/L
    💊 Acetamiprid 20% SP - 0.2 gm/L
    🦟 తెల్లదోమ నియంత్రణ తప్పనిసరి

🌱 **సేంద్రియ ఎంపికలు (Organic Options) - 6 రకాలు:**

12. **వేప నూనె (Neem Oil):** 5 ml/L + 1 gm సబ్బు
13. **వెల్లుల్లి స్ప్రే:** 100 gm/L (24 గంటలు నానబెట్టి)
14. **పంచగవ్యం:** 30 ml/L (3% ద్రావణం)
15. **NSKE 5%:** 50 gm వేప గింజలు/L (రాత్రి నానబెట్టి)
16. **బూడిద ద్రావణం:** 50 gm/L (వడపోసి వాడండి)
17. **వేప ఆకుల కషాయం:** 200 gm/L (మరిగించి)

💡 **సాగు చిట్కాలు (15 Important Tips):**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌱 **నాట్లు & విత్తనాలు:**
1. విత్తనాలు: తేజ, ఇందమ్-5, జీ4, ఎల్సీఏ-625
2. నాట్ల దూరం: 45 cm x 45 cm
3. విత్తన శుద్ధి: ట్రైకోడెర్మా 10 gm/kg

🌾 **ఎరువులు (Fertilizers):**
4. ఎన్:పి:కే = 120:60:40 kg/ఎకరా
5. సేంద్రియ ఎరువు: 10 టన్నులు/ఎకరా
6. జింక్ సల్ఫేట్: 25 kg/ఎకరా (30 రోజులకు)
7. బోరాన్: 10 kg/ఎకరా (పూతకు ముందు)

💧 **నీటి నిర్వహణ:**
8. డ్రిప్ ఇరిగేషన్ - 60% నీరు ఆదా
9. చిన్న చిన్న మోతాదుల్లో (వారానికి 2-3 సార్లు)

🍂 **మల్చింగ్ & కలుపు:**
10. ప్లాస్టిక్ మల్చ్ - కలుపు నియంత్రణ
11. 15, 30, 45 రోజులకు కలుపు తీయుట

🪤 **ట్రాప్స్ & నివారణ:**
12. నీలం రంగు స్టిక్కీ ట్రాప్స్ (12/ఎకరా)
13. ఫెరోమోన్ ట్రాప్స్ (6/ఎకరా)
14. లైట్ ట్రాప్స్ (1/2 ఎకరాకు)

⚠️ **ముఖ్య జాగ్రత్తలు:**
15. మందు పిచికారీ చేసిన 14-21 రోజుల తర్వాతే కోతకు తీసుకోండి

📞 **తెలుగులో మరిన్ని సలహాలకు:**
చేతి తొడుగులు, మాస్క్ తప్పనిసరి
స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి

🌾 **రైతుమిత్ర - మీ విశ్వసనీయ వ్యవసాయ స్నేహితుడు**"""

    # ============================================
    # COTTON (ప్రత్తి) - 15+ సంపూర్ణ సలహాలు
    # ============================================
    elif "cotton" in message or "ప్రత్తి" in message or "pratti" in message:
        response = """🌿 **ప్రత్తి పంట - 15+ సంపూర్ణ సలహాలు** 🌿
══════════════════════════════════════════════════

🐛 **పురుగులు (Pests) - 7 రకాలు:**

1. **పత్తి పురుగు (American Bollworm):**
   💊 Spinosad 45% SC - 0.5 ml/L
   💊 Emamectin Benzoate 5% SG - 0.4 gm/L
   💊 Indoxacarb 15.5% SC - 0.5 ml/L
   ⏰ PHI: 21 రోజులు
   🌿 సేంద్రియ: NSKE 5% + ఫెరోమోన్ ట్రాప్స్ (12/ఎకరా)

2. **పిండి పురుగు (Mealybug):**
   💊 Buprofezin 25% SC - 1.5 ml/L
   💊 Diafenthiuron 50% WP - 0.8 gm/L
   💊 Chlorpyriphos 20% EC - 2.0 ml/L
   🌿 సేంద్రియ: వేప నూనె 5ml/L + నీలం స్టిక్కీ ట్రాప్స్

3. **పొగాకు తొండ (Tobacco Caterpillar):**
   💊 Chlorantraniliprole 18.5% SC - 0.3 ml/L
   💊 Flubendiamide 20% WG - 0.3 gm/L
   🌿 సేంద్రియ: Bt + లైట్ ట్రాప్స్ (1/2 ఎకరాకు)

4. **సాలీడు పురుగు (Red Spider Mite):**
   💊 Abamectin 1.9% EC - 0.4 ml/L
   💊 Fenpyroximate 5% SC - 0.5 ml/L
   💊 Propargite 57% EC - 1.5 ml/L

5. **తెల్ల దోమ (Whitefly):**
   💊 Imidacloprid 17.8% SL - 0.3 ml/L
   💊 Diafenthiuron 50% WP - 0.6 gm/L
   💊 Pyriproxyfen 10% EC - 1.0 ml/L
   🌿 సేంద్రియ: పసుపు స్టిక్కీ ట్రాప్స్ (20/ఎకరా)

6. **ఆకు తొలుచు పురుగు (Leaf Roller):**
   💊 Cartap Hydrochloride 50% SP - 0.8 gm/L
   💊 Fipronil 5% SC - 1.0 ml/L

7. **బూడిద పురుగు (Grey Weevil):**
   💊 Thiamethoxam 25% WG - 0.2 gm/L
   💊 Acephate 75% SP - 1.0 gm/L

🍄 **వ్యాధులు (Diseases) - 5 రకాలు:**

8. **వేరు తెగులు (Root Rot):**
   💊 Trichoderma viride - 2.5 kg/ఎకరా
   💊 Carbendazim 50% WP - 1.0 gm/L
   🌿 సేంద్రియ: Pseudomonas fluorescens

9. **ఆకు మచ్చ (Alternaria Leaf Spot):**
   💊 Hexaconazole 5% SC - 1.0 ml/L
   💊 Propiconazole 25% EC - 1.0 ml/L
   💊 Chlorothalonil 75% WP - 2.0 gm/L

10. **ఆకు ముడత వైరస్ (Leaf Curl Virus):**
    💊 Imidacloprid + నూనె
    🦟 తెల్లదోమ నియంత్రణ తప్పనిసరి

11. **కొమ్మ తెగులు (Boll Rot):**
    💊 Carbendazim 50% WP - 1.0 gm/L
    💊 Copper Oxycloride 50% WP - 2.0 gm/L

12. **ఆకు ఎర్రబారు (Red Leaf):**
    💊 Magnesium Sulphate - 10 gm/L
    💊 Urea - 10 gm/L (ఆకు పైన స్ప్రే)

🌱 **సేంద్రియ ఎంపికలు (Organic Options) - 6 రకాలు:**

13. **NSKE 5%:** 50 gm/L (వేప గింజలు)
14. **వేప నూనె:** 5 ml/L + సబ్బు 1 gm/L
15. **పంచగవ్యం:** 30 ml/L (3% ద్రావణం)
16. **ట్రైకోగ్రామా కార్డ్స్:** 50/ఎకరా
17. **ఫెరోమోన్ ట్రాప్స్:** 12/ఎకరా
18. **లైట్ ట్రాప్స్:** 1/2 ఎకరాకు

🧪 **సూక్ష్మ పోషకాలు (Micro-nutrients):**

19. **జింక్ (Zinc):** జింక్ సల్ఫేట్ 25 kg/ఎకరా
20. **బోరాన్ (Boron):** బోరాక్స్ 10 kg/ఎకరా
21. **మెగ్నీషియం (Mg):** Mg Sulphate 15 kg/ఎకరా
22. **ఐరన్ (Iron):** ఫెర్రస్ సల్ఫేట్ 10 kg/ఎకరా
23. **కాల్షియం (Ca):** కాల్షియం నైట్రేట్ 5 kg/ఎకరా

💡 **సాగు చిట్కాలు (15 Important Tips):**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌱 **విత్తనాలు & నాట్లు:**
1. Bt ప్రత్తి: MECH-162, RCH-659, బన్నీ
2. నాట్ల దూరం: 90 cm x 60 cm (తూర్పు-పడమర)
3. విత్తన శుద్ధి: ఇమిడాక్లోప్రిడ్ 5 ml/kg

🌾 **ఎరువులు (Fertilizers):**
4. N:P:K = 120:60:60 kg/ఎకరా (Split doses)
5. సేంద్రియ ఎరువు: 10 టన్నులు/ఎకరా
6. DAP: 50 kg/ఎకరా (పూతకు ముందు)
7. MOP: 40 kg/ఎకరా (కాయలు ఏర్పడునపుడు)

💧 **నీటి నిర్వహణ:**
8. డ్రిప్ ఇరిగేషన్ - 80% నీరు ఆదా
9. క్లిష్టమైన దశలు: పూత, కాయలు ఏర్పడు సమయం

🍂 **కలుపు & మల్చింగ్:**
10. ప్లాస్టిక్ మల్చ్ (30 మైక్రాన్లు)
11. 30, 60, 90 రోజులకు కలుపు తీయుట

✂️ **కాపింగ్ (Pruning):**
12. 90-100 రోజులకు పై కొమ్మలు తొలగించండి
13. దెబ్బతిన్న కొమ్మలను తీసివేయండి

🪤 **ట్రాప్స్:**
14. పసుపు స్టిక్కీ ట్రాప్స్ (20/ఎకరా) - Whiteflyకు
15. నీలం ట్రాప్స్ (12/ఎకరా) - Thripsకు

⚠️ **ముఖ్య జాగ్రత్తలు:**
• పూత దశలో మందు పిచికారీ చేయవద్దు
• తేనెటీగల సంరక్షణకు ఉదయం 6-9 గంటల వరకే స్ప్రే చేయండి
• 40°C పైన స్ప్రే చేయకండి
• ప్రతి 10-15 రోజులకు మందు మార్చండి

🔄 **పంట మార్పిడి (3 సంవత్సరాలు):**
1వ సంవత్సరం: ప్రత్తి → 2వ సంవత్సరం: మిరప → 3వ సంవత్సరం: మొక్కజొన్న

🌾 **రైతుమిత్ర - మీ స్మార్ట్ వ్యవసాయ స్నేహితుడు**"""

    # ============================================
    # PADDY (వరి) - 15+ సంపూర్ణ సలహాలు
    # ============================================
    elif "paddy" in message or "వరి" in message or "vari" in message:
        response = """🌾 **వరి పంట - 15+ సంపూర్ణ సలహాలు** 🌾
══════════════════════════════════════════════════

🐛 **పురుగులు (Pests) - 6 రకాలు:**

1. **కాండం తొలుచు పురుగు (Stem Borer):**
   💊 Chlorantraniliprole 18.5% SC - 0.4 ml/L
   💊 Cartap Hydrochloride 50% SP - 0.8 gm/L
   💊 Fipronil 5% SC - 1.0 ml/L
   ⏰ స్ప్రే సమయం: 25-30, 45-50 రోజులకు
   🌿 సేంద్రియ: వేప నూనె + ఫెరోమోన్ ట్రాప్స్

2. **ఆకు మంట (Leaf Blast):**
   💊 Tricyclazole 75% WP - 0.6 gm/L
   💊 Isoprothiolane 40% EC - 1.5 ml/L
   💊 Kasugamycin 3% L - 1.5 ml/L
   ⏰ PHI: 25 రోజులు

3. **ఆకు తొలుచు పురుగు (Leaf Folder):**
   💊 Chlorantraniliprole 18.5% SC - 0.3 ml/L
   💊 Flubendiamide 20% WG - 0.3 gm/L
   🌿 సేంద్రియ: Bt + లైట్ ట్రాప్స్

4. **గోనె పురుగు (Case Worm):**
   💊 Fipronil 5% SC - 1.0 ml/L
   💊 Acephate 75% SP - 1.0 gm/L

5. **తామర పురుగు (Rice Hispa):**
   💊 Acephate 75% SP - 1.0 gm/L
   💊 Chlorpyriphos 20% EC - 2.0 ml/L

6. **కాండం తెగులు (Gall Midge):**
   💊 Chlorpyriphos 20% EC - 2.0 ml/L
   💊 Monocrotophos 36% SL - 1.5 ml/L

🍄 **వ్యాధులు (Diseases) - 6 రకాలు:**

7. **కాండం తెగులు (Sheath Blight):**
   💊 Hexaconazole 5% SC - 1.0 ml/L
   💊 Validamycin 3% L - 2.0 ml/L
   💊 Propiconazole 25% EC - 1.0 ml/L

8. **కొమ్మ తెగులు (Stem Rot):**
   💊 Carbendazim 50% WP - 1.0 gm/L
   💊 Tebuconazole 25% EC - 1.0 ml/L

9. **కంకి తెగులు (False Smut):**
   💊 Propiconazole 25% EC - 1.0 ml/L
   💊 Copper Oxycloride 50% WP - 2.0 gm/L
   ⏰ స్ప్రే సమయం: పూత దశలో (50% పూత వచ్చినప్పుడు)

10. **ఆకు మచ్చ (Brown Spot):**
    💊 Edifenphos 50% EC - 1.0 ml/L
    💊 Carbendazim 50% WP - 1.0 gm/L

11. **ఆకు బూడిద (Sheath Rot):**
    💊 Validamycin 3% L - 2.0 ml/L
    💊 Streptocycline - 0.5 gm/L

12. **నాటు విరుగుడు (Bacterial Blight):**
    💊 Streptocycline - 0.5 gm/L + రాగి

🌱 **సేంద్రియ ఎంపికలు (Organic Options) - 6 రకాలు:**

13. **వేప ఆకుల కషాయం:** 200 gm/L (మరిగించి)
14. **వేప నూనె:** 5 ml/L + 1 gm సబ్బు
15. **పంచగవ్యం:** 30 ml/L (3% ద్రావణం)
16. **ట్రైకోడెర్మా:** 2.5 kg/ఎకరా (నేలలో కలపాలి)
17. **ప్సూడోమోనాస్:** 2.5 kg/ఎకరా
18. **వేప గింజల ద్రావణం:** 50 gm/L (NSKE 5%)

💡 **సాగు చిట్కాలు (15 Important Tips):**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌱 **విత్తనాలు & నాట్లు:**
1. రకాలు: BPT 5204, MTU 1010, NLR 34449
2. విత్తన శుద్ధి: Carbendazim 2 gm/kg
3. నాట్ల దూరం: 15 cm x 10 cm (సన్నగా)
4. వయసు: 25-30 రోజుల మొక్కలు

🌾 **ఎరువులు (Fertilizers):**
5. N:P:K = 120:60:40 kg/ఎకరా (Split doses)
6. సేంద్రియ ఎరువు: 8-10 టన్నులు/ఎకరా
7. జింక్ సల్ఫేట్: 25 kg/ఎకరా (30 రోజులకు)
8. ఐరన్ (Fe): 20 kg/ఎకరా (నాట్లకు ముందు)

💧 **నీటి నిర్వహణ:**
9. AWD (Alternate Wetting & Drying) పద్ధతి
10. 2-3 cm నీరు మాత్రమే నిలువ ఉంచండి
11. పూత దశలో 5 cm నీరు అవసరం

🍂 **కలుపు నియంత్రణ:**
12. 15, 30, 45 రోజులకు చేతితో తీయుట
13. Butachlor 5% G - 10 kg/ఎకరా (3 రోజులలోపు)

🪤 **ట్రాప్స్:**
14. లైట్ ట్రాప్స్ (1/2 ఎకరాకు) - రాత్రి 6-10 గంటలు
15. ఫెరోమోన్ ట్రాప్స్ (6/ఎకరా) - Stem borerకు

⚠️ **ముఖ్య జాగ్రత్తలు:**
• వర్షం ముందు మందు పిచికారీ చేయవద్దు
• 35°C పైన స్ప్రే చేయకండి
• మందు కలిపిన 21-25 రోజుల తర్వాతే కోతకు తీసుకోండి
• ప్రతి స్ప్రేకు వేరే మందు వాడండి

🔄 **పంట మార్పిడి:**
ప్రత్తి → మిరప → వరి (2 సంవత్సరాల మార్పిడి)

🌾 **రైతుమిత్ర - మీ విశ్వసనీయ వ్యవసాయ స్నేహితుడు**"""

    # ============================================
    # TOMATO (టమోటా) - 15+ సంపూర్ణ సలహాలు
    # ============================================
    elif "tomato" in message or "టమోటా" in message:
        response = """🍅 **టమోటా పంట - 15+ సంపూర్ణ సలహాలు** 🍅
══════════════════════════════════════════════════

🐛 **పురుగులు (Pests) - 6 రకాలు:**

1. **ఆకు మైనర్ (Leaf Minor):**
   💊 Cyantraniliprole 10% OD - 0.3 ml/L
   💊 Abamectin 1.9% EC - 0.4 ml/L
   🌿 సేంద్రియ: పసుపు స్టిక్కీ ట్రాప్స్

2. **కాయ పురుగు (Fruit Borer):**
   💊 Emamectin Benzoate 5% SG - 0.4 gm/L
   💊 Indoxacarb 15.5% SC - 0.5 ml/L
   💊 Spinosad 45% SC - 0.5 ml/L

3. **తెల్ల దోమ (Whitefly):**
   💊 Imidacloprid 17.8% SL - 0.3 ml/L
   💊 Diafenthiuron 50% WP - 0.6 gm/L

4. **సాలీడు పురుగు (Mites):**
   💊 Propargite 57% EC - 1.5 ml/L
   💊 Fenazaquin 10% EC - 1.5 ml/L

5. **పిండి పురుగు (Mealybug):**
   💊 Buprofezin 25% SC - 1.5 ml/L
   💊 Chlorpyriphos 20% EC - 2.0 ml/L

6. **తొండ పురుగు (Tobacco Caterpillar):**
   💊 Chlorantraniliprole 18.5% SC - 0.3 ml/L

🍄 **వ్యాధులు (Diseases) - 6 రకాలు:**

7. **ఆకు మచ్చ (Early Blight):**
   💊 Chlorothalonil 75% WP - 2.0 gm/L
   💊 Mancozeb 75% WP - 2.0 gm/L

8. **వేరు తెగులు (Root Rot):**
   💊 Carbendazim 50% WP - 1.0 gm/L
   🌿 సేంద్రియ: Trichoderma viride

9. **ఆకు తెగులు (Late Blight):**
   💊 Metalaxyl + Mancozeb - 2.0 gm/L
   💊 Cymoxanil + Mancozeb - 2.0 gm/L

10. **కాయ తెగులు (Fruit Rot):**
    💊 Carbendazim 50% WP - 1.0 gm/L
    💊 Captan 50% WP - 2.0 gm/L

11. **ఆకు ముడత (Leaf Curl Virus):**
    💊 Imidacloprid + నూనె (Whitefly control)
    💊 వేప నూనె - 5 ml/L

12. **కాండం తెగులు (Stem Rot):**
    💊 Hexaconazole 5% SC - 1.0 ml/L

🌱 **సేంద్రియ ఎంపికలు (Organic Options) - 6 రకాలు:**

13. **వేప నూనె:** 5 ml/L + 1 gm సబ్బు
14. **వెల్లుల్లి స్ప్రే:** 100 gm/L (24 గంటలు నానబెట్టి)
15. **పంచగవ్యం:** 30 ml/L (3% ద్రావణం)
16. **బూడిద ద్రావణం:** 50 gm/L (వడపోసి)
17. **ట్రైకోడెర్మా:** 2.5 kg/ఎకరా
18. **ప్సూడోమోనాస్:** 2.5 kg/ఎకరా

🧪 **సూక్ష్మ పోషకాలు (Micro-nutrients):**

19. **జింక్:** జింక్ సల్ఫేట్ 25 kg/ఎకరా
20. **బోరాన్:** బోరాక్స్ 10 kg/ఎకరా
21. **కాల్షియం:** Ca Nitrate 5 gm/L (ఆకు పైన)
22. **మెగ్నీషియం:** Mg Sulphate 10 gm/L

💡 **సాగు చిట్కాలు (15 Important Tips):**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌱 **విత్తనాలు & నాట్లు:**
1. రకాలు: పూసా రూబీ, అర్కా వికాస్, PKM-1
2. విత్తన శుద్ధి: ట్రైకోడెర్మా 10 gm/kg
3. నాట్ల దూరం: 60 cm x 45 cm
4. నాటు వేయు లోతు: 5-7 cm

🌾 **ఎరువులు (Fertilizers):**
5. N:P:K = 100:60:60 kg/ఎకరా
6. సేంద్రియ ఎరువు: 15 టన్నులు/ఎకరా
7. DAP: 50 kg/ఎకరా (నాటు వేసేముందు)
8. MOP: 30 kg/ఎకరా (కాయలు ఏర్పడునపుడు)

💧 **నీటి నిర్వహణ:**
9. డ్రిప్ ఇరిగేషన్ (2 LPH emitters)
10. క్రమంగా (ప్రతి 4-5 రోజులకు)
11. కాయలు ఏర్పడు సమయంలో ఎక్కువ నీరు

🍂 **స్టేకింగ్ & కాపింగ్:**
12. స్టేకింగ్ తప్పనిసరి (6 అడుగుల కర్రలు)
13. పక్క కొమ్మలు తొలగించండి (Pruning)
14. దెబ్బతిన్న ఆకులు తీసివేయండి

🪤 **ట్రాప్స్:**
15. పసుపు స్టిక్కీ ట్రాప్స్ (20/ఎకరా)

⚠️ **ముఖ్య జాగ్రత్తలు:**
• పండిన కాయలను ముందుగా తీయండి
• మందు పిచికారీ చేసిన 7-14 రోజుల తర్వాతే కోతకు తీసుకోండి
• సేంద్రియ మరియు రసాయన మందులను కలిపి వాడండి
• నాణ్యమైన విత్తనాలు మాత్రమే వాడండి

🌾 **రైతుమిత్ర - మీ విశ్వసనీయ వ్యవసాయ స్నేహితుడు**"""

    # ============================================
    # HELP MENU
    # ============================================
    elif "help" in message or "సహాయం" in message or "menu" in message:
        response = """🌾 **రైతుమిత్ర సంపూర్ణ సహాయ మెనూ**
══════════════════════════════════════════════════

📱 **అందుబాటులో ఉన్న పంటలు (15+ సూచనలతో):**

1️⃣ 🌾 **వరి (Paddy)** - 15+ సూచనలు
   టైప్ చేయండి: "వరి" లేదా "paddy"
   • 6 పురుగుల నివారణ
   • 6 వ్యాధుల నియంత్రణ
   • 6 సేంద్రియ స్ప్రేలు
   • 15 సాగు చిట్కాలు

2️⃣ 🌿 **ప్రత్తి (Cotton)** - 15+ సూచనలు
   టైప్ చేయండి: "ప్రత్తి" లేదా "cotton"
   • 7 పురుగుల నివారణ
   • 5 వ్యాధుల నియంత్రణ
   • 6 సేంద్రియ ఎంపికలు
   • 5 సూక్ష్మ పోషకాలు
   • 15 సాగు చిట్కాలు

3️⃣ 🌶️ **మిరప (Chilli)** - 15+ సూచనలు
   టైప్ చేయండి: "మిరప" లేదా "chilli"
   • 6 పురుగుల నివారణ
   • 5 వ్యాధుల నియంత్రణ
   • 6 సేంద్రియ స్ప్రేలు
   • 15 సాగు చిట్కాలు

4️⃣ 🍅 **టమోటా (Tomato)** - 15+ సూచనలు
   టైప్ చేయండి: "టమోటా" లేదా "tomato"
   • 6 పురుగుల నివారణ
   • 6 వ్యాధుల నియంత్రణ
   • 6 సేంద్రియ ఎంపికలు
   • 15 సాగు చిట్కాలు

💬 **ఎలా వాడాలి:**
మీ పంట పేరు టైప్ చేయండి (తెలుగులో లేదా ఆంగ్లంలో)
ఉదాహరణ: "మిరప" లేదా "chilli"
నేను వెంటనే 15+ వివరణాత్మక సూచనలు ఇస్తాను

🆘 **ఇతర సందేహాలకు:**
స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి
వ్యవసాయ విశ్వవిద్యాలయాలను సందర్శించండి

🌾 **రైతుమిత్ర - మీ స్మార్ట్ వ్యవసాయ స్నేహితుడు!**
══════════════════════════════════════════════════"""

    # ============================================
    # DEFAULT RESPONSE
    # ============================================
    else:
        response = """🌾 **రైతుమిత్రకు స్వాగతం!**
══════════════════════════════════

📋 **అందుబాటులో ఉన్న పంటలు (15+ సూచనలతో):**

🌾 **1. వరి (Paddy)** - టైప్ చేయండి: "వరి" లేదా "paddy"
   → 6 పురుగులు, 6 వ్యాధులు, 15 సాగు చిట్కాలు

🌿 **2. ప్రత్తి (Cotton)** - టైప్ చేయండి: "ప్రత్తి" లేదా "cotton"
   → 7 పురుగులు, 5 వ్యాధులు, 5 సూక్ష్మ పోషకాలు

🌶️ **3. మిరప (Chilli)** - టైప్ చేయండి: "మిరప" లేదా "chilli"
   → 6 పురుగులు, 5 వ్యాధులు, 6 సేంద్రియ స్ప్రేలు

🍅 **4. టమోటా (Tomato)** - టైప్ చేయండి: "టమోటా" లేదా "tomato"
   → 6 పురుగులు, 6 వ్యాధులు, 6 సేంద్రియ ఎంపికలు

💡 **ఉదాహరణకు:**
"మిరప" లేదా "chilli" టైప్ చేసి 15+ సూచనలను పొందండి!

🆘 **సహాయం కోసం:** "help" లేదా "menu" టైప్ చేయండి

🌾 రైతుమిత్ర - మీ పంటకు పూర్తి సహాయకుడు!
══════════════════════════════════════════════"""
    
    # Save to database
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO farmer_queries (phone_number, query, response) VALUES (?, ?, ?)",
            (query.phone_number, query.message, response)
        )
        conn.commit()
        conn.close()
    except:
        pass  # Skip database errors for Vercel deployment
    
    return {
        "success": True,
        "message": response,
        "timestamp": datetime.now().isoformat()
    }

# Get crops API
@app.get("/api/crops")
async def get_crops():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crops")
    crops = cursor.fetchall()
    conn.close()
    return {"crops": [dict(crop) for crop in crops]}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RythuMitra", "version": "2.0.0"}

# For Vercel serverless
app_handler = app

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)