import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. PAGE CONFIG & BASKETBALL AUSTRIA CI STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Basketball Austria Benchmarking Tool",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Basketball Austria CI Farben
COLOR_NAVY = "#0A2240"
COLOR_RED = "#C8322B"
COLOR_LIGHT_BLUE = "#8BB8E8"
COLOR_BG_LIGHT = "#F4F6F9"

# Custom CSS für Basketball Austria Design
st.markdown(f"""
    <style>
    .main {{
        background-color: {COLOR_BG_LIGHT};
    }}
    h1, h2, h3 {{
        color: {COLOR_NAVY} !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }}
    .stButton>button {{
        background-color: {COLOR_RED};
        color: white;
        border-radius: 5px;
    }}
    .metric-card {{
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid {COLOR_RED};
    }}
    </style>
""", unsafe_allow_html=True)

st.title("🏀 Basketball Austria - Club Benchmarking & Simulator")
st.markdown("Interaktives Analysetool zur Messung und Simulation der Kriterien in den österreichischen Basketball-Clubs.")

# ---------------------------------------------------------
# 2. DATEN: CLUBS & KATERGORIEN (AUS DEINEN BILDERN)
# ---------------------------------------------------------
ALL_CLUBS = [
    "Vienna Timberwolves",
    "BK IMMOunited Dukes",
    "BC Vienna",
    "Flyers Wels",
    "SKN St.Pölten Basketball",
    "Traiskirchen Lions",
    "OCS Swans Gmunden",
    "OCS Bulls Kapfenberg",
    "UBSC Raiffeisen Graz",
    "CITIES Panthers Fürstenfeld",
    "COLDAMARIS BBC Nord Dragonz",
    "Unger Steel Gunners Oberwart"
]

CATEGORIES = {
    "Spieltag & Ticketing": [
        "An-/Abreise", "Ticketerwerb", "Ticketarten", "Ticketpreise", 
        "Ticketkontrolle", "Security", "Platzzuweisung", "Platzwahl", 
        "Kapazitäten", "Zeit Einlassbeginn"
    ],
    "Catering & Gastronomie": [
        "Anzahl Verpflegungsstationen", "Spezielle Aktionen", "Essen Spezifisches Sortiment", 
        "Buffet", "Essen serviert", "Wege zum Essen", "Bestellung Handy", 
        "Essenspreise", "Getränkepreise", "Rabatt-Aktionen"
    ],
    "Event & Unterhaltung": [
        "Art des Rahmenprogramms", "Ergebnisabhängige Rabattaktionen", 
        "Ankündigung nächstes Heimspiel", "Rollen Stadionsprecher", 
        "Stadionsprecher und DJ", "Anzeigetafel", "Spielerpräsentation"
    ],
    "Halle & Infrastruktur": [
        "Hallenbau", "Feld", "Gestaltung Spielfeld", "Arten von Werbung", 
        "Körbe", "Lichtqualität", "Beschaffung Lehne", "Sitzplätze Anordnung", 
        "Courtside Seats", "Gesamtkapazität", "Anzahl Tribünen", "Erhöhung Tribünen", 
        "Kampfgericht", "Position Hallensprecher", "Teamfoulanzeige", "Spielerbänke", 
        "Verkleidung Hallenwände", "Parkplätze TV-Crew", "Verkabelung für TV", 
        "Halle internationale Veranstaltungen"
    ],
    "Sport & Nachwuchs": [
        "Lizenzstufen Trainer", "Art der Ausbildung - Trainer", "Trainingsstätte", 
        "Trainingskapazitäten", "Anzahl Nachwuchsmannschaften", "Frauensparte", 
        "Nachwuchsleistungszentrum", "Kooperationen mit Schulen", "Erfolg", "3x3"
    ],
    "Marketing & Sponsoring": [
        "Vereinsapp", "Zuschauer WLAN", "LED-Wall", "Arten von Merch", 
        "Vertriebskanäle", "Give-Away", "Aktivierungsmöglichkeiten", 
        "Anzahl Sponsoren", "Arten von Engagement", "Volumina", 
        "Anzahl in Sponsoringkategorien", "Kanäle + Regelmäßigkeit", 
        "Anzahl Follower", "Newsletter", "Werbung am Spieltag"
    ],
    "Nachhaltigkeit & Soziales": [
        "Ökologische Nachhaltigkeit", "Inklusionssport", "Weitere gesellschaftliche Themen"
    ]
}

# ---------------------------------------------------------
# 3. SEITENLEISTE (SELEKTION & SIMULATION)
# ---------------------------------------------------------
st.sidebar.header("🎯 Fokus & Auswahl")

# 1. Auswahl der zu vergleichenden Clubs
selected_clubs = st.sidebar.multiselect(
    "Clubs auswählen", 
    ALL_CLUBS, 
    default=["Traiskirchen Lions", "BK IMMOunited Dukes", "OCS Swans Gmunden"]
)

# 2. Hauptkategorie-Fokus
selected_category = st.sidebar.selectbox(
    "Fokus-Kategorie wählen", 
    list(CATEGORIES.keys())
)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Simulation (Live-Veränderung)")
st.sidebar.write("Simuliere Verbesserungen für einen ausgewählten Club:")

focus_club = st.sidebar.selectbox("Fokus-Club für Simulation", selected_clubs if selected_clubs else ALL_CLUBS)

# Generieren von Schiebereglern für Kriterien der Fokus-Kategorie
current_kriteria = CATEGORIES[selected_category]
simulated_scores = {}

st.sidebar.markdown(f"**Anpassung: {selected_category}**")
for krit in current_kriteria[:6]:  # Die ersten Kriterien steuerbar machen
    simulated_scores[krit] = st.sidebar.slider(
        f"{krit}", 
        min_value=1.0, max_value=10.0, value=6.5, step=0.5, key=f"sim_{krit}"
    )

# ---------------------------------------------------------
# 4. DASHBOARD / HAUPTBEREICH
# ---------------------------------------------------------
if not selected_clubs:
    st.warning("Bitte wähle mindestens einen Club in der Seitenleiste aus.")
    st.stop()

# Erzeuge synthetische Ausgangsdaten für die Demo
np.random.seed(101)
data_records = []

for club in selected_clubs:
    for cat, kriterien in CATEGORIES.items():
        for krit in kriterien:
            # Baseline-Wert generieren
            base_val = np.random.uniform(4.0, 9.0)
            # Falls dieser Club im Fokus steht und Werte simuliert wurden:
            if club == focus_club and cat == selected_category and krit in simulated_scores:
                val = simulated_scores[krit]
            else:
                val = base_val
            
            data_records.append({
                "Club": club,
                "Kategorie": cat,
                "Kriterium": krit,
                "Score": round(val, 1)
            })

df = pd.DataFrame(data_records)

# KPI / Metrik-Übersicht oben
st.markdown("### 📈 Key Performance Indicators")
kpi_cols = st.columns(len(selected_clubs))

for idx, club in enumerate(selected_clubs):
    club_df = df[df["Club"] == club]
    avg_total = club_df["Score"].mean()
    avg_cat = club_df[club_df["Kategorie"] == selected_category]["Score"].mean()
    
    with kpi_cols[idx]:
        st.markdown(f"""
        <div class="metric-card">
            <h4>{club}</h4>
            <p><b>Ø Fokus-Kategorie:</b> <span style="color:{COLOR_RED}; font-size:1.2em;">{avg_cat:.2f} / 10</span></p>
            <p><b>Ø Gesamt-Benchmarking:</b> {avg_total:.2f} / 10</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# 5. FOKUS-VISUALISIERUNG (KATEGORIE & KRITERIEN)
# ---------------------------------------------------------
st.subheader(f"📊 Detail-Vergleich: {selected_category}")

df_category = df[df["Kategorie"] == selected_category]

# Grouped Bar Chart mit Matplotlib (im Basketball Austria CI Style)
fig, ax = plt.subplots(figsize=(12, 6))

kriterien_list = CATEGORIES[selected_category]
x = np.arange(len(kriterien_list))
bar_width = 0.8 / len(selected_clubs)

# Farbpalette passend zum CI
colors = [COLOR_NAVY, COLOR_RED, COLOR_LIGHT_BLUE, "#555555", "#E69F00", "#56B4E9"]

for i, club in enumerate(selected_clubs):
    club_scores = [
        df_category[(df_category["Club"] == club) & (df_category["Kriterium"] == k)]["Score"].values[0]
        for k in kriterien_list
    ]
    ax.bar(x + (i * bar_width), club_scores, width=bar_width, label=club, color=colors[i % len(colors)])

ax.set_ylabel("Bewertung (1 - 10)", fontsize=11, fontweight='bold', color=COLOR_NAVY)
ax.set_title(f"Performance-Analyse aller Kriterien in '{selected_category}'", fontsize=13, fontweight='bold', pad=15, color=COLOR_NAVY)
ax.set_xticks(x + bar_width * (len(selected_clubs) - 1) / 2)
ax.set_xticklabels(kriterien_list, rotation=45, ha="right", fontsize=10)
ax.set_ylim(0, 10.5)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend(frameon=True, facecolor='white', edgecolor='none')

# Design feintunen
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

st.markdown("---")

# ---------------------------------------------------------
# 6. GESAMT-KATEGORIEN-VERGLEICH & DATENTABELLE
# ---------------------------------------------------------
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🌐 Übersicht aller Kategorien")
    # Aggregiere Scores pro Kategorie & Club
    df_cat_summary = df.groupby(["Kategorie", "Club"])["Score"].mean().reset_index()
    
    pivot_summary = df_cat_summary.pivot(index="Kategorie", columns="Club", values="Score")
    st.dataframe(pivot_summary.style.highlight_max(axis=1, color="#d4edda"), use_container_width=True)

with col_right:
    st.subheader("📋 Kriterien-Details (Rohdaten)")
    st.dataframe(
        df_category[["Club", "Kriterium", "Score"]].sort_values(by=["Kriterium", "Club"]),
        use_container_width=True,
        height=350
    )
