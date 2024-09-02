# NQL_AI_Agent/main.py

import dotenv
import os
import re
import asyncio
from NQL_AI_Agent.prompt_processor import process_prompt
from NQL_AI_Agent.modules.charts import bar_chart

dotenv.load_dotenv()

def main():
    while True:
        user_input = input("Enter a prompt (type 'shut_down' to exit): ")

        if user_input == 'shut_down':
            print("Shutting down...")
            break

        # Run the async process_prompt in the event loop
        response = asyncio.run(process_prompt(user_input))

        if 'error' in response:
            print(f"Error: {response['error']}")
        else:
            print("\n\n======== AI AGENT RESPONSE ========")
            print(response['result'])

            # Ask the user if they want to plot a bar chart
            plot_chart = input("Do you want to plot a bar chart of the result? (yes/no): ").lower()
            if plot_chart == 'yes':
                bar_chart(response['result'])

if __name__ == "__main__":
    main()
