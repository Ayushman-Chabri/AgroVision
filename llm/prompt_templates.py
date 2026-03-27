def build_prompt(ctx: dict):
    # Find the specific data for the crop the user entered
    current_crop_data = next(
        (item for item in ctx.get('recommended_crops', []) 
         if item['crop'].lower() == ctx['crop_name'].lower()), 
        None
    )

    # Extract specific diseases/techniques if found, else use defaults
    diseases = current_crop_data['diseases'] if current_crop_data else "General regional pests"
    techniques = current_crop_data['techniques'] if current_crop_data else "Standard farming practices"

    return f"""
You are AgroVision — an expert Agricultural Consultant for Odisha. 
Use the provided data to give practical, low-cost advice to a farmer.

### SITE DATA:
- District: {ctx['district']}
- Soil: {ctx['soil_type']}
- Annual Rainfall: {ctx['avg_rainfall_mm']}mm

### FARMER'S PLAN:
- Crop: {ctx['crop_name']} ({ctx['seed_variety']} variety)
- Area: {ctx['land_area']} Acres
- Budget: ₹{ctx['investment']}
- Starting Month: {ctx['month_of_cropping']}

### TECHNICAL DATA:
- Local Risks: {diseases}
- Suggested Methods: {techniques}

### YOUR ADVICE (Keep it short and numbered):
1. Suitability: Is {ctx['crop_name']} good for {ctx['soil_type']} soil?
2. Action Plan: What should they do in {ctx['month_of_cropping']}?
3. Efficiency: How to use {techniques} within a ₹{ctx['investment']} budget?
4. Protection: How to avoid {diseases}?

Answer:"""