#Mark Zharikov 218390
import os
import subprocess


def convert_video_to_mp2(input_file, output_file):
    command = f"ffmpeg -i {input_file} -c:v mpeg2video {output_file}"
    subprocess.call(command, shell = True)

def parse_ffmpeg(input_file):

    input_file_video = str(input_file[0])

    # Showing the duration of the video
    duration = subprocess.check_output(f"ffmpeg -i {input_file} 2>&1 | grep Duration | awk '{{print $2}}' | tr -d ,", stderr=subprocess.STDOUT, shell=True)

    #Show the resolution of input video
    resolution = subprocess.check_output(f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x {input_file}", stderr=subprocess.STDOUT, shell=True)

    #Showing the video codec
    videocodec = subprocess.check_output(f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1 {input_file}", shell=True, stderr=subprocess.STDOUT)

    #Showing the audio codec
    audiocodec = subprocess.check_output(f"ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {input_file}", shell=True, stderr=subprocess.STDOUT, text=True)


    #Showing the bitrate of the video
    bitrate = subprocess.check_output(f"ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1 {input_file}", shell=True, stderr=subprocess.STDOUT, text=True)

    # Showing the framerate of the video
    framerate = subprocess.check_output(f"ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1 {input_file}", shell=True, stderr=subprocess.STDOUT, text=True)

    str_to_replace = str(r"\n\n")
    duration = str(duration)
    duration = duration.replace("b'", '')
    duration = duration.replace(str_to_replace, '')

    resolution = str(resolution)
    resolution = resolution.replace("b'", '')
    resolution = resolution.replace(str_to_replace, '')

    videocodec = str(videocodec)
    videocodec = videocodec.replace("b'", '')
    videocodec = videocodec.replace(str_to_replace, '')


    bitrate = str(bitrate)
    bitrate = bitrate.replace("b'", '')
    bitrate = bitrate.replace(str_to_replace, '')

    framerate = str(framerate)
    framerate = framerate.replace("b'", '')
    framerate = framerate.replace(str_to_replace, '')

    print('Duration: ' + duration)
    print('Resolution:' + resolution)
    print('Video Codec: ' + videocodec)
    print('Audio Bitrate: ' + bitrate + 'bps')
    print('Framerate: ' + framerate)

def change_resolution(input_file, output_resolution, new_width, new_height):
    command = f"ffmpeg -i {input_file} -vf scale={new_width}:{new_height} {output_resolution}"
    subprocess.call(command, shell=True)

def change_chroma_subsampling(input_file, output_subsampling, pix_fmt):
    command = f"ffmpeg -i {input_file} -c:v libx264 -pix_fmt {pix_fmt} {output_subsampling}"
    subprocess.call(command, shell=True)

def main():
    input_file = "/mnt/c/Users/User/Desktop/BBB.mp4"
    output_file = "/mnt/c/Users/User/Desktop/BBB.mpg"
    output_resolution = "/mnt/c/Users/User/Desktop/BBB_resolution.mp4"
    output_subsampling = "/mnt/c/Users/User/Desktop/BBB_yuv444p.mp4"

    while True:

        menu = input("1.Convert to mp2 input video\n2.Get Video Information\n3.Change Resolution\n4.Change Chroma Subsampling\n5.- Exit\n")
        menu = int(menu)
        # menu with case's
        match menu:  # match function only works in python 3.10 or superior
            case 1:
                print("Convert to mp2 input video")
                convert_video_to_mp2(input_file, output_file)

            case 2:
                print("Get Video Information")
                parse_ffmpeg(output_file)

            case 3:
                print("Change Resolution")
                new_width = input("Change the width:")
                new_width = int(new_width)
                new_height = input("Change the height:")
                new_height = int(new_height)
                change_resolution(input_file, output_resolution, new_width, new_height)
                
            case 4:
                print("Change the chroma subsampling")
                change_chroma_subsampling(input_file, output_subsampling, pix_fmt="yuv444p")

            case 5:
                print("Exit")
                return
            case _:
                print("Invalid input, choose [1, 2, 3, 4 or 5 ]")
                main()

if __name__ == '__main__':
    main()


