import pyaudio
import json
from vosk import Model, KaldiRecognizer
from transformers import MarianMTModel, MarianTokenizer

def load_marian_model(target_lang="zh"):
    lang_map = {
        "zh": "./Helsinki-NLP/opus-mt-en-zh"
    }
    model_name = lang_map.get(target_lang, "./Helsinki-NLP/opus-mt-en-zh")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def translate_offline(text, tokenizer, model):
    batch = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
    gen = model.generate(**batch)
    translated = tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
    return translated

def run_live_transcription(model_path="models/en", target_lang="zh"):
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    tokenizer, translator_model = load_marian_model(target_lang)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
    stream.start_stream()

    print("[INFO] Listening... Speak into the mic.")

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if text:
                    translated = translate_offline(text, tokenizer, translator_model)
                    print(f">>> EN: {text}")
                    print(f">>> {target_lang.upper()}: {translated}")
    except KeyboardInterrupt:
        print("\n[INFO] Transcription stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    run_live_transcription()