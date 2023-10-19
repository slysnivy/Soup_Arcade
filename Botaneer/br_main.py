import pygame
import random
import os
import math

# BASE COLORS
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

# PLANT COLORS
LIMER_GREEN = (100, 255, 10)
SWAMP_GREEN = (110, 195, 65)
FOREST_GREEN = (50, 110, 50)
RADIANT_GREEN = (16, 163, 16)
PASTEL_GREEN = (100, 200, 100)

# SOIL
LIGHT_BROWN = (75, 50, 25)


class Memory:
    """
    Class used to store data across game instances
    """
    def __init__(self, width, height, max_scale):
        self.res_width = width
        self.res_height = height
        self.scale = max_scale

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
        self.position = [int(self.position[0] * width),
                         int(self.position[1] * height)]
        self.position = tuple(self.position)
        self.font_size = int(self.font_size * max(width, height))

        # Apply those changes
        self.setup()
        self.render()


class Music:
    """
    Music class containing tracks available and the current music playing.
    Also responsible for music volume and music switching.
    """

    def __init__(self, perc_vol, music_folder, width, height):
        self.music_tracks = []  # Put file_name for music here
        music_files = os.listdir("songs/")
        for each_song in music_files:
            self.music_tracks += [each_song]
        self.end = pygame.USEREVENT + 0    # Unique event, for when music ends
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 0)
        # Everytime music ends, return the event

        self.folder_path = music_folder   # Folder path for audio

        self.current_track_index = 0    # Everything but the main menu theme

        self.perc_vol = perc_vol   # Volume set by the player as a percentage
        self.music_vol = 0              # Adjustable music volume
        self.vol_time = pygame.time.get_ticks()     # Increment music with time
        self.max_vol = 1 * self.perc_vol / 100   # Max volume possible for music
        # Change 1 value for changing music

        self.res_width = width
        self.res_height = height

        """pygame.mixer.music.load(self.folder_path + self.music_tracks[0])"""
        #   Load this music up upon loading

        pygame.mixer.music.set_volume(self.max_vol)     # Set to max for now
        # pygame.mixer.music.play(-1)
        # Start with this song and play forever
        if 0 < len(self.music_tracks):
            self.music_text = Text("PLAYING: " +
                                   str(self.music_tracks[
                                           self.current_track_index]),
                                   (self.res_width / 2, self.res_height -
                                    (self.res_height / 10)), 20,
                                   "impact", WHITE, None)
        self.text_timer = pygame.time.get_ticks()
        # Display what's currently playing

    def switch_music(self):
        # Reset music display timer
        self.text_timer = pygame.time.get_ticks()

        # Choose a random track index
        self.music_vol = 0
        self.current_track_index = random.randint(1, len(self.music_tracks) - 2)
        # Set the boundaries between 2nd/1 and 2nd last/len - 2 to avoid
        # main menu and credits

        # Update the music display text
        self.music_text = Text("PLAYING: " +
                               str(self.music_tracks[self.current_track_index]),
                               (self.res_width / 2, self.res_height -
                                (self.res_height / 10)),
                               20, "impact", WHITE, None)

        # Load the selected track
        pygame.mixer.music.load(self.folder_path +
                                (self.music_tracks[self.current_track_index]))

        # Set the volume
        pygame.mixer.music.set_volume(self.music_vol)

        pygame.mixer.music.play(0, 0, 0)  # Play the music once

    def set_music(self, track_num, vol, loops, start, fade_in):
        # Set the max volume
        self.max_vol = 0.7 * self.perc_vol / 100

        # Reset music display timer
        self.text_timer = pygame.time.get_ticks()

        # Update the current track index
        self.current_track_index = track_num

        # Update the music display text
        self.music_text = Text("PLAYING: " +
                               str(self.music_tracks[self.current_track_index]),
                               (self.res_width / 2, self.res_height -
                                (self.res_height / 10)),
                               20, "impact", WHITE, None)

        # Load the selected track
        pygame.mixer.music.load(self.folder_path +
                                (self.music_tracks[self.current_track_index]))

        # Set the volume
        self.music_vol = vol * self.perc_vol / 100
        pygame.mixer.music.set_volume(self.music_vol)

        pygame.mixer.music.play(loops, start, fade_in)  # Play the music

    def transition_music(self):
        # Slowly increase volume of music (0.01 every 0.075 seconds)
        # until volume reaches the max (0.7 or self.max_vol)
        # set the new self.max_vol if changed
        self.max_vol = 0.7 * self.perc_vol / 100
        while self.music_vol < self.max_vol and \
                75 < pygame.time.get_ticks() - self.vol_time:
            self.music_vol += 0.01  # Increase volume
            pygame.mixer.music.set_volume(self.music_vol)   # Update volume
            self.vol_time = pygame.time.get_ticks()     # Reset timer


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


class MainScene(Scene):
    """
    Where the game will mainly take place. It's an interface for interacting
    and watchng the plant grow
    """
    def __init__(self, memory):
        Scene.__init__(self)
        self.memory = memory

        # Define each pixel within that grid as rects
        self.pot_area = []
        x_counter, y_counter = 0, 0
        total_pixel_counter = 0
        bound_x = (self.memory.res_width +
                   (9 * self.memory.scale)) / self.memory.scale
        bound_y = (self.memory.res_height +
                   (8 * self.memory.scale)) / self.memory.scale

        # Make an area of 42 (x) by 15 (y) pixels
        while x_counter <= bound_x:
            while y_counter <= bound_y - 8 * 2:
                if 9 * 27 <= x_counter <= bound_x - 9 * 27 and \
                        8 * 45 <= y_counter:
                    self.pot_area += [pygame.Rect(
                        (x_counter * self.memory.scale),
                        (y_counter * self.memory.scale),
                        (9 * self.memory.scale),
                        (8 * self.memory.scale))]
                    total_pixel_counter += 1

                y_counter += 8

            y_counter = 0
            x_counter += 9

        # Hold the rects of the created pot
        self.pot = []

    def input(self, pressed, held):
        for action in pressed:
            if action is pygame.K_TAB:
                self.change_scene(PotCreate(self.pot,
                                            self.pot_area,
                                            self.memory))

    def update(self):
        pass

    def render(self, screen):
        screen.fill(WHITE)
        self.debug_render(screen)

    def debug_render(self, screen):
        # Visualize each pixel with borders defining their area
        for each_rect in self.pot_area:
            pygame.draw.rect(screen, RED, each_rect)
            pygame.draw.rect(screen, BLUE, each_rect, 1)

        # todo: Visualize pot boundary line


class PotCreate(Scene):
    """
    Different game instance to create a pot used in the MainScene
    """
    def __init__(self, current_pot, pot_area, memory):
        Scene.__init__(self)

        # Load in memory
        self.memory = memory

        # Screen movement
        self.xpos = 0
        self.ypos = 0

        # Pot interaction/interface
        self.pot = current_pot
        self.build_area = pot_area
        self.zoom_index = 1
        self.zoom_detect = False

        # Update Mouse Properties
        self.mouse_x = None
        self.mouse_y = None
        self.cursor_rect = None
        self.update_mouse()

        # Image icons loaded from images file
        self.sidetool_icons = []

        # Rect objects for click detection
        self.sidetool_rects = []

        # Toggle if sidetool is rendered, if I want to hide the bar in future
        self.sidetool_toggle = False

        # Index determining which tool the user is using
        self.tool_index = 0

        # Actions when player interacts with the icons, related to tool_index
        self.sidetool_actions = {
            0: self.add_pot, 1: self.remove_pot,
            2: self.zoom_in, 3: self.zoom_out
        }

        # Sidebar tool options
        """ Currently the options are (according to index)
        0: adding a pot piece 
        1: removing a pot piece
        2: zooming in
        3: zooming out
        """

        # Load icons
        self.load_sideicons()
        self.make_sidetool()

        # To ensure there's enough time in between holding buttons
        self.held_delay = pygame.time.get_ticks()

        # Toggle when to update the valid soil area
        self.toggle_soil = False

        # Rects describing soil area
        self.soil_area = []

    def input(self, pressed, held):
        for action in pressed:
            if action == pygame.MOUSEMOTION:
                self.update_mouse()

            # Mouse collision on loaded rects
            if action == pygame.MOUSEBUTTONDOWN and \
                    self.cursor_rect is not None:
                # On mouse click, change index first, then apply action
                if self.cursor_rect.collidelistall(self.sidetool_rects):
                    # Clicking the various icons on the sidetool to change index
                    closest_rect = self.closest_rects(self.cursor_rect,
                                                      self.sidetool_rects)

                    if closest_rect is not None:
                        self.tool_index = self.sidetool_rects.index(
                            closest_rect)

                if self.cursor_rect.collidelistall(self.build_area) and \
                        self.tool_index < 2 and not \
                        self.cursor_rect.collidelistall(self.sidetool_rects):
                    # Build pot when clicking on the build grid
                    self.sidetool_actions[self.tool_index]()

                elif self.cursor_rect.collidelistall(self.pot) and \
                        self.tool_index < 2 and not \
                        self.cursor_rect.collidelistall(self.sidetool_rects):
                    # Remove pot piece when clicking on build grid
                    self.sidetool_actions[self.tool_index]()

                elif self.cursor_rect.collidelistall(self.sidetool_rects) and \
                        1 < self.tool_index:
                    # Other options for instant reproducable action when click
                    self.cursor_rect.collidelistall(self.sidetool_rects)
                    self.sidetool_actions[self.tool_index]()

                self.toggle_soil = True

        if held[pygame.K_d] and \
                25 < pygame.time.get_ticks() - self.held_delay:
            self.xpos -= 9
            self.held_delay = pygame.time.get_ticks()
        if held[pygame.K_a] and \
                25 < pygame.time.get_ticks() - self.held_delay:
            self.xpos += 9
            self.held_delay = pygame.time.get_ticks()
        if held[pygame.K_w] and \
                25 < pygame.time.get_ticks() - self.held_delay:
            self.ypos += 8
            self.held_delay = pygame.time.get_ticks()
        if held[pygame.K_s] and \
                25 < pygame.time.get_ticks() - self.held_delay:
            self.ypos -= 8
            self.held_delay = pygame.time.get_ticks()

    def update(self):
        if 5 < self.zoom_index:
            self.zoom_index = 1
        elif self.zoom_index < 1:
            self.zoom_index = 5

        if self.zoom_detect:
            self.scale_rect(self.pot)
            self.scale_rect(self.build_area)
            self.scale_rect(self.soil_area)
            self.zoom_detect = not self.zoom_detect

        self.update_rect(self.pot)
        self.update_rect(self.build_area)
        self.update_rect(self.soil_area)

        if self.toggle_soil:
            self.pot_soil()
            self.toggle_soil = not self.toggle_soil

        self.xpos = 0
        self.ypos = 0

    def render(self, screen):
        screen.fill(WHITE)
        # Render build_area grid
        for each_rect in self.build_area:
            pygame.draw.rect(screen,
                             LIME_GREEN,
                             [each_rect.x,
                              each_rect.y,
                              each_rect.width,
                              each_rect.height], 1)

        # Render current_pot pieces/pixels already placed
        for each_rect in self.pot:
            pygame.draw.rect(screen,
                             BROWN,
                             [each_rect.x,
                              each_rect.y,
                              each_rect.width,
                              each_rect.height])

        self.render_sidebar(screen)
        # Highlight selected icon
        pygame.draw.rect(screen, YELLOW,
                         self.sidetool_rects[self.tool_index], 2)

        self.render_soil(screen)    # Render valid soil area

    def add_pot(self):
        """ Sidetool icon action that adds a pixel to the pot when clicked on"""
        closest_rect = self.closest_rects(self.cursor_rect,
                                          self.build_area)

        """Need to make a new rect as to avoid linking 
        the same rect multiple times to avoid repetition in
        changing rect properties"""
        if closest_rect is not None and \
                closest_rect not in self.pot:
            self.pot += [pygame.Rect(closest_rect.x,
                                     closest_rect.y,
                                     closest_rect.width,
                                     closest_rect.height)]

    def remove_pot(self):
        """ Sidetool icon action that removes a pixel from the pot
        when clicked on"""
        closest_rect = self.closest_rects(self.cursor_rect,
                                          self.pot)

        if closest_rect is not None:
            self.pot.remove(closest_rect)
        pass

    def zoom_in(self):
        """ Sidetool icon action that zooms in when clicked on"""
        self.inverse_scale(self.pot)
        self.inverse_scale(self.build_area)
        self.inverse_scale(self.soil_area)

        self.zoom_index += 1
        self.zoom_detect = True

    def zoom_out(self):
        """ Sidetool icon action that zooms out when clicked on"""
        self.inverse_scale(self.pot)
        self.inverse_scale(self.build_area)
        self.inverse_scale(self.soil_area)

        self.zoom_index -= 1
        self.zoom_detect = True

    def update_mouse(self):
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        self.cursor_rect = pygame.Rect(self.mouse_x,
                                       self.mouse_y,
                                       1, 1)

    def update_rect(self, in_rect):
        for each_rect in in_rect:
            # Update the positioning
            each_rect.x = each_rect.x + self.xpos
            each_rect.y = each_rect.y + self.ypos

    def inverse_scale(self, in_rect):
        # Will do the inverse of the scaling factor, then use it to scale
        pre_zoom = self.zoom_index
        self.zoom_index = 1 / pre_zoom
        self.scale_rect(in_rect)
        self.zoom_index = pre_zoom  # Revert scaling factor to normal

    def scale_rect(self, in_rect):
        for each_rect in in_rect:
            # For each rect, move the positioning to the center
            each_rect.x -= (self.memory.res_width / 2)
            each_rect.y -= (self.memory.res_height / 2)

            # Update the scaling of the rect position
            each_rect.x = math.ceil(each_rect.x * self.zoom_index)
            each_rect.y = math.ceil(each_rect.y * self.zoom_index)

            # Update the scaling of the rect size
            each_rect.width *= self.zoom_index
            each_rect.height *= self.zoom_index

            # Undo the center positioning back (0,0) top left positioning
            each_rect.x += (self.memory.res_width / 2)
            each_rect.y += (self.memory.res_height / 2)

    def render_sidebar(self, screen):
        for icon_index in range(len(self.sidetool_rects)):
            pygame.draw.rect(screen, BLACK, self.sidetool_rects[icon_index])
            screen.blit(self.sidetool_icons[icon_index],
                        self.sidetool_rects[icon_index])

    def load_sideicons(self):
        folder_path = "images/"
        images_path = os.listdir(folder_path)
        for each_image in images_path:
            self.sidetool_icons += [pygame.image.load(folder_path + each_image)]

    def make_sidetool(self):
        """ Make each option icon 20 x 20, sidebar should be 40 x 20(n),
         where n stands for the height of the sidebar"""

        # Distance the sidebar is from the right side
        right_dist = 80 * self.memory.scale
        # Icon size, assuming the icon is a perfect square (width == height)
        icon_size = 40 * self.memory.scale

        # Declare x position as - 60 to make room for 2 icons per row
        xpos = (self.memory.res_width - right_dist) * self.memory.scale
        # Start at the top of the screen
        ypos = 40 * self.memory.scale

        for icons in range(len(self.sidetool_icons)):
            self.sidetool_rects += [pygame.Rect(xpos, ypos,
                                    icon_size, icon_size)]
            if self.memory.res_width - (right_dist - icon_size) <= xpos:
                xpos = self.memory.res_width - right_dist
                ypos += icon_size
            else:
                xpos += icon_size

    def get_rows(self):
        rect_rows = {}  # Split the rect into rows

        for rect in self.pot:
            if rect.y not in rect_rows:
                rect_rows[rect.y] = [rect.x]
            else:
                rect_rows[rect.y] += [rect.x]

        for y in rect_rows:
            rect_rows[y] = sorted(rect_rows[y])

        return rect_rows

    def get_columns(self):
        rect_columns = {}

        # Find the rects that make the largest gaps
        for rect in self.pot:
            if rect.x not in rect_columns:
                rect_columns[rect.x] = [rect.y]
            else:
                rect_columns[rect.x] = [rect.y]

        return rect_columns

    def get_sides(self):
        """ In the perspective of rows, get the pair creating a gap in the pot
        """
        rect_rows = self.get_rows()
        rect_y = list(rect_rows.keys())

        valid_gaps = {}
        for y in rect_y:
            current_left = None
            current_right = None
            for x_ind in range(len(rect_rows[y]) - 1):
                if current_left is None and \
                        rect_rows[y][x_ind] + (9 * self.zoom_index) != \
                        rect_rows[y][x_ind + 1]:
                    current_left = rect_rows[y][x_ind]
                    current_right = rect_rows[y][x_ind + 1]
                if current_left is not None:
                    if y not in valid_gaps:
                        valid_gaps[y] = [[current_left, current_right]]
                    else:
                        valid_gaps[y] += [[current_left, current_right]]
                    current_left = None
                    current_right = None

        return valid_gaps

    def get_bases(self):
        if len(self.pot) < 1:
            return False

        rect_rows = self.get_rows()

        # Validate if pairs exist:
        row_y = list(rect_rows.keys())  # Get the rows

        valid_bases = {}
        pot_width_min = 2
        for y in row_y:
            bases = []
            for rect_index in range(len(rect_rows[y]) - 1):
                if rect_rows[y][rect_index + 1] - \
                        rect_rows[y][rect_index] <= \
                        math.floor(9 * self.zoom_index):
                    if len(bases) < 1:
                        bases += [rect_rows[y][rect_index]]

                    bases += [rect_rows[y][rect_index + 1]]
                else:
                    if (pot_width_min < len(bases) and
                        len(valid_bases) < 1) or \
                            (2 < len(bases) and 0 < len(valid_bases)):
                        if y not in valid_bases:
                            valid_bases[y] = [bases]
                        else:
                            valid_bases[y] += [bases]
                    bases = []

            if (pot_width_min < len(bases) and len(valid_bases) < 1) or \
                    (2 < len(bases) and 0 < len(valid_bases)):
                if y not in valid_bases:
                    valid_bases[y] = [bases]
                else:
                    valid_bases[y] += [bases]

        return valid_bases

    def validate_pot(self):
        # todo: redo get_pot() and turn into get_sides()
        """ In the perspective of rows, get the pair creating a gap in the pot
                """
        if len(self.pot) < 1:
            return False

        valid_sides = self.get_sides()
        if len(valid_sides) < 1:
            return False

        # Check if the base is valid
        valid_bases = self.get_bases()
        if len(valid_bases) < 1:
            return False

        return True

    def find_area(self, all_sides, all_bases):
        """
        Start with a loop of bases, need to get all_bases.keys
        From each base's y position, check two things (if):
            - at the y_val, check bases at the [0] and [-1] indexes,
                go upwards aka y_val - (8 * self.zoom_index), check if the y_val
                is present, and check each side pair at the [0] and [1]
                indexes and see if their x-values match
            - AT THIS POINT, the x-values need to match, aka a corner forming
                between the base and side starting point

        Put valid_potential corners in their own list as this:
            valid_corners = {}
            valid_corners[y_val - (8 - self.zoom_index)] = \
                all_sides[y_val - (8 - self.zoom_index)]

        After confirming valid corner points, we confirm that this is a valid
        pot base with an opening on the top. We want to now find the gaps that
        precede this.
        To start, we need to traverse the sides starting at the y_val
        in valid_corners. We need to check at the current y_val in sides and
        check for each pair:
            - If the y_val - (8 * self.zoom_index) x_values matches, or at
                that x_values + and - (9 * self.zoom_index)
            - If so, then iterate the current y_val by - (8 * self.zoom_index)
            - If there isn't a rect at y_val - (8 * self.zoom_index), then we
            reached the end of our pot top, but need to confirm that we're at
            a lip and not hitting another base
            (aka, confirm that this is a lip opening and not an enclosed space)

            To check, we need to see at this y_val, if the
            sides[y_val][pair_iter] [0] and [1], check if the
            y_val - (8 * self.zoom_index) exists in bases. Then see if it
            matches with the [0] and [-1] in
            bases[y_val - (8 * self.zoom_index)]. If they match,
            then this potential pot area is enclosed and invalid.
            Therefore we look for if they don't match, and if it doesn't
            add it to pot_gaps, aka the region defining a valid gap and
            passing the pot test. We'd like to define this as a class
            variable since it'll be rendered as well.

        :param all_sides:
        :param all_bases:
        :return:
        """
        valid_corners = {}
        base_y = list(all_bases.keys())
        for y in base_y:
            for current_base in all_bases[y]:
                if y - (8 * self.zoom_index) in all_sides:
                    for pair in all_sides[y - (8 * self.zoom_index)]:
                        if pair[0] in current_base and \
                                pair[1] in current_base:
                            if y - (8 * self.zoom_index) not in valid_corners:
                                valid_corners[y - (8 * self.zoom_index)] = [pair]
                            else:
                                valid_corners[y - (8 * self.zoom_index)] += [pair]

        corner_y = list(valid_corners.keys())
        print(valid_corners)
        pot_area = []   # todo: make a class to store PotArea 's
        emergency_break = 0
        for y in corner_y:
            current_y = y
            potential_gaps = {}
            for current_pair in valid_corners[y]:
                while current_y in all_sides:
                    for pair in all_sides[current_y]:
                        if pair[0] <= current_pair[0] + \
                                (9 * self.zoom_index) and \
                                current_pair[1] - \
                                (9 * self.zoom_index) <= pair[1]:
                            if current_y not in potential_gaps:
                                potential_gaps[current_y] = [pair]
                            else:
                                potential_gaps[current_y] += [pair]
                    current_y -= 8 * self.zoom_index

                    if 1000 < emergency_break:
                        raise "StuckInLoopError-find_area"

                    emergency_break += 1
                current_y += 8 * self.zoom_index
                if current_y in potential_gaps and \
                        current_y - (8 * self.zoom_index) in all_bases:
                    for each_pair in potential_gaps[current_y]:
                        for each_base in all_bases[current_y - (8 * self.zoom_index)]:
                            if each_pair[0] != each_base[0] and \
                                    each_pair[1] != each_base[-1]:
                                pot_area += [potential_gaps]
                else:
                    pot_area += [potential_gaps]

        return pot_area

    def add_soil(self, pot_area):
        """
        Using the defined gaps of a pot area, fill it with soil.
        :return:
        """
        # Added an extra loop to maybe define different pots areas in the future
        self.soil_area = []
        for each_area in pot_area:
            gap_y = list(each_area.keys())
            for y in gap_y:
                for pair in each_area[y]:
                    first_x = pair[0] + (9 * self.zoom_index)
                    last_x = pair[1]
                    while first_x < last_x:
                        self.soil_area += [pygame.Rect(first_x, y,
                                                       9 * self.zoom_index,
                                                       8 * self.zoom_index)]
                        first_x += (9 * self.zoom_index)

    def pot_soil(self):
        """
        Render a valid pot zone
        """
        if self.validate_pot():
            get_sides = self.get_sides()
            get_bases = self.get_bases()
            print("Valid")
            print("sides: {all_sides}".format(all_sides=get_sides))
            print("bases: {all_bases}".format(all_bases=get_bases))
            print("Now the pot area: "
                  "{pot_area}".format(pot_area=self.find_area(get_sides,
                                                              get_bases)))
            pot_area = self.find_area(get_sides, get_bases)
        else:
            pot_area = []
        self.add_soil(pot_area)

    def render_soil(self, screen):
        if 0 < len(self.soil_area):
            for rect in self.soil_area:
                pygame.draw.rect(screen, LIGHT_BROWN, rect)

    @staticmethod
    def closest_rects(current_rect, compare_rects):
        r_index = current_rect.collidelistall(compare_rects)
        # Get list of indices of all colliding rectangles
        closest_rect = None     # Initialize closest rect

        for each_index in r_index:
            if closest_rect is None:
                # Initialize first rect object
                closest_rect = compare_rects[each_index]
            elif abs(compare_rects[each_index].x -
                     current_rect.x) < \
                    abs(closest_rect.x - current_rect.x) and \
                    abs(compare_rects[each_index].y -
                        current_rect.y) < \
                    abs(closest_rect.y - current_rect.y):
                # Compare with next rect, new rect has smaller x and y dist
                closest_rect = compare_rects[each_index]
        return closest_rect     # None if no rect, otherwise give pygame.Rect


class PlantMechanics:
    """
    Should have two main functions for growth:
        - Grow: which grows the length of this part in a specified direction
        - Thicken: which will age the part by growing all associated segments
            perpendicular to the grow direction
    Both grow and thicken will occur symmetrically
    """
    def __init__(self, x_pos, y_pos):
        self.growth_list = LinkedTree()
        # Hold a type of plant segment
        self.random_event = pygame.time.get_ticks()
        # Timer for next random event

        self.x_pos = x_pos  # x pos of where the plant will start growing
        self.y_pos = y_pos  # y pos of where the plant will start growing

        self.direction = 0

    def grow(self, item):
        """
        Grow plant parallel to the growing direction
        """
        self.growth_list.append_right(item)

    def thicken(self, item1, item2):
        """
        Grow plant perpendicular to the growing direction
        :return:
        """
        head = self.growth_list.head
        while head is not None:
            head.item.append_left(item1)
            head.item.append_right(item2)
            head = head.next

    def update(self):
        pass


class Plant(PlantMechanics):
    def __init__(self, x_pos, y_pos):
        """ a text
        b text


        """
        self.age = 0                # How old the plant is
        self.max_age = 0            # Initialize how long the plant will grow
        self.growth_factor = 1      # How fast the plant will grow
        self.branching_freq = 0     # Determine how many branches occur
        self.leaf_freq = 0          # How many leaves present in a spot

        PlantMechanics.__init__(self, x_pos, y_pos)   # Basic mechanics
        self.growth_list.append_right(Stem(x_pos, y_pos))   # Start w/ stems

        # todo: Make methods of plant growth for Stem, Branch and Leave

    def grow(self, item):
        """
        Grow plant parallel to the growing direction
        """
        PlantMechanics.grow(self, item)

    def thicken(self, item1, item2):
        """
        Grow plant perpendicular to the growing direction
        """
        PlantMechanics.thicken(self, item1, item2)

    def update(self):
        time_to_grow = 3000  # todo: Randomize in future
        if time_to_grow < pygame.time.get_ticks() - self.random_event:
            self.x_pos += 9
            self.y_pos += 8
            self.grow(Stem(self.x_pos, self.y_pos))


class Stem(PlantMechanics):
    def __init__(self, x_pos, y_pos):
        PlantMechanics.__init__(self, x_pos, y_pos)   # Basic mechanics
        # Contains branches and plant pixels
        self.pixel = PlantPixel(x_pos, y_pos, 9, 8, DARK_GREEN)

    def grow(self, item):
        """
        Grow plant parallel to the growing direction
        """
        PlantMechanics.grow(self, item)

    def thicken(self, item1, item2):
        """
        Grow plant perpendicular to the growing direction
        """
        PlantMechanics.thicken(self, item1, item2)


class Branch(Stem):
    def __init__(self, x_pos, y_pos):
        PlantMechanics.__init__(self, x_pos, y_pos)   # Basic mechanics
        # Contains leaves and plant pixels
        self.pixel = PlantPixel(x_pos, y_pos, 9, 8, LIMER_GREEN)

    def grow(self, item):
        """
        Grow plant parallel to the growing direction
        """
        PlantMechanics.grow(self, item)

    def thicken(self, item1, item2):
        """
        Grow plant perpendicular to the growing direction
        """
        PlantMechanics.thicken(self, item1, item2)


class Leaves:
    pass


class PlantPixel:
    """
    Defining a pixels color, size and position
    A pixels size is usually 9 x 8 by default without scaling
    """
    def __init__(self, x_pos, y_pos, width, height, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color

    # In the future, need to return x, y, width, height, and color values
    # In the future, need to update x, y, width, height, and color values


class LinkedTree:
    def __init__(self):
        self.head = None    # Left pointer
        self.tail = None    # Right pointer

    def append_left(self, item):
        if self.head is None and self.tail is None:
            # Regardless of left/right, initialize 1 Node
            self.head = TreeNode(item)
            self.tail = self.head
        else:
            new_node = TreeNode(item)   # Make a new Node
            new_node.next = self.head   # Node to leftmost, put list to right
            self.head = new_node        # Make Node new start/head

    def append_right(self, item):
        if self.head is None and self.tail is None:
            # Regardless of left/right, initialize 1 Node
            self.head = TreeNode(item)
            self.tail = self.head
        else:
            new_node = TreeNode(item)   # Make a new Node
            self.tail.next = new_node   # Node to the right of tail
            self.tail = self.tail.next  # Make rightmost Node the new tail

    def check_len(self):
        check_node = self.head
        count = 0
        while check_node is not None:
            count += 1
            check_node = check_node.next

        return count

    def check_chain(self):
        check_node = self.head
        while check_node is not None:
            print("mem_id: " + str(id(check_node)))
            check_node = check_node.next


class TreeNode:
    def __init__(self, item):
        self.item = item
        self.next = None


class Program:
    """
    Class responsible for how the game runs
    """

    def __init__(self, width, height) -> None:
        self.running = True  # Determines if the game is running
        scale_width = game_width / 854
        scale_height = game_height / 480
        self.memory = Memory(width, height, min(scale_width,
                                                scale_height))
        # Initialize game memory

        self.memory.music = Music(100, "example_file_path", width, height)

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
        screen = pygame.display.set_mode([width, height])  # Set screen size

        pygame.scrap.init()
        if not pygame.scrap.get_init():
            raise Exception("pygame.scrap is no longer supported :(")

        scene = current_scene   # Set scene currently shown through a parameter
        # Start game loop
        while self.running:
            keys_pressed = []   # Keys pressed/tapped (key press)
            keys_held = pygame.key.get_pressed()    # Keys held collected
            for event in pygame.event.get():    # Collect all key presses
                # Quit condition if you press the X on the top right
                if event.type == pygame.QUIT:
                    # self.memory.write_save()
                    self.running = False    # Stop running this loop
                    pygame.mixer.music.stop()   # Stop the music
                    scene.run_scene = False     # Tell scene to stop running
                # If player does a keypress, append to our list for key presses
                if event.type == pygame.KEYDOWN:
                    keys_pressed.append(event.key)
                elif event.type == pygame.MOUSEMOTION or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    keys_pressed.append(event.type)

                """if event.type == self.memory.music.end:
                    self.memory.music.switch_music()"""

            # Stop the game using other conditions (running, but scene says off)
            if self.running and not scene.run_scene:
                # self.memory.write_save()
                self.running = False    # Stop running this loop
                pygame.mixer.music.stop()   # Stop the music
                scene.close_game()      # Tell scene to shut off
            else:
                # Functional game loop

                scene.input(keys_pressed, keys_held)    # Call to use keys in
                scene.update()  # Call to dynamically use/update/check changes
                scene.render(screen)    # Visually render desired graphics
                scene = scene.this_scene
                """This line is important to allow changing scenes (if
                this_scene is different like using
                scene.change_scene(next_scene). Otherwise, scene will not be
                changed and will continue being this scene (same memory
                address, no change)."""

                """if 0 != scene.level_id:
                    self.memory.music.transition_music()"""

            fps.tick(120)   # 120 frames per second
            pygame.display.update()     # Update the visual output dynamically


if __name__ == "__main__":
    pygame.init()   # Initialize pygame
    pygame.mixer.init()  # Initialize pygame's sound

    fps = pygame.time.Clock()   # Initialize the frame rate

    # Alter these values to change the resolution
    game_width = 854    # Default is 854, alternative is 1280
    game_height = 480   # Default is 480, alternative is 720

    file_path = "put_icon_file_path_here"
    """pygame.display.set_caption("display_window") # game window caption
    icon = pygame.image.load(file_path + "file_image_name") # loading image
    default_icon_image_size = (32, 32) # reducing size of image
    icon = pygame.transform.scale(icon, default_icon_image_size) 
    # scaling image correctly
    pygame.display.set_icon(icon) # game window icon"""

    start_game = Program(game_width, game_height)
    # Initialize running the game with Program
    start_scene = MainScene(start_game.memory)
    # Initialize the first scene/starting scene shown to the player
    start_game.run(game_width, game_height, start_scene)  # Run the game loop
    """The game loop will be stuck at this line (start_game.run) until the
    while loop (while self.running:) is no longer true. When self.running is
    False, the program will move onto the next line to quit"""

    pygame.quit()   # Quit the game/pygame instance
