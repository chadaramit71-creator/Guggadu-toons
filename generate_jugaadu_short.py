import os, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

OUT = Path("jugaadu_output")
FRAMES = OUT / "frames"
OUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)

STORIES = [
 {"title":"जादुई चिराग","scenes":[("चिंटू गरीब था, पर उसके सपने बड़े थे।","dream"),("उसे मिट्टी में एक पुराना चिराग मिला।","lamp"),("चिराग से नीला जिन्न बाहर आया!","genie"),("चिंटू ने माँगा एक करोड़ रुपया।","coins"),("सिक्के नकली निकले! चिंटू समझ गया।","oops"),("मेहनत ही असली जादू है! सब्सक्राइब करो।","work")]},
 {"title":"चालाक बंदर","scenes":[("एक बंदर को केले की टोकरी मिली।","monkey"),("लोमड़ी बोली: आधे केले मुझे दे दो।","fox"),("बंदर ने पूछा: तुमने मदद क्या की?","think"),("लोमड़ी चुपचाप वहाँ से चली गई।","fox"),("बंदर ने केले दोस्तों में बाँट दिए।","friends"),("सीख: बाँटो, पर समझदारी से!","work")]},
 {"title":"ईमानदार बच्चा","scenes":[("रवि को रास्ते में एक बटुआ मिला।","wallet"),("उसमें पैसे और एक पहचान पत्र था।","wallet"),("रवि ने मालिक को ढूँढने का फैसला किया।","think"),("वह बटुआ सही मालिक को लौटा आया।","happy"),("मालिक ने रवि को धन्यवाद कहा।","friends"),("सीख: ईमानदारी सबसे अच्छी नीति है!","work")]},
 {"title":"प्यासा कौआ","scenes":[("गर्मी में कौआ बहुत प्यासा था।","crow"),("उसे एक घड़े में थोड़ा पानी दिखा।","pot"),("उसकी चोंच पानी तक नहीं पहुँचती थी।","think"),("कौए ने घड़े में कंकड़ डालने शुरू किए।","stones"),("पानी ऊपर आया, कौए ने पानी पिया।","happy"),("सीख: अक्ल से मुश्किल हल होती है!","work")]}
]

def getfont(size, bold=False):
    paths = [
      "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_scene(idx, title, line, kind):
    w,h=720,1280
    im=Image.new("RGB",(w,h),(130,205,245)); d=ImageDraw.Draw(im)
    d.rectangle((0,760,w,h),fill=(87,175,93))
    d.ellipse((510,80,650,220),fill=(255,220,90))
    d.rounded_rectangle((28,35,692,130),radius=24,fill=(50,40,95))
    d.text((360,82),"JugaaduToons • "+title,font=getfont(29,True),fill="white",anchor="mm")
    d.polygon([(55,650),(180,520),(305,650)],fill=(145,76,48))
    d.rectangle((80,650,280,805),fill=(220,171,104))
    d.rectangle((150,710,205,805),fill=(90,55,40))
    d.ellipse((325,430,445,550),fill=(150,91,55),outline=(65,45,40),width=4)
    d.ellipse((350,470,365,490),fill="white"); d.ellipse((405,470,420,490),fill="white")
    d.ellipse((356,477,363,486),fill=(20,20,20)); d.ellipse((410,477,417,486),fill=(20,20,20))
    d.arc((370,485,410,520),0,180,fill=(70,25,25),width=4)
    d.rounded_rectangle((315,545,455,730),radius=32,fill=(255,157,48),outline=(65,45,40),width=4)
    d.line((330,590,275,665),fill=(150,91,55),width=20); d.line((440,590,490,650),fill=(150,91,55),width=20)
    d.line((350,720,330,790),fill=(50,60,115),width=25); d.line((420,720,445,790),fill=(50,60,115),width=25)
    if kind in ("lamp","genie","coins","oops"):
        d.ellipse((470,660,590,720),fill=(245,190,35),outline=(120,75,15),width=5)
        d.arc((500,635,565,700),180,350,fill=(120,75,15),width=7)
    if kind=="genie":
        d.ellipse((475,330,600,455),fill=(35,155,205),outline=(20,90,140),width=4)
        d.rounded_rectangle((490,430,585,590),radius=35,fill=(35,155,205))
        d.ellipse((505,370,520,390),fill="white"); d.ellipse((550,370,565,390),fill="white")
    if kind=="coins":
        for x,y in [(485,300),(550,260),(610,335),(510,400),(585,440)]:
            d.ellipse((x-20,y-20,x+20,y+20),fill=(255,215,40),outline=(145,100,10),width=3)
    if kind in ("monkey","fox","crow"):
        color=(160,100,60) if kind=="monkey" else ((230,120,45) if kind=="fox" else (45,45,55))
        d.ellipse((470,470,590,590),fill=color)
    if kind in ("wallet","pot","stones"):
        d.rounded_rectangle((480,540,610,630),radius=18,fill=(120,70,40) if kind=="wallet" else (80,135,195))
    if kind=="happy":
        d.text((540,400),"★",font=getfont(90,True),fill=(255,225,60),anchor="mm")
    d.rounded_rectangle((35,870,685,1165),radius=35,fill=(255,255,255),outline=(45,45,85),width=5)
    lines=textwrap.wrap(line,width=23)
    y=920
    for t in lines[:4]:
        d.text((360,y),t,font=getfont(37,True),fill=(35,35,70),anchor="mm",align="center")
        y+=62
    d.text((360,1220),"कहानी • सीख • मुस्कान",font=getfont(25,True),fill="white",anchor="mm")
    im.save(FRAMES/f"frame_{idx:02d}.png")

def main():
    run_index=int(os.getenv("GITHUB_RUN_NUMBER","1"))
    story=STORIES[(run_index-1)%len(STORIES)]
    for i,(line,kind) in enumerate(story["scenes"]):
        draw_scene(i,story["title"],line,kind)
    narration=" ".join(line for line,_ in story["scenes"])
    audio=OUT/"hindi_voice.mp3"
    gTTS(text=narration,lang="hi",slow=False).save(str(audio))
    concat=OUT/"frames.txt"
    with concat.open("w",encoding="utf-8") as f:
        for i in range(6):
            f.write(f"file 'frames/frame_{i:02d}.png'\n")
            f.write("duration 5\n")
        f.write("file 'frames/frame_05.png'\n")
    video=OUT/"jugaadu_short.mp4"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-i",str(audio),
      "-vf","scale=720:1280,format=yuv420p","-c:v","libx264","-preset","ultrafast","-r","30",
      "-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",str(video)],check=True)
    description="मज़ेदार हिंदी कार्टून कहानी और छोटी-सी सीख।\n\n#JugaaduToons #HindiCartoon #Shorts"
    (OUT/"metadata.txt").write_text("TITLE: "+story["title"]+" | Hindi Cartoon #Shorts\n\nDESCRIPTION:\n"+description+"\n\nNARRATION:\n"+narration+"\n",encoding="utf-8")
    print("Created",video)

if __name__=="__main__":
    main()
