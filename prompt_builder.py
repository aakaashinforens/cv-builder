def build_prompt(user_data, raw_text=None):
    schema = """
{
  "full_name": "",
  "contact": {
    "location": "",
    "email": "",
    "phone": "",
    "linkedin": ""
  },
  "sections": {
    "Professional Statement": "",
    "Work Experience": [
      {
        "title": "",
        "company": "",
        "location": "",
        "dates": "",
        "responsibilities": []
      }
    ],
    "Education": [
      {
        "degree": "",
        "field": "",
        "institution": "",
        "dates": "",
        "result": ""
      }
    ],
    "Skills": [],
    "Projects": [],
    "Certificates": []
    // Additional sections (like Languages, Positions of Responsibility) can appear here
  }
}
"""

    if raw_text:
        prompt = f"""
You are an expert CV parser and formatter.
Extract structured information from the following CV text.

⚠️ Rules:
- Return ONLY valid JSON in the schema below.
- If Professional Statement is missing, generate a concise professional summary suitable for the target country: {user_data.get('target_country', '')}.
- If any new sections exist in the CV (e.g., Languages, Positions of Responsibility), include them in JSON.
- If information is missing, leave the field empty, do not fabricate.
- Respect the JSON structure exactly as shown.

Schema:
{schema}

CV Text:
\"\"\" 
{raw_text}
\"\"\"
"""
    else:
        # For new workflow
        prompt = f"""
You are an expert CV generator. Use the provided information to create a professional CV.

⚠️ Rules:
- Return ONLY valid JSON in the schema below.
- Generate a Professional Statement based on user data if missing.
- Respect the JSON structure exactly as shown.
- If information is missing, leave the field empty, do not fabricate.

Schema:
{schema}

User Data:
{user_data}
"""

    return prompt
