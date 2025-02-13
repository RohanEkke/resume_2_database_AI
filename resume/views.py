from django.shortcuts import render
from google import genai
import re
import json
import os
from dotenv import load_dotenv
from .models import UserProfile
from .get_text import check_file_type


def extract_json_from_text(text):
    """Extract JSON content from text."""
    try:
        # Find all JSON-like structures in the response
        json_candidates = re.findall(r'{.*?}', text, re.DOTALL)
        
        # Check if there are multiple JSON blocks
        for candidate in json_candidates:
            try:
                return json.loads(candidate)  # Return the first valid JSON
            except json.JSONDecodeError:
                continue  # Try the next one if this candidate is not valid
        
        raise ValueError("No valid JSON content found.")
    
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return None


def clean_multiline_values(data):
    """Clean multiline values in the extracted JSON."""
    return {
        key: re.sub(r'[\n\t\u00a0\u2013]+', ' ', value) if isinstance(value, str) else value
        for key, value in data.items()
    }


def save_json_to_file(data, file_name):
    """Save cleaned JSON data to a file."""
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"JSON file '{file_name}' created successfully!")


def Extract(request):
    file_path = "Resumes/Jagan S Iyer PM.docx"
    resume_text = check_file_type(file_path)

    question_to_ask = f"""
    TEXT: ```{resume_text}```
    TASK 1:
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
    If any of the field is empty then type there "NO".
    Return the result in valid JSON format, as follows:

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

    """

    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("GEMINI_AIP_KEY")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=question_to_ask)
        response_text = response.text
        print(response_text)
    except Exception as e:
        return render(request, 'home.html', {'error': f"API request failed: {str(e)}"})

    # Extract and clean JSON from response
    json_data = extract_json_from_text(response_text)
    if not json_data:
        return render(request, 'home.html', {'error': "No valid JSON content found in response."})

    cleaned_data = clean_multiline_values(json_data)
    save_json_to_file(cleaned_data, "cleaned_data.json")

    if all(value == "NO" for value in cleaned_data.values()):
        context = {'error': "The file is neither a valid document nor contains a resume."}
    else:
        profile = UserProfile.objects.create(
            name=cleaned_data.get('Name'),
            email=cleaned_data.get('Email'),
            phone=cleaned_data.get('Phone'),
            location=cleaned_data.get('Location'),
            experience=cleaned_data.get('Experience'),
            education=cleaned_data.get('Education'),
            certificates=cleaned_data.get('Certificates'),
            skills=cleaned_data.get('Skills'),
            description=cleaned_data.get('Description'),
            projects=cleaned_data.get('Projects')
        )
        context = {
            'message': f"User profile for {profile.name} created successfully!",
            'response_textt': response_text
        }

    return render(request, 'home.html', context)
