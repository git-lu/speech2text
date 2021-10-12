import constants
from wrapt_timeout_decorator import timeout
from vosk import KaldiRecognizer, Model
from moviepy.editor import VideoFileClip
import json
import pathlib
import time
from datetime import timedelta
import subprocess


class Speech2TextProcesss():
    def __init__(self,
                 model_folder=constants.MODEL_PATH,
                 sample_rate=constants.SAMPLE_RATE,
                 res_type=constants.RES_TYPE,
                 buffer_path='./temp',
                 buffer_size=constants.BUFFER_SIZE,
                 log=constants.LOG
                 ):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.res_type = res_type
        self.temp_path = pathlib.Path(buffer_path)
        self.temp_path.mkdir(exist_ok=True)
        self.model = Model(model_folder)
        self.transcripted_audio = None
        self.clip_url = None
        self.log = log
        self.errors = []

    def log_data(self, data, end='', prefix='\r', log_type='info'):
        if self.log:
            print(prefix + data, end=end)
            print("\033[K "*100, end='')
            if log_type == 'error':
                self.errors.append([data, self.clip_url])

    def log_task_time(self, start_time, end='', prefix='\r'):
        print(
            prefix + f'elapesed_time: {timedelta(seconds=(time.time() - start_time))}', end=end)

    def transcript_audio(self, clip_url, dtype='int16'):
        self.clip_url = clip_url
        start_time = time.time()
        print('Transcription started...')
        rec = KaldiRecognizer(self.model, self.sample_rate)
        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                    self.clip_url,
                                    '-ar', str(self.sample_rate), '-ac', '1', '-f', 's16le', '-'],
                                   stdout=subprocess.PIPE)

        results = []
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))
        results.append(json.loads(rec.FinalResult()))
        self.transcripted_audio = results
        self.log_task_time(start_time)
        return results

    def check_transcript(self):
        if self.transcripted_audio is None:
            message = 'Run transcript_audio first'
            self.log_data(message)
            raise Speech2TextException(message)

    def vosk_transcript_2_text(self):
        self.check_transcript()
        text = ''
        for tr in self.transcripted_audio:
            if 'text' in tr:
                text = text + ' ' + tr['text']
        text = text.strip()
        return text


class Speech2TextException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
