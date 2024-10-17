import requests
import json
from pydub import AudioSegment
import io
import gradio as gr
import inference as lip
import inference_realesrgan_video as realesrgan
from moviepy.editor import VideoFileClip
import subprocess, platform

outfile = "result"
wav2lip_video = "inputs/wav2lip_out/output.mp4"
audio_file_path = "inputs/input_audio/ai.wav"


def generateAudio(video):
    # Load the video file
    video = VideoFileClip(video)

    # Extract audio from the video and save it as a WAV file
    audio = video.audio
    audio.write_audiofile(audio_file_path)


def process_video(video, text):

    try:
        generateAudio(video)
        videopath = "inputs/faces/{}.mp4".format(text)

        lip_sync_obj = lip.Wav2LipCall(
            face=videopath, audio=audio_file_path, outfile=outfile
        )
        lip_sync_obj.main()

        del lip_sync_obj

        # Enhance video using Real-ESRGAN
        enhance_video = realesrgan.RealEsrganUpscale(
            input=wav2lip_video, output=outfile
        )
        enhance_video.main()

        command = """ffmpeg -i {} -i result/result_out.mp4 -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
            [0:v][scaled]overlay=W-w--100:H-h" -c:a copy result/final_result.mp4 -y""".format(
            video
        )

        subprocess.call(command, shell=platform.system() != "Windows")

        return "result/final_result.mp4"

    finally:
        if enhance_video:
            del enhance_video
        print("Generated Successfully")


infer = gr.Interface(
    fn=process_video,
    inputs=["video", gr.Radio(["Male", "Female"], label="Character")],
    outputs="video",
    title="Lip Sync with Wav2Lip and Enhance with Real-ESRGAN",
    description="Upload a video and an audio file to perform lip sync and enhance the output video.",
)

infer.launch()