import pygame
import random
import os
import math
import numpy as np

DARK_RED = (139, 0, 0)
YELLOW = (235, 195, 65)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (30, 144, 255)
CYAN = (47, 237, 237)
RED = (194, 57, 33)
LIME_GREEN = (50, 205, 50)
LIGHT_RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
LIGHT_PINK = (255, 182, 193)
DARK_GREEN = (1, 100, 32)
PURPLE = (181, 60, 177)
BROWN = (150, 75, 0)
DARK_GREY = (52, 52, 52)


class Memory:
    """
    Class used to store data across game instances
    """

    def __init__(self, width, height):
        self.res_width = width
        self.res_height = height
        self.music = None

    def load_game(self):
        """ Load previous game instance, usually from a text_file"""
        pass

    def load_scenes(self):
        """ Load all scenes from a text file"""
        pass


class Text:
    """
    Class used to simplify text creation for pygame
    """

    def __init__(self, text, text_pos, font_size, font_type,
                 font_color, text_other):
        self.text = text  # Text as a string
        self.position = text_pos  # Text position as a tuple or list (x and y)
        self.font_size = int(font_size)  # Int determining how big the text is
        self.font_type = font_type  # String used to indicate what font
        """Font selection is determined by your computer and it's preset fonts
        """
        self.color = font_color
        """A constant string for a tuple or a tuple using RGB values"""
        self.other = text_other
        """PLACEHOLDER for any other variables needed or desired in text"""
        self.font = None  # Initialized here, defined in setup()
        self.text_rect = None  # Initialized here, defined in render()
        self.text_img = None  # Initialized here, defined in render()

        self.setup()  # Called to set up the font
        self.render()
        """Called to continuously update the position, rect, color, and text
        """

    def setup(self):
        """
        Uses font type and size to translate into pygame text font
        to make self.font
        """
        self.font = pygame.font.SysFont(self.font_type, self.font_size)

    def render(self):
        """
        Creates self.text_img or the pygame image of the text using self.text,
            self.color.
        Creates self.text_rect, or a rect object using the size of the text.
        Then centers the rect around the text (or the defined position)
        """
        self.text_img = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.center = self.position

    def scale(self, width, height):
        self.position = list(self.position)
        self.position[0] = int(self.position[0] * width)
        self.position[1] = int(self.position[1] * height)
        self.position = tuple(self.position)
        self.font_size = int(self.font_size * max(width, height))

        # Apply those changes
        self.setup()
        self.render()


class Scene:
    """
    Class template for creating scene based games
    """

    def __init__(self):
        """
        self.this_scene will tell the current scene it's on at that moment.
        Currently, it's set to itself, which means the
        current scene is this one.
        """
        self.this_scene = self
        self.run_scene = True
        self.level_id = -1

    def input(self, pressed, held):
        # this will be overridden in subclasses
        """
        This function should contain the pressed for loop and other held
        buttons. Pressing or holding these buttons should cause something
        to change such as a class variable (+= 1, True/False, change str.. etc.)
        or call another function.

        :param pressed: Detect buttons that are pressed (like if held, it will
        only be updated with the initial press)
        :param held: Detect buttons that are held down
        :return:
        """
        pass

    def update(self):
        # this will be overridden in subclasses
        """
        This function should check for variables that need to be updated
        continuously. A good way to distinguish this from input is that this
        update function doesn't directly respond from a button press. For
        example, let's have input add to self.x by 1, or self.x += 1. Then, if
        we wanted to keep self.x within the bounds of 0 to 10, we check for that
        in update. In update, we'd use if self.x < 0 and 10 < self.x to check
        whenever self.x goes out of these bounds to then reset self.x.

        :return:
        """
        pass

    def render(self, screen):
        # this will be overridden in subclasses
        """
        This function is solely used for rendering purposes such as
        screen.blit or pygame.draw
        :param screen:
        :return:
        """
        pass

    def change_scene(self, next_scene):
        """
        This function is used in the main pygame loop. This function is
        responsible for formally changing the scene
        """
        self.this_scene = next_scene

    def close_game(self):
        """
        Set the current scene to nothing and is used to stop the game.
        This function is responsible for ending the game loop (or scene)
        formally.
        """
        self.change_scene(None)


class Map(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.datapoints = []
        self.mouse = pygame.Rect(0, 0, 1, 1)
        self.select_point = None
        self.show_select = False
        self.sort_mode = 0

        self.x_offset = 0
        self.y_offset = 0

        self.follow_mouse = False

        self.edit_options = [pygame.Rect(1, 1, 1, 1),  # Icon color
                             pygame.Rect(2, 2, 1, 1),  # Icon location
                             pygame.Rect(3, 3, 1, 1)]  # Icon radius
        self.edit_modes = [self.mode_0,
                           self.mode_1,
                           self.mode_2,
                           self.mode_3
                           ]
        self.current_mode = 0
        """
        Reflects the corresponding edit options in human indices
        1: icon color
        2: icon location
        3: icon radius
        
        We reserve 0 for no options
        """

    def input(self, pressed, held):
        for action in pressed:
            if action == pygame.MOUSEMOTION:
                self.mouse.x = pygame.mouse.get_pos()[0]
                self.mouse.y = pygame.mouse.get_pos()[1]

            if action == pygame.MOUSEBUTTONDOWN:
                self.edit_modes[self.current_mode]()

            if action == pygame.MOUSEBUTTONUP and self.follow_mouse:
                self.follow_mouse = False

            if action == pygame.K_ESCAPE:
                self.run_scene = False

    def mode_0(self):
        # Move and add points
        point_index = 0
        mouse_point = DataPoint()
        mouse_point.change_icon_location(self.mouse.x,
                                         self.mouse.y)
        check_select = True

        while 0 < len(self.datapoints) and \
                (point_index < len(self.datapoints)):
            if self.select_point is self.datapoints[point_index] and \
                    self.calculate_mouse(self.datapoints[
                                             point_index]):
                self.follow_mouse = True
                check_select = False
            elif self.calculate_mouse(
                    self.datapoints[point_index]):
                self.select_point = self.datapoints[point_index]
                self.select_point.icon.display_options = True
                check_select = False

            point_index += 1

        if -1 < self.mouse.collidelist(self.edit_options) and \
                self.select_point is not None and \
                self.select_point.icon.display_options:
            # Edit options when clicked
            self.current_mode = self.mouse.collidelist(
                self.edit_options) + 1

        elif check_select:
            check_dist = True
            for point in self.datapoints:
                if self.calculate_mouse(point):
                    check_dist = False

            if check_dist:
                # Make a new point, only if it's far away from other points
                self.select_point = None
                new_point = DataPoint()
                new_point.change_icon_location(self.mouse.x,
                                               self.mouse.y)
                self.datapoints += [new_point]

        elif self.select_point is not None:
            self.update_option_pos()

    def mode_1(self):
        # On left click, find a valid point to click on that's not our point

        # Adding a line, must be more than 1 point
        if 1 < len(self.datapoints):
            find_point = False
            point_index = 0
            while not find_point and point_index < len(self.datapoints):
                if find_point is not self.select_point:
                    find_point = self.calculate_mouse(
                        self.datapoints[point_index])
                point_index += 1

            if find_point:
                self.select_point.add_point(find_point)
            else:
                self.select_point = None
                self.show_select = False
                self.current_mode = 0
        else:
            # No other points available, return to default mode
            self.current_mode = 0
            self.select_point = None
            self.show_select = False

    def mode_2(self):
        pass

    def mode_3(self):
        pass

    def update(self):
        if self.select_point is not None and \
                not self.select_point.icon.display_options:
            self.select_point = None

        if self.follow_mouse and self.select_point is not None:
            self.select_point.change_icon_location(self.mouse.x,
                                                   self.mouse.y)
            self.update_option_pos()

    def render(self, screen):
        screen.fill(WHITE)

        for each_point in self.datapoints:
            each_point.render(screen)

        if self.select_point is not None and \
                self.select_point.icon.display_options:
            for each_option in self.edit_options:
                pygame.draw.rect(screen, ORANGE, each_option, 1)

    def calculate_mouse(self, point_b):
        """Point a is self.mouse
        Point b is any datapoint
        """
        hitbox_mod = 5  # Radius size, change for more/less cluttering

        if math.sqrt((self.mouse.x - point_b.icon.center[0]) ** 2 + \
                     (self.mouse.y - point_b.icon.center[
                         1]) ** 2) <= point_b.icon.radius * hitbox_mod:
            # Top left corner
            return point_b
        elif math.sqrt((self.mouse.x + self.mouse.width -
                        point_b.icon.center[0]) ** 2 + \
                       (self.mouse.y - point_b.icon.center[
                           1]) ** 2) <= point_b.icon.radius * hitbox_mod:
            # Top right corner
            return point_b
        elif math.sqrt((self.mouse.x - point_b.icon.center[0]) ** 2 + \
                       (self.mouse.y + self.mouse.height -
                        point_b.icon.center[
                            1]) ** 2) <= point_b.icon.radius * hitbox_mod:
            # Bottom left corner
            return point_b
        elif math.sqrt((self.mouse.x + self.mouse.width -
                        point_b.icon.center[0]) ** 2 + \
                       (self.mouse.y + self.mouse.height -
                        point_b.icon.center[
                            1]) ** 2) <= point_b.icon.radius * hitbox_mod:
            # Bottom right corner
            return point_b
        else:
            # No points detected
            return None

    def calculate_distance(self, point_a, point_b):
        """Point a is self.mouse
        Point b is any datapoint
        """
        hitbox_mod = 5  # Radius size, change for more/less cluttering

        if math.sqrt((point_a.icon.center[0] - point_b.icon.center[0]) ** 2 +
                     (point_a.icon.center[1] -
                      point_b.icon.center[1]) ** 2) <= \
                point_b.icon.radius * hitbox_mod:
            return point_b
        else:
            # No points detected
            return None

    def update_option_pos(self):
        size = 20  # How big each icon should be
        offset = 10  # How far each icon is from the point
        for option_ind in range(len(self.edit_options)):
            self.edit_options[option_ind].x = \
                self.select_point.icon.center[0] + \
                (size * option_ind) + offset
            self.edit_options[option_ind].y = \
                self.select_point.icon.center[1] - size - offset
            self.edit_options[option_ind].width = size
            self.edit_options[option_ind].height = size


class DataPoint:
    def __init__(self):
        self.title = Text("", [0, 0], 24, "impact", BLACK, None)
        self.description = [""]
        self.icon = Circle(DARK_GREEN, [0, 0], 3)
        self.associated = []  # Other points related/connecting to this one
        self.line_color = []  # Line colors for connecting related points

    def change_title(self, in_text):
        self.title.text = in_text

    def change_description(self, in_desc):
        self.description = [""]
        desc_len = len(in_desc)
        max_char = 50  # How many characters per line
        for each_line in range(0, desc_len, max_char):
            self.description += [each_line]

    def change_icon_color(self, new_color):
        self.icon.color = new_color

    def change_icon_location(self, x, y):
        self.icon.center = [x, y]

    def change_icon_radius(self, new_radius):
        self.icon.radius = new_radius

    def add_point(self, in_point):
        # Add associated points to connect to this one
        self.associated += [in_point]
        self.line_color += [RED]

    def remove_point(self, in_point):
        del self.associated[self.associated.index(in_point)]

    def render(self, screen):
        self.icon.render(screen)
        if 0 < len(self.associated):
            for li in range(len(self.associated)):
                pygame.draw.line(screen, self.line_color[li],
                                 self.icon.center,
                                 self.associated[li].icon.center)


class Circle:
    def __init__(self, in_color, location, in_radius):
        self.color = in_color
        self.center = location
        self.radius = in_radius

        self.display_options = False

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)


class Program:
    """
    Class responsible for how the game runs
    """

    def __init__(self, width, height) -> None:
        self.running = True  # Determines if the game is running
        self.memory = Memory(width, height)  # Initialize game memory

    def run(self, width, height, current_scene):
        """
        Where the actual game loop is running.
        Everything game related is defined in scene.
        Scene is initialized by running Program (in main
        which is outer scope) with the screen size and scene.
        At this point in time, scene is run as MenuScene.

        Everything relating to calling the scene is called here, such as
        input, update, and render while the game is running.

        If the game isn't running, then in the final loop (or the loop when
        the game is told to close by various means), self.running is set to
        false and the scene is changed to nothing. Then the game is safe to
        close.

        This is also where inputs are collected before they are sent to
        the inputs for scene.

        Finally, this is where FPS is set and where the display is updated.
        """
        # self.memory.screen = pygame.display.set_mode([width, height])
        screen = pygame.display.set_mode([width, height])  # Set screen size

        pygame.scrap.init()
        if not pygame.scrap.get_init():
            raise Exception("pygame.scrap is no longer supported :(")

        # Put the resolution ratio into memory, where 1080 and 576 are the min

        scene = current_scene  # Set scene currently shown through a parameter
        # Start game loop
        while self.running:
            keys_pressed = []  # Keys pressed/tapped (key press)
            keys_held = pygame.key.get_pressed()  # Keys held collected
            for event in pygame.event.get():  # Collect all key presses
                # Quit condition if you press the X on the top right
                if event.type == pygame.QUIT:
                    # self.memory - write to your save here
                    self.running = False  # Stop running this loop
                    pygame.mixer.music.stop()  # Stop the music
                    scene.run_scene = False  # Tell scene to stop running
                # If player does a keypress, append to our list for key presses
                if event.type == pygame.KEYDOWN:
                    keys_pressed.append(event.key)
                elif event.type == pygame.MOUSEMOTION or \
                        event.type == pygame.MOUSEBUTTONDOWN or \
                        event.type == pygame.MOUSEBUTTONUP:
                    keys_pressed.append(event.type)

                """if event.type == self.memory.music.end:
                    self.memory.music.switch_music()"""

            # Stop the game using other conditions (running, but scene says off)
            if self.running and not scene.run_scene:
                # self.memory - write to your save here
                self.running = False  # Stop running this loop
                pygame.mixer.music.stop()  # Stop the music
                scene.close_game()  # Tell scene to shut off
            else:
                # Functional game loop

                scene.input(keys_pressed, keys_held)  # Call to use keys in
                scene.update()  # Call to dynamically use/update/check changes
                scene.render(screen)  # Visually render desired graphics
                scene = scene.this_scene
                """This line is important to allow changing scenes (if 
                this_scene is different like using 
                scene.change_scene(next_scene). Otherwise, scene will not be 
                changed and will continue being this scene (same memory
                address, no change)."""

                """if 0 != scene.level_id:
                    self.memory.music.transition_music()"""

            fps.tick(120)  # 120 frames per second
            pygame.display.update()  # Update the visual output dynamically


if __name__ == "__main__":
    pygame.init()  # Initialize pygame
    pygame.mixer.init()  # Initialize pygame's sound

    fps = pygame.time.Clock()  # Initialize the frame rate

    # Alter these values to change the resolution
    game_width = 1280
    game_height = 700

    file_path = "put_icon_file_path_here"
    """pygame.display.set_caption("display_window") # game window caption
    icon = pygame.image.load(file_path + "file_image_name") # loading image
    default_icon_image_size = (32, 32) # reducing size of image
    icon = pygame.transform.scale(icon, default_icon_image_size) 
    # scaling image correctly
    pygame.display.set_icon(icon) # game window icon"""

    start_game = Program(game_width, game_height)
    # Initialize running the game with Program
    start_scene = Map()
    # Initialize the first scene/starting scene shown to the player
    start_game.run(game_width, game_height, start_scene)  # Run the game loop
    """The game loop will be stuck at this line (start_game.run) until the
    while loop (while self.running:) is no longer true. When self.running is
    False, the program will move onto the next line to quit"""

    pygame.quit()  # Quit the game/pygame instance
