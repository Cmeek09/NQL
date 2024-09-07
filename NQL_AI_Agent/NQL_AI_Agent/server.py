# NQL_AI_Agent/server.py

import asyncio
import websockets
import json
from decimal import Decimal
from NQL_AI_Agent.prompt_processor import process_prompt

# async def process_prompt(prompt):
#     # Return a JSON object instead of a plain string
#     response = {
#         "status": "success",
#         "message": f"Received your prompt: {prompt}"
#     }
#     return json.dumps(response)


# Custom JSON encoder for Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # or str(obj) if you prefer string representation
        return super(DecimalEncoder, self).default(obj)


async def handler(websocket, path):
    try:
        async for message in websocket:
            # Expecting message as a JSON string
            data = json.loads(message)
            prompt = data.get('prompt', '')

            # Print the received prompt to the server's console
            print(f"Server received prompt: {prompt}")

            # Process the prompt (just echo it back for now)
            result = process_prompt(prompt)

            # Send the result back to the client
            await websocket.send(json.dumps(result, cls=DecimalEncoder))

    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")

async def async_main():
    async with websockets.serve(handler, "localhost", 5000):
        print("WebSocket server started on ws://localhost:5000")
        await asyncio.Future()  # run forever

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
