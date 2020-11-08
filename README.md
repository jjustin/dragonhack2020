# Totally Listening To You (TLTY.py for short)

## Presented to you by **Trivial Group**
***

## Features


## Speech to text

### Google cloud authentication:
https://cloud.google.com/docs/authentication/getting-started#windows

Activate you have to activate your key in the shell the project is running in with:
```
set GOOGLE_APPLICATION_CREDENTIALS=C:/Users/Frenk/auth/trivial-dh-2020-c45bdf0254cc.json
```

## Requirements
Download driver from [this url](https://chromedriver.chromium.org/),
check your chrome version before.

- ffmpeg
- https://vb-audio.com/Cable/
- OBS

### Zoom/application sound transcription
Enable Stereo Mix in windows sound settings.
Then check the device index of stereo mix (there is a tool in speect_to_text.py)
and set it in speech_stream_to_text.pi as a global variable.

### AudioPy
For some reason (only on Windows), you must build AudioPy from a wheel file, the default pip install does not work.
