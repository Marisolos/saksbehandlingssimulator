# 🏛️ Saksbehandlingssimulator

Et lite Python-prosjekt som simulerer enkel, regelstyrt saksbehandling – slik det kan foregå i offentlig forvaltning (f.eks. hos NAV eller kommunen). 

Prosjektet er laget som del av en søknad til master i forvaltningsinformatikk, og demonstrerer regelbaserte beslutninger, lagring av søknader i database, og innsikt i offentlig logikk.

## 🎯 Funksjoner

- Registrering av søker med alder, inntekt og arbeidsstatus
- Automatisk vurdering etter enkle regler (eks. for høy inntekt gir avslag)
- Lagring av alle saker i SQLite-database
- Visning av tidligere saker i terminalen

## 📦 Teknologi

- Python 3.x
- SQLAlchemy
- SQLite

## 🚀 Kom i gang

1. **Lag virtuelt miljø og aktiver det**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # for PowerShell


# Installer avhengigheter
pip install sqlalchemy

#  Kjør programmet
python app.py

