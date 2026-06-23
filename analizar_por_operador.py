#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ANALIZADOR DE CONTACTOS POR OPERADOR
================================================================================

Este programa analiza los contactos agrupados por operador (campo OPERATOR)
y genera gráficos estadísticos para cada operador.

Útil para:
- Ver qué operador hizo más contactos
- Analizar en qué bandas/modos opera cada operador
- Identificar horarios de actividad por operador
- Estadísticas de equipo compartido o club station

Uso:
    python analizar_por_operador.py

================================================================================
"""

import re
import os
from collections import defaultdict, Counter
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

plt.style.use("seaborn-v0_8")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 10
plt.rcParams["axes.grid"] = True

# ==============================================================================
# MAPA DE PREFIJOS DE INDICATIVOS A PAÍSES (ITU Prefix Allocation)
# ==============================================================================

PREFIX_COUNTRY_MAP = {
    "EA": "Spain", "EB": "Spain", "EC": "Spain", "ED": "Spain",
    "EE": "Spain", "EF": "Spain", "EG": "Spain", "EH": "Spain",
    "CT": "Portugal", "CS": "Portugal",
    "F": "France",
    "DA": "Germany", "DB": "Germany", "DC": "Germany", "DD": "Germany",
    "DE": "Germany", "DF": "Germany", "DG": "Germany", "DH": "Germany",
    "DI": "Germany", "DJ": "Germany", "DK": "Germany", "DL": "Germany",
    "DM": "Germany", "DN": "Germany", "DO": "Germany",
    "G": "England", "M": "England", "2E": "England",
    "MM": "Scotland", "GM": "Scotland",
    "GI": "Northern Ireland", "MI": "Northern Ireland",
    "GW": "Wales", "MW": "Wales", "GD": "Isle of Man", "MD": "Isle of Man",
    "GU": "Guernsey", "GJ": "Jersey",
    "I": "Italy", "IK": "Italy", "IZ": "Italy", "IU": "Italy",
    "IW": "Italy", "IN": "Italy", "IQ": "Italy", "IR": "Italy",
    "IS": "Italy", "IT": "Italy",
    "ON": "Belgium", "OR": "Belgium",
    "PA": "Netherlands", "PB": "Netherlands", "PC": "Netherlands",
    "PD": "Netherlands", "PE": "Netherlands", "PI": "Netherlands",
    "OE": "Austria",
    "OK": "Czech Republic", "OL": "Czech Republic",
    "OM": "Slovakia",
    "SP": "Poland", "SQ": "Poland", "SR": "Poland",
    "LZ": "Bulgaria",
    "9A": "Croatia",
    "HA": "Hungary", "HG": "Hungary",
    "S5": "Slovenia",
    "OZ": "Denmark",
    "TF": "Iceland",
    "UR": "Ukraine", "UT": "Ukraine", "UU": "Ukraine",
    "UY": "Ukraine", "UZ": "Ukraine", "EM": "Ukraine", "EO": "Ukraine",
    "SV": "Greece", "SY": "Greece",
    "EI": "Ireland", "EJ": "Ireland",
    "C3": "Andorra",
    "9H": "Malta",
    "TA": "Turkey", "TB": "Turkey", "TC": "Turkey",
    "V3": "Belize",
    "HB": "Switzerland", "HE": "Switzerland",
    "LX": "Luxembourg",
    "LA": "Norway", "LB": "Norway",
    "SM": "Sweden", "SK": "Sweden", "SA": "Sweden",
    "OH": "Finland", "OI": "Finland",
    "YO": "Romania", "YR": "Romania",
    "YU": "Serbia", "YT": "Serbia",
    "E7": "Bosnia and Herzegovina",
    "EW": "Belarus",
    "ER": "Moldova",
    "LY": "Lithuania",
    "YL": "Latvia",
    "ES": "Estonia",
    "JA": "Japan", "JH": "Japan",
    "PY": "Brazil", "PT": "Brazil", "PU": "Brazil",
    "K": "United States", "N": "United States", "W": "United States",
    "AA": "United States", "AB": "United States", "AC": "United States",
    "AD": "United States", "AE": "United States", "AF": "United States",
    "AG": "United States", "AH": "United States", "AI": "United States",
    "AJ": "United States", "AK": "United States", "AL": "United States",
    "KA": "United States", "KB": "United States", "KC": "United States",
    "KD": "United States", "KE": "United States", "KF": "United States",
    "KG": "United States", "KH": "United States", "KI": "United States",
    "KJ": "United States", "KK": "United States", "KL": "United States",
    "KM": "United States", "KN": "United States", "KO": "United States",
    "KP": "United States", "KQ": "United States", "KR": "United States",
    "KS": "United States", "KT": "United States", "KU": "United States",
    "KV": "United States", "KW": "United States", "KX": "United States",
    "KY": "United States", "KZ": "United States",
    "NA": "United States", "NB": "United States", "NC": "United States",
    "ND": "United States", "NE": "United States", "NF": "United States",
    "NG": "United States", "NH": "United States", "NI": "United States",
    "NJ": "United States", "NK": "United States", "NL": "United States",
    "NM": "United States", "NN": "United States", "NO": "United States",
    "NP": "United States", "NQ": "United States",
    "WA": "United States", "WB": "United States", "WC": "United States",
    "WD": "United States", "WE": "United States", "WF": "United States",
    "WG": "United States", "WH": "United States", "WI": "United States",
    "WJ": "United States", "WK": "United States", "WL": "United States",
    "WM": "United States", "WN": "United States", "WO": "United States",
    "WP": "United States", "WQ": "United States", "WR": "United States",
    "WS": "United States", "WT": "United States", "WU": "United States",
    "WV": "United States", "WW": "United States", "WX": "United States",
    "WY": "United States", "WZ": "United States",
    "KP3": "United States", "KP4": "United States", "NP3": "United States", "NP4": "United States",
    "VA": "Canada", "VE": "Canada", "VO": "Canada", "VY": "Canada",
    "R": "Russia", "RA": "Russia", "RB": "Russia", "RC": "Russia",
    "RD": "Russia", "RE": "Russia", "RF": "Russia", "RG": "Russia",
    "RH": "Russia", "RI": "Russia", "RJ": "Russia", "RK": "Russia",
    "RL": "Russia", "RM": "Russia", "RN": "Russia", "RO": "Russia",
    "RP": "Russia", "RQ": "Russia", "RR": "Russia", "RS": "Russia",
    "RT": "Russia", "RU": "Russia", "RV": "Russia", "RW": "Russia",
    "RX": "Russia", "RY": "Russia", "RZ": "Russia",
    "UA": "Russia", "UB": "Russia", "UC": "Russia", "UD": "Russia",
    "UE": "Russia", "UF": "Russia", "UG": "Russia", "UH": "Russia",
    "UI": "Russia",
    "3V": "Tunisia",
    "5B": "Cyprus",
    "CN": "Morocco",
    "SU": "Egypt",
    "ZS": "South Africa",
    "VK": "Australia",
    "ZL": "New Zealand",
    "YB": "Indonesia",
    "DU": "Philippines",
    "4X": "Israel", "4Z": "Israel",
    "A6": "United Arab Emirates",
    "A7": "Qatar",
    "A9": "Bahrain",
    "HZ": "Saudi Arabia",
    "EX": "Kyrgyzstan",
    "EK": "Armenia",
    "UK": "Uzbekistan",
    "UN": "Kazakhstan",
    "EY": "Tajikistan",
    "EZ": "Turkmenistan",
    "5R": "Madagascar",
    "9X": "Rwanda",
    "HI": "Dominican Republic",
    "HP": "Panama",
    "CM": "Cuba", "CO": "Cuba",
    "LU": "Argentina",
    "CX": "Uruguay",
    "CE": "Chile",
    "OA": "Peru",
    "HC": "Ecuador",
    "YV": "Venezuela",
    "HK": "Colombia", "HJ": "Colombia",
    "XE": "Mexico",
    "ZB": "Gibraltar",
    "VU": "India",
    "BA": "China", "BG": "China", "BH": "China",
    "VR": "Hong Kong",
    "BV": "Taiwan",
    "HL": "South Korea",
    "7X": "Algeria",
    "ST": "Sudan",
    "5A": "Libya",
    "5N": "Nigeria",
    "9G": "Ghana",
    "9K": "Kuwait",
    "AP": "Pakistan",
    "HS": "Thailand",
    "9M": "Malaysia",
    "9V": "Singapore",
    "9N": "Nepal",
    "EP": "Iran",
    "YI": "Iraq",
    "JY": "Jordan",
    "OD": "Lebanon",
    "YK": "Syria",
    "4L": "Georgia",
    "4J": "Azerbaijan",
    "JT": "Mongolia",
    "S2": "Bangladesh",
}


def get_country_from_callsign(call):
    if not call:
        return "Desconocido"
    call = call.upper().strip()
    if "/" in call:
        call = call.split("/")[0]
    max_len = min(4, len(call))
    for length in range(max_len, 0, -1):
        prefix = call[:length]
        if prefix in PREFIX_COUNTRY_MAP:
            return PREFIX_COUNTRY_MAP[prefix]
    return "Desconocido"


def assign_countries(qsos):
    for qso in qsos:
        country = qso.get("COUNTRY", "")
        if not country or country == "Desconocido" or country == "Unknown":
            call = qso.get("CALL", "")
            if call:
                qso["COUNTRY"] = get_country_from_callsign(call)


# Paleta de colores para operadores
OPERATOR_COLORS = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#ffff33",
    "#a65628",
    "#f781bf",
    "#999999",
    "#66c2a5",
]


# ==============================================================================
# PARSEO ADIF
# ==============================================================================


def parse_adi_file(filename):
    """
    Parsea archivo ADIF y devuelve lista de QSOs con operador.

    Args:
        filename (str): Ruta al archivo .adi

    Returns:
        list: Lista de diccionarios QSO con campo OPERATOR
    """
    encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
    content = None

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue

    if content is None:
        with open(filename, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

    eoh_match = re.search(r"<EOH>", content, re.IGNORECASE)
    if not eoh_match:
        return []

    qso_data = content[eoh_match.end() :]
    qso_records = re.split(r"<EOR>", qso_data, flags=re.IGNORECASE)

    parsed_qsos = []

    for record in qso_records:
        if not record.strip():
            continue

        qso = {}
        fields = re.findall(r"<([^>]+)>([^<]*)", record)

        for field_def, value in fields:
            if ":" in field_def:
                field_name, length = field_def.split(":", 1)
                try:
                    length = int(length)
                    value = value[:length]
                except ValueError:
                    pass
            else:
                field_name = field_def

            qso[field_name.upper()] = value.strip()

        if qso:
            parsed_qsos.append(qso)

    return parsed_qsos


# ==============================================================================
# ANÁLISIS POR OPERADOR
# ==============================================================================


def group_by_operator(qsos):
    """
    Agrupa QSOs por operador.

    Args:
        qsos (list): Lista de QSOs parseados

    Returns:
        dict: {operador: [lista de QSOs]}
    """
    operators = defaultdict(list)

    for qso in qsos:
        operator = qso.get("OPERATOR", "DESCONOCIDO")
        if operator:
            operators[operator].append(qso)

    return dict(operators)


def analyze_operator_stats(qsos):
    """
    Genera estadísticas detalladas de un operador.

    Args:
        qsos (list): Lista de QSOs del operador

    Returns:
        dict: Estadísticas {
            'total': número total de QSOs,
            'bandas': {banda: count},
            'modos': {modo: count},
            'horas': {hora: count},
            'dias': {dia_semana: count},
            'paises': {país: count}
        }
    """
    bandas = Counter()
    modos = Counter()
    horas = Counter()
    dias = Counter()
    paises = Counter()

    dias_nombres = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    for qso in qsos:
        # Banda
        band = qso.get("BAND", "Desconocida")
        if band:
            # Normalizar: 20M y 20m son lo mismo
            band_normalized = band.upper().replace("M", "M").replace("C", "CM")
            bandas[band_normalized] += 1

        # Modo
        mode = qso.get("MODE", "Desconocido")
        if mode:
            modos[mode] += 1

        # Hora
        time_str = qso.get("TIME_ON", "")
        if time_str and len(time_str) >= 2:
            try:
                hour = int(time_str[:2])
                horas[hour] += 1
            except ValueError:
                pass

        # Día de la semana
        date_str = qso.get("QSO_DATE", "")
        if date_str and len(date_str) >= 8:
            try:
                date = datetime.strptime(date_str[:8], "%Y%m%d")
                dia = dias_nombres[date.weekday()]
                dias[dia] += 1
            except ValueError:
                pass

        # País
        country = qso.get("COUNTRY", "Desconocido")
        if country:
            paises[country] += 1

    return {
        "total": len(qsos),
        "bandas": dict(bandas.most_common()),
        "modos": dict(modos.most_common()),
        "horas": dict(horas.most_common()),
        "dias": dict(dias.most_common()),
        "paises": dict(paises.most_common()),
    }


# ==============================================================================
# GRÁFICOS
# ==============================================================================


def create_operator_summary_chart(operators_data, output_prefix="operador"):
    """
    Genera gráfico resumen comparativo de todos los operadores.

    Muestra barras apiladas de QSOs por operador.

    Args:
        operators_data (dict): {operador: {stats}}
        output_prefix (str): Prefijo para el nombre del archivo
    """
    if not operators_data:
        return

    # Ordenar por total de QSOs
    sorted_ops = sorted(
        operators_data.items(), key=lambda x: x[1]["total"], reverse=True
    )
    operators = [op[0] for op in sorted_ops]
    totals = [op[1]["total"] for op in sorted_ops]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Barras de total
    colors = [OPERATOR_COLORS[i % len(OPERATOR_COLORS)] for i in range(len(operators))]
    bars = ax1.bar(operators, totals, color=colors, edgecolor="black", alpha=0.8)
    ax1.set_xlabel("Operador", fontsize=12)
    ax1.set_ylabel("Total de QSOs", fontsize=12)
    ax1.set_title("QSOs por Operador", fontsize=14, fontweight="bold")
    ax1.tick_params(axis="x", rotation=45)

    for bar, total in zip(bars, totals):
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + 1,
            str(total),
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    # Pastel del total
    ax2.pie(totals, labels=operators, autopct="%1.1f%%", colors=colors, startangle=90)
    ax2.set_title("Distribución por Operador", fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.savefig(f"{output_prefix}_resumen.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"  ✓ {output_prefix}_resumen.png")


def create_bands_by_operator_chart(operators_data, output_prefix="operador"):
    """
    Genera gráfico de barras por banda para cada operador.

    Args:
        operators_data (dict): {operador: {stats}}
        output_prefix (str): Prefijo para el nombre del archivo
    """
    if not operators_data:
        return

    # Obtener todas las bandas únicas
    all_bands = set()
    for op_data in operators_data.values():
        all_bands.update(op_data["bandas"].keys())
    all_bands = sorted(all_bands)

    # Preparar datos para barras apiladas
    n_operators = len(operators_data)
    n_bands = len(all_bands)

    # Matrix: operadores x bandas
    data_matrix = np.zeros((n_operators, n_bands))
    operator_names = list(operators_data.keys())

    for i, op in enumerate(operator_names):
        for j, band in enumerate(all_bands):
            data_matrix[i][j] = operators_data[op]["bandas"].get(band, 0)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

    # Barras agrupadas
    x = np.arange(len(operator_names))
    width = 0.8 / n_bands

    for j, band in enumerate(all_bands):
        offset = (j - n_bands / 2 + 0.5) * width
        values = data_matrix[:, j]
        bars = ax1.bar(x + offset, values, width, label=band, alpha=0.8)

    ax1.set_xlabel("Operador", fontsize=12)
    ax1.set_ylabel("Número de QSOs", fontsize=12)
    ax1.set_title("Distribución por Banda y Operador", fontsize=14, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(operator_names, rotation=45)
    ax1.legend(title="Banda", bbox_to_anchor=(1.02, 1), loc="upper left")

    # Heatmap
    im = ax2.imshow(data_matrix, cmap="YlGnBu", aspect="auto")

    ax2.set_xticks(range(n_bands))
    ax2.set_xticklabels(all_bands, rotation=45)
    ax2.set_yticks(range(n_operators))
    ax2.set_yticklabels(operator_names)
    ax2.set_xlabel("Banda", fontsize=12)
    ax2.set_ylabel("Operador", fontsize=12)
    ax2.set_title("Heatmap: Banda vs Operador", fontsize=14, fontweight="bold")

    plt.colorbar(im, ax=ax2, label="QSOs")

    # Añadir valores en celdas
    for i in range(n_operators):
        for j in range(n_bands):
            val = int(data_matrix[i][j])
            if val > 0:
                color = (
                    "white" if data_matrix[i][j] > data_matrix.max() / 2 else "black"
                )
                ax2.text(
                    j, i, str(val), ha="center", va="center", color=color, fontsize=8
                )

    plt.tight_layout()
    plt.savefig(f"{output_prefix}_bandas.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"  ✓ {output_prefix}_bandas.png")


def create_modes_by_operator_chart(operators_data, output_prefix="operador"):
    """
    Genera gráfico de modos para cada operador.

    Args:
        operators_data (dict): {operador: {stats}}
        output_prefix (str): Prefijo para el nombre del archivo
    """
    if not operators_data:
        return

    all_modes = set()
    for op_data in operators_data.values():
        all_modes.update(op_data["modos"].keys())
    all_modes = sorted(all_modes)

    n_operators = len(operators_data)
    n_modes = len(all_modes)

    data_matrix = np.zeros((n_operators, n_modes))
    operator_names = list(operators_data.keys())

    for i, op in enumerate(operator_names):
        for j, mode in enumerate(all_modes):
            data_matrix[i][j] = operators_data[op]["modos"].get(mode, 0)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

    # Barras agrupadas
    x = np.arange(len(operator_names))
    width = 0.8 / n_modes

    mode_colors = plt.cm.Set2(np.linspace(0, 1, n_modes))

    for j, mode in enumerate(all_modes):
        offset = (j - n_modes / 2 + 0.5) * width
        values = data_matrix[:, j]
        ax1.bar(x + offset, values, width, label=mode, color=mode_colors[j], alpha=0.8)

    ax1.set_xlabel("Operador", fontsize=12)
    ax1.set_ylabel("Número de QSOs", fontsize=12)
    ax1.set_title("Distribución por Modo y Operador", fontsize=14, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(operator_names, rotation=45)
    ax1.legend(title="Modo", bbox_to_anchor=(1.02, 1), loc="upper left")

    # Heatmap
    im = ax2.imshow(data_matrix, cmap="PuBuGn", aspect="auto")

    ax2.set_xticks(range(n_modes))
    ax2.set_xticklabels(all_modes, rotation=45)
    ax2.set_yticks(range(n_operators))
    ax2.set_yticklabels(operator_names)
    ax2.set_xlabel("Modo", fontsize=12)
    ax2.set_ylabel("Operador", fontsize=12)
    ax2.set_title("Heatmap: Modo vs Operador", fontsize=14, fontweight="bold")

    plt.colorbar(im, ax=ax2, label="QSOs")

    for i in range(n_operators):
        for j in range(n_modes):
            val = int(data_matrix[i][j])
            if val > 0:
                color = (
                    "white" if data_matrix[i][j] > data_matrix.max() / 2 else "black"
                )
                ax2.text(
                    j, i, str(val), ha="center", va="center", color=color, fontsize=8
                )

    plt.tight_layout()
    plt.savefig(f"{output_prefix}_modos.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"  ✓ {output_prefix}_modos.png")


def create_hours_by_operator_chart(operators_data, output_prefix="operador"):
    """
    Genera gráfico de actividad horaria para cada operador.

    Args:
        operators_data (dict): {operador: {stats}}
        output_prefix (str): Prefijo para el nombre del archivo
    """
    if not operators_data:
        return

    operator_names = list(operators_data.keys())
    n_operators = len(operator_names)

    # Matrix: operadores x 24 horas
    hours_matrix = np.zeros((n_operators, 24))

    for i, op in enumerate(operator_names):
        horas = operators_data[op]["horas"]
        for hour in range(24):
            hours_matrix[i][hour] = horas.get(hour, 0)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12))

    # Heatmap de horas
    im = ax1.imshow(hours_matrix, cmap="OrRd", aspect="auto")

    ax1.set_xticks(range(24))
    ax1.set_xticklabels([f"{h:02d}" for h in range(24)], fontsize=9)
    ax1.set_yticks(range(n_operators))
    ax1.set_yticklabels(operator_names)
    ax1.set_xlabel("Hora (UTC)", fontsize=12)
    ax1.set_ylabel("Operador", fontsize=12)
    ax1.set_title(
        "Heatmap: Actividad Horaria por Operador", fontsize=14, fontweight="bold"
    )

    plt.colorbar(im, ax=ax1, label="QSOs")

    # Líneas de tendencia por operador
    hours = list(range(24))
    for i, op in enumerate(operator_names):
        color = OPERATOR_COLORS[i % len(OPERATOR_COLORS)]
        ax2.plot(
            hours,
            hours_matrix[i],
            marker="o",
            label=op,
            color=color,
            linewidth=2,
            markersize=6,
        )

    ax2.set_xlabel("Hora (UTC)", fontsize=12)
    ax2.set_ylabel("Número de QSOs", fontsize=12)
    ax2.set_title("Distribución Horaria por Operador", fontsize=14, fontweight="bold")
    ax2.set_xticks(hours)
    ax2.set_xticklabels([f"{h:02d}:00" for h in hours], rotation=45)
    ax2.legend(title="Operador", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_prefix}_horas.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"  ✓ {output_prefix}_horas.png")


def create_operator_individual_charts(operators_data):
    """
    Genera gráficos individuales detallados para cada operador.

    Args:
        operators_data (dict): {operador: {stats}}
    """
    dias_nombres = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    for i, (operator, data) in enumerate(operators_data.items()):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        color = OPERATOR_COLORS[i % len(OPERATOR_COLORS)]

        # 1. Bandas
        if data["bandas"]:
            bands = list(data["bandas"].keys())
            band_counts = list(data["bandas"].values())
            ax1.bar(bands, band_counts, color=color, edgecolor="black", alpha=0.7)
            ax1.set_title(f"Bandas - {operator}", fontsize=12, fontweight="bold")
            ax1.set_xlabel("Banda")
            ax1.set_ylabel("QSOs")
            ax1.tick_params(axis="x", rotation=45)

        # 2. Modos
        if data["modos"]:
            modos = list(data["modos"].keys())
            mode_counts = list(data["modos"].values())
            colors_pie = plt.cm.Set3(np.linspace(0, 1, len(modos)))
            ax2.pie(mode_counts, labels=modos, autopct="%1.1f%%", colors=colors_pie)
            ax2.set_title(f"Modos - {operator}", fontsize=12, fontweight="bold")

        # 3. Horas
        hours = list(range(24))
        hour_counts = [data["horas"].get(h, 0) for h in hours]
        ax3.fill_between(hours, hour_counts, alpha=0.5, color=color)
        ax3.plot(hours, hour_counts, marker="o", color=color, linewidth=2)
        ax3.set_title(f"Actividad Horaria - {operator}", fontsize=12, fontweight="bold")
        ax3.set_xlabel("Hora (UTC)")
        ax3.set_ylabel("QSOs")
        ax3.set_xticks(hours)
        ax3.set_xticklabels([f"{h:02d}" for h in hours], fontsize=8)
        ax3.grid(True, alpha=0.3)

        # 4. Días de la semana
        if data["dias"]:
            dias_ordered = [d for d in dias_nombres if d in data["dias"]]
            dia_counts = [data["dias"][d] for d in dias_ordered]
            ax4.bar(dias_ordered, dia_counts, color=color, edgecolor="black", alpha=0.7)
            ax4.set_title(
                f"Días de la Semana - {operator}", fontsize=12, fontweight="bold"
            )
            ax4.set_xlabel("Día")
            ax4.set_ylabel("QSOs")

        fig.suptitle(
            f"{operator} - {data['total']} QSOs", fontsize=16, fontweight="bold"
        )
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        safe_name = operator.replace("/", "_").replace(" ", "_")
        plt.savefig(f"operador_{safe_name}.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"  ✓ operador_{safe_name}.png")


def create_comparison_bands_chart(operators_data, output_prefix="operador"):
    """
    Genera gráfico comparativo de bandas (barras agrupadas).

    Args:
        operators_data (dict): {operador: {stats}}
        output_prefix (str): Prefijo para el nombre del archivo
    """
    if not operators_data:
        return

    operators = list(operators_data.keys())

    # Encontrar bandas principales (las que aparecen en al menos un operador con > 0)
    all_bands = set()
    for data in operators_data.values():
        all_bands.update(data["bandas"].keys())

    # Filtrar solo bandas con actividad significativa
    band_totals = Counter()
    for data in operators_data.values():
        band_totals.update(data["bandas"])

    main_bands = [b for b, c in band_totals.most_common(8)]

    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(operators))
    width = 0.8 / len(main_bands)

    for j, band in enumerate(main_bands):
        offset = (j - len(main_bands) / 2 + 0.5) * width
        values = [operators_data[op]["bandas"].get(band, 0) for op in operators]
        bars = ax.bar(x + offset, values, width, label=band, alpha=0.8)

    ax.set_xlabel("Operador", fontsize=12)
    ax.set_ylabel("Número de QSOs", fontsize=12)
    ax.set_title("Comparación de Bandas por Operador", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(operators, rotation=45)
    ax.legend(title="Banda", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(f"{output_prefix}_comparacion_bandas.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"  ✓ {output_prefix}_comparacion_bandas.png")


def create_comparison_modes_chart(operators_data, output_prefix="operador"):
    """
    Genera gráfico comparativo de modos (barras agrupadas).

    Args:
        operators_data (dict): {operador: {stats}}
        output_prefix (str): Prefijo para el nombre del archivo
    """
    if not operators_data:
        return

    operators = list(operators_data.keys())

    mode_totals = Counter()
    for data in operators_data.values():
        mode_totals.update(data["modos"])

    main_modes = [m for m, c in mode_totals.most_common(6)]

    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(operators))
    width = 0.8 / len(main_modes)
    mode_colors = plt.cm.Set2(np.linspace(0, 1, len(main_modes)))

    for j, mode in enumerate(main_modes):
        offset = (j - len(main_modes) / 2 + 0.5) * width
        values = [operators_data[op]["modos"].get(mode, 0) for op in operators]
        ax.bar(x + offset, values, width, label=mode, color=mode_colors[j], alpha=0.8)

    ax.set_xlabel("Operador", fontsize=12)
    ax.set_ylabel("Número de QSOs", fontsize=12)
    ax.set_title("Comparación de Modos por Operador", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(operators, rotation=45)
    ax.legend(title="Modo", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(f"{output_prefix}_comparacion_modos.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"  ✓ {output_prefix}_comparacion_modos.png")


# ==============================================================================
# REPORTE
# ==============================================================================


def generate_report(operators_data):
    """
    Genera reporte completo de estadísticas por operador.

    Args:
        operators_data (dict): {operador: {stats}}
    """
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS POR OPERADOR")
    print("=" * 70)

    # Ordenar por total de QSOs
    sorted_ops = sorted(
        operators_data.items(), key=lambda x: x[1]["total"], reverse=True
    )

    for operator, stats in sorted_ops:
        print(f"\n{'─' * 50}")
        print(f"📻 OPERADOR: {operator}")
        print(f"{'─' * 50}")
        print(f"   Total QSOs: {stats['total']}")

        if stats["bandas"]:
            top_band = max(stats["bandas"].items(), key=lambda x: x[1])
            print(f"   Banda favorita: {top_band[0]} ({top_band[1]} QSOs)")

        if stats["modos"]:
            top_mode = max(stats["modos"].items(), key=lambda x: x[1])
            print(f"   Modo favorito: {top_mode[0]} ({top_mode[1]} QSOs)")

        if stats["horas"]:
            top_hour = max(stats["horas"].items(), key=lambda x: x[1])
            print(f"   Hora pico: {top_hour[0]:02d}:00 UTC ({top_hour[1]} QSOs)")

        if stats["dias"]:
            top_day = max(stats["dias"].items(), key=lambda x: x[1])
            print(f"   Día favorito: {top_day[0]} ({top_day[1]} QSOs)")

        if stats["paises"]:
            print(f"   Países únicos: {len(stats['paises'])}")

    print("\n" + "=" * 70)


# ==============================================================================
# MAIN
# ==============================================================================


def main():
    """
    Función principal del programa.
    """
    filename = "aaa.adi"

    if not os.path.exists(filename):
        print(f"Error: No se encuentra el archivo {filename}")
        return

    print("=" * 70)
    print("ANÁLISIS DE CONTACTOS POR OPERADOR")
    print("=" * 70)
    print(f"\nProcesando archivo: {filename}")

    qsos = parse_adi_file(filename)
    print(f"Total QSOs encontrados: {len(qsos)}")

    # Asignar países basados en prefijos de indicativos
    print("Asignando países basados en prefijos de indicativos...")
    assign_countries(qsos)

    # Agrupar por operador
    operators_qsos = group_by_operator(qsos)
    print(f"Operadores encontrados: {len(operators_qsos)}")
    print(f"Operadores: {list(operators_qsos.keys())}")

    # Analizar cada operador
    operators_data = {}
    for operator, op_qsos in operators_qsos.items():
        operators_data[operator] = analyze_operator_stats(op_qsos)

    # Generar reporte
    generate_report(operators_data)

    # Generar gráficos
    print("\n" + "-" * 50)
    print("Generando gráficos...")
    print("-" * 50)

    # Gráficos comparativos
    create_operator_summary_chart(operators_data)
    create_bands_by_operator_chart(operators_data)
    create_modes_by_operator_chart(operators_data)
    create_hours_by_operator_chart(operators_data)

    # Gráficos de comparación
    create_comparison_bands_chart(operators_data)
    create_comparison_modes_chart(operators_data)

    # Gráficos individuales
    print("\n  Gráficos individuales por operador:")
    create_operator_individual_charts(operators_data)

    # Resumen final
    print("\n" + "=" * 70)
    print("ANÁLISIS COMPLETADO")
    print("=" * 70)
    print("\nArchivos generados:")
    print("  COMPARATIVOS:")
    print("    - operador_resumen.png")
    print("    - operador_bandas.png")
    print("    - operador_modos.png")
    print("    - operador_horas.png")
    print("    - operador_comparacion_bandas.png")
    print("    - operador_comparacion_modos.png")
    print("  INDIVIDUALES:")
    for op in operators_qsos.keys():
        safe_name = op.replace("/", "_").replace(" ", "_")
        print(f"    - operador_{safe_name}.png")
    print("=" * 70)


if __name__ == "__main__":
    main()
