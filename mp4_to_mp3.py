from moviepy.editor import VideoFileClip
import argparse
import os
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

def convert_mp4_to_mp3(input_path, output_path=None):
    clip = None
    try:
        clip = VideoFileClip(input_path)
        audio = clip.audio
        
        if not output_path:
            base = os.path.splitext(input_path)[0]
            output_path = f"{base}.mp3"
        
        # 改用iter_frames跟踪进度
        with tqdm(total=int(clip.duration), unit='s', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            audio.write_audiofile(output_path, ffmpeg_params=['-loglevel', 'quiet'])
            # 手动完成进度条
            pbar.update(int(clip.duration) - pbar.n)
        
        return True
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return False
    finally:
        if clip is not None:
            clip.close()

def process_directory(input_dir, output_dir=None):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.mp4'):
                input_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, input_dir)
                output_path = os.path.join(output_dir, rel_path, os.path.splitext(file)[0] + '.mp3') if output_dir else None
                convert_mp4_to_mp3(input_path, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MP4转MP3转换器')
    parser.add_argument('input', nargs='?', help='输入MP4文件路径或目录（可选）')
    parser.add_argument('-o', '--output', help='输出目录路径（可选）')
    
    args = parser.parse_args()
    
    if not args.input:
        root = tk.Tk()
        root.withdraw()
        input_path = filedialog.askopenfilename(title='选择MP4文件', filetypes=[('MP4 files', '*.mp4')])
        if not input_path:
            print("未选择目录，程序退出")
            exit()
        
        output_path = filedialog.askdirectory(title='选择输出目录（可选）') 
        convert_mp4_to_mp3(input_path, os.path.join(output_path, os.path.basename(input_path).replace('.mp4', '.mp3')) if output_path else None)
        print("\n批量转换完成！")
    else:
        if not os.path.exists(args.input):
            print("错误：输入路径不存在")
            exit(1)
            
        if os.path.isdir(args.input):
            process_directory(args.input, args.output)
            print("\n批量转换完成！")
        else:
            if convert_mp4_to_mp3(args.input, args.output):
                print("\n转换完成！")
            else:
                print("\n转换过程中发生错误")