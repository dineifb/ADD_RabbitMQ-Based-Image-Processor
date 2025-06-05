from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3
import os
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

app = FastAPI()

DB_PATH = os.path.join(os.path.dirname(__file__), "image_predictions.db")

# templates document   
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/predictions")
def get_predictions():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, image_name, file_path, prediction, confidence, processed_at FROM image_predictions")
        rows = cursor.fetchall()
        conn.close()
        results = [
            {
                "id": row[0],
                "image_name": row[1],
                "file_path": row[2],
                "prediction": row[3],
                "confidence": row[4],
                "processed_at": row[5],
            }
            for row in rows
        ]
        return JSONResponse(content={"predictions": results})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/predictions/{image_name}")
def get_prediction_by_image(image_name: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, image_name, file_path, prediction, confidence, processed_at FROM image_predictions WHERE image_name = ?", (image_name.lower(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            result = {
                "id": row[0],
                "image_name": row[1],
                "file_path": row[2],
                "prediction": row[3],
                "confidence": row[4],
                "processed_at": row[5],
            }
            return JSONResponse(content=result)
        else:
            return JSONResponse(status_code=404, content={"error": "Image not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/", response_class=HTMLResponse)
@app.get("/predictions/html", response_class=HTMLResponse)
def predictions_html(request: Request):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, image_name, file_path, prediction, confidence, processed_at FROM image_predictions")
        rows = cursor.fetchall()
        conn.close()
        return templates.TemplateResponse(
            "predictions.html",
            {"request": request, "predictions": rows}
        )
    except Exception as e:
        return HTMLResponse(f"<h1>Hata: {e}</h1>", status_code=500) 