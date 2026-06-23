# 📻 Analizador de Logs ADIF para Radioaficionados

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![ADIF](https://img.shields.io/badge/Format-ADIF%203.1.4-orange.svg)

Scripts en Python para analizar archivos de log de radioaficionados en formato ADIF y generar gráficos estadísticos completos.

## 📋 Descripción

Este proyecto contiene dos scripts que generan **más de 30 gráficos estadísticos** a partir de archivos ADIF:

| Script | Descripción | Gráficos |
|--------|-------------|-----------|
| `analizar_adi_grafico.py` | Análisis general del log completo | 22 gráficos |
| `analizar_por_operador.py` | Análisis detallado por operador | 14 gráficos |

### 🌍 Asignación Automática de Países

Muchos archivos ADIF no incluyen el campo `COUNTRY` en los QSOs. Los scripts resuelven automáticamente el país de cada estación a partir del **prefijo ITU del indicativo** (call sign):

- `EA`/`EB`/`EC`... → Spain
- `F` → France
- `DL`/`DK`/`DO`... → Germany
- `G`/`M`/`2E`... → England
- `I`/`IK`/`IZ`... → Italy
- `CT`/`CS`... → Portugal
- Y más de **400 prefijos** de todos los países

Esto garantiza que **todos los QSOs tengan país asignado** incluso cuando el archivo ADIF no incluye el campo `COUNTRY`.

## 🚀 Uso Rápido

```bash
# ============================================
# 1. CONFIGURAR ENTORNO (solo la primera vez)
# ============================================
./setup_and_run.sh

# O manualmente:
python3 -m venv venv_adi
source venv_adi/bin/activate
pip install -r requirements.txt

# ============================================
# 2. EJECUTAR ANÁLISIS GENERAL (17 gráficos)
# ============================================
./run_analysis.sh

# O directamente:
python analizar_adi_grafico.py

# ============================================
# 3. EJECUTAR ANÁLISIS POR OPERADOR (14 gráficos)
# ============================================
source venv_adi/bin/activate
python analizar_por_operador.py
```

## 📁 Estructura del Proyecto

```
├── aaa.adi                          # Archivo ADIF de ejemplo (524 QSOs)
├── analizar_adi_grafico.py           # Script 1: Análisis general
├── analizar_por_operador.py          # Script 2: Análisis por operador
├── requirements.txt                  # Dependencias Python
├── setup_and_run.sh                 # Script: Setup + ejecutar análisis general
├── run_analysis.sh                  # Script: Ejecutar análisis general
├── estadisticas_adi.json            # Estadísticas en JSON
│
├── GRÁFICOS ANÁLISIS GENERAL (22):
│   ├── grafico_paises.png           # Top 15 países (barras + pastel)
│   ├── grafico_localizadores.png    # Top 20 localizadores Maidenhead
│   ├── grafico_modos_bandas.png     # Modos y bandas (4 subplots)
│   ├── grafico_estaciones_top.png   # Top 20 estaciones
│   ├── grafico_distribucion_horaria.png  # Actividad por hora
│   ├── grafico_mapa_mundial.png     # Dispersión mundial
│   ├── grafico_heatmap_dia_hora.png # Heatmap día/hora
│   ├── grafico_distancias.png       # Histograma de distancias
│   ├── grafico_zonas.png            # Zonas CQ e ITU
│   ├── grafico_timeline.png         # QSOs acumulados
│   ├── grafico_frecuencias.png      # Histograma frecuencias
│   ├── grafico_potencia_distancia.png  # Scatter potencia/distancia
│   ├── grafico_banda_modo.png       # Heatmap banda vs modo
│   ├── grafico_dxcc.png             # Top 20 DXCC
│   ├── grafico_dashboard.png        # Dashboard resumen (6 subplots)
│   ├── grafico_distancia_locator.png # Distancia por banda/modo
│   ├── grafico_qrz_lookups.png      # Lookups en QRZ.com
│   ├── grafico_fonia_por_hora.png   # Fonía por hora UTC
│   ├── grafico_banda_hora.png       # Heatmap banda vs hora
│   ├── grafico_estaciones_unicas.png # Únicas vs repetidas
│   ├── grafico_mapa_operadores.png  # Mapa por operador
│   └── grafico_sankey.html          # Diagrama Sankey interactivo
│
└── GRÁFICOS ANÁLISIS POR OPERADOR (14):
    ├── operador_resumen.png             # Comparativa total QSOs
    ├── operador_bandas.png             # Bandas por operador (heatmap)
    ├── operador_modos.png              # Modos por operador (heatmap)
    ├── operador_horas.png              # Actividad horaria por operador
    ├── operador_comparacion_bandas.png # Barras agrupadas bandas
    ├── operador_comparacion_modos.png  # Barras agrupadas modos
    ├── operador_EB4GSN.png             # Detalle individual EB4GSN
    ├── operador_EA4INH.png             # Detalle individual EA4INH
    ├── operador_EA4IFI.png             # Detalle individual EA4IFI
    ├── operador_EA7LHS.png             # Detalle individual EA7LHS
    ├── operador_EA3JAQ.png             # Detalle individual EA3JAQ
    ├── operador_EB1CU.png              # Detalle individual EB1CU
    ├── operador_EA4HUK.png             # Detalle individual EA4HUK
    └── operador_EA3JCP.png             # Detalle individual EA3JCP
```

---

## 📈 Script 1: Análisis General (17 gráficos)

### Gráficos Básicos

#### 1. Distribución por Países
![Gráfico de Países](grafico_paises.png)

Top 15 países contactados con barras y distribución porcentual.

#### 2. Localizadores Maidenhead
![Gráfico de Localizadores](grafico_localizadores.png)

Top 20 cuadrículas Maidenhead más contactadas.

#### 3. Modos y Bandas
![Gráfico de Modos y Bandas](grafico_modos_bandas.png)

Análisis de modos (SSB, FT8, FM, DIGITALVOICE, MFSK) y bandas (40M, 20M, 70cm).

#### 4. Top Estaciones
![Gráfico de Estaciones](grafico_estaciones_top.png)

Estaciones más contactadas por número de QSOs.

#### 5. Distribución Horaria General
![Gráfico Horario](grafico_distribucion_horaria.png)

Patrón de actividad por hora UTC para todos los modos.

---

### Gráficos Avanzados

#### 6. Mapa Mundial de Localizadores
![Mapa Mundial](grafico_mapa_mundial.png)

Dispersión geográfica de localizadores Maidenhead.

#### 7. Heatmap Día/Hora
![Heatmap](grafico_heatmap_dia_hora.png)

Actividad semanal: días y horas de mayor operación.

#### 8. Distribución de Distancias
![Distancias](grafico_distancias.png)

Histograma lineal y logarítmico de distancias en km.

| Métrica | Valor |
|---------|-------|
| Distancia media | 1,524 km |
| Distancia máxima | 10,524 km |

#### 9. Distancias por Localizador (Banda, Modo y Potencia)
![Distancias por Localizador](grafico_distancia_locator.png)

Análisis de distancias calculadas entre emisor y receptor:
- **Gráfico 1:** Distancia promedio por banda con desviación estándar
- **Gráfico 2:** Distancia promedio por modo de operación
- **Gráfico 3:** Scatter plot mostrando distancia por banda (color=modo, tamaño=potencia)
- **Gráfico 4:** Box plot de distribución de distancias por banda

Calcula la distancia usando los localizadores Maidenhead del operador (MY_GRIDSQUARE) y del contacto (GRIDSQUARE).

#### 10. Zonas CQ e ITU
![Zonas](grafico_zonas.png)

Distribución de contactos por zonas geográficas internacionales.

#### 11. Timeline de QSOs
![Timeline](grafico_timeline.png)

Progreso acumulado de contactos y QSOs por día.

#### 12. Frecuencias Usadas
![Frecuencias](grafico_frecuencias.png)

Histograma de frecuencias exactas en MHz.

#### 13. Potencia vs Distancia
![Potencia Distancia](grafico_potencia_distancia.png)

Scatter plot y mapa de densidad potencia/distancia.

#### 14. Heatmap Banda vs Modo
![Banda Modo](grafico_banda_modo.png)

Matriz banda-modo con valores en cada celda.

#### 15. Entidades DXCC
![DXCC](grafico_dxcc.png)

Top 20 entidades DXCC (países reconocidos por ARRL).

#### 16. Dashboard Resumen
![Dashboard](grafico_dashboard.png)

Vista consolidada con 6 subplots: países, modos, bandas, estaciones, horario y distancias.

---

### Gráficos Especiales

#### 17. QRZ.com Lookups
![QRZ Lookups](grafico_qrz_lookups.png)

Correlación entre contactos y número de lookups en QRZ.com.

| Indicativo | Lookups | Contactos |
|------------|---------|-----------|
| EA8CWA | 83,483 | 9 |
| EA8AE | 71,971 | 6 |
| EA5NA | 69,523 | 10 |
| EA5FHC | 48,780 | 7 |
| EA4HNO | 19,404 | 12 |

#### 18. Fonía por Hora
![Fonía](grafico_fonia_por_hora.png)

Análisis específico de contactos en fonía (SSB/FM) por hora UTC.

| Métrica | Valor |
|---------|-------|
| Total QSOs fonía | 277 |
| Hora pico | 10:00 UTC |
| QSOs en hora pico | 44 |

---

## 👥 Script 2: Análisis por Operador (14 gráficos)

Agrupa los contactos por el campo `OPERATOR` y genera estadísticas individuales y comparativas.

### Operadores Encontrados

| Operador | Total QSOs | Banda Favorita | Modo Favorito | Hora Pico |
|----------|-----------|----------------|---------------|-----------|
| **EB4GSN** | 229 | 20M (187) | FT8 (131) | 08:00 UTC |
| **EA4IFI** | 90 | 40M (90) | SSB (90) | 10:00 UTC |
| **EB1CU** | 54 | 15M (23) | FT8 (54) | 21:00 UTC |
| **EA3JAQ** | 45 | 40M (35) | SSB (45) | 07:00 UTC |
| **EA4HUK** | 36 | 20M (36) | SSB (36) | 11:00 UTC |
| **EA7LHS** | 27 | 20M (11) | FT8 (17) | 22:00 UTC |
| **EA3JCP** | 23 | 2M (23) | FM (23) | 09:00 UTC |
| **EA4INH** | 20 | 40M (20) | SSB (20) | 11:00 UTC |

### Gráficos Comparativos

#### Resumen por Operador
![Resumen](operador_resumen.png)

Total de QSOs y distribución porcentual por operador.

#### Bandas por Operador
![Bandas](operador_bandas.png)

Heatmap y barras mostrando qué bandas usa cada operador.

#### Modos por Operador
![Modos](operador_modos.png)

Análisis de modos por operador con heatmap.

#### Actividad Horaria por Operador
![Horas](operador_horas.png)

Heatmap y líneas de tendencia horaria.

#### Comparación de Bandas
![Comparación Bandas](operador_comparacion_bandas.png)

Barras agrupadas comparando bandas entre operadores.

#### Comparación de Modos
![Comparación Modos](operador_comparacion_modos.png)

Barras agrupadas comparando modos entre operadores.

### Gráficos Individuales (4 subplots cada uno)

Cada operador tiene su propio gráfico con: Bandas, Modos (pastel), Actividad horaria, Días de la semana.

| EB4GSN | EA4IFI | EB1CU |
|--------|--------|--------|
| ![EB4GSN](operador_EB4GSN.png) | ![EA4IFI](operador_EA4IFI.png) | ![EB1CU](operador_EB1CU.png) |

| EA3JAQ | EA4HUK | EA7LHS |
|--------|--------|--------|
| ![EA3JAQ](operador_EA3JAQ.png) | ![EA4HUK](operador_EA4HUK.png) | ![EA7LHS](operador_EA7LHS.png) |

| EA3JCP | EA4INH |
|--------|--------|
| ![EA3JCP](operador_EA3JCP.png) | ![EA4INH](operador_EA4INH.png) |

---

## 📊 Estadísticas del Log de Ejemplo

```
Total QSOs analizados:       524
Operadores únicos:             8
Países contactados:           45
Localizadores únicos:        135
Estaciones únicas:           435
Zonas CQ únicas:              4
Zonas ITU únicas:             5
Distancia media:        1,524 km
Distancia máxima:      10,524 km

Modos utilizados:
  - SSB (Fonía): 250 QSOs
  - FT8 (Digital): 202 QSOs
  - MFSK (FT4): 45 QSOs
  - FM: 27 QSOs

Bandas utilizadas:
  - 40M, 20M, 15M, 10M (HF)
  - 2M (VHF)
```

---

## 🌍 Corrección de Países Faltantes

Si tu archivo ADIF no incluye el campo `COUNTRY`, los scripts lo asignan automáticamente analizando el prefijo ITU del indicativo (campo `CALL`). La función `get_country_from_callsign()` en ambos scripts reconoce **más de 400 prefijos** de todo el mundo.

Si algún QSO queda sin país ("Desconocido"), puedes extender el diccionario `PREFIX_COUNTRY_MAP` añadiendo el prefijo que falte:

```python
PREFIX_COUNTRY_MAP["XX"] = "Mi País"
```

---

### Cambiar archivo de entrada

Edita la variable `filename` en ambos scripts:

```python
def main():
    filename = 'tu_archivo.adi'  # Cambiar aquí
```

### Agregar más datos de QRZ Lookups

Edita `create_qrz_lookups_chart()` en `analizar_adi_grafico.py`:

```python
lookups_data = {
    'TUIndicATIVO': {'lookups': 12345, 'contactos': 5},  # Añadir aquí
}
```

### Añadir nuevos gráficos

Agregar función `create_nuevo_grafico()` y llamarla desde `generate_statistics_report()`.

---

## 📦 Dependencias

```
matplotlib>=3.5.0
seaborn>=0.11.0
pandas>=1.3.0
numpy>=1.21.0
```

Instalación: `pip install -r requirements.txt`

---

## 📖 Campos ADIF Soportados

| Campo | Descripción |
|-------|-------------|
| CALL | Indicativo de la estación |
| COUNTRY | País |
| OPERATOR | Operador que realizó el contacto |
| FREQ | Frecuencia (MHz) |
| BAND | Banda |
| MODE | Modo |
| TX_PWR | Potencia (W) |
| GRIDSQUARE | Locator Maidenhead |
| QSO_DATE | Fecha (YYYYMMDD) |
| TIME_ON | Hora (HHMM UTC) |
| DISTANCE | Distancia (km) |
| CQZ | Zona CQ |
| ITUZ | Zona ITU |
| NAME | Nombre del operador |
| RST_RCVD/SENT | Reporte RST |

---

## 🎓 Formato ADIF

El script maneja automáticamente:
- Codificación UTF-8, Latin-1, CP1252, ISO-8859-1
- Formato `NOMBRE:LONGITUD>valor` (estándar ADIF 3.x)
- Registros con `EOH` (header) y `EOR` (fin de registro)

---

## 📝 Licencia

MIT License - Libre para uso y modificación.

---

*Generado con analizar_adi_grafico.py y analizar_por_operador.py*
*Para EA1JBW/AM26PADRE* 🇪🇸
