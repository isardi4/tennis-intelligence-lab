"""Componentes observables de perfiles; no asigna etiquetas tácticas ni probabilidades."""
from tennis_lab.ingestion.quality import match_issues, number


def profile_observations(row: dict[str, str], side: str) -> dict[str, tuple[float, float]]:
    """Numerador/denominador: agregarlos antes de dividir evita promediar porcentajes.

    El llamador debe filtrar fechas, identidades y discrepancias entre proveedores.
    Un registro inválido se excluye conservadoramente para ambos jugadores.
    """
    if side not in ("w", "l"):
        raise ValueError("side debe ser w o l")
    score = row.get("score", "").upper()
    if not score.strip() or any(marker in score for marker in ("W/O", "RET", "DEF", "ABN", "WALK")):
        return {}
    if match_issues(row):
        return {}
    opponent = "l" if side == "w" else "w"
    own = lambda suffix: number(row.get(f"{side}_{suffix}"))
    other = lambda suffix: number(row.get(f"{opponent}_{suffix}"))
    result = {}

    def add(name, numerator, denominator):
        if numerator is not None and denominator is not None and denominator > 0 and 0 <= numerator <= denominator:
            result[name] = numerator, denominator

    add("ace_rate", own("ace"), own("svpt"))
    add("double_fault_rate", own("df"), own("svpt"))
    add("first_serve_in_rate", own("1stIn"), own("svpt"))
    add("first_serve_points_won", own("1stWon"), own("1stIn"))
    if own("svpt") is not None and own("1stIn") is not None:
        add("second_serve_points_won", own("2ndWon"), own("svpt") - own("1stIn"))
    if own("1stWon") is not None and own("2ndWon") is not None:
        add("serve_points_won", own("1stWon") + own("2ndWon"), own("svpt"))
    if other("1stIn") is not None and other("1stWon") is not None:
        add("first_serve_return_points_won", other("1stIn") - other("1stWon"), other("1stIn"))
    if other("svpt") is not None and other("1stIn") is not None and other("2ndWon") is not None:
        second = other("svpt") - other("1stIn")
        add("second_serve_return_points_won", second - other("2ndWon"), second)
    if other("svpt") is not None and other("1stWon") is not None and other("2ndWon") is not None:
        add("return_points_won", other("svpt") - other("1stWon") - other("2ndWon"), other("svpt"))
    return result
