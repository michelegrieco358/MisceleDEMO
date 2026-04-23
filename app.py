import streamlit as st
import pandas as pd
from copy import deepcopy

st.set_page_config(page_title="Gestione Miscele - Configurazione", layout="wide")


destination_tanks_default = [
    {"selected": True,  "tank": "TK-125", "cod_range": "44000-48000", "solvents": 800, "v_min": 40, "v_max": 60},
    {"selected": True,  "tank": "TK-126", "cod_range": "43000-47000", "solvents": 750, "v_min": 20, "v_max": 40},
    {"selected": False, "tank": "TK-127", "cod_range": "45000-49000", "solvents": 850, "v_min": 0,  "v_max": 30},
]

source_tanks_default = [
    {
        "tank": "S-01", "qty_available": 45, "cod": 52000, "solvents": 780, "boro": 4.2,
        "cl": 120, "n": 18,
        "empty_tank": True, "priority": "Alta", "incompatibility": "",
        "destination_tank": "TK-125", "transfer_volume": 20,
        "vol_min": 20, "vol_max": 45, "notes": ""
    },
    {
        "tank": "S-02", "qty_available": 42, "cod": 86000, "solvents": 1320, "boro": 4.5,
        "cl": 108, "n": 17,
        "empty_tank": False, "priority": "Media", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0,
        "vol_min": 0, "vol_max": 32, "notes": ""
    },
    {
        "tank": "S-03", "qty_available": 35, "cod": 118000, "solvents": 420, "boro": 3.1,
        "cl": 95, "n": 12,
        "empty_tank": False, "priority": "Media", "incompatibility": "S-08",
        "destination_tank": "TK-126", "transfer_volume": 15,
        "vol_min": 0, "vol_max": 25, "notes": ""
    },
    {
        "tank": "S-04", "qty_available": 50, "cod": 72000, "solvents": 1600, "boro": 4.8,
        "cl": 110, "n": 15,
        "empty_tank": False, "priority": "Alta", "incompatibility": "",
        "destination_tank": "TK-126", "transfer_volume": 10,
        "vol_min": 10, "vol_max": 40, "notes": ""
    },
    {
        "tank": "S-05", "qty_available": 38, "cod": 94000, "solvents": 980, "boro": 4.1,
        "cl": 102, "n": 16,
        "empty_tank": False, "priority": "Alta", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0,
        "vol_min": 0, "vol_max": 28, "notes": ""
    },
    {
        "tank": "S-06", "qty_available": 33, "cod": 59000, "solvents": 640, "boro": 3.4,
        "cl": 92, "n": 13,
        "empty_tank": False, "priority": "Bassa", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0,
        "vol_min": 0, "vol_max": 22, "notes": ""
    },
    {
        "tank": "S-07", "qty_available": 30, "cod": 31000, "solvents": 95, "boro": 2.9,
        "cl": 88, "n": 10,
        "empty_tank": False, "priority": "Bassa", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0,
        "vol_min": 0, "vol_max": 20, "notes": ""
    },
    {
        "tank": "S-08", "qty_available": 25, "cod": 146000, "solvents": 5100, "boro": 6.1,
        "cl": 130, "n": 22,
        "empty_tank": True, "priority": "Alta", "incompatibility": "S-03",
        "destination_tank": "", "transfer_volume": 12,
        "vol_min": 15, "vol_max": 25, "notes": ""
    },
    {
        "tank": "S-09", "qty_available": 20, "cod": 68000, "solvents": 1150, "boro": 3.7,
        "cl": 90, "n": 20,
        "empty_tank": False, "priority": "Media", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0,
        "vol_min": 0, "vol_max": 15, "notes": "rifiuto da dosare"
    },
    {
        "tank": "TK-125 residuo", "qty_available": 5, "cod": 47000, "solvents": 740, "boro": 4.0,
        "cl": 105, "n": 16,
        "empty_tank": False, "priority": "", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 5,
        "vol_min": 15, "vol_max": 15, "notes": "residuo"
    },
    {
        "tank": "TK-126 residuo", "qty_available": 0, "cod": 45500, "solvents": 720, "boro": 3.8,
        "cl": 98, "n": 14,
        "empty_tank": False, "priority": "", "incompatibility": "",
        "destination_tank": "", "transfer_volume": 0,
        "vol_min": 0, "vol_max": 10, "notes": "residuo"
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
                "vol_min": None,
                "vol_max": None,
                "notes": "residuo" if is_residue else "",
            }
        )
    return empty_rows


def is_missing(value):
    return value is None or pd.isna(value)


def fmt_int_or_dash(value):
    if is_missing(value):
        return "\u2014"
    try:
        return int(float(value))
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
        st.session_state.page_mode = "config"
    if "out_recipe_tk125" not in st.session_state:
        st.session_state.out_recipe_tk125 = None
    if "out_recipe_tk126" not in st.session_state:
        st.session_state.out_recipe_tk126 = None
    if "show_add_comp_tk125" not in st.session_state:
        st.session_state.show_add_comp_tk125 = False
    if "show_add_comp_tk126" not in st.session_state:
        st.session_state.show_add_comp_tk126 = False
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
    return [r["tank"] for r in st.session_state.destination_tanks if r.get("selected")]


def enforce_destination_tank_rules():
    selected_tanks = set(get_selected_destination_tanks())
    for row in st.session_state.source_tanks:
        raw_destination = row.get("destination_tank", "")
        destination = "" if is_missing(raw_destination) else str(raw_destination).strip()
        if destination and destination not in selected_tanks:
            row["destination_tank"] = ""
            destination = ""

        is_residue = "residuo" in str(row["tank"]).lower()
        if is_residue:
            row["empty_tank"] = False
            row["priority"] = ""
            row["destination_tank"] = ""
            continue


def build_coherence_issues():
    issues = []
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
    for row in st.session_state.source_tanks:
        dest = str(row.get("destination_tank", "")).strip()
        if not dest or dest not in destination_transfer_sum:
            continue
        try:
            transfer_volume = float(row.get("transfer_volume", 0) or 0)
        except (TypeError, ValueError):
            transfer_volume = 0.0
        destination_transfer_sum[dest] += transfer_volume

    for tank, total_transfer in destination_transfer_sum.items():
        vmax = destination_vmax[tank]
        if total_transfer > vmax:
            issues.append(
                f"{tank}: volume totale da trasferire {int(total_transfer)} m3 superiore al V max impostato {int(vmax)} m3"
            )
    return issues


def build_output_recipe_dataframe():
    rows = []
    selected_destinations = set(get_selected_destination_tanks())
    for row in st.session_state.source_tanks:
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
    if row_index is None or row_index < 0 or row_index >= len(st.session_state.source_tanks):
        st.warning("Nessun record valido selezionato.")
        if st.button("Chiudi", width="content", key=f"edit_close_{dialog_nonce}"):
            st.session_state.show_edit_dialog = False
            st.rerun()
        return

    row = st.session_state.source_tanks[row_index]
    is_residue = "residuo" in str(row["tank"]).lower()

    info_col, edit_col = st.columns(2, gap="large")

    with info_col:
        st.markdown("#### Dati informativi")
        st.text_input("Serbatoio", value=str(row["tank"]), disabled=True, key=f"info_tank_{dialog_nonce}")
        st.text_input(
            "Q.t\u00e0 disponibile",
            value=f"{safe_info_text(row['qty_available'])} m3" if not is_missing(row["qty_available"]) else "\u2014",
            disabled=True,
            key=f"info_qty_{dialog_nonce}",
        )
        st.text_input("COD", value=safe_info_text(row["cod"]), disabled=True, key=f"info_cod_{dialog_nonce}")
        st.text_input("Cl", value=safe_info_text(row["cl"]), disabled=True, key=f"info_cl_{dialog_nonce}")
        st.text_input("N", value=safe_info_text(row["n"]), disabled=True, key=f"info_n_{dialog_nonce}")
        st.text_input("Boro", value=safe_info_text(row["boro"]), disabled=True, key=f"info_boro_{dialog_nonce}")

    with edit_col:
        st.markdown("#### Parametri modificabili")
        empty_tank = st.checkbox(
            "Svuota serbatoio",
            value=bool(row["empty_tank"]),
            disabled=is_residue,
            key=f"edit_empty_tank_{dialog_nonce}",
        )
        priority_options = ["Alta", "Media", "Bassa"]
        if is_residue:
            priority_options = [""]
        current_priority = row["priority"] if row["priority"] in priority_options else ""
        priority = st.selectbox(
            "Priorit\u00e0",
            options=priority_options,
            index=priority_options.index(current_priority),
            format_func=lambda x: "\u2014" if x == "" else x,
            disabled=is_residue,
            key=f"edit_priority_{dialog_nonce}",
        )
        incompatibility = st.text_input(
            "Incompatibilit\u00e0",
            value=str(row["incompatibility"]),
            key=f"edit_incompatibility_{dialog_nonce}",
        )
        destination_options = [""] + get_selected_destination_tanks()
        if is_residue:
            destination_options = [""]
        current_destination = (
            row["destination_tank"] if row["destination_tank"] in destination_options else ""
        )
        destination_tank = st.selectbox(
            "Serbatoio di destinazione",
            options=destination_options,
            index=destination_options.index(current_destination),
            format_func=lambda x: "\u2014" if x == "" else x,
            disabled=is_residue,
            key=f"edit_destination_{dialog_nonce}",
        )
        transfer_volume = st.number_input(
            "Volume da trasferire",
            value=safe_int_input(row["transfer_volume"]),
            step=1,
            key=f"edit_transfer_volume_{dialog_nonce}",
        )
        vol_min = st.number_input(
            "Vol. min",
            value=safe_int_input(row["vol_min"]),
            step=1,
            key=f"edit_vol_min_{dialog_nonce}",
        )
        vol_max = st.number_input(
            "Vol. max",
            value=safe_int_input(row["vol_max"]),
            step=1,
            key=f"edit_vol_max_{dialog_nonce}",
        )
        notes = st.text_area(
            "Note",
            value=str(row["notes"]),
            key=f"edit_notes_{dialog_nonce}",
        )

    cancel_col, save_col, _ = st.columns([1, 1, 2], gap="small")
    with cancel_col:
        if st.button("Annulla", width="stretch", key=f"edit_cancel_{dialog_nonce}"):
            st.session_state.show_edit_dialog = False
            st.rerun()
    with save_col:
        if st.button("Salva", width="stretch", type="primary", key=f"edit_save_{dialog_nonce}"):
            if not is_residue:
                st.session_state.source_tanks[row_index]["empty_tank"] = empty_tank
                st.session_state.source_tanks[row_index]["priority"] = priority
            st.session_state.source_tanks[row_index]["incompatibility"] = incompatibility
            st.session_state.source_tanks[row_index]["destination_tank"] = "" if is_residue else destination_tank
            st.session_state.source_tanks[row_index]["transfer_volume"] = transfer_volume
            st.session_state.source_tanks[row_index]["vol_min"] = vol_min
            st.session_state.source_tanks[row_index]["vol_max"] = vol_max
            st.session_state.source_tanks[row_index]["notes"] = notes
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
    background: #dfe5ea;
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
}

.block-container {
    max-width: 1500px;
    padding: 14px;
    margin-top: 0.3rem;
    margin-bottom: 0.7rem;
    border-radius: 8px;
    background: #eef1f4;
}

.top-titlebar {
    background: #1f4b8f;
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    line-height: 1.35;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
}

.st-key-top_toolbar {
    margin: 10px 0 8px;
    padding: 0;
}

.st-key-top_toolbar [data-testid="stHorizontalBlock"] {
    align-items: center;
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
    font-size: 12px;
    font-weight: 600;
    min-height: 32px;
    padding: 6px 14px;
    border-radius: 6px;
}

.st-key-top_toolbar [data-testid="stButton"] > button[kind="primary"] {
    background: #3fbf69;
    border-color: #35aa5d;
    color: #ffffff;
}

.st-key-top_toolbar [data-testid="stButton"] > button:disabled {
    opacity: 1;
    background: #eceff3;
    border-color: #d9dee6;
    color: #9aa5b1;
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

if st.session_state.page_mode == "output":
    if "abbatt_cod_output" not in st.session_state:
        st.session_state.abbatt_cod_output = int(st.session_state.cod_reduction_pct)
    abbatt_display = st.session_state.abbatt_cod_output

    _default_tk125 = [
        {"Componente": "Residuo TK-125", "Volume": 15, "COD": 47000, "Solventi": 740, "Boro": 4.0},
        {"Componente": "S-01",           "Volume": 18, "COD": 52000, "Solventi": 780, "Boro": 4.2},
        {"Componente": "S-07",           "Volume": 17, "COD": 31000, "Solventi":  95, "Boro": 2.9},
        {"Componente": "S-06",           "Volume":  5, "COD": 59000, "Solventi": 640, "Boro": 3.4},
        {"Componente": "S-ALTA",         "Volume":  2, "COD":110000, "Solventi":2900, "Boro": 5.1},
    ]
    _default_tk126 = [
        {"Componente": "Residuo TK-126", "Volume": 10, "COD": 45500, "Solventi": 720, "Boro": 3.8},
        {"Componente": "S-07",           "Volume": 12, "COD": 31000, "Solventi":  95, "Boro": 2.9},
        {"Componente": "S-01",           "Volume": 10, "COD": 52000, "Solventi": 780, "Boro": 4.2},
        {"Componente": "S-06",           "Volume":  8, "COD": 59000, "Solventi": 640, "Boro": 3.4},
    ]
    if st.session_state.out_recipe_tk125 is None:
        st.session_state.out_recipe_tk125 = pd.DataFrame(_default_tk125)
    if st.session_state.out_recipe_tk126 is None:
        st.session_state.out_recipe_tk126 = pd.DataFrame(_default_tk126)

    def _recompute_quota(df):
        total = df["Volume"].sum()
        df = df.copy()
        df["Quota %"] = (df["Volume"] / total * 100).round(1) if total > 0 else 0.0
        return df

    recipe_tk125 = _recompute_quota(st.session_state.out_recipe_tk125)
    recipe_tk126 = _recompute_quota(st.session_state.out_recipe_tk126)

    _vol_125_top = int(recipe_tk125["Volume"].sum())
    _vol_126_top = int(recipe_tk126["Volume"].sum())
    _cod_125_top = int((recipe_tk125["Volume"] * recipe_tk125["COD"]).sum() / _vol_125_top) if _vol_125_top > 0 else 0
    _cod_126_top = int((recipe_tk126["Volume"] * recipe_tk126["COD"]).sum() / _vol_126_top) if _vol_126_top > 0 else 0
    _sol_125_top = int((recipe_tk125["Volume"] * recipe_tk125["Solventi"]).sum() / _vol_125_top) if _vol_125_top > 0 else 0
    _sol_126_top = int((recipe_tk126["Volume"] * recipe_tk126["Solventi"]).sum() / _vol_126_top) if _vol_126_top > 0 else 0
    _COD_125_MIN, _COD_125_MAX = 44000, 48000
    _COD_126_MIN, _COD_126_MAX = 43000, 47000
    _cod_125_ok = _COD_125_MIN <= _cod_125_top <= _COD_125_MAX
    _cod_126_ok = _COD_126_MIN <= _cod_126_top <= _COD_126_MAX

    st.markdown(
        '<div class="top-titlebar">Creazione e ottimizzazione miscele TOP — Risultato e confronto ricette</div>',
        unsafe_allow_html=True,
    )

    output_toolbar = st.container(key="output_toolbar", width="stretch")
    with output_toolbar:
        left_actions, right_badges = st.columns([3.5, 1.5], gap="small")
        with left_actions:
            c1, c2, c3, c4, c5, _ = st.columns([1.4, 1.5, 1.5, 1.5, 1.8, 0.8], gap="small")
            with c1:
                if st.button("Modifica scenario", width="content", key="btn_out_mod_scenario"):
                    st.session_state.page_mode = "config"
                    st.rerun()
            with c2:
                st.button("Duplica Scenario", width="content", key="btn_out_dup")
            with c3:
                st.button("Export Risultati", width="content", key="btn_out_export")
            with c4:
                st.button("Export Report", width="content", key="btn_out_export_report")
            with c5:
                st.button("Conferma ricetta TOP", width="content", type="primary", key="btn_out_confirm")
        with right_badges:
            _, rc = st.columns([0.1, 1.2], gap="small")
            with rc:
                st.markdown('<div class="top-chip" style="float:right">Scenario A</div>', unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6, gap="small")
    with kpi1:
        st.markdown('<div class="output-kpi"><div class="output-kpi-title">Serbatoi attivi</div><div class="output-kpi-value">2</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="output-kpi"><div class="output-kpi-title">Volume totale</div><div class="output-kpi-value">{_vol_125_top + _vol_126_top} m3</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="output-kpi"><div class="output-kpi-title">Componenti</div><div class="output-kpi-value">{len(recipe_tk125) + len(recipe_tk126)}</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown('<div class="output-kpi"><div class="output-kpi-title">TK-125 COD target</div><div class="output-kpi-value">44000–48000</div></div>', unsafe_allow_html=True)
    with kpi5:
        st.markdown('<div class="output-kpi"><div class="output-kpi-title">TK-126 COD target</div><div class="output-kpi-value">43000–47000</div></div>', unsafe_allow_html=True)
    with kpi6:
        st.markdown('<div class="output-kpi"><div class="output-kpi-title">Verifica vincoli</div><div class="output-kpi-value" style="color:#2e7d32">OK</div></div>', unsafe_allow_html=True)

    out_left, out_right = st.columns([2.0, 1.0], gap="medium")

    with out_left:
        output_recipe_box = st.container(key="output_recipe_box", width="stretch")
        with output_recipe_box:
            st.markdown('<div class="right-main-title">Miscele TOP proposte</div>', unsafe_allow_html=True)
            tab_a, tab_b, tab_cmp = st.tabs(["Scenario A", "Scenario B", "Confronto"])

            with tab_a:
                tank_125, tank_126 = st.tabs(["TK-125", "TK-126"])

                with tank_125:
                    st.markdown("""<div class="tank-target-box">
                        <div class="tank-target-row">
                            <span class="tgt-chip">COD target <b>44000 – 48000</b></span>
                            <span class="tgt-chip">Solv max <b>800</b></span>
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
                                f"Volume – {_sc}", min_value=0, step=1,
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
                    if st.button("+ Aggiungi componente", key="btn_add_comp_tk125"):
                        st.session_state.show_add_comp_tk125 = not st.session_state.show_add_comp_tk125
                    if st.session_state.show_add_comp_tk125:
                        _existing_125 = set(st.session_state.out_recipe_tk125["Componente"].tolist())
                        _tank_opts_125 = [t["tank"] for t in st.session_state.source_tanks if t["tank"] not in _existing_125]
                        _sel_col, _add_col, _ann_col = st.columns([2.5, 1, 1], gap="small")
                        with _sel_col:
                            _new_tank_125 = st.selectbox("Serbatoio", _tank_opts_125, key="add_comp_sel_tk125", label_visibility="collapsed")
                        with _add_col:
                            if st.button("Aggiungi", key="btn_add_comp_confirm_tk125"):
                                _tank_data = next((t for t in st.session_state.source_tanks if t["tank"] == _new_tank_125), None)
                                if _tank_data:
                                    _new_row = pd.DataFrame([{
                                        "Componente": _tank_data["tank"],
                                        "Volume": 10,
                                        "COD": _tank_data["cod"] // 1000,
                                        "Solventi": _tank_data["solvents"] // 10,
                                        "Boro": _tank_data["boro"],
                                    }])
                                    st.session_state.out_recipe_tk125 = pd.concat(
                                        [st.session_state.out_recipe_tk125, _new_row], ignore_index=True
                                    )
                                    st.session_state.show_add_comp_tk125 = False
                                    st.rerun()
                        with _ann_col:
                            if st.button("Annulla", key="btn_add_comp_cancel_tk125"):
                                st.session_state.show_add_comp_tk125 = False
                                st.rerun()

                with tank_126:
                    st.markdown("""<div class="tank-target-box">
                        <div class="tank-target-row">
                            <span class="tgt-chip">COD target <b>43000 – 47000</b></span>
                            <span class="tgt-chip">Solv max <b>750</b></span>
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
                                f"Volume – {_sc}", min_value=0, step=1,
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
                    if st.button("+ Aggiungi componente", key="btn_add_comp_tk126"):
                        st.session_state.show_add_comp_tk126 = not st.session_state.show_add_comp_tk126
                    if st.session_state.show_add_comp_tk126:
                        _existing_126 = set(st.session_state.out_recipe_tk126["Componente"].tolist())
                        _tank_opts_126 = [t["tank"] for t in st.session_state.source_tanks if t["tank"] not in _existing_126]
                        _sel_col, _add_col, _ann_col = st.columns([2.5, 1, 1], gap="small")
                        with _sel_col:
                            _new_tank_126 = st.selectbox("Serbatoio", _tank_opts_126, key="add_comp_sel_tk126", label_visibility="collapsed")
                        with _add_col:
                            if st.button("Aggiungi", key="btn_add_comp_confirm_tk126"):
                                _tank_data = next((t for t in st.session_state.source_tanks if t["tank"] == _new_tank_126), None)
                                if _tank_data:
                                    _new_row = pd.DataFrame([{
                                        "Componente": _tank_data["tank"],
                                        "Volume": 10,
                                        "COD": _tank_data["cod"] // 1000,
                                        "Solventi": _tank_data["solvents"] // 10,
                                        "Boro": _tank_data["boro"],
                                    }])
                                    st.session_state.out_recipe_tk126 = pd.concat(
                                        [st.session_state.out_recipe_tk126, _new_row], ignore_index=True
                                    )
                                    st.session_state.show_add_comp_tk126 = False
                                    st.rerun()
                        with _ann_col:
                            if st.button("Annulla", key="btn_add_comp_cancel_tk126"):
                                st.session_state.show_add_comp_tk126 = False
                                st.rerun()

                st.markdown('<div class="right-main-title" style="margin-top:16px">Parametri attesi in uscita da TOP</div>', unsafe_allow_html=True)
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
                st.markdown('<div style="color:#8b97a4;font-size:13px;padding:20px 4px">Scenario B — configurazione alternativa non ancora definita.</div>', unsafe_allow_html=True)

            with tab_cmp:
                st.markdown('<div style="color:#8b97a4;font-size:13px;padding:20px 4px">Confronto — seleziona due ricette per confrontarle.</div>', unsafe_allow_html=True)

    with out_right:
        with st.container(key="out_right_confronto", width="stretch"):
            st.markdown('<div class="left-subpanel-title">Confronto ricette</div>', unsafe_allow_html=True)
            cr1, cr2 = st.columns(2, gap="small")
            with cr1:
                st.markdown('<div style="font-size:11px;color:#7b8794;margin-bottom:3px">Ricetta da confrontare</div><div class="conf-chip-sel">Scenario B</div>', unsafe_allow_html=True)
            with cr2:
                st.markdown('<div style="font-size:11px;color:#7b8794;margin-bottom:3px">Serbatoio di riferimento</div><div class="conf-chip-sel">TK-126</div>', unsafe_allow_html=True)
            ca, cb = st.columns(2, gap="small")
            with ca:
                st.markdown(f"""<div class="cmp-card">
                    <div class="cmp-card-title">Scenario A</div>
                    <div class="cmp-row">COD TK-126 <b style="color:#e08c00">{_cod_126_top}</b></div>
                    <div class="cmp-row">Solventi <b>{_sol_126_top} mg/l</b></div>
                    <div class="cmp-row esito-ok">Esito &nbsp;<b>Nel range</b></div>
                </div>""", unsafe_allow_html=True)
            with cb:
                st.markdown("""<div class="cmp-card">
                    <div class="cmp-card-title">Scenario B</div>
                    <div class="cmp-row">COD TK-126 <b style="color:#e08c00">48200</b></div>
                    <div class="cmp-row">Solventi <b>820 mg/l</b></div>
                    <div class="cmp-row esito-warn">Esito &nbsp;<b>Fuori range</b></div>
                </div>""", unsafe_allow_html=True)

        with st.container(key="out_right_criticita", width="stretch"):
            st.markdown('<div class="left-subpanel-title">Criticità di ricetta</div>', unsafe_allow_html=True)
            _crit_items = []
            if not _cod_125_ok:
                _dir_125 = "superiore" if _cod_125_top > _COD_125_MAX else "inferiore"
                _crit_items.append(f"""<div class="crit-item crit-error">
                    <div class="crit-title">TK-125 – COD miscela fuori range</div>
                    <div class="crit-body">COD {_cod_125_top} oltre il limite {_dir_125} ({_COD_125_MIN}–{_COD_125_MAX})</div>
                </div>""")
            if not _cod_126_ok:
                _dir_126 = "superiore" if _cod_126_top > _COD_126_MAX else "inferiore"
                _crit_items.append(f"""<div class="crit-item crit-error" style="margin-top:6px">
                    <div class="crit-title">TK-126 – COD miscela fuori range</div>
                    <div class="crit-body">COD {_cod_126_top} oltre il limite {_dir_126} ({_COD_126_MIN}–{_COD_126_MAX})</div>
                </div>""")
            _crit_items.append(f"""<div class="crit-item crit-warn" style="margin-top:6px">
                    <div class="crit-title">TK-126 – COD miscela</div>
                    <div class="crit-body">Vicino al limite superiore del range target</div>
                </div>
                <div class="crit-item crit-warn" style="margin-top:6px">
                    <div class="crit-title">TK-126 – Solventi miscela</div>
                    <div class="crit-body">Valore sotto il limite ma da monitorare</div>
                </div>
                <div class="crit-item crit-info" style="margin-top:6px">
                    <div class="crit-title">TK-127</div>
                    <div class="crit-body">Non coinvolto perché il serbatoio non è selezionato</div>
                </div>""")
            st.markdown("\n".join(_crit_items), unsafe_allow_html=True)

        with st.container(key="out_right_azioni", width="stretch"):
            st.markdown('<div class="left-subpanel-title">Azioni sul risultato</div>', unsafe_allow_html=True)
            if st.button("Modifica scenario", width="stretch", key="btn_out_mod_scenario_right"):
                st.session_state.page_mode = "config"
                st.rerun()
            st.button("Conferma ricetta TOP", width="stretch", type="primary", key="btn_out_confirm_right")

    st.stop()

st.markdown(
    '<div class="top-titlebar">Gestione Miscele - Configurazione</div>',
    unsafe_allow_html=True,
)

toolbar = st.container(key="top_toolbar", width="stretch")
with toolbar:
    left_actions, right_badges = st.columns([3.7, 1.3], gap="small")

    with left_actions:
        btn_new_col, btn_dup_col, btn_sim_col, btn_run_col, _ = st.columns(
            [1.3, 1.5, 1.8, 1.9, 3.0],
            gap="small",
        )

        with btn_new_col:
            if st.button("Nuovo scenario", width="content", key="btn_new_scenario"):
                st.session_state.scenario_counter += 1
                next_letter = chr(ord("A") + st.session_state.scenario_counter - 1)
                st.session_state.current_scenario = f"Scenario {next_letter}"
                st.session_state.destination_tanks = deepcopy(destination_tanks_default)
                st.session_state.pop("destination_tanks_editor", None)
                st.session_state.source_tanks = build_empty_source_tanks()
                st.session_state.selected_row_index = None
                st.session_state.show_edit_dialog = False
                st.session_state.cod_reduction_pct = 70
                st.session_state.page_mode = "config"

        with btn_dup_col:
            if st.button("Duplica scenario", width="content", key="btn_duplicate_scenario"):
                st.session_state.scenario_counter += 1
                next_letter = chr(ord("A") + st.session_state.scenario_counter - 1)
                st.session_state.current_scenario = f"Scenario {next_letter}"
                st.session_state.show_edit_dialog = False
                st.session_state.page_mode = "config"

        with btn_sim_col:
            st.button(
                "Esegui simulazione",
                width="content",
                disabled=True,
                key="btn_run_simulation",
            )

        with btn_run_col:
            if st.button(
                "Esegui ottimizzazione",
                width="content",
                type="primary",
                key="btn_run_optimization",
            ):
                if not build_coherence_issues():
                    st.session_state.page_mode = "output"
                    st.session_state.show_edit_dialog = False
                    st.rerun()

    with right_badges:
        _, plant_col, scenario_col = st.columns([2.2, 0.9, 1.4], gap="small")
        with plant_col:
            st.markdown(f'<div class="top-chip">{st.session_state.plant}</div>', unsafe_allow_html=True)
        with scenario_col:
            st.markdown(
                f'<div class="top-chip">{st.session_state.current_scenario}</div>',
                unsafe_allow_html=True,
            )

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

        active_tanks = [r["tank"] for r in st.session_state.destination_tanks if r["selected"]]

        st.markdown(
            f"""
            <div class="recipe-card">
                <div class="recipe-head">Impostazione ricetta</div>
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
    st.markdown(
        """
        <div class="mode-tabs">
            <span class="mode-tab">Simulazione</span>
            <span class="mode-tab mode-tab-active">Ottimizzazione</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    table_state = st.session_state.get("source_tanks_table", {})
    selected_idx_for_actions = st.session_state.selected_row_index
    if isinstance(table_state, dict):
        selected_rows_state = table_state.get("selection", {}).get("rows", [])
        if selected_rows_state:
            selected_idx_for_actions = selected_rows_state[0]

    st.markdown('<div class="right-main-title">Serbatoi disponibili per alimentazione TOP</div>', unsafe_allow_html=True)

    mode_actions = st.container(key="mode_actions", width="stretch")
    with mode_actions:
        act_left, act_spacer, act_right = st.columns([2.4, 1.2, 1.8], gap="small")
        with act_left:
            btn_refresh_col, btn_edit_col, btn_remove_col = st.columns([2.0, 1.1, 1.1], gap="small")
            with btn_refresh_col:
                if st.button(
                    "Aggiorna con dati Skysym",
                    width="content",
                    key="btn_refresh_skysym",
                ):
                    st.session_state.source_tanks = deepcopy(source_tanks_default)
                    enforce_destination_tank_rules()
                    st.session_state.selected_row_index = None
                    st.session_state.show_edit_dialog = False
                    st.rerun()
            with btn_edit_col:
                if st.button(
                    "Modifica",
                    width="content",
                    disabled=selected_idx_for_actions is None,
                    key="btn_edit_row_top",
                ):
                    st.session_state.selected_row_index = selected_idx_for_actions
                    st.session_state.show_edit_dialog = True
                    st.session_state.edit_dialog_nonce += 1
            with btn_remove_col:
                if st.button(
                    "Rimuovi",
                    width="content",
                    disabled=selected_idx_for_actions is None,
                    key="btn_remove_row_top",
                ):
                    if selected_idx_for_actions is not None and 0 <= selected_idx_for_actions < len(st.session_state.source_tanks):
                        st.session_state.source_tanks.pop(selected_idx_for_actions)
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

    df_source = pd.DataFrame(st.session_state.source_tanks)

    df_grid = df_source[
        [
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
    ].copy()

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
            "vol_min": "Vol. min",
            "vol_max": "Vol. max",
            "notes": "Note",
        }
    )

    df_grid["Q.t\u00e0 disp."] = df_grid["Q.t\u00e0 disp."].apply(fmt_qty_or_dash)
    df_grid["COD"] = df_grid["COD"].apply(fmt_int_or_dash)
    df_grid["Solventi"] = df_grid["Solventi"].apply(fmt_int_or_dash)
    df_grid["Boro"] = df_grid["Boro"].apply(lambda x: fmt_float_or_dash(x, decimals=1))
    df_grid["Volume da trasferire"] = df_grid["Volume da trasferire"].apply(fmt_int_or_dash)
    df_grid["Vol. min"] = df_grid["Vol. min"].apply(fmt_int_or_dash)
    df_grid["Vol. max"] = df_grid["Vol. max"].apply(fmt_int_or_dash)
    df_grid["Svuota serbatoio"] = df_grid["Svuota serbatoio"].map(lambda x: "\u2713" if x else "")
    df_grid["Incompatibilit\u00e0"] = df_grid["Incompatibilit\u00e0"].fillna("").replace("", "\u2014")
    df_grid["Note"] = df_grid["Note"].fillna("").replace("", "\u2014")

    styled_grid = (
        df_grid.style
        .apply(style_priority_column, axis=0)
        .apply(style_empty_tank_column, axis=0)
        .apply(style_incompatibility_column, axis=0)
    )

    selection_event = st.dataframe(
        styled_grid,
        width="stretch",
        hide_index=True,
        height=360,
        column_config={
            "Note": st.column_config.TextColumn("Note", width="medium"),
        },
        on_select="rerun",
        selection_mode="single-row",
        key="source_tanks_table",
    )

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
        st.markdown(
            f"""
            <div class="mini-panel">
                <div class="mini-title">Parametri medi disponibili</div>
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
