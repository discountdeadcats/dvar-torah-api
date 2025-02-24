# Torah Learning API

## Overview
A FastAPI-based API that serves random Divrei Torah (Torah teachings) and Jewish learning materials.

## Current Features
- Random Dvar Torah endpoint (`/learn`)
- Three pre-loaded Divrei Torah about Creation and Kayin & Hevel
- Easy-to-use REST API interface
- FastAPI automatic documentation

## Setup and Installation
To get started with the API:

1. Clone the repository
```bash
git clone https://github.com/discountdeadcats/dvar-torah-api
```

2. Install required packages
```bash
pip install fastapi uvicorn
```

3. Run the server
```bash
uvicorn main:app --reload
```

4. Access the API:
- API documentation: `http://localhost:8000/docs`
- Get random Dvar Torah: `http://localhost:8000/learn`

## Code Example
```python
from fastapi import FastAPI
import random

app = FastAPI(title="Dvar Torah API")

dvar_torah = {
    1: """Foundations For Jewish Learning: A Final Solution...""",
    2: """Now it came to pass at the end of days...""",
    3: """The opening words of the Torah..."""
}

@app.get("/learn")
async def learn():
    filled_keys = [k for k, v in dvar_torah.items() if v.strip()]
    random_key = random.choice(filled_keys)
    return {"id": random_key, "content": dvar_torah[random_key]}
```

## Planned Features

### Short Term
* Add POST endpoint to contribute new Divrei Torah
* Add Daf Yomi content and daily updates
* Add source filtering (Chumash, Prophets, Talmud)
* Input validation for new submissions
* Basic authentication for content submission

### Long Term
* Weekly Parsha insights
* Multiple language support (Hebrew, English)
* Categories for different topics (Mussar, Halacha)
* User accounts for personalized learning
* API key implementation for security
* Connection to popular Jewish text APIs (Sefaria)

## API Endpoints (Planned)
```markdown
GET /learn - Get random Dvar Torah
POST /submit - Submit new Dvar Torah
GET /daf-yomi - Get today's Daf Yomi
GET /parsha - Get insights on the weekly Torah portion
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Content Note
All Torah content should be treated with appropriate respect. Please verify sources and attributions when contributing new material.

## License
GNU General Public License


---
*This project is meant to help spread Torah learning and understanding. Please use and share the content appropriately.*
