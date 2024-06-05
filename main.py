import pandas as pd
import parselmouth
from vosk import Model, KaldiRecognizer
import os
import wave
import json
import logging

logging.basicConfig(level=logging.ERROR)
def transcribe_audio_to_text(file_path, model_path):
    wf = wave.open(file_path, "rb")
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    full_text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            full_text += result.get("text", "") + " "
    final_result = json.loads(rec.FinalResult())
    full_text += final_result.get("text", "")

    return full_text.strip()


def calculate_speaking_rate(transcribed_text, audio_file_path):
    word_count = len(transcribed_text.split())

    with wave.open(audio_file_path, 'r') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration_seconds = frames / float(rate)
        duration_minutes = duration_seconds / 60

    speaking_rate = word_count / duration_minutes
    return speaking_rate, word_count, duration_minutes


def extract_features(sound_file):
    # extracting using parselmouth
    sound = parselmouth.Sound(sound_file)
    pitch = parselmouth.praat.call(sound, "To Pitch (ac)...", 0.0, 75.0, 15, "off", 0.09, 0.5, 0.055, 0.35, 0.14, 600.0)
    min_pitch = parselmouth.praat.call(pitch, "Get minimum", 0, 0, "hertz", "Parabolic")
    max_pitch = parselmouth.praat.call(pitch, "Get maximum", 0, 0, "hertz", "Parabolic")
    mean_pitch = parselmouth.praat.call(pitch, "Get mean", 0, 0, "hertz")
    sd_pitch = parselmouth.praat.call(pitch, "Get standard deviation", 0, 0, "hertz")

    intensity = parselmouth.praat.call(sound, "To Intensity", 100.0, 0.0)
    min_intensity = parselmouth.praat.call(intensity, "Get minimum", 0, 0, "Parabolic")
    max_intensity = parselmouth.praat.call(intensity, "Get maximum", 0, 0, "Parabolic")
    mean_intensity = parselmouth.praat.call(intensity, "Get mean", 0, 0, 'energy')
    sd_intensity = parselmouth.praat.call(intensity, "Get standard deviation", 0, 0)

    point_process = parselmouth.praat.call(sound, 'To PointProcess (periodic, cc)', 75.0, 600.0)
    local_jitter = parselmouth.praat.call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    local_shimmer = parselmouth.praat.call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    harmonicity = parselmouth.praat.call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = parselmouth.praat.call(harmonicity, "Get mean", 0, 0)

    return {
        "Min Pitch": min_pitch,
        "Max Pitch": max_pitch,
        "Mean Pitch": mean_pitch,
        "SD Pitch": sd_pitch,
        "Min Intensity": min_intensity,
        "Max Intensity": max_intensity,
        "Mean Intensity": mean_intensity,
        "SD Intensity": sd_intensity,
        "Jitter (Local)": local_jitter,
        "Shimmer (Local)": local_shimmer,
        "HNR": hnr,
    }
def process_audio_files(audio_folder, model_path, output_csv):
    emotions = ["Happy", "Angry", "Sad", "Afraid", "Surprised", "Disgusted", "Neutral"]
    audio_files = [f"{emotion}.wav" for emotion in emotions]

    # DataFrame
    results_df = pd.DataFrame(columns=[
        "Speech File", "Min Pitch", "Max Pitch", "Mean Pitch", "Sd Pitch", "Min Intensity",
        "Max Intensity", "Mean Intensity", "Sd Intensity", "Speaking Rate", "Jitter",
        "Shimmer", "HNR"
    ])


    for emotion, audio_file in zip(emotions, audio_files):
        file_path = os.path.join(audio_folder, audio_file)
        transcribed_text = transcribe_audio_to_text(file_path, model_path)

        #  speaking rate --- calculating here
        speaking_rate, word_count, duration_minutes = calculate_speaking_rate(transcribed_text, file_path)
        # transcribed text, word count, and words per minute
        features = extract_features(file_path)
        current_results = pd.DataFrame([{
            "Speech File": emotion,
            "Min Pitch": features["Min Pitch"],
            "Max Pitch": features["Max Pitch"],
            "Mean Pitch": features["Mean Pitch"],
            "Sd Pitch": features["SD Pitch"],
            "Min Intensity": features["Min Intensity"],
            "Max Intensity": features["Max Intensity"],
            "Mean Intensity": features["Mean Intensity"],
            "Sd Intensity": features["SD Intensity"],
            "Speaking Rate": speaking_rate,
            "Jitter": features["Jitter (Local)"],
            "Shimmer": features["Shimmer (Local)"],
            "HNR": features["HNR"]
        }])
        results_df = pd.concat([results_df, current_results], ignore_index=True)
    results_df.to_csv(output_csv, index=False)

# audio folder, vosk model and output
audio_folder = 'my_sounds'
model_path = 'vosk-model-en-us-0.22'
output_csv = 'my_features.csv'


process_audio_files(audio_folder, model_path, output_csv)



