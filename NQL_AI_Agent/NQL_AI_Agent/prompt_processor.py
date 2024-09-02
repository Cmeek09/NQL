# NQL_AI_Agent/prompt_processor.py

import os
import re
from NQL_AI_Agent.modules.db import PostgresManager
from NQL_AI_Agent.modules import llm

SQL_DELIMITER = "---------"
POSTGRES_TABLE_DEFINITIONS_CAP_REF = "TABLE_DEFINITIONS"
RESPONSE_FORMAT_CAP_REF = "RESPONSE_FORMAT"

# Load environment variables
DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def process_prompt(prompt):
    prompt = f"Generate the postgres SQL query to fulfill the following request: {prompt}. "

    with PostgresManager() as db:
        db.connect_with_url(DB_URL)

        table_definitions = db.get_table_definitions_for_prompt()

        # Guardrails
        prompt = llm.add_cap_ref(
            prompt,
            f"Use these {POSTGRES_TABLE_DEFINITIONS_CAP_REF} to satisfy the database query.",
            POSTGRES_TABLE_DEFINITIONS_CAP_REF,
            table_definitions,
        )

        prompt = llm.add_cap_ref(
            prompt,
            f"\n\nRespond in this format {RESPONSE_FORMAT_CAP_REF}. Replace the text between <> with its request. I need to be able to easily parse the sql query from your response.",
            RESPONSE_FORMAT_CAP_REF,
            f"{SQL_DELIMITER}\n<sql query exclusively as raw text>\n{SQL_DELIMITER}"
        )

        prompt_response = llm.prompt(prompt)

        match = re.search(f"{SQL_DELIMITER}\n(.+){SQL_DELIMITER}", prompt_response, re.DOTALL)
        if match:
            sql_query = match.group(1).replace('\n', ' ').strip()
            result = db.run_sql(sql_query)
            return {
                'result': result,
                'sql': sql_query
            }
        else:
            return {"error": "SQL delimiter not found in the response."}
