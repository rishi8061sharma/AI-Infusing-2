
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parent / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"



PRICES = {
    "shoes": 799,
    "hat": 399,
    "bag": 1420,
    "shorts": 1299,
    "pants": 1699,
}

def get_price(item):
    print(f"🔧 Tool called: get_price({item})")
    price = PRICES.get(item.lower())
    return f"₹{price}" if price is not None else f"Price not found for {item}"

tools = [{
    "type": "function",
    "function": {
        "name": "get_price",
        "description": "Get the price of a shop item.",
        "parameters": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "The item name"
                }
            },
            "required": ["item"],
            "additionalProperties": False
        }
    }
}]

def agent(user_message):
    messages = [{"role": "user", "content": user_message}]

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content or ""

        for call in msg.tool_calls:
            if call.function.name != "get_price":
                result = "Unknown tool"
            else:
                args = json.loads(call.function.arguments)
                result = get_price(args["item"])

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return "I couldn't complete the request after several tool calls."

if __name__ == "__main__":
    print(agent("How much are the shoes?"))
    print(agent("Hi! What can you help with?"))
