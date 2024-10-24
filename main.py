import json
import os
import subprocess
from pydub import AudioSegment
import concurrent.futures
import tempfile


def text_to_audio(text, output_file, voice="Kyoko"):
    with tempfile.NamedTemporaryFile(suffix='.aiff', delete=False) as temp_aiff:
        subprocess.run(["say", "-v", voice, "-o", temp_aiff.name, text], check=True)
    # AIFFファイルをMP3に変換
    audio = AudioSegment.from_file(temp_aiff.name, format="aiff")
    audio.export(output_file, format="mp3")
    # 一時AIFFファイルを削除
    os.unlink(temp_aiff.name)

def create_mp3_segment(args):
    time_str, segment, output_dir, speed_factor, voice = args

    current_time = parse_time(time_str)
    temp_file = os.path.join(output_dir, f"segment_{current_time:04d}.mp3")
    text_to_audio(segment, temp_file, voice)
    # 音声の速度を調整
    audio = AudioSegment.from_mp3(temp_file)
    audio = audio.speedup(playback_speed=speed_factor)

    # セグメントの前後に少し無音を追加
    silence = AudioSegment.silent(duration=100)  # 100ミリ秒の無音
    audio = silence + audio + silence
    audio.export(temp_file, format="mp3")
    print(f"セグメント {time_str} の長さ: {len(audio) / 1000:.2f}秒")  # デバッグ情報
    return (current_time, temp_file, len(audio))

def create_mp3_segments(json_data, output_dir="temp_audio", speed_factor=1.2, voice="Kyoko"):
    os.makedirs(output_dir, exist_ok=True)
    sorted_segments = sorted(json_data.items(), key=lambda x: parse_time(x[0]))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        segment_files = list(executor.map(create_mp3_segment,
                                          [(time_str, segment, output_dir, speed_factor, voice)
                                           for time_str, segment in sorted_segments]))
    return segment_files

def merge_mp3_files(segment_files, output_file="output.mp3"):
    final_audio = AudioSegment.empty()
    last_end_time = 0
    for current_time, file_path, segment_duration in segment_files:
        audio_segment = AudioSegment.from_mp3(file_path)
        start_time = current_time * 1000
        if start_time > last_end_time:
            silence_duration = start_time - last_end_time

            final_audio += AudioSegment.silent(duration=silence_duration)
            print(f"無音追加: {silence_duration / 1000:.2f}秒")  # デバッグ情報
        final_audio += audio_segment

        last_end_time = len(final_audio)
        print(f"セグメント追加: 開始時間 {current_time}秒, 長さ {segment_duration / 1000:.2f}秒")  # デバッグ情報
    final_audio.export(output_file, format="mp3")

    print(f"合計時間: {len(final_audio) / 1000:.2f}秒")

def parse_time(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds


if __name__ == "__main__":
    with open("text.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 利用可能な日本語の女性音声を確認
    voices = subprocess.check_output(["say", "-v", "?"], universal_newlines=True)

    japanese_female_voices = [line.split()[0] for line in voices.split('\n') if 'ja_JP' in line and 'female' in line.lower()]
    if japanese_female_voices:
        print("利用可能な日本語女性音声:")

        for i, voice in enumerate(japanese_female_voices):
            print(f"{i+1}. {voice}")
        choice = int(input("使用する音声の番号を入力してください: ")) - 1

        voice = japanese_female_voices[choice]
        print(f"選択された音声: {voice}")
    else:
        voice = "Kyoko"
        print("警告: 日本語の女性音声が見つかりません。デフォルトの音声 Kyoko を使用します。")
    segment_files = create_mp3_segments(data, speed_factor=1.2, voice=voice)
    merge_mp3_files(segment_files)
    # 一時ファイルを削除
    for _, file_path, _ in segment_files:
        os.remove(file_path)
    os.rmdir("temp_audio")