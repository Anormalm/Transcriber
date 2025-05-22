# Meeting Transcriber & Translator

A real-time speech transcription tool using Vosk + translation support via:

- `transcriber.py`: Online translator using Deep Translator (Google Translate backend)
- `transcriber_local.py`: Offline translation using MarianMT (Hugging Face)

## Features
- Live microphone transcription using Vosk (English, Chinese, German supported)
- Optional real-time translation to another language (e.g., Chinese)
- Offline and firewall-safe version with no need for internet
- Clean console output, minimal dependencies

## Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```
### 2. Download models
•	Vosk model (e.g. English):
https://alphacephei.com/vosk/models
→ Place in model/
•	MarianMT translation model (e.g. opus-mt-en-zh):
https://huggingface.co/Helsinki-NLP/opus-mt-en-zh
→ Place in Helsinki-NLP/opus-mt-en-zh/

### 3. Run Online Version
```bash
python transcriber.py
```
### 4. Run Offline Version
```bash
python transcriber_local.py
``` 
## Notes
	•	model/, Helsinki-NLP/, and venv/ are excluded from version control
	•	For offline use, download models manually on a VPN-enabled device if needed
