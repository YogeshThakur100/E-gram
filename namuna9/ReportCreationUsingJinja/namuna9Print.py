from jinja2 import Environment, FileSystemLoader
import os
import requests
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()
# Load templates from the 'templates' folder (adjust path as needed)
# Init environment
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
template_dir = os.path.join(base_dir, 'templates')
template_dir = os.path.join(template_dir ,'Namuna9' )
namuna9_template_regualar_dir = os.path.join(template_dir ,'Regular' )
namuna9_template_sutsaha_dir = os.path.join(template_dir ,'Sut Saha' )
namuna9_template_viseshpani_dir = os.path.join(template_dir ,'Vishesh Pani' )
namuna9_template_viseshpaniSafai_dir = os.path.join(template_dir ,'VisheshPani with Safai Tax' )
static_dir = os.path.join(base_dir, 'static')
regularEnv = Environment(loader=FileSystemLoader(namuna9_template_regualar_dir))
SutSahaEnv = Environment(loader=FileSystemLoader(namuna9_template_sutsaha_dir))
visheshPaniEnv = Environment(loader=FileSystemLoader(namuna9_template_viseshpani_dir))
visheshPaniSafaiEnv = Environment(loader=FileSystemLoader(namuna9_template_viseshpaniSafai_dir))

localhost = "http://127.0.0.1:8000"

@router.post('/regular/namuna9All')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9All.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/regular/namuna9AllPG2')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9AllPG2.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/regular/namuna9Gen')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9Gen.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/regular/namuna9GenPG2')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9GenPG2.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
    
@router.post('/regular/namuna9Pani')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9Pani.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/regular/namuna9PaniPG2')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9PaniPG2.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/regular/namuna9Vasuli1')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9Vasuli1.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/regular/namuna9Vasuli2')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9Vasuli2.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/regular/namuna9Vasuli3')
def prakar1():
    try:
        # Load template
        template = regularEnv.get_template('namuna9Vasuli3.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
    
@router.post('/sutsaha/namuna9All')
def prakar1():
    try:
        # Load template
        template = SutSahaEnv.get_template('namuna9AllSutSaha.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/sutsaha/namuna9Gen')
def prakar1():
    try:
        # Load template
        template = SutSahaEnv.get_template('namuna9GenSutSaha.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPani/namuna9All')
def prakar1():
    try:
        # Load template
        template = visheshPaniEnv.get_template('namuna9AllVisheshPain.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPani/namuna9AllPG2')
def prakar1():
    try:
        # Load template
        template = visheshPaniEnv.get_template('namuna9AllPG2VisheshPain.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPani/namuna9Gen')
def prakar1():
    try:
        # Load template
        template = visheshPaniEnv.get_template('namuna9GenVisheshPain.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPani/namuna9GenPG2')
def prakar1():
    try:
        # Load template
        template = visheshPaniEnv.get_template('namuna9GenPG2VisheshPain.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPani/namuna9Pani')
def prakar1():
    try:
        # Load template
        template = visheshPaniEnv.get_template('namuna9PaniVisheshPain.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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

@router.post('/visheshPani/namuna9PaniPG2')
def prakar1():
    try:
        # Load template
        template = visheshPaniEnv.get_template('namuna9PaniPG2VisheshPain.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPani/namuna9Vasuli1')
def prakar1():
    try:
        # Load template
        template = visheshPaniEnv.get_template('namuna9Vasuli1VisheshPain.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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

@router.post('/visheshPani/namuna9Vasuli2')
def prakar1():
    try:
        # Load template
        template = visheshPaniEnv.get_template('namuna9Vasuli2VisheshPain.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPaniSafai/namuna9All')
def prakar1():
    try:
        # Load template
        template = visheshPaniSafaiEnv.get_template('namuna9AllVisheshPaniSafai.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPaniSafai/namuna9AllPG2')
def prakar1():
    try:
        # Load template
        template = visheshPaniSafaiEnv.get_template('namuna9AllPG2VisheshPaniSafai.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPaniSafai/namuna9Gen')
def prakar1():
    try:
        # Load template
        template = visheshPaniSafaiEnv.get_template('namuna9GenVisheshPaniSafai.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPaniSafai/namuna9GenPG2')
def prakar1():
    try:
        # Load template
        template = visheshPaniSafaiEnv.get_template('namuna9GenPG2VisheshPaniSafai.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPaniSafai/namuna9Vasuli1')
def prakar1():
    try:
        # Load template
        template = visheshPaniSafaiEnv.get_template('namuna9Vasuli1VisheshPaniSafai.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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
        
@router.post('/visheshPaniSafai/namuna9Vasuli2')
def prakar1():
    try:
        # Load template
        template = visheshPaniSafaiEnv.get_template('namuna9Vasuli2VisheshPaniSafai.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        # data = [
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "स्वत:",
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # },
        #             {
        #     "id": "1",
        #     "srNo": 1,
        #     "propertyNumber": "जरीचेवखडकाचे",
        #     "propertyDescription": "दगड सिमेंट चुना अर्ध पक्के घर, आर सी सी",
        #     "gramPanchayat": "गट नं 6",
        #     "village": "गट नं 6",
        #     "taluka": "null",
        #     "jilha": "null",
        #     "yearFrom": 2024,
        #     "yearTo": 2027,
        #     "photoURL": "null",
        #     "QRcodeURL": "null",
        #     "total_arearinfoot": 9879.0,
        #     "totalareainmeters": 917.79,
        #     "occupantName": "श्री रामराव पि.तत्तवराव पावडे"  ,
        #     "aadharNumber": "",
        #     "ownerName": "श्री रामराव पि.तत्तवराव पावडे",
        #     "roadName": "",
        #     "cityWardGatNumber": "",
        #     "areaEast": 133.5,
        #     "areaWest": 133.5,
        #     "areaNorth": 74.5,
        #     "areaSouth": 73.5,
        #     "totalArea": 9879.0,
        #     "boundaryEast": "पांडुरंग बाबाराव",
        #     "boundaryWest": "रस्ता वि. द. शाळा",
        #     "boundaryNorth": "बाजरीचे व खडकाचे",
        #     "boundarySouth": " खडकाचे",
        #     "removeLightHealthTax": "true",
        #     "applyCleaningTax": "true",
        #     "applyToiletTax": "false",
        #     "taxNotApplicable": "false",
        #     "khaliJaga": [
        #         {
        #             "constructiontype": "खाली जागा",
        #             "length": 8538.0,
        #             "width": 1,
        #             "year": 2025,
        #             "rate": "null",
        #             "floor": "null",
        #             "usage": "null",
        #             "capitalValue": 541133,
        #             "houseTax": 0,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": "null",
        #             "totalkhalijagaareainfoot": 8538.0,
        #             "totalkhalijagaareainmeters": 793.21
        #         }
        #     ],
        #     "constructionType": [
        #         {
        #             "type": "दगड सिमेंट चुना अर्ध पक्के घर",
        #             "length": 494.0,
        #             "width": 1.0,
        #             "year": "1999",
        #             "rate": 14137.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 406,
        #             "depreciation_rate": 70,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 0.75
        #         },
        #         {
        #             "type": "आर सी सी",
        #             "length": 847.0,
        #             "width": 1.0,
        #             "year": "2005",
        #             "rate": 17424.0,
        #             "floor": "तळमजला",
        #             "usage": "निवासी",
        #             "capitalValue": 541133,
        #             "houseTax": 541,
        #             "depreciation_rate": 75,
        #             "usageBasedBuildingWeightageFactor": 1,
        #             "taxRates": 1.0
        #         }
        #     ],
        #     "waterFacility1": "सामान्य पाणीकर",
        #     "waterFacility2": "सामान्य पाणीकर",
        #     "toilet": "आहे",
        #     "house": "आहे",
        #     "totalCapitalValue": 0,
        #     "totalHouseTax": 0,
        #     "housingUnit": "sqft",
        #     "lightingTax": 300,
        #     "healthTax": 300,
        #     "waterTax": 0,
        #     "cleaningTax": 300,
        #     "toiletTax": 0,
        #     "totaltax": 0,
        #     "userId": [
        #         2
        #     ],
        #     "villageId": "3",
        #     "creationAt": "2025-07-03T11:16:50.572730",
        #     "updationAt": "2025-07-03T11:16:50.572730"
        # }
        # ]
        
        # data = data * 100

        # Render template
        if not isinstance(data, list):
            data = [data]
        # Extract top-level fields from the first record
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
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