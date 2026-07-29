import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
from backend.tools import TOOLS, TOOL_MAP

load_dotenv()

app = FastAPI(title="IlIllumi PFM Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model definition
MODEL = "gpt-4o"

class ChatRequest(BaseModel):
    message: str

SYSTEM_PROMPT = """
You are IlIllumi, a sharp, authentic, and helpful personal financial AI assistant.
Answer the user's spending queries concisely and clearly based on their statement data.
Always call tools when you need transaction data. Never guess financial numbers.
"""

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.message}
        ]

        # First request to OpenAI
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Check if the model decided to call a tool
        if response_message.tool_calls:
            messages.append(response_message)  # Add model's request to conversation history

            # Execute each tool requested by the LLM
            for tool_call in response_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments or "{}")
                print(f"--- ILIllumi IS CALLING TOOL: {func_name} WITH ARGS: {func_args} ---")

                if func_name in TOOL_MAP:
                    # Execute tool
                    tool_output = TOOL_MAP[func_name](**func_args)
                    print(f"--- TOOL RETURNED: {tool_output} ---")
                    # Append tool response back to LLM context
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_output)
                    })

            # Second call to OpenAI with tool outputs included
            final_response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            return {"reply": final_response.choices[0].message.content}

        return {"reply": response_message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))