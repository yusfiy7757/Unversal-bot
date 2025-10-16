import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_watermark(video_path):
    try:
        output_path = f"watermarked_{os.path.basename(video_path)}"

        # Videoni o‘qiymiz
        video = VideoFileClip(video_path)

        # Chap past burchakka matnli watermark
        txt = TextClip(
            "@podshox_bot",
            fontsize=24,
            color='white',
            font="Arial-Bold"
        ).set_position(("left", "bottom")).set_duration(video.duration)

        # Video + watermarkni birlashtirish
        final = CompositeVideoClip([video, txt])
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')

        video.close()
        final.close()

        return output_path

    except Exception as e:
        print(f"Xato: {e}")
        return None
