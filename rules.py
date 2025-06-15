def evaluate_case(applicant):
    if applicant.age < 18:
        return "rejected", "Under 18 år"
    if applicant.income > 200000:
        return "rejected", "For høy inntekt"
    if applicant.employment_status != "unemployed":
        return "rejected", "Ikke arbeidsledig"

    return "approved", "Krav oppfylt"
