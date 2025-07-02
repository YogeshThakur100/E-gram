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
namuna8_template_dir = os.path.join(template_dir ,'Namuna8' )
static_dir = os.path.join(base_dir, 'static')
env = Environment(loader=FileSystemLoader(namuna8_template_dir))

# API base URL
localhost = "http://127.0.0.1:8000"

@router.post('/single_print')
def singlePrint():
    try:
        # Load template
        template = env.get_template('singlePrint1.html')

        # Call API
        response = requests.get(f'{localhost}/namuna8/recordresponses/property_record/1')
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        data = response.json()

        # Render template
        rendered_html = template.render(data)

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