# NQL_AI_Agent/server.py

import asyncio
import websockets
import json
from NQL_AI_Agent.prompt_processor import process_prompt

async def handler(websocket, path):
    try:
        async for message in websocket:
            # Expecting message as a JSON string
            data = json.loads(message)
            prompt = data.get('prompt', '')

            # Process the prompt
            response = await process_prompt(prompt)  # Await the async function

            # Send the result back to the client
            await websocket.send(json.dumps(response))

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
