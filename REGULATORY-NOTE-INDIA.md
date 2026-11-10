# Regulatory note — India (CDSCO Medical Device Software guidance, 2026)

*This note is contributed from outside the project as a pointer to the applicable Indian guidance. It is
not legal advice, and it does not change any existing file in this repository.*

## The guidance

India's Central Drugs Standard Control Organisation (CDSCO) issued its final **Guidance Document on
Medical Device Software**, Doc No. `CDSCO/MD/GD/MDSW/01/2026`, on **21 July 2026**, under the Medical
Devices Rules, 2017 (MDR-2017). It applies to software **intended for a medical purpose** — diagnosis,
prevention, monitoring, treatment or alleviation of disease or disorder.

## Why it appears to apply here

This project performs three of the listed medical purposes:

| Feature | Medical purpose |
|---|---|
| Symptom-based disease prediction with a confidence score | **Diagnosis** |
| Disease-specific medicine information (`dataset/medicine.csv` lists prescription-class medicines) | **Treatment information** |
| Emergency level with a recommended action (`dataset/emergency_level.csv`) | **Triage** |

## Indicative classification

For standalone software the guidance classifies on two axes — the seriousness of the condition, and the
significance of the information provided:

- **Significance:** treat or diagnose — the highest of the three levels.
- **Condition:** serious for most of the diseases in the dataset.
- **Result:** serious + treat-or-diagnose → **Class C**.
- **Escalation:** the guidance notes that standalone software used by **non-clinical users without
  professional support** in a serious situation may be treated as used in a *critical* situation, which
  moves it toward **Class D**.

## The disclaimer does not change the classification

The project README states that this is "not a medical device". CDSCO reads intended use from the
labelling, instructions for use, website and promotional material. A feature that predicts disease is a
diagnostic claim regardless of a disclaimer, so the disclaimer should not be relied upon as a
regulatory position.

## If this project moves toward real users

1. **Write an intended-use statement first.** It drives the classification and the documentation set.
2. **Test licence before evaluation.** Evaluation or demonstration with real patients is not
   commercialisation, but it still requires a test licence (Form MD-12/MD-13 for domestic manufacture)
   through the National Single Window System (NSWS) portal.
3. **Manufacturing licence before real use.** Commercial distribution requires a manufacturing licence
   or registration under Chapter IIIB of MDR-2017.
4. **Validation.** A model trained on synthetically generated data is not clinical validation. The
   guidance expects clinical evidence that the software performs safely and effectively for its
   intended purpose.
5. **AI-specific risk documentation.** The guidance expects hazard identification, cybersecurity risk,
   **AI bias**, **model drift** and **hallucination** to be addressed in the risk file — the last is
   directly relevant to a disease-answering chatbot.

## If this is a learning or portfolio project

Nothing here requires action, provided the software is not presented to patients as a diagnostic tool.
The practical safeguard is to keep the disclaimer accurate about *what the software does* rather than
about *what it legally is* — for example, stating that predictions are for educational demonstration and
must not be used to make health decisions.

## Source

Guidance Document on Medical Device Software, CDSCO/MD/GD/MDSW/01/2026, published on the CDSCO website
(Medical Devices division). Readers should rely on the statutory provisions of the Drugs and Cosmetics
Act, 1940 and MDR-2017 rather than on this note.
