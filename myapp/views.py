from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import DataRow
from django.contrib import messages

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
                row.kinnaur = kinnaur
                row.lahaul = lahaul
                row.spiti = spiti
                row.pangi = pangi
                row.bharmaur = bharmaur

                # Set the revised estimate as the new sanctioned budget
                # row.sanctioned_budget = revised_estimate  # Updated to use revised estimate as sanctioned budget
                row.revised_estimate = revised_estimate + in_divisible  # Ensure revised estimate is also saved
                row.save()  # Save the updated row

                return JsonResponse({'status': 'success', 'message': 'Revised estimate updated and sanctioned budget set.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Row not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DataRow

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
                department_code = row["department_code"]
                department_name = row["department_name"]
                head_name = row["head_name"]
                scheme_name = row["scheme_name"]
                soe_name = row["soe_name"]
                sanctioned_budget = float(row["sanctioned_budget"])
                in_divisible = float(row["in_divisible"]) if row.get("in_divisible") else None
                kinnaur = float(row["kinnaur"]) if row.get("kinnaur") else None
                lahaul = float(row["lahaul"]) if row.get("lahaul") else None
                spiti = float(row["spiti"]) if row.get("spiti") else None
                pangi = float(row["pangi"]) if row.get("pangi") else None
                bharmaur = float(row["bharmaur"]) if row.get("bharmaur") else None

                try:
                    # Create or update the DataRow
                    data, created = DataRow.objects.update_or_create(
                        unique_search=f"{department_code}-{department_name}-{scheme_name}-{head_name}-{soe_name}",
                        defaults={
                            "department_code": department_code,
                            "department_name": department_name,
                            "head_name": head_name,
                            "scheme_name": scheme_name,
                            "soe_name": soe_name,
                            "sanctioned_budget": sanctioned_budget,
                            "in_divisible": in_divisible,
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
        department_code = request.POST.get('department_code')
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
            department_code=department_code,
            department_name=department_name,
            scheme_name=scheme_name
        )
        messages.success(request, 'Data added successfully!')
        
        # Redirect to the home page or a success page
        return redirect('index')

    return render(request, 'add.html')  # Render the add form
