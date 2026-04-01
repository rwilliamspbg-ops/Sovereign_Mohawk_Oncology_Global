from math import sqrt
from typing import Dict, List, Sequence, Set


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(a: Sequence[float]) -> float:
    return sqrt(sum(x * x for x in a))


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    na = _norm(a)
    nb = _norm(b)
    if na == 0 or nb == 0:
        return -1.0
    return _dot(a, b) / (na * nb)


def euclidean_distance(a: Sequence[float], b: Sequence[float]) -> float:
    return sqrt(sum((x - y) * (x - y) for x, y in zip(a, b)))


def _vector_mean(vectors: List[List[float]]) -> List[float]:
    if not vectors:
        return []
    dims = len(vectors[0])
    mean = [0.0] * dims
    for v in vectors:
        for i in range(dims):
            mean[i] += v[i]
    return [x / len(vectors) for x in mean]


def detect_poisoned_clients(
    client_vectors: Dict[str, List[float]],
    min_cosine_similarity: float,
    max_krum_score: float,
) -> Set[str]:
    """Detect poisoned clients using cosine and Krum-style distance scores.

    Krum-style score here is a lightweight approximation: sum of distances to
    the closest n-2 vectors for each client update.
    """
    if len(client_vectors) < 3:
        return set()

    clients = list(client_vectors.keys())
    vectors = [client_vectors[c] for c in clients]
    dims = {len(v) for v in vectors}
    if len(dims) != 1:
        return set(clients)

    centroid = _vector_mean(vectors)
    poisoned: Set[str] = set()

    for client_id, vector in client_vectors.items():
        cos = cosine_similarity(vector, centroid)
        if cos < min_cosine_similarity:
            poisoned.add(client_id)
            continue

        distances = []
        for other_id, other_vec in client_vectors.items():
            if other_id == client_id:
                continue
            distances.append(euclidean_distance(vector, other_vec))
        distances.sort()

        neighbors = max(1, len(distances) - 1)
        krum_score = sum(distances[:neighbors])
        if krum_score > max_krum_score:
            poisoned.add(client_id)

    return poisoned
