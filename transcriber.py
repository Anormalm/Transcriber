import pyaudio
import json
from vosk import Model, KaldiRecognizer
from deep_translator import MyMemoryTranslator

def run_live_transcription(model_path="models/en", target_lang="zh-CN"):
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...Speak into the microphone.")
    translator = MyMemoryTranslator(source='en-US', target=target_lang)
    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '')
                if text:
                    translated_text = translator.translate(text)
                    print(f">>> {text}")
                    print(f">>> {target_lang.upper()}: {translated_text}")
    except KeyboardInterrupt:
        print("\nTranscription stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    run_live_transcription()