# JugaaduToons Hindi Shorts Automation

This adds a separate workflow and does not replace the existing USA Shorts workflow.

## Android setup
1. Download and extract this ZIP on your Android phone.
2. Open your GitHub repository: https://github.com/chadaramit71-creator/Usa_short_agent
3. Upload `generate_jugaadu_short.py` and `upload_jugaadu_youtube.py` to the repository root.
4. Upload `.github/workflows/jugaadu-toons.yml` to the same path in the repository.
5. Keep the existing `requirements.txt`; it already includes Pillow, gTTS and YouTube API libraries.
6. Open the repository's **Actions** tab, select **JugaaduToons Hindi Shorts**, and tap **Run workflow**.
7. When finished, open the run and download the `jugaadu-short-...` artifact ZIP.

## Schedule
The workflow is scheduled at 12:00 and 17:00 UTC, which is 5:30 PM and 10:30 PM India time. GitHub may delay scheduled workflows, and repository activity/usage limits apply.

## Optional YouTube upload
The workflow uploads privately only when all three repository Actions secrets exist:
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

Use OAuth with the `youtube.upload` scope. Never share these values in chat or commit them to files. Until OAuth is fully configured, videos are only saved as downloadable artifacts.

## Important limitation
This free workflow makes vertical cartoon-style illustrated panels with Hindi TTS, not full 3D character animation. gTTS needs internet access. Review the story, voice, captions, and video before publishing.
