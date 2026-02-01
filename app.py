import streamlit as st
import pandas as pd
import plotly.express as px

# =============================
# Configuration Streamlit
# =============================
st.set_page_config(
    page_title="Covid Dashboard",
    layout="wide"
)

st.title("🦠 Covid-19 Dashboard")
st.write("📊 Suivi des vagues de Covid à partir des données ECDC")
st.write(
    "Lien vers les données : https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country"
)

# =============================
# Chargement des données
# =============================
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# Nettoyage et préparation
df["dateRep"] = pd.to_datetime(df["dateRep"], dayfirst=True)
df = df.sort_values("dateRep").reset_index(drop=True)
df["cases"] = df["cases"].clip(lower=0)
df["deaths"] = df["deaths"].clip(lower=0)

# =============================
# Affichage des données brutes
# =============================
show_data = st.checkbox("Afficher les données")
if show_data:
    st.dataframe(
        df,
        column_config={
            "year": st.column_config.NumberColumn(format="%d"),
            "popData2020": st.column_config.NumberColumn(format="%d"),
        }
    )

# =============================
# ANALYSE MONDIALE
# =============================
st.subheader("Analyse au niveau mondial")

df_world = df.groupby("dateRep", as_index=False)["cases"].sum()
df_world["cas_cumules"] = df_world["cases"].cumsum()
df_world["moyenne_7j"] = df_world["cases"].rolling(7).mean()

# Cas cumulés
fig = px.area(
    df_world,
    x="dateRep",
    y="cas_cumules",
    title="Nombre de cas cumulés"
)
fig.update_layout(xaxis_title=None, yaxis_title=None)
st.plotly_chart(fig, use_container_width=True)

# Nouveaux cas
fig = px.line(
    df_world,
    x="dateRep",
    y=["cases", "moyenne_7j"],
    title="Nouveaux cas"
)

fig.update_layout(
    xaxis_title=None,
    yaxis_title=None
)

fig.update_traces(
    selector=dict(name="cases"),
    name="Nouveaux cas"
)

fig.update_traces(
    line=dict(color="orange"),
    selector=dict(name="moyenne_7j"),
    name="Moyenne sur 7 jours"
)

st.plotly_chart(fig, use_container_width=True)


# =============================
# ANALYSE PAR PAYS
# =============================
st.subheader("Analyse par pays")

# Correspondance FR -> EN
noms_pays = {
    "Allemagne": "Germany",
    "Autriche": "Austria",
    "Belgique": "Belgium",
    "Bulgarie": "Bulgaria",
    "Croatie": "Croatia",
    "Chypre": "Cyprus",
    "Danemark": "Denmark",
    "Espagne": "Spain",
    "Estonie": "Estonia",
    "Finlande": "Finland",
    "France": "France",
    "Grèce": "Greece",
    "Hongrie": "Hungary",
    "Islande": "Iceland",
    "Irlande": "Ireland",
    "Italie": "Italy",
    "Lettonie": "Latvia",
    "Liechtenstein": "Liechtenstein",
    "Lituanie": "Lithuania",
    "Luxembourg": "Luxembourg",
    "Malte": "Malta",
    "Norvège": "Norway",
    "Pays-Bas": "Netherlands",
    "Pologne": "Poland",
    "Portugal": "Portugal",
    "Roumanie": "Romania",
    "Slovaquie": "Slovakia",
    "Slovénie": "Slovenia",
    "Suède": "Sweden",
    "Tchéquie": "Czechia"
}

pays_choisi = st.selectbox(
    "Quel pays souhaitez-vous visualiser ?",
    options=["Tous les pays"] + list(noms_pays.keys())
)

if pays_choisi == "Tous les pays":
    df_pays = (
        df.groupby("dateRep", as_index=False)
          .agg({
              "cases": "sum",
              "deaths": "sum"
          })
          .sort_values("dateRep")
    )
else:
    pays_en = noms_pays[pays_choisi]
    df_pays = (
        df[df["countriesAndTerritories"] == pays_en]
        .sort_values("dateRep")
    )


# Moyennes mobiles
df_pays["moyenne_cas_7j"] = df_pays["cases"].rolling(7).mean()
df_pays["moyenne_deces_7j"] = df_pays["deaths"].rolling(7).mean()

# =============================
# TAUX DE CROISSANCE
# =============================
df_pays["taux_croissance_mensuel"] = (
    df_pays["moyenne_cas_7j"] /
    df_pays["moyenne_cas_7j"].shift(30)
)

taux_mensuel = df_pays["taux_croissance_mensuel"].iloc[-1]

st.metric(
    label="Taux de croissance mensuel",
    value=f"{taux_mensuel:.3f}"
)

st.caption(
    "Le taux de croissance mensuel compare la moyenne des cas sur 7 jours de la dernière date étudiée dans ce dataset "
    "à celle observée 30 jours plus tôt. \n\n"
    "S’il est supérieur à 1, l’épidémie a progressé. "
    "S’il est inférieur à 1, la vague a ralenti.")

# =============================
# GRAPHIQUES PAR PAYS
# =============================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cas positifs")

    fig_cases = px.line(
        df_pays,
        x="dateRep",
        y=["cases", "moyenne_cas_7j"]
    )

    fig_cases.update_layout(
        xaxis_title=None,
        yaxis_title=None
    )

    # Ligne bleue plus fine — renommée
    fig_cases.update_traces(
        selector=dict(name="cases"),
        line=dict(width=1.5),
        name="Cas par jour"
    )

    # Moyenne 7 jours — orange — renommée
    fig_cases.update_traces(
        selector=dict(name="moyenne_cas_7j"),
        line=dict(color="orange"),
        name="Moyenne sur 7 jours"
    )

    st.plotly_chart(fig_cases, use_container_width=True)


# Décès
with col2:
    st.subheader("Décès")

    fig_deaths = px.line(
        df_pays,
        x="dateRep",
        y=["deaths", "moyenne_deces_7j"]
    )

    fig_deaths.update_layout(
        xaxis_title=None,
        yaxis_title=None
    )

    # Ligne bleue plus fine — renommée
    fig_deaths.update_traces(
        selector=dict(name="deaths"),
        line=dict(width=1.5),
        name="Décès"
    )

    # Moyenne 7 jours — orange — renommée
    fig_deaths.update_traces(
        selector=dict(name="moyenne_deces_7j"),
        line=dict(color="orange"),
        name="Moyenne sur 7 jours"
    )

    st.plotly_chart(fig_deaths, use_container_width=True)
