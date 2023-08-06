"""extention to tk

adds the syntax and coordinate changes creatid in AM to a clean setup
"""
import tkinter
import typing

__all__ = ["Canvas", "Tk"]

imageType = typing.NewType("image", tkinter.PhotoImage)
"the type used for internal typing of the tkinter.photoImage"


class Canvas(tkinter.Canvas):
    """extended canvas

    a overide to the tk canvas with all the functionality
    of oure AM write function just cleaner
    """
    def __init__(self, *args: tuple, **kwargs: dict):
        """contructor 

        @param master: the master as discribed in tk doc\n
        @type master: tkinter.Tk
        @param origin: the origin defautl is 0,0\n
        @type origin: tuple<int, int>
        @param bd: Border width in pixels. Default is 2.
        @param bg: Normal background color.
        @param confine: If true (the default), the canvas cannot be scrolled outside of the scrollregion.
 	    
        @param height: Size of the canvas in the Y dimension.
        @param cursor: Cursor used in the canvas like arrow, circle, dot etc.
        @param highlightcolor: Color shown in the focus highlight.
        @param relief: Relief specifies the type of the border. Some of the values are SUNKEN, RAISED, GROOVE, and RIDGE.
        @param scrollregion: A tuple (w, n, e, s) that defines over how large an area the canvas can be scrolled, where w is the left side, n the top, e the right side, and s the bottom.
        @param width: Size of the canvas in the X dimension.
        @param xscrollincrement: If you set this option to some positive dimension, the canvas can be positioned only on multiples of that distance, and the value will be used for scrolling by scrolling units, such as when the user clicks on the arrows at the ends of a scrollbar.
        @param xscrollcommand: If the canvas is scrollable, this attribute should be the .set() method of the horizontal scrollbar.
        @param yscrollincrement: Works like xscrollincrement, but governs vertical movement.
        @param yscrollcommand: If the canvas is scrollable, this attribute should be the .set() method of the vertical scrollbar.
        """
        ##@param cursor: Cursor used in the canvas like arrow, circle, dot etc.
        #init origin
        self.setOrigin(kwargs["origin"] if "origin" in kwargs.keys() else (0,0))
        try: kwargs.pop("origin")
        except: pass


        super(Canvas, self).__init__(*args, **kwargs)
    

    def setOrigin(self, *origin: typing.Tuple[int, int]) -> None:
        """set the origin of the canvas

        @param origin: the new origin
        @type origin: tuple<int, int>
        """
        origin = origin[0] if isinstance(origin[0], tuple) else origin
        assert isinstance(origin, (tuple, list)), f"origin must be a tuple of ints not {type(origin)}"
        assert len(origin) == 2, f"invalid origin point len for 2d space {origin} must be tuple of len 2"
        assert isinstance(origin[0], (float, int)), f"invalid positon {origin} elements must be ints not {type(origin[0])}"
        assert isinstance(origin[1], (float, int)), f"invalid positon {origin} elements must be ints not {type(origin[1])}"

        self.origin = origin
        "the origin of the coordiante system set with setOrigin"
    
    def get_cor(self, x: int, y: int) -> typing.Tuple[int, int]:
        """conversion to tk coordiate system

        @param x, y: the x, y positons to be converted
        @type x, y: int
        """
        assert hasattr(x, "__int__"), f"x must be an int not {type(x)}"
        assert hasattr(y, "__int__"), f"y must be an int not {type(y)}"
        x, y = int(x), int(y)
        dx, dy = self.origin
        return (x+dx, dy-y)
    
    def create_rectangle(self, x: int, y: int, x2: int, y2: int, fillColor: str="white", outlineColor:str="black") -> None:
        """crate a rectange

        crate a rectangel with cornen points (x, y) and (x2, y2)
        @param x, y: the pos of the fist point
        @type x, y : int
        @param x2, y2: the position to the second point
        @type x2, y2: int

        @param fillColor: the color to fill the rectangle with

        @param outlineColor: the outline color of the rectangle
        """
        x, y = self.get_cor(x,y)
        x2, y2 = self.get_cor(x2, y2)
        tkinter.Canvas.create_rectangle(self, x, y, x2, y2, fill=fillColor, outline=outlineColor)

    def create_square(self, x:int, y:int, a:int=1, fillColor: str="white", outlineColor:str="black") ->None:
        """creates a square

            creats a quare around x, y with side len a

            @param x, y: the pos of the center of the square
            @type x, y: int
            
            @param a: the side length of the suqare defaults to 1
            @type a: int

            @param fillColor: the color to fill the rectangle with
            @param outlineColor: the outline color of the rectangle"""
        assert hasattr(x, "__int__"), f"x must be an int not {type(x)}"
        assert hasattr(y, "__int__"), f"y must be an int not {type(y)}"
        assert hasattr(a, "__int__"), f"a must be an int not {type(a)}"
        a, x, y = int(a)/2, int(x), int(y)
        self.create_rectangle(x+a, y+a, x-a, y-a, fillColor=fillColor, outlineColor=outlineColor)

    def create_line(self, x: int, y: int, x2: int, y2: int, color: str="black", width: int = 1) -> None:
        """crates line

        crates a line form (x, y) to (x2, y2)

        @param x: the x pos of point 1
        @type x: int
        @param y: the y pos of point 1
        @type y. int
        @param x: the x pos of point 2
        @type x: int
        @param y: the y pos of point 2
        @type y. int

        @param color: the color of the line
        
        @param width: the width of the line
        @type width: int
        """
        assert hasattr(width, "__init__"), f"width must be int not {type(width)}"
        x, y = self.get_cor(x, y)
        x2, y2 = self.get_cor(x2, y2)
        tkinter.Canvas.create_line(self, x, y, x2, y2, fill=color, width=width)

    def create_oval(self, x: int, y: int, x2: int, y2: int, color: str="white", outline: str="black") ->None:
        """crates line

        crates an oval form (x, y) to (x2, y2)

        @param x: the x pos of point 1
        @type x: int
        @param y: the y pos of point 1
        @type y. int
        @param x: the x pos of point 2
        @type x: int
        @param y: the y pos of point 2
        @type y. int

        @param color: fillcolor of the oval
        
        @param outline: the outline color of the oval
        """
        x, y = self.get_cor(x,y)
        x2, y2 = self.get_cor(x2, y2)
        tkinter.Canvas.create_oval(self, x, y, x2, y2, fill=color, outline=outline)

    def create_circle(self, x: int, y: int, r: int, color: str="white", outline: str="black") ->None:
        """create a circle

            crate a circle around (x, y) with radius r and color color aswellas outlien color outline

            @param x: the x cor of the center of the circle
            @type x: int
            
            @param y: the y cor of the center of the circle
            @type y: int

            @param r: the radius of the circle
            @type r: int

            @param color: the fill color fo the circle
            @param outline: the outline color fo the circle
        """
        return self.create_oval(x+r, y+r, x-r, y-r, color, outline)
    
    def create_polygon(self, *points: typing.Tuple[typing.Tuple[int, int]], color: str="white", outline: str="black", width:int=1) ->None:
        """crates a poligon

            crate a poligon around the points passed a tupples via *points

            >>> cv = Canvas(master)
            >>> cv.pack()
            >>> cv.crate_poligon((x, y), (x2,y2) .., color, outlineColor)

            @param points: a tuple containing the positions of the corners of the poligon
            @type points: tuple(*tuple(int, int))

            @param color: the fill color fo the poligon
            @param outline: the outline color fo the poligon

            @param width: the with of the outline\n
                            defaults to 1
            @type width: int
        """
        assert hasattr(width, "__init__"), f"width must be an int not {type(width)}"# make sure width can be converted to int
        new = []
        for x, y in points:
            nx, ny = self.get_cor(x, y)
            new.append(nx)
            new.append(ny)
        tkinter.Canvas.create_polygon(self, new, fill=color, outline=outline, width = int(width))

    def create_bitmap(self, x: int, y: int, bit: str)->None:
        """crate a bitmap

            The method create_bitmap() can be be used to include a bitmap on a canvas. The following bitmaps are available on all platforms:
            "error", "gray75", "gray50", "gray25", "gray12", "hourglass", "info", "questhead", "question", "warning" 
            see tkinter doc for details

            
            @param x, y: the x y postion of the result
            @type x, y; int

            @param bit: the bit to be renderd
            @type bit: i dont have the fogierst idear
            """
        x, y = self.get_cor(x, y)
        tkinter.Canvas.create_bitmap(x, y, bit)
    
    def create_image(self, x:int, y:int, img: imageType, **kwargs)->None:
        """render image

            The Canvas method create_image(x0,y0, options ...) is used to draw an image on a canvas. create_image doesn't accept an image directly. It uses an object which is created by the PhotoImage() method. The PhotoImage class can only read GIF and PGM/PPM images from files
        
            >>> cv.crate_image(10, 10, rocks.ppm)

            @param x: the x cor of the image
            @type x: int
            @param y: the y cor of the image
            @type y: int
            @param img: the image 
            @type img: str (path) or tkinter.photoImage
            """ 
        if isinstance(img, str):
            img = tkinter.PhotoImage(file = img)
        
        assert hasattr(x, "__int__"), f"x must be int not {type(x)}"
        assert hasattr(y, "__int__"), f"y must be int not {type(y)}"
        assert type(img) is tkinter.PhotoImage, f"img must be photoImage not {type(img)}"
        print(type(img))
        kwargs["image"] = img
        x, y = self.get_cor(x, y)
        return tkinter.Canvas.create_image(self, x, y, image=img)

    def create_text(self, x: int, y: int, **kwargs) ->None:
        """create a text object

            crate tk text object

            @param x: the x pos of the text widget
            @type x: int
            @param y: the y pos of the text widget
            @type y: int
            """
        
        assert hasattr(x, "__int__"), f"x must be and int not {type(x)}"
        assert hasattr(y, "__int__"), f"y must be and int not {type(y)}"
        x, y = self.get_cor(x, y)
        tkinter.Canvas.create_text(self, x, y, **kwargs)

    def create_arc(self, x: int, y: int, x2:int, y2: int, **kwargs) ->None:
        """create an arc

            creats an arc from x, y to x2, y2

            @param x, y, x2, y2: the postions of the values
            @type x, y, x2, y2: int
            """
        
        assert hasattr(x, "__int__"), f"x must be an int not {type(x)}"
        assert hasattr(y, "__int__"), f"y must be an int not {type(y)}"
        assert hasattr(x2, "__int__"), f"x2 must be an int not {type(x2)}"
        assert hasattr(y2, "__int__"), f"y2 must be an int not {type(y2)}"

        x, y = self.get_cor(x, y)
        x2, y2 = self.get_cor(x2, y2)

        tkinter.Canvas.create_arc(self, x, y, x2, y2, **kwargs)

    def plot(self, fun, top:int=500, bottom:int=-500, scale:float=1, dx:float =0, dy:float=0, color: str="black", width:int =1) -> None:
        """plots a function

            plots a function 

            @param fun: the function to plot
            @type fun: function [carefull no assersion]

            @param top: the top x to plot (default to 1000)
            @type top: int

            @param bottom: the bottom x to plot (defaults to -1000)
            @type bottom: int

            @param scale: the scale of the plot
            @type scale: float

            @param dx: move x to the side
            @type dx: float

            @param dy: move plot to y side
            @type dy: float"""

        func = lambda x: fun((x-dx)/scale)*scale + dx
        x, y = bottom, func(bottom)
        while bottom < top:
            bottom += 1
            newx, newy = bottom, func(bottom)
            self.create_line(x, y, newx, newy, color, width)




class Tk(tkinter.Tk):
    """extended Tk

    an overide for tkinter tk with the custom functionaliy form am
    currently empty
    """
    @staticmethod
    def _(a):return