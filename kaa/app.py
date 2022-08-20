import json

import flask
import numpy as np

from . import steps


app = flask.Flask(__name__)

story = steps.Story(
    app,
    'Kaa Demo',
    defaults={
        'layout': {
            'xaxis': {
                'showgrid': False,
            },
            'yaxis': {
                'showgrid': False,
                'range': (np.sqrt(10) * np.array([-3, 3])).tolist(),
            },
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
        },
        'animate': True
    },
    animation_settings={
        'transition': {
            'duration': 500,
            'easing': 'cubic-in-out'
        },
        'frame': {
            'duration': 500,
        }
    },
    sequence_settings={
        'transition': {
            'duration': 0,
            'easing': 'cubic-in-out'
        },
        'frame': {
            'duration': 0,
            'redraw': False
        }
    },
)

section1 = story.make_section('Intro')
section2 = story.make_section('Body', figure_left=False)
section3 = story.make_section('Outro', figure_left=False)


@app.route('/')
def main():
    return flask.render_template('index.html', story=story)


@section1.add_animated_step(text='''
This is the first step of the story.
''')
def step1():
    return {
        'data': [{
            'x': list(range(10)),
            'y': np.random.RandomState(1).normal(size=10).cumsum().tolist()
        }]
    }

@section1.add_animated_step(text='''
This is the second step of the story, which introduces a new plot.
''')
def step2():
    return {
        'data': [{
            'x': list(range(10)),
            'y': np.random.RandomState(2).normal(size=10).cumsum().tolist()
        }]
    }

@section1.add_animated_step(text='''
In addition to the data, we can change any features of the plot we wish, such
adding a title or axes scale.
''')
def step100():
    return {
        'data': [{
            'x': list(range(10)),
            'y': np.random.RandomState(2).normal(size=10).cumsum().tolist()
        }],
        'layout': {
            'title': {'text': 'kaa'},
            'yaxis': {
                'range': (np.sqrt(8) * np.array([-3, 3])).tolist()
            }
        }
    }


@section1.add_animated_step(text='''
This is the last step of the first section. After this step, we'll switch up
the layout and start with a fresh plot.
''')
def step3():
    return {
        'data': [{
            'x': list(range(10)),
            'y': np.random.RandomState(3).normal(size=10).cumsum().tolist(),
        }]
    }


@section2.add_animated_step(text='''
This is the first step of a new section. Here, we opted to reverse the layout
to indicate this is a new context.
''')
def step4():
    rng = np.random.RandomState(4)
    x, y = rng.normal(size=30), rng.normal(size=30)
    return {
        'data': [{
            'x': x.tolist(),
            'y': y.tolist(),
            'mode': 'markers',
            'marker': {
                'color': (np.sqrt(x ** 2 + y ** 2) < 1).astype(int).tolist(),
            },
        }],
        'layout': {
            'xaxis': {'range': [-3, 3]},
            'yaxis': {'range': [-3, 3]}
        }
    }


@section2.add_animated_step(text='''
At any point we can scroll up to revisit previous steps to see how things are changing.
''')
def step5():
    rng = np.random.RandomState(5)
    x, y = rng.normal(size=30), rng.normal(size=30)
    return {
        'data': [{
            'x': x.tolist(),
            'y': y.tolist(),
            'mode': 'markers',
            'marker': {
                'color': (np.sqrt(x ** 2 + y ** 2) < 1).astype(int).tolist(),
            },
        }],
        'layout': {
            'xaxis': {'range': [-3, 3]},
            'yaxis': {'range': [-3, 3]}
        }
    }



@section2.add_animated_step(text='''
This is the final step of the second section. We'll start the next section
with a fresh plot, but keep the layout the same this time.
''')
def step6():
    rng = np.random.RandomState(6)
    x, y = rng.normal(size=30), rng.normal(size=30)
    return {
        'data': [{
            'x': x.tolist(),
            'y': y.tolist(),
            'mode': 'markers',
            'marker': {
                'color': (np.sqrt(x ** 2 + y ** 2) < 1).astype(int).tolist(),
            },
        }],
        'layout': {
            'xaxis': {'range': [-3, 3]},
            'yaxis': {'range': [-3, 3]}
        }
    }


@section3.add_animated_step(text='''
This is the first step of a third section.
''')
def step7():
    return {
        'data': [{
            'x': list(range(10)),
            'y': np.random.RandomState(7).normal(size=10).cumsum().tolist()
        }]
    }


section3.add_text_only_step(text='''
    Sometimes it is convenient to add a step that doesn't change the plot.
    ''',
    name='explanatory-text1'
)


for step_args in [('explanatory-text2', 'This allows us to add several segments of commentary to a single image.')]:
    section3.add_text_only_step(*step_args)


@section3.add_animated_step(text='''
    This concludes the demo.
    ''',
    is_sequence=True
)
def step10():
    x = np.linspace(-10, 10)
    offset = 10 * np.random.normal(size=30)
    a = -abs(np.random.normal(size=30))
    b = np.random.normal(size=30)
    c = np.random.normal(size=30)

    fireworks = (
        (a[None, :] * (offset[None, :] - x[:, None]) ** 2 + b[None, :] * (offset[None, :] - x[:, None]) + c[None, :])
        - (a[None, :] * offset[None, :] ** 2 + b[None, :] * offset[None, :] + c[None, :])
    )

    return {
        'data': [
            {
                'data': [
                    {
                        'x': (offset[j] - x[:i]).tolist(),
                        'y': fireworks[:i, j].T.tolist(),
                        'mode': 'lines'
                    } for j in range(len(a))
                ]
            } for i in range(len(x))
        ]
    }



if __name__ == '__main__':
    app.run()
