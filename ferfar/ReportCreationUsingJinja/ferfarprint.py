from jinja2 import Environment, FileSystemLoader
import os
import requests
from fastapi import APIRouter , Request
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()
# Load templates from the 'templates' folder (adjust path as needed)
# Init environment
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
template_dir = os.path.join(base_dir, 'templates')
ferfar_template_dir = os.path.join(template_dir ,'ferfar' )
static_dir = os.path.join(base_dir, 'reports')
env = Environment(loader=FileSystemLoader(ferfar_template_dir))

localhost = "http://127.0.0.1:8000"


@router.post('/prakar1')
async def prakar1():
    try:
        template = env.get_template('registerPrakar1.html')

        # # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/ferfar/recordresponses')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
    #     data = {
    #     "PN101": [
    #         {
    #         "entry_number": "001",
    #         "village": "Ramwadi",
    #         "transaction_date": "2025-01-10",
    #         "roadName": "Main Road",
    #         "propertyNumber": "PN101",
    #         "propertyDescription": "Residential Plot",
    #         "previousOwnerName": "Shyam Pawar",
    #         "currentOwnerName": "Ravi Patil",
    #         "modification_reference_remarks": "As per sale deed No. 1234",
    #         "assessment_register_entry_details": "Page 12, Resolution No. 45, Date: 2025-01-09"
    #         }
    #     ],
    #     "PN102": [
    #         {
    #         "entry_number": "002",
    #         "village": "Gadkari Nagar",
    #         "transaction_date": "2025-02-05",
    #         "roadName": "Station Road",
    #         "propertyNumber": "PN102",
    #         "propertyDescription": "Commercial Shop",
    #         "previousOwnerName": "Meena Deshmukh",
    #         "currentOwnerName": "Kiran Joshi",
    #         "modification_reference_remarks": "Gift deed dated 2025-02-01",
    #         "assessment_register_entry_details": "Page 20, Resolution No. 47, Date: 2025-02-04"
    #         },
    #         {
    #         "entry_number": "003",
    #         "village": "Gadkari Nagar",
    #         "transaction_date": "2025-02-20",
    #         "roadName": "Station Road",
    #         "propertyNumber": "PN102",
    #         "propertyDescription": "Commercial Shop",
    #         "previousOwnerName": "Kiran Joshi",
    #         "currentOwnerName": "Neha Kulkarni",
    #         "modification_reference_remarks": "Family settlement",
    #         "assessment_register_entry_details": "Page 21, Resolution No. 48, Date: 2025-02-18"
    #         }
    #     ],
    #     "PN103": [
    #         {
    #         "entry_number": "004",
    #         "village": "Jijamata Nagar",
    #         "transaction_date": "2025-03-10",
    #         "roadName": "MG Road",
    #         "propertyNumber": "PN103",
    #         "propertyDescription": "Open Land",
    #         "previousOwnerName": "Sunil Shinde",
    #         "currentOwnerName": "Suresh Gaikwad",
    #         "modification_reference_remarks": "Auction transfer",
    #         "assessment_register_entry_details": "Page 30, Resolution No. 50, Date: 2025-03-09"
    #         }
    #     ],
    #     "PN104": [
    #         {
    #         "entry_number": "005",
    #         "village": "Lokmanya Nagar",
    #         "transaction_date": "2025-04-15",
    #         "roadName": "Tilak Marg",
    #         "propertyNumber": "PN104",
    #         "propertyDescription": "Row House",
    #         "previousOwnerName": "Aarti Kale",
    #         "currentOwnerName": "Vishal Pawar",
    #         "modification_reference_remarks": "Registered sale deed",
    #         "assessment_register_entry_details": "Page 35, Resolution No. 52, Date: 2025-04-14"
    #         }
    #     ]
    # }

        # Render template
        context = {
            'data': data
        }
        rendered_html = template.render(**context)
        
        # Save output.html
        os.makedirs(static_dir, exist_ok=True)
        output_path = os.path.join(static_dir, 'output.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Output file is created",
                "data": {}
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Error: {str(e)}",
                "data": {}
            }
        )
        
@router.post('/prakar2')
async def prakar1():
    try:
        template = env.get_template('registerPrakar2.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/ferfar/recordresponses')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
    #     data = {
    #     "PN101": [
    #         {
    #         "entry_number": "001",
    #         "village": "Ramwadi",
    #         "transaction_date": "2025-01-10",
    #         "roadName": "Main Road",
    #         "propertyNumber": "PN101",
    #         "propertyDescription": "Residential Plot",
    #         "previousOwnerName": "Shyam Pawar",
    #         "currentOwnerName": "Ravi Patil",
    #         "modification_reference_remarks": "As per sale deed No. 1234",
    #         "assessment_register_entry_details": "Page 12, Resolution No. 45, Date: 2025-01-09"
    #         }
    #     ],
    #     "PN102": [
    #         {
    #         "entry_number": "002",
    #         "village": "Gadkari Nagar",
    #         "transaction_date": "2025-02-05",
    #         "roadName": "Station Road",
    #         "propertyNumber": "PN102",
    #         "propertyDescription": "Commercial Shop",
    #         "previousOwnerName": "Meena Deshmukh",
    #         "currentOwnerName": "Kiran Joshi",
    #         "modification_reference_remarks": "Gift deed dated 2025-02-01",
    #         "assessment_register_entry_details": "Page 20, Resolution No. 47, Date: 2025-02-04"
    #         },
    #         {
    #         "entry_number": "003",
    #         "village": "Gadkari Nagar",
    #         "transaction_date": "2025-02-20",
    #         "roadName": "Station Road",
    #         "propertyNumber": "PN102",
    #         "propertyDescription": "Commercial Shop",
    #         "previousOwnerName": "Kiran Joshi",
    #         "currentOwnerName": "Neha Kulkarni",
    #         "modification_reference_remarks": "Family settlement",
    #         "assessment_register_entry_details": "Page 21, Resolution No. 48, Date: 2025-02-18"
    #         }
    #     ],
    #     "PN103": [
    #         {
    #         "entry_number": "004",
    #         "village": "Jijamata Nagar",
    #         "transaction_date": "2025-03-10",
    #         "roadName": "MG Road",
    #         "propertyNumber": "PN103",
    #         "propertyDescription": "Open Land",
    #         "previousOwnerName": "Sunil Shinde",
    #         "currentOwnerName": "Suresh Gaikwad",
    #         "modification_reference_remarks": "Auction transfer",
    #         "assessment_register_entry_details": "Page 30, Resolution No. 50, Date: 2025-03-09"
    #         }
    #     ],
    #     "PN104": [
    #         {
    #         "entry_number": "005",
    #         "village": "Lokmanya Nagar",
    #         "transaction_date": "2025-04-15",
    #         "roadName": "Tilak Marg",
    #         "propertyNumber": "PN104",
    #         "propertyDescription": "Row House",
    #         "previousOwnerName": "Aarti Kale",
    #         "currentOwnerName": "Vishal Pawar",
    #         "modification_reference_remarks": "Registered sale deed",
    #         "assessment_register_entry_details": "Page 35, Resolution No. 52, Date: 2025-04-14"
    #         }
    #     ]
    # }

        # Render template
        context = {
            'data': data
        }
        rendered_html = template.render(**context)
        
        # Save output.html
        os.makedirs(static_dir, exist_ok=True)
        output_path = os.path.join(static_dir, 'output.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Output file is created",
                "data": {}
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Error: {str(e)}",
                "data": {}
            }
        )