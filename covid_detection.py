import logging
import os
from PIL import Image
from src.sound import sound
from settings import IMAGE_DIR, DURATION, WAVE_OUTPUT_FILE
from setup_logging import setup_logging
import librosa, librosa.display
import matplotlib.pyplot as plt

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

title = "COVID-19 Detection"
st.title(title)
image = Image.open(os.path.join(IMAGE_DIR, 'covid.png'))
st.image(image, use_column_width=True)






setup_logging()
logger = logging.getLogger('heart')


def get_spectrogram(type='mel'):
    logger.info("Extracting spectrogram")
    y, sr = librosa.load(WAVE_OUTPUT_FILE, duration=DURATION)
    ps = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    logger.info("Spectrogram Extracted")
    format = '%+2.0f'
    if type == 'DB':
        ps = librosa.power_to_db(ps, ref=np.max)
        format = ''.join[format, 'DB']
        logger.info("Converted to DB scale")
    
    return ps, format

    

def display(spectrogram, format):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10, 4))

    librosa.display.specshow(spectrogram, y_axis='mel', x_axis='time')
    plt.title('Mel-frequency spectrogram')
    plt.colorbar(format=format)
    plt.tight_layout()
    st.pyplot(clear_figure=False)

    fig = plt.Figure(figsize=(10, 4))
    ax = fig.add_subplot(111)
    p = librosa.display.specshow(spectrogram, ax=ax, y_axis='mel', x_axis='time')
    fig.savefig('output/recording/spectogram.png')





if st.button('Record'):
    with st.spinner(f'Recording for {DURATION} seconds ....'):
        sound.record()
    st.success("Recording completed")

if st.button('Play'):
    # sound.play()
    try:
        audio_file = open(WAVE_OUTPUT_FILE, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    except:
        st.write("Please record sound first")

if st.button('Display Spectrogram'):
    # type = st.radio("Scale of spectrogram:",
    #                 ('mel', 'DB'))
    if os.path.exists(WAVE_OUTPUT_FILE):
        spectrogram, format = get_spectrogram(type='mel')
        display(spectrogram, format)




    else:
        st.write("Please record sound first")

