import random
import re
from collections import Counter

from knowledge_base import data


def normalize(text: str) -> str:
    """Egyszeru domain-specifikus normalizalas magyar kerdesekhez."""
    t = text.lower().strip()

    replacements = [
        (r"https?://\S+|www\.\S+", " url "),
        (r"\d+", " num "),
        (r"szigeten|szigetre|szigetnek|szigetr[oó]l", " sziget "),
        (r"fesztiv[aá]lon|fesztiv[aá]lra|fesztiv[aá]lnak|fesztiv[aá]lr[oó]l|fesztiv[aá]ln[aá]l", " fesztival "),
        (r"jegyek|jegy[aá]r|jegy[aá]rak|bel[eé]p[oő]|b[eé]rlet", " jegy "),
        (r"[aá]rak|[aá]ra|[aá]r[aá]t|[aá]ron|ker[uü]l|ker[uü]lnek", " ar "),
        (r"fell[eé]p[oő]k|el[oő]ad[oó]k|fell[eé]p[oő]|el[oő]ad[oó]|zen[eé]sz|zen[eé]szek|artist", " lineup "),
        (r"s[aá]tor|s[aá]traz[aá]s|s[aá]torz[aá]s", " kemping "),
        (r"k[aá]rty[aá]val|k[aá]rty[aá]s|k[aá]rtya", " kartya "),
        (r"k[eé]szp[eé]nz|k[eé]szp[eé]nzzel", " keszpenz "),
        (r"kaj[aá]t|kaj[aá]val|kaja|[ée]tel|[ée]teleket|ennival[oó]|enni", " kaja "),
        (r"internet|wifi|net", " wifi "),
        (r"lessz", " lesz "),
        (r"biztons[aá]g(os|i|ot)?", " biztonsag "),
        (r"program(ok|okat|okra)?|sz[oó]rakoz([aá]s|ni|[aá]si)", " program "),
        (r"koncert(ek|re|en)?", " koncert "),
        (r"mikor|mett[oő]l|mikort[oó]l|id[oő]pont|d[aá]tum|menetrend|program.*rend", " mikor "),
        (r"hol|helysz[ií]n|helyen|helysz[ií]nen|hova|megrendez|rendezik", " hol "),
        (r"mennyi(re|be|t)?|dr[aá]ga|olcs[oó]|kedvezm[eé]ny", " ar "),
        (r"sokan|zs[uú]folt|telt|tele|t[oö]meg", " zsufolt "),
        (r"workshop(ok|on|ra)?|kreat[ií]v|foglalkoz", " workshop "),
        (r"[ée]rdemes|meg[eé]ri|aj[aá]nl|[ée]rdemi|javasol", " erdemes "),
        (r"jutok ki|kijutni|k[oö]zleked[eé]s|t[oö]megk[oö]zleked[eé]s|eljutni", " kozlekedes "),
    ]

    for pattern, replacement in replacements:
        t = re.sub(pattern, replacement, t)

    t = re.sub(r"[^a-z0-9a-záéíóöőúüű<>\s]", " ", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def tokenize(text: str) -> list[str]:
    return [token for token in normalize(text).split(" ") if token]


def ngrams(tokens: list[str], size: int) -> list[str]:
    if len(tokens) < size:
        return []
    return [" ".join(tokens[i:i + size]) for i in range(len(tokens) - size + 1)]


def weighted_similarity(left: str, right: str) -> float:
    """Sajat, dependency-mentes hasonlosag TF-IDF helyett.

    A pontszam a token-egyezes, 2-gram egyezes es reszleges fedes kombinalasa.
    """
    left_tokens = tokenize(left)
    right_tokens = tokenize(right)

    if not left_tokens or not right_tokens:
        return 0.0

    left_set = set(left_tokens)
    right_set = set(right_tokens)
    token_overlap = len(left_set & right_set) / max(len(left_set | right_set), 1)

    left_bigrams = set(ngrams(left_tokens, 2))
    right_bigrams = set(ngrams(right_tokens, 2))
    if left_bigrams or right_bigrams:
        bigram_overlap = len(left_bigrams & right_bigrams) / max(len(left_bigrams | right_bigrams), 1)
    else:
        bigram_overlap = 0.0

    left_counts = Counter(left_tokens)
    right_counts = Counter(right_tokens)
    common_weight = sum(min(left_counts[token], right_counts[token]) for token in (left_counts.keys() & right_counts.keys()))
    length_weight = common_weight / max(len(left_tokens), len(right_tokens), 1)

    return round((token_overlap * 0.5) + (bigram_overlap * 0.25) + (length_weight * 0.25), 4)


class SzigetChatbot:
    FALLBACK_RESPONSES = [
        "Hmm, ezt nem teljesen ertem. Kerdezhetsz jegyekrol, lineuprol, campingrol, programokrol vagy szabalyokrol is.",
        "Erre most nincs biztos valaszom. Probald meg mashogy megfogalmazni, vagy kerdezz ra egy konkret Sziget-temara.",
        "Ezt most nem talaltam el eleg pontosan. Jo irany lehet peldaul a jegy, a lineup, a kemping vagy a programok temaja.",
    ]

    def __init__(self, threshold: float = 0.15):
        self.threshold = threshold
        self.questions = [q for q, _, _ in data]
        self.intents = [i for _, i, _ in data]
        self.answers = [a for _, _, a in data]

    def get_response(self, user_input: str) -> dict:
        if not user_input.strip():
            return self._fallback()

        best_index = -1
        best_score = 0.0

        for index, question in enumerate(self.questions):
            score = weighted_similarity(user_input, question)
            if score > best_score:
                best_score = score
                best_index = index

        if best_index == -1 or best_score < self.threshold:
            result = self._fallback()
            result["confidence"] = best_score
            return result

        return {
            "answer": self.answers[best_index],
            "intent": self.intents[best_index],
            "confidence": round(best_score, 4),
            "matched_q": self.questions[best_index],
            "fallback": False,
        }

    def _fallback(self) -> dict:
        return {
            "answer": random.choice(self.FALLBACK_RESPONSES),
            "intent": "unknown",
            "confidence": 0.0,
            "matched_q": "",
            "fallback": True,
        }

    def get_intents(self) -> list:
        return sorted(set(self.intents))

    def get_questions_by_intent(self, intent: str) -> list:
        return [q for q, i, _ in data if i == intent]


if __name__ == "__main__":
    bot = SzigetChatbot(threshold=0.15)
    samples = [
        "Mikor van a Sziget iden?",
        "Mennyibe kerul a jegy?",
        "Van kemping a fesztivalon?",
        "Kik lepnek fel 2026-ban?",
        "Be lehet vinni kajat?",
        "Milyen programok vannak napkozben?",
    ]

    for sample in samples:
        result = bot.get_response(sample)
        print(f"K: {sample}")
        print(f"V: {result['answer']}")
        print(f"Intent: {result['intent']} | score: {result['confidence']}")
        print("-" * 50)
