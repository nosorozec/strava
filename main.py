import uvicorn
from fastapi import FastAPI
import strava

app = FastAPI()

@app.get("/health")
async def get_server_health():
    return {"success": True, "message": "ludw strava server running"}

@app.get("/flash")
async def get_flash():
    access_token = strava.get_access_token()
    df = strava.get_strava_df(access_token)
    
    return {
        "success": True,
        "message": strava.get_flash(df)
    }

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)