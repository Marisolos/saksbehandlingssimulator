import streamlit as st
from database import Session, init_db
from models import Applicant, Case, Base 
from rules import evaluate_case
from sqlalchemy import create_engine
from sqlalchemy.orm import close_all_sessions
from collections import Counter
from datetime import datetime
import pandas as pd
import io
import csv
import os

# Page config
st.set_page_config(page_title="Saksbehandlingssimulator", page_icon="🏩", layout="centered")

# Init DB and session
init_db()
session = Session()


with st.expander("🔧 Utviklerverktøy: Nullstill database"):
    if st.button("❌ Slett og gjenopprett database"):
        try:
            # Lukk alle aktive tilkoblinger
            close_all_sessions()
            session.close()

            # Forsøk å slette databasen
            if os.path.exists("cases.db"):
                os.remove("cases.db")

            # Reopprett database
            engine = create_engine("sqlite:///cases.db")
            Base.metadata.create_all(bind=engine)
            engine.dispose()  # 🔥 Viktig!

            # Re-initialiser session
            init_db()
            session = Session()

            st.success("✅ Databasen ble nullstilt!")

        except Exception as e:
            st.error(f"Klarte ikke nullstille databasen: {e}")


# Header
st.markdown("<h1 style='text-align: center; color: #1f4e79;'>🏩 Saksbehandlingssimulator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>Simuler forenklet, regelstyrt saksbehandling i offentlig sektor</p>", unsafe_allow_html=True)
st.divider()

# 📄 Søknadsskjema
with st.container():
    st.subheader("📄 Ny søknad")
    with st.form("soknadsskjema", border=True):
        name = st.text_input("Fullt navn")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Alder", min_value=0, max_value=120, value=25)
        with col2:
            income = st.number_input("Årlig inntekt (kr)", min_value=0.0, step=1000.0, value=100000.0)

        col3, col4 = st.columns(2)
        with col3:
            status = st.selectbox("Arbeidsstatus", ["unemployed", "employed"])
        with col4:
            has_children = st.checkbox("Har barn under 18 år?", value=False)

        education_level = st.selectbox(
            "Utdanningsnivå",
            ["none", "highschool", "university"],
            format_func=lambda x: {
                "none": "Ingen utdanning",
                "highschool": "Videregående skole",
                "university": "Høyere utdanning"
            }[x]
        )

        documentation_provided = st.checkbox("📎 Jeg bekrefter at dokumentasjon er levert")

        submitted = st.form_submit_button("📨 Send søknad")

        if submitted:
            try:
                applicant = Applicant(
                    name=name,
                    age=age,
                    income=income,
                    employment_status=status,
                    has_children=has_children,
                    education_level=education_level,
                    documentation_provided=documentation_provided
                )
                session.add(applicant)
                session.commit()

                decision, reason = evaluate_case(applicant)

                case = Case(
                    applicant_id=applicant.id,
                    status=decision,
                    decision_reason=reason,
                    created_at=datetime.utcnow()
                )
                session.add(case)
                session.commit()

                if decision == "approved":
                    st.success(f"✅ Søknad innvilget: {reason}")
                else:
                    st.error(f"❌ Søknad avslått: {reason}")

            except Exception as e:
                st.error(f"Feil under behandling: {e}")

st.divider()
st.subheader("📋 Tidligere saker")

try:
    cases = session.query(Case).all()

    if not cases:
        st.info("Ingen saker registrert ennå.")
    else:
        st.markdown("### 🎛️ Filtrering")
        colf1, colf2, colf3 = st.columns(3)

        with colf1:
            status_filter = st.selectbox("Filtrer etter status", ["Alle", "approved", "rejected"])
        with colf2:
            order_filter = st.selectbox("Sorter etter", ["Nyeste først", "Eldste først"])
        with colf3:
            emp_filter = st.selectbox("Arbeidsstatus", ["Alle", "unemployed", "employed"])

        filtered_cases = cases

        if status_filter != "Alle":
            filtered_cases = [c for c in filtered_cases if c.status == status_filter]
        if emp_filter != "Alle":
            filtered_cases = [
                c for c in filtered_cases
                if session.query(Applicant).get(c.applicant_id).employment_status == emp_filter
            ]
        if order_filter == "Nyeste først":
            filtered_cases = filtered_cases[::-1]

        for c in filtered_cases:
            applicant = session.query(Applicant).get(c.applicant_id)
            created_str = c.created_at.strftime("%d.%m.%Y %H:%M") if c.created_at else "?"
            edu = {
                "none": "Ingen utdanning",
                "highschool": "Videregående",
                "university": "Høyere utdanning"
            }.get(applicant.education_level, "?")
            st.markdown(f"""
            <div style="background-color:#f8f9fa;padding:10px;border-radius:8px;margin-bottom:10px">
                <b>Sak {c.id}</b><br>
                Søker: {applicant.name} – {applicant.age} år<br>
                Inntekt: {applicant.income:,.0f} kr – Status: <span style="color:{'green' if c.status == 'approved' else 'red'}">{c.status.upper()}</span><br>
                Arbeidsstatus: {applicant.employment_status} – Barn: {"Ja" if applicant.has_children else "Nei"}<br>
                Utdanning: {edu} – Dokumentasjon: {"Levert" if applicant.documentation_provided else "Ikke levert"}<br>
                Behandlet: {created_str}<br>
                Begrunnelse: {c.decision_reason}
            </div>
            """, unsafe_allow_html=True)

        st.subheader("📈 Økonomisk innsikt")
        grouped = {"approved": [], "rejected": []}
        for c in cases:
            a = session.query(Applicant).get(c.applicant_id)
            grouped[c.status].append(a.income)
        for status in grouped:
            if grouped[status]:
                avg = sum(grouped[status]) / len(grouped[status])
                st.write(f"🔹 Gjennomsnittlig inntekt for {status.upper()}: {avg:,.0f} kr")

        st.subheader("📊 Statistikk")
        statuses = [c.status for c in cases]
        counter = Counter(statuses)
        df = pd.DataFrame.from_dict(counter, orient='index', columns=['Antall saker'])
        st.bar_chart(df)

        st.subheader("📄 Eksport")
        if st.button("📅 Last ned filtrerte saker som CSV"):
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["SakID", "Navn", "Alder", "Inntekt", "Arbeidsstatus", "Barn", "Utdanning", "Dokumentasjon", "Status", "Begrunnelse", "Dato"])

            for c in filtered_cases:
                a = session.query(Applicant).get(c.applicant_id)
                writer.writerow([
                    c.id, a.name, a.age, a.income, a.employment_status,
                    "Ja" if a.has_children else "Nei",
                    a.education_level,
                    "Levert" if a.documentation_provided else "Ikke levert",
                    c.status, c.decision_reason,
                    c.created_at.strftime("%d.%m.%Y %H:%M") if c.created_at else ""
                ])

            st.download_button(
                label="📄 Last ned CSV",
                data=output.getvalue(),
                file_name="saker.csv",
                mime="text/csv"
            )

except Exception as e:
    st.error(f"Feil ved lasting av saker: {e}")
