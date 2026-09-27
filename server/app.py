from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# ── Replace with your real API key from aistudio.google.com ──
API_KEY = "TU_API_KEY_AQUI"

client = genai.Client(
    api_key=API_KEY,
    http_options={"api_version": "v1"},
)

MODEL = "models/gemini-3.8-flash"

def call_gemini(prompt: str) -> str:
    resp = client.models.generate_content(model=MODEL, contents=prompt)
    return resp.text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/refactor', methods=['POST'])
def refactor_code():
    data = request.json
    legacy_code = data.get('code', '')
    target_lang = data.get('language', 'TypeScript')

    if not legacy_code:
        return jsonify({'error': 'No enviaste código'}), 400

    try:
        # ── Step 1: Refactor the code ──────────────────────────────────────
        code_prompt = f"""You are Bob, an expert code refactoring assistant.
Refactor the following legacy code into clean, modern {target_lang}.
Apply best practices: strong typing, modern syntax, idiomatic patterns, and remove anti-patterns.
IMPORTANT: Respond with ONLY the raw refactored code — no markdown fences, no backticks, no explanations, no comments about the changes. Just the code.

Legacy Code:
{legacy_code}"""

        refactored_result = call_gemini(code_prompt)

        # Strip markdown fences if the model includes them anyway
        if refactored_result.startswith("```"):
            lines = refactored_result.split('\n')
            if len(lines) > 2:
                refactored_result = '\n'.join(lines[1:-1]).strip()

        # ── Step 2: Generate a meaningful explanation ──────────────────────
        explain_prompt = f"""You are Bob, a code refactoring expert.
A developer just refactored the following legacy code into {target_lang}.

Original code:
{legacy_code}

Refactored code:
{refactored_result}

Write a concise, developer-friendly explanation (3-5 sentences) of the key improvements made:
what anti-patterns were removed, what modern features were applied, and why the new code is better.
Be specific — mention actual constructs used (e.g. arrow functions, const/let, type annotations, etc.).
Write in plain English. No bullet points, no markdown, no headers."""

        explanation = call_gemini(explain_prompt)

        return jsonify({
            'refactored_code': refactored_result,
            'explanation': explanation
        })

    except Exception as e:
        error_msg = str(e)
        print(f"[BobRefactor ERROR] {error_msg}")
        # Return the real error to the frontend so it's visible during development
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)