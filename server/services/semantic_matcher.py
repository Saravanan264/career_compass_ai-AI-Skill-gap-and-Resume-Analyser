import os
import re
import math
from collections import Counter
from typing import Dict, Any, Tuple

# Force PyTorch backend for sentence_transformers
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

# Reusable model singleton holder
_SENTENCE_MODEL = None
_MODEL_LOADED = False
_MODEL_ERROR = None

def get_sentence_model():
    """
    Singleton lazy-loader for sentence-transformers model.
    Falls back gracefully if library or model weights are unavailable.
    """
    global _SENTENCE_MODEL, _MODEL_LOADED, _MODEL_ERROR
    if _MODEL_LOADED:
        return _SENTENCE_MODEL

    try:
        # pyrefly: ignore [missing-import]
        from sentence_transformers import SentenceTransformer
        _SENTENCE_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        _MODEL_LOADED = True
        print("[INFO] sentence-transformers model (all-MiniLM-L6-v2) loaded successfully.")
    except Exception as e:
        _MODEL_LOADED = True
        _MODEL_ERROR = str(e)
        _SENTENCE_MODEL = None
        print(f"[INFO] sentence-transformers model unavailable ({e}). Using lightweight TF-IDF Vector Cosine Fallback.")

    return _SENTENCE_MODEL


def preprocess_text_for_embedding(text: str) -> str:
    """
    Clean text for embedding/similarity while preserving technical symbols
    (C++, C#, .NET, Node.js, React.js, CI/CD, REST API).
    """
    if not text:
        return ""
    # Normalize consecutive spaces & line breaks
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Remove excessive punctuation except + # . - /
    text = re.sub(r'[^\w\s+#./-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    """
    Extract meaningful word tokens and technical terms from preprocessed text.
    """
    cleaned = preprocess_text_for_embedding(text).lower()
    # Match words including symbols like c++, c#, .net, ci/cd, react.js
    tokens = re.findall(r'\b[a-z0-9+#./-]+\b|[a-z0-9]+', cleaned)
    # Filter out tiny 1-char stop-words except 'c' and 'r'
    stopwords = {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "by", "of", "is", "are", "was", "were", "be", "been", "has", "have", "had", "this", "that", "it", "as"}
    return [t for t in tokens if t not in stopwords and (len(t) > 1 or t in {"c", "r"})]


def compute_tf_idf_cosine_similarity(text1: str, text2: str) -> float:
    """
    Lightweight TF-IDF / Sub-word n-gram vector cosine similarity implementation.
    Operates 100% offline with zero external dependencies.
    """
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)

    if not tokens1 or not tokens2:
        return 0.0

    # Build unigram & bigram counts
    bigrams1 = [f"{tokens1[i]}_{tokens1[i+1]}" for i in range(len(tokens1)-1)]
    bigrams2 = [f"{tokens2[i]}_{tokens2[i+1]}" for i in range(len(tokens2)-1)]

    freq1 = Counter(tokens1 + bigrams1)
    freq2 = Counter(tokens2 + bigrams2)

    # Vocabulary space
    vocabulary = set(freq1.keys()).union(set(freq2.keys()))
    if not vocabulary:
        return 0.0

    # Vector representations
    vec1 = []
    vec2 = []

    for word in vocabulary:
        # Inverse Document Frequency weighting approximation
        df = (1 if word in freq1 else 0) + (1 if word in freq2 else 0)
        idf = math.log((2.0 + 1.0) / (df + 1.0)) + 1.0
        vec1.append(freq1[word] * idf)
        vec2.append(freq2[word] * idf)

    # Compute dot product and magnitudes
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    cosine_sim = dot_product / (mag1 * mag2)
    # Scale & bound to [0, 100]
    return round(min(100.0, max(0.0, cosine_sim * 100.0)), 1)


def compute_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """
    Computes semantic similarity score (0.0 to 100.0) between resume and JD text.
    Uses sentence-transformers model if loaded; otherwise uses lightweight vector TF-IDF cosine.
    """
    model = get_sentence_model()

    if model is not None:
        try:
            # pyrefly: ignore [missing-import]
            from sentence_transformers import util
            clean_res = preprocess_text_for_embedding(resume_text)
            clean_jd = preprocess_text_for_embedding(jd_text)
            emb_res = model.encode(clean_res, convert_to_tensor=True)
            emb_jd = model.encode(clean_jd, convert_to_tensor=True)
            sim = util.cos_sim(emb_res, emb_jd).item()
            return round(min(100.0, max(0.0, sim * 100.0)), 1)
        except Exception as e:
            print(f"[WARN] Error executing sentence-transformers model ({e}). Falling back to TF-IDF vector cosine.")

    return compute_tf_idf_cosine_similarity(resume_text, jd_text)


def compute_hybrid_match(
    rule_based_score: float,
    resume_text: str,
    jd_text: str,
    rule_weight: float = 0.60,
    semantic_weight: float = 0.40
) -> Dict[str, Any]:
    """
    Computes hybrid match score combining rule-based heuristic match score
    and semantic similarity score.
    """
    semantic_score = compute_semantic_similarity(resume_text, jd_text)

    # Weighted combination
    hybrid_score = round(
        (rule_based_score * rule_weight) + (semantic_score * semantic_weight),
        1
    )

    return {
        "rule_based_match_score": round(rule_based_score, 1),
        "semantic_similarity_score": semantic_score,
        "hybrid_match_score": hybrid_score,
        "weights": {
            "rule_weight": rule_weight,
            "semantic_weight": semantic_weight
        },
        "engine": "SentenceTransformers (all-MiniLM-L6-v2)" if _SENTENCE_MODEL is not None else "TF-IDF Vector Cosine (Hybrid)"
    }
