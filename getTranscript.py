from typing import Text
import constants
from voskSpeech2Text import Speech2TextProcesss, Speech2TextException
import logging


class GetTranscript():

    def __init__(self,
                 model_path=constants.MODEL_PATH,
                 sample_rate=constants.SAMPLE_RATE,
                 log=constants.LOG,
                 buffer_path=constants.BUFFER_PATH,
                 buffer_size=constants.BUFFER_SIZE,
                 ):

        self.s2t_model = Speech2TextProcesss(
            model_folder=model_path,
            sample_rate=sample_rate,
            log=log,
            buffer_path=buffer_path,
            buffer_size=buffer_size,
        )

    def make_transcript(self, clip_url):
        s2t_model = self.s2t_model
        logging.info("Downloaded clip succesfully.")
        s2t_model.transcript_audio(clip_url)
        logging.info("Transcription done.")
        text = s2t_model.vosk_transcript_2_text()
        logging.info("Text")
        return text

    def process(self, clip_url, dest_fpath):
        transcription = {}
        logging.info('Starting transcription')
        transcription = self.make_transcript(clip_url)
        if transcription:
            with open(dest_fpath, 'w') as f:
                f.write(transcription)
        logging.info(f'Finalized transcription. Saved in {dest_fpath}')
