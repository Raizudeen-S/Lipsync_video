import requests
import json
from pydub import AudioSegment
import io
import gradio as gr
from dotenv import dotenv_values

config = dotenv_values(".env")
url = config["URL"]

audio_file_path = "ai.wav"
male_voice = ['en-AU-WilliamNeural', 'en-CA-LiamNeural', 'en-HK-SamNeural', 'en-IN-PrabhatNeural', 'en-IE-ConnorNeural', 'en-KE-ChilembaNeural', 'en-NZ-MitchellNeural', 'en-NG-AbeoNeural', 'en-PH-JamesNeural', 'en-SG-WayneNeural', 'en-ZA-LukeNeural', 'en-TZ-ElimuNeural', 'en-GB-RyanNeural', 'en-GB-ThomasNeural', 'en-US-AndrewMultilingualNeural', 'en-US-BrianMultilingualNeural', 'en-US-AndrewNeural', 'en-US-BrianNeural', 'en-US-ChristopherNeural', 'en-US-EricNeural', 'en-US-GuyNeural', 'en-US-RogerNeural', 'en-US-SteffanNeural']
female_voice = ['en-AU-NatashaNeural', 'en-CA-ClaraNeural', 'en-HK-YanNeural', 'en-IN-NeerjaExpressiveNeural', 'en-IN-NeerjaNeural', 'en-IE-EmilyNeural', 'en-KE-AsiliaNeural', 'en-NZ-MollyNeural', 'en-NG-EzinneNeural', 'en-PH-RosaNeural', 'en-SG-LunaNeural', 'en-ZA-LeahNeural', 'en-TZ-ImaniNeural', 'en-GB-LibbyNeural', 'en-GB-MaisieNeural', 'en-GB-SoniaNeural', 'en-US-AvaMultilingualNeural', 'en-US-EmmaMultilingualNeural', 'en-US-AvaNeural', 'en-US-EmmaNeural', 'en-US-AnaNeural', 'en-US-AriaNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural']

def update_voice_list(gender):
    if gender == "Male":
        return gr.update(choices=male_voice,visible=True)
    elif gender == "Female":
        return gr.update(choices=female_voice,visible=True)

def TTS_run(text,voice):
    payload = {
    "data": [
        text,
        voice,
        None
    ],
    "event_data": None,
    "fn_index": 1
}
    response = requests.post(url+"/run/predict", json=payload)

    if response.status_code == 200:
        try:
            json_data = response.json() 

            data = json_data.get('data')
            file_name = url + "/file=" +data[0]['name']

            response = requests.get(file_name)

            if response.status_code == 200:
                mp3_data = io.BytesIO(response.content)
                audio = AudioSegment.from_mp3(mp3_data)
                audio.export(audio_file_path, format="wav")
                return audio_file_path
                
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")

        except ValueError:
            print("Response is not in valid JSON format")
    else:
        print(f"Request failed with status code: {response.status_code}")

def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("Lip Sync")
        with gr.Row():
            # Left column: Inputs
            with gr.Column():
                video_input = gr.Video()
                text_input = gr.Textbox(label="Input Text")
                with gr.Row():
                    gender_input = gr.Dropdown(choices=["Male", "Female"], label="Gender", interactive=True)
                    voice_dropdown = gr.Dropdown(label="Voice", interactive=True)
                # Set up dependency between gender and voice dropdown
                gender_input.change(update_voice_list, inputs=gender_input, outputs=voice_dropdown)
            with gr.Column():

                # Interface for TTS
                output = gr.Audio()
                video_output = gr.Video()
                submit_button = gr.Button("Generate Video")

                voice_dropdown.change(TTS_run, inputs=[text_input, voice_dropdown], outputs=output)
                submit_button.click(TTS_run, inputs=[text_input, voice_dropdown], outputs=output)

    # Launch the interface
    demo.launch()

create_interface()