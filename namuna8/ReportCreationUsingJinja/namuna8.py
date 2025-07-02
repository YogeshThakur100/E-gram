from jinja2 import Environment, FileSystemLoader
import os
import requests

# Load templates from the 'templates' folder (adjust path as needed)

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__) , '../../'))

template_dir = os.path.join(base_dir , 'templates')
static_dir = os.path.join(base_dir , 'static')
namuna8_dir = os.path.join(template_dir , 'Namuna8')
print(namuna8_dir)
env = Environment(loader=FileSystemLoader(namuna8_dir))

# Load the template file
template = env.get_template('singlePrint1.html')

response = requests.get('http://127.0.0.1:8000/namuna8/recordresponses/property_record/465')
data = response.json()
# print(data)
# Render template with data
rendered_html = template.render(data)

# Save the output to an HTML file
output_path = os.path.join(static_dir, 'output.html')  # or any public folder
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(rendered_html)
