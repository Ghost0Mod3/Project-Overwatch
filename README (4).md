# PROJECT OVERWATCH

<div align="center">

```text
 ██████╗ ██╗   ██╗███████╗██████╗ ██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗
██╔═══██╗██║   ██║██╔════╝██╔══██╗██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║
██║   ██║██║   ██║█████╗  ██████╔╝██║ █╗ ██║███████║   ██║   ██║     ███████║
██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║███╗██║██╔══██║   ██║   ██║     ██╔══██║
╚██████╔╝ ╚████╔╝ ███████╗██║  ██║╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║
 ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
```

### Global intelligence headlines. Regional signals. One tactical interface.

![Python](https://img.shields.io/badge/Python-3.10%2B-39ff14?style=for-the-badge&logo=python&logoColor=black)
![PySide6](https://img.shields.io/badge/UI-PySide6-00aa44?style=for-the-badge&logo=qt&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active%20Prototype-ffb000?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078d4?style=for-the-badge&logo=windows&logoColor=white)

</div>

---

## Mission

**Project Overwatch** is a desktop intelligence-monitoring prototype built with Python and PySide6. It collects reporting from enabled RSS sources, scores and classifies incoming articles, organizes reports by region and topic, and presents the results through a tactical black-and-neon-green dashboard.

The system is designed for rapid situational awareness without forcing the operator to jump between dozens of news pages.

> **Project Overwatch does not produce official intelligence or threat assessments.** Signal levels are experimental, news-derived indicators based on the articles retrieved by the application.

---

## System Overview

Project Overwatch combines five core systems:

1. **RSS collection** from international, regional, defense, cyber, infrastructure, technology, and emergency-monitoring sources.
2. **Article classification** into operational categories such as missile, drone, cyber, naval, air, ground, homeland, diplomatic, and general intelligence.
3. **Relevance scoring** using configurable keywords and event weighting.
4. **Regional monitoring** with focused filters generated from article metadata already flowing through the feed.
5. **Tactical visualization** through an offline GeoJSON world map, animated hotspot markers, and color-coded signal panels.

---

## Current Capabilities

### Intelligence Feed

- Retrieves up to four reports per enabled source.
- Removes duplicate links and normalized duplicate headlines.
- Sorts reports by relevance and event priority.
- Refreshes network feeds every three minutes.
- Runs feed retrieval in a background thread so the dashboard remains responsive.
- Rotates visible non-pinned reports every ten seconds.
- Shows eight rotating reports per page.
- Pins the highest-scoring report at the top as **PINNED URGENT**.
- Displays publication date and time when available.
- Preserves the article or broadcast URL.
- Opens a report in the default browser when the row is clicked.

### Regional Filtering

The filter menu is rebuilt from region metadata found in the current RSS results.

Examples may include:

- Ukraine
- Russia
- NATO
- Black Sea
- Taiwan
- Taiwan Strait
- China
- South China Sea
- Philippines
- Middle East
- Israel
- Gaza
- Iran
- Yemen
- Red Sea
- United States

Regions with the most reports appear first. Selecting **ALL REPORTS** restores the complete feed.

### Live Search

The search box works together with the regional filter and searches across:

- Headline
- Summary
- Source
- Region
- Category
- Event type

Example workflow:

```text
Region: UKRAINE
Search: drone
Result: Ukraine-related drone reports only
```

### Global Threat Signals

The Global Threats panel currently monitors:

- Ukraine
- Taiwan
- Middle East
- South China Sea

Each panel displays:

```text
REGION: SIGNAL LEVEL
SIGNAL SCORE | MATCHING REPORTS
```

Signal levels:

```text
NO SIGNAL
LOW
GUARDED
ELEVATED
HIGH
CRITICAL
```

### Homeland Watch

The Homeland Watch panel monitors United States-related reporting for:

- Cyber activity
- Critical infrastructure
- Border security
- Public safety
- Energy grid
- Transportation

### Offline Tactical Map

- Loads country geometry from `resources/world.geojson`.
- Draws neon-green country outlines.
- Displays latitude and longitude grid lines.
- Displays the equator and prime meridian.
- Supports mouse-wheel zoom.
- Supports drag-to-pan.
- Resets the view on double-click.
- Displays animated prototype hotspot pulses.
- Requires no browser engine or external map service.

---

## Interface Layout

```text
+-----------------------------------------------------------------------+
|                         PROJECT OVERWATCH                             |
+------------------------------------------+----------------------------+
| ACTIVE EVENTS                            | GLOBAL THREATS             |
| [REGION FILTER] [LIVE SEARCH]            | Ukraine                    |
|                                          | Taiwan                     |
| [PINNED URGENT REPORT]                    | Middle East                |
| [Rotating clickable reports]             | South China Sea            |
+------------------------------------------+----------------------------+
| GLOBAL OPERATIONS MAP                    | HOMELAND WATCH             |
|                                          | Cyber                      |
| Offline GeoJSON world map                | Infrastructure             |
| Animated hotspot visualization           | Border Security            |
|                                          | Public Safety              |
|                                          | Energy Grid                |
|                                          | Transportation             |
+------------------------------------------+----------------------------+
| SYSTEM STATUS | ARTICLE COUNT | FILTER | REFRESH STATE | MAP STATUS   |
+-----------------------------------------------------------------------+
```

---

## Project Structure

```text
Project Overwatch/
|
|-- app.py
|-- requirements.txt
|-- README.md
|
|-- feeds/
|   |-- __init__.py
|   |-- rss_fetcher.py
|   `-- sources.py
|
|-- intelligence/
|   |-- __init__.py
|   |-- classifier.py
|   `-- relevance.py
|
|-- resources/
|   `-- world.geojson
|
`-- ui/
    |-- __init__.py
    |-- main_window.py
    `-- map_widget.py
```

---

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer recommended
- Internet access for RSS retrieval
- Local `world.geojson` file for the tactical map

Python packages:

```text
PySide6
feedparser
requests
beautifulsoup4
sqlalchemy
```

---

## Installation

### 1. Open PowerShell in the project directory

```powershell
cd "C:\Users\D4lew\OneDrive\Desktop\Project Overwatch"
```

### 2. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 3. Confirm the map data exists

```powershell
Get-Item ".\resources\world.geojson"
```

### 4. Compile-check the critical files

```powershell
py -m py_compile .\app.py
py -m py_compile .\ui\main_window.py
py -m py_compile .\ui\map_widget.py
py -m py_compile .\feeds\rss_fetcher.py
py -m py_compile .\feeds\sources.py
py -m py_compile .\intelligence\classifier.py
py -m py_compile .\intelligence\relevance.py
```

No output means the files passed Python syntax compilation.

### 5. Launch Project Overwatch

```powershell
py app.py
```

---

## Operator Controls

### Active Events

| Action | Result |
|---|---|
| Select a region | Filters reports to the selected region |
| Type in the search box | Filters reports immediately |
| Click a report | Opens the source page in the default browser |
| Clear the search box | Restores the selected region's reports |
| Select `ALL REPORTS` | Restores the complete intelligence feed |

### Tactical Map

| Action | Result |
|---|---|
| Drag | Pan the map |
| Mouse wheel | Zoom in or out |
| Double-click | Reset the map view |
| Hover over a hotspot | Display hotspot details |

---

## Timing Configuration

Timing values are defined in `ui/main_window.py`:

```python
REFRESH_INTERVAL_MS = 180_000
ROTATION_INTERVAL_MS = 10_000
ROTATING_ARTICLES_PER_PAGE = 8
```

Current behavior:

```text
RSS network refresh:       every 3 minutes
Headline display rotation: every 10 seconds
Reports shown per page:    8 plus the pinned urgent report
```

---

## RSS Source Registry

Sources are configured in:

```text
feeds/sources.py
```

Each source can include:

```python
{
    "name": "BBC World",
    "category": "WORLD",
    "region": "GLOBAL",
    "url": "RSS URL",
    "aggregated": False,
    "enabled": True,
    "trust_score": 92,
}
```

The source registry supports:

- Direct RSS feeds
- Google News RSS searches
- Region metadata
- Category metadata
- Enable or disable state
- Source trust metadata
- Registry validation

---

## Classification Codes

| Code | Classification |
|---|---|
| `MSL` | Missile |
| `UAV` | Drone or unmanned aircraft |
| `CYB` | Cybersecurity |
| `NAV` | Naval activity |
| `AIR` | Air activity or airstrike |
| `GRD` | Ground activity |
| `DIP` | Diplomatic development |
| `HML` | Homeland or infrastructure |
| `INT` | General intelligence reporting |

---

## Signal Engine

The experimental signal engine considers:

- Article relevance score
- Event classification
- Number of matching reports
- Source-assigned region
- Headline and summary keywords
- Strongest matching reports
- Reduced weighting for lower-ranked reports

The signal engine is intended to highlight reporting volume and relevance. It does not verify events independently and must not be treated as an emergency warning system.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'ui.main_window'`

Confirm the filename is exactly:

```text
ui\main_window.py
```

Also confirm this file exists:

```text
ui\__init__.py
```

### Missing method errors

Clear Python's cached modules:

```powershell
Remove-Item ".\ui\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
```

Then compile the file again:

```powershell
py -m py_compile .\ui\main_window.py
```

### Map data not found

Confirm:

```text
resources\world.geojson
```

Then validate it:

```powershell
py -c "import json; data=json.load(open(r'.\resources\world.geojson', encoding='utf-8')); print(data['type'], len(data.get('features', [])))"
```

### Dashboard opens slowly

Project Overwatch may have a large enabled RSS registry. Feed retrieval runs in the background, but a full update can still take time depending on source availability and network response times.

### Some feeds fail

RSS endpoints may become unavailable, reject automated requests, redirect, or return malformed XML. The fetcher records feed-level errors and continues processing the remaining sources.

---

## Roadmap

- [x] Native PySide6 dashboard
- [x] Offline GeoJSON world map
- [x] Animated hotspot visualization
- [x] Multi-source RSS collection
- [x] Relevance scoring
- [x] Event classification
- [x] Background feed retrieval
- [x] Three-minute automatic refresh
- [x] Clickable source links
- [x] Pinned urgent report
- [x] Publication date and time
- [x] Ten-second headline rotation
- [x] Focused regional filters
- [x] Live report search
- [x] News-derived Global Threat signals
- [x] News-derived Homeland Watch signals
- [ ] Clickable map countries that activate feed filters
- [ ] Article detail preview panel
- [ ] Manual refresh control
- [ ] Source enable and disable settings
- [ ] Persistent local article database
- [ ] Historical signal charting
- [ ] Map hotspots generated from live article locations
- [ ] Saved operator filter profiles
- [ ] Packaged Windows executable

---

## Security and Accuracy Notice

Project Overwatch processes public reporting and configured RSS search results. The presence of an article does not prove that the underlying event is accurate, current, independently confirmed, or correctly classified.

Always verify critical information against multiple reputable primary sources and official emergency or government channels.

Project Overwatch is not intended for military operations, emergency dispatch, law enforcement decisions, investment decisions, or personal safety decisions.

---

## Data and Content Notice

Article headlines, summaries, links, publication metadata, and source names remain the property of their respective publishers. Project Overwatch displays retrieved metadata and directs the operator to the original source page.

Country geometry is loaded from the local GeoJSON dataset placed in the `resources` directory. Review the dataset's accompanying license and boundary notes before redistribution.

---

## Development Philosophy

```text
SEE THE SIGNAL.
FILTER THE NOISE.
VERIFY THE SOURCE.
NEVER CONFUSE VOLUME WITH TRUTH.
```

Project Overwatch is being built iteratively, one working system at a time. The priority is a responsive interface, transparent scoring, modular code, and direct access to original reporting.

---

<div align="center">

## SYSTEM STATUS

```text
[ DASHBOARD ONLINE ]
[ RSS ENGINE CONNECTED ]
[ TACTICAL MAP READY ]
[ REGIONAL FILTERS ACTIVE ]
[ LIVE SEARCH ACTIVE ]
[ OPERATOR VERIFICATION REQUIRED ]
```

**PROJECT OVERWATCH**

*Global monitoring prototype built for clarity, speed, and control.*

</div>
