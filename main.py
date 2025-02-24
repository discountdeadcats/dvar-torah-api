from fastapi import FastAPI
import random
import uvicorn

app = FastAPI()

dvar_torah = {
    1: """Foundations For Jewish Learning: A Final Solution

If we could go back in time and prevent the first murder of history what a contribution that would be. Even if we could go back and learn the lesson of the first murder of history what a gift that would be for humanity. In this century alone, more people have been killed by governments and in war than the entire population of the world at the time of the Roman conquest of Israel, more than one hundred million people....""",
    
    2: """Now it came to pass at the end of days, that Kayin brought of the fruit of the soil an offering to HASHEM. And Hevel he too brought of the firstborn of his flocks and of their fattest, and HASHEM turned to Hevel and to his offering, but to Kayin and to his offering He did not turn... (Breishis 4:2-5)...""",
    
    3: """The opening words of the Torah are too often misread, "In the beginning G-d created the heavens and the earth." That statement would imply that the Torah is communicating cosmology, as a science text book, and is interested in satisfying our curiosity about the order of creation...""",
    
    4: "",  # Space for future dvar Torah
    
    5: "",  # Space for future dvar Torah
    
    6: "",  # Space for future dvar Torah
    
    7: "",  # Space for future dvar Torah
    
    8: "",  # Space for future dvar Torah
    
    9: "",  # Space for future dvar Torah
    
    10: ""  # Space for future dvar Torah
}

@app.get("/learn", description="Returns a random dvar Torah")
def learn():
    # Get a list of keys that have content
    filled_keys = [k for k, v in dvar_torah.items() if v.strip()]
    
    if not filled_keys:
        return {"error": "No divrei Torah available"}
        
    # Pick a random key from the filled entries
    random_key = random.choice(filled_keys)
    return {"id": random_key, "content": dvar_torah[random_key]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)