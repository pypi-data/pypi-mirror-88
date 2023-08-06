"""The module that contains the Presentation and Slide classes that are used to generate web presentations

Classes
-------
#### Slide
The class that is used to generate slides that are fed into the Presentation object

####Presentation
The class for defining the presentation configuration, and primary entrypoint to exporting presentations

Notes
-----
- On first run you will need an internet connection to download webslides

Examples
--------
#### Creating a presentation with a slide and exporting it to ./Presentation
```
from ezprez.core import Presentation, Slide

# This slide is auto-added to the Presentation object by default
Slide('This is the title', 'and this is the content')

prez = Presentation(title, description, url)

# Export the files to the current directory at /Presentation, and delete existing files if they're found
prez.export(".", force=True, folder_name="Presentation")
```
"""
# Standard lib dependencies
import os                                   # Used in path validation
from datetime import datetime               # Used to get date for export
from typing import Union, List              # Used to enrich type hints in methods
from shutil import copyfile, copytree, rmtree         # Used to do high level filesystem operations
from dataclasses import dataclass, field    # Used to make class generation faster and more efficient

# Internal dependencies
from ezprez.components import *             # Used for type checking in content generation
from ezprez.components import _Component    # Used for type checking in content generation

# External Dependencies
from tqdm import tqdm                       # Used for progress bars
from elevate import elevate                 # Used for any protected folder access such as system wide python installs or exports
from pystall.core import ZIPResource, build # Used to download webslides from the latest version and extract it for use on export


class Slide:
    """The class that is used to generate slides that are fed into the Presentation object

    Class Variables
    ---------------
    all: (List[Slide])
        Contains all slide instances that have been instatiated, accessed through Slide.all

    Attributes
    ----------
    heading: (str)
        The slide's title/heading

    contents: (str, list, or Component)
        An arbitrary number of strings, lists or Component subclasses that make up the contents of the slide

    background: (False or str)
        The background color of the slide (see notes), optional by default False

    image: (False or Image)
        An image to use as a background for the slide, optional by default False

    horizontal_alignment: (str)
        Where to align the slide contents horizontally, optional defaults to 'center'

    vertical_alignment: (str)
        Where to align the slide contents vertically, optional defaults to 'center'
    
    animation: (str)
        Which animation to use for slide transition, optional defaults to 'fadeIn'

    Notes
    -----
    - Horizontal alignment can be left, right or center
    - Vertical alignment can be top, bottom or center
    - Background colors available can be found at https://webslides.tv/demos/components#slide=27; just make sure to remove 'bg', so for example 'bg-black' becomes 'black'
    - Contents is an unpacked variable, meaning you just specify multiple sets of contents such as Slide(title, 'this is content', ['and', 'so', 'is', 'this'], Button('This to', '#'))
    - Animation can be fadeIn, fadeInUp, zoomIn, slideInLeft, slideInRight
    - You can also add 'slow' to the end of any animation to slow the animation i.e. 'zoomIn slow'


    Examples
    --------
    ### Create a basic text slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Button

    Slide('Here is a text slide', 'and this is the text')
    ```

    ### Create a slide with some text, a list, and a button
    ```
    from ezprez.core import Slide
    from ezprez.components import Button

    Slide('This is the title...', '... and this is content', ['and', 'so', 'is', 'this'], Button('This to', '#'))
    ```
    """
    all = []

    def __init__(self, heading:str, *contents:Union[str, list, tuple, _Component], background:Union[bool,str] = False, horizontal_alignment:str = "center", vertical_alignment:str = "center", image:Union[bool, Image]=False, animation:str = "fadeIn" ):
        # Assign class attributes
        self.image = image
        self.heading = heading
        self.contents = contents
        self.background = background
        self.vertical_alignment = vertical_alignment 
        self.horizontal_alignment = horizontal_alignment
        self.animation = animation

        # Append slide to the class variable Slide.all
        Slide.all.append(self)

    def _generate_content(self):
        """Generates the necessary html with the provided contents"""
        result = f"\n\t\t\t<section class='bg-{self.background} slide-{self.vertical_alignment}'>"
        
        if self.image:
            result += f"\n\t\t\t\t<span class='background' style='background-image:url(\"./static/images/{self.image.filename}\")'></span>"
        result += f"\n\t\t\t\t<div class='wrap {self.animation}'>\n\t\t\t\t\t<div class='content-{self.horizontal_alignment}'>\n\t\t\t\t\t<h2>{self.heading}</h2>\n"
        
        for content in self.contents:
            if type(content) == str: # If the current peice of content is a str
                result += f"\t\t\t\t\t<p>{content}</p>\n"

            elif type(content) == list or type(content) == tuple: # If the current peice of content is a list or tuple
                result += f"\t\t\t\t\t<div class='grid {'content-' + self.horizontal_alignment if not self.horizontal_alignment == 'right' else ''}'>\n\t\t\t\t\t\t\t<ul style='text-align:justify;'>\n"
                for bullet_point in content: # Iterate through each element in the list/tuple
                    result += f"\t\t\t\t\t\t\t\t<li>{bullet_point}</li>\n"
                result += "\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</ul>\n"
            elif isinstance(content, _Component) or type(SocialLink): # If the current peice of content is a Component
                result += content.__html__()
        result += "\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</section>\n"

        yield result


    def __html__(self):
        """Generates the markup for each slide"""
        result = ""
        for content in self._generate_content():
            result+= content
        return result


@dataclass
class Presentation:
    """The class for defining the presentation configuration, and primary entrypoint to exporting presentations

    Attributes
    ----------
    title: (str)
        The title of the presentation

    description: (str)
        The description of the presentation

    url: (str)
        The canonical URL the presentation will be deployed at

    slides: List[Slide]
        The slides to generate the presentation with, optional and defaults to Slide.all

    background: (str)
        What color the intro slie and default slide background color should be, optional defaults to 'white'

    image: (Image or False)
        Path to background image to use for og tags, and intro slide, optional defaults to False

    endcard: (bool)
        Whether to add the endcard, optional defaults to True

    intro: (bool)
        Generate an introduction slide with the background image, title, and description, optional defaults to True

    favicon: (Image or False)
        The image to use for the favicon, optional defaults to False

    vertical: (bool)
        Whether the slideshow should be vertical or not, optional defaults to False

    navbar: (Navbar or False)
        The navbar for the site, optional defaults to False

    footer: (Footer or False)
        The footer for the site, optional defaults to False

    Methods
    -------
    export:
        Exports the presentation files

    Examples
    --------
    ### Creating a presentation and exporting it to ./Presentation
    ```
    from ezprez.core import Presentation

    prez = Presentation(title, description, url)

    # Export the files to the current directory at /Presentation, and delete existing files if they're found
    prez.export(".", force=True, folder_name="Presentation")
    ```

    ### Creating a presentation with a slide and exporting it to ./Presentation
    ```
    from ezprez.core import Presentation, Slide

    # This slide is auto-added to the Presentation object by default
    Slide('This is the title', 'and this is the content')

    prez = Presentation(title, description, url)

    # Export the files to the current directory at /Presentation, and delete existing files if they're found
    prez.export(".", force=True, folder_name="Presentation")
    ```
    """
    title: str 
    description: str 
    url: str
    intro: bool = True
    endcard: bool = True
    vertical: bool = False
    background: str = "white"
    image: Union[bool, Image] = False
    favicon: Union[bool, Image] = False
    navbar: Union[bool, Navbar] = False
    footer: Union[bool, Footer] = False
    slides: List[Slide] = field(default_factory=lambda: Slide.all) 


    def _generate_favicon_markup(self):
        """Generates the html to render the favicon properly"""
        if self.favicon:
            return f'''<!-- FAVICONS -->
            <link rel="apple-touch-icon icon" sizes="76x76" href="./static/images/{self.favicon.filename}">'''
        else:
            return f'''<!-- FAVICONS -->
            <link rel="apple-touch-icon icon" sizes="76x76" href="static/images/favicons/favicon-152.png">'''


    def _generate_intro_slide(self):
        """Generates the first slide in a presentation"""
        if self.intro:
            if self.image:
                return f"""\t\t\t<section class='bg-{self.background}'>
                <span class='background' style='background-image:url("./static/images/{self.image.filename}")'></span>
                    <div class='wrap aligncenter'>
                        <h1><strong>{self.title}</strong></h1>
                        <p class='text-intro'>{self.description}</p>
                    </div>
            </section>"""
            else:
                return f"""\t\t\t<section class='bg-{self.background}'>
                    <div class='wrap aligncenter'>
                        <h1><strong>{self.title}</strong></h1>
                        <p class='text-intro'>{self.description}</p>
                    </div>
            </section>"""


    def _generate_endcard(self) -> str:
        """Generates the slide that goes at the end of Presentation's"""
        if self.endcard:
            return f"""\t\t\t<section class='bg-{self.background}'>
                    <div class='wrap aligncenter'>
                        <h2><strong>Thank you</strong></h2>
                        <h4 class='text-intro'>This presentation was made with the help of</h4>
                        <h4>
                            <strong><em><a href='https://webslides.tv' target='_blank'>WebSlides</a></em></strong> 
                        </h4>
                        <h4>
                            <strong><em><a href='https://github.com/Descent098/ezprez' target='_blank'>ezprez</a></em></strong>
                        </h4>
                    </div>
            </section>"""
        else:
            return ""


    def __len__(self) -> int:
        """Returns the number of slides in the presentation"""
        return len(self.slides)


    def __html__(self) -> str:
        """Generates the index.html file of a presentation using the provided slides"""
        slides_html = ""
        slide_iterator = tqdm(self.slides)
        slide_iterator.set_description_str("Generating slide content")
        for slide in slide_iterator:
            if not slide.background:
                slide.background = self.background
            slides_html += slide.__html__()

        result = f'''<!doctype html>
<html lang="en" prefix="og: http://ogp.me/ns#">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- SEO -->
        <title>{self.title}</title>
        <meta name="description" content="{self.description}">

        <!-- URL CANONICAL -->
        <link rel="canonical" href="{self.url}">

        <!-- Google Fonts -->
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,100i,300,300i,400,400i,700,700i%7CMaitree:200,300,400,600,700&amp;subset=latin-ext" rel="stylesheet">

        <!-- CSS WebSlides -->
        <link rel="stylesheet" type='text/css' media='all' href="static/css/webslides.css">

        <!-- Optional - CSS SVG Icons (Font Awesome) -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css" integrity="sha512-+4zCK9k+qNFUR5X+cKL9EIR+ZOhtIloNl9GIKS57V1MyNsYpYcUrUeQc9vNfzsWfV28IaLL3i96P9sdNyeRssA==" crossorigin="anonymous" />

        <!-- SOCIAL CARDS (ADD YOUR INFO) -->

        <!-- FACEBOOK -->
        <meta property="og:url" content="{self.url}">
        <meta property="og:type" content="article">
        <meta property="og:title" content="{self.title}"> 
        <meta property="og:description" content="{self.description}">
        <meta property="og:updated_time" content="{datetime.today()}">
        <meta property="og:image" content="{self.image if self.image else "static/images/share-webslides.jpg"}">

        <!-- TWITTER -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="{self.title}"> 
        <meta name="twitter:description" content="{self.description}"> 
        <meta name="twitter:image" content="{self.image if self.image else "static/images/share-webslides.jpg"}">

        {self._generate_favicon_markup()}

        <!-- Android -->
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="theme-color" content="#f0f0f0">

        <!-- Code highlighting -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.4.0/styles/default.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.4.0/highlight.min.js"></script>
        <script>hljs.initHighlightingOnLoad();</script>

    </head>
    {self.navbar.__html__() if self.navbar else ""}
    <body>

    <main role='main'>
        <article id='webslides' {'class="vertical"' if self.vertical else ""}>
{self._generate_intro_slide()}
{slides_html}
{self._generate_endcard()}

        </article>
        <!-- end article -->
    </main>
    <!-- end main -->

    <!-- Required -->
    <script src='static/js/webslides.js'></script>
    <script>
        window.ws = new WebSlides();
    </script>

    <!-- OPTIONAL - svg-icons.js (fontastic.me - Font Awesome as svg icons) -->
    <script defer src='static/js/svg-icons.js'></script>

    </body>
    {self.footer.__html__() if self.footer else ""}
</html>
        '''
        return result


    def export(self, file_path:str, folder_name:Union[str, bool] = False, force:bool = False):
        """Exports the presentation files

        Parameters
        ----------
        file_path : (str)
            The path to export the folder of content to

        folder_name : (str or False)
            If you want to overwrite the folder name the output files are put in (defaults to Presentation.title), optional and defaults to False

        force : (bool)
            Whether to force generating files (overwrite existing files if found), optional and defaults to False

        Notes
        -----
        - all files are exported to file_path/folder_name
        - folder_name defaults to Presenation.title

        Raises
        ------
        FileExistsError
            If force is False, and a folder exists at file_path/folder_name

        Examples
        --------
        ### Export a presentation to the current directory at /Presentation
        ```
        from ezprez.core import Presentation
        prez = Presentation(title, description, url)

        # Export the files to the current directory at /Presentation
        prez.export(".", force=True, folder_name="Presentation")
        ```
        """
        if not folder_name:
            folder_name = self.title
        file_path = os.path.abspath(file_path)

        # finding downloads folder
        if os.name == "nt":
            DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
        else: # PORT: Assuming variable is there for MacOS and Linux installs
            DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads" 

        # check if webslides is downloaded, if it is use those files, if not download and extract it
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "webslides")):
            try:
                build(ZIPResource("webslides", "https://webslides.tv/webslides-latest.zip", overwrite_agreement=True))
                copytree(os.path.join(DOWNLOAD_FOLDER, "webslides"), os.path.join(os.path.dirname(__file__), "webslides"))
            except PermissionError:
                elevate()
                copytree(os.path.join(DOWNLOAD_FOLDER, "webslides"), os.path.join(os.path.dirname(__file__), "webslides"))
        try:
            copytree(os.path.join(os.path.dirname(__file__), "webslides"), os.path.join(file_path, folder_name))
        except FileExistsError:
            if force:
                rmtree(os.path.join(file_path, folder_name))
                copytree(os.path.join(os.path.dirname(__file__), "webslides"), os.path.join(file_path, folder_name))
            else:
                raise FileExistsError(f"The file path {os.path.join(file_path, folder_name)} exists, to replace use Presentation.export({file_path}, force=True)")

        # Copy image files
        if os.path.exists("./img"):
            for file_name in os.listdir("./img"):
                if os.path.isfile(os.path.join("img", file_name)):
                    copyfile(os.path.join("img", file_name), os.path.join(file_path, folder_name, "static", "images", file_name))
        elif os.path.exists("./images"):
            for file_name in os.listdir("./images"):
                if os.path.isfile(os.path.join("images", file_name)):
                    copyfile(os.path.join("images", file_name), os.path.join(file_path, folder_name, "static", "images", file_name))

        # replace index.html with generated html
        presentation_content = self.__html__()
        index_path = os.path.join(file_path, folder_name, "index.html")
        print(f"Writing html to {index_path}")
        with open(index_path, "w+") as presentation_file:
            presentation_file.write(presentation_content)
