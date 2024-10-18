import argparse
import cv2
import glob
import mimetypes
import numpy as np
import os
import shutil
import subprocess
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from os import path as osp
from tqdm import tqdm
from multiprocessing import Lock

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

try:
    import ffmpeg
except ImportError:
    import pip
    pip.main(['install', '--user', 'ffmpeg-python'])
    import ffmpeg

# Create a global lock for synchronizing the creation of the Gradio application
gradio_lock = Lock()

def get_video_meta_info(video_path):
    ret = {}
    probe = ffmpeg.probe(video_path)
    video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
    ret['width'] = video_streams[0]['width']
    ret['height'] = video_streams[0]['height']
    ret['fps'] = eval(video_streams[0]['avg_frame_rate'])
    ret['audio'] = ffmpeg.input(video_path).audio if has_audio else None
    return ret

# Ensure Gradio application is created only once
def create_gradio_app():
    with gradio_lock:
        # Check if the Gradio app is already created
        if not hasattr(create_gradio_app, "app"):
            import gradio as gr
            # Define your Gradio app here
            def inference(input_video):
                # Your inference code here
                return "Processed video path"

            create_gradio_app.app = gr.Interface(fn=inference, inputs="video", outputs="text")
            create_gradio_app.app.launch()

# Call the function to create the Gradio app
create_gradio_app()