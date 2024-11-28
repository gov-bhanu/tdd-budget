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
    if request.method == 'POST':
        # Get form data
        head_name = request.POST.get('head_name')
        head_type = request.POST.get('head_type')
        itdp_name = request.POST.get('itdp_name')
        soe_name = request.POST.get('soe_name')
        sanctioned_budget = request.POST.get('sanctioned_budget')
        revised_estimate = request.POST.get('revised_estimate')
        # department_code = request.POST.get('department_code')
        department_name = request.POST.get('department_name')
        scheme_name = request.POST.get('scheme_name')

        # Save the data into the database
        DataRow.objects.create(
            head_name=head_name,
            head_type=head_type,
            itdp_name=itdp_name,
            soe_name=soe_name,
            sanctioned_budget=sanctioned_budget,
            revised_estimate=revised_estimate,
            # department_code=department_code,
            department_name=department_name,
            scheme_name=scheme_name
        )
        messages.success(request, 'Data added successfully!')
        
        # Redirect to the home page or a success page
        return redirect('index')

    return render(request, 'add.html')  # Render the add form














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
