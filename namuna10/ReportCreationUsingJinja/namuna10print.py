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
namuna10_template_dir = os.path.join(template_dir ,'Namuna10' )
static_dir = os.path.join(base_dir, 'reports')
env = Environment(loader=FileSystemLoader(namuna10_template_dir))

# API base URL
localhost = "http://127.0.0.1:8000"

@router.post('/vasuliprint')
async def prakar1(request : Request):
    try:
        # Load template
        requestDate = await request.json()
        stateDate = requestDate.get("startDate")
        endDate = requestDate.get("endDate")
        template = env.get_template('vasuliHishob.html')

        # Call API
        async with httpx.AsyncClient() as client:    
            response = await client.get(f'{localhost}/namuna8/recordresponses/property_record/1')
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
            "stateDate" : stateDate,
            "endDate" : endDate
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