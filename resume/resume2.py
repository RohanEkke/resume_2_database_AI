from google import genai
import docx2txt
import re
import json

text = docx2txt.process("Resumes/Siddhartha Gandroju.docx")
cleaned_text = "\n".join([line for line in text.splitlines() if line.strip()])
print(cleaned_text)

questionToAsk = f"""
From the provided text, extract the following fields and return them in JSON format. Ensure the output is valid JSON with proper escaping of special characters and correct syntax. I don't want any comments in json file. Follow these rules:
- `Name`: Extract the candidate's name.
- `Email`: Extract the candidate's email address.
- `Phone`: Extract the candidate's mobile phone number.
- `Location`: Extract the candidate's current location (city and state).
- `Experience`: Extract the total years of experience in years as a string (e.g., "6 years")
- `Education`: Extract the candidate's educational qualifications.
- `Certificates`: Extract any certifications or relevant achievements. Leave it empty if none are found.
- `Skills`: Extract all technical and professional skills, as listed or implied (e.g., languages, frameworks, tools, methodologies).
- `Description`: Extract the professional summary, if available.
- `Projects`: Extract any mentioned projects. These can be explicitly labeled as projects or derived from significant achievements or contributions under job responsibilities.

Return the result in JSON format, as follows:

{{
  "Name": "",
  "Email": "",
  "Phone": "",
  "Location": "",
  "Experience": "",
  "Education": "",
  "Certificates": "",
  "Skills": "",
  "Description": "",
  "Projects": "",
}}
Text: {cleaned_text}
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("GEMINI_AIP_KEY")

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=questionToAsk
)
text = response.text
print(text)

json_content = re.search(r'{(.*)}', text, re.DOTALL).group(0)

# Convert to a dictionary
data = json.loads(json_content)

# Save the dictionary as a JSON file
with open("data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file created successfully!")




from .models import UserProfile  # Replace 'your_app' with your app name

# Load the JSON file
with open('path/to/your/json_file.json', 'r') as file:
    data = json.load(file)

# Create a new UserProfile object and save it to the database
profile = UserProfile.objects.create(
    name=data.get('Name'),
    email=data.get('Email'),
    phone=data.get('Phone'),
    location=data.get('Location'),
    experience=data.get('Experience'),
    education=data.get('Education'),
    certificates=data.get('Certificates'),
    skills=data.get('Skills'),
    description=data.get('Description'),
    projects=data.get('Projects')
)

print(f"User profile for {profile.name} created successfully!")
