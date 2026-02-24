# JD Analyzer - AI-Powered Job Description Analysis Tool

## 📋 Project Overview

**JD Analyzer** is an intelligent web application that analyzes job descriptions using Groq AI (llama-3.3-70b-versatile model). It provides comprehensive quality assessments across five critical dimensions: **Clarity**, **Inclusivity**, **Structure**, **Tone**, and **Requirements**.

### Key Features
- **Real-time Analysis**: Instant job description evaluation powered by Groq AI
- **5-Dimension Assessment**: Detailed scoring on clarity, inclusivity, structure, tone, and requirements
- **Bias Detection**: Identifies discriminatory language and biased terminology
- **Actionable Insights**: Prioritized suggestions for improvement
- **Comprehensive Extraction**: Automatically extracts job title, seniority level, skills, and responsibilities
- **Interactive UI**: Beautiful, responsive web interface with animated progress rings

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python) |
| **AI/LLM** | Groq API (llama-3.3-70b-versatile) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Deployment** | render, Python 3.x |

---

## 📁 Project Structure

```
.
├── app.py                 # Flask application & routes
├── utils.py              # Core analysis logic with Groq integration
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version specification
├── templates/
│   ├── index.html        # Landing/input page
│   └── result.html       # Results display page
├── static/
│   └── style.css         # Comprehensive styling
└── data/
    └── biased_words.txt  # Reference data for bias detection
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Groq API key (get free at [console.groq.com](https://console.groq.com))

### Steps

1. **Clone/Navigate to project**
   ```bash
   cd /path/to/jd-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   echo "GROQ_API_KEY=gsk_your_actual_key_here" > .env
   ```

5. **Run development server**
   ```bash
   python app.py
   ```
   Access at `http://localhost:5000`

---

## 📊 Analysis Framework

### Scoring Dimensions

| Dimension | Weight | Focus Area |
|-----------|--------|-----------|
| **Clarity** | 25% | Writing precision, technical accuracy, unambiguous requirements |
| **Inclusivity** | 20% | Bias-free language, diverse team appeal, accessibility |
| **Structure** | 20% | Organization, logical flow, section completeness |
| **Tone** | 15% | Professional tone, candidate appeal, enthusiasm level |
| **Requirements** | 20% | Clarity of expectations, reasonable seniority levels, skill specificity |

### Verdict Scale
- **Excellent**: 85-100 points
- **Good**: 70-84 points
- **Fair**: 55-69 points
- **Needs Work**: 40-54 points
- **Poor**: 0-39 points

### Output JSON Structure
The analysis returns comprehensive JSON containing:
- Overall score and verdict
- Executive summary
- Per-category analysis (score, grade, summary, details)
- Extracted metadata (job title, seniority, skills)
- Issues identified with severity levels
- Actionable improvement suggestions
- Biased terms detected

---

## 🚀 How It Works

### User Flow
1. User pastes job description (min 50 characters)
2. Frontend validates and shows character count
3. Form submission triggers loading overlay
4. Backend calls Groq API with structured prompt
5. Groq analyzes JD and returns JSON assessment
6. Results rendered with animated score rings
7. User can analyze another JD or view details

### Backend Flow
```
POST /analyze
    ↓
validate_input (length check)
    ↓
analyze_jd(job_description)
    ↓
groq.chat.completions.create() with JSON response format
    ↓
json.loads(response) → results dict
    ↓
render result.html with results context
```

---

