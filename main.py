import uvicorn
from fastapi import FastAPI, Response
import io

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

@app.get("/suffer")
async def get_suffer():
    access_token = strava.get_access_token()
    df = strava.get_strava_df(access_token)
    
    buf = io.BytesIO()
    buf = strava.plot_suffer_score(df)

    return Response(buf.getvalue(), media_type='image/png')

if __name__ == "__main__":
    uvicorn.run("main:app", root_path="/strava", host="0.0.0.0", port=5000, reload=True)
