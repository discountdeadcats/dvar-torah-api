from fastapi import FastAPI, HTTPException
import random
import uvicorn
import threading
from pydantic import BaseModel
from storage import storage, counter, save_storage  # Import storage and save function
import httpx



app = FastAPI()

# Lock to prevent race conditions when modifying storage
storage_lock = threading.Lock()

# Credit of the divrei Torah goes to https://torah.org/learning/dvartorah/
# The divrei Torah are from the parshas of the Torah



@app.get("/parsha/", description="Returns the weekly parsha.")
async def parsha():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.sefaria.org/api/calendars?diaspora=1", headers={"Accept": "application/json"})
        response_json = response.json()
    
    # Look specifically for parashat_hashavua in the calendar items
    parsha = "Unknown"
    calendar_items = response_json.get("calendar_items", [])
    for item in calendar_items:
        if item.get("category") == "parashat_hashavua" and "displayValue" in item:
            parsha = item["displayValue"]
            break
    
    return {"parsha": parsha}

class InputData(BaseModel):
    text: str

@app.post("/add/", description="Adds a new Dvar Torah to storage.")
async def add_entry(data: InputData):
    global counter
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    with storage_lock:
        counter += 1  # Increment key
        storage[counter] = data.text  # Add new entry
        save_storage()  # Save updated dictionary to file

    return {"message": "Added successfully", "id": counter, "content": data.text}

@app.get("/learn/", description="Returns a random Dvar Torah.")
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