"""
JD Analyzer — Flask application
"""
import os
from flask import Flask, render_template, request
from utils import analyze_jd

app = Flask(__name__)


# ── Jinja2 Filters ──────────────────────────────────────────────────────────

def score_color(score: int) -> str:
    if score >= 90: return '#059669'
    if score >= 75: return '#0891B2'
    if score >= 60: return '#D97706'
    if score >= 40: return '#EA580C'
    return '#DC2626'


def score_class(score: int) -> str:
    if score >= 90: return 'excellent'
    if score >= 75: return 'good'
    if score >= 60: return 'fair'
    if score >= 40: return 'needs-work'
    return 'poor'


app.jinja_env.filters['score_color'] = score_color
app.jinja_env.filters['score_class'] = score_class


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    job_description = request.form.get('job_description', '').strip()

    if not job_description:
        return render_template('index.html',
                               error='Please paste a job description to analyze.',
                               prev_jd='')

    if len(job_description) < 50:
        return render_template('index.html',
                               error='Job description is too short. Please provide a complete description.',
                               prev_jd=job_description)

    results = analyze_jd(job_description)

    if 'error' in results:
        return render_template('index.html',
                               error=results['error'],
                               prev_jd=job_description)

    return render_template('result.html',
                           results=results,
                           job_description=job_description)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
