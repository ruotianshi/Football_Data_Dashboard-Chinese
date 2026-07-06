import pandas as pd


def extract_match_side_info(match_row, side: str) -> dict:
    team_col = f"{side}_team"
    team_name_col = f"{side}_team_name"
    team_id_col = f"{side}_team_id"

    name = match_row.get(team_name_col, "")
    team_id = match_row.get(team_id_col)

    team_val = match_row.get(team_col, {})
    if isinstance(team_val, dict):
        if _is_blank(name):
            name = _first_non_empty(team_val, [team_name_col, "name", "team_name"])
        if _is_missing(team_id):
            team_id = _first_non_empty(team_val, [team_id_col, "id", "team_id"])
    elif isinstance(team_val, str) and _is_blank(name):
        name = team_val

    return {
        "name": str(name or "").strip(),
        "id": _coerce_int(team_id),
    }


def _first_non_empty(values: dict, keys: list[str]):
    for key in keys:
        if key not in values:
            continue
        value = values.get(key)
        if _is_missing(value) or _is_blank(value):
            continue
        return value
    return None


def _coerce_int(value):
    try:
        return int(value) if not _is_missing(value) else None
    except (TypeError, ValueError):
        return None


def _is_missing(value) -> bool:
    return value is None or (isinstance(value, float) and pd.isna(value))


def _is_blank(value) -> bool:
    return isinstance(value, str) and not value.strip()
