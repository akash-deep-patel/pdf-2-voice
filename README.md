# PDF/Docx to Audio Converter API

This FastAPI application provides endpoints to convert text, PDF, or DOCX files into MP3 audio using the ElevenLabs API.

## Features

- **/convert_to_audio**: Convert raw text to MP3 audio.
- **/convert_file_to_audio**: Upload a PDF or DOCX file and receive an MP3 audio file of its contents.

## Requirements

- Python 3.8+
- ElevenLabs API key

### Python Dependencies

Install dependencies using:

```bash
pip install -r requirements.txt
```

**requirements.txt**
```
fastapi
uvicorn
pydantic
elevenlabs
PyPDF2
docx2txt
```

## Usage

### 1. Start the API server

```bash
uvicorn audios.app:app --reload
```

### 2. Endpoints

#### Convert Text to Audio

- **POST** `/convert_to_audio`
- **Body (JSON):**
  ```json
  {
    "api_key": "YOUR_ELEVENLABS_API_KEY",
    "text": "Your text to convert"
  }
  ```
- **Response:** MP3 audio file

#### Convert PDF/DOCX File to Audio

- **POST** `/convert_file_to_audio`
- **Form Data:**
  - `api_key`: Your ElevenLabs API key
  - `file`: PDF or DOCX file
- **Response:** MP3 audio file

## Notes

- Only PDF and DOCX files are supported for file uploads.
- Audio files are saved in the `audios` directory.
- Temporary uploads are stored in `temp_uploads` and deleted after processing.

## License

MIT License