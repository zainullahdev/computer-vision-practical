import cv2
import numpy as np
import time as t


class CaptureManager(object):
    def __init__(self, capture, preview_window_manager=None,
                 should_mirror_preview=True):
        self.preview_window_manager = preview_window_manager
        self.should_mirror_preview = should_mirror_preview
        self._capture = capture
        self._channel = 0
        self._entered_frame = False
        self._frame = None
        self._image_filename = None
        self._video_filename = None
        self._video_encoding = None
        self._video_writer = None
        self._start_time = None
        self._frames_elapsed = long(0)
        self._fps_estimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._entered_frame and self._frame is None:
            _, self._frame = self._capture.retrieve(channel=self._channel)
        return self._frame

    @property
    def is_writing_image(self):
        return self._imageFilename is not None

    @property
    def is_writing_video(self):
        return self._videoFilename is not None

    def enter_frame(self):
        """Capture the next frame, if any."""

        # But first, check that any previous frame was exited.
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame()'

        if self._capture is not None:
            self._entered_frame = self._capture.grab()

    def exit_frame(self):
        """Draw to the window. Write to files. Release the frame."""

        # Check whether any grabbed frame is retrievable.
        # The getter may retrieve and cache the frame.
        if self._frame is None:
            self._entered_frame = False
            return