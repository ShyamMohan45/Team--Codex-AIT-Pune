"""
Sample clinical notes for testing the RAG system
"""

SAMPLE_NOTES = {
    "pneumonia_case": """
Chief Complaint:
Fever, cough, and shortness of breath

History of Present Illness:
Mr. Sharma, 65-year-old male, presents with fever (38.9°C), productive cough with yellow sputum, and shortness of breath for 3 days. Patient reports progressive worsening of dyspnea on exertion. Denies chest pain, but reports feeling weak and fatigued. No recent travel. Patient is a former smoker (20 pack-years, quit 5 years ago).

Past Medical History:
Type 2 Diabetes Mellitus (controlled on metformin)
Hypertension (controlled on lisinopril)
Hyperlipidemia

Medications:
Metformin 1000mg BID
Lisinopril 10mg daily
Atorvastatin 20mg daily

Allergies:
Penicillin (rash)

Vital Signs:
Temperature: 38.9°C (102°F)
Blood Pressure: 135/85 mmHg
Heart Rate: 98 bpm
Respiratory Rate: 24/min
SpO2: 91% on room air

Physical Exam:
General: Alert, oriented, appears ill and in mild respiratory distress
HEENT: Normal
Neck: No lymphadenopathy
Lungs: Decreased breath sounds in right lower lobe, crackles present on auscultation
Heart: Regular rate and rhythm, no murmurs
Abdomen: Soft, non-tender
Extremities: No edema

Laboratory:
WBC: 16.5 x10^9/L (elevated, reference 4-11)
Neutrophils: 82% (elevated)
CRP: 120 mg/L (elevated, reference <10)
Procalcitonin: 2.5 ng/mL (elevated, reference <0.5)
Blood glucose: 145 mg/dL
Creatinine: 1.0 mg/dL (normal)

Imaging:
Chest X-ray (PA and Lateral):
- Right lower lobe consolidation consistent with lobar pneumonia
- No pleural effusion
- No pneumothorax
- Cardiac silhouette normal

Assessment and Plan:
65-year-old male with clinical and radiographic findings consistent with community-acquired pneumonia (CAP). Given penicillin allergy, will initiate treatment with respiratory fluoroquinolone. Close monitoring required given age and comorbidities.
""",
    
    "mi_case": """
Chief Complaint:
Chest pain

History of Present Illness:
Ms. Johnson, 58-year-old female, presents to ED with acute onset substernal chest pressure that started 2 hours ago while at rest. Pain radiates to left arm and jaw. Associated with diaphoresis, nausea, and shortness of breath. Patient describes pain as "crushing" and rates it 8/10. No relief with rest. No prior similar episodes.

Past Medical History:
Hypertension (poorly controlled)
Dyslipidemia
Family history: Father had MI at age 60

Medications:
Amlodipine 5mg daily
Simvastatin 40mg daily

Allergies:
None known

Vital Signs:
Blood Pressure: 165/95 mmHg
Heart Rate: 105 bpm
Respiratory Rate: 20/min
SpO2: 95% on room air
Temperature: 37.2°C

Physical Exam:
General: Anxious, diaphoretic
HEENT: Normal
Neck: JVP not elevated
Lungs: Clear bilaterally
Heart: Tachycardic, regular rhythm, no murmurs
Abdomen: Soft, non-tender
Extremities: No edema, pulses intact

Laboratory:
Troponin I: 2.5 ng/mL (elevated, reference <0.04) at presentation, 5.8 ng/mL at 3 hours (rising)
CK-MB: 45 U/L (elevated)
BNP: 250 pg/mL (mildly elevated)
D-dimer: Normal
Complete blood count: Normal

ECG:
ST-segment elevation of 3mm in leads II, III, and aVF
Reciprocal ST depression in leads I and aVL
Concerning for acute inferior wall STEMI

Imaging:
Chest X-ray: Normal heart size, clear lung fields

Assessment and Plan:
58-year-old female presenting with acute chest pain, elevated cardiac biomarkers, and ECG findings consistent with acute ST-elevation myocardial infarction (STEMI) - inferior wall. Cardiology consulted. Patient being prepared for urgent cardiac catheterization. Aspirin, clopidogrel, and heparin initiated.
""",
    
    "sepsis_case": """
Chief Complaint:
Confusion and fever

History of Present Illness:
Mr. Lee, 72-year-old male, brought to ED by family for altered mental status and fever. Family reports patient has been increasingly confused over past 24 hours. Patient has had decreased oral intake, appears weak, and has had multiple episodes of diarrhea. Temperature at home was 39.2°C. Patient has chronic indwelling urinary catheter for neurogenic bladder.

Past Medical History:
Spinal cord injury (T10 level) from MVA 10 years ago
Neurogenic bladder with chronic Foley catheter
Recurrent UTIs
Hypertension

Medications:
Lisinopril 20mg daily
Tamsulosin 0.4mg daily

Vital Signs:
Temperature: 39.5°C (103.1°F)
Blood Pressure: 85/50 mmHg (hypotensive)
Heart Rate: 125 bpm (tachycardic)
Respiratory Rate: 26/min (tachypneic)
SpO2: 94% on room air

Physical Exam:
General: Lethargic, confused, responds to voice
HEENT: Dry mucous membranes
Neck: Supple
Lungs: Clear to auscultation
Heart: Tachycardic, regular rhythm
Abdomen: Soft, mild suprapubic tenderness
GU: Foley catheter in place, cloudy urine noted in bag
Extremities: Cool, delayed capillary refill

Laboratory:
WBC: 22.0 x10^9/L with 15% bands (left shift)
Lactate: 4.2 mmol/L (elevated, reference <2.0)
Creatinine: 2.1 mg/dL (elevated from baseline 1.0)
BUN: 45 mg/dL
Procalcitonin: 8.5 ng/mL (markedly elevated)
Urinalysis: >100 WBCs, positive nitrites, positive leukocyte esterase
Blood cultures: Pending (2 sets drawn)
Urine culture: Pending

Assessment and Plan:
72-year-old male with indwelling catheter presenting with sepsis, likely urosepsis given cloudy urine, positive UA, and suprapubic tenderness. Meets SIRS criteria (fever, tachycardia, tachypnea, elevated WBC) and has hypotension with elevated lactate indicating septic shock. Initiated aggressive IV fluid resuscitation, broad-spectrum antibiotics (meropenem given history of resistant organisms), and will monitor closely in ICU.
"""
}


def get_sample_note(case_name: str = "pneumonia_case") -> str:
    """Get a sample clinical note by name"""
    return SAMPLE_NOTES.get(case_name, SAMPLE_NOTES["pneumonia_case"])


def list_cases():
    """List available sample cases"""
    return list(SAMPLE_NOTES.keys())


if __name__ == "__main__":
    print("Available clinical cases:")
    for i, case in enumerate(list_cases(), 1):
        print(f"{i}. {case}")
    
    print("\nSample note (pneumonia_case):")
    print("-" * 60)
    print(get_sample_note("pneumonia_case")[:500] + "...")
