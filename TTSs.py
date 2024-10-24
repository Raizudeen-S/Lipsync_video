from os import listdir, path
import numpy as np
import scipy, cv2, os, sys, argparse, audio
import json, subprocess, random, string
import gradio as gr
from tts import male_voice, female_voice
import inference as lip
import inference_upscale as realesrgan
import subprocess, platform
import edge_tts


enhance_video = realesrgan.RealEsrganUpscale()
enhance_video.main(inputs="inputs/wav2lip_out/output.mp4", output="result")