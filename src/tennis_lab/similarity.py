"""Vecinos descriptivos en métricas estandarizadas; no estima efecto táctico."""
from math import sqrt
from statistics import mean, pstdev


def neighbors(profiles, features, minimum_matches=10, limit=5):
    eligible = {key: metrics for key, metrics in profiles.items()
                if all(feature in metrics and metrics[feature]["matches"] >= minimum_matches
                       and metrics[feature]["denominator"] > 0 for feature in features)}
    centers = {feature: mean(metrics[feature]["rate"] for metrics in eligible.values()) for feature in features} if eligible else {}
    scales = {feature: pstdev(metrics[feature]["rate"] for metrics in eligible.values()) for feature in features} if eligible else {}
    active = [feature for feature in features if scales.get(feature, 0) > 0]
    result = {}
    for key, metrics in eligible.items():
        candidates = []
        if active:
            for other, comparison in eligible.items():
                if other == key:
                    continue
                differences = {feature: abs(metrics[feature]["rate"] - comparison[feature]["rate"]) / scales[feature] for feature in active}
                candidates.append({"player_id": other, "distance": sqrt(mean(value ** 2 for value in differences.values())),
                                   "closest_features": sorted(differences, key=differences.get)[:3],
                                   "largest_difference": max(differences, key=differences.get),
                                   "minimum_metric_matches": min(comparison[feature]["matches"] for feature in features)})
        result[key] = sorted(candidates, key=lambda item: (item["distance"], item["player_id"]))[:limit]
    return {"eligible_players": len(eligible), "features": active, "mean": centers, "standard_deviation": scales,
            "minimum_matches_policy": minimum_matches, "neighbors": result}
