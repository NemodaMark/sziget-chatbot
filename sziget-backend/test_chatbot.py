# tesztesetek Daninak
#
#Nem vagy köteles ezzel a fájllal gyártani a teszteseteket, de használhatod meg átnézheted hogy kb mire van szükség
#
# Futtatás:
#   python test_chatbot.py
#
# A tesztek lefedik:
#   - Pontos egyezések (a tudásbázisban szereplő kérdések)
#   - Parafrazeált / más szavakkal megfogalmazott kérdések
#   - Tematikusan közel eső, de nem szó szerinti kérdések
#   - Fallback esetek (irreleváns / értelmetlen input)
#   - Üres input kezelése

import sys
from chatbot_engine import SzigetChatbot

# ============================================================
# Tesztesetek definíciója
# ============================================================

TEST_CASES = [
    # (bemeneti kérdés, elvárt intent, leírás)

    # --- festival_info ---
    ("Mikor van a Sziget 2026-ban?",          "festival_info",   "Dátum kérdés"),
    ("Hol rendezik meg a Szigetet?",           "festival_info",   "Helyszín kérdés"),
    ("Hány napig tart a fesztivál?",           "festival_info",   "Időtartam kérdés"),
    ("Hogyan jutok ki a Szigetre?",            "festival_info",   "Közlekedés kérdés"),

    # --- pricing ---
    ("Mennyibe kerül a belépő?",               "pricing",         "Jegyár kérdés"),
    ("Lehet olcsóbban jegyet venni?",          "pricing",         "Kedvezmény kérdés"),
    ("Kártyával lehet fizetni a fesztiválon?", "pricing",         "Fizetési mód"),
    ("Drágák az ételek a Szigeten?",           "pricing",         "Árak belül"),

    # --- camping ---
    ("Milyen a sátorozási lehetőség?",         "camping",         "Kemping általános"),
    ("Van fürdési lehetőség a kempingben?",    "camping",         "Zuhany kérdés"),
    ("Mennyire zsúfolt a kemping?",            "camping",         "Zsúfoltság"),

    # --- rules ---
    ("Mit nem vihetek be magammal?",           "rules",           "Tiltott tárgyak"),
    ("Van biztonsági ellenőrzés?",             "rules",           "Beléptetés"),
    ("Mennyire biztonságos a fesztivál?",      "rules",           "Biztonság"),

    # --- lineup_schedule ---
    ("Kik lesznek a fellépők?",                "lineup_schedule", "Lineup kérdés"),
    ("Lesz-e magyar zenész a Szigeten?",       "lineup_schedule", "Magyar fellépő"),
    ("Milyen zenei stílusok lesznek?",         "lineup_schedule", "Stílusok"),
    ("Hol nézhetem meg a menetrendet?",        "lineup_schedule", "Program forrás"),

    # --- programs ---
    ("Mit lehet csinálni napközben?",          "programs",        "Nappali programok"),
    ("Vannak-e workshopok?",                   "programs",        "Workshopok"),
    ("Milyen szórakozási lehetőség van?",      "programs",        "Szórakozás általános"),

    # --- general ---
    ("Érdemes elmenni a Szigetre?",            "general",         "Ajánlás kérdés"),
    ("Sokan vannak ott?",                      "general",         "Teltség kérdés"),

    # --- fallback esetek ---
    ("Mi a GDP növekedése Magyarországon?",    "unknown",         "Irreleváns kérdés"),
    ("Mikor volt az első holdra szállás?",     "unknown",         "Teljesen off-topic"),
    ("",                                       "unknown",         "Üres input"),
    ("asdfjkl qwerty zxcvbn",                  "unknown",         "Értelmetlen szöveg"),
]

# ============================================================
# Teszt futtató
# ============================================================

def run_tests(threshold: float = 0.15, verbose: bool = True) -> dict:
    bot = SzigetChatbot(threshold=threshold)

    passed   = 0
    failed   = 0
    results  = []

    print("=" * 70)
    print("  SZIGET CHATBOT – Automatizált tesztek")
    print(f"  Tesztesetek száma: {len(TEST_CASES)}  |  Threshold: {threshold}")
    print("=" * 70)

    for i, (question, expected_intent, description) in enumerate(TEST_CASES, 1):
        result = bot.get_response(question)
        actual_intent = result["intent"]
        ok = actual_intent == expected_intent

        if ok:
            passed += 1
            status = "✅ OK    "
        else:
            failed += 1
            status = "❌ FAIL  "

        entry = {
            "id":          i,
            "description": description,
            "question":    question,
            "expected":    expected_intent,
            "actual":      actual_intent,
            "confidence":  result["confidence"],
            "answer":      result["answer"],
            "passed":      ok,
        }
        results.append(entry)

        if verbose:
            print(f"\n[{i:02d}] {status} | {description}")
            print(f"     Kérdés    : {question!r}")
            print(f"     Elvárt    : {expected_intent}")
            print(f"     Kapott    : {actual_intent}  (conf: {result['confidence']:.3f})")
            print(f"     Válasz    : {result['answer'][:80]}{'...' if len(result['answer']) > 80 else ''}")
            if not ok:
                print(f"     ⚠️  Egyezés : {result['matched_q']!r}")

    # Összesítés
    accuracy = passed / len(TEST_CASES) * 100
    print("\n" + "=" * 70)
    print(f"  Eredmény: {passed}/{len(TEST_CASES)} helyes  |  Pontosság: {accuracy:.1f}%")
    print("=" * 70)

    # Intent-szintű összesítés
    print("\n📊 Intent-szintű eredmények:")
    intent_stats = {}
    for r in results:
        key = r["expected"]
        if key not in intent_stats:
            intent_stats[key] = {"total": 0, "passed": 0}
        intent_stats[key]["total"] += 1
        if r["passed"]:
            intent_stats[key]["passed"] += 1

    for intent, stats in sorted(intent_stats.items()):
        pct = stats["passed"] / stats["total"] * 100
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        print(f"  {intent:<20s} [{bar}] {stats['passed']}/{stats['total']}  ({pct:.0f}%)")

    return {
        "passed":   passed,
        "failed":   failed,
        "total":    len(TEST_CASES),
        "accuracy": accuracy,
        "details":  results,
    }


if __name__ == "__main__":
    verbose = "--quiet" not in sys.argv
    run_tests(threshold=0.15, verbose=verbose)
