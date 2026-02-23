from logic.precropping_logic.context_builder import build_context
from logic.precropping_logic.risk_analysis import analyze_crop

# -------------------------------
# DEMO TEST INPUT
# -------------------------------

region = "odisha"
district = "Cuttack"
crop_id = "groundnut"
season = "rabi"

land_area = 2          # hectares
investment = 60000     # rupees
seed_type = "hybrid"

# -------------------------------
# Load context bundle
# -------------------------------

print("🔹 Loading Context...")
context = build_context(region)
print("✅ Context Loaded Successfully\n")

# -------------------------------
# Run Layer 2 analysis
# -------------------------------

print("🔹 Running Risk + Profit Analysis...\n")

report = analyze_crop(
    crop_id=crop_id,
    district=district,
    season=season,
    context=context,
    land_area=land_area,
    investment=investment,
    seed_type=seed_type
)

# -------------------------------
# Print Output
# -------------------------------

print("\n========== LAYER 2 OUTPUT ==========\n")

if "error" in report:
    print("❌ ERROR:", report["error"])
else:
    print("Crop:", report["crop"])
    print("District:", report["district"])
    print("Confidence Score:", report["confidence"])

    print("\n--- Warnings ---")
    if report["warnings"]:
        for w in report["warnings"]:
            print("•", w)
    else:
        print("None")

    print("\n--- Suggestions ---")
    if report["suggestions"]:
        for s in report["suggestions"]:
            print("•", s)
    else:
        print("None")

    print("\n--- Seasonal Risks ---")
    if report["seasonal_risks"]:
        for r in report["seasonal_risks"]:
            print("•", r)
    else:
        print("None")

    print("\n--- Production & Finance ---")
    print("Land Area (ha):", report["land_area"])
    print("Expected Production (kg):", round(report["expected_production_kg"], 2))
    print("Expected Revenue (₹):", round(report["expected_revenue"], 2))
    print("Investment (₹):", report["investment"])
    print("Net Value (₹):", round(report["net_value"], 2))
    print("Financial Outcome:", report["financial_outcome"])

    print("\n--- Recommended Policies ---")
    if report["recommended_policies"]:
        for p in report["recommended_policies"]:
            print("•", p)
    else:
        print("None")

print("\n=====================================\n")
