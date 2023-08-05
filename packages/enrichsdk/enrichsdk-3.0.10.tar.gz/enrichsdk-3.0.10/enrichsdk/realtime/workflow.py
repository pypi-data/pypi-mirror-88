"""
Workflow
--------

This module has simple modules for building a realtime transform
pipeline. They are called workflows here to avoid confusion with
'pipeline' used elsewhere.

"""

import traceback
import logging

logger = logging.getLogger('app')

class State(object):
    """
    Internal state objects. Transform classes use this
    state object to store and retrieve state during
    execution.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = {}

    def put(self, name, value):
        self.frames[name] = value

    def get(self, name):
        if name not in self.frames:
            raise Exception("Missing records")
        return self.frames[name]

class WorkflowBase(object):
    """
    Base class to define a workflow. This class registers new
    transforms. Right now it is a simple linear flow. We expect to
    support DAGs in future.

    """
    def __init__(self, *args, **kwargs):
        """
        """
        self.config = kwargs.get('config', {})
        self.debug = kwargs.get('debug', False)
        self.transforms = []

    def add(self, t):
        if isinstance(t, list):
            self.transforms.extend(t)
        else:
            self.transforms.append(t)

        for t in self.transforms:
            t.pipeline = self

    def process(self, streamrow, params={}):
        """
        Process one input record obtained from the stream such as
        Kafka.

        """
        state = State()
        state.put('streamrow', streamrow)

        for t in self.transforms:
            try:
                state = t.process(state)
            except:
                logger.exception("Unable to process")
                raise

        return state

    def get_extra(self):
        """
        Generate pipeline metadata
        """
        extra = {}
        if self.debug:
            versions = [str(t) for t in self.transforms]
            extra = {
                'versions': versions
            }
        return extra



