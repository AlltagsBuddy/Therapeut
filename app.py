from flask import Flask, request, jsonify, render_template
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from dotenv import load_dotenv
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Beispielhafte System-Prompts für verschiedene Anliegen
PROMPTS = {
    "stress": "Du bist ein einfühlsamer digitaler Therapeut. Hilf dem Nutzer mit seinem Stress umzugehen, indem du beruhigende Fragen stellst und Techniken wie Atemübungen oder Perspektivwechsel empfiehlst.",
    "einsamkeit": "Du bist ein KI-Therapeut, der Menschen unterstützt, die sich einsam fühlen. Stelle sensible Fragen, vermittle Nähe und rege zu Kontaktaufbau oder Selbstfürsorge an.",
    "antriebslosigkeit": "Als digitaler Coach hilfst du bei Antriebslosigkeit. Mach Mut, frage nach Zielen und gib kleine alltagstaugliche Aktivierungsimpulse.",
    "konflikte": "Du bist ein Mediator. Unterstütze bei emotionalen oder zwischenmenschlichen Konflikten, indem du Verständnisfragen stellst und Kommunikationshilfen gibst.",
    "reflexion": "Du bist ein reflektierender Begleiter. Stelle Fragen zum heutigen Tag, zur Stimmung, zu Herausforderungen und kleinen Erfolgen.",
    "achtsamkeit": "Führe den Nutzer durch eine kleine Achtsamkeitsübung oder eine geführte Atemtechnik, ruhig und klar erklärt.",
    "notfall": "Antworte NICHT als KI. Gib stattdessen sofort Hinweise zu echten Hilfsangeboten in akuten psychischen Krisen."
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/therapeut-app")
def app_view():
    return render_template("therapeut-app.html")

@app.route("/api/therapeut", methods=["POST"])
def api_therapeut():
    data = request.get_json()
    inhalt = data.get("inhalt", "").strip()
    kategorie = data.get("kategorie", "").strip()

    if not inhalt or not kategorie:
        return jsonify({"error": "Eingabe und Anliegen sind erforderlich."}), 400

    if kategorie == "notfall":
        return jsonify({
            "antwort": (
                "📞 Bitte suche bei akuter Belastung sofort Hilfe bei:\n"
                "- Telefonseelsorge: 0800 111 0 111 oder 0800 111 0 222 (kostenfrei & anonym)\n"
                "- Krisenchat für junge Menschen: https://krisenchat.de\n"
                "- Caritas Onlineberatung: https://www.caritas.de/hilfeundberatung/onlineberatung/"
            )
        })

    system_prompt = PROMPTS.get(kategorie, PROMPTS["reflexion"])

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": inhalt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        response = completion.choices[0].message["content"].strip()
        return jsonify({"antwort": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
