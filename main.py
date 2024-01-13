import uvicorn
from fastapi import FastAPI, Response, BackgroundTasks
import io

import strava
import finance

app = FastAPI()

# https://fastapi.tiangolo.com/advanced/behind-a-proxy/
# root_path = "/ludw"

# bez przedrostka -> funkcje implementowane bezpośrednio w main.py
# s -> strava.py
#   /s/suffer
#   /s/flash
# f -> finance.py
#   /f/currency


@app.get("/health")
async def get_server_health():
    return {"success": True, "message": "ludw strava server running"}

@app.get("/s/flash")
async def get_flash():
    access_token = strava.get_access_token()
    df = strava.get_strava_df(access_token)
    
    return {
        "success": True,
        "message": strava.get_flash(df)
    }

@app.get("/s/suffer")
async def get_suffer(btasks: BackgroundTasks):
    access_token = strava.get_access_token()
    df = strava.get_strava_df(access_token)
    
    buf = io.BytesIO()
    buf = strava.plot_suffer_score(df)
    btasks.add_task(buf.close)
    return Response(buf.getvalue(), media_type='image/png')


@app.get("/f/currency")
async def get_eur(btasks: BackgroundTasks):
    buf = io.BytesIO()
    buf = finance.get_cur_chart()
    
    btasks.add_task(buf.close)
    return Response(content=buf.getvalue(), media_type='image/png')


if __name__ == "__main__":
    uvicorn.run("main:app", root_path="/ludw", host="0.0.0.0", port=5001, reload=True)
