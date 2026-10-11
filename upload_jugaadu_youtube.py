import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def main():
    required=["YOUTUBE_CLIENT_ID","YOUTUBE_CLIENT_SECRET","YOUTUBE_REFRESH_TOKEN"]
    missing=[k for k in required if not os.getenv(k)]
    if missing:
        raise SystemExit("Missing Actions secrets: "+", ".join(missing))
    creds=Credentials(token=None,refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
      token_uri="https://oauth2.googleapis.com/token",client_id=os.environ["YOUTUBE_CLIENT_ID"],
      client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
      scopes=["https://www.googleapis.com/auth/youtube.upload"])
    youtube=build("youtube","v3",credentials=creds)
    metadata=Path("jugaadu_output/metadata.txt").read_text(encoding="utf-8")
    title=metadata.split("TITLE: ",1)[1].splitlines()[0][:100]
    description=metadata.split("DESCRIPTION:\n",1)[1].split("\n\nNARRATION:",1)[0]
    req=youtube.videos().insert(part="snippet,status",
      body={"snippet":{"title":title,"description":description,
      "tags":["JugaaduToons","Hindi cartoon","Shorts"],"categoryId":"1"},
      "status":{"privacyStatus":"private","selfDeclaredMadeForKids":False}},
      media_body=MediaFileUpload("jugaadu_output/jugaadu_short.mp4",chunksize=-1,resumable=True))
    result=req.execute()
    print("Uploaded private video ID:",result.get("id"))

if __name__=="__main__":
    main()
