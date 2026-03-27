from loaders.soil_loader import load_soil_data
from loaders.weather_loader import load_weather_data
from loaders.region_loader import load_region_data
from loaders.disease_loader import load_disease_data
from loaders.technique_loader import load_technique_data
from loaders.validation import validate_district

def recommend_full(district):
    # 1. Load all datasets
    soil_data = load_soil_data()
    weather_data = load_weather_data()
    region_data = load_region_data()
    disease_data = load_disease_data()
    technique_data = load_technique_data()

    # 2. Validate district existence
    if not validate_district(district, soil_data):
        return None  # Return None so main.py can handle the error

    # 3. Extract Soil and Rainfall (Optimized lookups)
    soil_type = next((s["soil_type"] for s in soil_data if s["district"].lower() == district.lower()), "Unknown")
    rainfall = next((w["avg_rainfall_mm"] for w in weather_data if w["district"].lower() == district.lower()), 0)
    
    # Get initial list of recommended crops for the region
    crops = next((r["recommended_crops"] for r in region_data if r["district"].lower() == district.lower()), [])

    # 4. Enrich Crop Data with Diseases and Techniques
    crop_details = []
    for crop in crops:
        # Find diseases for this specific crop
        diseases = next(([x["name"] for x in d["common_diseases"]] 
                         for d in disease_data if d["crop"].lower() == crop.lower()), [])

        # Find techniques for this specific crop
        techniques = next((t["recommended_techniques"] 
                           for t in technique_data if t["crop"].lower() == crop.lower()), [])

        crop_details.append({
            "crop": crop,
            "diseases": diseases,
            "techniques": techniques
        })

    # 5. Return the full context dictionary
    return {
        "district": district,
        "soil_type": soil_type,
        "avg_rainfall_mm": rainfall,
        "recommended_crops": crop_details
    }