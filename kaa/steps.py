from collections import defaultdict
from dataclasses import dataclass
from functools import partial, wraps


class Story:
    def __init__(self, app, title, defaults=None, animation_settings=None, sequence_settings=None):
        self.app = app
        self.title = title
        # create a deep copy of the defaults
        self.defaults = merge({}, defaults or {'data': [{}], 'layout': {}, 'animate': True})
        self.animation_settings = animation_settings or {}
        self.sequence_settings = sequence_settings or {}
        self._sections = []

    def make_section(self, *args, **kwargs):
        section = Section(*args, story=self, **kwargs)
        self._sections.append(section)
        return section

    def __iter__(self):
        return iter(self._sections)


class Section:
    def __init__(self, name, story, *, figure_left=True):
        self.name = name
        self.figure_left = figure_left
        self.story = story
        self._steps = []

    def add_animated_step(self, fn=None, *args, **kwargs):
        if fn is None:
            return partial(self.add_animated_step, *args, **kwargs)
        step_name = kwargs.get('name', fn.__name__)
        self._steps.append(Step(step_name, *args, **kwargs, animate=True))
        return self.story.app.route(f'/steps/{step_name}')(fn)

    def add_text_only_step(self, *args, **kwargs):
        self._steps.append(Step(*args, **kwargs, animate=False))

    def __iter__(self):
        return iter(self._steps)


@dataclass
class Step:
    name: str
    text: str
    animate: bool
    is_sequence: bool = False


def merge(source, destination):
    """
    run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination
