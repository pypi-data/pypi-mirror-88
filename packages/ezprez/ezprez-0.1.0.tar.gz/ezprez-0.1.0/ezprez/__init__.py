"""An object based api for generating web presentations

Note
----
If this is your first time using ezprez I would recommend looking at the user docs at https://ezprez.readthedocs.io

Installation
------------
#### From pypi
```pip install ezprez``` or ```sudo pip3 install ezprez```

#### From source
1. ```git clone https://github.com/Descent098/ezprez```
2. ```pip install .``` or ```sudo pip3 install .```

Modules
-------
#### core

The module that contains the Presentation and Slide classes that are used to generate web presentations

#### components

The module that contains all component subclasses that can be used to generate Slide content

Quickstart
----------
#### Creating a presentation with a text slide and exporting it to ./Presentation
```
from ezprez.core import Presentation, Slide

# This slide is auto-added to the Presentation object by default
Slide('This is the title', 'and this is the content')

prez = Presentation(title, description, url)

# Export the files to the current directory at /Presentation, and delete existing files if they're found
prez.export(".", force=True, folder_name="Presentation")
```

#### Creating a presentation with a slide that has text, and a code snippet and exporting it to ./Presentation
```
from ezprez.core import Presentation, Slide
from ezprez.components import Code

# This slide is auto-added to the Presentation object by default
Slide('This is the title', 'and here is some python code', Code('python', 'Hello World'))

prez = Presentation(title, description, url)

# Export the files to the current directory at /Presentation, and delete existing files if they're found
prez.export(".", force=True, folder_name="Presentation")
```
"""