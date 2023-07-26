import uvicorn, os
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )


@app.get("/download_excel/{file_name}/")
async def download_excel(file_name: str) -> FileResponse:
    headers = {'Content-Disposition': f'attachment; filename="{file_name}"'}
    excel_file_path = os.path.join("excel", file_name)
    return FileResponse(
        path=excel_file_path,
        headers=headers,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.post("/upload_excel/")
async def upload_excel_file(file: UploadFile = File(...)) -> dict:
    file_save_path = os.path.join("excel", file.filename)
    with open(file_save_path, "wb") as f:
        f.write(await file.read())
    return {"message": "File uploaded and saved successfully"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
