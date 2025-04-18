import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

template = """
Analyze the following unstructured business document and extract the following information:

1. Module Functionalities
2. Use Cases
3. Key Stakeholders
4. Risks or Limitations
5. Timelines or Priorities

Format your answer in JSON format with the following structure:

{{
  "modules": [
    {{
      "name": "Module Name",
      "functionality": "Short explanation"
    }}
  ],
  "use_cases": [
    "Use case 1",
    "Use case 2"
  ],
  "stakeholders": [
    {{
      "role": "Stakeholder Role",
      "responsibility": "Brief responsibility"
    }}
  ],
  "risks": [
    "Risk 1",
    "Risk 2"
  ],
  "timeline_priority": [
    {{
      "module": "Module Name",
      "priority": "High/Medium/Low",
      "expected_timeline": "Timeframe (e.g., Q3 2025)"
    }}
  ]
}}

Text:
\"\"\"
{text}
\"\"\"
"""

def analyze_document_with_genai(text):
    temp = template.format(text=text)
    prompt = (
        "You are a document analysis assistant designed to extract module functionality "
        "and use case details from unstructured business documents. Read the following "
        "unstructured business document and extract structured information about module "
        "functionalities and use cases and Present it clearly.\n\n"
        f"{temp}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"