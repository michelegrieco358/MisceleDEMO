import streamlit as st
import pandas as pd
from copy import deepcopy

st.set_page_config(page_title="Gestione Miscele - Configurazione", layout="wide")


destination_tanks_default = [
    {"selected": True,  "tank": "TK-125", "cod_range": "44000-48000", "solvents": 800, "v_min": 40, "v_max": 100},
    {"selected": True,  "tank": "TK-126", "cod_range": "43000-47000", "solvents": 750, "v_min": 20, "v_max": 100},
    {"selected": False, "tank": "TK-127", "cod_range": "45000-49000", "solvents": 850, "v_min": 0,  "v_max": 30},
]

TOP_TRANSFER_FIELDS = {
    "TK-125": "transfer_tk125",
    "TK-126": "transfer_tk126",
    "TK-127": "transfer_tk127",
}

SCENARIO_SCOPE_TOP = "top"
SCENARIO_SCOPE_ALL = "all"
SCENARIO_PRESET_TOP = "scenario_a_top"
SCENARIO_PRESET_SIM_TOP = "scenario_b_sim_top"
SCENARIO_PRESET_ALL = "scenario_c_all"

source_tanks_default = [
    {
        "tank": "S-01", "qty_available": 45, "cod": 52000, "solvents": 780, "boro": 4.2,
        "cl": 120, "n": 18,
        "empty_tank": False, "priority": "", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 45, "transfer_tk125": 45,
        "vol_min": None, "vol_max": None, "notes": ""
    },
    {
        "tank": "S-02", "qty_available": 42, "cod": 86000, "solvents": 1320, "boro": 4.5,
        "cl": 108, "n": 17,
        "empty_tank": False, "priority": "", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 42, "transfer_tk125": 20, "transfer_tk126": 22, "transfer_tk127": 0,
        "vol_min": None, "vol_max": None, "notes": ""
    },
    {
        "tank": "S-03", "qty_available": 35, "cod": 118000, "solvents": 420, "boro": 3.1,
        "cl": 95, "n": 12,
        "empty_tank": False, "priority": "Media", "incompatibility": "S-08",
        "destination_tank": "", "transfer_volume": 0, "transfer_tk125": 0, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": 0, "vol_max": 25, "notes": ""
    },
    {
        "tank": "S-04", "qty_available": 50, "cod": 72000, "solvents": 1600, "boro": 4.8,
        "cl": 110, "n": 15,
        "empty_tank": False, "priority": "Alta", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0, "transfer_tk125": 0, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": 10, "vol_max": 40, "notes": ""
    },
    {
        "tank": "S-05", "qty_available": 38, "cod": 94000, "solvents": 980, "boro": 4.1,
        "cl": 102, "n": 16,
        "empty_tank": True, "priority": "", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0, "transfer_tk125": 0, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": None, "vol_max": None, "notes": "residuo"
    },
    {
        "tank": "S-06", "qty_available": 33, "cod": 59000, "solvents": 640, "boro": 3.4,
        "cl": 92, "n": 13,
        "empty_tank": False, "priority": "Bassa", "incompatibility": "",
        "destination_tank": "TK-126", "transfer_volume": 0, "transfer_tk125": 0, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": None, "vol_max": None, "notes": ""
    },
    {
        "tank": "S-07", "qty_available": 30, "cod": 31000, "solvents": 95, "boro": 2.9,
        "cl": 88, "n": 10,
        "empty_tank": False, "priority": "Bassa", "incompatibility": "",
        "destination_tank": "TK-125", "transfer_volume": 0, "transfer_tk125": 0, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": 0, "vol_max": 20, "notes": ""
    },
    {
        "tank": "S-08", "qty_available": 25, "cod": 146000, "solvents": 5100, "boro": 6.1,
        "cl": 130, "n": 22,
        "empty_tank": True, "priority": "Alta", "incompatibility": "S-03",
        "destination_tank": "", "transfer_volume": 5, "transfer_tk125": 0, "transfer_tk126": 5, "transfer_tk127": 0,
        "vol_min": 15, "vol_max": 25, "notes": ""
    },
    {
        "tank": "S-09", "qty_available": 20, "cod": 68000, "solvents": 1150, "boro": 3.7,
        "cl": 90, "n": 20,
        "empty_tank": False, "priority": "Media", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 5, "transfer_tk125": 5, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": 0, "vol_max": 15, "notes": "rifiuto da dosare"
    },
    {
        "tank": "TK-125 residuo", "qty_available": 5, "cod": 47000, "solvents": 740, "boro": 4.0,
        "cl": None, "n": None,
        "empty_tank": False, "priority": "", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0, "transfer_tk125": 0, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": None, "vol_max": None, "notes": "residuo"
    },
    {
        "tank": "TK-126 residuo", "qty_available": 0, "cod": 45500, "solvents": 720, "boro": 3.8,
        "cl": None, "n": None,
        "empty_tank": False, "priority": "", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0, "transfer_tk125": 0, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": None, "vol_max": None, "notes": "residuo"
    },
    {
        "tank": "TK-127 residuo", "qty_available": 0, "cod": 46800, "solvents": 790, "boro": 3.9,
        "cl": None, "n": None,
        "empty_tank": False, "priority": "", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0, "transfer_tk125": 0, "transfer_tk126": 0, "transfer_tk127": 0,
        "vol_min": None, "vol_max": None, "notes": ""
    },
]


def build_empty_source_tanks():
    empty_rows = []
    for row in source_tanks_default:
        is_residue = "residuo" in str(row["tank"]).lower()
        empty_rows.append(
            {
                "tank": row["tank"],
                "qty_available": None,
                "cod": None,
                "solvents": None,
                "boro": None,
                "cl": None,
                "n": None,
                "empty_tank": False,
                "priority": "",
                "incompatibility": "",
                "destination_tank": "",
                "transfer_volume": None,
                "transfer_tk125": None,
                "transfer_tk126": None,
                "transfer_tk127": None,
                "vol_min": None,
                "vol_max": None,
                "notes": "residuo" if is_residue else "",
            }
        )
    return empty_rows


def build_skysym_partial_source_tanks():
    rows = []
    for row in source_tanks_default:
        is_residue = "residuo" in str(row.get("tank", "")).lower()
        rows.append(
            {
                "tank": row.get("tank", ""),
                "qty_available": row.get("qty_available"),
                "cod": row.get("cod"),
                "solvents": row.get("solvents"),
                "boro": row.get("boro"),
                "cl": None,
                "n": None,
                "empty_tank": False,
                "priority": "",
                "incompatibility": "",
                "destination_tank": "",
                "transfer_volume": None,
                "transfer_tk125": None,
                "transfer_tk126": None,
                "transfer_tk127": None,
                "vol_min": None,
                "vol_max": None,
                "notes": "residuo" if is_residue else "",
            }
        )
    return rows


def apply_skysym_top_fields_on_existing_rows(rows):
    default_by_tank = {
        str(row.get("tank", "")).strip(): row
        for row in source_tanks_default
        if str(row.get("tank", "")).strip()
    }

    updated_rows = []
    for row in rows:
        updated_row = deepcopy(row)
        tank_name = str(updated_row.get("tank", "")).strip()
        default_row = default_by_tank.get(tank_name)
        if default_row:
            updated_row["qty_available"] = default_row.get("qty_available")
            updated_row["cod"] = default_row.get("cod")
            updated_row["solvents"] = default_row.get("solvents")
            updated_row["boro"] = default_row.get("boro")
        updated_rows.append(updated_row)
    return updated_rows


def is_grid_empty_for_refresh(rows):
    if not rows:
        return True
    for row in rows:
        for key in ["qty_available", "cod", "solvents", "boro"]:
            if not is_missing(row.get(key)):
                return False
    return True


def build_simulation_source_tanks():
    sim_rows = deepcopy(source_tanks_default)
    demo_transfer_map = {
        "S-01": 18,
        "S-02": 9,
        "S-03": 12,
        "S-04": 10,
        "S-05": 8,
        "S-06": 5,
        "S-07": 7,
        "S-08": 6,
        "S-09": 4,
        "TK-125 residuo": 5,
        "TK-126 residuo": 0,
        "TK-127 residuo": 0,
    }

    for row in sim_rows:
        tank_name = str(row.get("tank", "")).strip()
        if tank_name in demo_transfer_map:
            row["transfer_volume"] = demo_transfer_map[tank_name]
        row["destination_tank"] = ""

    return sim_rows


def get_next_simulation_tank_name(source_rows):
    used_tanks = {
        str(row.get("tank", "")).strip().upper()
        for row in source_rows
        if str(row.get("tank", "")).strip()
    }
    idx = 1
    while True:
        candidate = f"S-{idx:02d}"
        if candidate.upper() not in used_tanks:
            return candidate
        idx += 1


def build_new_simulation_row(source_rows):
    return {
        "tank": "",
        "qty_available": None,
        "cod": None,
        "solvents": None,
        "boro": None,
        "cl": None,
        "n": None,
        "empty_tank": False,
        "priority": "",
        "incompatibility": "",
        "destination_tank": "",
        "transfer_volume": None,
        "transfer_tk125": None,
        "transfer_tk126": None,
        "transfer_tk127": None,
        "vol_min": None,
        "vol_max": None,
        "notes": "",
    }


def get_active_source_tanks():
    if st.session_state.get("config_mode") == "simulation":
        return st.session_state.simulation_source_tanks
    return st.session_state.source_tanks


def is_missing(value):
    return value is None or pd.isna(value)


def fmt_int_or_dash(value):
    if is_missing(value):
        return "\u2014"
    try:
        return str(int(float(value)))
    except (TypeError, ValueError):
        return "\u2014"


def fmt_float_or_dash(value, decimals=1):
    if is_missing(value):
        return "\u2014"
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return "\u2014"


def fmt_qty_or_dash(value):
    if is_missing(value):
        return "\u2014"
    try:
        return f"{int(float(value))} m3"
    except (TypeError, ValueError):
        return "\u2014"


def safe_info_text(value):
    return "\u2014" if is_missing(value) else str(value)


def safe_int_input(value, default=0):
    if is_missing(value):
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def initialize_state():
    if "plant" not in st.session_state:
        st.session_state.plant = "TOP"
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = "Scenario A"
    if "scenario_counter" not in st.session_state:
        st.session_state.scenario_counter = 1
    if "destination_tanks" not in st.session_state:
        st.session_state.destination_tanks = deepcopy(destination_tanks_default)
    if "source_tanks" not in st.session_state:
        st.session_state.source_tanks = deepcopy(source_tanks_default)
    if "simulation_source_tanks" not in st.session_state:
        st.session_state.simulation_source_tanks = build_simulation_source_tanks()
    if "selected_row_index" not in st.session_state:
        st.session_state.selected_row_index = None
    if "show_edit_dialog" not in st.session_state:
        st.session_state.show_edit_dialog = False
    if "edit_dialog_nonce" not in st.session_state:
        st.session_state.edit_dialog_nonce = 0
    if "show_cod_setting" not in st.session_state:
        st.session_state.show_cod_setting = False
    if "cod_reduction_pct" not in st.session_state:
        st.session_state.cod_reduction_pct = 70
    if "page_mode" not in st.session_state:
        st.session_state.page_mode = "home"
    if "config_mode" not in st.session_state:
        st.session_state.config_mode = "optimization"
    if "scenario_scope" not in st.session_state:
        st.session_state.scenario_scope = SCENARIO_SCOPE_TOP
    if "destination_view_mode" not in st.session_state:
        st.session_state.destination_view_mode = "Serbatoi TOP"
    if "out_recipe_tk125" not in st.session_state:
        st.session_state.out_recipe_tk125 = None
    if "out_recipe_tk126" not in st.session_state:
        st.session_state.out_recipe_tk126 = None
    if "out_recipe_b_tk125" not in st.session_state:
        st.session_state.out_recipe_b_tk125 = None
    if "out_recipe_b_tk126" not in st.session_state:
        st.session_state.out_recipe_b_tk126 = None
    if "show_add_comp_tk125" not in st.session_state:
        st.session_state.show_add_comp_tk125 = False
    if "show_add_comp_tk126" not in st.session_state:
        st.session_state.show_add_comp_tk126 = False
    if "output_compare_scenario" not in st.session_state:
        st.session_state.output_compare_scenario = ""
    if "output_has_scenario_a_plus" not in st.session_state:
        st.session_state.output_has_scenario_a_plus = False
    if "shell_sidebar_open" not in st.session_state:
        st.session_state.shell_sidebar_open = True
initialize_state()


def sync_destination_tanks_from_editor():
    editor_state = st.session_state.get("destination_tanks_editor", {})
    edited_rows = editor_state.get("edited_rows", {})
    for row_idx, changes in edited_rows.items():
        idx = int(row_idx)
        if 0 <= idx < len(st.session_state.destination_tanks):
            for col_name, value in changes.items():
                st.session_state.destination_tanks[idx][col_name] = value
    enforce_destination_tank_rules()


def get_selected_destination_tanks():
    is_simulation_mode = st.session_state.get("config_mode") == "simulation"
    if is_simulation_mode:
        destination_mode = st.session_state.get("destination_view_mode", "Serbatoi TOP")
        if destination_mode == "Serbatoi TOP":
            return ["TK-125", "TK-126"]

        destination_tanks_all = []
        simulation_extra_destinations = ["S-10", "S-11", "S-12"]
        for row in st.session_state.destination_tanks:
            tank_name = str(row.get("tank", "")).strip()
            if tank_name:
                destination_tanks_all.append(tank_name)

        destination_tanks_all.extend(simulation_extra_destinations)

        for row in get_active_source_tanks():
            tank_name = str(row.get("tank", "")).strip()
            if not tank_name:
                continue
            if "residuo" in tank_name.lower():
                continue
            if tank_name.upper().startswith("TK-"):
                destination_tanks_all.append(tank_name)

        return list(dict.fromkeys(destination_tanks_all))

    return [r["tank"] for r in st.session_state.destination_tanks if r.get("selected")]


def enforce_destination_tank_rules():
    allowed_tanks = get_selected_destination_tanks()
    selected_tanks = set(allowed_tanks)
    is_simulation_mode = st.session_state.get("config_mode") == "simulation"
    source_rows = get_active_source_tanks()

    for row_idx, row in enumerate(source_rows):
        raw_destination = row.get("destination_tank", "")
        destination = "" if is_missing(raw_destination) else str(raw_destination).strip()
        if destination and destination not in selected_tanks:
            row["destination_tank"] = ""
            destination = ""

        if not is_simulation_mode:
            for field in TOP_TRANSFER_FIELDS.values():
                if field not in row:
                    row[field] = 0

            # Backward compatibility: migrate legacy destination+volume into dedicated TK columns.
            has_split_transfer = any(safe_int_input(row.get(field), 0) > 0 for field in TOP_TRANSFER_FIELDS.values())
            legacy_volume = safe_int_input(row.get("transfer_volume"), 0)
            if not has_split_transfer and destination in TOP_TRANSFER_FIELDS and legacy_volume > 0:
                row[TOP_TRANSFER_FIELDS[destination]] = legacy_volume

            for tank, field in TOP_TRANSFER_FIELDS.items():
                if tank not in selected_tanks:
                    row[field] = 0

            row["destination_tank"] = destination
            row["transfer_volume"] = sum(safe_int_input(row.get(field), 0) for field in TOP_TRANSFER_FIELDS.values())

        if bool(row.get("empty_tank")):
            row["vol_min"] = None
            row["vol_max"] = None

        is_residue = "residuo" in str(row["tank"]).lower()
        if is_residue:
            row["empty_tank"] = False
            row["priority"] = ""
            if not is_simulation_mode:
                row["destination_tank"] = ""
                continue

        if is_simulation_mode and allowed_tanks:
            transfer_volume = safe_int_input(row.get("transfer_volume"), 0)
            if transfer_volume > 0 and not destination:
                row["destination_tank"] = allowed_tanks[row_idx % len(allowed_tanks)]


def apply_simulation_demo_destinations():
    if st.session_state.get("config_mode") != "simulation":
        return

    allowed_tanks = get_selected_destination_tanks()
    if not allowed_tanks:
        return

    allowed_set = set(allowed_tanks)
    destination_mode = st.session_state.get("destination_view_mode", "Serbatoi TOP")
    top_mode_map = {
        "S-01": "TK-125",
        "S-03": "TK-126",
        "S-04": "TK-125",
        "S-08": "TK-126",
        "TK-125 residuo": "TK-125",
        "TK-127 residuo": "TK-125",
    }
    all_mode_map = {
        "S-01": "TK-125",
        "S-02": "S-10",
        "S-03": "S-11",
        "S-04": "TK-125",
        "S-05": "S-12",
        "S-06": "S-11",
        "S-08": "S-10",
        "S-09": "S-12",
        "TK-125 residuo": "TK-126",
        "TK-127 residuo": "S-11",
    }
    preferred_map = top_mode_map if destination_mode == "Serbatoi TOP" else all_mode_map

    for row_idx, row in enumerate(get_active_source_tanks()):
        transfer_volume = safe_int_input(row.get("transfer_volume"), 0)
        if transfer_volume <= 0:
            continue

        tank_name = str(row.get("tank", "")).strip()
        preferred_destination = preferred_map.get(tank_name, "")
        if preferred_destination in allowed_set:
            row["destination_tank"] = preferred_destination
            continue

        current_destination = str(row.get("destination_tank", "")).strip()
        if not current_destination or current_destination not in allowed_set:
            row["destination_tank"] = allowed_tanks[row_idx % len(allowed_tanks)]


def sync_simulation_destination_mode():
    enforce_destination_tank_rules()
    apply_simulation_demo_destinations()


def apply_scenario_scope(scope: str):
    normalized_scope = scope if scope in {SCENARIO_SCOPE_TOP, SCENARIO_SCOPE_ALL} else SCENARIO_SCOPE_TOP
    st.session_state.scenario_scope = normalized_scope
    if normalized_scope == SCENARIO_SCOPE_ALL:
        st.session_state.destination_view_mode = "Tutti i serbatoi"
        st.session_state.config_mode = "simulation"
    else:
        st.session_state.destination_view_mode = "Serbatoi TOP"
        if st.session_state.get("config_mode") not in {"simulation", "optimization"}:
            st.session_state.config_mode = "optimization"


def create_new_scenario(scope: str):
    st.session_state.scenario_counter += 1
    next_letter = chr(ord("A") + st.session_state.scenario_counter - 1)
    st.session_state.current_scenario = f"Scenario {next_letter}"
    st.session_state.destination_tanks = deepcopy(destination_tanks_default)
    st.session_state.pop("destination_tanks_editor", None)
    st.session_state.source_tanks = build_empty_source_tanks()
    st.session_state.simulation_source_tanks = build_empty_source_tanks()
    st.session_state.selected_row_index = None
    st.session_state.show_edit_dialog = False
    st.session_state.show_cod_setting = False
    st.session_state.cod_reduction_pct = 70
    st.session_state.pop("abbatt_cod_output", None)
    st.session_state.out_recipe_tk125 = None
    st.session_state.out_recipe_tk126 = None
    st.session_state.out_recipe_b_tk125 = None
    st.session_state.out_recipe_b_tk126 = None
    st.session_state.show_add_comp_tk125 = False
    st.session_state.show_add_comp_tk126 = False
    st.session_state.output_compare_scenario = ""
    st.session_state.output_has_scenario_a_plus = False
    apply_scenario_scope(scope)
    if st.session_state.scenario_scope == SCENARIO_SCOPE_TOP:
        st.session_state.config_mode = "optimization"
    st.session_state.page_mode = "config"
    enforce_destination_tank_rules()
    if st.session_state.config_mode == "simulation":
        sync_simulation_destination_mode()


def open_predefined_scenario(preset: str):
    st.session_state.destination_tanks = deepcopy(destination_tanks_default)
    st.session_state.pop("destination_tanks_editor", None)
    st.session_state.source_tanks = deepcopy(source_tanks_default)
    st.session_state.simulation_source_tanks = build_simulation_source_tanks()
    st.session_state.selected_row_index = None
    st.session_state.show_edit_dialog = False
    st.session_state.show_cod_setting = False
    st.session_state.cod_reduction_pct = 70
    st.session_state.pop("abbatt_cod_output", None)
    st.session_state.out_recipe_tk125 = None
    st.session_state.out_recipe_tk126 = None
    st.session_state.out_recipe_b_tk125 = None
    st.session_state.out_recipe_b_tk126 = None
    st.session_state.show_add_comp_tk125 = False
    st.session_state.show_add_comp_tk126 = False
    st.session_state.output_compare_scenario = ""
    st.session_state.output_has_scenario_a_plus = False

    if preset == SCENARIO_PRESET_TOP:
        st.session_state.current_scenario = "Scenario A"
        apply_scenario_scope(SCENARIO_SCOPE_TOP)
        st.session_state.config_mode = "optimization"
        st.session_state.destination_view_mode = "Serbatoi TOP"
        enforce_destination_tank_rules()
    elif preset == SCENARIO_PRESET_SIM_TOP:
        st.session_state.current_scenario = "Scenario B"
        apply_scenario_scope(SCENARIO_SCOPE_TOP)
        st.session_state.config_mode = "simulation"
        st.session_state.destination_view_mode = "Serbatoi TOP"
        sync_simulation_destination_mode()
    else:
        st.session_state.current_scenario = "Scenario C"
        apply_scenario_scope(SCENARIO_SCOPE_ALL)
        st.session_state.config_mode = "simulation"
        st.session_state.destination_view_mode = "Tutti i serbatoi"
        sync_simulation_destination_mode()

    st.session_state.page_mode = "config"


def get_display_scenario_label():
    scenario_name = str(st.session_state.get("current_scenario", "Scenario A")).strip() or "Scenario A"
    scope = st.session_state.get("scenario_scope", SCENARIO_SCOPE_TOP)
    mode = st.session_state.get("config_mode", "optimization")

    if scope == SCENARIO_SCOPE_ALL:
        if scenario_name in {"Scenario A", "Scenario B", "Scenario C"}:
            return "Scenario C"
        return scenario_name

    if mode == "simulation":
        if scenario_name in {"Scenario A", "Scenario B"}:
            return "Scenario B"
        if scenario_name.endswith("-sim"):
            return scenario_name
        return f"{scenario_name}-sim"

    if scenario_name == "Scenario B":
        return "Scenario A"
    if scenario_name.endswith("-sim"):
        return scenario_name[:-4]
    return scenario_name


def build_coherence_issues():
    issues = []
    is_simulation_mode = st.session_state.get("config_mode") == "simulation"
    for row in st.session_state.destination_tanks:
        if row["selected"] and row["v_min"] > row["v_max"]:
            issues.append(
                f'{row["tank"]}: volume minimo impostato {row["v_min"]} m3 superiore al volume massimo impostato {row["v_max"]} m3'
            )

    destination_vmax = {}
    for row in st.session_state.destination_tanks:
        if not row.get("selected"):
            continue
        try:
            destination_vmax[row["tank"]] = float(row["v_max"])
        except (TypeError, ValueError):
            continue

    destination_transfer_sum = {tank: 0.0 for tank in destination_vmax}
    for row in get_active_source_tanks():
        if is_simulation_mode:
            dest = str(row.get("destination_tank", "")).strip()
            if not dest or dest not in destination_transfer_sum:
                continue
            try:
                transfer_volume = float(row.get("transfer_volume", 0) or 0)
            except (TypeError, ValueError):
                transfer_volume = 0.0
            destination_transfer_sum[dest] += transfer_volume
            continue

        for tank, field in TOP_TRANSFER_FIELDS.items():
            if tank not in destination_transfer_sum:
                continue
            destination_transfer_sum[tank] += float(safe_int_input(row.get(field), 0))

    for tank, total_transfer in destination_transfer_sum.items():
        vmax = destination_vmax[tank]
        if total_transfer > vmax:
            issues.append(
                f"{tank}: volume totale da trasferire {int(total_transfer)} m3 superiore al V max impostato {int(vmax)} m3"
            )

    source_rows = get_active_source_tanks()
    rows_by_tank = {
        str(row.get("tank", "")).strip().upper(): row
        for row in source_rows
        if str(row.get("tank", "")).strip()
    }

    def get_destinations_with_volume(row):
        if is_simulation_mode:
            destination = str(row.get("destination_tank", "")).strip()
            volume = safe_int_input(row.get("transfer_volume"), 0)
            return {destination: volume} if destination and volume > 0 else {}

        result = {}
        for tank, field in TOP_TRANSFER_FIELDS.items():
            volume = safe_int_input(row.get(field), 0)
            if volume > 0:
                result[tank] = volume
        return result

    def check_incompatibility_pair(tank_a: str, tank_b: str):
        row_a = rows_by_tank.get(tank_a.upper())
        row_b = rows_by_tank.get(tank_b.upper())
        if not row_a or not row_b:
            return

        vols_a = get_destinations_with_volume(row_a)
        vols_b = get_destinations_with_volume(row_b)
        conflicting_destinations = sorted(set(vols_a).intersection(vols_b))
        if not conflicting_destinations:
            return

        if len(conflicting_destinations) == 1:
            issues.append(
                f"Incompatibilita: {tank_a} e {tank_b} valorizzati entrambi su {conflicting_destinations[0]} con volume > 0"
            )
        else:
            joined = ", ".join(conflicting_destinations)
            issues.append(
                f"Incompatibilita: {tank_a} e {tank_b} valorizzati entrambi sugli stessi serbatoi ({joined})"
            )

    processed_pairs = set()
    for row in source_rows:
        tank_name = str(row.get("tank", "")).strip()
        if not tank_name:
            continue

        incompatibility_text = str(row.get("incompatibility", "") or "").strip()
        if not incompatibility_text:
            continue

        incompatible_tanks = [
            item.strip() for item in incompatibility_text.replace(";", ",").split(",") if item.strip()
        ]
        for incompatible_tank in incompatible_tanks:
            pair_key = tuple(sorted([tank_name.upper(), incompatible_tank.upper()]))
            if pair_key in processed_pairs:
                continue
            processed_pairs.add(pair_key)
            check_incompatibility_pair(tank_name, incompatible_tank)

    # Fallback esplicito per la regola demo richiesta: S-03 vs S-08.
    demo_pair_key = tuple(sorted(["S-03", "S-08"]))
    if demo_pair_key not in processed_pairs:
        check_incompatibility_pair("S-03", "S-08")
    return issues


def build_output_recipe_dataframe():
    rows = []
    is_simulation_mode = st.session_state.get("config_mode") == "simulation"
    selected_destinations = set(get_selected_destination_tanks())
    for row in st.session_state.source_tanks:
        if is_simulation_mode:
            destination = str(row.get("destination_tank", "")).strip()
            if not destination:
                continue
            if selected_destinations and destination not in selected_destinations:
                continue
            transfer_volume = safe_int_input(row.get("transfer_volume"), 0)
            if transfer_volume <= 0:
                continue
            rows.append(
                {
                    "Serbatoio sorgente": row["tank"],
                    "Serbatoio di destinazione": destination,
                    "Volume trasferito": transfer_volume,
                    "COD": safe_int_input(row.get("cod"), 0),
                    "Solventi": safe_int_input(row.get("solvents"), 0),
                    "Boro": float(row.get("boro", 0) or 0),
                    "Note": str(row.get("notes", "")).strip() or "\u2014",
                }
            )
            continue

        for destination, field in TOP_TRANSFER_FIELDS.items():
            if selected_destinations and destination not in selected_destinations:
                continue
            transfer_volume = safe_int_input(row.get(field), 0)
            if transfer_volume <= 0:
                continue
            rows.append(
                {
                    "Serbatoio sorgente": row["tank"],
                    "Serbatoio di destinazione": destination,
                    "Volume trasferito": transfer_volume,
                    "COD": safe_int_input(row.get("cod"), 0),
                    "Solventi": safe_int_input(row.get("solvents"), 0),
                    "Boro": float(row.get("boro", 0) or 0),
                    "Note": str(row.get("notes", "")).strip() or "\u2014",
                }
            )

    if not rows:
        fallback_destination = get_selected_destination_tanks()[0] if get_selected_destination_tanks() else "\u2014"
        for row in st.session_state.source_tanks:
            if "residuo" in str(row["tank"]).lower():
                continue
            qty = safe_int_input(row.get("qty_available"), 0)
            rows.append(
                {
                    "Serbatoio sorgente": row["tank"],
                    "Serbatoio di destinazione": fallback_destination,
                    "Volume trasferito": max(5, min(20, qty if qty > 0 else 10)),
                    "COD": safe_int_input(row.get("cod"), 0),
                    "Solventi": safe_int_input(row.get("solvents"), 0),
                    "Boro": float(row.get("boro", 0) or 0),
                    "Note": "ricetta proposta demo",
                }
            )
            if len(rows) >= 2:
                break

    return pd.DataFrame(rows)


def compute_output_summary(recipe_df: pd.DataFrame):
    if recipe_df.empty:
        return {
            "components": 0,
            "total_volume": 0,
            "avg_cod": 0,
            "avg_solvents": 0,
            "avg_boro": 0.0,
        }

    vol = pd.to_numeric(recipe_df["Volume trasferito"], errors="coerce").fillna(0.0)
    total_volume = int(vol.sum())

    def weighted_metric(column_name: str):
        values = pd.to_numeric(recipe_df[column_name], errors="coerce").fillna(0.0)
        if vol.sum() > 0:
            return float((values * vol).sum() / vol.sum())
        return float(values.mean()) if len(values) else 0.0

    return {
        "components": int(len(recipe_df)),
        "total_volume": total_volume,
        "avg_cod": int(round(weighted_metric("COD"))),
        "avg_solvents": int(round(weighted_metric("Solventi"))),
        "avg_boro": round(weighted_metric("Boro"), 1),
    }


def style_priority_column(col: pd.Series):
    if col.name != "Priorit\u00e0":
        return [""] * len(col)

    palette = {
        "Alta": ("#e4efff", "#5f7fb8"),
        "Media": ("#f8efd4", "#b19449"),
        "Bassa": ("#edf1f5", "#6f7f90"),
    }

    styles = []
    for value in col:
        bg, fg = palette.get(str(value), ("#edf1f5", "#6f7f90"))
        styles.append(f"background-color: {bg}; color: {fg}; font-weight: 700; text-align: center;")
    return styles


def style_empty_tank_column(col: pd.Series):
    if "Svuota" not in str(col.name):
        return [""] * len(col)

    styles = []
    for value in col:
        if str(value).strip():
            styles.append("color: #1a9e46; font-weight: 800; text-align: center;")
        else:
            styles.append("color: #9aa5b1; text-align: center;")
    return styles


def style_incompatibility_column(col: pd.Series):
    if "Incompat" not in str(col.name):
        return [""] * len(col)

    styles = []
    for value in col:
        marker = str(value).strip()
        if marker and marker not in {"-", "\u2014"}:
            styles.append("color: #c62828; font-weight: 800;")
        else:
            styles.append("color: #9aa5b1;")
    return styles


enforce_destination_tank_rules()


@st.dialog("Modifica serbatoio", width="large")
def edit_source_tank_dialog(row_index: int, dialog_nonce: int):
    source_rows = get_active_source_tanks()
    if row_index is None or row_index < 0 or row_index >= len(source_rows):
        st.warning("Nessun record valido selezionato.")
        if st.button("Chiudi", width="content", key=f"edit_close_{dialog_nonce}"):
            st.session_state.show_edit_dialog = False
            st.rerun()
        return

    row = source_rows[row_index]

    left_edit_col, right_edit_col = st.columns(2, gap="large")

    with left_edit_col:
        st.markdown("#### Caratteristiche")
        source_tank_name = st.text_input("Serbatoio", value=str(row.get("tank", "")), key=f"edit_tank_{dialog_nonce}")
        qty_available = st.number_input(
            "Q.ta disponibile",
            value=safe_int_input(row.get("qty_available")),
            step=1,
            key=f"edit_qty_available_{dialog_nonce}",
        )
        cod = st.number_input(
            "COD",
            value=safe_int_input(row.get("cod")),
            step=1,
            key=f"edit_cod_{dialog_nonce}",
        )
        solvents = st.number_input(
            "Solventi",
            value=safe_int_input(row.get("solvents")),
            step=1,
            key=f"edit_solvents_{dialog_nonce}",
        )
        cl = st.number_input(
            "Cl",
            value=safe_int_input(row.get("cl")),
            step=1,
            key=f"edit_cl_{dialog_nonce}",
        )
        n_value = st.number_input(
            "N",
            value=safe_int_input(row.get("n")),
            step=1,
            key=f"edit_n_{dialog_nonce}",
        )
        boro_default = 0.0
        if not is_missing(row.get("boro")):
            try:
                boro_default = float(row.get("boro"))
            except (TypeError, ValueError):
                boro_default = 0.0
        boro = st.number_input(
            "Boro",
            value=boro_default,
            step=0.1,
            format="%.1f",
            key=f"edit_boro_{dialog_nonce}",
        )

    with right_edit_col:
        st.markdown("#### Vincoli e Preferenze")
        empty_tank = st.checkbox(
            "Svuota serbatoio",
            value=bool(row.get("empty_tank")),
            key=f"edit_empty_tank_{dialog_nonce}",
        )
        priority_options = ["", "Alta", "Media", "Bassa"]
        current_priority = row.get("priority", "") if row.get("priority", "") in priority_options else ""
        priority = st.selectbox(
            "Priorita",
            options=priority_options,
            index=priority_options.index(current_priority),
            format_func=lambda x: "\u2014" if x == "" else x,
            key=f"edit_priority_{dialog_nonce}",
        )
        incompatibility = st.text_input(
            "Incompatibilita",
            value=str(row.get("incompatibility", "")),
            key=f"edit_incompatibility_{dialog_nonce}",
        )
        is_simulation_dialog = st.session_state.get("config_mode") == "simulation"
        active_destinations = set(get_selected_destination_tanks())
        transfer_by_tk = {}
        destination_tank = ""
        transfer_volume = 0

        if is_simulation_dialog:
            base_destination_options = get_selected_destination_tanks()
            destination_options = base_destination_options if base_destination_options else [""]
            current_destination = (
                row.get("destination_tank", "")
                if row.get("destination_tank", "") in destination_options
                else (destination_options[0] if destination_options else "")
            )
            destination_tank = st.selectbox(
                "Serbatoio di destinazione",
                options=destination_options,
                index=destination_options.index(current_destination),
                format_func=lambda x: "\u2014" if x == "" else x,
                key=f"edit_destination_{dialog_nonce}",
            )
            transfer_volume = st.number_input(
                "Volume da trasferire",
                value=safe_int_input(row.get("transfer_volume")),
                step=1,
                key=f"edit_transfer_volume_{dialog_nonce}",
            )
        else:
            for dest_tank, field in TOP_TRANSFER_FIELDS.items():
                default_volume = safe_int_input(row.get(field), 0)
                if default_volume == 0 and str(row.get("destination_tank", "")).strip() == dest_tank:
                    default_volume = safe_int_input(row.get("transfer_volume"), 0)
                transfer_by_tk[field] = st.number_input(
                    f"Volume da trasferire in {dest_tank}",
                    value=default_volume,
                    min_value=0,
                    step=1,
                    disabled=dest_tank not in active_destinations,
                    key=f"edit_{field}_{dialog_nonce}",
                )
        vol_min = st.number_input(
            "Vol. min",
            value=safe_int_input(row.get("vol_min")),
            step=1,
            disabled=empty_tank,
            key=f"edit_vol_min_{dialog_nonce}",
        )
        vol_max = st.number_input(
            "Vol. max",
            value=safe_int_input(row.get("vol_max")),
            step=1,
            disabled=empty_tank,
            key=f"edit_vol_max_{dialog_nonce}",
        )
        notes = st.text_area(
            "Note",
            value=str(row.get("notes", "")),
            key=f"edit_notes_{dialog_nonce}",
        )

    cancel_col, save_col, _ = st.columns([1, 1, 2], gap="small")
    with cancel_col:
        if st.button("Annulla", width="stretch", key=f"edit_cancel_{dialog_nonce}"):
            st.session_state.show_edit_dialog = False
            st.rerun()
    with save_col:
        if st.button("Salva", width="stretch", type="primary", key=f"edit_save_{dialog_nonce}"):
            source_rows[row_index]["tank"] = str(source_tank_name).strip()
            source_rows[row_index]["qty_available"] = qty_available
            source_rows[row_index]["cod"] = cod
            source_rows[row_index]["solvents"] = solvents
            source_rows[row_index]["cl"] = cl
            source_rows[row_index]["n"] = n_value
            source_rows[row_index]["boro"] = boro
            source_rows[row_index]["empty_tank"] = empty_tank
            source_rows[row_index]["priority"] = priority
            source_rows[row_index]["incompatibility"] = incompatibility
            if is_simulation_dialog:
                source_rows[row_index]["destination_tank"] = destination_tank
                source_rows[row_index]["transfer_volume"] = transfer_volume
            else:
                for dest_tank, field in TOP_TRANSFER_FIELDS.items():
                    source_rows[row_index][field] = transfer_by_tk[field] if dest_tank in active_destinations else 0
                source_rows[row_index]["destination_tank"] = ""
                source_rows[row_index]["transfer_volume"] = sum(
                    safe_int_input(source_rows[row_index].get(field), 0) for field in TOP_TRANSFER_FIELDS.values()
                )
            source_rows[row_index]["vol_min"] = None if empty_tank else vol_min
            source_rows[row_index]["vol_max"] = None if empty_tank else vol_max
            source_rows[row_index]["notes"] = notes
            enforce_destination_tank_rules()
            st.session_state.show_edit_dialog = False
            st.rerun()


st.markdown("""
<style>
header[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    display: none !important;
}

.stApp {
    background: #d5d7db;
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
}

.block-container {
    max-width: none;
    padding: 8px 14px 14px;
    margin-top: 84px;
    margin-left: 252px;
    margin-right: 14px;
    margin-bottom: 0.7rem;
    border-radius: 0;
    background: transparent;
}

.shell-topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 48px;
    background: #ffffff;
    border-bottom: 1px solid #dce2ea;
    z-index: 1200;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    min-width: 0;
}

.shell-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #1f2f4a;
}

.shell-brand-mark-wrap {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3px;
}

.shell-brand-mark {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #cd909f;
    position: relative;
    overflow: hidden;
    flex: 0 0 34px;
}

.shell-brand-mark::before {
    content: "";
    position: absolute;
    top: -8px;
    left: 8px;
    width: 14px;
    height: 50px;
    border-left: 4px solid #ffffff;
    border-radius: 28px;
    transform: rotate(-21deg);
    box-shadow: 8px 0 0 #ffffff;
}

.shell-brand-mark-line {
    width: 34px;
    height: 4px;
    border-radius: 1px;
    background: #cd909f;
}

.shell-brand-copy {
    display: inline-flex;
    flex-direction: column;
    justify-content: center;
    gap: 2px;
}

.shell-brand-text {
    font-size: 16px;
    font-weight: 300;
    letter-spacing: 1.9px;
    line-height: 1;
    color: #9aa2ab;
}

.shell-brand-sub {
    font-size: 7px;
    color: #8b949f;
    letter-spacing: 2.2px;
    font-weight: 500;
    white-space: nowrap;
}

.shell-top-right {
    display: flex;
    align-items: stretch;
    height: 100%;
    flex-wrap: nowrap;
    white-space: nowrap;
}

.shell-top-sep {
    width: 1px;
    background: #e4e9f0;
}

.shell-top-actions {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 0 10px;
    flex-wrap: nowrap;
}

.shell-top-action {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 1px solid #d7dde7;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #f5f7fa;
    position: relative;
}

.shell-top-icon {
    width: 13px;
    height: 13px;
    stroke: #8a93a0;
    fill: none;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.shell-top-icon-fill {
    fill: #8a93a0;
    stroke: none;
}

.shell-top-action-badge {
    position: absolute;
    top: -4px;
    right: -3px;
    min-width: 13px;
    height: 13px;
    border-radius: 8px;
    background: #d63535;
    color: #fff;
    font-size: 8px;
    font-weight: 700;
    line-height: 13px;
    text-align: center;
    padding: 0 2px;
}

.shell-userbox {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #506178;
    padding: 0 12px;
    white-space: nowrap;
}

.shell-avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #3cbf8f;
    color: #ffffff;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
}

.shell-user-meta {
    display: flex;
    flex-direction: column;
    line-height: 1.15;
}

.shell-user-name {
    color: #3b4b61;
    font-size: 13px;
    font-weight: 600;
}

.shell-user-role {
    color: #8a96a6;
    font-size: 11px;
}

.shell-subtop {
    position: fixed;
    top: 48px;
    left: 240px;
    right: 0;
    height: 32px;
    background: #27447f;
    z-index: 1100;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    color: #ffffff;
}

.shell-subtop-title {
    font-size: 14px;
    font-weight: 600;
    line-height: 1;
    letter-spacing: 0.1px;
    position: static;
    padding-bottom: 0;
}

.shell-subtop-title::after {
    display: none;
}

.shell-subtop-path {
    font-size: 12px;
    color: #d3dced;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.shell-subtop-homeicon {
    color: #ffffff;
    font-size: 12px;
    line-height: 1;
}

.shell-sidebar {
    position: fixed;
    top: 48px;
    left: 0;
    bottom: 0;
    width: 240px;
    background: #28467f;
    border-right: 1px solid #213962;
    z-index: 1150;
    overflow-y: auto;
}

.shell-nav-head {
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #dce6f7;
    border-bottom: 1px solid #375388;
    padding: 0 8px 0 10px;
    font-size: 12px;
    font-weight: 600;
}

.shell-nav-head-left {
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.shell-nav-timer {
    color: #56b6e6;
    font-size: 12px;
    font-weight: 500;
}

.shell-nav-toggle {
    width: 56px;
    height: 32px;
    background: #1b1f29;
    color: #ffffff;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    margin-right: -10px;
    text-decoration: none;
}

.shell-menu {
    padding: 8px 0 14px;
}

.shell-menu-item {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #dbe5f6;
    font-size: 14px;
    font-weight: 600;
    padding: 10px 14px 10px 16px;
    border-left: 3px solid transparent;
    cursor: default;
    white-space: nowrap;
}

.shell-menu-item:hover {
    background: #33518c;
}

.shell-menu-item-active {
    background: #3a5d9b;
    border-left-color: #61c38f;
    color: #ffffff;
}

.shell-menu-icon {
    width: 18px;
    min-width: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #f2f6ff;
}

.shell-menu-icon svg {
    width: 16px;
    height: 16px;
    stroke: currentColor;
    fill: none;
    stroke-width: 1.9;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.shell-menu-icon-fill {
    fill: currentColor;
    stroke: none;
}

.shell-menu-item-label {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.shell-menu-caret {
    color: #b8c8e3;
    font-size: 10px;
}

@media (max-width: 1200px) {
    .shell-sidebar {
        width: 220px;
    }

    .shell-subtop {
        left: 220px;
    }

    .block-container {
        margin-left: 228px;
    }

    .shell-subtop-title {
        font-size: 14px;
    }
}

@media (max-width: 900px) {
    .shell-sidebar {
        display: none;
    }

    .shell-subtop {
        left: 0;
    }

    .block-container {
        margin-left: 12px;
        margin-right: 12px;
    }
}

.top-titlebar {
    background: #1f4b8f;
    color: #ffffff;
    font-size: 16px;
    font-weight: 700;
    line-height: 1.35;
    padding: 9px 14px;
    border-radius: 8px;
    margin-bottom: 10px;
}

.st-key-top_toolbar {
    margin: 10px 0 8px;
    padding: 0;
}

.st-key-top_toolbar [data-testid="stHorizontalBlock"] {
    align-items: flex-start !important;
}

.st-key-output_toolbar {
    margin: 10px 0 8px;
    padding: 0;
}

.st-key-output_toolbar [data-testid="stHorizontalBlock"] {
    align-items: center;
}

.st-key-top_toolbar [data-testid="stButton"] > button {
    border: 1px solid #d9dee6;
    background: white;
    color: #586576;
    font-size: 11.5px;
    font-weight: 600;
    min-height: 32px;
    padding: 6px 10px;
    border-radius: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.st-key-top_toolbar [data-testid="stButton"] > button[kind="primary"] {
    background: #2f5bb4;
    border-color: #244d9a;
    color: #ffffff;
}

.st-key-top_toolbar [data-testid="stButton"] > button:disabled {
    opacity: 1;
    background: #eceff3;
    border-color: #d9dee6;
    color: #9aa5b1;
}

.st-key-new_scenario_hover_menu,
.st-key-open_scenario_hover_menu {
    position: relative;
}

.st-key-new_scenario_hover_menu [data-testid="stVerticalBlock"],
.st-key-open_scenario_hover_menu [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

.st-key-new_scenario_hover_menu [data-testid="stElementContainer"],
.st-key-open_scenario_hover_menu [data-testid="stElementContainer"] {
    margin-bottom: 0 !important;
}

.st-key-new_scenario_hover_items,
.st-key-open_scenario_hover_items {
    display: none;
    position: absolute;
    top: 36px;
    left: 0;
    width: 100%;
    z-index: 1200;
    border: 1px solid #d9dee6;
    border-radius: 6px;
    background: #ffffff;
    box-shadow: 0 8px 16px rgba(27, 39, 58, 0.12);
    padding: 4px;
}

.st-key-new_scenario_hover_menu:hover .st-key-new_scenario_hover_items,
.st-key-open_scenario_hover_menu:hover .st-key-open_scenario_hover_items {
    display: block;
}

.st-key-new_scenario_hover_items [data-testid="stButton"] > button,
.st-key-open_scenario_hover_items [data-testid="stButton"] > button {
    border: 0 !important;
    border-radius: 4px !important;
    background: #ffffff !important;
    color: #586576 !important;
    font-size: 11.5px !important;
    font-weight: 600 !important;
    min-height: 30px !important;
    justify-content: flex-start !important;
    padding: 6px 8px !important;
}

.st-key-new_scenario_hover_items [data-testid="stButton"] > button:hover,
.st-key-open_scenario_hover_items [data-testid="stButton"] > button:hover {
    background: #eef3fa !important;
}

.st-key-output_toolbar [data-testid="stButton"] > button {
    border: 1px solid #d9dee6;
    background: white;
    color: #586576;
    font-size: 12px;
    font-weight: 600;
    min-height: 32px;
    padding: 6px 14px;
    border-radius: 6px;
}

.st-key-btn_out_mod_scenario [data-testid="stButton"] > button,
.st-key-btn_out_dup [data-testid="stButton"] > button {
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    padding: 6px 10px !important;
}

.top-chip {
    border: 1px solid #d9dee6;
    background: #ffffff;
    color: #586576;
    font-size: 12px;
    font-weight: 600;
    min-height: 32px;
    padding: 6px 14px;
    border-radius: 6px;
    text-align: center;
    display: inline-flex;
    width: fit-content;
    white-space: nowrap;
    align-items: center;
    justify-content: center;
}

.st-key-left_config_panel,
.st-key-left_coherence_panel {
    border: 1px solid #d9dee6;
    border-radius: 8px;
    background: #ffffff;
    padding: 10px 12px 12px;
}

.st-key-left_coherence_panel {
    margin-top: 12px;
    min-height: 128px;
}

.left-panel-head {
    border-bottom: 1px solid #e8edf3;
    margin: -10px -12px 10px;
    padding: 10px 12px 9px;
    background: #fafbfd;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

.left-panel-title {
    font-size: 15px;
    font-weight: 700;
    color: #334155;
    margin-bottom: 2px;
}

.left-panel-caption {
    font-size: 11.5px;
    color: #8b97a4;
}

.st-key-destination_view_selector [data-testid="stRadio"] > div {
    gap: 14px;
}

.st-key-destination_view_selector [data-testid="stRadio"] label {
    font-size: 12px;
    color: #546273;
}

.left-subpanel-title {
    font-size: 15px;
    font-weight: 700;
    color: #334155;
    margin-bottom: 8px;
}

.st-key-left_config_panel [data-testid="stDataEditor"] {
    border: 1px solid #d9dee6;
    border-radius: 8px;
    overflow: hidden;
    --gdg-text-group-header: #1f3048;
    --gdg-text-dark: #1f3048;
    --gdg-text-medium: #2d425e;
    --gdg-text-light: #5a6b80;
    --gdg-bg-header: #f1f3f6;
    --gdg-bg-header-has-focus: #e8edf5;
    --gdg-header-font-style: 700 11px;
}

.st-key-left_config_panel [data-testid="stDataEditor"] [role="columnheader"] {
    background: #f1f3f6;
    color: #1f3048 !important;
    font-weight: 700;
    font-size: 10.5px;
}

.st-key-left_config_panel [data-testid="stDataEditor"] [role="gridcell"] {
    font-size: 11px;
}

.recipe-card {
    border: 1px solid #d9dee6;
    background: #f4f5f8;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 12.5px;
    margin-top: 4px;
}

.recipe-head {
    font-size: 12.5px;
    font-weight: 700;
    color: #334155;
    margin-bottom: 6px;
}

.recipe-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin: 4px 0;
}

.recipe-label {
    color: #7b8794;
}

.recipe-value {
    font-weight: 700;
    color: #334155;
}

.st-key-cod_setting_box {
    margin-top: 8px;
    border: 1px solid #d9dee6;
    background: #f7f9fc;
    border-radius: 8px;
    padding: 8px 10px;
}

.cod-setting-label {
    color: #334155;
    font-size: 12px;
    font-weight: 600;
    line-height: 30px;
}

.cod-setting-unit {
    color: #7b8794;
    font-size: 12px;
    font-weight: 600;
    line-height: 30px;
}

.st-key-cod_setting_box [data-testid="stNumberInput"] input {
    text-align: right;
    font-weight: 600;
}

.st-key-left_config_panel [data-testid="stButton"] > button {
    border: 1px solid #d9dee6;
    border-radius: 8px;
    color: #7b8794;
    background: #ffffff;
    font-weight: 600;
    min-height: 32px;
    padding: 6px 14px;
    font-size: 12px;
}

.st-key-left_config_panel [data-testid="stButton"] > button:disabled {
    opacity: 1;
    color: #8f9baa;
    background: #fbfcfe;
}

.coh-count {
    color: #d17e7e;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
}

.coh-list {
    margin: 0;
    padding-left: 18px;
    color: #546273;
    font-size: 12.5px;
}

.coh-list li {
    margin-bottom: 6px;
}

.coh-ok {
    color: #2e7d32;
    background: #edf7ee;
    border: 1px solid #cfe8d3;
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 12.5px;
    font-weight: 600;
}

.right-main-title {
    font-size: 15px;
    font-weight: 700;
    color: #334155;
    margin: 2px 0 8px;
    padding: 2px 2px 6px;
    background: transparent;
    border: none;
    border-radius: 0;
}

.mode-tabs {
    display: flex;
    gap: 22px;
    align-items: flex-end;
    border-bottom: 1px solid #d9dee6;
    margin: 0 0 8px;
    padding: 0 12px;
}

.mode-tab {
    font-size: 16px;
    font-weight: 600;
    color: #8b97a4;
    padding: 0 0 8px;
}

.mode-tab-active {
    color: #1f4b8f;
    font-weight: 700;
    border-bottom: 3px solid #2f5bb4;
    margin-bottom: -1px;
}

.st-key-config_mode_tabs {
    display: block;
    border-bottom: 1px solid #d9dee6;
    margin: 0 0 8px;
    padding: 0 12px 0;
}

.st-key-config_mode_tabs [data-testid="stHorizontalBlock"] {
    align-items: flex-end;
}

.st-key-config_mode_tabs [data-testid="stButton"] > button {
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    border-radius: 0;
    color: #8b97a4;
    font-size: 15px;
    font-weight: 600;
    min-height: 32px;
    line-height: 1.2;
    padding: 0 8px 6px;
    margin-bottom: -1px;
    box-shadow: none;
    white-space: nowrap;
}

.st-key-config_mode_tabs [data-testid="stButton"] > button[kind="primary"] {
    color: #1f4b8f;
    font-weight: 700;
    border-bottom-color: #2f5bb4;
}

.st-key-mode_actions {
    margin: 6px 0 10px;
}

.st-key-right_main_box {
    border: 1px solid #d9dee6;
    border-radius: 12px;
    background: #ffffff;
    padding: 10px 12px 12px;
}

.st-key-mode_actions [data-testid="stButton"] > button {
    border: 1px solid #c8d2df;
    background: #f3f6fb;
    color: #1b2f48;
    font-size: 12px;
    font-weight: 700;
    min-height: 32px;
    padding: 5px 14px;
    border-radius: 8px;
    box-shadow: 0 1px 0 rgba(15, 23, 42, 0.03);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.st-key-mode_actions [data-testid="stButton"] > button:hover:not(:disabled) {
    border-color: #b8c6d8;
    background: #e8eef6;
}

.st-key-mode_actions [data-testid="stButton"] > button:disabled {
    opacity: 1;
    background: #eceff3;
    border-color: #d9dee6;
    color: #9aa5b1;
}

.st-key-btn_refresh_skysym [data-testid="stButton"] > button {
    background: #e9eff8;
    border-color: #c5d2e2;
    color: #1f3c5d;
}

.st-key-btn_edit_row_top [data-testid="stButton"] > button {
    background: #eef4ff;
    border-color: #b8cbef;
    color: #214d8d;
}

.st-key-btn_remove_row_top [data-testid="stButton"] > button {
    background: #fff2f2;
    border-color: #eebaba;
    color: #8f2626;
}

.st-key-btn_add_row_simulation [data-testid="stButton"] > button {
    font-size: 11.5px;
    padding: 5px 10px;
}

.st-key-btn_filters [data-testid="stButton"] > button {
    min-width: 0;
    width: 100%;
}

.st-key-mode_actions [data-testid="stTextInput"] input {
    border: 1px solid #d9dee6 !important;
    background: #ffffff !important;
    color: #334155 !important;
    border-radius: 8px !important;
    min-height: 32px;
    font-size: 12px;
}

.st-key-source_tanks_table [data-testid="stDataFrame"] {
    border: 1px solid #d9dee6;
    border-radius: 8px;
    overflow: hidden;
    --gdg-text-group-header: #1f3048;
    --gdg-text-dark: #1f3048;
    --gdg-text-medium: #2d425e;
    --gdg-text-light: #5a6b80;
    --gdg-bg-header: #f1f3f6;
    --gdg-bg-header-has-focus: #e8edf5;
    --gdg-header-font-style: 700 11px;
}

.st-key-source_tanks_table [role="columnheader"] {
    background: #f1f3f6;
    color: #1f3048 !important;
    font-weight: 700;
    font-size: 11px;
}

.st-key-source_tanks_table [role="gridcell"] {
    font-size: 11px;
}

.mini-panel {
    background: #ffffff;
    border: 1px solid #d9dee6;
    border-radius: 8px;
    overflow: hidden;
}

.mini-title {
    font-weight: 700;
    padding: 10px 12px 6px;
    color: #334155;
}

.mini-body {
    padding: 0 12px 12px;
}

.metric-list {
    display: grid;
    gap: 8px;
}

.metric {
    border: 1px solid #d9dee6;
    border-radius: 8px;
    background: #fafbfd;
    padding: 10px 12px;
    font-size: 12px;
    color: #67768a;
}

.metric b {
    color: #334155;
    margin-left: 8px;
}

.output-kpi {
    border: 1px solid #d9dee6;
    border-radius: 8px;
    background: #ffffff;
    padding: 10px 12px;
}

.output-kpi-title {
    color: #7b8794;
    font-size: 11px;
    margin-bottom: 4px;
}

.output-kpi-value {
    color: #1f4b8f;
    font-size: 20px;
    font-weight: 700;
    line-height: 1.1;
}

.st-key-output_recipe_box,
.st-key-output_status_box {
    border: 1px solid #d9dee6;
    border-radius: 12px;
    background: #ffffff;
    padding: 10px 12px 12px;
}

/* Keep "Confronto" visible as a fake/disabled tab in output view. */
.st-key-output_recipe_box [data-baseweb="tab-list"] button:nth-child(3) {
    pointer-events: none;
    opacity: 0.55;
    cursor: not-allowed;
}

/* Force stronger contrast on Glide Data Grid headers (Streamlit DataFrame/DataEditor). */
[data-testid="stDataFrame"],
[data-testid="stDataEditor"] {
    --gdg-text-group-header: #14263f !important;
    --gdg-text-dark: #14263f !important;
    --gdg-text-medium: #2a3f5c !important;
    --gdg-bg-header: #edf2f8 !important;
    --gdg-bg-header-has-focus: #e6ecf5 !important;
    --gdg-header-font-style: 700 12px !important;
}

[data-testid="stDataFrame"] [class^="gdg-"],
[data-testid="stDataFrame"] [class*=" gdg-"],
[data-testid="stDataEditor"] [class^="gdg-"],
[data-testid="stDataEditor"] [class*=" gdg-"],
[data-testid="stDataFrame"] div[style*="--gdg-"],
[data-testid="stDataEditor"] div[style*="--gdg-"] {
    --gdg-text-group-header: #14263f !important;
    --gdg-text-dark: #14263f !important;
    --gdg-text-medium: #2a3f5c !important;
    --gdg-bg-header: #edf2f8 !important;
    --gdg-bg-header-has-focus: #e6ecf5 !important;
    --gdg-header-font-style: 700 12px !important;
}

[data-testid="stDataFrame"] .gdg-c1tqibwd,
[data-testid="stDataEditor"] .gdg-c1tqibwd,
[data-testid="stDataFrame"] [role="columnheader"],
[data-testid="stDataEditor"] [role="columnheader"] {
    color: #14263f !important;
    font-weight: 700 !important;
}

/* ---- Output view ---- */

.st-key-output_toolbar [data-testid="stButton"] > button[kind="primary"] {
    background: #3fbf69;
    border-color: #35aa5d;
    color: #ffffff;
}

.st-key-output_status_box [data-testid="stButton"] > button {
    border: 1px solid #d9dee6;
    background: white;
    color: #586576;
    font-size: 12px;
    font-weight: 600;
    min-height: 32px;
    padding: 6px 14px;
    border-radius: 6px;
    width: 100%;
    margin-bottom: 4px;
}

.st-key-output_status_box [data-testid="stButton"] > button[kind="primary"] {
    background: #3fbf69;
    border-color: #35aa5d;
    color: #ffffff;
}

.out-section-label {
    font-size: 11px;
    font-weight: 700;
    color: #8b97a4;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 8px 0 5px;
}

.tank-target-box {
    background: #f7f9fc;
    border: 1px solid #e4eaf2;
    border-radius: 8px;
    padding: 8px 10px;
}

.tank-target-title {
    font-size: 12px;
    font-weight: 700;
    color: #334155;
    margin-bottom: 6px;
}

.tank-target-row {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.tgt-chip {
    background: #edf2f8;
    border: 1px solid #d4dde9;
    border-radius: 5px;
    padding: 2px 8px;
    font-size: 11px;
    color: #4a5a6d;
    white-space: nowrap;
}

.tank-table-title {
    font-size: 12px;
    font-weight: 700;
    color: #334155;
    margin: 6px 0 3px;
}

.tank-summary-row {
    display: flex;
    gap: 14px;
    padding: 6px 10px;
    background: #f4f6fa;
    border: 1px solid #dde4ee;
    border-radius: 0 0 6px 6px;
    font-size: 11.5px;
    color: #546273;
    margin-top: -2px;
}

.tank-summary-row b {
    color: #334155;
    margin-left: 2px;
}

.param-list {
    background: #f7f9fc;
    border: 1px solid #e4eaf2;
    border-radius: 7px;
    overflow: hidden;
}

.param-row {
    display: flex;
    justify-content: space-between;
    padding: 5px 10px;
    font-size: 11.5px;
    border-bottom: 1px solid #edf1f6;
    color: #546273;
}

.param-row:last-child {
    border-bottom: none;
}

.param-row b {
    color: #334155;
}

.conf-chip-sel {
    display: inline-block;
    background: #e8f0fc;
    border: 1.5px solid #b8ceef;
    color: #1f4b8f;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
}

.cmp-card {
    border: 1px solid #e0e7f0;
    border-radius: 8px;
    padding: 8px 10px;
    background: #fafbfd;
    font-size: 12px;
    margin-top: 8px;
}

.cmp-card-title {
    font-size: 12px;
    font-weight: 700;
    color: #334155;
    margin-bottom: 6px;
    padding-bottom: 4px;
    border-bottom: 1px solid #e8edf3;
}

.cmp-row {
    color: #546273;
    margin: 3px 0;
}

.cmp-row b { color: #334155; }

.esito-ok {
    color: #2e7d32 !important;
    font-weight: 600;
    margin-top: 5px;
    padding-top: 5px;
    border-top: 1px solid #e8edf3;
}

.esito-warn {
    color: #b35c00 !important;
    font-weight: 600;
    margin-top: 5px;
    padding-top: 5px;
    border-top: 1px solid #e8edf3;
}

.crit-item {
    border-radius: 7px;
    padding: 7px 10px;
    font-size: 12px;
}

.crit-warn {
    background: #fff8ec;
    border: 1px solid #f0d080;
}

.crit-info {
    background: #f4f5f8;
    border: 1px solid #dde3ec;
}

.crit-title {
    font-weight: 700;
    color: #334155;
    margin-bottom: 1px;
}

.crit-error {
    background: #fff0f0;
    border: 1px solid #f5a0a0;
}

.crit-warn .crit-body  { color: #8a5a00; font-size: 11.5px; }
.crit-info .crit-body  { color: #7b8794;  font-size: 11.5px; }
.crit-error .crit-title { color: #c0392b; }
.crit-error .crit-body  { color: #c0392b; font-size: 11.5px; }

.st-key-out_right_confronto,
.st-key-out_right_criticita,
.st-key-out_right_azioni {
    border: 1px solid #d9dee6;
    border-radius: 10px;
    background: #ffffff;
    padding: 10px 12px 12px;
    margin-bottom: 10px;
}

.st-key-out_right_azioni [data-testid="stButton"] > button {
    border: 1px solid #d9dee6;
    background: white;
    color: #586576;
    font-size: 12px;
    font-weight: 600;
    min-height: 32px;
    padding: 6px 14px;
    border-radius: 6px;
    width: 100%;
    margin-bottom: 4px;
}

.st-key-out_right_azioni [data-testid="stButton"] > button[kind="primary"] {
    background: #3fbf69;
    border-color: #35aa5d;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

shell_sidebar_open = bool(st.session_state.get("shell_sidebar_open", True))
shell_sidebar_width = 240 if shell_sidebar_open else 56
shell_content_margin_left = 252 if shell_sidebar_open else 68
shell_subtop_left = shell_sidebar_width
shell_menu_label_display = "inline" if shell_sidebar_open else "none"
shell_menu_caret_display = "inline" if shell_sidebar_open else "none"
shell_menu_item_justify = "flex-start" if shell_sidebar_open else "center"
shell_menu_item_padding = "10px 14px 10px 16px" if shell_sidebar_open else "10px 0"
shell_nav_head_left_display = "inline-flex" if shell_sidebar_open else "none"
shell_nav_head_justify = "space-between" if shell_sidebar_open else "center"
shell_sidebar_icon_width = "18px" if shell_sidebar_open else "auto"
shell_content_width_px = shell_content_margin_left + 14
shell_content_margin_top = 66
shell_toggle_left = max(0, shell_sidebar_width - 56)

st.markdown(
    f"""
<style>
.shell-sidebar {{ width: {shell_sidebar_width}px !important; }}
.shell-subtop {{ left: {shell_subtop_left}px !important; }}
.block-container {{
    margin-left: {shell_content_margin_left}px !important;
    margin-top: {shell_content_margin_top}px !important;
    padding-top: 2px !important;
    width: calc(100vw - {shell_content_width_px}px) !important;
    max-width: calc(100vw - {shell_content_width_px}px) !important;
}}
.shell-nav-head {{ justify-content: {shell_nav_head_justify} !important; }}
.shell-nav-head-left {{ display: {shell_nav_head_left_display} !important; }}
.shell-menu-item-label {{ display: {shell_menu_label_display} !important; }}
.shell-menu-caret {{ display: {shell_menu_caret_display} !important; }}
.shell-menu-item {{ justify-content: {shell_menu_item_justify} !important; padding: {shell_menu_item_padding} !important; }}
.shell-menu-icon {{ width: {shell_sidebar_icon_width} !important; }}
.st-key-shell_sidebar_toggle {{
    position: fixed;
    top: 48px;
    left: {shell_toggle_left}px;
    width: 56px;
    height: 32px;
    z-index: 1305;
}}
.st-key-shell_sidebar_toggle [data-testid="stButton"] > button {{
    width: 56px;
    min-height: 32px;
    height: 32px;
    border: none;
    border-radius: 0;
    background: #1b1f29;
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    padding: 0;
    line-height: 1;
}}
.st-key-shell_sidebar_toggle [data-testid="stButton"] > button:hover {{
    background: #151923;
    color: #ffffff;
}}
.st-key-shell_sidebar_toggle [data-testid="stButton"] > button:focus {{
    box-shadow: none;
}}
@media (max-width: 900px) {{
    .block-container {{
        margin-left: 12px !important;
        width: auto !important;
        max-width: none !important;
    }}
    .shell-subtop {{ left: 0 !important; }}
}}
</style>
""",
    unsafe_allow_html=True,
)

shell_sidebar_toggle = st.container(key="shell_sidebar_toggle", width="stretch")
with shell_sidebar_toggle:
    if st.button("\u2630", key="btn_shell_sidebar_toggle", width="content"):
        st.session_state.shell_sidebar_open = not shell_sidebar_open
        st.rerun()

st.markdown(
    f"""
    <div class="shell-topbar">
        <div class="shell-brand">
            <span class="shell-brand-mark-wrap">
                <span class="shell-brand-mark"></span>
                <span class="shell-brand-mark-line"></span>
            </span>
            <span class="shell-brand-copy">
                <span class="shell-brand-text">SKYLINE</span>
                <span class="shell-brand-sub">INNOVAZIONE DIGITALE</span>
            </span>
        </div>
        <div class="shell-top-right">
            <span class="shell-top-sep"></span>
            <div class="shell-top-actions">
                <span class="shell-top-action">
                    <svg class="shell-top-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M5 6h14v9H9l-4 3v-3H5z"></path>
                    </svg>
                </span>
            </div>
            <span class="shell-top-sep"></span>
            <div class="shell-top-actions">
                <span class="shell-top-action">
                    <svg class="shell-top-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <rect x="4" y="6" width="12" height="9" rx="1.5"></rect>
                        <circle class="shell-top-icon-fill" cx="8" cy="17" r="1.5"></circle>
                        <circle class="shell-top-icon-fill" cx="14" cy="17" r="1.5"></circle>
                        <path d="M16 9h4l1 2v4h-5"></path>
                    </svg>
                </span>
                <span class="shell-top-action">
                    <svg class="shell-top-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <rect x="4" y="6" width="12" height="9" rx="1.5"></rect>
                        <circle class="shell-top-icon-fill" cx="8" cy="17" r="1.5"></circle>
                        <circle class="shell-top-icon-fill" cx="14" cy="17" r="1.5"></circle>
                        <path d="M16 9h4l1 2v4h-5"></path>
                        <path d="M7 10l2 2 3-3"></path>
                    </svg>
                </span>
                <span class="shell-top-action">
                    <svg class="shell-top-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M5 15a7 7 0 0 1 10 0"></path>
                        <path d="M8 12a4.5 4.5 0 0 1 6 0"></path>
                        <path d="M11.5 9.5a2 2 0 0 1 1 0"></path>
                        <path d="M5 6l14 12"></path>
                    </svg>
                </span>
                <span class="shell-top-action">
                    <svg class="shell-top-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M12 5a4 4 0 0 1 4 4v3.5l1.7 2.2H6.3L8 12.5V9a4 4 0 0 1 4-4z"></path>
                        <path d="M10 18a2 2 0 0 0 4 0"></path>
                    </svg>
                    <span class="shell-top-action-badge">5</span>
                </span>
            </div>
            <span class="shell-top-sep"></span>
            <div class="shell-top-actions">
                <span class="shell-top-action">
                    <svg class="shell-top-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <circle cx="12" cy="12" r="6"></circle>
                        <circle cx="12" cy="12" r="2.2"></circle>
                        <path d="M12 3v3M12 18v3M3 12h3M18 12h3"></path>
                    </svg>
                </span>
            </div>
        </div>
    </div>
    <div class="shell-sidebar">
        <div class="shell-nav-head">
            <span class="shell-nav-head-left"><span>Navigation</span><span class="shell-nav-timer">Toggle timer</span></span>
            <span class="shell-nav-toggle"></span>
        </div>
        <div class="shell-menu">
            <div class="shell-menu-item"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11l9-7 9 7"></path><path d="M5 10v10h14V10"></path><path d="M10 20v-6h4v6"></path></svg></span><span class="shell-menu-item-label">Home</span></div>
            <div class="shell-menu-item"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="1.5"></rect><path d="M8 20h8M12 16v4"></path></svg></span><span class="shell-menu-item-label">Sinottico</span></div>
            <div class="shell-menu-item"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4a4 4 0 0 1 4 4v3.5l1.8 2.3H6.2L8 11.5V8a4 4 0 0 1 4-4z"></path><path d="M10.5 18a1.5 1.5 0 0 0 3 0"></path></svg></span><span class="shell-menu-item-label">Storico eventi/allarmi</span></div>
            <div class="shell-menu-item"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="11" height="8" rx="1.5"></rect><path d="M14 9h4l3 2.5V15h-7"></path><circle class="shell-menu-icon-fill" cx="8" cy="16.5" r="1.7"></circle><circle class="shell-menu-icon-fill" cx="18" cy="16.5" r="1.7"></circle></svg></span><span class="shell-menu-item-label">Gestione transiti</span><span class="shell-menu-caret">&#9662;</span></div>
            <div class="shell-menu-item"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="11" height="8" rx="1.5"></rect><path d="M14 9h4l3 2.5V15h-7"></path><circle class="shell-menu-icon-fill" cx="8" cy="16.5" r="1.7"></circle><circle class="shell-menu-icon-fill" cx="18" cy="16.5" r="1.7"></circle></svg></span><span class="shell-menu-item-label">Varco carrabile</span><span class="shell-menu-caret">&#9662;</span></div>
            <div class="shell-menu-item"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 6h14v9H9l-4 3v-3H5z"></path></svg></span><span class="shell-menu-item-label">Notifiche</span><span class="shell-menu-caret">&#9662;</span></div>
            <div class="shell-menu-item"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3"></circle><path d="M12 2.8v2.4M12 18.8v2.4M4.9 4.9l1.7 1.7M17.4 17.4l1.7 1.7M2.8 12h2.4M18.8 12h2.4M4.9 19.1l1.7-1.7M17.4 6.6l1.7-1.7"></path></svg></span><span class="shell-menu-item-label">Configurazioni</span><span class="shell-menu-caret">&#9662;</span></div>
            <div class="shell-menu-item"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 6h12M8 12h12M8 18h12"></path><circle class="shell-menu-icon-fill" cx="4.5" cy="6" r="1.2"></circle><circle class="shell-menu-icon-fill" cx="4.5" cy="12" r="1.2"></circle><circle class="shell-menu-icon-fill" cx="4.5" cy="18" r="1.2"></circle></svg></span><span class="shell-menu-item-label">Audit</span></div>
            <div class="shell-menu-item shell-menu-item-active"><span class="shell-menu-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 3h4"></path><path d="M11 3v5l-5.5 9a2 2 0 0 0 1.7 3h9.6a2 2 0 0 0 1.7-3L13 8V3"></path><path d="M8.5 13h7"></path></svg></span><span class="shell-menu-item-label">Gestione miscele</span></div>
        </div>
    </div>
    <div class="shell-subtop">
        <span class="shell-subtop-title">SKYsym_Web v.2.2.1.61 - Skyline</span>
        <span class="shell-subtop-path"><span class="shell-subtop-homeicon">&#8962;</span><span>/ Home</span></span>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.page_mode == "output":
    if "abbatt_cod_output" not in st.session_state:
        st.session_state.abbatt_cod_output = int(st.session_state.cod_reduction_pct)
    abbatt_display = st.session_state.abbatt_cod_output

    _default_tk125 = [
        {"Componente": "Residuo TK-125", "Volume": 15, "COD": 47000, "Solventi": 740, "Boro": 4.0},
        {"Componente": "S-01",           "Volume": 18, "COD": 52000, "Solventi": 780, "Boro": 4.2},
        {"Componente": "S-07",           "Volume": 17, "COD": 31000, "Solventi":  95, "Boro": 2.9},
        {"Componente": "S-06",           "Volume":  5, "COD": 59000, "Solventi": 640, "Boro": 3.4},
        {"Componente": "S-ALTO",         "Volume":  2, "COD":110000, "Solventi":2900, "Boro": 5.1},
    ]
    _default_tk126 = [
        {"Componente": "Residuo TK-126", "Volume": 10, "COD": 45500, "Solventi": 720, "Boro": 3.8},
        {"Componente": "S-07",           "Volume": 12, "COD": 31000, "Solventi":  95, "Boro": 2.9},
        {"Componente": "S-01",           "Volume": 10, "COD": 52000, "Solventi": 780, "Boro": 4.2},
        {"Componente": "S-06",           "Volume":  8, "COD": 59000, "Solventi": 640, "Boro": 3.4},
    ]
    _default_b_tk125 = [
        {"Componente": "Residuo TK-125", "Volume": 14, "COD": 47000, "Solventi":  740, "Boro": 4.0},
        {"Componente": "S-01",           "Volume": 16, "COD": 52000, "Solventi":  780, "Boro": 4.2},
        {"Componente": "S-07",           "Volume": 18, "COD": 31000, "Solventi":   95, "Boro": 2.9},
        {"Componente": "S-06",           "Volume":  6, "COD": 59000, "Solventi":  640, "Boro": 3.4},
        {"Componente": "S-02",           "Volume":  3, "COD": 86000, "Solventi": 1320, "Boro": 4.5},
    ]
    _default_b_tk126 = [
        {"Componente": "Residuo TK-126", "Volume": 10, "COD": 45500, "Solventi": 720, "Boro": 3.8},
        {"Componente": "S-01",           "Volume": 15, "COD": 52000, "Solventi": 780, "Boro": 4.2},
        {"Componente": "S-06",           "Volume":  7, "COD": 59000, "Solventi": 640, "Boro": 3.4},
        {"Componente": "S-07",           "Volume":  8, "COD": 31000, "Solventi":  95, "Boro": 2.9},
    ]
    _compare_options = ["", "Scenario B", "Scenario C", "Scenario D", "Scenario E", "Scenario F"]
    _base_compare_scenario = ""
    if st.session_state.output_has_scenario_a_plus:
        _current_scenario_label = str(st.session_state.current_scenario).strip()
        _base_compare_scenario = _current_scenario_label.rstrip("+").strip()
        if not _base_compare_scenario:
            _base_compare_scenario = "Scenario A"
        _compare_options = ["", _base_compare_scenario] + _compare_options[1:]
    compare_choice = (
        st.session_state.output_compare_scenario
        if st.session_state.output_compare_scenario in _compare_options
        else ""
    )
    if compare_choice != st.session_state.output_compare_scenario:
        st.session_state.output_compare_scenario = compare_choice
    compare_active = compare_choice != ""

    if st.session_state.out_recipe_tk125 is None:
        st.session_state.out_recipe_tk125 = pd.DataFrame(_default_tk125)
    if st.session_state.out_recipe_tk126 is None:
        st.session_state.out_recipe_tk126 = pd.DataFrame(_default_tk126)
    if compare_active and st.session_state.out_recipe_b_tk125 is None:
        if _base_compare_scenario and compare_choice == _base_compare_scenario:
            st.session_state.out_recipe_b_tk125 = st.session_state.out_recipe_tk125.copy(deep=True)
        else:
            st.session_state.out_recipe_b_tk125 = pd.DataFrame(_default_b_tk125)
    if compare_active and st.session_state.out_recipe_b_tk126 is None:
        if _base_compare_scenario and compare_choice == _base_compare_scenario:
            st.session_state.out_recipe_b_tk126 = st.session_state.out_recipe_tk126.copy(deep=True)
        else:
            st.session_state.out_recipe_b_tk126 = pd.DataFrame(_default_b_tk126)
    if not compare_active:
        st.session_state.out_recipe_b_tk125 = None
        st.session_state.out_recipe_b_tk126 = None

    def _recompute_quota(df):
        total = df["Volume"].sum()
        df = df.copy()
        df["Quota %"] = (df["Volume"] / total * 100).round(1) if total > 0 else 0.0
        return df

    _empty_recipe = pd.DataFrame(columns=["Componente", "Volume", "COD", "Solventi", "Boro"])
    recipe_tk125 = _recompute_quota(st.session_state.out_recipe_tk125)
    recipe_tk126 = _recompute_quota(st.session_state.out_recipe_tk126)
    recipe_b_tk125 = _recompute_quota(st.session_state.out_recipe_b_tk125 if st.session_state.out_recipe_b_tk125 is not None else _empty_recipe)
    recipe_b_tk126 = _recompute_quota(st.session_state.out_recipe_b_tk126 if st.session_state.out_recipe_b_tk126 is not None else _empty_recipe)

    _vol_125_top = int(recipe_tk125["Volume"].sum())
    _vol_126_top = int(recipe_tk126["Volume"].sum())
    _vol_125_b = int(recipe_b_tk125["Volume"].sum())
    _vol_126_b = int(recipe_b_tk126["Volume"].sum())
    _cod_125_top = int((recipe_tk125["Volume"] * recipe_tk125["COD"]).sum() / _vol_125_top) if _vol_125_top > 0 else 0
    _cod_126_top = int((recipe_tk126["Volume"] * recipe_tk126["COD"]).sum() / _vol_126_top) if _vol_126_top > 0 else 0
    _cod_125_b = int((recipe_b_tk125["Volume"] * recipe_b_tk125["COD"]).sum() / _vol_125_b) if _vol_125_b > 0 else 0
    _cod_126_b = int((recipe_b_tk126["Volume"] * recipe_b_tk126["COD"]).sum() / _vol_126_b) if _vol_126_b > 0 else 0
    _sol_125_top = int((recipe_tk125["Volume"] * recipe_tk125["Solventi"]).sum() / _vol_125_top) if _vol_125_top > 0 else 0
    _sol_126_top = int((recipe_tk126["Volume"] * recipe_tk126["Solventi"]).sum() / _vol_126_top) if _vol_126_top > 0 else 0
    _sol_125_b = int((recipe_b_tk125["Volume"] * recipe_b_tk125["Solventi"]).sum() / _vol_125_b) if _vol_125_b > 0 else 0
    _sol_126_b = int((recipe_b_tk126["Volume"] * recipe_b_tk126["Solventi"]).sum() / _vol_126_b) if _vol_126_b > 0 else 0
    _COD_125_MIN, _COD_125_MAX = 44000, 48000
    _COD_126_MIN, _COD_126_MAX = 43000, 47000
    _cod_125_ok = _COD_125_MIN <= _cod_125_top <= _COD_125_MAX
    _cod_126_ok = _COD_126_MIN <= _cod_126_top <= _COD_126_MAX

    def _range_esito(value, min_value, max_value):
        if min_value <= value <= max_value:
            return "Nel range", "esito-ok"
        if value > max_value:
            return "Fuori range (alto)", "esito-warn"
        return "Fuori range (basso)", "esito-warn"

    _esito_126_a, _esito_cls_126_a = _range_esito(_cod_126_top, _COD_126_MIN, _COD_126_MAX)
    if compare_active:
        _esito_126_b, _esito_cls_126_b = _range_esito(_cod_126_b, _COD_126_MIN, _COD_126_MAX)
        _compare_label = compare_choice
        _cod_126_b_display = str(_cod_126_b)
        _sol_126_b_display = f"{_sol_126_b} mg/l"
    else:
        _esito_126_b, _esito_cls_126_b = "Non valutato", ""
        _compare_label = "Nessuna"
        _cod_126_b_display = "-"
        _sol_126_b_display = "-"

    st.markdown(
        '<div class="top-titlebar">Creazione e ottimizzazione miscele TOP - Risultato e confronto miscele</div>',
        unsafe_allow_html=True,
    )

    output_toolbar = st.container(key="output_toolbar", width="stretch")
    with output_toolbar:
        left_actions, right_badges = st.columns([3.5, 1.5], gap="small")
        with left_actions:
            c1, c2, _ = st.columns([1.55, 1.5, 5.95], gap="small")
            with c1:
                if st.button("Modifica scenario", width="content", key="btn_out_mod_scenario"):
                    st.session_state.page_mode = "config"
                    st.rerun()
            with c2:
                if st.button("Duplica Scenario", width="content", key="btn_out_dup"):
                    _base_scenario = str(st.session_state.current_scenario).strip().rstrip("+").strip()
                    if not _base_scenario:
                        _base_scenario = "Scenario A"
                    st.session_state.out_recipe_b_tk125 = st.session_state.out_recipe_tk125.copy(deep=True)
                    st.session_state.out_recipe_b_tk126 = st.session_state.out_recipe_tk126.copy(deep=True)
                    st.session_state.output_has_scenario_a_plus = True
                    st.session_state.current_scenario = f"{_base_scenario}+"
                    st.session_state.output_compare_scenario = _base_scenario
                    st.rerun()
        with right_badges:
            _, rc = st.columns([0.1, 1.2], gap="small")
            with rc:
                st.markdown(
                    f'<div class="top-chip" style="float:right">{st.session_state.current_scenario}</div>',
                    unsafe_allow_html=True,
                )

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6, gap="small")
    with kpi1:
        st.markdown('<div class="output-kpi"><div class="output-kpi-title">Serbatoi attivi</div><div class="output-kpi-value">2</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="output-kpi"><div class="output-kpi-title">Volume totale</div><div class="output-kpi-value">{_vol_125_top + _vol_126_top} m3</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="output-kpi"><div class="output-kpi-title">Componenti</div><div class="output-kpi-value">{len(recipe_tk125) + len(recipe_tk126)}</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown('<div class="output-kpi"><div class="output-kpi-title">TK-125 COD target</div><div class="output-kpi-value">44000 - 48000</div></div>', unsafe_allow_html=True)
    with kpi5:
        st.markdown('<div class="output-kpi"><div class="output-kpi-title">TK-126 COD target</div><div class="output-kpi-value">43000 - 47000</div></div>', unsafe_allow_html=True)
    with kpi6:
        st.markdown('<div class="output-kpi"><div class="output-kpi-title">Verifica vincoli</div><div class="output-kpi-value" style="color:#2e7d32">OK</div></div>', unsafe_allow_html=True)

    out_left, out_right = st.columns([2.0, 1.0], gap="medium")

    with out_left:
        output_recipe_box = st.container(key="output_recipe_box", width="stretch")
        with output_recipe_box:
            st.markdown('<div class="right-main-title">Miscele TOP proposte</div>', unsafe_allow_html=True)
            tab_a_label = st.session_state.current_scenario
            tab_b_label = compare_choice if compare_choice else "Scenario confronto"
            tab_a, tab_b, tab_cmp = st.tabs([tab_a_label, tab_b_label, "Confronto"])

            with tab_a:
                tank_125, tank_126 = st.tabs(["TK-125", "TK-126"])

                with tank_125:
                    st.markdown("""<div class="tank-target-box">
                        <div class="tank-target-row">
                            <span class="tgt-chip">COD target <b>44000 - 48000</b></span>
                            <span class="tgt-chip">Solventi max <b>800</b></span>
                            <span class="tgt-chip">Vol min <b>40</b></span>
                            <span class="tgt-chip">Vol max <b>60</b></span>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown('<div class="out-section-label" style="margin-top:10px">Componenti consigliati</div>', unsafe_allow_html=True)
                    _ev_125 = st.dataframe(
                        recipe_tk125,
                        width="stretch",
                        hide_index=True,
                        height=215,
                        on_select="rerun",
                        selection_mode="single-row",
                        column_config={
                            "Componente": st.column_config.TextColumn("Componente", width="medium"),
                            "Volume":    st.column_config.NumberColumn("Volume",    format="%d",   width="small"),
                            "COD":       st.column_config.NumberColumn("COD",       format="%d",   width="small"),
                            "Solventi":  st.column_config.NumberColumn("Solventi",  format="%d",   width="small"),
                            "Boro":      st.column_config.NumberColumn("Boro",      format="%.1f", width="small"),
                            "Quota %":   st.column_config.NumberColumn("Quota %",   format="%.1f", width="small"),
                        },
                    )
                    if st.button("+ Aggiungi componente", key="btn_add_comp_tk125"):
                        st.session_state.show_add_comp_tk125 = not st.session_state.show_add_comp_tk125
                    if st.session_state.show_add_comp_tk125:
                        _existing_125 = set(st.session_state.out_recipe_tk125["Componente"].tolist())
                        _tank_opts_125 = [t["tank"] for t in st.session_state.source_tanks if t["tank"] not in _existing_125]
                        _volume_opts_125 = list(range(1, 101))
                        _sel_col, _vol_col, _add_col, _ann_col = st.columns([2.3, 1.1, 1, 1], gap="small")
                        with _sel_col:
                            _new_tank_125 = st.selectbox(
                                "Serbatoio",
                                _tank_opts_125,
                                index=None,
                                placeholder="Seleziona serbatoio",
                                key="add_comp_sel_tk125",
                                label_visibility="collapsed",
                            )
                        with _vol_col:
                            _new_vol_125 = st.selectbox(
                                "Volume nuovo componente TK-125",
                                options=_volume_opts_125,
                                index=None,
                                placeholder="Volume",
                                key="add_comp_vol_sel_tk125",
                                label_visibility="collapsed",
                            )
                        with _add_col:
                            if st.button("Aggiungi", key="btn_add_comp_confirm_tk125"):
                                _tank_data = next((t for t in st.session_state.source_tanks if t["tank"] == _new_tank_125), None)
                                if _tank_data and _new_vol_125 is not None:
                                    _new_row = pd.DataFrame([{
                                        "Componente": _tank_data["tank"],
                                        "Volume": int(_new_vol_125),
                                        "COD": safe_int_input(_tank_data.get("cod")),
                                        "Solventi": safe_int_input(_tank_data.get("solvents")),
                                        "Boro": _tank_data["boro"],
                                    }])
                                    st.session_state.out_recipe_tk125 = pd.concat(
                                        [st.session_state.out_recipe_tk125, _new_row], ignore_index=True
                                    )
                                    st.session_state.show_add_comp_tk125 = False
                                    st.rerun()
                                st.warning("Seleziona serbatoio e volume.", icon="\u26a0\ufe0f")
                        with _ann_col:
                            if st.button("Annulla", key="btn_add_comp_cancel_tk125"):
                                st.session_state.show_add_comp_tk125 = False
                                st.rerun()
                    _vol_125 = int(recipe_tk125["Volume"].sum())
                    _cod_125 = int((recipe_tk125["Volume"] * recipe_tk125["COD"]).sum() / _vol_125) if _vol_125 > 0 else 0
                    _sol_125 = int((recipe_tk125["Volume"] * recipe_tk125["Solventi"]).sum() / _vol_125) if _vol_125 > 0 else 0
                    st.markdown(f"""<div class="tank-summary-row">
                        <span>Volume finale <b>{_vol_125} m3</b></span>
                        <span>COD miscela <b style="color:#2f5bb4">{_cod_125}</b></span>
                        <span>Solventi <b>{_sol_125}</b></span>
                    </div>""", unsafe_allow_html=True)
                    _sel_rows_125 = _ev_125.selection.rows
                    if _sel_rows_125:
                        _si = _sel_rows_125[0]
                        _sc = recipe_tk125.iloc[_si]["Componente"]
                        _vc, _rc = st.columns([3, 1], gap="small")
                        with _vc:
                            _new_vol_125 = st.number_input(
                                f"Volume - {_sc}", min_value=0, step=1,
                                value=int(recipe_tk125.iloc[_si]["Volume"]),
                                key=f"vol_edit_tk125_{_si}",
                            )
                            if st.button("Aggiorna volume", key="btn_vol_upd_tk125"):
                                st.session_state.out_recipe_tk125.at[_si, "Volume"] = _new_vol_125
                                st.rerun()
                        with _rc:
                            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                            if st.button("Rimuovi", key="btn_rem_row_tk125"):
                                st.session_state.out_recipe_tk125 = (
                                    st.session_state.out_recipe_tk125
                                    .drop(index=_si).reset_index(drop=True)
                                )
                                st.rerun()
                with tank_126:
                    st.markdown("""<div class="tank-target-box">
                        <div class="tank-target-row">
                            <span class="tgt-chip">COD target <b>43000 - 47000</b></span>
                            <span class="tgt-chip">Solventi max <b>750</b></span>
                            <span class="tgt-chip">Vol min <b>20</b></span>
                            <span class="tgt-chip">Vol max <b>40</b></span>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown('<div class="out-section-label" style="margin-top:10px">Componenti consigliati</div>', unsafe_allow_html=True)
                    _ev_126 = st.dataframe(
                        recipe_tk126,
                        width="stretch",
                        hide_index=True,
                        height=215,
                        on_select="rerun",
                        selection_mode="single-row",
                        column_config={
                            "Componente": st.column_config.TextColumn("Componente", width="medium"),
                            "Volume":    st.column_config.NumberColumn("Volume",    format="%d",   width="small"),
                            "COD":       st.column_config.NumberColumn("COD",       format="%d",   width="small"),
                            "Solventi":  st.column_config.NumberColumn("Solventi",  format="%d",   width="small"),
                            "Boro":      st.column_config.NumberColumn("Boro",      format="%.1f", width="small"),
                            "Quota %":   st.column_config.NumberColumn("Quota %",   format="%.1f", width="small"),
                        },
                    )
                    if st.button("+ Aggiungi componente", key="btn_add_comp_tk126"):
                        st.session_state.show_add_comp_tk126 = not st.session_state.show_add_comp_tk126
                    if st.session_state.show_add_comp_tk126:
                        _existing_126 = set(st.session_state.out_recipe_tk126["Componente"].tolist())
                        _tank_opts_126 = [t["tank"] for t in st.session_state.source_tanks if t["tank"] not in _existing_126]
                        _volume_opts_126 = list(range(1, 101))
                        _sel_col, _vol_col, _add_col, _ann_col = st.columns([2.3, 1.1, 1, 1], gap="small")
                        with _sel_col:
                            _new_tank_126 = st.selectbox(
                                "Serbatoio",
                                _tank_opts_126,
                                index=None,
                                placeholder="Seleziona serbatoio",
                                key="add_comp_sel_tk126",
                                label_visibility="collapsed",
                            )
                        with _vol_col:
                            _new_vol_126 = st.selectbox(
                                "Volume nuovo componente TK-126",
                                options=_volume_opts_126,
                                index=None,
                                placeholder="Volume",
                                key="add_comp_vol_sel_tk126",
                                label_visibility="collapsed",
                            )
                        with _add_col:
                            if st.button("Aggiungi", key="btn_add_comp_confirm_tk126"):
                                _tank_data = next((t for t in st.session_state.source_tanks if t["tank"] == _new_tank_126), None)
                                if _tank_data and _new_vol_126 is not None:
                                    _new_row = pd.DataFrame([{
                                        "Componente": _tank_data["tank"],
                                        "Volume": int(_new_vol_126),
                                        "COD": safe_int_input(_tank_data.get("cod")),
                                        "Solventi": safe_int_input(_tank_data.get("solvents")),
                                        "Boro": _tank_data["boro"],
                                    }])
                                    st.session_state.out_recipe_tk126 = pd.concat(
                                        [st.session_state.out_recipe_tk126, _new_row], ignore_index=True
                                    )
                                    st.session_state.show_add_comp_tk126 = False
                                    st.rerun()
                                st.warning("Seleziona serbatoio e volume.", icon="\u26a0\ufe0f")
                        with _ann_col:
                            if st.button("Annulla", key="btn_add_comp_cancel_tk126"):
                                st.session_state.show_add_comp_tk126 = False
                                st.rerun()
                    _vol_126 = int(recipe_tk126["Volume"].sum())
                    _cod_126 = int((recipe_tk126["Volume"] * recipe_tk126["COD"]).sum() / _vol_126) if _vol_126 > 0 else 0
                    _sol_126 = int((recipe_tk126["Volume"] * recipe_tk126["Solventi"]).sum() / _vol_126) if _vol_126 > 0 else 0
                    st.markdown(f"""<div class="tank-summary-row">
                        <span>Volume finale <b>{_vol_126} m3</b></span>
                        <span>COD miscela <b style="color:#e08c00">{_cod_126}</b></span>
                        <span>Solventi <b>{_sol_126}</b></span>
                    </div>""", unsafe_allow_html=True)
                    _sel_rows_126 = _ev_126.selection.rows
                    if _sel_rows_126:
                        _si = _sel_rows_126[0]
                        _sc = recipe_tk126.iloc[_si]["Componente"]
                        _vc, _rc = st.columns([3, 1], gap="small")
                        with _vc:
                            _new_vol_126 = st.number_input(
                                f"Volume - {_sc}", min_value=0, step=1,
                                value=int(recipe_tk126.iloc[_si]["Volume"]),
                                key=f"vol_edit_tk126_{_si}",
                            )
                            if st.button("Aggiorna volume", key="btn_vol_upd_tk126"):
                                st.session_state.out_recipe_tk126.at[_si, "Volume"] = _new_vol_126
                                st.rerun()
                        with _rc:
                            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                            if st.button("Rimuovi", key="btn_rem_row_tk126"):
                                st.session_state.out_recipe_tk126 = (
                                    st.session_state.out_recipe_tk126
                                    .drop(index=_si).reset_index(drop=True)
                                )
                                st.rerun()
                st.markdown('<div class="right-main-title" style="margin-top:16px">Parametri attesi in ingresso e uscita da Top</div>', unsafe_allow_html=True)
                ab_l, ab_m, ab_r, _ = st.columns([2.0, 0.7, 0.3, 5.0], gap="small")
                with ab_l:
                    st.markdown('<p style="font-size:12px;color:#546273;margin:0;padding-top:8px">Abbattimento COD previsto</p>', unsafe_allow_html=True)
                with ab_m:
                    st.number_input("abbatt", min_value=0, max_value=100, step=1,
                        key="abbatt_cod_output", label_visibility="collapsed")
                with ab_r:
                    st.markdown('<p style="font-size:12px;color:#7b8794;margin:0;padding-top:8px">%</p>', unsafe_allow_html=True)
                st.session_state.cod_reduction_pct = st.session_state.abbatt_cod_output

                par_l, par_r = st.columns(2, gap="medium")
                with par_l:
                    st.markdown('<div class="tank-table-title">TK-125</div>', unsafe_allow_html=True)
                    st.markdown(f"""<div class="param-list">
                        <div class="param-row"><span>COD atteso miscela</span><b>{_cod_125_top}</b></div>
                        <div class="param-row"><span>Solventi attesi</span><b>{_sol_125_top} mg/l</b></div>
                        <div class="param-row"><span>Cl atteso</span><b>108</b></div>
                        <div class="param-row"><span>COD atteso dopo abbattimento</span><b>{int(_cod_125_top * abbatt_display / 100)}</b></div>
                    </div>""", unsafe_allow_html=True)
                with par_r:
                    st.markdown('<div class="tank-table-title">TK-126</div>', unsafe_allow_html=True)
                    st.markdown(f"""<div class="param-list">
                        <div class="param-row"><span>COD atteso miscela</span><b>{_cod_126_top}</b></div>
                        <div class="param-row"><span>Solventi attesi</span><b>{_sol_126_top} mg/l</b></div>
                        <div class="param-row"><span>Cl atteso</span><b>98</b></div>
                        <div class="param-row"><span>COD atteso dopo abbattimento</span><b>{int(_cod_126_top * abbatt_display / 100)}</b></div>
                    </div>""", unsafe_allow_html=True)

            with tab_b:
                if not compare_active:
                    st.markdown('<div style="color:#8b97a4;font-size:13px;padding:20px 4px">Nessuna miscela di confronto selezionata. Seleziona una miscela dal box "Confronto miscele" nella barra laterale destra.</div>', unsafe_allow_html=True)
                else:
                    tank_125_b, tank_126_b = st.tabs(["TK-125", "TK-126"])

                    with tank_125_b:
                        st.markdown("""<div class="tank-target-box">
                            <div class="tank-target-row">
                                <span class="tgt-chip">COD target <b>44000 - 48000</b></span>
                                <span class="tgt-chip">Solventi max <b>800</b></span>
                                <span class="tgt-chip">Vol min <b>40</b></span>
                                <span class="tgt-chip">Vol max <b>60</b></span>
                            </div>
                        </div>""", unsafe_allow_html=True)
                        st.markdown('<div class="out-section-label" style="margin-top:10px">Componenti proposti</div>', unsafe_allow_html=True)
                        st.dataframe(
                            recipe_b_tk125,
                            width="stretch",
                            hide_index=True,
                            height=215,
                            column_config={
                                "Componente": st.column_config.TextColumn("Componente", width="medium"),
                                "Volume":    st.column_config.NumberColumn("Volume",    format="%d",   width="small"),
                                "COD":       st.column_config.NumberColumn("COD",       format="%d",   width="small"),
                                "Solventi":  st.column_config.NumberColumn("Solventi",  format="%d",   width="small"),
                                "Boro":      st.column_config.NumberColumn("Boro",      format="%.1f", width="small"),
                                "Quota %":   st.column_config.NumberColumn("Quota %",   format="%.1f", width="small"),
                            },
                        )
                        st.markdown(f"""<div class="tank-summary-row">
                            <span>Volume finale <b>{_vol_125_b} m3</b></span>
                            <span>COD miscela <b style="color:#2f5bb4">{_cod_125_b}</b></span>
                            <span>Solventi <b>{_sol_125_b}</b></span>
                        </div>""", unsafe_allow_html=True)

                    with tank_126_b:
                        st.markdown("""<div class="tank-target-box">
                            <div class="tank-target-row">
                                <span class="tgt-chip">COD target <b>43000 - 47000</b></span>
                                <span class="tgt-chip">Solventi max <b>750</b></span>
                                <span class="tgt-chip">Vol min <b>20</b></span>
                                <span class="tgt-chip">Vol max <b>40</b></span>
                            </div>
                        </div>""", unsafe_allow_html=True)
                        st.markdown('<div class="out-section-label" style="margin-top:10px">Componenti proposti</div>', unsafe_allow_html=True)
                        st.dataframe(
                            recipe_b_tk126,
                            width="stretch",
                            hide_index=True,
                            height=215,
                            column_config={
                                "Componente": st.column_config.TextColumn("Componente", width="medium"),
                                "Volume":    st.column_config.NumberColumn("Volume",    format="%d",   width="small"),
                                "COD":       st.column_config.NumberColumn("COD",       format="%d",   width="small"),
                                "Solventi":  st.column_config.NumberColumn("Solventi",  format="%d",   width="small"),
                                "Boro":      st.column_config.NumberColumn("Boro",      format="%.1f", width="small"),
                                "Quota %":   st.column_config.NumberColumn("Quota %",   format="%.1f", width="small"),
                            },
                        )
                        st.markdown(f"""<div class="tank-summary-row">
                            <span>Volume finale <b>{_vol_126_b} m3</b></span>
                            <span>COD miscela <b style="color:#e08c00">{_cod_126_b}</b></span>
                            <span>Solventi <b>{_sol_126_b}</b></span>
                        </div>""", unsafe_allow_html=True)

                    st.markdown('<div class="right-main-title" style="margin-top:16px">Parametri attesi in ingresso e uscita da Top</div>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size:12px;color:#546273;margin:0 0 8px 0">Abbattimento COD previsto: <b>{abbatt_display}%</b></p>', unsafe_allow_html=True)
                    par_b_l, par_b_r = st.columns(2, gap="medium")
                    with par_b_l:
                        st.markdown('<div class="tank-table-title">TK-125</div>', unsafe_allow_html=True)
                        st.markdown(f"""<div class="param-list">
                            <div class="param-row"><span>COD atteso miscela</span><b>{_cod_125_b}</b></div>
                            <div class="param-row"><span>Solventi attesi</span><b>{_sol_125_b} mg/l</b></div>
                            <div class="param-row"><span>Cl atteso</span><b>106</b></div>
                            <div class="param-row"><span>COD atteso dopo abbattimento</span><b>{int(_cod_125_b * abbatt_display / 100)}</b></div>
                        </div>""", unsafe_allow_html=True)
                    with par_b_r:
                        st.markdown('<div class="tank-table-title">TK-126</div>', unsafe_allow_html=True)
                        st.markdown(f"""<div class="param-list">
                            <div class="param-row"><span>COD atteso miscela</span><b>{_cod_126_b}</b></div>
                            <div class="param-row"><span>Solventi attesi</span><b>{_sol_126_b} mg/l</b></div>
                            <div class="param-row"><span>Cl atteso</span><b>100</b></div>
                            <div class="param-row"><span>COD atteso dopo abbattimento</span><b>{int(_cod_126_b * abbatt_display / 100)}</b></div>
                        </div>""", unsafe_allow_html=True)

    with out_right:
        with st.container(key="out_right_confronto", width="stretch"):
            st.markdown('<div class="left-subpanel-title">Confronto miscele</div>', unsafe_allow_html=True)
            st.selectbox(
                "Miscela di confronto",
                options=_compare_options,
                format_func=lambda x: "Seleziona miscela di confronto..." if x == "" else x,
                key="output_compare_scenario",
                label_visibility="collapsed",
            )
            cr1, cr2 = st.columns(2, gap="small")
            with cr1:
                st.markdown(
                    f'<div style="font-size:11px;color:#7b8794;margin-bottom:3px">Miscela da confrontare</div>'
                    f'<div class="conf-chip-sel">{_compare_label}</div>',
                    unsafe_allow_html=True,
                )
            with cr2:
                st.markdown('<div style="font-size:11px;color:#7b8794;margin-bottom:3px">Serbatoio di riferimento</div><div class="conf-chip-sel">TK-126</div>', unsafe_allow_html=True)
            ca, cb = st.columns(2, gap="small")
            with ca:
                st.markdown(f"""<div class="cmp-card">
                    <div class="cmp-card-title">{st.session_state.current_scenario}</div>
                    <div class="cmp-row">COD TK-126 <b style="color:#e08c00">{_cod_126_top}</b></div>
                    <div class="cmp-row">Solventi <b>{_sol_126_top} mg/l</b></div>
                    <div class="cmp-row {_esito_cls_126_a}">Esito &nbsp;<b>{_esito_126_a}</b></div>
                </div>""", unsafe_allow_html=True)
            with cb:
                st.markdown(f"""<div class="cmp-card">
                    <div class="cmp-card-title">{_compare_label if compare_active else "Scenario confronto"}</div>
                    <div class="cmp-row">COD TK-126 <b style="color:#e08c00">{_cod_126_b_display}</b></div>
                    <div class="cmp-row">Solventi <b>{_sol_126_b_display}</b></div>
                    <div class="cmp-row {_esito_cls_126_b}">Esito &nbsp;<b>{_esito_126_b}</b></div>
                </div>""", unsafe_allow_html=True)

        with st.container(key="out_right_criticita", width="stretch"):
            st.markdown('<div class="left-subpanel-title">Criticita di miscela</div>', unsafe_allow_html=True)
            _crit_items = []
            if not _cod_125_ok:
                _dir_125 = "superiore" if _cod_125_top > _COD_125_MAX else "inferiore"
                _crit_items.append(f"""<div class="crit-item crit-error">
                    <div class="crit-title">TK-125 - COD miscela fuori range</div>
                    <div class="crit-body">COD {_cod_125_top} oltre il limite {_dir_125} ({_COD_125_MIN}-{_COD_125_MAX})</div>
                </div>""")
            if not _cod_126_ok:
                _dir_126 = "superiore" if _cod_126_top > _COD_126_MAX else "inferiore"
                _crit_items.append(f"""<div class="crit-item crit-error" style="margin-top:6px">
                    <div class="crit-title">TK-126 - COD miscela fuori range</div>
                    <div class="crit-body">COD {_cod_126_top} oltre il limite {_dir_126} ({_COD_126_MIN}-{_COD_126_MAX})</div>
                </div>""")
            _crit_items.append(f"""<div class="crit-item crit-warn" style="margin-top:6px">
                    <div class="crit-title">TK-126 - COD miscela</div>
                    <div class="crit-body">Vicino al limite superiore del range target</div>
                </div>
                <div class="crit-item crit-warn" style="margin-top:6px">
                    <div class="crit-title">TK-126 - Solventi miscela</div>
                    <div class="crit-body">Valore sotto il limite ma da monitorare</div>
                </div>
                <div class="crit-item crit-info" style="margin-top:6px">
                    <div class="crit-title">TK-127</div>
                    <div class="crit-body">Non coinvolto perche il serbatoio non e selezionato</div>
                </div>""")
            st.markdown("\n".join(_crit_items), unsafe_allow_html=True)

        with st.container(key="out_right_azioni", width="stretch"):
            st.markdown('<div class="left-subpanel-title">Azioni sul risultato</div>', unsafe_allow_html=True)
            st.button("Export Risultati", width="stretch", key="btn_out_export_right")
            st.button("Export Report", width="stretch", key="btn_out_export_report_right")
            st.button("Conferma miscele TOP", width="stretch", type="primary", key="btn_out_confirm_right")

    st.stop()

scenario_scope = st.session_state.get("scenario_scope", SCENARIO_SCOPE_TOP)
if scenario_scope not in {SCENARIO_SCOPE_TOP, SCENARIO_SCOPE_ALL}:
    scenario_scope = SCENARIO_SCOPE_TOP
st.session_state.scenario_scope = scenario_scope

if scenario_scope == SCENARIO_SCOPE_ALL:
    st.session_state.config_mode = "simulation"
    st.session_state.destination_view_mode = "Tutti i serbatoi"
else:
    st.session_state.destination_view_mode = "Serbatoi TOP"

config_mode = st.session_state.config_mode if st.session_state.config_mode in {"simulation", "optimization"} else "optimization"
if scenario_scope == SCENARIO_SCOPE_ALL:
    config_mode = "simulation"
st.session_state.config_mode = config_mode
is_simulation_mode = config_mode == "simulation"
config_title = "Movimenti tra serbatoi - Simulazione" if is_simulation_mode else "Gestione Miscele - Configurazione"
scenario_label = get_display_scenario_label()
show_plant_badge = not (
    is_simulation_mode
    and st.session_state.get("destination_view_mode") == "Tutti i serbatoi"
)

st.markdown(
    f'<div class="top-titlebar">{config_title}</div>',
    unsafe_allow_html=True,
)

toolbar = st.container(key="top_toolbar", width="stretch")
with toolbar:
    left_actions, _ = st.columns([5.8, 0.2], gap="small")

    with left_actions:
        btn_new_col, btn_open_col, btn_dup_col, btn_sim_col, btn_run_col, _ = st.columns(
            [1.35, 1.7, 1.55, 1.95, 2.1, 2.35],
            gap="small",
        )

        with btn_new_col:
            with st.container(key="new_scenario_hover_menu"):
                st.button("Nuovo scenario", width="stretch", key="btn_new_scenario_trigger")
                with st.container(key="new_scenario_hover_items"):
                    create_top_scenario = st.button("Miscele TOP", width="stretch", key="btn_new_scenario_top")
                    create_all_scenario = st.button("Tutti i serbatoi", width="stretch", key="btn_new_scenario_all")
            if create_top_scenario:
                create_new_scenario(SCENARIO_SCOPE_TOP)
                st.rerun()
            if create_all_scenario:
                create_new_scenario(SCENARIO_SCOPE_ALL)
                st.rerun()

        with btn_open_col:
            with st.container(key="open_scenario_hover_menu"):
                st.button("Apri scenario", width="stretch", key="btn_open_scenario_trigger")
                with st.container(key="open_scenario_hover_items"):
                    open_scenario_a = st.button("Scenario A - ottimTOP", width="stretch", key="btn_open_scenario_a")
                    open_scenario_b = st.button("Scenario B - simulTOP", width="stretch", key="btn_open_scenario_b")
                    open_scenario_c = st.button("Scenario C - all", width="stretch", key="btn_open_scenario_c")
            if open_scenario_a:
                open_predefined_scenario(SCENARIO_PRESET_TOP)
                st.rerun()
            if open_scenario_b:
                open_predefined_scenario(SCENARIO_PRESET_SIM_TOP)
                st.rerun()
            if open_scenario_c:
                open_predefined_scenario(SCENARIO_PRESET_ALL)
                st.rerun()

        with btn_dup_col:
            if st.button("Duplica scenario", width="stretch", key="btn_duplicate_scenario"):
                st.session_state.scenario_counter += 1
                next_letter = chr(ord("A") + st.session_state.scenario_counter - 1)
                st.session_state.current_scenario = f"Scenario {next_letter}"
                st.session_state.show_edit_dialog = False
                if scenario_scope == SCENARIO_SCOPE_ALL:
                    st.session_state.config_mode = "simulation"
                    st.session_state.destination_view_mode = "Tutti i serbatoi"
                else:
                    st.session_state.config_mode = "optimization"
                    st.session_state.destination_view_mode = "Serbatoi TOP"
                st.session_state.page_mode = "config"

        with btn_sim_col:
            if st.button(
                "Esegui simulazione",
                width="stretch",
                type="primary" if st.session_state.config_mode == "simulation" else "secondary",
                disabled=st.session_state.config_mode != "simulation",
                key="btn_run_simulation",
            ):
                st.session_state.config_mode = "simulation"
                sync_simulation_destination_mode()
                st.session_state.show_edit_dialog = False
                st.rerun()

        with btn_run_col:
            if st.button(
                "Esegui ottimizzazione",
                width="stretch",
                type="primary" if st.session_state.config_mode == "optimization" else "secondary",
                disabled=(st.session_state.config_mode != "optimization") or (scenario_scope == SCENARIO_SCOPE_ALL),
                key="btn_run_optimization",
            ):
                st.session_state.config_mode = "optimization"
                if not build_coherence_issues():
                    st.session_state.output_compare_scenario = ""
                    st.session_state.output_has_scenario_a_plus = False
                    st.session_state.out_recipe_b_tk125 = None
                    st.session_state.out_recipe_b_tk126 = None
                    st.session_state.page_mode = "output"
                    st.session_state.show_edit_dialog = False
                    st.rerun()

if st.session_state.get("page_mode") == "home":
    st.stop()

left_col, right_col = st.columns([0.82, 2.18], gap="medium")

with left_col:
    left_config_panel = st.container(key="left_config_panel", width="stretch")
    with left_config_panel:
        st.markdown(
            """
            <div class="left-panel-head">
                <div class="left-panel-title">Configurazione per serbatoio di destinazione</div>
                <div class="left-panel-caption">Per ciascun serbatoio si definiscono i target della miscela</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if is_simulation_mode:
            destination_view_selector = st.container(key="destination_view_selector", width="stretch")
            with destination_view_selector:
                _scope_label = "Miscele TOP" if scenario_scope == SCENARIO_SCOPE_TOP else "Tutti i serbatoi"
                st.markdown(
                    f'<div class="left-panel-caption" style="margin:2px 0 8px">Tipo scenario simulazione: <b>{_scope_label}</b></div>',
                    unsafe_allow_html=True,
                )

        df_dest = pd.DataFrame(st.session_state.destination_tanks)

        st.data_editor(
            df_dest,
            hide_index=True,
            width="stretch",
            num_rows="fixed",
            column_config={
                "selected": st.column_config.CheckboxColumn("", width="small"),
                "tank": st.column_config.TextColumn("Serbatoio", disabled=True, width=88),
                "cod_range": st.column_config.TextColumn("COD", width=88),
                "solvents": st.column_config.NumberColumn("Solventi", step=1, format="%d", width=108),
                "v_min": st.column_config.NumberColumn("V min", step=1, format="%d", width="small"),
                "v_max": st.column_config.NumberColumn("V max", step=1, format="%d", width="small"),
            },
            disabled=["tank"],
            key="destination_tanks_editor",
            on_change=sync_destination_tanks_from_editor,
        )

        if is_simulation_mode and scenario_scope == SCENARIO_SCOPE_ALL:
            base_tanks = {
                str(row.get("tank", "")).strip()
                for row in st.session_state.destination_tanks
                if str(row.get("tank", "")).strip()
            }
            all_tanks_for_view = get_selected_destination_tanks()
            extra_tanks = [tank for tank in all_tanks_for_view if tank not in base_tanks]
            if extra_tanks:
                with st.expander(f"Visualizza altri serbatoi ({len(extra_tanks)})", expanded=False):
                    extra_df = pd.DataFrame(
                        [{"Serbatoio": tank, "Tipo": "Ricevimento"} for tank in extra_tanks]
                    )
                    st.dataframe(
                        extra_df,
                        hide_index=True,
                        width="stretch",
                        height=min(220, 60 + len(extra_df) * 35),
                    )

        active_tanks = [r["tank"] for r in st.session_state.destination_tanks if r["selected"]]

        st.markdown(
            f"""
            <div class="recipe-card">
                <div class="recipe-head">Impostazioni miscele</div>
                <div class="recipe-row">
                    <span class="recipe-label">Serbatoi destinazione attivi</span>
                    <span class="recipe-value">{", ".join(active_tanks) if active_tanks else "-"}</span>
                </div>
                <div class="recipe-row">
                    <span class="recipe-label">Numero serbatoi selezionati</span>
                    <span class="recipe-value">{len(active_tanks)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Altre impostazioni...", width="content", key="btn_other_settings"):
            st.session_state.show_cod_setting = True

        if st.session_state.show_cod_setting:
            with st.container(key="cod_setting_box", width="stretch"):
                cod_label_col, cod_input_col, cod_unit_col = st.columns([2.3, 1.0, 0.25], gap="small")
                with cod_label_col:
                    st.markdown('<div class="cod-setting-label">Abbattimento COD</div>', unsafe_allow_html=True)
                with cod_input_col:
                    cod_reduction_value = st.number_input(
                        "Abbattimento COD (%)",
                        min_value=0,
                        max_value=100,
                        step=1,
                        value=int(st.session_state.cod_reduction_pct),
                        label_visibility="collapsed",
                    )
                    st.session_state.cod_reduction_pct = int(cod_reduction_value)
                with cod_unit_col:
                    st.markdown('<div class="cod-setting-unit">%</div>', unsafe_allow_html=True)

    coherence_issues = build_coherence_issues()

    left_coherence_panel = st.container(key="left_coherence_panel", width="stretch")
    with left_coherence_panel:
        st.markdown('<div class="left-subpanel-title">Controlli di coerenza</div>', unsafe_allow_html=True)
        if coherence_issues:
            issue_items = "".join(f"<li>{issue}</li>" for issue in coherence_issues)
            st.markdown(
                f"""
                <div class="coh-count">{len(coherence_issues)} criticit\u00e0</div>
                <ul class="coh-list">{issue_items}</ul>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="coh-ok">Nessuna criticit\u00e0</div>', unsafe_allow_html=True)

with right_col:
    right_main_box = st.container(key="right_main_box", width="stretch")

with right_main_box:
    config_mode_tabs = st.container(key="config_mode_tabs", width="stretch")
    with config_mode_tabs:
        tabs_left, tabs_right = st.columns([3.9, 1.3], gap="small")

        with tabs_left:
            if scenario_scope == SCENARIO_SCOPE_ALL:
                if st.button(
                    "Simulazione",
                    width="stretch",
                    type="primary",
                    key="btn_cfg_tab_simulation_only",
                ):
                    st.session_state.config_mode = "simulation"
                    sync_simulation_destination_mode()
                    st.rerun()
            else:
                mode_sim_col, mode_opt_col = st.columns([1.0, 1.0], gap="medium")
                with mode_sim_col:
                    if st.button(
                        "Simulazione",
                        width="stretch",
                        type="primary" if is_simulation_mode else "secondary",
                        key="btn_cfg_tab_simulation",
                    ):
                        st.session_state.config_mode = "simulation"
                        sync_simulation_destination_mode()
                        st.rerun()
                with mode_opt_col:
                    if st.button(
                        "Ottimizzazione",
                        width="stretch",
                        type="primary" if not is_simulation_mode else "secondary",
                        key="btn_cfg_tab_optimization",
                    ):
                        st.session_state.config_mode = "optimization"
                        st.rerun()

        with tabs_right:
            _, plant_chip_col, scenario_chip_col = st.columns([1.0, 1.0, 1.6], gap="small")
            with plant_chip_col:
                if show_plant_badge:
                    st.markdown(
                        f'<div class="top-chip" style="margin-top:8px; margin-right:-2px; float:right">{st.session_state.plant}</div>',
                        unsafe_allow_html=True,
                    )
            with scenario_chip_col:
                st.markdown(
                    f'<div class="top-chip" style="margin-top:8px; margin-right:-2px; float:right">{scenario_label}</div>',
                    unsafe_allow_html=True,
                )

    table_state = st.session_state.get("source_tanks_table", {})
    selected_idx_for_actions = st.session_state.selected_row_index
    if isinstance(table_state, dict):
        selected_rows_state = table_state.get("selection", {}).get("rows", [])
        if selected_rows_state:
            selected_idx_for_actions = selected_rows_state[0]

    active_source_rows = get_active_source_tanks()
    df_source = pd.DataFrame(active_source_rows)
    selected_top_tanks = [
        str(row.get("tank", "")).strip()
        for row in st.session_state.destination_tanks
        if row.get("selected") and str(row.get("tank", "")).strip() in TOP_TRANSFER_FIELDS
    ]
    selected_transfer_pairs = [(tank, TOP_TRANSFER_FIELDS[tank]) for tank in selected_top_tanks]

    for field in TOP_TRANSFER_FIELDS.values():
        if field not in df_source.columns:
            df_source[field] = 0

    if is_simulation_mode:
        grid_columns = [
            "tank",
            "qty_available",
            "cod",
            "solvents",
            "boro",
            "empty_tank",
            "priority",
            "incompatibility",
            "destination_tank",
            "transfer_volume",
            "vol_min",
            "vol_max",
            "notes",
        ]
    else:
        grid_columns = [
            "tank",
            "qty_available",
            "cod",
            "solvents",
            "boro",
            *[field for _, field in selected_transfer_pairs],
            "empty_tank",
            "priority",
            "destination_tank",
            "vol_min",
            "vol_max",
            "incompatibility",
            "notes",
        ]

    df_grid = df_source[grid_columns].copy()

    df_grid = df_grid.rename(
        columns={
            "tank": "Serbatoio",
            "qty_available": "Q.t\u00e0 disp.",
            "cod": "COD",
            "solvents": "Solventi",
            "boro": "Boro",
            "empty_tank": "Svuota serbatoio",
            "priority": "Priorit\u00e0",
            "incompatibility": "Incompatibilit\u00e0",
            "destination_tank": "Serbatoio di destinazione",
            "transfer_volume": "Volume da trasferire",
            "transfer_tk125": "Volume da trasferire in TK-125",
            "transfer_tk126": "Volume da trasferire in TK-126",
            "transfer_tk127": "Volume da trasferire in TK-127",
            "vol_min": "Vol. min",
            "vol_max": "Vol. max",
            "notes": "Note",
        }
    )

    df_grid["Q.t\u00e0 disp."] = df_grid["Q.t\u00e0 disp."].apply(fmt_qty_or_dash)
    df_grid["COD"] = df_grid["COD"].apply(fmt_int_or_dash)
    df_grid["Solventi"] = df_grid["Solventi"].apply(fmt_int_or_dash)
    df_grid["Boro"] = df_grid["Boro"].apply(lambda x: fmt_float_or_dash(x, decimals=1))
    if is_simulation_mode:
        df_grid["Volume da trasferire"] = df_grid["Volume da trasferire"].apply(fmt_int_or_dash)
    else:
        transfer_display_cols = [f"Volume da trasferire in {tank}" for tank, _ in selected_transfer_pairs]
        for col_name in transfer_display_cols:
            if col_name in df_grid.columns:
                df_grid[col_name] = df_grid[col_name].apply(
                    lambda v: "" if safe_int_input(v, 0) == 0 else fmt_int_or_dash(v)
                )
    empty_tank_mask = df_grid["Svuota serbatoio"].fillna(False).astype(bool)
    df_grid["Vol. min"] = df_grid["Vol. min"].apply(fmt_int_or_dash)
    df_grid["Vol. max"] = df_grid["Vol. max"].apply(fmt_int_or_dash)
    df_grid.loc[empty_tank_mask, ["Vol. min", "Vol. max"]] = ""
    df_grid["Svuota serbatoio"] = df_grid["Svuota serbatoio"].map(lambda x: "\u2713" if x else "")
    df_grid["Incompatibilit\u00e0"] = df_grid["Incompatibilit\u00e0"].fillna("").replace("", "\u2014")
    df_grid["Note"] = df_grid["Note"].fillna("").replace("", "\u2014")

    if is_simulation_mode:
        hidden_sim_columns = [
            "Priorit\u00e0",
            "Svuota serbatoio",
            "Incompatibilit\u00e0",
            "Vol. min",
            "Vol. max",
        ]
        df_grid = df_grid.drop(columns=[c for c in hidden_sim_columns if c in df_grid.columns])

    styled_grid = (
        df_grid.style
        .apply(style_priority_column, axis=0)
        .apply(style_empty_tank_column, axis=0)
        .apply(style_incompatibility_column, axis=0)
    )

    if is_simulation_mode:
        grid_tab_moves, grid_tab_status = st.tabs(["Movimenti tra serbatoi", "Simulazione stato serbatoi"])
    else:
        grid_tab_moves = st.container()
        grid_tab_status = None

    with grid_tab_moves:
        if not is_simulation_mode:
            st.markdown('<div class="right-main-title">Serbatoi disponibili per alimentazione TOP</div>', unsafe_allow_html=True)

        mode_actions = st.container(key="mode_actions", width="stretch")
        with mode_actions:
            if is_simulation_mode:
                act_left, act_spacer, act_right = st.columns([3.8, 0.2, 1.6], gap="small")
            else:
                act_left, act_spacer, act_right = st.columns([3.0, 0.8, 1.7], gap="small")
            with act_left:
                if is_simulation_mode:
                    btn_refresh_col, btn_add_col, btn_edit_col, btn_remove_col = st.columns([2.5, 2.0, 1.15, 1.15], gap="small")
                else:
                    btn_refresh_col, btn_edit_col, btn_remove_col = st.columns([2.5, 1.25, 1.25], gap="small")
                with btn_refresh_col:
                    refresh_button_width = "stretch"
                    if st.button(
                        "Aggiorna con dati Skysym",
                        width=refresh_button_width,
                        key="btn_refresh_skysym",
                    ):
                        if is_simulation_mode:
                            if is_grid_empty_for_refresh(st.session_state.simulation_source_tanks):
                                st.session_state.simulation_source_tanks = build_skysym_partial_source_tanks()
                                sync_simulation_destination_mode()
                            else:
                                st.session_state.simulation_source_tanks = apply_skysym_top_fields_on_existing_rows(
                                    st.session_state.simulation_source_tanks
                                )
                        else:
                            if is_grid_empty_for_refresh(st.session_state.source_tanks):
                                st.session_state.source_tanks = build_skysym_partial_source_tanks()
                                enforce_destination_tank_rules()
                            else:
                                st.session_state.source_tanks = apply_skysym_top_fields_on_existing_rows(
                                    st.session_state.source_tanks
                                )
                        st.session_state.selected_row_index = None
                        st.session_state.show_edit_dialog = False
                        st.rerun()
                if is_simulation_mode:
                    with btn_add_col:
                        if st.button(
                            "+ Nuovo movimento",
                            width="stretch",
                            key="btn_add_row_simulation",
                        ):
                            st.session_state.simulation_source_tanks.append(
                                build_new_simulation_row(st.session_state.simulation_source_tanks)
                            )
                            enforce_destination_tank_rules()
                            st.session_state.selected_row_index = None
                            st.session_state.show_edit_dialog = False
                            st.rerun()
                with btn_edit_col:
                    if st.button(
                        "Modifica",
                        width="stretch",
                        disabled=selected_idx_for_actions is None,
                        key="btn_edit_row_top",
                    ):
                        st.session_state.selected_row_index = selected_idx_for_actions
                        st.session_state.show_edit_dialog = True
                        st.session_state.edit_dialog_nonce += 1
                with btn_remove_col:
                    if st.button(
                        "Rimuovi",
                        width="stretch",
                        disabled=selected_idx_for_actions is None,
                        key="btn_remove_row_top",
                    ):
                        if selected_idx_for_actions is not None and 0 <= selected_idx_for_actions < len(active_source_rows):
                            active_source_rows.pop(selected_idx_for_actions)
                            st.session_state.selected_row_index = None
                            st.session_state.show_edit_dialog = False
                            st.rerun()
            with act_right:
                search_col, filter_col = st.columns([3.2, 1.1], gap="small")
                with search_col:
                    st.text_input(
                        "Ricerca",
                        value="",
                        placeholder="Cerca rifiuto, cliente, produttore...",
                        label_visibility="collapsed",
                        key="opt_search_text",
                    )
                with filter_col:
                    st.button("Filtri", width="stretch", key="btn_filters")

        selection_event = st.dataframe(
            styled_grid,
            width="stretch",
            hide_index=True,
            height=360,
            column_config={
                "Serbatoio": st.column_config.TextColumn("Serbatoio", width=120),
                "Note": st.column_config.TextColumn("Note", width="medium"),
            },
            on_select="rerun",
            selection_mode="single-row",
            key="source_tanks_table",
        )

    if grid_tab_status is not None:
        with grid_tab_status:
            sim_rows = []
            if scenario_scope == SCENARIO_SCOPE_ALL:
                # In scenario "all", show status for every available destination tank.
                status_tanks = get_selected_destination_tanks()
                status_destinations = [{"tank": tank, "cod_range": ""} for tank in status_tanks]
            else:
                status_destinations = [r for r in st.session_state.destination_tanks if r.get("selected")]

            for dest in status_destinations:
                dest_tank = str(dest.get("tank", "")).strip()
                if not dest_tank:
                    continue
                cod_range_text = str(dest.get("cod_range", "")).replace(" ", "")
                cod_min = None
                cod_max = None
                if "-" in cod_range_text:
                    parts = cod_range_text.split("-", 1)
                    try:
                        cod_min = int(float(parts[0]))
                        cod_max = int(float(parts[1]))
                    except (TypeError, ValueError):
                        cod_min = None
                        cod_max = None

                matching_sources = []
                for row in active_source_rows:
                    row_dest = str(row.get("destination_tank", "")).strip()
                    if row_dest != dest_tank:
                        continue
                    vol = safe_int_input(row.get("transfer_volume"), 0)
                    if vol <= 0:
                        continue
                    matching_sources.append(row)

                volume_total = sum(safe_int_input(r.get("transfer_volume"), 0) for r in matching_sources)
                cod_sim = 0
                solv_sim = 0
                if volume_total > 0:
                    cod_sim = int(round(
                        sum(safe_int_input(r.get("cod"), 0) * safe_int_input(r.get("transfer_volume"), 0) for r in matching_sources)
                        / volume_total
                    ))
                    solv_sim = int(round(
                        sum(safe_int_input(r.get("solvents"), 0) * safe_int_input(r.get("transfer_volume"), 0) for r in matching_sources)
                        / volume_total
                    ))

                esito = "Nessun movimento"
                if volume_total > 0:
                    if cod_min is not None and cod_max is not None:
                        if cod_min <= cod_sim <= cod_max:
                            esito = "Nel range"
                        elif cod_sim > cod_max:
                            esito = "Fuori range (alto)"
                        else:
                            esito = "Fuori range (basso)"
                    else:
                        esito = "Da verificare"

                sim_rows.append(
                    {
                        "Serbatoio": dest_tank,
                        "Vol. simulato (m3)": volume_total,
                        "COD simulato": cod_sim if volume_total > 0 else "\u2014",
                        "Solventi simulati": solv_sim if volume_total > 0 else "\u2014",
                        "Esito COD": esito,
                    }
                )

            if sim_rows:
                sim_df = pd.DataFrame(sim_rows)
                if scenario_scope == SCENARIO_SCOPE_ALL and "Esito COD" in sim_df.columns:
                    sim_df = sim_df.drop(columns=["Esito COD"])
                st.dataframe(
                    sim_df,
                    width="stretch",
                    hide_index=True,
                    height=240,
                    column_config={
                        "Serbatoio": st.column_config.TextColumn("Serbatoio", width="small"),
                        "Vol. simulato (m3)": st.column_config.NumberColumn("Vol. simulato (m3)", format="%d", width="small"),
                        "COD simulato": st.column_config.TextColumn("COD simulato", width="small"),
                        "Solventi simulati": st.column_config.TextColumn("Solventi simulati", width="small"),
                        "Esito COD": st.column_config.TextColumn("Esito COD", width="medium"),
                    },
                )
            else:
                st.info("Nessun serbatoio di destinazione selezionato per la simulazione.")

    selected_rows = selection_event.selection.rows
    st.session_state.selected_row_index = selected_rows[0] if selected_rows else None

    if st.session_state.show_edit_dialog and st.session_state.selected_row_index is not None:
        edit_source_tank_dialog(
            st.session_state.selected_row_index,
            st.session_state.edit_dialog_nonce,
        )
    elif st.session_state.show_edit_dialog and st.session_state.selected_row_index is None:
        st.session_state.show_edit_dialog = False

    total_tanks = len(df_source)
    empty_count = int(df_source["empty_tank"].sum())
    active_dest_count = len(active_tanks)
    incompatibility_count = int(df_source["incompatibility"].fillna("").ne("").sum())

    cod_series = pd.to_numeric(df_source["cod"], errors="coerce")
    solvents_series = pd.to_numeric(df_source["solvents"], errors="coerce")
    boro_series = pd.to_numeric(df_source["boro"], errors="coerce")

    avg_cod = int(cod_series.mean()) if cod_series.notna().any() else 0
    avg_solvents = int(solvents_series.mean()) if solvents_series.notna().any() else 0
    avg_boro = round(float(boro_series.mean()), 1) if boro_series.notna().any() else 0.0

    bottom_left, bottom_right = st.columns(2, gap="medium")

    with bottom_left:
        st.markdown(
            f"""
            <div class="mini-panel">
                <div class="mini-title">Sintesi configurazione</div>
                <div class="mini-body">
                    <div class="metric-list">
                        <div class="metric">Serbatoi valutati <b>{total_tanks}</b></div>
                        <div class="metric">Serbatoi da svuotare <b>{empty_count}</b></div>
                        <div class="metric">Compatibilit\u00e0 critiche <b>{incompatibility_count}</b></div>
                        <div class="metric">Serbatoi destinazione attivi <b>{active_dest_count}</b></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with bottom_right:
        right_panel_title = "Parametri medi miscela simulata" if is_simulation_mode else "Parametri medi disponibili"
        st.markdown(
            f"""
            <div class="mini-panel">
                <div class="mini-title">{right_panel_title}</div>
                <div class="mini-body">
                    <div class="metric-list">
                        <div class="metric">COD medio componenti selezionabili <b>{avg_cod}</b></div>
                        <div class="metric">Solventi medi componenti selezionabili <b>{avg_solvents}</b></div>
                        <div class="metric">Boro medio componenti selezionabili <b>{avg_boro}</b></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


