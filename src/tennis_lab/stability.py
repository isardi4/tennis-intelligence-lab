"""Retención de vecinos con la misma población elegible en ambas ventanas."""
from statistics import median
from tennis_lab.similarity import neighbors


def compare_windows(original, perturbed, features):
    def sufficient(metrics):
        return all(key in metrics and metrics[key]["matches"] >= 10 and metrics[key]["denominator"] > 0 for key in features)
    common = {key for key in original.keys() & perturbed.keys() if sufficient(original[key]) and sufficient(perturbed[key])}
    if len(common) < 6:
        return {"comparable_players": len(common), "status": "insufficient_population", "players": {}}
    first = neighbors({key: original[key] for key in common}, features)
    second = neighbors({key: perturbed[key] for key in common}, features)
    rows = {}
    for key in sorted(common):
        left = {row["player_id"] for row in first["neighbors"][key]}
        right = {row["player_id"] for row in second["neighbors"][key]}
        if len(left) == len(right) == 5:
            rows[key] = {"retained_of_five": len(left & right)}
    return {"comparable_players": len(common), "status": "compared" if rows else "no_informative_features",
            "players": rows, "median_retained": median(row["retained_of_five"] for row in rows.values()) if rows else None,
            "retaining_at_least_three": sum(row["retained_of_five"] >= 3 for row in rows.values())}
