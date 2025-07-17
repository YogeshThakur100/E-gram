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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = regularEnv.get_template('namuna9All.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        template = regularEnv.get_template('namuna9AllPG2.html')
        villageId = requestData.get("villageID")

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = regularEnv.get_template('namuna9Gen.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = regularEnv.get_template('namuna9GenPG2.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = regularEnv.get_template('namuna9Pani.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = regularEnv.get_template('namuna9PaniPG2.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = regularEnv.get_template('namuna9Vasuli1.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = regularEnv.get_template('namuna9Vasuli2.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request: Request):
    try:
        requestData = await request.json()
        villageId = requestData.get('villageID')
        template = regularEnv.get_template('namuna9Vasuli3.html')
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")
        data = response.json()
        if not isinstance(data, list):
            data = [data]
        context = {
            'data': data,
            'gramPanchayat': data[0].get('gramPanchayat', '') if data else '',
            'village': data[0].get('village', '') if data else '',
            'taluka': data[0].get('taluka', '') if data else '',
            'jilha': data[0].get('jilha', '') if data else '',
            'yearFrom': data[0].get('yearFrom', '') if data else '',
            'yearTo': data[0].get('yearTo', '') if data else '',
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
        }
        rendered_html = template.render(**context)
        os.makedirs(static_dir, exist_ok=True)
        output_path = os.path.join(static_dir, 'output.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        return JSONResponse(status_code=200, content={"success": True, "message": "Output file is created", "data": {}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "message": f"Error: {str(e)}", "data": {}})

@router.post('/sutsaha/namuna9All')
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = SutSahaEnv.get_template('namuna9AllSutSaha.html')

        # Call API
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = SutSahaEnv.get_template('namuna9GenSutSaha.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniEnv.get_template('namuna9AllVisheshPain.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniEnv.get_template('namuna9AllPG2VisheshPain.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniEnv.get_template('namuna9GenVisheshPain.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniEnv.get_template('namuna9GenPG2VisheshPain.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniEnv.get_template('namuna9PaniVisheshPain.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniEnv.get_template('namuna9PaniPG2VisheshPain.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniEnv.get_template('namuna9Vasuli1VisheshPain.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniEnv.get_template('namuna9Vasuli2VisheshPain.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniSafaiEnv.get_template('namuna9AllVisheshPaniSafai.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniSafaiEnv.get_template('namuna9AllPG2VisheshPaniSafai.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniSafaiEnv.get_template('namuna9GenVisheshPaniSafai.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniSafaiEnv.get_template('namuna9GenPG2VisheshPaniSafai.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniSafaiEnv.get_template('namuna9Vasuli1VisheshPaniSafai.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")
        
        
        data = response.json()
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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        villageId = requestData.get("villageID")
        template = visheshPaniSafaiEnv.get_template('namuna9Vasuli2VisheshPaniSafai.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_records_by_village/{villageId}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()
        

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
            'removeDhakit': requestData.get('removeDhakit', ''),
            'removeChalu': requestData.get('removeChalu', ''),
            'removeYekun': requestData.get('removeYekun', ''),
            'removePurnaYekun': requestData.get('removePurnaYekun', ''),
            'removePaniZero': requestData.get('removePaniZero', ''),
            'removeZeroTax': requestData.get('removeZeroTax', ''),
            'totalPrint': requestData.get('totalPrint', ''),
            'namuna9Based': requestData.get('namuna9Based', ''),
            'selectedVillage': requestData.get('selectedVillage', ''),
            'selectedYear': requestData.get('selectedYear', ''),
            'villageID': requestData.get('villageID', ''),
            'year': requestData.get('year', ''),
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