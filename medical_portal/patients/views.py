from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, DocumentUploadForm
from .models import Document, TestResult
from .forms import BloodCountForm
from .models import BloodCount
import csv

from django.http import HttpResponse
# Normal ranges for blood test components
NORMAL_RANGES = {
    'RBC': (4.7, 6.1),   # million cells/mcL
    'WBC': (4.0, 11.0),  # thousand cells/mcL
    'Hemoglobin': (13.8, 17.2), # g/dL
    'Platelets': (150, 450), # thousand/mcL
    'Hematocrit': (1.2, 2.1),  # million cells/mcL

}

# Disease indicators (example: anemia)
DISEASE_INDICATORS = {
    'Anemia': {
        'Hemoglobin': (0, 13.8)  # Hemoglobin level lower than 13.8 g/dL might indicate anemia
    },
}

def home(request):
    return render(request, 'patients/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'patients/register.html', {'form': form})


@login_required
def test_results(request):
    test_results = TestResult.objects.filter(patient=request.user.patient)
    return render(request, 'patients/test_results.html', {'test_results': test_results})

@login_required
def upload_blood_count(request):

    if request.method == 'POST':
        form = BloodCountForm(request.POST, request.FILES)
        if form.is_valid():
            blood_count = form.save(commit=False)
            blood_count.patient = request.user
            blood_count.save()
            return redirect('view_blood_counts')
    else:
        form = BloodCountForm()
    return render(request, 'patients/upload_blood_count.html', {'form': form})


@login_required
def view_blood_count_file(request, blood_count_id):
    blood_count = get_object_or_404(BloodCount, id=blood_count_id)
    file_path = blood_count.file.path

    # Read the CSV file and extract data
    table_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            table_data.append(row)

    return render(request, 'patients/view_blood_count_file.html', {
        'blood_count': blood_count,
        'table_data': table_data
    })

@login_required
def view_blood_counts(request):

    blood_counts = BloodCount.objects.all()
    return render(request, 'patients/view_blood_counts.html', {'blood_counts': blood_counts})

@login_required
def file_explanation(request, blood_count_id):
    blood_count = get_object_or_404(BloodCount, id=blood_count_id)
    # English explanation
    explanation_en = """
    This file contains a comprehensive blood count (CBC) report for the patient. 
    A CBC is a blood test used to evaluate your overall health and detect a wide range of disorders, including anemia, infection, and many other diseases.

    Key components of this test include:
    - **Red Blood Cell (RBC) Count**: Measures the number of red blood cells in your blood, which carry oxygen.
    - **White Blood Cell (WBC) Count**: Indicates the number of white blood cells, which are essential for fighting infections.
    - **Hemoglobin (Hgb)**: The protein in red blood cells that carries oxygen. Low levels can indicate anemia.
    - **Hematocrit (Hct)**: The proportion of red blood cells to the fluid component in your blood.
    - **Platelet Count**: Measures the number of platelets, which help with blood clotting.
    - **Mean Corpuscular Volume (MCV)**: Indicates the average size of your red blood cells. 
    - **Mean Corpuscular Hemoglobin (MCH)**: The average amount of hemoglobin in an individual red blood cell.
    - **Mean Corpuscular Hemoglobin Concentration (MCHC)**: The average concentration of hemoglobin in a given volume of red cells.

    The values in this file are crucial for diagnosing and monitoring various health conditions.
    """
    # Hebrew translation
    explanation_he = """
    קובץ זה מכיל דוח ספירת דם מקיפה (CBC) עבור המטופל.
    בדיקת CBC היא בדיקת דם המשמשת להערכת הבריאות הכללית שלך ולגילוי מגוון רחב של הפרעות, כולל אנמיה, זיהום ומחלות רבות אחרות.

    מרכיבי מפתח של בדיקה זו כוללים:
    - **מספר תאי דם אדומים (RBC)**: מודד את מספר תאי הדם האדומים בדם שלך, שנושאים חמצן.
    - **מספר תאי דם לבנים (WBC)**: מציין את מספר תאי הדם הלבנים, שהם חיוניים למלחמה בזיהומים.
    - **המוגלובין (Hgb)**: החלבון בתאי הדם האדומים שנושא חמצן. רמות נמוכות עשויות להצביע על אנמיה.
    - **המטוקריט (Hct)**: יחס תאי הדם האדומים לנפח הנוזל בדם.
    - **מספר טסיות (Platelet Count)**: מודד את מספר הטסיות, המסייעות בקרישת דם.
    - **נפח כדוריות דם ממוצע (MCV)**: מציין את הגודל הממוצע של תאי הדם האדומים שלך.
    - **המוגלובין ממוצע בתא דם (MCH)**: כמות ההמוגלובין הממוצעת בתא דם אדום יחיד.
    - **ריכוז המוגלובין ממוצע בתאי דם (MCHC)**: ריכוז ההמוגלובין הממוצע בנפח נתון של תאי דם אדומים.

    הערכים בקובץ זה חיוניים לאבחון ומעקב אחר מגוון של מצבים בריאותיים.
    """

    return render(request, 'patients/file_explanation.html', {
        'blood_count': blood_count,
        'explanation_en': explanation_en,
        'explanation_he': explanation_he
    })


@login_required
def analyze_blood_test(request, blood_count_id):
    blood_count = get_object_or_404(BloodCount, id=blood_count_id)
    file_path = blood_count.file.path

    # Extract blood test data from CSV
    blood_test_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify encoding
        reader = csv.DictReader(file)
        for row in reader:
            # Assume CSV headers match the component names
            blood_test_data.update(row)

    # Convert values to float for comparison
    for key in blood_test_data:
        blood_test_data[key] = float(blood_test_data[key])

    # Analyze the test data
    analysis_results = analyze_health(blood_test_data)

    return render(request, 'patients/analyze_blood_test.html', {
        'blood_count': blood_count,
        'analysis_results': analysis_results
    })

def analyze_health(test_data):
    results = []

    # Check for disease indicators
    for disease, indicators in DISEASE_INDICATORS.items():
        for component, (low, high) in indicators.items():
            if component in test_data:
                value = test_data[component]
                if value < low or value > high:
                    results.append({
                        'status': 'Potential Indicator',
                        'disease': disease,
                        'component': component,
                        'value': value,
                        'description': f"{component} level of {value} may indicate {disease}. {DISEASE_INDICATORS[disease][component]}"
                    })

    # General checks against normal ranges
    for component, (low, high) in NORMAL_RANGES.items():
        if component in test_data:
            value = test_data[component]
            if value < low:
                results.append({
                    'status': 'Below Normal Range',
                    'component': component,
                    'value': value,
                    'normal_range': f"{low}-{high}"
                })
            elif value > high:
                results.append({
                    'status': 'Above Normal Range',
                    'component': component,
                    'value': value,
                    'normal_range': f"{low}-{high}"
                })

    if not results:
        results.append({
            'status': 'Normal',
            'message': "All blood test values are within the normal ranges."
        })

    return results
