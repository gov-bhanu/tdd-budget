from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, F, Count
from django.db.models.functions import Substr, Length
from django.utils.dateparse import parse_date
from django.utils.timezone import now, timedelta
from django.core.serializers import serialize
import json
import csv
from collections import defaultdict
from .models import DataRow






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
        
        if not csv_file or not csv_file.name.endswith(".csv"):
            messages.error(request, "File is not a valid CSV.")
            return redirect("import_csv")

        try:
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            print("CSV Columns:", reader.fieldnames)

            with transaction.atomic():
                for row in reader:
                    try:
                        soe_name = row["SOE Name"].strip()
                        head_name = row["Head Name"].strip()
                        # Other fields from CSV (for new records) are:
                        department_name = row["Department Name"].strip()
                        scheme_name = row["Scheme Name"].strip()

                        # Convert numeric values, using None if empty.
                        def safe_float(value):
                            return float(value) if value and value.strip() != "" else None

                        # Values to update
                        in_divisible = safe_float(row.get("In Divisible"))
                        divisible = safe_float(row.get("Divisible"))
                        kinnaur = safe_float(row.get("Kinnaur"))
                        lahaul = safe_float(row.get("Lahaul"))
                        spiti = safe_float(row.get("Spiti"))
                        pangi = safe_float(row.get("Pangi"))
                        bharmaur = safe_float(row.get("Bharmaur"))

                        try:
                            # Try to retrieve an existing record using the unique constraint fields.
                            data_row = DataRow.objects.get(soe_name=soe_name, head_name=head_name)
                            # Update only the specified fields.
                            data_row.in_divisible = in_divisible
                            data_row.divisible = divisible
                            data_row.kinnaur = kinnaur
                            data_row.lahaul = lahaul
                            data_row.spiti = spiti
                            data_row.pangi = pangi
                            data_row.bharmaur = bharmaur
                            # Note: department_name, scheme_name, sanctioned_budget, etc. remain unchanged.
                            data_row.save()
                        except DataRow.DoesNotExist:
                            # If record doesn't exist, create a new one using all available values.
                            sanctioned_budget = safe_float(row.get("SB"))
                            DataRow.objects.create(
                                department_name=department_name,
                                head_name=head_name,
                                scheme_name=scheme_name,
                                soe_name=soe_name,
                                sanctioned_budget=sanctioned_budget,
                                in_divisible=in_divisible,
                                divisible=divisible,
                                kinnaur=kinnaur,
                                lahaul=lahaul,
                                spiti=spiti,
                                pangi=pangi,
                                bharmaur=bharmaur,
                            )
                    except KeyError as e:
                        messages.error(request, f"Missing column: {e}. Check CSV headers.")
                        return redirect("import_csv")
                    except ValueError as e:
                        messages.error(request, f"Invalid data format: {e}.")
                        return redirect("import_csv")
            
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
    "Secondary Education", "Special Nutrition Programme", "Social Welfare", "Town and Country Planning", "Transport","Tribal Development", "University and Higher Education", "Vigilance Department", "Water Supply", 
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
        )

        # Convert the QuerySet to a list of dictionaries
        data_list = list(data)

        data_list = list(data)

        # Store totals for each head
        head_name_totals = {}
        current_head = None

        # Collect the data and calculate totals
        result_data = []

        for row in data_list:
            head_name = row['head_name']
            # Initialize totals for new head if needed
            if head_name != current_head:
                if current_head:  # Add the previous head totals before the new head
                    result_data.append({
                        'head_name': f'{current_head} Total',
                        'sanctioned_budget': head_name_totals[current_head]['sanctioned_budget'],
                        'revised_estimate': head_name_totals[current_head]['revised_estimate'],
                        'excess': head_name_totals[current_head]['excess'],
                        'surrender': head_name_totals[current_head]['surrender'],
                    })

                # Reset totals for new head
                head_name_totals[head_name] = {
                    'sanctioned_budget': 0.0,
                    'revised_estimate': 0.0,
                    'excess': 0.0,
                    'surrender': 0.0,
                }

                current_head = head_name

            # Add row to result data and aggregate totals
            head_name_totals[head_name]['sanctioned_budget'] += float(row['sanctioned_budget'] or 0.0)
            head_name_totals[head_name]['revised_estimate'] += float(row['revised_estimate'] or 0.0)
            head_name_totals[head_name]['excess'] += float(row['excess'] or 0.0)
            head_name_totals[head_name]['surrender'] += float(row['surrender'] or 0.0)

            result_data.append(row)

        # Add the final total for the last head
        if current_head:
            result_data.append({
                'head_name': f'{current_head} Total',
                'sanctioned_budget': head_name_totals[current_head]['sanctioned_budget'],
                'revised_estimate': head_name_totals[current_head]['revised_estimate'],
                'excess': head_name_totals[current_head]['excess'],
                'surrender': head_name_totals[current_head]['surrender'],
            })

        return JsonResponse({
            'status': 'success',
            'data': result_data,
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        })









def revision_report_view(request):
    return render(request, 'revision_report.html')

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

        # Store totals for each head
        head_name_totals = {}
        current_head = None

        # Collect the data and calculate totals
        result_data = []

        for row in data_list:
            head_name = row['head_name']
            # Initialize totals for new head if needed
            if head_name != current_head:
                if current_head:  # Add the previous head totals before the new head
                    result_data.append({
                        'head_name': f'{current_head} Total',
                        'sanctioned_budget': head_name_totals[current_head]['sanctioned_budget'],
                        'revised_estimate': head_name_totals[current_head]['revised_estimate'],
                        'excess': head_name_totals[current_head]['excess'],
                        'surrender': head_name_totals[current_head]['surrender'],
                        'last_change_date': ''
                    })

                # Reset totals for new head
                head_name_totals[head_name] = {
                    'sanctioned_budget': 0.0,
                    'revised_estimate': 0.0,
                    'excess': 0.0,
                    'surrender': 0.0,
                }

                current_head = head_name

            # Add row to result data and aggregate totals
            head_name_totals[head_name]['sanctioned_budget'] += float(row['sanctioned_budget'] or 0.0)
            head_name_totals[head_name]['revised_estimate'] += float(row['revised_estimate'] or 0.0)
            head_name_totals[head_name]['excess'] += float(row['excess'] or 0.0)
            head_name_totals[head_name]['surrender'] += float(row['surrender'] or 0.0)

            result_data.append(row)

        # Add the final total for the last head
        if current_head:
            result_data.append({
                'head_name': f'{current_head} Total',
                'sanctioned_budget': head_name_totals[current_head]['sanctioned_budget'],
                'revised_estimate': head_name_totals[current_head]['revised_estimate'],
                'excess': head_name_totals[current_head]['excess'],
                'surrender': head_name_totals[current_head]['surrender'],
                'last_change_date': ''
            })

        return JsonResponse({
            'status': 'success',
            'data': result_data,
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        })









def final_report(request):
    # Existing data fetch logic
    data = DataRow.objects.all().values(
        'department_name', 
        'head_name', 
        'scheme_name', 
        'soe_name',
        'sanctioned_budget',
        'revised_estimate',
        'excess',
        'surrender'
    )

    # SOE and Department totals calculation
    soe_totals = {}
    department_totals = {}
    total_sanctioned_budget_soe = 0
    total_revised_estimate_soe = 0
    total_excess_soe = 0
    total_surrender_soe = 0
    total_sanctioned_budget_dept = 0
    total_revised_estimate_dept = 0
    total_excess_dept = 0
    total_surrender_dept = 0

    for row in data:
        # SOE Wise Total
        soe_name = row['soe_name']
        if soe_name not in soe_totals:
            soe_totals[soe_name] = {
                'sanctioned_budget': 0,
                'revised_estimate': 0,
                'excess': 0,
                'surrender': 0,
            }
        soe_totals[soe_name]['sanctioned_budget'] += row['sanctioned_budget']
        soe_totals[soe_name]['revised_estimate'] += row['revised_estimate']
        soe_totals[soe_name]['excess'] += row['excess'] or 0
        soe_totals[soe_name]['surrender'] += row['surrender'] or 0

        # Department Wise Total
        department_name = row['department_name']
        if department_name not in department_totals:
            department_totals[department_name] = {
                'sanctioned_budget': 0,
                'revised_estimate': 0,
                'excess': 0,
                'surrender': 0,
            }
        department_totals[department_name]['sanctioned_budget'] += row['sanctioned_budget']
        department_totals[department_name]['revised_estimate'] += row['revised_estimate']
        department_totals[department_name]['excess'] += row['excess'] or 0
        department_totals[department_name]['surrender'] += row['surrender'] or 0

    # Calculate final totals for SOE and Department
    for totals in soe_totals.values():
        total_sanctioned_budget_soe += totals['sanctioned_budget']
        total_revised_estimate_soe += totals['revised_estimate']
        total_excess_soe += totals['excess']
        total_surrender_soe += totals['surrender']

    for totals in department_totals.values():
        total_sanctioned_budget_dept += totals['sanctioned_budget']
        total_revised_estimate_dept += totals['revised_estimate']
        total_excess_dept += totals['excess']
        total_surrender_dept += totals['surrender']

    # Sort the dictionaries by keys
    sorted_soe_totals = dict(sorted(soe_totals.items()))
    sorted_department_totals = dict(sorted(department_totals.items()))

    # Group data by Head Category (first 4 characters of head_name)
    head_category_totals = (
        DataRow.objects
        .annotate(head_category=Substr('head_name', 1, 4))  # Extract first 4 characters
        .values('head_category')
        .annotate(
            sanctioned_budget=Sum('sanctioned_budget'),
            revised_estimate=Sum('revised_estimate'),
            excess=Sum('excess'),
            surrender=Sum('surrender')
        )
        .order_by('head_category')
    )
    # Calculate total values for the head_category_totals
    total_sanctioned_budget_head_category = sum(item['sanctioned_budget'] for item in head_category_totals)
    total_revised_estimate_head_category = sum(item['revised_estimate'] for item in head_category_totals)
    total_excess_head_category = sum(item['excess'] for item in head_category_totals)
    total_surrender_head_category = sum(item['surrender'] for item in head_category_totals)

    # Group data by Head Category (first 7 characters of head_name)
    head_category_totals_7 = (
        DataRow.objects
        .annotate(head_category_7=Substr('head_name', 1, 7))  # Extract first 7 characters
        .values('head_category_7')
        .annotate(
            sanctioned_budget=Sum('sanctioned_budget'),
            revised_estimate=Sum('revised_estimate'),
            excess=Sum('excess'),
            surrender=Sum('surrender')
        )
        .order_by('head_category_7')
    )

    # Group data by Head Category (first 11 characters of head_name)
    head_category_totals_11 = (
        DataRow.objects
        .annotate(head_category_11=Substr('head_name', 1, 11))  # Extract first 11 characters
        .values('head_category_11')
        .annotate(
            sanctioned_budget=Sum('sanctioned_budget'),
            revised_estimate=Sum('revised_estimate'),
            excess=Sum('excess'),
            surrender=Sum('surrender')
        )
        .order_by('head_category_11')
    )

    # Calculate totals for the first 7 characters group
    total_sanctioned_budget_head_category_7 = sum(item['sanctioned_budget'] for item in head_category_totals_7)
    total_revised_estimate_head_category_7 = sum(item['revised_estimate'] for item in head_category_totals_7)
    total_excess_head_category_7 = sum(item['excess'] for item in head_category_totals_7)
    total_surrender_head_category_7 = sum(item['surrender'] for item in head_category_totals_7)

    context = {
        'data': data,
        'soe_totals': sorted_soe_totals,
        'department_totals': sorted_department_totals,
        'total_sanctioned_budget_soe': total_sanctioned_budget_soe,
        'total_revised_estimate_soe': total_revised_estimate_soe,
        'total_excess_soe': total_excess_soe,
        'total_surrender_soe': total_surrender_soe,
        'total_sanctioned_budget_dept': total_sanctioned_budget_dept,
        'total_revised_estimate_dept': total_revised_estimate_dept,
        'total_excess_dept': total_excess_dept,
        'total_surrender_dept': total_surrender_dept,
        'head_category_totals': head_category_totals,
        'total_sanctioned_budget_head_category': total_sanctioned_budget_head_category,
        'total_revised_estimate_head_category': total_revised_estimate_head_category,
        'total_excess_head_category': total_excess_head_category,
        'total_surrender_head_category': total_surrender_head_category,
        'head_category_totals_7': head_category_totals_7,
        'head_category_totals_11': head_category_totals_11,
        'total_sanctioned_budget_head_category_7': total_sanctioned_budget_head_category_7,
        'total_revised_estimate_head_category_7': total_revised_estimate_head_category_7,
        'total_excess_head_category_7': total_excess_head_category_7,
        'total_surrender_head_category_7': total_surrender_head_category_7,
    }


    return render(request, 'final_report.html', context)





def group_summary(request):
    # Existing data fetch logic
    data = DataRow.objects.all().values(
        'department_name', 
        'head_name', 
        'scheme_name', 
        'soe_name',
        'sanctioned_budget',
        'revised_estimate',
        'excess',
        'surrender'
    )

    # SOE and Department totals calculation
    total_sanctioned_budget_soe = 0
    total_revised_estimate_soe = 0
    total_excess_soe = 0
    total_surrender_soe = 0
    total_sanctioned_budget_dept = 0
    total_revised_estimate_dept = 0
    total_excess_dept = 0
    total_surrender_dept = 0

    # Totals report by head group (C, S, A)
    head_groups = (
        DataRow.objects
        .annotate(head_name_length=Length('head_name'))
        .annotate(head_group=Substr('head_name', F('head_name_length') - 3, 4))  # Extract last 4 characters
        .values('head_group')
        .annotate(
            total_sanctioned_budget=Sum('sanctioned_budget'),
            total_revised_estimate=Sum('revised_estimate'),
            total_excess=Sum('excess'),
            total_surrender=Sum('surrender')
        )
        .order_by('head_group')
    )

    # Separate groups based on the starting letter
    group_c = [item for item in head_groups if item['head_group'].startswith('C')]
    group_s = [item for item in head_groups if item['head_group'].startswith('S')]
    group_a = [item for item in head_groups if item['head_group'].startswith('A')]

    # Final totals for all groups
    total_sanctioned_budget_a = sum(item['total_sanctioned_budget'] for item in group_a)
    total_revised_estimate_a = sum(item['total_revised_estimate'] for item in group_a)
    total_excess_a = sum(item['total_excess'] for item in group_a)
    total_surrender_a = sum(item['total_surrender'] for item in group_a)

    total_sanctioned_budget_c = sum(item['total_sanctioned_budget'] for item in group_c)
    total_revised_estimate_c = sum(item['total_revised_estimate'] for item in group_c)
    total_excess_c = sum(item['total_excess'] for item in group_c)
    total_surrender_c = sum(item['total_surrender'] for item in group_c)

    total_sanctioned_budget_s = sum(item['total_sanctioned_budget'] for item in group_s)
    total_revised_estimate_s = sum(item['total_revised_estimate'] for item in group_s)
    total_excess_s = sum(item['total_excess'] for item in group_s)
    total_surrender_s = sum(item['total_surrender'] for item in group_s)

    # Final totals for all groups (A, C, S)
    final_total_sanctioned_budget = total_sanctioned_budget_a + total_sanctioned_budget_c + total_sanctioned_budget_s
    final_total_revised_estimate = total_revised_estimate_a + total_revised_estimate_c + total_revised_estimate_s
    final_total_excess = total_excess_a + total_excess_c + total_excess_s
    final_total_surrender = total_surrender_a + total_surrender_c + total_surrender_s
    

    context = {
        'data': data,
        'total_sanctioned_budget_soe': total_sanctioned_budget_soe,
        'total_revised_estimate_soe': total_revised_estimate_soe,
        'total_excess_soe': total_excess_soe,
        'total_surrender_soe': total_surrender_soe,
        'total_sanctioned_budget_dept': total_sanctioned_budget_dept,
        'total_revised_estimate_dept': total_revised_estimate_dept,
        'total_excess_dept': total_excess_dept,
        'total_surrender_dept': total_surrender_dept,
        'group_c': group_c,
        'group_s': group_s,
        'group_a': group_a,
        'total_sanctioned_budget_a': total_sanctioned_budget_a,
        'total_revised_estimate_a': total_revised_estimate_a,
        'total_excess_a': total_excess_a,
        'total_surrender_a': total_surrender_a,
        'total_sanctioned_budget_c': total_sanctioned_budget_c,
        'total_revised_estimate_c': total_revised_estimate_c,
        'total_excess_c': total_excess_c,
        'total_surrender_c': total_surrender_c,
        'total_sanctioned_budget_s': total_sanctioned_budget_s,
        'total_revised_estimate_s': total_revised_estimate_s,
        'total_excess_s': total_excess_s,
        'total_surrender_s': total_surrender_s,
        'final_total_sanctioned_budget': final_total_sanctioned_budget,
        'final_total_revised_estimate': final_total_revised_estimate,
        'final_total_excess': final_total_excess,
        'final_total_surrender': final_total_surrender,
    }


    return render(request, 'group_summary.html', context)












def type_summary(request):
    # Fetch all data rows
    data = DataRow.objects.all()

    # Separate data by head_type
    revenue_data = data.filter(head_type='Revenue')
    capital_data = data.filter(head_type='Capital')
    loan_data = data.filter(head_type='Loan')

    # For each type (Revenue, Capital, Loan), separate by head group (C, S, A)
    def get_head_group_totals(data):
        return (
            data
            .annotate(head_group=Substr('head_name', Length('head_name') - 3, 4))  # Extract last 4 characters of head_name
            .values('head_group')
            .annotate(
                total_sanctioned_budget=Sum('sanctioned_budget'),
                total_revised_estimate=Sum('revised_estimate'),
                total_excess=Sum('excess'),
                total_surrender=Sum('surrender')
            )
            .order_by('head_group')
        )
    
    # Get totals for Revenue, Capital, Loan types
    revenue_groups = get_head_group_totals(revenue_data)
    capital_groups = get_head_group_totals(capital_data)
    loan_groups = get_head_group_totals(loan_data)

    # Group by C, S, A for each type
    def separate_groups_by_type(groups):
        group_c = [item for item in groups if item['head_group'].startswith('C')]
        group_s = [item for item in groups if item['head_group'].startswith('S')]
        group_a = [item for item in groups if item['head_group'].startswith('A')]
        return group_c, group_s, group_a

    revenue_group_c, revenue_group_s, revenue_group_a = separate_groups_by_type(revenue_groups)
    capital_group_c, capital_group_s, capital_group_a = separate_groups_by_type(capital_groups)
    loan_group_c, loan_group_s, loan_group_a = separate_groups_by_type(loan_groups)

    # Summing totals for each group (Revenue, Capital, Loan)
    def sum_totals(group):
        return {
            'sanctioned_budget': sum(item['total_sanctioned_budget'] for item in group),
            'revised_estimate': sum(item['total_revised_estimate'] for item in group),
            'excess': sum(item['total_excess'] for item in group),
            'surrender': sum(item['total_surrender'] for item in group),
        }

    revenue_totals_c = sum_totals(revenue_group_c)
    revenue_totals_s = sum_totals(revenue_group_s)
    revenue_totals_a = sum_totals(revenue_group_a)

    capital_totals_c = sum_totals(capital_group_c)
    capital_totals_s = sum_totals(capital_group_s)
    capital_totals_a = sum_totals(capital_group_a)

    loan_totals_c = sum_totals(loan_group_c)
    loan_totals_s = sum_totals(loan_group_s)
    loan_totals_a = sum_totals(loan_group_a)

    # Grand totals for each category group (C, S, A)
    final_group_c = {
        'sanctioned_budget': revenue_totals_c['sanctioned_budget'] + capital_totals_c['sanctioned_budget'] + loan_totals_c['sanctioned_budget'],
        'revised_estimate': revenue_totals_c['revised_estimate'] + capital_totals_c['revised_estimate'] + loan_totals_c['revised_estimate'],
        'excess': revenue_totals_c['excess'] + capital_totals_c['excess'] + loan_totals_c['excess'],
        'surrender': revenue_totals_c['surrender'] + capital_totals_c['surrender'] + loan_totals_c['surrender']
    }

    final_group_s = {
        'sanctioned_budget': revenue_totals_s['sanctioned_budget'] + capital_totals_s['sanctioned_budget'] + loan_totals_s['sanctioned_budget'],
        'revised_estimate': revenue_totals_s['revised_estimate'] + capital_totals_s['revised_estimate'] + loan_totals_s['revised_estimate'],
        'excess': revenue_totals_s['excess'] + capital_totals_s['excess'] + loan_totals_s['excess'],
        'surrender': revenue_totals_s['surrender'] + capital_totals_s['surrender'] + loan_totals_s['surrender']
    }

    final_group_a = {
        'sanctioned_budget': revenue_totals_a['sanctioned_budget'] + capital_totals_a['sanctioned_budget'] + loan_totals_a['sanctioned_budget'],
        'revised_estimate': revenue_totals_a['revised_estimate'] + capital_totals_a['revised_estimate'] + loan_totals_a['revised_estimate'],
        'excess': revenue_totals_a['excess'] + capital_totals_a['excess'] + loan_totals_a['excess'],
        'surrender': revenue_totals_a['surrender'] + capital_totals_a['surrender'] + loan_totals_a['surrender']
    }

    # Grand totals for all types combined
    final_total_sanctioned_budget = revenue_totals_c['sanctioned_budget'] + capital_totals_c['sanctioned_budget'] + loan_totals_c['sanctioned_budget']
    final_total_revised_estimate = revenue_totals_c['revised_estimate'] + capital_totals_c['revised_estimate'] + loan_totals_c['revised_estimate']
    final_total_excess = revenue_totals_c['excess'] + capital_totals_c['excess'] + loan_totals_c['excess']
    final_total_surrender = revenue_totals_c['surrender'] + capital_totals_c['surrender'] + loan_totals_c['surrender']


    final_total = {
    "sanctioned_budget": final_group_c["sanctioned_budget"] + final_group_s["sanctioned_budget"] + final_group_a["sanctioned_budget"],
    "revised_estimate": final_group_c["revised_estimate"] + final_group_s["revised_estimate"] + final_group_a["revised_estimate"],
    "excess": final_group_c["excess"] + final_group_s["excess"] + final_group_a["excess"],
    "surrender": final_group_c["surrender"] + final_group_s["surrender"] + final_group_a["surrender"],
}


    context = {
        'revenue_group_c': revenue_group_c,
        'revenue_group_s': revenue_group_s,
        'revenue_group_a': revenue_group_a,
        'capital_group_c': capital_group_c,
        'capital_group_s': capital_group_s,
        'capital_group_a': capital_group_a,
        'loan_group_c': loan_group_c,
        'loan_group_s': loan_group_s,
        'loan_group_a': loan_group_a,
        'revenue_totals_c': revenue_totals_c,
        'revenue_totals_s': revenue_totals_s,
        'revenue_totals_a': revenue_totals_a,
        'capital_totals_c': capital_totals_c,
        'capital_totals_s': capital_totals_s,
        'capital_totals_a': capital_totals_a,
        'loan_totals_c': loan_totals_c,
        'loan_totals_s': loan_totals_s,
        'loan_totals_a': loan_totals_a,
        'final_group_c': final_group_c,
        'final_group_s': final_group_s,
        'final_group_a': final_group_a,
        'final_total_sanctioned_budget': final_total_sanctioned_budget,
        'final_total_revised_estimate': final_total_revised_estimate,
        'final_total_excess': final_total_excess,
        'final_total_surrender': final_total_surrender,
        'final_total': final_total,
    }

    return render(request, 'type_summary.html', context)
