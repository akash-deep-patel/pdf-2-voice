from fastapi import FastAPI, Query, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
import os

# Add these imports for file reading
from PyPDF2 import PdfReader
import docx2txt

app = FastAPI()

class ConvertRequest(BaseModel):
    elevenlabs_api_key: str
    text: str

@app.post("/convert_to_audio")
async def convert_to_audio(request: ConvertRequest):
    try:
        filename = f"audio_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("audios", filename)
        os.makedirs("audios", exist_ok=True)
        elevenlabs = ElevenLabs(
            api_key=request.elevenlabs_api_key,
        )

        audio = elevenlabs.text_to_speech.convert(
            text=request.text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        save(audio, filepath)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail="Audio file could not be created")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during audio conversion: {str(e)}")
    return FileResponse(filepath, media_type="audio/mpeg", filename=filename)

@app.post("/convert_file_to_audio")
async def convert_file_to_audio(
    elevenlabs_api_key: str = Query(...),
    file: UploadFile = File(...)
):
    try:
        # Save uploaded file temporarily
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}_{file.filename}")
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Extract text based on file type
        #multimodel content handling in pdf and docx is not supported
        if file.filename.lower().endswith(".pdf"):
            reader = PdfReader(temp_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file.filename.lower().endswith(".docx"):
            text = docx2txt.process(temp_path)
        else:
            os.remove(temp_path)
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and DOCX are supported.")

        os.remove(temp_path)

        # Reuse the audio conversion logic
        filename = f"audio_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("audios", filename)
        os.makedirs("audios", exist_ok=True)
        elevenlabs = ElevenLabs(
            api_key=elevenlabs_api_key,
        )

        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        save(audio, filepath)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail="Audio file could not be created")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during file to audio conversion: {str(e)}")
    return FileResponse(filepath, media_type="audio/mpeg", filename=filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)