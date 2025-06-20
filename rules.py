def evaluate_case(applicant):
    #  Teknisk kontroll
    if applicant.income < 0:
        return "rejected", "Teknisk avslag: Inntekt kan ikke være negativ"
    if applicant.age <= 0 or applicant.age > 120:
        return "rejected", "Teknisk avslag: Ugyldig alder"
    if not applicant.documentation_provided:
        return "rejected", "Teknisk avslag: Mangler dokumentasjon"

    # Reelle vurderinger
    if applicant.age < 18:
        return "rejected", "Alder under 18 – oppfyller ikke krav"
    if applicant.age > 67:
        return "rejected", "Over pensjonsalder – krav oppfylt via annen ordning"
    if applicant.income > 200000:
        return "rejected", "Inntekt overstiger inntektsgrensen"
    if applicant.employment_status != "unemployed":
        return "rejected", "Søker må være arbeidsledig"
    if applicant.education_level == "none":
        return "rejected", "Utdanningskrav ikke oppfylt"

    #  Godkjente kriterier
    if applicant.has_children:
        return "approved", "Barn gir rett til støtte"
    if applicant.income < 250000:
        return "approved", "Lav inntekt gir rett til støtte"

    return "rejected", "Oppfyller ikke kriteriene"
