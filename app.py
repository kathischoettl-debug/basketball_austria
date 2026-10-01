import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Seiten-Konfiguration
st.set_page_config(
    page_title="Basketball Club Benchmarking",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏀 Basketball Club Benchmarking & Analyse Tool")
st.markdown("Vergleiche verschiedene Basketballclubs basierend auf ihren Infrastruktur-, Matchday-, Marketing- und Sport-Kriterien.")

# ---------------------------------------------------------
# DATENSTRUCTURE & KRITERIEN (AUS DEM BILD)
# ---------------------------------------------------------
kriterien_kategorien = {
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
    "Marketing, Digitales & Sponsoring": [
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
# SEITENLEISTE: Steuerung & Clubauswahl
# ---------------------------------------------------------
st.sidebar.header("⚙️ Benchmarking-Einstellungen")

# Club-Auswahl
clubs = ["Club A (z.B. FC Bayern)", "Club B (z.B. ALBA Berlin)", "Club C (z.B. Ratiopharm Ulm)"]
selected_clubs = st.sidebar.multiselect("Clubs für Vergleich auswählen", clubs, default=clubs[:2])

# Kategorie-Auswahl
selected_kategorie = st.sidebar.selectbox("Fokus-Kategorie wählen", list(kriterien_kategorien.keys()))

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Simulation / Bewertung anpassen")
st.sidebar.markdown("Bewerte die Kriterien der gewählten Kategorie (1 = Mangelhaft, 10 = Exzellent):")

# Dynamische Regler für die ausgewählte Kategorie
kriterien_in_kat = kriterien_kategorien[selected_kategorie]
scores_club_a = {}
for krit in kriterien_in_kat[:5]:  # Beispielhaft die ersten 5 Kriterien als Regler
    scores_club_a[krit] = st.sidebar.slider(f"{krit}", 1, 10, 7, key=krit)

# ---------------------------------------------------------
# HAUPTSEITE: Visualisierungen & Vergleich
# ---------------------------------------------------------

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📊 Benchmarking-Vergleich: {selected_kategorie}")
    
    # Dummy-Daten generieren für Demonstration
    np.random.seed(42)
    data = []
    for club in selected_clubs:
        for krit in kriterien_in_kat:
            score = scores_club_a.get(krit, np.random.randint(4, 10)) if "Club A" in club else np.random.randint(3, 10)
            data.append({"Club": club, "Kriterium": krit, "Score": score})
    
    df_scores = pd.DataFrame(data)
    
    # Balkendiagramm erzeugen
    fig, ax = plt.subplots(figsize=(10, 6))
    for club in selected_clubs:
        sub_df = df_scores[df_scores["Club"] == club]
        ax.barh(sub_df["Kriterium"], sub_df["Score"], alpha=0.6, label=club)
    
    ax.set_xlabel("Bewertung / Performance (1-10)")
    ax.set_xlim(0, 10)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="lower right")
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("📋 Kriterien-Übersicht")
    st.write(f"In der Kategorie **{selected_kategorie}** befinden sich insgesamt **{len(kriterien_in_kat)} Kriterien** aus deinem Katalog:")
    for k in kriterien_in_kat:
        st.markdown(f"- **{k}**")

st.markdown("---")

# Detaillierte Datentabelle
if st.checkbox("🔍 Vollständige Benchmarking-Matrix als Tabelle anzeigen"):
    pivoted_df = df_scores.pivot(index="Kriterium", columns="Club", values="Score")
    st.dataframe(pivoted_df, use_container_width=True)
