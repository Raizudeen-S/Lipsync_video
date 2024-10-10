from pprint import pprint
import os
import sys
import uuid , time
import edge_tts
import ast
from asyncio import run as async_run
import asyncio
audio_responses_directory = "audio_responses"
if not os.path.exists(audio_responses_directory):
    os.mkdir(audio_responses_directory)
current_directory = "./audio_responses"
 
male_voice = []
female_voice = []
async def voice_list():
  from edge_tts import VoicesManager
  voices = await VoicesManager.create()
  voice = voices.find(Gender="Male", Language="en")
  for voi in voice:
    male_voice.append(voi["ShortName"])
  #pprint(male_voice)
  voice = voices.find(Gender="Female", Language="en")
  for voi in voice:
    female_voice.append(voi["ShortName"])
  #pprint(female_voice)
 
import asyncio
loop = asyncio.get_event_loop_policy().get_event_loop()
try:
   loop.run_until_complete(voice_list())
finally:
   loop.close()
print("Voice list setup completed")
print(male_voice)
 
STYLE = """
body {
    background-color: #1a1a1a;
    color: #ffffff;
}
#prompt-txt > label > span {
    display: none !important;
}
#prompt-txt > label > textarea {
    border: transparent;
    box-shadow: none;
}
.light-theme #prompt-txt > label > textarea {
    color: #000000; /* Text color for light theme */
}
.dark-theme #prompt-txt > label > textarea {
    color: #ffffff; /* Text color for dark theme */
}
 
#left-top {
  padding-left: 0; /* Remove left padding completely */
  padding-right: 2%;
  margin-left: 0; /* Remove any left margin */
  text-align: left; /* Ensure text starts at the left edge */
  font-weight: bold;
  font-size: 1.5em;
  color: #ffffff;
}
 
#aux-btns-popup {
    position: absolute !important;
}
#aux-btns-popup > div {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
.aux-btn {
    flex: 0 0 98%; /* Adjusted width to be half of the window */
    margin: 1%; /* Added margin for spacing between buttons */
    font-weight: unset !important;
    box-shadow: none !important;
    border-radius: 20px !important;
}
.light-theme .aux-btn {
    color: #000000; /* Adjust text color for light theme */
}
.dark-theme .aux-btn {
    color: #ffffff; /* Adjust text color for dark theme */
}
.aux-btn:hover {
    box-shadow: 0.3px 0.3px 0.3px gray !important;
}
"""
 
audio__store_current_directory = 'audio_responses'
async def gen_audio(text,VoiceId):
    try:
        unique_hex_name = f"{int(time.time())}_{uuid.uuid4().hex}"
        communicate = edge_tts.Communicate(text, VoiceId)
    except Exception as e:
        print(Exception)
    output = os.path.join(audio__store_current_directory, f"{unique_hex_name}.mp3")
    with open(output, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
    return f"{audio__store_current_directory}/{unique_hex_name}.mp3"
 
import gradio as gr
with gr.Blocks(css=STYLE) as kb_chatbot:
  with gr.Column(scale=1, min_width=180,visible=True) as component1:
    gr.Markdown("Edge TTS", elem_id="left-top")
    voice_char = gr.Dropdown(["female_voice","male_voice"],elem_id="chara",label="Select Character",show_label=True)
    female_voice_char = gr.Dropdown([i for i in female_voice],elem_id="fchara",label="female_voice",show_label=True,visible=False)
    male_voice_char = gr.Dropdown([j for j in male_voice],elem_id="mchara",label="male_voice",show_label=True,visible=False)
    instruction_txtbox = gr.Textbox(placeholder="Enter the text", label="",elem_id="prompt-txt")
    aud = gr.Audio(autoplay=True,visible=True)
 
    #Api components
    with gr.Row():
      api_data = gr.Textbox(visible=False)
      api_response = gr.JSON(visible=False)
      api_send_button = gr.Button(visible=False)
 
  async def audio_stream(text,female_voice_char,male_voice_char):
    try:
      VoiceId = ""
      if female_voice_char != None:
        VoiceId = female_voice_char
      if male_voice_char != None:
        VoiceId = male_voice_char
      unique_hex_name = f"{int(time.time())}_{uuid.uuid4().hex}"
      communicate = edge_tts.Communicate(text, VoiceId)
    except Exception as e:
      print(Exception)
      sys.exit(-1)
    output = os.path.join(current_directory, f"{unique_hex_name}.mp3")
    with open(output, "wb") as file:
      async for chunk in communicate.stream():
        if chunk["type"] == "audio":
          file.write(chunk["data"])
    return f"{current_directory}/{unique_hex_name}.mp3"
 
  def voice_selection(voice_char):
    if voice_char == "female_voice":
      return female_voice_char.update(visible=True),male_voice_char.update(visible=False,value=None)
    if voice_char == "male_voice":
      return female_voice_char.update(visible=False,value=None),male_voice_char.update(visible=True)
 
  def api_respond(api_data):
    print(api_data)
    api_data = ast.literal_eval(api_data)
    message = api_data.get('text')
    voice_id = api_data.get('voice_id','')
    if voice_id == '':
        voice_id = 'en-IN-NeerjaExpressiveNeural'            
    try:
      audio_filename = async_run(gen_audio(message,voice_id))
      print(audio_filename)
      api_response = {
          'audio_url': f'http://43.205.228.194/file={os.path.abspath(audio_filename)}'
      }
      return api_response
    except Exception as e:
      api_response = {
          'audio_url': f'Failed to generate response'
      }
      return api_response
 
  voice_char.change(voice_selection,voice_char,[female_voice_char,male_voice_char])
  instruction_txtbox.submit(audio_stream, inputs=[instruction_txtbox,female_voice_char,male_voice_char], outputs=[aud])
 
  api_send_button.click(api_respond, inputs=[api_data], outputs=[api_response],api_name="audio")
 
kb_chatbot.launch(share=False, debug=True)
#kb_chatbot.launch(share=True, debug=True,server_port=8000)