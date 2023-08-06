![ezprez logo](https://raw.githubusercontent.com/Descent098/ezprez/master/.github/logo.png)

# ezprez

*An object based api for generating web presentations/slideshows*

## Table of Contents
- [What does ezprez do?](#what-does-ezprez-do)
- [Features & Roadmap](#features--roadmap)
- [Why should I use ezprez?](#why-should-i-use-ezprez)
- [Who is ezprez for?](#who-is-ezprez-for)
- [Installation](#installation)
  - [From source](#from-source)
  - [From PyPi](#from-pypi)
- [Quick-start](#quick-start)
- [Additional Documentation](#additional-documentation)
  - [Examples and Resources](#examples-and-resources) 

## What does ezprez do?

Let's you write simple python scripts to generate web presentations/slideshows

## Features & Roadmap

### Simple class based api

The api iteself uses native python classes to create presentations in a short script that's easily editable

### No web experience needed

Since this is a pure python API you can write web presentations without knowing HTML

### Backed on a reliable web framework

Webslides powers this project and is a well-tested and stable web framework.

## Why should I use ezprez?

Ezprez is the simplest API for writing web presentations without needing explicit knowledge of web development. If you are looking to create powerpoint style presentations [python-pptx](https://python-pptx.readthedocs.io/en/latest/) or [the google slides api](https://developers.google.com/slides/quickstart/python) is better suited for this job.

## Who is ezprez for?

- People who want an easy way to create web presentations without editing html
- People who know python but not web development technologies

## Installation

### From PyPi

1. Run ```pip install ezprez```

### From source

1. Clone this repo: (put github/source code link here)
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory

## Quick-start

For just plain text slides the easiest way to get started is just using the ```Slide``` and ```Presentation``` objects:

```python
from ezprez.core import Slide, Presentation

# Create a slide object (don't need to assign it to a variable or anything it's added to presentation on instantiation)
Slide("This is the slide title", "this is some content")

# Setup the actual presentation settings
presentation_url = "https://kieranwood.ca/ezprez-example" # The URL the presentation will be hosted at
prez = Presentation("This is the presentation title", "This is the presentation description", presentation_url)

# Export the presentation in the current directory at /Presentation
prez.export(".", folder_name="Presentation")
```

There will then be a folder called Presentation, and inside the ```index.html``` file will contain your presentation. Just put that up on a static hosting service and you're good to go.


## Additional Documentation


[User Docs](https://ezprez.readthedocs.io)

[API Docs](https://kieranwood.ca/ezprez) (I would recommend the user docs first)

## Examples and resources

[Template repository for bootstrapping projects](https://github.com/QU-UP/ezprez)

Example presentation: [Live demo](https://kieranwood.ca/ezprez-example), [Source Code](https://github.com/Descent098/ezprez-example)
