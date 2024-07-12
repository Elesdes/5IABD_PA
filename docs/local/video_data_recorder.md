# How to use video_data_recorder.py

This guide will explain how to use the video_data_recorder.py. Remember, you must use the Myo Armband and you need to connect it before using it.

## System Setup

### Set locale

Your local setup needs a camera and the support of the Myo Armband device to operate correctly.
Local file use a specific environment. All libraries are standard but myo-python. You still need to install it.

```bash
pip install -r requirements.txt
```

Once done, you can now launch `video_data_recorder.py`

### Interface

The interface allow the user to record the data and the camera at the same time up to 10min.
The file can be named, but you cannot change the prediction. It must be the same predict everytime.
Two options are available. Since the Myo Armband can register its orientation, the csv can have two additional columns.
