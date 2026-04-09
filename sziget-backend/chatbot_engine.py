# NLP motor
# Módszer: TF-IDF vektorizálás + koszinusz-hasonlóság (intent-alapú visszakeresés)
# Működési logika:
#   1. A tudásbázis kérdéseit TF-IDF vektorokká alakítjuk
#   2. A felhasználói kérdést szintén vektorizáljuk
#   3. Koszinusz-hasonlósággal megkeressük a legközelebbi kérdést
#   4. Ha a hasonlóság elég magas (threshold), visszaadjuk a hozzá tartozó választ
#   5. Ha nem találunk elég jó egyezést, fallback választ adunk

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from knowledge_base import data


# 1. Szöveg-normalizálás (Barni preprocesszora alapján, kiegészítve)

def normalize(text: str) -> str:
    """Kisbetűsítés, URL/szám maszkolás, domain-specifikus szótövesítés."""
    t = text.lower().strip()

    t = re.sub(r"https?://\S+|www\.\S+", "<url>", t)
    t = re.sub(r"\d+", "<num>", t)

    t = re.sub(r"szigeten|szigetre|szigetnek|szigetről", "sziget", t)
    t = re.sub(r"fesztiválon|fesztiválra|fesztiválnak|fesztiválról|fesztiválnál", "fesztival", t)
    t = re.sub(r"jegyek|jegyár|jegyárak|belépő|bérlet", "jegy", t)
    t = re.sub(r"árak|ára|árát|áron|kerül|kerülnek", "ar", t)
    t = re.sub(r"fellépők|előadók|fellépő|előadó|zenész|zenészek|artist", "lineup", t)
    t = re.sub(r"sátor|sátrazás|sátorzás", "kemping", t)
    t = re.sub(r"kártyával|kártyás|kártya", "kartya", t)
    t = re.sub(r"készpénz|készpénzzel", "keszpenz", t)
    t = re.sub(r"kaját|kajával|kaja|étel|ételeket|ennivaló|enni", "kaja", t)
    t = re.sub(r"internet|wifi|net", "wifi", t)
    t = re.sub(r"lessz", "lesz", t)
    t = re.sub(r"biztonság(os|i|ot)?", "biztonsag", t)
    t = re.sub(r"program(ok|okat|okra)?|szórakoz(ás|ni|ási)", "program", t)
    t = re.sub(r"koncert(ek|re|en)?", "koncert", t)
    t = re.sub(r"mikor|mettől|mikortól|időpont|dátum", "mikor", t)
    t = re.sub(r"hol|helyszín|helyen|helyszínen|hova|megrendez", "hol", t)
    t = re.sub(r"mennyi(re|be|t)?|drága|olcsó|kedvezmény", "ar", t)
    t = re.sub(r"sokan|zsúfolt|telt|tele|tömeg", "zsufolt", t)
    t = re.sub(r"workshop(ok|on|ra)?|kreatív|foglalkoz", "workshop", t)
    t = re.sub(r"érdemes|megéri|ajánl|érdemi|javasol", "erdemes", t)
    t = re.sub(r"jutok ki|kijutni|közlekedés|tömegközlekedés|eljutni", "kozlekedes", t)

    t = re.sub(r"[^a-záéíóöőúüű<>\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

# 2. Chatbot osztály

class SzigetChatbot:
    """
    TF-IDF + koszinusz-hasonlóság alapú chatbot.

    Attribútumok:
        vectorizer  – TfidfVectorizer, a tudásbázis kérdéseire illesztve
        kb_vectors  – a tudásbázis TF-IDF mátrixa (n_questions × n_features)
        questions   – eredeti kérdések listája
        answers     – hozzájuk tartozó válaszok listája
        intents     – intent-címkék listája
        threshold   – minimális koszinusz-hasonlóság, ami alatt fallback-et adunk
    """

    FALLBACK_RESPONSES = [
        "Hmm, ezt nem egészen értem. 🤔 Kérdezhetsz a jegyárakról, a kempingről, "
        "a fellépőkről, a programokról vagy a szabályokról!",
        "Ezt nem tudom biztosan. Próbálj meg más szavakkal kérdezni, "
        "vagy nézd meg a szigetfestival.com oldalt!",
        "Sajnos erre nincs pontos válaszom. Mit szeretnél tudni a Szigetről? "
        "(pl. árak, kemping, lineup, programok...)",
    ]

    def __init__(self, threshold: float = 0.15):
        self.threshold = threshold
        self._build_index()

    def _build_index(self):
        """TF-IDF mátrix felépítése a tudásbázisból."""
        self.questions = [q for q, _, _ in data]
        self.intents   = [i for _, i, _ in data]
        self.answers   = [a for _, _, a in data]

        self.vectorizer = TfidfVectorizer(
            preprocessor=normalize,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
        )
        self.kb_vectors = self.vectorizer.fit_transform(self.questions)

    def get_response(self, user_input: str) -> dict:
        """
        Visszaadja a legjobb választ a felhasználói kérdésre.

        Returns:
            dict {
                "answer":     str  – a válasz szövege,
                "intent":     str  – felismert intent,
                "confidence": float – koszinusz-hasonlóság (0–1),
                "matched_q":  str  – a legközelebbi tudásbázis-kérdés,
                "fallback":   bool – True, ha nem találtunk elég jó egyezést
            }
        """
        if not user_input.strip():
            return self._fallback()

        user_vec = self.vectorizer.transform([user_input])
        scores   = cosine_similarity(user_vec, self.kb_vectors)[0]
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        if best_score < self.threshold:
            result = self._fallback()
            result["confidence"] = best_score
            return result

        return {
            "answer":     self.answers[best_idx],
            "intent":     self.intents[best_idx],
            "confidence": round(best_score, 4),
            "matched_q":  self.questions[best_idx],
            "fallback":   False,
        }

    def _fallback(self) -> dict:
        import random
        return {
            "answer":     random.choice(self.FALLBACK_RESPONSES),
            "intent":     "unknown",
            "confidence": 0.0,
            "matched_q":  "",
            "fallback":   True,
        }

    def get_intents(self) -> list:
        """Az összes egyedi intent listája."""
        return sorted(set(self.intents))

    def get_questions_by_intent(self, intent: str) -> list:
        """Visszaadja az adott intenthez tartozó kérdéseket."""
        return [q for q, i, _ in data if i == intent]

# 3. Gyors teszt – közvetlen futtatáshoz

if __name__ == "__main__":
    bot = SzigetChatbot(threshold=0.15)

    test_inputs = [
        "Mikor van a Sziget idén?",
        "Mennyibe kerül a jegy?",
        "Van kemping a fesztiválon?",
        "Kik lépnek fel 2026-ban?",
        "Be lehet vinni kaját?",
        "Milyen programok vannak napközben?",
        "Biztonságos a fesztivál?",
        "Ott lesz Peggy Gou?",
        "Mi a helyzet a wc-kkel?",
        "Ezt nem értem egyáltalán",
        "",                             
    ]

    print("=" * 65)
    print("  SZIGET CHATBOT – Motor teszt")
    print("=" * 65)

    for q in test_inputs:
        result = bot.get_response(q)
        print(f"\n❓ Kérdés   : {q!r}")
        print(f"🎯 Intent   : {result['intent']}  (conf: {result['confidence']:.3f})")
        if result["matched_q"]:
            print(f"🔍 Egyezés  : {result['matched_q']!r}")
        print(f"💬 Válasz   : {result['answer'][:100]}{'...' if len(result['answer']) > 100 else ''}")
        if result["fallback"]:
            print("   ⚠️  [FALLBACK]")
