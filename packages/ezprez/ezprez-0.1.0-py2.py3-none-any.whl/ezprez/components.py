"""The module that contains all component subclasses that can be used to generate Slide content

Classes
-------
#### SocialLink
Can be used to create a social media link icon, or just the icon

#### Link
A component for generating web links

#### Code
A component for adding code demos with syntax highlighting

#### Icon
A component that generates an icon

#### F‎ooter_
Allows you to add a footer to the presentation

#### Navbar
Allows you to add a navbar to the presentation

#### Button
A component that allows you to add html buttons

#### Raw
A component that dumps provided raw html

#### TableOfContents
A component used to generate table of contents for a presentation

#### Video
A component that allows you to embed a youtube video

#### Image
A component to include images

#### Grid
A component that allows you to evenly space multiple peices of content
"""
# Internal Dependencies
import enum
from abc import ABC
from typing import List, Union
from dataclasses import dataclass


class _Component(ABC):
    """Base class used for type checking, and inheritance on all components"""
    def __html__(self) -> str:
        raise NotImplementedError("Components require a __html__() method to be defined")


class SocialLink(enum.Enum):
    """Can be used to create a social media link icon, or just the icon

    Notes 
    -----
    - If you don't call the object's link function, it will just return the social media icon

    Examples
    -------
    ### Adding an icon link to someone's github in a navbar
    ```
    from ezprez.core import Presentation
    from ezprez.components import SocialLink, Navbar

    header = Navbar('Basic web technologies', [SocialLink.github.link("https://github.com/descent098")])
    Presentation(title, url, content, navbar=header)
    ```

    ### Adding an icon with no link to a Slide
    ```
    from ezprez.core import Slide
    from ezprez.components import SocialLink

    Slide('This is a youtube icon with no link', SocialLink.youtube)
    ```
    """
    url:str
    icon_color:str
    youtube = 0
    github = 1
    twitter = 2
    linkedin = 3
    twitch = 4


    def link(self, link):
        """Function used to asign URL parameter to the link

        Parameters
        ----------
        link : (str)
            The url you want to link to

        Returns
        -------
        The instance called from
        """
        self.url = link
        return self

    def color(self, color:str):
        """Function used to asign color parameter

        Parameters
        ----------
        color : (str)
            The color you want the icon to be

        Returns
        -------
        The instance called from
        """
        self.icon_color = color
        return self


    def __html__(self, header:bool = False) -> str:
        try: # If no icon_color is set
            self.__getattribute__("icon_color")
        except AttributeError:
            self.icon_color = "#141414"

        try: # If no url is set
            self.__getattribute__("url")
        except AttributeError:
            self.url = "#"

        if header:
            return f"""\n\t\t\t\t\t<a href='{self.url}' target='_blank' rel='external' style='background-color:#fff; color:{str(self.icon_color)};'>
                                <i class='fab fa-{self.name} fa-3x'></i>
                            </a>\n"""
        else:
            return f"""\n\t\t\t\t\t<a href='{self.url}' target='_blank' rel='external' style='color:{str(self.icon_color)};'>
                                <i class='fab fa-{self.name} fa-3x'></i>
                            </a>\n"""


@dataclass
class Link(_Component):
    """A component for generating web links

    Attributes
    ----------
    label : (str)
        The text shown that the link is applied to

    link : (str)
        The link to tie the label to

    Examples
    -------
    ### Add a link to google to a slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Link

    Slide('This is a link to Google', Link('Click this to go to google', 'https://google.ca'))
    ```
    """
    label: str
    link: str
    color: str = "#4dd"


    def __html__(self, header:bool = False) -> str:
        if not header:
            return f"""\n\t\t\t\t\t<a href={self.link} target='_blank' rel='external' style='color:{self.color};'>{self.label}</a>\n"""
        else:
            return f"""\n\t\t\t\t\t<a href={self.link} target='_blank' rel='external' style='background-color:#fff; color:#141414;'>{self.label}</a>\n"""


@dataclass
class Code(_Component):
    """A component for adding code demos with syntax highlighting

    Attributes
    ----------
    language: (str)
        The programming language (Supports all the common languages listed on https://highlightjs.org/download/ )

    content: (str)
        The code to show off

    Notes
    -----
    - Uses highlightJS for syntax highlighting: https://highlightjs.org/download/

    Examples
    --------
    ### Add some html example code to a slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Code

    Slide("Here is some example html", Code("html", "<p>This is some example code</p>"))
    ```
    """
    language: str
    content: str


    def _escape(self) -> str:
        """Escapes self.content so it's HTML safe

        Returns
        -------
        str
            The escaped string of content
        """
        self.content = self.content.replace("<", "&lt").replace(">", "&gt").replace("&", "&amp")
        return self.content


    def __html__(self) -> str:
        return f"""\t\t\t\t\t<pre><code class='language-{self.language.lower()}'>{self._escape()}</code></pre>\n"""


@dataclass
class Icon(_Component):
    """A component that generates an icon

    Attributes
    ----------
    label: (str)
        The icon name i.e. 'fa-heart' (details at https://fontawesome.com/)

    size: (str), optional;
        The size of icon, i.e. 60px, defaults to 48px

    Examples
    -------
    ### Put a heart icon in the middle of a slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Icon

    Slide("This is a heart icon", Icon("fa-heart"))
    ```
    """
    label: str
    size: str = "48px"
    color: str = "#141414"


    def __html__(self) -> str:
        return f"""\t\t\t\t\t<svg class='{self.label}' style='width:{self.size};height:{self.size};color:{self.color};'><use xlink:href='#{self.label}'></use></svg>\n"""


@dataclass
class Footer(_Component):
    """Allows you to add a footer to the presentation

    Attributes
    ----------
    links: (list[Link or SocialLink])
        A list of Link's or SocialLink's to include in the footer

    Examples
    --------
    ### Adding a footer with a github link to a presentation
    ```
    from ezprez.core import Presentation
    from ezprez.components import Footer

    foot = Footer([SocialLink.github.link("https://github.com/Descent098/ezprez-example")])
    Presentation(title, description, url, footer=foot)
    ```
    """
    links: List[Union[Link, SocialLink]]


    def __html__(self) -> str:
        result =f"""
        <footer>
        """

        for link in self.links:
            if type(link) == Link or type(link) == SocialLink:
                result += f"\n\t\t\t{link.__html__()}\n"
            else:
                raise ValueError(f"Footer arguments must be of type ezprez.components.Link or ezprez.components.SocialLink, got \n\ttype {type(link)}\n\tValue{link}")

        result += """
        </footer>\n
        """
        return result


@dataclass
class Button(_Component):
    """A component that allows you to add html buttons

    Attributes
    ----------
    label: (str)
        The text that is shown on the button
    
    url: (str)
        The url the button links to
    
    icon: (False or Icon)
        Provide an Icon component to display in the button, optional and defaults to False
    
    ghost: (bool)
        Whether to not fill a color, optional and defaults to False
    
    rounding: (bool)
        Whether to round the corners of the button or not, optional and defaults to True
    
    color: (False or str)
        The color of the button, optional and defaults to False
    
    text_color: (False or str)
        The color of the button text, optional and defaults to False

    Notes 
    -----
    - The color and text_color attribute takes an HTML color as a string i.e. #f0f0f0, blue, rgba(255, 255, 255, 0.9)
    - If ghost is set to True all other colors will be ignored
    - The URL parameter also can use anchor links to other slides

    Examples
    --------
    ### Adding a button to a slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Button

    b = Button("click me", "https://kieranwood.ca")
    Slide("Here's a button", b)
    ```
    """
    label: str # The text to put inside the button
    url: str # The url to link the button to
    icon: Union[bool, Icon] = False # The icon to put on the button (if you want one)
    ghost: bool = False # Whether to fill in a color or use ghost styling
    rounding: bool = True # Whether to round
    color: Union[bool, str] = False # The color to make the button
    text_color: Union[bool, str] = False # The color to make the button text

    def __html__(self) -> str:
        color_string = ""
        if self.color and self.text_color and not self.ghost:
            color_string = f"style='background-color:{self.color};color:{self.text_color};'"
        elif self.color or self.text_color and not self.ghost:
            color_string = "style="
            if self.color:
                color_string += f'\"background-color:{self.color};\"'
            if self.text_color:
                color_string += f'\"color:{self.text_color};\"'

        return f"""\n\t\t\t<a href='{self.url}' class='button{' ghost' if self.ghost else ''}{' radius' if self.rounding else ''}' {color_string}>{self.icon.__html__() if self.icon else ''} {self.label} </a>\n"""


@dataclass
class Navbar(_Component):
    """Allows you to add a navbar to the presentation

    Attributes
    ----------
    title: (str)
        The presentation title (used for accessibility reasons)

    links: (list[Link or SocialLink])
        A list of Link's or SocialLink's to include in the Navbar

    Examples
    --------
    ### Adding a Navbar with a github link to a presentation
    ```
    from ezprez.core import Presentation
    from ezprez.components import Navbar

    nav = Navbar('Presentation title', [SocialLink.github.link("https://github.com/Descent098/ezprez-example")])
    Presentation(title, description, url, navbar=nav)
    ```
    """
    title: str
    links: List[Union[Link, SocialLink]]


    def __html__(self) -> str:
        result =f"""
        <header role="banner">
            <nav role="navigation">
                <p class="logo"><a href="" target="_blank" title="{self.title}">{self.title}</a></p>
                <ul>
        """

        for link in self.links:
            if type(link) == Link or type(link) == SocialLink:
                result += f"\n\t\t\t\t\t<li>{link.__html__(header=True)}</li>\n"
            else:
                raise ValueError(f"Navbar arguments must be of type ezprez.components.Link or ezprez.components.SocialLink, got \n\ttype {type(link)}\n\tValue{link}")
        result += """
                </ul>
            </nav>
        </header>
        """

        return result


@dataclass
class Raw(_Component):
    """A component that dumps provided raw html

    Attributes
    ----------
    content: (str) 
        The HTML content to generate

    Examples
    -------
    ### Add a manual paragraph tag to a Slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Raw

    content = '<p>This is some text</p>'

    Slide('This is some raw content', Raw(content))
    ```
    """
    content:str


    def __html__(self) -> str:
        return self.content

@dataclass
class TableOfContents(_Component):
    """A component used to generate table of contents for a presentation

    Attributes
    ----------
    sections: (dict)
        A dictionary of {label:slide_number}'s to generate the table of contents with

    Examples
    ----------
    ### Create a table of contents Slide for a presentation
    ```
    from ezprez.core import Slide
    from ezprez.components import TableOfContents

    # The argument is a dictionary where each key is the label in the table
    # and each value is the slide number
    sections = {'Intro':2, 'End': 5}

    Slide('Table of contents', TableOfContents(sections))
    ```
    """
    sections: dict


    def __html__(self) -> str:
        result = "\n\t\t<hr>\n\t\t<div class='toc'>\n\t\t\t<ol>"
        for section_title in self.sections:
            result += f"\n\t\t\t\t<li>\n\t\t\t\t\t<a href='#slide={self.sections[section_title]}' title='Go to {section_title}'>\n\t\t\t\t\t<span class='chapter'>{section_title}</span>\n\t\t\t\t\t<span class='toc-page'>{self.sections[section_title]}</span>\n\t\t\t\t</a></li>"
        result += "\n\t\t\t</ol>\n\t\t</div>\n"
        return result 


@dataclass
class Video(_Component):
    """A component that allows you to embed a youtube video

    Attributes
    ----------
    video_id: (str)
        The youtube video id, for example if the url is youtube.com/watch?v=wSVljLh1VmI then the id is 'wSVljLh1VmI'

    Examples
    --------
    ### Adding a youtube video to a Slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Video

    Slide('Here is a video', Video('wSVljLh1VmI'))
    ```
    """
    video_id: str

    def __html__(self) -> str:
        return f"""\n\t\t\t\t<div class='embed'>\n\t\t\t\t\t<iframe src='https://www.youtube.com/embed/{self.video_id}' frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen ></iframe>\n\t\t\t\t</div> """

@dataclass
class Image(_Component):
    """A component to include images

    Attributes
    ----------
    title: (str) 
        The alternate text to describe what an image is

    filename: (str)
        The filename of the image

    browser: (bool)
        If true you can add a browser window border to the image https://webslides.tv/demos/components#slide=114

    width: (int or False)
        Used to override the width of an image, optional and defaults to False

    height: (int or False)
        Used to override the height of an image, optional and defaults to False

    Notes
    -----
    - All images must be included in the same directory as the presentation source file under /img or /images

    Examples
    --------
    ### Add an image to a slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Image

    Slide("This is an image", Image("low poly ice caps", "kieran-wood-lp-ice-caps-4k-w-peng.jpg"))
    ```

    ### Add a background image to a slide
    ```
    from ezprez.core import Slide
    from ezprez.components import Image

    Slide("This is a background image", image=Image("low poly ice caps", "kieran-wood-abstract-landscape.jpg"), background="black")
    ```
    """
    title: str
    filename: str
    browser: bool = False
    width: Union[bool, int] = False
    height: Union[bool, int] = False

    def __html__(self) -> str:
        if not self.browser:
            return f"""<img src='./static/images/{self.filename}' alt='{self.title}'{f' width={self.width} ' if self.width else ''} {f' height={self.height} ' if self.height else ''}>"""
        else:
            return f"""<figure class='browser'><img src='./static/images/{self.filename}' alt='{self.title}'{f' width={self.width} ' if self.width else ''} {f' height={self.height} ' if self.height else ''}></figure>\n """


class Grid(_Component):
    """A component that allows you to evenly space multiple peices of content

    Attributes
    ----------
    contents: (Component, str, List[Component], List[str])
        The contents you want to include in the grid

    Examples
    --------
    ### Add a grid with content
    ```
    from ezprez.core import Slide
    from ezprez.components import Grid

    Slide("You can also have grids", Grid("With", "Lots", "of", "content"))
    ```

    ### Add a slide of a grid of lists
    ```
    from ezprez.core import Slide
    from ezprez.components import Grid

    Slide("Like, alot of content...", Grid(["You can stack content within grids", ["like this", "and this", "and even this"]], ["This is getting too much now", ["way", "way way", "too much"]]))
    ```
    """
    def __init__(self, *contents:Union[_Component, str, List[_Component], List[str]]):
        self.contents = contents

    def __html__(self):
        result = "\n\t\t\t\t<div class='grid'>"
        for content in self.contents:
            if type(content) == str:
                result += f"\n\t\t\t\t\t<div class='column'><p>{content}</p></div>\n"
            elif isinstance(content, _Component):
                result += "\n\t\t\t\t\t<div class='column'>"
                result += content.__html__()
                result += "</div>"
            elif type(content) == list:
                result += "\n\t\t\t\t\t<div class='column'>"
                for subcontent in content:
                    if isinstance(subcontent, _Component):
                        result += subcontent.__html__()
                    elif type(subcontent) == str:
                        result += f"\n\t\t\t\t\t<p>{subcontent}</p>\n"
                    elif type(subcontent) == list:
                        result += "\n\t\t\t\t\t<ul>"
                        for point in subcontent:
                            result += f"\n\t\t\t\t\t<li>{point}</li>\n"
                        result += "\n\t\t\t\t\t</ul>"
                result += "\n\t\t\t\t\t</div>"
            else:
                raise ValueError(f"Provided content to Grid was {type(content)}, which is not List, Component or string")
        return result