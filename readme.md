# Saksbehandlingssimulator

Et lite Python-prosjekt som simulerer enkel, regelstyrt saksbehandling – slik det kan foregå i offentlig forvaltning (f.eks. hos NAV eller kommunen). 

Prosjektet demonstrerer regelbaserte beslutninger, lagring av søknader i database, og innsikt i offentlig logikk.

## Screenshots
<img width="399" height="288" alt="Skjermbilde 2025-08-18 005735" src="https://github.com/user-attachments/assets/6a1e2801-0790-4901-b718-3b265c84dbaa" />

<img width="343" height="275" alt="image" src="https://github.com/user-attachments/assets/7774956c-f58b-42c5-9565-a6a3feffd878" />


## Funksjoner

- Registrering av søker med alder, inntekt og arbeidsstatus
- Automatisk vurdering etter enkle regler (eks. for høy inntekt gir avslag)
- Lagring av alle saker i SQLite-database
- Visning av tidligere saker i terminalen

## Teknologi

- Python 3.x
- SQLAlchemy
- SQLite

## Kom i gang

1. **Lag virtuelt miljø og aktiver det**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # for PowerShell


# Installer avhengigheter
pip install sqlalchemy

#  Kjør programmet
python app.py

