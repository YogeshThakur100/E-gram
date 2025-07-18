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
certificate_template_dir = os.path.join(template_dir ,'Certificates' )
static_dir = os.path.join(base_dir, 'static')
env = Environment(loader=FileSystemLoader(certificate_template_dir))

localhost = "http://127.0.0.1:8000"

@router.post('/birth')
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        userID = requestData.get("userID")
        template = env.get_template('janma.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/certificates/birth/{userID}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

        # Render template
        if not isinstance(data, list):
            data = [data]
        rendered_html = template.render(**data[0])
        
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
        
@router.post('/death')
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        userID = requestData.get("userID")
        template = env.get_template('death.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/certificates/death/{userID}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

        # Render template
        if not isinstance(data, list):
            data = [data]
        rendered_html = template.render(**data[0])
        
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
        
@router.post('/birthdeath')
async def prakar1(request : Request):
    try:
        # Load template
        requestData = await request.json()
        userID = requestData.get("userID")
        template = env.get_template('janmndeath.html')

        # Call API
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{localhost}/certificates/birthdeath-unavailability/{userID}')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

        # Render template
        if not isinstance(data, list):
            data = [data]
        rendered_html = template.render(**data[0])
        
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