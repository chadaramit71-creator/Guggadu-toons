import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

OUT = Path("output")
FRAMES = OUT / "frames"
OUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)

EPISODES = [
    {
        "title": "Robot Ki Pehli Naukri",
        "scenes": [
            "जुगाड़ू: रोबोट, चाय बना दो!",
            "रोबोट ने चाय की जगह सूप बना दिया!",
            "जुगाड़ू: ये कैसी चाय है?",
            "रोबोट: आपने गरम पेय माँगा था!",
            "जुगाड़ू: मेरी तो छुट्टी हो गई!"
        ]
    },
    {
        "title": "Homework Ka Jugaad",
        "scenes": [
            "जुगाड़ू: रोबोट, मेरा होमवर्क कर दो!",
            "रोबोट: पहले मेरी छुट्टी मंजूर करो!",
            "जुगाड़ू: तुम मशीन हो!",
            "रोबोट: और आप बहाने बनाने के मास्टर!",
            "जुगाड़ू: ये रोबोट किसने बनाया?"
        ]
    },
    {
        "title": "Magic Samosa",
        "scenes": [
            "समोसा: इच्छा माँगो, जुगाड़ू!",
            "जुगाड़ू: मुझे सौ समोसे चाहिए!",
            "समोसा: पैसे पहले दो!",
            "जुगाड़ू: ये कैसा जादू है?",
            "समोसा: बिजनेस में सब चलता है!"
        ]
    },
    {
        "title": "Smartphone Ka Jugaad",
        "scenes": [
            "जुगाड़ू: बिजली नहीं है, फोन कैसे चार्ज करूँ?",
            "दोस्त: पावर बैंक इस्तेमाल कर ले!",
            "जुगाड़ू: नहीं, मैं साइकिल से चार्ज करूँगा!",
            "दोस्त: पहले साइकिल में चार्जिंग पोर्ट तो लगा!",
            "जुगाड़ू: आइडिया अच्छा था, बस छोटी सी कमी थी!"
        ]
    }
]

def get_font(size, bold=True):
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def wrap_lines(draw, text, font, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def draw_character(draw, robot, index):
    if robot:
        x, y = 520, 610
        draw.rounded_rectangle((x-75, y-100, x+75, y+45), 24,
                               fill=(100, 205, 230), outline=(25, 55, 80), width=6)
        for ex in (x-35, x+35):
            draw.ellipse((ex-15, y-60, ex+15, y-30), fill="white")
            draw.ellipse((ex-6, y-52, ex+6, y-40), fill=(15, 35, 65))
        draw.arc((x-30, y-25, x+30, y+15), 0, 180, fill=(15, 35, 65), width=5)
        draw.line((x, y-100, x, y-135), fill=(25, 55, 80), width=7)
        draw.ellipse((x-12, y-150, x+12, y-126), fill=(255, 190, 65))
        draw.rounded_rectangle((x-90, y+45, x+90, y+145), 20,
                               fill=(65, 145, 195), outline=(25, 55, 80), width=6)
        draw.line((x-75, y+65, x-125, y+105), fill=(25, 55, 80), width=13)
        draw.line((x+75, y+65, x+125, y+105), fill=(25, 55, 80), width=13)
        draw.line((x-40, y+140, x-50, y+185), fill=(25, 55, 80), width=15)
        draw.line((x+40, y+140, x+50, y+185), fill=(25, 55, 80), width=15)
    else:
        x, y = 190, 625
        draw.ellipse((x-65, y-145, x+65, y-15), fill=(255, 195, 140),
                     outline=(85, 45, 30), width=5)
        draw.pieslice((x-72, y-165, x+72, y-35), 180, 360, fill=(35, 25, 25))
        draw.ellipse((x-34, y-95, x-19, y-80), fill=(25, 25, 25))
        draw.ellipse((x+19, y-95, x+34, y-80), fill=(25, 25, 25))
        draw.arc((x-28, y-70, x+28, y-35), 0, 180, fill=(130, 30, 30), width=5)
        draw.rounded_rectangle((x-75, y-15, x+75, y+145), 25,
                               fill=(245, 130, 40), outline=(85, 45, 30), width=5)
        draw.line((x-60, y+20, x-105, y+90), fill=(85, 45, 30), width=14)
        draw.line((x+60, y+20, x+105, y+90), fill=(85, 45, 30), width=14)
        draw.line((x-35, y+140, x-45, y+190), fill=(35, 45, 90), width=17)
        draw.line((x+35, y+140, x+45, y+190), fill=(35, 45, 90), width=17)

def make_frame(text, index, title):
    w, h = 720, 1280
    image = Image.new("RGB", (w, h), (255, 225, 155))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, w, 290), fill=(85, 175, 230))
    draw.ellipse((535, 45, 635, 145), fill=(255, 225, 75))
    draw.rectangle((0, 290, w, h), fill=(255, 220, 145))
    draw.rounded_rectangle((25, 25, w-25, 105), 22, fill=(70, 55, 150))
    draw.text((w//2, 65), "JugaaduToons", font=get_font(36), fill="white", anchor="mm")
    draw.text((w//2, 165), title, font=get_font(27), fill=(70, 45, 100), anchor="mm")
    draw_character(draw, robot=(index % 2 == 1), index=index)
    draw.rounded_rectangle((28, 850, w-28, 1135), 28, fill=(255, 255, 245),
                           outline=(70, 55, 150), width=5)
    lines = wrap_lines(draw, text, get_font(32), w-95)
    line_height = 48
    y = 990 - (len(lines) * line_height)//2
    for line in lines:
        draw.text((w//2, y), line, font=get_font(32), fill=(35, 35, 55), anchor="mm")
        y += line_height
    draw.text((w//2, 1210), "HINDI COMEDY • CARTOON SHORTS",
              font=get_font(19), fill=(70, 55, 110), anchor="mm")
    image.save(FRAMES / f"frame_{index:03d}.png")

def main():
    run_number = int(os.getenv("GITHUB_RUN_NUMBER", "1"))
    episode = EPISODES[(run_number - 1) % len(EPISODES)]
    narration = " ".join(episode["scenes"])
    gTTS(text=narration, lang="hi", slow=False).save(str(OUT / "voice.mp3"))

    for i, scene in enumerate(episode["scenes"]):
        make_frame(scene, i, episode["title"])

    concat = OUT / "frames.txt"
    with concat.open("w", encoding="utf-8") as file:
        for i in range(len(episode["scenes"])):
            file.write(f"file 'frames/frame_{i:03d}.png'\n")
            file.write("duration 4\n")
        file.write(f"file 'frames/frame_{len(episode['scenes'])-1:03d}.png'\n")

    video = OUT / "jugaadu_toons.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(OUT / "voice.mp3"),
        "-vf", "scale=720:1280,format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-r", "30",
        "-c:a", "aac", "-b:a", "128k", "-shortest",
        "-movflags", "+faststart", str(video)
    ], check=True)

    description = (
        "Original Hindi cartoon comedy by JugaaduToons.\n"
        "#JugaaduToons #HindiComedy #Cartoon #Shorts"
    )
    (OUT / "metadata.txt").write_text(
        f"TITLE: {episode['title']} | JugaaduToons #Shorts\n\n"
        f"DESCRIPTION:\n{description}\n\nNARRATION:\n{narration}\n",
        encoding="utf-8"
    )
    print(f"Created {video}: {episode['title']}")

if __name__ == "__main__":
    main()
