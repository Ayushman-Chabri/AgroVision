from recommender import recommend_full
from llm.generator import ask_ai

def start_app():
    district_name = input("Enter Odisha district: ")
    
    # Step 1: Get data from Loaders
    data_profile = recommend_full(district_name)

    # Step 2: Get specific user inputs
    print(f"\nFound data for {district_name}. Let's refine your plan:")
    user_context = {
        "crop_name": input("Enter crop name: "),
        "land_area": input("Enter land area (acres): "),
        "investment": input("Enter investment (rupees): "),
        "month_of_cropping": input("Enter starting month: "),
        "seed_variety": input("Enter seed variety (HYV/Normal): "),
    }

    # Step 3: Merge and Ask AI
    final_context = {**data_profile, **user_context}
    
    print("\n🌾 AgroVision is thinking...")
    advice = ask_ai(final_context)

    print("\n--- AI FARMER COPILOT ADVICE ---")
    print(advice)

if __name__ == "__main__":
    start_app()