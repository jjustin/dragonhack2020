from __future__ import division
from google.cloud import speech
import re
import sys
import pyaudio
from six.moves import queue
import time


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

        self.input_device_index = 2

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()

        for i in range(self._audio_interface.get_device_count()):
            pass
            # print(self._audio_interface.get_device_info_by_index(i))

        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            input_device_index=self.input_device_index,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


class SpeechStream:
    def __init__(self, rate, chunk, keywords):
        language_code = 'en-US'  # a BCP-47 language tag

        self.keywords = keywords

        self.rate = rate
        self.chunk = chunk

        self.client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=rate,
            language_code=language_code)
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        self.stream_array = []
        self.responses = None
        self.current_keywords = []

    def get_words(self):
        # Returns the last 40 characters of stream
        return self.stream_array[-40:].lower() if len(self.stream_array) > 0 else ''

    def listen_print_loop(self):
        num_chars_printed = 0
        for response in self.responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            if not result.is_final:
                self.stream_array = transcript

    def code_driver(self):
        with MicrophoneStream(self.rate, self.chunk) as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            self.responses = self.client.streaming_recognize(
                self.streaming_config, requests)
            self.listen_print_loop()

    def get_keywords(self):
        chars = self.get_words()
        for k in self.keywords:
            # if chars.find(k) > 0:
            if k.lower() in chars:
                self.current_keywords.append(k.lower())

    def get_current_keyword(self):
        if len(self.current_keywords) == 0:
            return None

        kword = self.current_keywords[0]
        self.current_keywords.remove(kword)
        return kword.lower()
