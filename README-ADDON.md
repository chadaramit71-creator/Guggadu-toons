# JugaaduToons Automation Add-on

This bundle adds a Hindi cartoon Shorts generator and a twice-daily GitHub Actions workflow to the existing `Usa_short_agent` repository.

## Add to your existing repository
Copy these two files into the matching paths:
- `generate_jugaadu_toons.py` → repository root
- `.github/workflows/jugaadu-toons.yml` → `.github/workflows/`

The existing repository must already contain `requirements.txt` and `upload_youtube.py`.

## Schedule
The workflow runs at 14:00 and 22:00 UTC (19:30 and 03:30 India time). GitHub can delay scheduled workflows, and schedules may be disabled for inactive repositories.

## Output
Each run generates one vertical 720×1280 MP4 with original drawn cartoon characters, Hindi text, and Hindi TTS narration. The video is saved as a GitHub Actions artifact for 7 days.

## YouTube upload
The workflow calls the existing `upload_youtube.py` only if all three repository Actions secrets exist:
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

The included uploader uploads privately. OAuth setup, API quota and permissions must be valid. The generator creates simple illustrated scenes, not full-motion 3D animation. Review the result before publishing.
