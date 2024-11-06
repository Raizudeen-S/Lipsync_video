import inference as lip
from multiprocessing import Process
import inference_upscale as realesrgan
from temporary import main
import setup1


print("Hello")

enhance_video = realesrgan.RealEsrganUpscale()
enhance_video.main(inputs="inputs/wav2lip_out/output.mp4", output="result")

# enhance_video = realesrgan.RealEsrganUpscale()
# enhance_video.main(inputs="inputs/wav2lip_out/output.mp4", output="result")

# main("inputs/wav2lip_out/output.mp4", ""inputs/wav2lip_out/output.mp4"")

# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()


# Right  = ffmpeg -i "C:\Users\019161\Downloads\sample_video.mp4" -i "C:\Users\019161\Downloads\result_out1.mp4" -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/3:ih/3[scaled];  [0:v][scaled]overlay=W-w/1.4:H-h" -map 1:a -c:a copy Right.mp4 -y

# Left = ffmpeg -i "C:\Users\019161\Downloads\sample_video.mp4" -i "C:\Users\019161\Downloads\result_out1.mp4" -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/3:ih/3[scaled];  [0:v][scaled]overlay=-W/5:H-h" -map 1:a -c:a copy Left.mp4 -y

# Top Right = ffmpeg -i "C:\Users\019161\Downloads\sample_video.mp4" -i "C:\Users\019161\Downloads\result_out1.mp4" -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/4:ih/4[scaled]; [0:v][scaled]overlay=W-w--200:0" -map 1:a -c:a copy TopRight.mp4 -y

# Top Left = ffmpeg -i "C:\Users\019161\Downloads\sample_video.mp4" -i "C:\Users\019161\Downloads\result_out1.mp4" -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/4:ih/4[scaled]; [0:v][scaled]overlay=-200:0" -map 1:a -c:a copy TopLeft.mp4 -y

# Bottom Left = ffmpeg -i "C:\Users\019161\Downloads\sample_video.mp4" -i "C:\Users\019161\Downloads\result_out1.mp4" -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/4:ih/4[scaled]; [0:v][scaled]overlay=-200:H-h" -map 1:a -c:a copy BottomLeft.mp4 -y

# Bottom Right = ffmpeg -i "C:\Users\019161\Downloads\sample_video.mp4" -i "C:\Users\019161\Downloads\result_out1.mp4" -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[cleaned]; [cleaned]scale=iw/4:ih/4[scaled]; [0:v][scaled]overlay=W-w--200:H-h" -map 1:a -c:a copy BottomRight.mp4 -y