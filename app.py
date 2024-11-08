import gradio as gr
import setup1
from multiprocessing import Process
from temporary import main_upscale
from tts import male_voice, female_voice
import inference as lip
import inference_upscale as realesrgan
import subprocess, platform
import edge_tts
 
male_images = ["inputs/faces/thumbnils/men1.png", "inputs/faces/thumbnils/men2.png", "inputs/faces/thumbnils/men3.png"]
female_images = ["inputs/faces/thumbnils/women1.png", "inputs/faces/thumbnils/women2.png", "inputs/faces/thumbnils/women3.png"]
 
outfile = "result"
wav2lip_video = "inputs/wav2lip_out/output.mp4"
audio_file_path = "inputs/input_audio/ai.wav"
enchance_video_ouput = "result/output_out.mp4"
final_output = "result/final_result.mp4"
 
enhance_video = realesrgan.RealEsrganUpscale()
 
def tts(input_text, voice):
    # Function to handle the TTS
    com = edge_tts.Communicate(input_text, voice)
    com.save_sync(audio_file_path)
    return audio_file_path
 
 
def update_previews(gender):
    if gender == "Male":
        return male_images, gr.update(choices=male_voice, visible=True)
    elif gender == "Female":
        return female_images, gr.update(choices=female_voice, visible=True)
 
def select_image(selection: gr.SelectData):
    # Function to handle the selected image
    return selection.value["image"]["orig_name"]
 
def preview_video_process(video_input, selected_image, video_gen_location):
    preview_video = "inputs/faces/" + selected_image.split(".")[0] + ".mp4"
    preview_output = "temp/preview.mp4"
 
    if video_gen_location == "Bottom Right":
        command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
        [0:v][scaled]overlay=W-w--100:H-h" -c:a copy -t 10 {} -y""".format(
            video_input, preview_video, preview_output
        )
    elif video_gen_location == "Bottom Left":
        command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
        [0:v][scaled]overlay=-100:H-h" -c:a copy -t 10 {} -y""".format(
            video_input, preview_video, preview_output
        )
    elif video_gen_location == "Top Right":
        command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
        [0:v][scaled]overlay=W-w--100:0" -c:a copy -t 10 {} -y""".format(
            video_input, preview_video, preview_output
        )
    elif video_gen_location == "Top Left":
        command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
        [0:v][scaled]overlay=-100:0" -c:a copy -t 10 {} -y""".format(
            video_input, preview_video, preview_output
        )
    elif video_gen_location == "Right":
        command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned];
        [cleaned]scale=iw/1.5:ih/1.5[scaled];  [0:v][scaled]overlay=W/2:H-h" -c:a copy -t 10 {} -y""".format(
            video_input, preview_video, preview_output
        )
    elif video_gen_location == "Left":
        command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned];
        [cleaned]scale=iw/1.5:ih/1.5[scaled];  [0:v][scaled]overlay=-W/5:H-h" -c:a copy -t 10 {} -y""".format(
            video_input, preview_video, preview_output
        )
 
    else:
        return 0
 
    subprocess.call(command, shell=platform.system() != "Windows")
 
    return preview_output
 
def create_interface():
    def process_video(video_input, audio_output, video_gen_location, selected_image):
        try:
            preview_video = "inputs/faces/" + selected_image.split(".")[0] + ".mp4"

            lip_sync_obj = lip.Wav2LipCall(face=preview_video, audio="inputs/input_audio/ai.wav", outfile=outfile)
            lip_sync_obj.main()

            del lip_sync_obj
            # Enhance video using Real-ESRGAN

            main()

            if video_gen_location == "Bottom Right":
                command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
                [0:v][scaled]overlay=W-w--100:H-h" -map 1:a -c:a copy {} -y""".format(
                    video_input, enchance_video_ouput, final_output
                )
            elif video_gen_location == "Bottom Left":
                command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
                [0:v][scaled]overlay=-100:H-h" -map 1:a -c:a copy {} -y""".format(
                    video_input, enchance_video_ouput, final_output
                )
            elif video_gen_location == "Top Right":
                command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
                [0:v][scaled]overlay=W-w--100:0" -map 1:a -c:a copy {} -y""".format(
                    video_input, enchance_video_ouput, final_output
                )
            elif video_gen_location == "Top Left":
                command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/2.5:ih/2.5[scaled];
                [0:v][scaled]overlay=-100:0" -map 1:a -c:a copy {} -y""".format(
                    video_input, enchance_video_ouput, final_output
                )
            elif video_gen_location == "Right":
                command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/1.5:ih/1.5[scaled];  [0:v][scaled]overlay=W-w/1.4:H-h" -map 1:a -c:a copy {} -y""".format(
                    video_input, enchance_video_ouput, final_output
                )
            elif video_gen_location == "Left":
                command = """ffmpeg -i {} -i {} -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned];
                [cleaned]scale=iw/1.5:ih/1.5[scaled];  [0:v][scaled]overlay=-W/5:H-h" -map 1:a -c:a copy {} -y""".format(
                    video_input, enchance_video_ouput, final_output
                )
            else:
                return 0

            subprocess.call(command, shell=platform.system() != "Windows")
            return final_output

        finally:
            print("Generated Successfully")

    with gr.Blocks() as demo:
        gr.Markdown("Lip Sync")
        with gr.Row():
            # Left column: Inputs
            with gr.Column():
                video_input = gr.Video()
                text_input = gr.Textbox(label="Input Text")

                with gr.Row():
                    gender_input = gr.Radio(choices=["Male", "Female"], label="Gender", interactive=True, value=None)
                    voice_dropdown = gr.Dropdown(label="Voice", interactive=True)
                # Set up dependency between gender and voice dropdown
                with gr.Row():
                    image_gallery = gr.Gallery(
                        label="Image Previews",
                        interactive=True,
                        columns=3,
                        show_download_button=False,
                        show_share_button=False,
                    )

                    gender_input.change(
                        fn=update_previews,
                        inputs=gender_input,
                        outputs=[image_gallery, voice_dropdown],
                    )

                    selected_image = gr.State()

                    image_gallery.select(fn=select_image, inputs=None, outputs=selected_image)

                video_gen_location = gr.Radio(
                    label="Video Generation Location",
                    choices=["Top Right", "Top Left", "Bottom Right", "Bottom Left", "Right", "Left"],
                    interactive=True,
                )

            with gr.Column():

                # Interface for TTS
                audio_output = gr.Audio(visible=False)
                preview_output = gr.Video(visible=False)
                video_output = gr.Video()
                submit_button = gr.Button("Generate Video")

                voice_dropdown.change(tts, inputs=[text_input, voice_dropdown], outputs=audio_output).then(
                    lambda audio_path: gr.update(visible=True), inputs=audio_output, outputs=audio_output
                )
                video_gen_location.change(preview_video_process, inputs=[video_input, selected_image, video_gen_location], outputs=preview_output).then(
                    lambda preview_path: gr.update(visible=True), inputs=preview_output, outputs=preview_output
                )
                submit_button.click(
                    process_video,
                    inputs=[video_input, audio_output, video_gen_location, selected_image],
                    outputs=video_output,
                )

    # Launch the interface
    demo.launch(debug=True, server_name="0.0.0.0",server_port=5000)


if __name__ == "__main__":
    create_interface()
