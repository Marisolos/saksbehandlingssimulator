from database import Session, init_db
from models import Applicant, Case
from rules import evaluate_case

def main():
    init_db()
    session = Session()

    name = input("Navn: ")
    age = int(input("Alder: "))
    income = float(input("Inntekt: "))
    status = input("Arbeidsstatus (employed/unemployed): ")

    applicant = Applicant(name=name, age=age, income=income, employment_status=status)
    session.add(applicant)
    session.commit()

    decision, reason = evaluate_case(applicant)
    case = Case(applicant_id=applicant.id, status=decision, decision_reason=reason)
    session.add(case)
    session.commit()

    print(f"\n📝 Saksstatus: {decision.upper()} ({reason})")

    print("\n📋 Tidligere saker:")
    for case in session.query(Case).all():
        print(f"Sak {case.id}: {case.status.upper()} – {case.decision_reason}")

if __name__ == "__main__":
    main()
