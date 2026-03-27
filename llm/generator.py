from .ollama_client import generate_response
from .prompt_templates import build_prompt
from .response_formatter import format_response
from .memory import save_to_json, get_last_record

def ask_ai(combined_ctx: dict):
    # 1. Pull past history for this district
    history = get_last_record(combined_ctx['district'])
    
    # 2. Build the prompt with data + history
    prompt = build_prompt(combined_ctx, history)

    # 3. Get AI response
    raw_response = generate_response(prompt)

    # 4. Save this session to memory
    save_to_json(combined_ctx)

    return format_response(raw_response)