from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from collections import defaultdict
from .models import DataRow
from django.db.models import Sum
import json
import csv
from django.core.serializers import serialize
from django.db.models import F
from django.utils.dateparse import parse_date
from django.utils.timezone import now, timedelta


def index(request):
    """Render the main page."""
    return render(request, 'index.html')  # Render the main template

def fetch_data(request):
    """Fetch all data to populate the table."""
    data = list(DataRow.objects.values())
    return JsonResponse({'status': 'success', 'data': data})









@csrf_exempt
def update_revised_estimate(request):
    """Update the revised estimate and set it as the new Sanctioned Budget in the database."""
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            unique_search = body.get('uniqueSearch')
            revised_estimate = body.get('revisedEstimate')
            in_divisible = body.get('in_divisible')            
            divisible = body.get('divisible')
            kinnaur = body.get('kinnaur')
            lahaul = body.get('lahaul')
            spiti = body.get('spiti')
            pangi = body.get('pangi')
            bharmaur = body.get('bharmaur')

            if not unique_search or revised_estimate is None:
                return JsonResponse({'status': 'error', 'message': 'Missing required data'})

            # Find the row matching the unique_search value
            row = DataRow.objects.filter(unique_search=unique_search).first()
            if row:
                # Update the row with the new values
                row.in_divisible = in_divisible
                row.divisible = divisible
                row.kinnaur = kinnaur
                row.lahaul = lahaul
                row.spiti = spiti
                row.pangi = pangi
                row.bharmaur = bharmaur

                # revised estimate = in_divisible + divisible
                row.revised_estimate = in_divisible + divisible  # Ensure revised estimate is also saved
                # Set the last_change_date to the current time
                row.last_change_date = now()
                row.save()  # Save the updated row

                return JsonResponse({'status': 'success', 'message': 'Revised estimate updated and sanctioned budget set.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Row not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})















def import_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "File is not a valid CSV.")
            return redirect("import_csv")

        try:
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                # department_code = row["department_code"]
                department_name = row["department_name"]
                head_name = row["head_name"]
                scheme_name = row["scheme_name"]
                soe_name = row["soe_name"]
                sanctioned_budget = float(row["sanctioned_budget"])
                revised_estimate = float(row["in_divisible"]) if row.get("in_divisible") else None
                in_divisible = float(row["in_divisible"]) if row.get("in_divisible") else None                
                divisible = float(row["in_divisible"]) if row.get("divisible") else None
                kinnaur = float(row["kinnaur"]) if row.get("kinnaur") else None
                lahaul = float(row["lahaul"]) if row.get("lahaul") else None
                spiti = float(row["spiti"]) if row.get("spiti") else None
                pangi = float(row["pangi"]) if row.get("pangi") else None
                bharmaur = float(row["bharmaur"]) if row.get("bharmaur") else None

                try:
                    # Create or update the DataRow
                    data, created = DataRow.objects.update_or_create(
                        # unique_search=f"{department_code}-{department_name}-{scheme_name}-{head_name}-{soe_name}",
                        unique_search=f"{department_name}-{scheme_name}-{head_name}-{soe_name}",
                        defaults={
                            # "department_code": department_code,
                            "department_name": department_name,
                            "head_name": head_name,
                            "scheme_name": scheme_name,
                            "soe_name": soe_name,
                            "sanctioned_budget": sanctioned_budget,
                            "revised_estimate": revised_estimate,
                            "in_divisible": in_divisible,
                            "divisible": divisible,
                            "kinnaur": kinnaur,
                            "lahaul": lahaul,
                            "spiti": spiti,
                            "pangi": pangi,
                            "bharmaur": bharmaur,
                        },
                    )
                except Exception as e:
                    messages.error(request, f"Row error: {row}. Error: {str(e)}")
            
            messages.success(request, "CSV file imported successfully!")
            return redirect("/")
        
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return redirect("import_csv")

    return render(request, "import.html")











def add_data(request):
    """Render the add form and handle new data submission."""
    departments = ["Agriculture", "Allopathy", "Animal Husbandry", "Art & Culture", "Ayurveda", "Border Area Development Programme", "Child Welfare", "Civil Supplies", "Co-operation", 
    "Dairy and Milk Supply", "Elementary Education", "Energy", "Excise and Taxation", "Fisheries", "Fire Services", "Forest", "General Administration", "Health and Family Welfare", 
    "Horticulture", "Hortriculture", "Industry and Minerals", "Irrigation and Flood Control", "Judiciary", "Labour and Employment", "Medical Education and Research", 
    "Mountaineering and Allied Sports", "Police Housing", "Planning Department", "Prison Department", "Public Works", "Rural Development", "Science Technology and Environment", 
    "Secondary Education", "Special Nutrition Programme", "Social Welfare", "Town and Country Planning", "Transport", "University and Higher Education", "Vigilance Department", "Water Supply", 
    "Water Supply and Sewerage", "Welfare of SCs/STs/OBCs", "Women and Child Development", "Youth Services and Sports"]

    soes = [
    "01-Salaries", "02-Wages", "03-Travel Expenses", "05-Office Expenses", "06-Medical Reimbursement", "07-Rent Rates and Taxes", "09-Advertising and Publicity", "10-Hospitality and Entertainment Expenses", 
    "12-Professional & Special Services", "15-Training", "16-Social Security Pension", "20-Other Charges", "21-Maintenance", "29-Compensations", "30-Motor Vehicles (Outsourced Vehicles/Pol/Repairs)", 
    "31-Machinery and Equipment", "33-Materials and Supplies", "37-Major Works", "40-Scholarships Stipends and Concessions", "40-Scholarships- Stipends and Concessions", 
    "41-Grants-in-Aid General (Salary)", "42-Grants-in-Aid General (Non-Salary)", "42-Grants-in-Aid General (Non-Salary) SDG New_add", "43-Investment", "44-Grants-in-Aid for Capital Assets", 
    "44-Grants-in-Aid for Capital Assets SDG New_add", "48-Loans", "62-Subsidy on Interests", "63-Subsidy", "64-Transfer Expenses", "65-Outsourcing Charges", "79-Suspense"]


    if request.method == 'POST':
        # Get form data from request
        department_name = request.POST.get('department_name')
        head_name = request.POST.get('head_name')
        scheme_name = request.POST.get('scheme_name')
        soe_name = request.POST.get('soe_name')
        sanctioned_budget = request.POST.get('sanctioned_budget')
        in_divisible = request.POST.get('in_divisible', 0)  # Default to 0 if empty
        kinnaur = request.POST.get('kinnaur', 0)  # Default to 0 if empty
        lahaul = request.POST.get('lahaul', 0)  # Default to 0 if empty
        spiti = request.POST.get('spiti', 0)  # Default to 0 if empty
        pangi = request.POST.get('pangi', 0)  # Default to 0 if empty
        bharmaur = request.POST.get('bharmaur', 0)  # Default to 0 if empty

        # Save the data into the database
        DataRow.objects.create(
            department_name=department_name,
            head_name=head_name,
            scheme_name=scheme_name,
            soe_name=soe_name,
            sanctioned_budget=sanctioned_budget,
            in_divisible=in_divisible,
            kinnaur=kinnaur,
            lahaul=lahaul,
            spiti=spiti,
            pangi=pangi,
            bharmaur=bharmaur
        )
        messages.success(request, 'Data added successfully!')

        # Redirect to the home page or a success page
        return redirect('index')  # Make sure 'index' is the correct URL name

    return render(request, 'add.html', {'departments': departments, 'soes': soes})













# View to render the final_report page
def final_report_view(request):
    return render(request, 'final_report.html')

# API to fetch data for the final_report table, including totals for each head_name and department_name
def fetch_data(request):
    try:
        # Fetch all data from the database
        data = DataRow.objects.all().values(
            'department_name',
            'head_name',
            'scheme_name',
            'soe_name',
            'sanctioned_budget',
            'revised_estimate',
            'in_divisible',
            'divisible',
            'kinnaur',
            'lahaul',
            'spiti',
            'pangi',
            'bharmaur',
        )

        # Convert the QuerySet to a list of dictionaries
        data_list = list(data)

        # Initialize total dictionaries for department and head name
        department_totals = defaultdict(lambda: defaultdict(float))
        head_name_totals = defaultdict(lambda: defaultdict(float))

        # Function to safely convert to float, treating None as 0.0
        def safe_float(value):
            return float(value) if value is not None else 0.0

        # Calculate totals for each department and head_name
        for row in data_list:
            department_totals[row['department_name']]['sanctioned_budget'] += safe_float(row['sanctioned_budget'])
            department_totals[row['department_name']]['revised_estimate'] += safe_float(row['revised_estimate'])
            department_totals[row['department_name']]['in_divisible'] += safe_float(row['in_divisible'])
            department_totals[row['department_name']]['divisible'] += safe_float(row['divisible'])
            department_totals[row['department_name']]['kinnaur'] += safe_float(row['kinnaur'])
            department_totals[row['department_name']]['lahaul'] += safe_float(row['lahaul'])
            department_totals[row['department_name']]['spiti'] += safe_float(row['spiti'])
            department_totals[row['department_name']]['pangi'] += safe_float(row['pangi'])
            department_totals[row['department_name']]['bharmaur'] += safe_float(row['bharmaur'])
            
            head_name_totals[row['head_name']]['sanctioned_budget'] += safe_float(row['sanctioned_budget'])
            head_name_totals[row['head_name']]['revised_estimate'] += safe_float(row['revised_estimate'])
            head_name_totals[row['head_name']]['in_divisible'] += safe_float(row['in_divisible'])
            head_name_totals[row['head_name']]['divisible'] += safe_float(row['divisible'])
            head_name_totals[row['head_name']]['kinnaur'] += safe_float(row['kinnaur'])
            head_name_totals[row['head_name']]['lahaul'] += safe_float(row['lahaul'])
            head_name_totals[row['head_name']]['spiti'] += safe_float(row['spiti'])
            head_name_totals[row['head_name']]['pangi'] += safe_float(row['pangi'])
            head_name_totals[row['head_name']]['bharmaur'] += safe_float(row['bharmaur'])

        # Return data along with totals
        return JsonResponse({
            'status': 'success',
            'data': data_list,
            'department_totals': department_totals,
            'head_name_totals': head_name_totals
        }, safe=False)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)






# View to render the supplementary report page
def supplementary_report_view(request):
    return render(request, 'supplementary_report.html')

# API to fetch supplementary report data, including totals for each head_name
def fetch_supplementary_data(request):
    try:
        # Fetch all data from the database
        data = DataRow.objects.all().values(
            'department_name',
            'head_name',
            'scheme_name',
            'soe_name',
            'sanctioned_budget',
            'revised_estimate',
            'excess',
            'surrender',
            'variation',
        )

        # Convert the QuerySet to a list of dictionaries
        data_list = list(data)

        # Initialize total dictionary for head_name
        head_name_totals = defaultdict(lambda: defaultdict(float))

        # Function to safely convert to float, treating None as 0.0
        def safe_float(value):
            return float(value) if value is not None else 0.0

        # Calculate totals for each head_name
        for row in data_list:
            head_name_totals[row['head_name']]['sanctioned_budget'] += safe_float(row['sanctioned_budget'])
            head_name_totals[row['head_name']]['revised_estimate'] += safe_float(row['revised_estimate'])
            head_name_totals[row['head_name']]['excess'] += safe_float(row['excess'])
            head_name_totals[row['head_name']]['surrender'] += safe_float(row['surrender'])
            head_name_totals[row['head_name']]['variation'] += safe_float(row['variation'])

        return JsonResponse({
            'status': 'success',
            'data': data_list,
            'head_name_totals': head_name_totals,
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })









def revision_report_view(request):
    return render(request, 'revision_report.html')

from collections import defaultdict

def fetch_revision_data(request):
    try:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        rows = DataRow.objects.exclude(sanctioned_budget=F('revised_estimate'))

        if start_date:
            rows = rows.filter(last_change_date__gte=parse_date(start_date))
        if end_date:
            rows = rows.filter(last_change_date__lte=parse_date(end_date))

        data = rows.values(
            'department_name',
            'head_name',
            'scheme_name',
            'soe_name',
            'sanctioned_budget',
            'revised_estimate',
            'excess',
            'surrender',
            'last_change_date',
        )

        data_list = list(data)

        head_name_totals = defaultdict(lambda: defaultdict(float))

        def safe_float(value):
            return float(value) if value is not None else 0.0

        for row in data_list:
            head_name_totals[row['head_name']]['sanctioned_budget'] += safe_float(row['sanctioned_budget'])
            head_name_totals[row['head_name']]['revised_estimate'] += safe_float(row['revised_estimate'])
            head_name_totals[row['head_name']]['excess'] += safe_float(row['excess'])
            head_name_totals[row['head_name']]['surrender'] += safe_float(row['surrender'])

        return JsonResponse({
            'status': 'success',
            'data': data_list,
            'head_name_totals': head_name_totals,
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        })
