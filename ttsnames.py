import gradio as gr
from tts import male_voice,female_voice,TTS_run

male_images = ["inputs/faces/thumbnils/men1.png", "inputs/faces/thumbnils/men2.png", "inputs/faces/thumbnils/men3.png"]
female_images = ["inputs/faces/thumbnils/women1.png", "inputs/faces/thumbnils/women2.png", "inputs/faces/thumbnils/women3.png"]

def update_previews(gender):
    if gender == "Male":
        return male_images, gr.update(choices=male_voice,visible=True)
    elif gender == "Female":
        return female_images, gr.update(choices=female_voice,visible=True)

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
                with gr.Row():
                    image_gallery = gr.Gallery(label="Image Previews", interactive=True,columns=3)
                    gender_input.change(fn=update_previews, inputs=gender_input, outputs=[image_gallery,voice_dropdown])

                video_gen_location = gr.Radio(label="Video Generation Location", choices=["Top Rigth","Top Left","Bottom Right", "Bottom Left"], value="Top Right",interactive=True)

            with gr.Column():

                # Interface for TTS
                output = gr.Audio()
                video_output = gr.Video()
                submit_button = gr.Button("Generate Video")

                voice_dropdown.change(TTS_run, inputs=[text_input, voice_dropdown], outputs=output)
                submit_button.click(TTS_run, inputs=[text_input, voice_dropdown], outputs=output)

    # Launch the interface
    demo.launch(debug=True)

create_interface()