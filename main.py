import uvicorn
from fastapi import FastAPI, Response, BackgroundTasks
import io

import strava
import finance

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
async def get_suffer(btasks: BackgroundTasks):
    access_token = strava.get_access_token()
    df = strava.get_strava_df(access_token)
    
    buf = io.BytesIO()
    buf = strava.plot_suffer_score(df)
    btasks.add_task(buf.close)
    return Response(buf.getvalue(), media_type='image/png')


@app.get("/currency")
async def get_eur(btasks: BackgroundTasks):
    buf = io.BytesIO()
    buf = finance.get_eur_chart()
    
    btasks.add_task(buf.close)
    return Response(content=buf.getvalue(), media_type='image/png')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
