import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pipeline')))

from utils.llm_helper import GroqLLM

prompt = """
Generate a comprehensive README.md and RUNBOOK.md for the AI-Powered Healthcare Pipeline.
README should include:
- Project Overview (Medallion Architecture)
- Setup Instructions (Dependencies)
- Usage (Running the Prefect flow)
- Project Structure

RUNBOOK should include:
- Execution steps
- Failure Handling (Missing files, null values)
- Recovery procedures

Output the README first, then the RUNBOOK, separated by a clear marker '---'.
Use Markdown formatting.
"""

llm = GroqLLM()
content = llm.generate_code(prompt)
print(content)
