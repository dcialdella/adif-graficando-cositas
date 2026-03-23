#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ANALIZADOR DE ARCHIVOS ADIF PARA RADIOAFICIONADOS
================================================================================

Este programa analiza archivos en formato ADIF (Amateur Data Interchange Format)
y genera gráficos estadísticos detallados de los contactos de radioaficionado.

Autor: Análisis de logs EA1JBW/AM26PADRE
Versión: 2.0
Fecha: Marzo 2026

================================================================================
ESTRUCTURA DEL PROGRAMA
================================================================================

El programa está organizado en las siguientes secciones:

1. PARSEO (parse_adi_file)
   - Lee y parsea archivos ADIF
   - Maneja diferentes codificaciones de caracteres

2. ANÁLISIS (funciones analyze_*)
   - analyze_countries()     - Contadores por país
   - analyze_locators()      - Localizadores Maidenhead
   - analyze_mode_band()     - Modos y bandas
   - analyze_stations()      - Estaciones/indicativos
   - analyze_time_distribution() - Distribución horaria
   - analyze_zones()         - Zonas CQ e ITU
   - analyze_band_mode_matrix() - Matriz banda vs modo

3. CONVERSIÓN (funciones de utilidad)
   - maidenhead_to_latlon() - Convierte localizador a coordenadas

4. GRÁFICOS (funciones create_*)
   - create_countries_chart()     - Top países (barras + pastel)
   - create_locators_chart()      - Top localizadores
   - create_mode_band_chart()     - Modos y bandas (4 subplots)
   - create_stations_chart()      - Top estaciones
   - create_time_distribution_chart() - Distribución horaria general
   - create_world_map()           - Mapa mundial de localizadores
   - create_heatmap_day_hour()     - Heatmap día/hora
   - create_distance_histogram()   - Histograma de distancias
   - create_zones_chart()         - Zonas CQ e ITU
   - create_timeline()            - QSOs acumulados en el tiempo
   - create_frequency_histogram()  - Distribución de frecuencias
   - create_power_distance_scatter() - Potencia vs distancia
   - create_band_mode_heatmap()   - Matriz banda vs modo
   - create_dxcc_analysis()       - Entidades DXCC
   - create_summary_dashboard()    - Dashboard resumen
   - create_qrz_lookups_chart()   - Lookups en QRZ.com
   - create_fonia_por_hora_chart() - Fonía por hora UTC

5. REPORTE (generate_statistics_report)
   - Genera todos los gráficos y estadísticas

6. PRINCIPAL (main)
   - Punto de entrada del programa

================================================================================
CAMPOS ADIF SOPORTADOS
================================================================================

El programa extrae y analiza los siguientes campos del archivo ADIF:

- CALL:      Indicativo de la estación contactada
- COUNTRY:   País de la estación
- FREQ:      Frecuencia en MHz
- BAND:      Banda de operación (20M, 40M, etc.)
- MODE:      Modo de operación (SSB, FT8, FM, etc.)
- TX_PWR:    Potencia de transmisión en vatios
- GRIDSQUARE: Locator Maidenhead (ej: IO91VL)
- QSO_DATE:  Fecha del contacto (formato: YYYYMMDD)
- TIME_ON:   Hora de inicio (formato: HHMM UTC)
- DISTANCE:  Distancia en kilómetros
- CQZ:       Zona CQ
- ITUZ:      Zona ITU
- NAME:      Nombre del operador
- RST_RCVD:  Reporte recibido
- RST_SENT:  Reporte enviado

================================================================================
SALIDA DEL PROGRAMA
================================================================================

El programa genera los siguientes archivos:

ESTADÍSTICAS (JSON):
- estadisticas_adi.json - Todos los datos en formato JSON

GRÁFICOS (PNG):
- BÁSICOS:
  * grafico_paises.png         - Top 15 países con pastel
  * grafico_localizadores.png   - Top 20 localizadores
  * grafico_modos_bandas.png   - 4 subplots: modos, bandas, pasteles
  * grafico_estaciones_top.png  - Top 20 estaciones (horizontal)
  * grafico_distribucion_horaria.png - Barras + línea por hora

- AVANZADOS:
  * grafico_mapa_mundial.png       - Dispersión de localizadores en mapa
  * grafico_heatmap_dia_hora.png   - Actividad día/hora (semanal)
  * grafico_distancias.png         - Histograma lineal y logarítmico
  * grafico_zonas.png              - Zonas CQ e ITU
  * grafico_timeline.png           - Progreso temporal de QSOs
  * grafico_frecuencias.png        - Histograma de frecuencias
  * grafico_potencia_distancia.png - Scatter y hexbin
  * grafico_banda_modo.png         - Heatmap interactivo
  * grafico_dxcc.png              - Top 20 entidades DXCC
  * grafico_dashboard.png         - Resumen en 6 subplots

- ESPECIALES:
  * grafico_qrz_lookups.png      - Lookups en QRZ.com
  * grafico_fonia_por_hora.png   - Fonía (SSB/FM) por hora UTC

================================================================================
DEPENDENCIAS
================================================================================

Python >= 3.8
- matplotlib >= 3.5.0  (gráficos)
- seaborn >= 0.11.0   (estilos)
- pandas >= 1.3.0     (manipulación de datos)
- numpy >= 1.21.0     (cálculos numéricos)

Instalación: pip install -r requirements.txt

================================================================================
USO
================================================================================

Ejecución completa (crea entorno si no existe):
  ./setup_and_run.sh

Ejecución rápida (usa entorno existente):
  ./run_analysis.sh

Directamente con Python:
  python analizar_adi_grafico.py

================================================================================
"""

import re
import os
from collections import defaultdict, Counter, OrderedDict
from datetime import datetime
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# ==============================================================================
# CONFIGURACIÓN GLOBAL DE GRÁFICOS
# ==============================================================================

plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True


# ==============================================================================
# SECCIÓN 1: PARSEO DEL ARCHIVO ADIF
# ==============================================================================

def parse_adi_file(filename):
    """
    Parsea un archivo ADIF y devuelve una lista de diccionarios con los QSOs.
    
    El formato ADIF consiste en campos entre ángulos: <CAMPO:longitud>valor
    Después de <EOH> (End Of Header) vienen los registros QSO terminados en <EOR>.
    
    Args:
        filename (str): Ruta al archivo .adi a parsear
        
    Returns:
        list: Lista de diccionarios, cada uno representando un QSO
              con claves en mayúsculas (CALL, COUNTRY, FREQ, etc.)
              
    Note:
        Maneja automáticamente codificaciones UTF-8, Latin-1, CP1252, ISO-8859-1
    """
    # Intentar diferentes codificaciones para compatibilidad
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    content = None
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    # Fallback: reemplazar caracteres no válidos
    if content is None:
        with open(filename, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    
    # Buscar el final del header (EOH = End Of Header)
    eoh_match = re.search(r'<EOH>', content)
    if not eoh_match:
        return []
    
    # Extraer datos después del header
    qso_data = content[eoh_match.end():]
    
    # Separar por registros QSO (EOR = End Of Record)
    qso_records = qso_data.split('<EOR>')
    
    parsed_qsos = []
    
    for record in qso_records:
        if not record.strip():
            continue
            
        qso = {}
        # Buscar todos los campos: <NOMBRE:LONGITUD>valor
        fields = re.findall(r'<([^>]+)>([^<]*)', record)
        
        for field_def, value in fields:
            # Parsear definición de campo (NOMBRE:LONGITUD)
            if ':' in field_def:
                field_name, length = field_def.split(':', 1)
                try:
                    length = int(length)
                    # Recortar valor según longitud especificada en ADIF
                    value = value[:length]
                except ValueError:
                    pass
            else:
                field_name = field_def
            
            # Normalizar a mayúsculas
            qso[field_name.upper()] = value.strip()
        
        if qso:
            parsed_qsos.append(qso)
    
    return parsed_qsos


# ==============================================================================
# SECCIÓN 2: FUNCIONES DE ANÁLISIS
# ==============================================================================

def analyze_countries(qsos):
    """
    Cuenta QSOs por país.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        dict: Diccionario ordenado {país: cantidad} de mayor a menor
    """
    countries = Counter()
    
    for qso in qsos:
        country = qso.get('COUNTRY', 'Desconocido')
        if country:
            countries[country] += 1
    
    return dict(countries.most_common())


def analyze_locators(qsos):
    """
    Cuenta QSOs por localizador Maidenhead.
    
    Los localizadores Maidenhead tienen formato: FN31pr (6 caracteres)
    - 2 letras: campo de longitude (-180 a -60)
    - 2 números: subcampo de 2° precisión  
    - 2 letras: subcampo de 5' precisión
    
    Se agrupan por los primeros 4 caracteres para análisis por cuadrícula principal.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        dict: Diccionario ordenado {locator: cantidad}
    """
    locators = Counter()
    
    for qso in qsos:
        locator = qso.get('GRIDSQUARE', '')
        if locator:
            # Tomar solo los primeros 4 caracteres (cuadrícula 2°)
            main_locator = locator[:4] if len(locator) >= 4 else locator
            locators[main_locator] += 1
    
    return dict(locators.most_common())


def analyze_mode_band(qsos):
    """
    Analiza distribución por modo y banda de operación.
    
    Modos comunes: SSB (fonía), FT8 (digital), FM, AM, CW, RTTY
    Bandas HF: 160M, 80M, 40M, 20M, 15M, 10M
    Bandas VHF/UHF: 2M, 70cm, 23cm
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        dict: {
            'por_modo': {modo: cantidad},
            'por_banda': {banda: cantidad},
            'modo_banda_combinado': {'modo - banda': cantidad}
        }
    """
    mode_band = Counter()
    modes = Counter()
    bands = Counter()
    
    for qso in qsos:
        mode = qso.get('MODE', 'Desconocido')
        band = qso.get('BAND', 'Desconocida')
        
        modes[mode] += 1
        bands[band] += 1
        mode_band[f"{mode} - {band}"] += 1
    
    return {
        'por_modo': dict(modes.most_common()),
        'por_banda': dict(bands.most_common()),
        'modo_banda_combinado': dict(mode_band.most_common())
    }


def analyze_stations(qsos):
    """
    Cuenta QSOs por indicativo de estación.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        dict: Diccionario ordenado {indicativo: cantidad}
    """
    stations = Counter()
    
    for qso in qsos:
        call = qso.get('CALL', '')
        if call:
            stations[call] += 1
    
    return dict(stations.most_common())


def analyze_time_distribution(qsos):
    """
    Analiza distribución horaria de QSOs en UTC.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        dict: Diccionario con claves 0-23 representando cada hora UTC
    """
    hours = Counter()
    
    for qso in qsos:
        time_on = qso.get('TIME_ON', '')
        if time_on and len(time_on) >= 2:
            try:
                hour = int(time_on[:2])
                hours[hour] += 1
            except ValueError:
                continue
    
    # Crear diccionario completo de 24 horas (incluye horas sin actividad)
    sorted_hours = {hour: hours.get(hour, 0) for hour in range(24)}
    
    return sorted_hours


def analyze_zones(qsos):
    """
    Analiza Zonas CQ y Zonas ITU contactadas.
    
    - Zonas CQ: 40 zonas numeradas (1-40), dividen el mundo por meridianos
    - Zonas ITU: 90 zonas, dividen el mundo por latitud y longitud
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        tuple: (dict_cq_zones, dict_itu_zones)
    """
    cq_zones = Counter()
    itu_zones = Counter()
    
    for qso in qsos:
        cqz = qso.get('CQZ', qso.get('CQ_ZONE', ''))
        ituz = qso.get('ITUZ', qso.get('ITU_ZONE', ''))
        
        if cqz:
            cq_zones[cqz] += 1
        if ituz:
            itu_zones[ituz] += 1
    
    return dict(cq_zones.most_common()), dict(itu_zones.most_common())


def analyze_band_mode_matrix(qsos):
    """
    Crea matriz de confusión banda vs modo para análisis cruzado.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        tuple: (matrix numpy, lista_bandas, lista_modos)
    """
    band_mode = defaultdict(lambda: defaultdict(int))
    all_bands = set()
    all_modes = set()
    
    for qso in qsos:
        band = qso.get('BAND', 'Unknown')
        mode = qso.get('MODE', 'Unknown')
        all_bands.add(band)
        all_modes.add(mode)
        band_mode[band][mode] += 1
    
    bands = sorted(all_bands)
    modes = sorted(all_modes)
    
    matrix = np.zeros((len(bands), len(modes)))
    for i, band in enumerate(bands):
        for j, mode in enumerate(modes):
            matrix[i][j] = band_mode[band][mode]
    
    return matrix, bands, modes


# ==============================================================================
# SECCIÓN 3: FUNCIONES DE UTILIDAD
# ==============================================================================

def maidenhead_to_latlon(locator):
    """
    Convierte un localizador Maidenhead a coordenadas geográficas.
    
    El sistema Maidenhead divide el mundo en campos de 18° de longitud 
    y 9° de latitud, subdivididos hasta precisión de 5'x2.5'.
    
    Ejemplo: IO91VL -> (51.5, -2.0) aproximadamente
    
    Args:
        locator (str): Localizador Maidenhead (mínimo 4 caracteres)
        
    Returns:
        tuple: (latitud, longitud) o (None, None) si es inválido
    """
    if not locator or len(locator) < 4:
        return None, None
    
    locator = locator.upper()
    
    try:
        # Campo: letras A-R (18 campos de 20°)
        lon = (ord(locator[0]) - ord('A')) * 20 - 180
        lat = (ord(locator[2]) - ord('A')) * 10 - 90
        
        # Subcampo: números 0-9 (10 subcampos de 2°)
        if len(locator) >= 4:
            lon += int(locator[1]) * 2
            lat += int(locator[3]) * 1
        
        # Sub-subcampo: letras A-X (24 subcampos de 5')
        if len(locator) >= 6:
            lon += (ord(locator[4]) - ord('A')) * (2/24)
            lat += (ord(locator[5]) - ord('A')) * (1/24)
        
        # Centro del cuadrado (no esquina)
        lon += 1
        lat += 0.5
        
        return lat, lon
        
    except (ValueError, IndexError):
        return None, None


# ==============================================================================
# SECCIÓN 4: GRÁFICOS - BÁSICOS
# ==============================================================================

def create_countries_chart(countries_data, total_qsos):
    """
    Genera gráfico de países con barras y pastel.
    
    Muestra top 15 países en barras horizontales y top 10 en pastel.
    
    Args:
        countries_data (dict): {país: cantidad}
        total_qsos (int): Total de QSOs para referencia
    """
    top_countries = dict(list(countries_data.items())[:15])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    countries = list(top_countries.keys())
    counts = list(top_countries.values())
    
    # Gráfico de barras
    bars = ax1.bar(countries, counts, color='skyblue', edgecolor='navy', alpha=0.7)
    ax1.set_title('Top 15 Países - Contactos por País', fontsize=14, fontweight='bold')
    ax1.set_xlabel('País')
    ax1.set_ylabel('Número de QSOs')
    ax1.tick_params(axis='x', rotation=45)
    
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}', ha='center', va='bottom')
    
    # Gráfico de pastel (top 10 + Otros)
    top_10 = dict(list(countries_data.items())[:10])
    others_count = sum(list(countries_data.values())[10:])
    if others_count > 0:
        top_10['Otros'] = others_count
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(top_10)))
    wedges, texts, autotexts = ax2.pie(
        top_10.values(), 
        labels=top_10.keys(), 
        autopct='%1.1f%%', 
        colors=colors, 
        startangle=90
    )
    ax2.set_title('Distribución por Países (Top 10)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('grafico_paises.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_locators_chart(locators_data):
    """
    Genera gráfico de localizadores Maidenhead más contactados.
    
    Args:
        locators_data (dict): {locator: cantidad}
    """
    top_locators = dict(list(locators_data.items())[:20])
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    locators = list(top_locators.keys())
    counts = list(top_locators.values())
    
    bars = ax.bar(locators, counts, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
    ax.set_title('Top 20 Localizadores Maidenhead', fontsize=14, fontweight='bold')
    ax.set_xlabel('Localizador (4 caracteres)')
    ax.set_ylabel('Número de QSOs')
    ax.tick_params(axis='x', rotation=45)
    
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{count}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('grafico_localizadores.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_mode_band_chart(mode_band_data):
    """
    Genera gráfico de 4 subplots: modos, bandas, y sus pasteles.
    
    Args:
        mode_band_data (dict): Datos de modos y bandas
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Subplot 1: Distribución por modo
    modes = list(mode_band_data['por_modo'].keys())
    mode_counts = list(mode_band_data['por_modo'].values())
    
    bars1 = ax1.bar(modes, mode_counts, color='coral', edgecolor='darkred', alpha=0.7)
    ax1.set_title('Distribución por Modo', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Modo')
    ax1.set_ylabel('Número de QSOs')
    
    for bar, count in zip(bars1, mode_counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}', ha='center', va='bottom')
    
    # Subplot 2: Distribución por banda
    bands = list(mode_band_data['por_banda'].keys())
    band_counts = list(mode_band_data['por_banda'].values())
    
    bars2 = ax2.bar(bands, band_counts, color='lightblue', edgecolor='darkblue', alpha=0.7)
    ax2.set_title('Distribución por Banda', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Banda')
    ax2.set_ylabel('Número de QSOs')
    
    for bar, count in zip(bars2, band_counts):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}', ha='center', va='bottom')
    
    # Subplot 3: Pastel de modos
    colors1 = plt.cm.Pastel1(np.linspace(0, 1, len(modes)))
    ax3.pie(mode_counts, labels=modes, autopct='%1.1f%%', colors=colors1, startangle=90)
    ax3.set_title('Distribución de Modos', fontsize=12, fontweight='bold')
    
    # Subplot 4: Pastel de bandas
    colors2 = plt.cm.Pastel2(np.linspace(0, 1, len(bands)))
    ax4.pie(band_counts, labels=bands, autopct='%1.1f%%', colors=colors2, startangle=90)
    ax4.set_title('Distribución de Bandas', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('grafico_modos_bandas.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_stations_chart(stations_data):
    """
    Genera gráfico horizontal de top estaciones por número de contactos.
    
    Args:
        stations_data (dict): {indicativo: cantidad}
    """
    top_stations = dict(list(stations_data.items())[:20])
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    stations = list(top_stations.keys())
    counts = list(top_stations.values())
    
    # Gráfico horizontal para mejor legibilidad de indicativos largos
    bars = ax.barh(stations, counts, color='gold', edgecolor='orange', alpha=0.7)
    ax.set_title('Top 20 Estaciones por Número de Contactos', fontsize=14, fontweight='bold')
    ax.set_xlabel('Número de QSOs')
    ax.set_ylabel('Indicativo')
    
    for bar, count in zip(bars, counts):
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                f'{count}', ha='left', va='center')
    
    ax.invert_yaxis()  # Mayor arriba
    
    plt.tight_layout()
    plt.savefig('grafico_estaciones_top.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_time_distribution_chart(time_data):
    """
    Genera gráfico de distribución horaria general (todas las modalidades).
    
    Args:
        time_data (dict): Diccionario {hora: cantidad} para 0-23
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    hours = list(range(24))
    counts = [time_data.get(hour, 0) for hour in hours]
    
    # Gráfico de barras
    bars = ax1.bar(hours, counts, color='mediumpurple', edgecolor='purple', alpha=0.7)
    ax1.set_title('Distribución de Contactos por Hora UTC', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Hora (UTC)')
    ax1.set_ylabel('Número de QSOs')
    ax1.set_xticks(hours)
    ax1.set_xticklabels([f'{h:02d}:00' for h in hours], rotation=45)
    
    for bar, count in zip(bars, counts):
        if count > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                    f'{count}', ha='center', va='bottom', fontsize=8)
    
    # Gráfico de línea con área
    ax2.plot(hours, counts, marker='o', linewidth=2, markersize=6, 
             color='darkviolet', markerfacecolor='mediumpurple')
    ax2.fill_between(hours, counts, alpha=0.3, color='mediumpurple')
    ax2.set_title('Tendencia de Actividad por Hora', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Hora (UTC)')
    ax2.set_ylabel('Número de QSOs')
    ax2.set_xticks(hours)
    ax2.set_xticklabels([f'{h:02d}:00' for h in hours], rotation=45)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('grafico_distribucion_horaria.png', dpi=300, bbox_inches='tight')
    plt.close()


# ==============================================================================
# SECCIÓN 4: GRÁFICOS - AVANZADOS
# ==============================================================================

def create_world_map(qsos):
    """
    Genera mapa mundial con scatter plot de localizadores contactados.
    
    Utiliza maidenhead_to_latlon() para convertir localizadores a coordenadas.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
    """
    try:
        lats, lons, countries, counts = [], [], [], []
        
        # Agrupar por localizador para evitar duplicados
        loc_count = Counter()
        for qso in qsos:
            loc = qso.get('GRIDSQUARE', '')
            if loc and len(loc) >= 4:
                # Usar 6 caracteres para mayor precisión
                loc_main = loc[:6] if len(loc) >= 6 else loc[:4]
                country = qso.get('COUNTRY', 'Unknown')
                loc_count[(loc_main, country)] += 1
        
        # Convertir localizadores a coordenadas
        for (loc, country), count in loc_count.items():
            lat, lon = maidenhead_to_latlon(loc)
            if lat is not None and lon is not None:
                lats.append(lat)
                lons.append(lon)
                countries.append(country)
                counts.append(count)
        
        if not lats:
            print("  (no hay localizadores válidos para el mapa)")
            return
        
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        
        # Scatter plot con tamaño proporcional a cantidad de contactos
        scatter = ax.scatter(
            lons, lats, 
            c=counts, 
            cmap='hot', 
            s=[c*5 for c in counts], 
            alpha=0.6, 
            edgecolors='black', 
            linewidth=0.5
        )
        
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.set_xlabel('Longitud', fontsize=12)
        ax.set_ylabel('Latitud', fontsize=12)
        ax.set_title('Distribución Mundial de Localizadores Maidenhead', 
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Líneas de referencia
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)  # Ecuador
        ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)   # Meridiano 0
        
        plt.colorbar(scatter, ax=ax, label='Número de QSOs')
        
        plt.tight_layout()
        plt.savefig('grafico_mapa_mundial.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        print(f"  (mapa mundial omitido: {e})")


def create_heatmap_day_hour(qsos):
    """
    Genera heatmap de actividad: día de la semana vs hora UTC.
    
    Útil para identificar patrones de actividad (contests, horarios favoritos).
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
    """
    day_hour = defaultdict(lambda: defaultdict(int))
    dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    for qso in qsos:
        date_str = qso.get('QSO_DATE', '')
        time_str = qso.get('TIME_ON', '')
        
        if date_str and len(date_str) >= 8:
            try:
                date = datetime.strptime(date_str[:8], '%Y%m%d')
                day = date.weekday()  # 0=Lunes, 6=Domingo
                
                if time_str and len(time_str) >= 2:
                    hour = int(time_str[:2])
                    day_hour[day][hour] += 1
            except ValueError:
                continue
    
    # Crear matriz 7x24
    matrix = np.zeros((7, 24))
    for day in range(7):
        for hour in range(24):
            matrix[day][hour] = day_hour[day][hour]
    
    fig, ax = plt.subplots(figsize=(16, 6))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(range(24))
    ax.set_xticklabels([f'{h:02d}' for h in range(24)])
    ax.set_yticks(range(7))
    ax.set_yticklabels(dias_semana)
    ax.set_xlabel('Hora (UTC)', fontsize=12)
    ax.set_ylabel('Día de la semana', fontsize=12)
    ax.set_title('Heatmap: Actividad por Día y Hora', fontsize=14, fontweight='bold')
    
    plt.colorbar(im, ax=ax, label='Número de QSOs')
    
    plt.tight_layout()
    plt.savefig('grafico_heatmap_dia_hora.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_distance_histogram(qsos):
    """
    Genera histograma de distancias de los contactos.
    
    Muestra distribución lineal y logarítmica para ver tanto
    contactos locales como DX.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        list: Lista de distancias en km (o None si no hay datos)
    """
    distances = []
    for qso in qsos:
        dist = qso.get('DISTANCE', '')
        if dist:
            try:
                distances.append(int(dist))
            except ValueError:
                continue
    
    if not distances:
        print("  (no hay datos de distancia)")
        return None
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Histograma lineal
    ax1.hist(distances, bins=30, color='steelblue', edgecolor='navy', alpha=0.7)
    ax1.set_xlabel('Distancia (km)', fontsize=12)
    ax1.set_ylabel('Número de QSOs', fontsize=12)
    ax1.set_title('Distribución de Distancias', fontsize=14, fontweight='bold')
    ax1.axvline(np.mean(distances), color='red', linestyle='--', 
                label=f'Media: {np.mean(distances):.0f} km')
    ax1.legend()
    
    # Histograma logarítmico (muestra mejor DX)
    log_bins = np.logspace(
        np.log10(max(1, min(distances))), 
        np.log10(max(distances) + 1), 
        20
    )
    ax2.hist(distances, bins=log_bins, color='coral', edgecolor='darkred', alpha=0.7)
    ax2.set_xlabel('Distancia (km) - Escala logarítmica', fontsize=12)
    ax2.set_ylabel('Número de QSOs', fontsize=12)
    ax2.set_title('Distribución de Distancias (Escala Log)', fontsize=14, fontweight='bold')
    ax2.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig('grafico_distancias.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return distances


def create_zones_chart(qsos):
    """
    Genera gráfico de Zonas CQ e ITU contactadas.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        tuple: (cq_zones, itu_zones)
    """
    cq_zones, itu_zones = analyze_zones(qsos)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    if cq_zones:
        zones = list(cq_zones.keys())
        counts = list(cq_zones.values())
        ax1.bar(zones, counts, color='teal', edgecolor='darkcyan', alpha=0.7)
        ax1.set_xlabel('Zona CQ', fontsize=12)
        ax1.set_ylabel('Número de QSOs', fontsize=12)
        ax1.set_title('Distribución por Zonas CQ', fontsize=14, fontweight='bold')
    
    if itu_zones:
        zones = list(itu_zones.keys())
        counts = list(itu_zones.values())
        ax2.bar(zones, counts, color='darkorange', edgecolor='orangered', alpha=0.7)
        ax2.set_xlabel('Zona ITU', fontsize=12)
        ax2.set_ylabel('Número de QSOs', fontsize=12)
        ax2.set_title('Distribución por Zonas ITU', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('grafico_zonas.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return cq_zones, itu_zones


def create_timeline(qsos):
    """
    Genera timeline de QSOs acumulados y QSOs por día.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        tuple: (unique_dates, cumulative) o (None, None)
    """
    dates = []
    for qso in qsos:
        date_str = qso.get('QSO_DATE', '')
        if date_str and len(date_str) >= 8:
            try:
                date = datetime.strptime(date_str[:8], '%Y%m%d')
                dates.append(date)
            except ValueError:
                continue
    
    if not dates:
        print("  (no hay datos de fecha)")
        return None, None
    
    dates.sort()
    date_counts = Counter(dates)
    
    # Crear lista ordenada de fechas únicas
    unique_dates = list(OrderedDict.fromkeys(dates))
    
    # Calcular acumulados
    cumulative = []
    total = 0
    for d in unique_dates:
        total += date_counts[d]
        cumulative.append(total)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Línea de QSOs acumulados
    ax1.plot(unique_dates, cumulative, marker='o', linewidth=2, color='darkgreen')
    ax1.fill_between(unique_dates, cumulative, alpha=0.3, color='green')
    ax1.set_xlabel('Fecha', fontsize=12)
    ax1.set_ylabel('QSOs Acumulados', fontsize=12)
    ax1.set_title('Progreso de QSOs en el Tiempo', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Barras de QSOs por día
    daily_counts = [date_counts[d] for d in unique_dates]
    ax2.bar(unique_dates, daily_counts, color='coral', edgecolor='darkred', alpha=0.7)
    ax2.set_xlabel('Fecha', fontsize=12)
    ax2.set_ylabel('QSOs por día', fontsize=12)
    ax2.set_title('QSOs por Día', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('grafico_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return unique_dates, cumulative


def create_frequency_histogram(qsos):
    """
    Genera histograma de frecuencias usadas.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
    """
    frequencies = []
    for qso in qsos:
        freq = qso.get('FREQ', '')
        if freq:
            try:
                frequencies.append(float(freq))
            except ValueError:
                continue
    
    if not frequencies:
        print("  (no hay datos de frecuencia)")
        return
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.hist(frequencies, bins=50, color='purple', edgecolor='darkviolet', alpha=0.7)
    ax.set_xlabel('Frecuencia (MHz)', fontsize=12)
    ax.set_ylabel('Número de QSOs', fontsize=12)
    ax.set_title('Distribución de Frecuencias Usadas', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('grafico_frecuencias.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_power_distance_scatter(qsos):
    """
    Genera scatter plot de potencia vs distancia.
    
    Útil para analizar qué potencia se necesita para diferentes distancias.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
    """
    data = []
    for qso in qsos:
        dist = qso.get('DISTANCE', '')
        pwr = qso.get('TX_PWR', qso.get('POWER', ''))
        
        if dist and pwr:
            try:
                data.append((float(pwr), int(dist)))
            except ValueError:
                continue
    
    if not data:
        print("  (no hay datos de potencia/distancia)")
        return
    
    powers = [d[0] for d in data]
    distances = [d[1] for d in data]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Scatter simple
    ax1.scatter(powers, distances, alpha=0.5, c='steelblue', edgecolors='navy')
    ax1.set_xlabel('Potencia (W)', fontsize=12)
    ax1.set_ylabel('Distancia (km)', fontsize=12)
    ax1.set_title('Potencia vs Distancia', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Hexbin (densidad)
    ax2.hexbin(powers, distances, gridsize=20, cmap='YlOrRd')
    ax2.set_xlabel('Potencia (W)', fontsize=12)
    ax2.set_ylabel('Distancia (km)', fontsize=12)
    ax2.set_title('Densidad: Potencia vs Distancia', fontsize=14, fontweight='bold')
    plt.colorbar(ax2.collections[0], ax=ax2, label='Conteo')
    
    plt.tight_layout()
    plt.savefig('grafico_potencia_distancia.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_band_mode_heatmap(qsos):
    """
    Genera heatmap interactivo de banda vs modo.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
    """
    matrix, bands, modes = analyze_band_mode_matrix(qsos)
    
    if matrix.size == 0:
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(matrix, cmap='Blues', aspect='auto')
    
    ax.set_xticks(range(len(modes)))
    ax.set_xticklabels(modes, rotation=45, ha='right')
    ax.set_yticks(range(len(bands)))
    ax.set_yticklabels(bands)
    
    # Añadir valores en celdas
    for i in range(len(bands)):
        for j in range(len(modes)):
            if matrix[i][j] > 0:
                color = 'white' if matrix[i][j] > matrix.max()/2 else 'black'
                ax.text(j, i, int(matrix[i][j]), ha='center', va='center', color=color)
    
    ax.set_xlabel('Modo', fontsize=12)
    ax.set_ylabel('Banda', fontsize=12)
    ax.set_title('Heatmap: Banda vs Modo', fontsize=14, fontweight='bold')
    plt.colorbar(im, ax=ax, label='Número de QSOs')
    
    plt.tight_layout()
    plt.savefig('grafico_banda_modo.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_dxcc_analysis(qsos):
    """
    Genera análisis DXCC (entities para buscar en hamqth)
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        dict: Diccionario de entidades DXCC ordenadas
    """
    dxcc_countries = Counter()
    
    for qso in qsos:
        country = qso.get('COUNTRY', 'Unknown')
        if country and country != 'Unknown':
            dxcc_countries[country] += 1
    
    if not dxcc_countries:
        return None
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    countries = list(dxcc_countries.keys())[:20]
    counts = [dxcc_countries[c] for c in countries]
    
    bars = ax.barh(countries, counts, color='indianred', edgecolor='darkred', alpha=0.7)
    ax.set_xlabel('Número de QSOs', fontsize=12)
    ax.set_ylabel('País (DXCC)', fontsize=12)
    ax.set_title('Top 20 Entidades DXCC', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
               str(count), va='center')
    
    plt.tight_layout()
    plt.savefig('grafico_dxcc.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return dict(dxcc_countries.most_common())


def create_summary_dashboard(qsos):
    """
    Genera dashboard resumen con 6 subplots.
    
    Incluye: países, modos, bandas, estaciones, actividad horaria y distancias.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
    """
    fig = plt.figure(figsize=(20, 12))
    
    ax1 = fig.add_subplot(2, 3, 1)
    ax2 = fig.add_subplot(2, 3, 2)
    ax3 = fig.add_subplot(2, 3, 3)
    ax4 = fig.add_subplot(2, 3, 4)
    ax5 = fig.add_subplot(2, 3, 5)
    ax6 = fig.add_subplot(2, 3, 6)
    
    # Recoger datos
    countries = analyze_countries(qsos)
    modes = analyze_mode_band(qsos)['por_modo']
    bands = analyze_mode_band(qsos)['por_banda']
    stations = analyze_stations(qsos)
    time_dist = analyze_time_distribution(qsos)
    
    # Subplot 1: Top 5 países
    top_countries = dict(list(countries.items())[:5])
    ax1.bar(top_countries.keys(), top_countries.values(), color='skyblue')
    ax1.set_title('Top 5 Países', fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    
    # Subplot 2: Modos (pastel)
    ax2.pie(list(modes.values()), labels=list(modes.keys()), autopct='%1.1f%%')
    ax2.set_title('Modos', fontweight='bold')
    
    # Subplot 3: Bandas (pastel, top 6)
    ax3.pie(list(bands.values())[:6], labels=list(bands.keys())[:6], autopct='%1.1f%%')
    ax3.set_title('Bandas', fontweight='bold')
    
    # Subplot 4: Top 5 estaciones
    top_stations = dict(list(stations.items())[:5])
    ax4.barh(list(top_stations.keys()), list(top_stations.values()), color='gold')
    ax4.set_title('Top 5 Estaciones', fontweight='bold')
    ax4.invert_yaxis()
    
    # Subplot 5: Actividad horaria
    hours = list(range(24))
    counts = [time_dist.get(h, 0) for h in hours]
    ax5.fill_between(hours, counts, alpha=0.5, color='mediumpurple')
    ax5.plot(hours, counts, marker='o', color='darkviolet')
    ax5.set_title('Actividad Horaria', fontweight='bold')
    ax5.set_xlabel('Hora UTC')
    
    # Subplot 6: Distancias
    distances = []
    for qso in qsos:
        dist = qso.get('DISTANCE', '')
        if dist:
            try:
                distances.append(int(dist))
            except ValueError:
                continue
    
    if distances:
        ax6.hist(distances, bins=20, color='steelblue', edgecolor='navy', alpha=0.7)
        ax6.set_title('Distancias', fontweight='bold')
        ax6.set_xlabel('km')
    
    fig.suptitle(f'Dashboard Resumen - Total: {len(qsos)} QSOs', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('grafico_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()


# ==============================================================================
# SECCIÓN 4: GRÁFICOS - ESPECIALES (QRZ y FONÍA)
# ==============================================================================

def create_qrz_lookups_chart():
    """
    Genera gráfico de lookups en QRZ.com de las estaciones más contactadas.
    
    Los datos de lookups se obtienen manualmente de qrz.com/db/indicativo
    y representan la popularidad de cada estación en la base de datos QRZ.
    
    Muestra correlación entre contactos en el log y lookups en QRZ.
    """
    # Datos obtenidos de qrz.com (consulta manual)
    # Formato: {indicativo: {'lookups': número, 'contactos': número}}
    lookups_data = {
        'EA8CWA': {'lookups': 83483, 'contactos': 9},   # Canarias - muy activo
        'EA8AE':  {'lookups': 71971, 'contactos': 6},   # Canarias
        'EA5NA':  {'lookups': 69523, 'contactos': 10}, # Alicante
        'EA5FHC': {'lookups': 48780, 'contactos': 7},   # Valencia
        'EA4HNO': {'lookups': 19404, 'contactos': 12}, # Madrid
        'EA4RCD': {'lookups': 13998, 'contactos': 11}, # Burgos
        'EA3IWT': {'lookups': 4936, 'contactos': 6},   # Barcelona
        'EA7LLM': {'lookups': 665, 'contactos': 6},    # Sevilla
        'EB4CJL': {'lookups': 297, 'contactos': 6},     # Madrid
    }
    
    # Ordenar por lookups descendente
    sorted_data = sorted(lookups_data.items(), key=lambda x: x[1]['lookups'], reverse=True)
    calls = [x[0] for x in sorted_data]
    lookups = [x[1]['lookups'] for x in sorted_data]
    contactos = [x[1]['contactos'] for x in sorted_data]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Colores según cantidad de lookups
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(calls)))[::-1]
    
    # Gráfico de barras horizontales
    bars = ax1.barh(calls, lookups, color=colors, edgecolor='black', alpha=0.8)
    ax1.set_xlabel('Número de Lookups en QRZ.com', fontsize=12)
    ax1.set_ylabel('Indicativo', fontsize=12)
    ax1.set_title('Top Estaciones por Lookups en QRZ', fontsize=14, fontweight='bold')
    ax1.invert_yaxis()
    
    for bar, lookup in zip(bars, lookups):
        ax1.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2, 
                f'{lookup:,}', va='center', fontsize=9)
    
    # Scatter: contactos vs lookups
    scatter = ax2.scatter(contactos, lookups, s=200, c=lookups, cmap='RdYlGn', 
                edgecolors='black', linewidth=1, alpha=0.8)
    for i, call in enumerate(calls):
        ax2.annotate(call, (contactos[i], lookups[i]), 
                    textcoords="offset points", xytext=(5, 5), fontsize=9)
    
    ax2.set_xlabel('Número de Contactos en tu Log', fontsize=12)
    ax2.set_ylabel('Lookups en QRZ.com', fontsize=12)
    ax2.set_title('Contactos vs Lookups QRZ', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('grafico_qrz_lookups.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_fonia_por_hora_chart(qsos):
    """
    Genera gráfico de contactos en fonía (SSB/FM) por hora UTC.
    
    La fonía (comunicación de voz) es diferente de los modos digitales
    como FT8. Este gráfico muestra cuándo se opera en voz.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs
        
    Returns:
        dict: Estadísticas de fonía {
            'total': número total de QSOs fonía,
            'hora_pico': hora con más actividad,
            'qsos_hora_pico': QSOs en hora pico,
            'distribucion': {hora: cantidad}
        }
    """
    fonia_por_hora = defaultdict(int)
    
    for qso in qsos:
        mode = qso.get('MODE', '').upper()
        # Incluir SSB, PHONE y FM (fonía)
        if mode == 'SSB' or 'PHONE' in mode or mode == 'FM':
            time_str = qso.get('TIME_ON', '')
            if time_str and len(time_str) >= 2:
                try:
                    hour = int(time_str[:2])
                    fonia_por_hora[hour] += 1
                except ValueError:
                    continue
    
    hours = list(range(24))
    fonia_counts = [fonia_por_hora.get(h, 0) for h in hours]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
    
    # Gráfico de barras con valores
    bars = ax1.bar(hours, fonia_counts, color='coral', edgecolor='darkred', alpha=0.8)
    ax1.set_xlabel('Hora (UTC)', fontsize=12)
    ax1.set_ylabel('Número de QSOs en Fonía', fontsize=12)
    ax1.set_title('Contactos en Fonía (SSB/FM) por Hora UTC', fontsize=14, fontweight='bold')
    ax1.set_xticks(hours)
    ax1.set_xticklabels([f'{h:02d}:00' for h in hours], rotation=45)
    
    for bar, count in zip(bars, fonia_counts):
        if count > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                    f'{count}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Gráfico de línea con marcadores
    ax2.plot(hours, fonia_counts, marker='o', linewidth=2.5, markersize=10, 
             color='darkred', markerfacecolor='coral', markeredgecolor='darkred')
    ax2.fill_between(hours, fonia_counts, alpha=0.3, color='coral')
    
    # Anotaciones en picos
    for h, count in zip(hours, fonia_counts):
        if count > 0:
            ax2.annotate(f'{count}', (h, count), textcoords="offset points", 
                        xytext=(0, 8), ha='center', fontsize=9, fontweight='bold')
    
    ax2.set_xlabel('Hora (UTC)', fontsize=12)
    ax2.set_ylabel('Número de QSOs en Fonía', fontsize=12)
    ax2.set_title('Distribución Horaria de Contactos en Fonía', fontsize=14, fontweight='bold')
    ax2.set_xticks(hours)
    ax2.set_xticklabels([f'{h:02d}:00' for h in hours], rotation=45)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, max(fonia_counts) * 1.15)
    
    plt.tight_layout()
    plt.savefig('grafico_fonia_por_hora.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Calcular estadísticas
    total_fonia = sum(fonia_counts)
    hora_pico = max(fonia_counts) if fonia_counts else 0
    hora_pico_idx = fonia_counts.index(hora_pico) if hora_pico > 0 else 0
    
    return {
        'total': total_fonia,
        'hora_pico': hora_pico_idx,
        'qsos_hora_pico': hora_pico,
        'distribucion': dict(fonia_por_hora)
    }


# ==============================================================================
# SECCIÓN 5: REPORTE PRINCIPAL
# ==============================================================================

def generate_statistics_report(qsos):
    """
    Genera reporte completo de estadísticas y todos los gráficos.
    
    Esta es la función principal que orquesta la generación de todos
    los análisis y gráficos del programa.
    
    Args:
        qsos (list): Lista de diccionarios de QSOs parseados
        
    Returns:
        dict: Diccionario con todas las estadísticas para guardar en JSON
    """
    print("=" * 80)
    print("ANÁLISIS ESTADÍSTICO DE ARCHIVO ADI")
    print("=" * 80)
    print(f"Total de QSOs analizados: {len(qsos)}")
    print()
    
    # Ejecutar todos los análisis
    countries = analyze_countries(qsos)
    locators = analyze_locators(qsos)
    mode_band_data = analyze_mode_band(qsos)
    stations = analyze_stations(qsos)
    time_dist = analyze_time_distribution(qsos)
    
    # --- GRÁFICOS BÁSICOS ---
    print("Generando gráficos básicos...")
    
    create_countries_chart(countries, len(qsos))
    print("  ✓ grafico_paises.png")
    
    create_locators_chart(locators)
    print("  ✓ grafico_localizadores.png")
    
    create_mode_band_chart(mode_band_data)
    print("  ✓ grafico_modos_bandas.png")
    
    create_stations_chart(stations)
    print("  ✓ grafico_estaciones_top.png")
    
    create_time_distribution_chart(time_dist)
    print("  ✓ grafico_distribucion_horaria.png")
    
    # --- GRÁFICOS AVANZADOS ---
    print("\nGenerando gráficos avanzados...")
    
    create_world_map(qsos)
    print("  ✓ grafico_mapa_mundial.png")
    
    create_heatmap_day_hour(qsos)
    print("  ✓ grafico_heatmap_dia_hora.png")
    
    distances = create_distance_histogram(qsos)
    if distances:
        print(f"  ✓ grafico_distancias.png (media: {np.mean(distances):.0f} km)")
    else:
        print("  ✓ grafico_distancias.png (sin datos de distancia)")
    
    cq_zones, itu_zones = create_zones_chart(qsos)
    if cq_zones:
        print(f"  ✓ grafico_zonas.png ({len(cq_zones)} zonas CQ, {len(itu_zones)} zonas ITU)")
    
    timeline_data = create_timeline(qsos)
    if timeline_data:
        print("  ✓ grafico_timeline.png")
    
    create_frequency_histogram(qsos)
    print("  ✓ grafico_frecuencias.png")
    
    create_power_distance_scatter(qsos)
    print("  ✓ grafico_potencia_distancia.png")
    
    create_band_mode_heatmap(qsos)
    print("  ✓ grafico_banda_modo.png")
    
    dxcc = create_dxcc_analysis(qsos)
    if dxcc:
        print(f"  ✓ grafico_dxcc.png ({len(dxcc)} entidades DXCC)")
    
    create_summary_dashboard(qsos)
    print("  ✓ grafico_dashboard.png")
    
    # --- GRÁFICOS ESPECIALES ---
    print("\nGenerando gráficos especiales...")
    
    create_qrz_lookups_chart()
    print("  ✓ grafico_qrz_lookups.png")
    
    fonia_data = create_fonia_por_hora_chart(qsos)
    print(f"  ✓ grafico_fonia_por_hora.png ({fonia_data['total']} QSOs fonía, pico: {fonia_data['hora_pico']:02d}:00 UTC)")
    
    print()
    
    # --- RESUMEN ESTADÍSTICO ---
    print("RESUMEN ESTADÍSTICO:")
    print("-" * 40)
    print(f"Países contactados: {len(countries)}")
    print(f"Localizadores únicos: {len(locators)}")
    print(f"Estaciones únicas: {len(stations)}")
    print(f"Modos utilizados: {list(mode_band_data['por_modo'].keys())}")
    print(f"Bandas utilizadas: {list(mode_band_data['por_banda'].keys())}")
    
    if distances:
        print(f"Distancia media: {np.mean(distances):.0f} km")
        print(f"Distancia máxima: {max(distances):,} km")
    
    if cq_zones:
        print(f"Zonas CQ únicas: {len(cq_zones)}")
    if itu_zones:
        print(f"Zonas ITU únicas: {len(itu_zones)}")
    
    print(f"\nTop 5 países: {list(countries.keys())[:5]}")
    print(f"Top 5 localizadores: {list(locators.keys())[:5]}")
    print(f"Top 5 estaciones: {list(stations.keys())[:5]}")
    
    # Devolver todas las estadísticas para JSON
    return {
        'total_qsos': len(qsos),
        'paises': countries,
        'localizadores': locators,
        'modos_bandas': mode_band_data,
        'estaciones': stations,
        'distribucion_horaria': time_dist,
        'distancias': {
            'media': float(np.mean(distances)) if distances else 0,
            'max': max(distances) if distances else 0
        },
        'zonas_cq': cq_zones,
        'zonas_itu': itu_zones,
        'dxcc': dxcc if dxcc else {},
        'fonia': fonia_data
    }


# ==============================================================================
# SECCIÓN 6: PUNTO DE ENTRADA
# ==============================================================================

def main():
    """
    Función principal del programa.
    
    1. Verifica que exista el archivo ADI
    2. Parsea el archivo
    3. Genera estadísticas y gráficos
    4. Guarda resultados en JSON
    """
    filename = 'aaa.adi'
    
    # Verificar archivo
    if not os.path.exists(filename):
        print(f"Error: No se encuentra el archivo {filename}")
        print("Coloca tu archivo .adi en el directorio actual y renómbralo a 'aaa.adi'")
        return
    
    print("Procesando archivo ADI...")
    qsos = parse_adi_file(filename)
    
    if not qsos:
        print("No se encontraron QSOs en el archivo.")
        return
    
    # Generar todo el reporte
    stats = generate_statistics_report(qsos)
    
    # Guardar estadísticas en JSON
    with open('estadisticas_adi.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print("✓ Estadísticas guardadas en 'estadisticas_adi.json'")
    
    # Listado final de archivos
    print("\n" + "=" * 80)
    print("ANÁLISIS COMPLETADO")
    print("=" * 80)
    print("\nArchivos generados:")
    print("\n  ESTADÍSTICAS:")
    print("    - estadisticas_adi.json")
    print("\n  GRÁFICOS BÁSICOS:")
    print("    - grafico_paises.png")
    print("    - grafico_localizadores.png")
    print("    - grafico_modos_bandas.png")
    print("    - grafico_estaciones_top.png")
    print("    - grafico_distribucion_horaria.png")
    print("\n  GRÁFICOS AVANZADOS:")
    print("    - grafico_mapa_mundial.png")
    print("    - grafico_heatmap_dia_hora.png")
    print("    - grafico_distancias.png")
    print("    - grafico_zonas.png")
    print("    - grafico_timeline.png")
    print("    - grafico_frecuencias.png")
    print("    - grafico_potencia_distancia.png")
    print("    - grafico_banda_modo.png")
    print("    - grafico_dxcc.png")
    print("    - grafico_dashboard.png")
    print("\n  GRÁFICOS ESPECIALES:")
    print("    - grafico_qrz_lookups.png")
    print("    - grafico_fonia_por_hora.png")
    print("=" * 80)


if __name__ == "__main__":
    main()
