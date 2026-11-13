from flask import Flask, render_template, request
import pdfplumber
import spacy
import re

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_resume(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    doc = nlp(text)

    emails = re.findall(
        r'[\w.+-]+@[\w-]+\.[\w.-]+', text
    )

    phones = re.findall(
        r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b', text
    )

    skills_list = [
        "Python", "Java", "C++", "SQL",
        "HTML", "CSS", "JavaScript",
        "Flask", "Machine Learning",
        "Data Analysis", "React"
    ]

    found_skills = [
        skill for skill in skills_list
        if skill.lower() in text.lower()
    ]

    name = "Not found"

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    return {
        "name": name,
        "email": emails[0] if emails else "Not found",
        "phone": phones[0] if phones else "Not found",
        "skills": found_skills,
        "text": text
    }


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        file = request.files.get("resume")

        if file and file.filename.lower().endswith(".pdf"):
            result = extract_resume(file)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)