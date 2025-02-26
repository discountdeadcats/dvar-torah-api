from fastapi import FastAPI, HTTPException
import random
import uvicorn
import threading
from pydantic import BaseModel
from storage import storage, counter, save_storage  # Import storage and save function
import requests


app = FastAPI()

# Lock to prevent race conditions when modifying storage
storage_lock = threading.Lock()

def sefariaCalendar():
    response = requests.get("https://www.sefaria.org/api/calendars", headers={"Accept": "application/json"})
    response_json = response.json()
    return response_json

@app.get("/test")
def test():
    return {"message": sefariaCalendar()}





@app.get("/parsha", description="Returns the weekly parsha.")
def parsha():
    # Look specifically for parashat_hashavua in the calendar items
    calendar_items = sefariaCalendar()['calendar_items']
    for item in calendar_items:
        if item['title']['en'] == 'Parashat Hashavua':
            parasha_ref = item['ref'] 
            parasha_name = item['displayValue']['en']
    
    return {"parsha": parasha_name}

class InputData(BaseModel):
    text: str

@app.post("/add", description="Adds a new Dvar Torah to storage.")
async def add_entry(data: InputData):
    global counter
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    with storage_lock:
        counter += 1  # Increment key
        storage[counter] = data.text  # Add new entry
        save_storage()  # Save updated dictionary to file

    return {"message": "Added successfully", "id": counter, "content": data.text}
# Credit of the divrei Torah goes to https://torah.org/learning/dvartorah/
# The divrei Torah are from the parshas of the Torah

@app.get("/learn", description="Returns a random Dvar Torah.")
async def learn():
    with storage_lock:
        # Get a list of keys that have content
        filled_keys = [k for k, v in storage.items() if v.strip()]

        if not filled_keys:
            raise HTTPException(status_code=404, detail="No divrei Torah available")

        # Pick a random key from the filled entries
        random_key = random.choice(filled_keys)

    return {"id": random_key, "content": storage[random_key]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)