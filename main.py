from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from namuna8 import namuna8_apis
from namuna9 import namuna9_apis
from certificates import birth_certificate_apis, death_certificate_apis, birthdeath_unavailability_apis, resident_certificate_apis, family_certificate_apis, toilet_certificate_apis, no_objection_certificate_apis, no_benefit_certificate_apis, life_certificate_apis, good_conduct_certificate_apis, niradhar_certificate_apis
from namuna8.recordresponses import property_record_response

# Import database components and models
from database import engine, Base
from namuna8 import namuna8_model
from namuna9 import namuna9_model
from certificates import birth_certificate_model
from namuna8.ReportCreationUsingJinja import namuna8Print
from fastapi.staticfiles import StaticFiles
from namuna8.mastertab.mastertabapis import router as mastertab_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(namuna8_apis.router)
app.include_router(namuna9_apis.router)
app.include_router(birth_certificate_apis.router)
app.include_router(death_certificate_apis.router)
app.include_router(birthdeath_unavailability_apis.router)
app.include_router(resident_certificate_apis.router)
app.include_router(family_certificate_apis.router)
app.include_router(toilet_certificate_apis.router)
app.include_router(no_objection_certificate_apis.router)
app.include_router(no_benefit_certificate_apis.router)
app.include_router(life_certificate_apis.router)
app.include_router(good_conduct_certificate_apis.router)
app.include_router(niradhar_certificate_apis.router)
app.include_router(property_record_response.router, prefix="/namuna8/recordresponses")
app.include_router(namuna8Print.router , prefix="/namuna8/print")
app.include_router(mastertab_router)
# --- Auto-register routers in E-gram submodules ---
import importlib
import pkgutil
import sys

api_packages = [
    "namuna8",
    "namuna9",
    "certificates"
]

for package_name in api_packages:
    try:
        package = importlib.import_module(package_name)
        for _, modname, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package_name}.{modname}")
            if hasattr(module, "router"):
                print(f"[Auto-register] Including router from {package_name}.{modname}")
                app.include_router(module.router)
    except Exception as e:
        print(f"[Auto-register] Skipped {package_name}: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to E-gram Panchayat API"}
