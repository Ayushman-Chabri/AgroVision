from .rules import (
    INITIAL_CONFIDENCE,
    W_SOIL_MISMATCH,
    W_RAINFALL_MISMATCH,
    W_TEMP_MISMATCH,
    W_TOPOGRAPHY_MISMATCH,
    W_SEASONAL_RISK,
    MIN_CONFIDENCE,
    UNIVERSAL_POLICIES,
    INSURANCE_POLICY
)


def analyze_crop(crop_id, district, season, context, land_area=1, investment=0, seed_type="local"):

    season = season.lower()

    confidence = INITIAL_CONFIDENCE
    suggestions = []
    warnings = []

    # -------------------------------
    # Load crop + location data
    # -------------------------------
    crop_data = next(
        (c for c in context["crops"]["crops"] if c["crop_id"] == crop_id),
        None
    )

    if not crop_data:
        return {"error": "Crop not found in database"}

    district_data = context["locations"]["districts"].get(district)

    if not district_data:
        return {"error": "District not found in database"}

    dominant_soil = district_data["dominant_soil"]

    # -------------------------------
    # 1. Soil Matching
    # -------------------------------
    if dominant_soil not in crop_data["suitable_soils"]:
        confidence -= W_SOIL_MISMATCH
        warnings.append("Soil type is not ideal for this crop.")

        soil_profile = context["soil"]["soil_types"].get(dominant_soil)

        if soil_profile:
            retention = soil_profile["water_retention"]

            suggestions.append(
                f"Soil water retention is {retention}. Consider irrigation or soil improvement techniques."
            )

    # -------------------------------
    # 2. Rainfall Matching 
    # -------------------------------
    rainfall_data = district_data.get("rainfall_level")

    if isinstance(rainfall_data, dict):
        region_rainfall = rainfall_data.get(season.capitalize())
    elif isinstance(rainfall_data, str):
        region_rainfall = rainfall_data
    else:
        region_rainfall = None

    if region_rainfall != crop_data["rainfall_range"]:
        confidence -= W_RAINFALL_MISMATCH
        warnings.append("Rainfall level mismatch detected.")

        if region_rainfall == "low":
            suggestions.append("Arrange irrigation support (PMKSY scheme recommended).")

    # -------------------------------
    # 3. Temperature Matching
    # -------------------------------
    if crop_data["temperature_pref"] not in district_data["temperature_band"]:
        confidence -= W_TEMP_MISMATCH
        warnings.append("Temperature conditions may not be optimal.")

    # -------------------------------
    # 4. Topography Matching
    # -------------------------------
    topo = district_data["land_topography"]

    if topo not in crop_data["topography"]:
        confidence -= W_TOPOGRAPHY_MISMATCH
        warnings.append("Topography mismatch: crop may face growth stress.")

    # -------------------------------
    # 5. Seasonal Risk Check
    # -------------------------------
    season_risks = context["weather"]["season_profiles"][season]["common_risks"]

    if season_risks:
        confidence -= W_SEASONAL_RISK
        warnings.append("Seasonal risks exist in this region.")

    confidence = max(confidence, MIN_CONFIDENCE)

    # ---------------------------------
    # 6. Profit Estimation 
    # ---------------------------------

    # Yield estimation from crop data
    base_yield = crop_data.get("base_yield_per_hectare", 0)

    seed_multiplier = crop_data.get(
        "seed_variety_multiplier", {}
    ).get(seed_type, 1)

    # Soil fertility modifier
    soil_profile = context["soil"]["soil_types"].get(dominant_soil, {})
    fertility_level = soil_profile.get("fertility_level", "moderate")

    fertility_map = {
        "high": 1.1,
        "moderate": 1.0,
        "low": 0.85
    }

    fertility_modifier = fertility_map.get(fertility_level, 1)

    climate_modifier = confidence / 100

    adjusted_yield = (
        base_yield
        * fertility_modifier
        * seed_multiplier
        * climate_modifier
    )

    total_production = adjusted_yield * land_area

    # -------------------------------
    # Price Prediction
    # -------------------------------
    price_data = context["prices"]["crops"].get(crop_id)

    if price_data:
        recent_prices = price_data["pre"][-3:]

        if len(recent_prices) == 3:
            predicted_price = (
                recent_prices[2] * 0.5 +
                recent_prices[1] * 0.3 +
                recent_prices[0] * 0.2
            )
        else:
            predicted_price = sum(recent_prices) / len(recent_prices)
    else:
        predicted_price = 0

    revenue = total_production * (predicted_price / 100)

    net_value = revenue - investment

    if net_value > 0:
        financial_outcome = "Profit"
    elif net_value < 0:
        financial_outcome = "Loss"
    else:
        financial_outcome = "Break-even"
    

        # ---------------------------------
    # 7. Policy Recommendation Logic
    # ---------------------------------

    applicable_policies = []

    # 1. If investment is high → recommend subsidy schemes
    if investment > 50000:
        applicable_policies.append("Agriculture Investment Subsidy Scheme")

    # 2. If confidence is low → recommend crop insurance
    if confidence < 60:
        applicable_policies.append(INSURANCE_POLICY)

    # 3. If seasonal risks exist → insurance mandatory suggestion
    if season_risks:
        applicable_policies.append("Pradhan Mantri Fasal Bima Yojana")

    # 4. If rainfall mismatch low → irrigation scheme
    if region_rainfall == "low":
        applicable_policies.append("Pradhan Mantri Krishi Sinchayee Yojana")

    # 5. Always available policies
    applicable_policies.extend(UNIVERSAL_POLICIES)

    applicable_policies = list(set(applicable_policies))

    # -------------------------------
    # Final Return
    # -------------------------------

    return {
        "crop": crop_data["display_name"],
        "district": district,
        "confidence": confidence,
        "warnings": warnings,
        "suggestions": suggestions,
        "seasonal_risks": season_risks,

        "land_area": land_area,
        "expected_production_kg": total_production,
        "expected_revenue": revenue,
        "investment": investment,
        "net_value": net_value,
        "financial_outcome": financial_outcome,

        "recommended_policies": applicable_policies
    }