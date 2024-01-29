import pygame
import pickle
import os
import math

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
        self.dp = []
        self.memory_manager = MemoryPoint()
        self.dp = self.memory_manager.depickle_dp("save")

    def load_game(self):
        """ Load previous game instance, usually from a text_file"""
        pass

    def load_scenes(self):
        """ Load all scenes from a text file"""
        pass


class MemoryPoint:
    """
    Class used to manage and hold all storage actions
    """
    def __init__(self):
        # Datapoints:
        self.dp_titles = []
        self.dp_desc = []
        self.dp_icons = {}
        self.dp_lines = {}
        self.dp_line_colors = {}

    def comp_dp(self, dp_list):
        for dp in dp_list:
            self.dp_titles += [[str(dp.title.text)]]
            self.dp_desc += [dp.description]
            self.dp_icons[dp.id] = [dp.icon.color, dp.icon.rect.x,
                                    dp.icon.rect.y, dp.icon.width,
                                    dp.icon.height]
            self.dp_lines[dp.id] = [[other_dp.id]
                                    for other_dp in dp.associated]
            self.dp_line_colors[dp.id] = dp.line_color

    def pickle_dp(self, pickle_path):
        with open(pickle_path + "/my_map", "wb") as out_file:
            pickle.dump(self.dp_titles, out_file)
            pickle.dump(self.dp_desc, out_file)
            pickle.dump(self.dp_icons, out_file)
            pickle.dump(self.dp_lines, out_file)
            pickle.dump(self.dp_line_colors, out_file)

        out_file.close()

    def depickle_dp(self, pickle_path):
        dp_list = []
        dp_dict = {}
        if len(os.listdir("save")) < 1:
            return dp_list

        with open(pickle_path + "/my_map", "rb") as in_file:
            self.dp_titles = pickle.load(in_file)
            self.dp_desc = pickle.load(in_file)
            self.dp_icons = pickle.load(in_file)
            self.dp_lines = pickle.load(in_file)
            self.dp_line_colors = pickle.load(in_file)

        all_id = list(self.dp_icons.keys())
        # Create datapoint list
        for dp_id in all_id:
            new_point = DataPoint()
            # todo: add more stuff to dp and method call here respectively
            new_point.change_icon_location(self.dp_icons[dp_id][1],
                                           (self.dp_icons[dp_id][2]))
            new_point.change_icon_color(self.dp_icons[dp_id][0])
            new_point.change_id(dp_id)
            new_point.description = self.dp_desc[dp_id]
            new_point.description.split_text(new_point.sel_page)

            dp_list += [new_point]
            dp_dict[dp_id] = new_point
        # Make lines by establishing connections in our current datapoints
        for dp_id in all_id:
            if 0 < len(self.dp_lines[dp_id]):
                for line in self.dp_lines[dp_id]:
                    dp_dict[dp_id].associated += [dp_dict[line[0]]]
                dp_dict[dp_id].line_color = self.dp_line_colors[dp_id]

        return dp_list


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
    def __init__(self, memory):
        Scene.__init__(self)

        self.memory = memory

        self.datapoints = self.memory.dp
        self.mouse = pygame.Rect(0, 0, 1, 1)
        self.select_point = None
        self.show_select = False
        self.sort_mode = 0

        self.x_offset = 0
        self.y_offset = 0
        self.dir_delay = pygame.time.get_ticks()

        self.follow_mouse = False

        self.edit_options = [pygame.Rect(1, 1, 1, 1),  # Make connections
                             pygame.Rect(2, 2, 1, 1),  # None
                             pygame.Rect(3, 3, 1, 1),
                             pygame.Rect(4, 4, 1, 1)]  # None
        self.edit_modes = [self.mode_0,
                           self.mode_1,
                           self.mode_2,
                           self.mode_3,
                           self.mode_4
                           ]
        self.current_mode = 0
        """
        Reflects the corresponding edit options in human indices
        1: icon color
        2: icon location
        3: icon radius
        
        We reserve 0 for no options
        """
        self.render_modes = [self.render_mode_0,
                             self.render_mode_0,
                             self.render_mode_1,
                             self.render_mode_2,
                             self.render_mode_3]
        # Render modes reflect self.current_mode as well

        self.color_options = [DARK_RED, DARK_GREEN, DARK_GREY,
                              RED, LIME_GREEN, GREY,
                              BLUE, YELLOW, ORANGE,
                              CYAN, PURPLE]
        self.rect_colors = []
        self.line_col_ind = 0
        x, y = 0, 0
        width, height = 20, 20
        color_per_row = 3
        color_iter = 0
        for color in self.color_options:
            self.rect_colors += [Rect(color, [x + (width * color_iter),
                                              y],
                                      width, height)]

            if color_per_row - 2 < color_iter:
                y += height
                color_iter = 0
            else:
                color_iter += 1

        if 0 < len(self.memory.memory_manager.dp_icons):
            self.id_count = max(list(
                self.memory.memory_manager.dp_icons.keys())) + 1
        else:
            self.id_count = 0

        self.confirm_rect = pygame.Rect(self.memory.res_width - 30,
                                        self.memory.res_height - 30,
                                        30, 30)     # Exit description mode
        self.desc_right = pygame.Rect(self.memory.res_width - 30,
                                      self.memory.res_height - 90, 30, 30)      # Go right/next page
        self.desc_left = pygame.Rect(30, self.memory.res_height - 90, 30, 30)   # Go left/previous page
        self.text = ""
        self.last_char = None
        self.cap_toggle = False
        self.held_char_timer = pygame.time.get_ticks()
        self.initial_held = pygame.time.get_ticks()

        self.confirm_delete = pygame.Rect(((self.memory.res_width * 2) // 3,
                                          (self.memory.res_height * 2) // 3,
                                          30, 30))      # Click to delete a point
        self.confirm_keep = pygame.Rect((self.memory.res_width // 3,
                                        (self.memory.res_height * 2) // 3,
                                        30, 30))        # Click to not delete a point

        self.confirm_title = pygame.Rect(self.memory.res_width / 2,
                                         (self.memory.res_height / 2) + 60,
                                         30, 30)

    def input(self, pressed, held):
        for action in pressed:
            if action == pygame.MOUSEMOTION:
                self.mouse.x = pygame.mouse.get_pos()[0]
                self.mouse.y = pygame.mouse.get_pos()[1]

            if action == pygame.MOUSEBUTTONDOWN:
                # This can be put here since only current_mode 4 is only being affected
                if self.current_mode == 4:
                    self.select_point.title.font_size = 30
                    self.select_point.title.setup()
                    self.select_point.title.render()

                # Different modes when pressing left click
                self.edit_modes[self.current_mode]()

            if action == pygame.MOUSEBUTTONUP and self.follow_mouse:
                self.follow_mouse = False

            if action == pygame.K_ESCAPE:
                self.run_scene = False

            if self.current_mode == 1 or self.current_mode == 0:
                if action == pygame.K_w:
                    self.y_offset += 5
                elif action == pygame.K_s:
                    self.y_offset -= 5
                if action == pygame.K_a:
                    self.x_offset += 5
                elif action == pygame.K_d:
                    self.x_offset -= 5

            if self.current_mode == 2:
                # Typing mode

                if action == pygame.K_CAPSLOCK:
                    self.cap_toggle = not self.cap_toggle

                """
                If statement for character finds, in this order:
                    - Lowercase
                    - Uppercase
                    - Numbers
                    - Then every other crucial key like !, ?, (, ), ,, etc.
                """
                if 97 <= action <= 122 and self.cap_toggle:
                    self.last_char = action - 32
                    self.select_point.description.write_page(self.select_point.sel_page,
                                                             action - 32)
                    self.initial_held = pygame.time.get_ticks()
                elif 97 <= action <= 122 or \
                        48 <= action <= 57 or \
                        action in [33, 44, 46, 47, 58, 63]:
                    self.last_char = action
                    self.select_point.description.write_page(self.select_point.sel_page,
                                                             action)
                    self.initial_held = pygame.time.get_ticks()
                elif action == pygame.K_SPACE:
                    self.last_char = -14
                    self.select_point.description.write_page(self.select_point.sel_page,
                                                             -14)
                    self.initial_held = pygame.time.get_ticks()
                elif action == pygame.K_BACKSPACE:
                    self.last_char = 0
                    self.select_point.description.erase_write(self.select_point.sel_page)
                    self.initial_held = pygame.time.get_ticks()
                else:
                    self.last_char = None

            elif self.current_mode == 4:
                if action == pygame.K_CAPSLOCK:
                    self.cap_toggle = not self.cap_toggle
                if 97 <= action <= 122 and self.cap_toggle:
                    self.last_char = action - 32
                    self.select_point.change_title(action - 32)
                    self.initial_held = pygame.time.get_ticks()
                elif 97 <= action <= 122 or \
                        48 <= action <= 57 or \
                        action in [33, 44, 46, 47, 58, 63]:
                    self.last_char = action
                    self.select_point.change_title(action)
                    self.initial_held = pygame.time.get_ticks()
                elif action == pygame.K_SPACE:
                    self.last_char = -14
                    self.select_point.change_title(-14)
                    self.initial_held = pygame.time.get_ticks()
                elif action == pygame.K_BACKSPACE:
                    self.last_char = 0
                    self.select_point.change_title(0)
                    self.initial_held = pygame.time.get_ticks()
                else:
                    self.last_char = None

        if self.current_mode == 2 and True in held and \
                20 < pygame.time.get_ticks() - \
                self.held_char_timer and \
                500 < pygame.time.get_ticks() - self.initial_held and \
                self.last_char is not None:
            self.select_point.description.write_page(self.select_point.sel_page,
                                                     self.last_char)
            self.held_char_timer = pygame.time.get_ticks()
        elif self.current_mode == 4 and True in held and \
                20 < pygame.time.get_ticks() - \
                self.held_char_timer and \
                500 < pygame.time.get_ticks() - self.initial_held and \
                self.last_char is not None:
            self.select_point.change_title(self.last_char)
            self.held_char_timer = pygame.time.get_ticks()

        if (self.current_mode == 1 or self.current_mode == 0) and \
                20 < pygame.time.get_ticks() - self.dir_delay:
            if held[pygame.K_w]:
                self.y_offset += 5
                self.dir_delay = pygame.time.get_ticks()
            elif held[pygame.K_s]:
                self.y_offset -= 5
                self.dir_delay = pygame.time.get_ticks()
            if held[pygame.K_a]:
                self.x_offset += 5
                self.dir_delay = pygame.time.get_ticks()
            elif held[pygame.K_d]:
                self.x_offset -= 5
                self.dir_delay = pygame.time.get_ticks()

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
                    self.calculate_mouse(self.datapoints[point_index]) and \
                    self.mouse.collidelist(self.edit_options) < 0:
                self.follow_mouse = True
                check_select = False
            elif self.calculate_mouse(
                    self.datapoints[point_index]):
                self.select_point = self.datapoints[point_index]
                self.select_point.icon.display_options = True
                check_select = False

            point_index += 1

        # Update mouse position temporarily
        temp_mouse = pygame.Rect(self.mouse.x - self.x_offset,
                                 self.mouse.y - self.y_offset,
                                 self.mouse.width, self.mouse.height)
        # When not clicking on a point

        if -1 < temp_mouse.collidelist(self.edit_options) and \
                self.select_point is not None and \
                self.select_point.icon.display_options:
            # Edit options when clicked
            self.current_mode = temp_mouse.collidelist(
                self.edit_options) + 1

        elif check_select:
            # When not clicking on a point
            check_dist = True
            for point in self.datapoints:
                if self.calculate_mouse(point):
                    check_dist = False
            if check_dist and self.select_point is None:
                # Make a new point, only if it's far away from other points
                # Only make a new point once we deselected our point
                new_point = DataPoint()
                new_point.change_icon_location(self.mouse.x - self.x_offset,
                                               self.mouse.y - self.y_offset)
                new_point.change_id(self.id_count)
                self.id_count += 1
                self.datapoints += [new_point]
            elif -1 < self.mouse.collidelist(self.rect_colors) and \
                    self.select_point is not None:
                self.select_point.change_icon_color(
                    self.color_options[self.mouse.collidelist(
                        self.rect_colors)])
            else:
                # Deselect our point
                self.select_point = None

        elif self.select_point is not None:
            self.update_option_pos()

    def mode_1(self):
        # On left click, find a valid point to click on that's not our point

        # Change color of lines added
        if -1 < self.mouse.collidelist(self.rect_colors):
            self.line_col_ind = self.mouse.collidelist(self.rect_colors)
        # Adding or removing a line on left click
        elif 1 < len(self.datapoints):
            find_point = False
            point_index = 0
            while not find_point and point_index < len(self.datapoints):
                if find_point is not self.select_point:
                    find_point = self.calculate_mouse(
                        self.datapoints[point_index])
                point_index += 1

            if find_point and 0 < len(self.select_point.associated) and \
                    find_point in self.select_point.associated:
                self.select_point.remove_point(find_point)
            elif find_point and 0 < len(find_point.associated) and \
                    self.select_point in find_point.associated:
                find_point.remove_point(self.select_point)
            elif find_point:
                self.select_point.add_point(find_point, self.color_options[self.line_col_ind])
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
        # On left click, start typing
        # todo: Add a left click to select where text goes
        # Press left and right to move onto the next page
        if self.mouse.colliderect(self.desc_right):
            if len(self.select_point.description.pages) - 1 <= self.select_point.sel_page:
                self.select_point.description.add_page()
            self.select_point.sel_page += 1
            self.select_point.description.split_text(self.select_point.sel_page)
        elif 0 < self.select_point.sel_page and self.mouse.colliderect(self.desc_left):
            self.select_point.sel_page -= 1
            self.select_point.description.split_text(self.select_point.sel_page)

        # Left click special rect to leave typing interface
        if self.mouse.colliderect(self.confirm_rect):
            self.current_mode = 0

    def mode_3(self):
        if self.mouse.colliderect(self.confirm_delete):
            self.current_mode = 0
            self.show_select = False
            del self.datapoints[self.datapoints.index(self.select_point)]
            self.select_point = None
        elif self.mouse.colliderect(self.confirm_keep):
            self.current_mode = 0

    def mode_4(self):
        if self.mouse.colliderect(self.confirm_title):
            self.select_point.title.font_size = 12
            self.select_point.title.setup()
            self.select_point.title.render()
            self.current_mode = 0
            self.select_point = None
            self.show_select = False

    def update(self):
        if self.select_point is not None and \
                not self.select_point.icon.display_options:
            self.select_point = None

        if self.follow_mouse and self.select_point is not None:
            self.select_point.change_icon_location(self.mouse.x - self.x_offset,
                                                   self.mouse.y - self.y_offset)
            self.update_option_pos()

    def render(self, screen):
        screen.fill(WHITE)
        self.render_modes[self.current_mode](screen)  # type: ignore

    def render_mode_0(self, screen):
        # Default rendering mode

        # Render lines under points
        for each_point in self.datapoints:
            each_point.render_lines(screen, self.x_offset, self.y_offset)

        # Render points
        for each_point in self.datapoints:
            if self.current_mode == 1 and each_point is not self.select_point:
                # Turn points to rects to show that it's clickable
                each_point.change_icon_border(0)
            else:
                # Circle default rendering with title/text above them
                each_point.change_icon_border(100)
                screen.blit(each_point.title.text_img,
                            [each_point.icon.center[0]- (each_point.title.text_rect.width / 2),
                             each_point.icon.center[1] - (each_point.title.text_rect.height)])
            each_point.render(screen, self.x_offset, self.y_offset)

        # Render options
        if self.select_point and \
                self.select_point.icon.display_options:
            for each_option in self.edit_options:
                pygame.draw.rect(screen, ORANGE, [each_option.x + self.x_offset,
                                                  each_option.y + self.y_offset,
                                                  each_option.width,
                                                  each_option.height], 1)

        # Render color options
        if self.select_point:
            for color in self.rect_colors:
                color.render(screen)

    def render_mode_1(self, screen):
        pygame.draw.rect(screen, LIME_GREEN, self.confirm_rect)
        self.select_point.description.render_page(screen, self.select_point.sel_page)
        pygame.draw.rect(screen, YELLOW, self.desc_right)
        pygame.draw.rect(screen, YELLOW, self.desc_left)

    def render_mode_2(self, screen):
        delete_text = Text("Do you want to delete this point?",
                           (self.memory.res_width / 2,
                            self.memory.res_height / 2),
                           50, "impact", RED, None)

        self.select_point.render(screen, 0, 0)
        pygame.draw.rect(screen, DARK_RED, self.confirm_keep)
        pygame.draw.rect(screen, DARK_GREEN, self.confirm_delete)
        screen.blit(delete_text.text_img, delete_text.text_rect)

    def render_mode_3(self, screen):
        screen.blit(self.select_point.title.text_img,
                    self.select_point.title.text_rect)
        pygame.draw.rect(screen, LIME_GREEN, self.confirm_title)

    def calculate_mouse(self, point_b):
        """Point a is self.mouse
        Point b is any datapoint
        """
        hitbox_mod = 3  # Radius size, change for more/less cluttering

        if math.sqrt((self.mouse.x - self.x_offset - point_b.icon.center[0]) ** 2 +
                     (self.mouse.y - self.y_offset - point_b.icon.center[
                         1]) ** 2) <= point_b.icon.width * hitbox_mod:
            # Top left corner
            return point_b
        elif math.sqrt((self.mouse.x - self.x_offset + self.mouse.width -
                        point_b.icon.center[0]) ** 2 +
                       (self.mouse.y - self.y_offset - point_b.icon.center[
                           1]) ** 2) <= point_b.icon.width * hitbox_mod:
            # Top right corner
            return point_b
        elif math.sqrt((self.mouse.x - self.x_offset - point_b.icon.center[0]) ** 2 +
                       (self.mouse.y - self.y_offset + self.mouse.height -
                        point_b.icon.center[
                            1]) ** 2) <= point_b.icon.width * hitbox_mod:
            # Bottom left corner
            return point_b
        elif math.sqrt((self.mouse.x - self.x_offset + self.mouse.width -
                        point_b.icon.center[0]) ** 2 +
                       (self.mouse.y - self.y_offset + self.mouse.height -
                        point_b.icon.center[
                            1]) ** 2) <= point_b.icon.width * hitbox_mod:
            # Bottom right corner
            return point_b
        else:
            # No points detected
            return None

    def calculate_distance(self, point_a, point_b):
        """Get distance between point_a and point_b and return point_b
        if point_a is touching
        """
        hitbox_mod = 3  # Radius size, change for more/less cluttering

        if math.sqrt((point_a.icon.center[0] - point_b.icon.center[0]) ** 2 +
                     (point_a.icon.center[1] -
                      point_b.icon.center[1]) ** 2) <= \
                point_b.icon.width * hitbox_mod:
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

    def save_map(self):
        out_path = os.getcwd()
        if "save" not in os.listdir(out_path):
            # Debug here for no save folder
            return None

        if len(os.listdir(out_path + "/save")) < 1:
            # Debug here for no map in folder, or just a warning
            pass

        # todo: Update the map to have a map selector in the future

        new_save = MemoryPoint()
        new_save.comp_dp(self.datapoints)
        new_save.pickle_dp(out_path + "/save")


class DataPoint:
    def __init__(self):
        self.title = Text("", [1280 / 2, 720 / 2], 24, "impact", BLACK, None)
        self.description = Description()
        self.icon = Icon(LIME_GREEN, [0, 0], 5, 5)
        self.associated = []  # Other points related/connecting to this one
        self.line_color = []  # Line colors for connecting related points
        self.id = 0
        self.sel_page = 0

    def change_title(self, in_text):
        if 0 <= len(self.title.text) < 30 and in_text not in [-14, 0]:
            self.title.text += chr(in_text)
        elif in_text == -14 and len(self.title.text) < 30:
            self.title.text += " "
        elif in_text == 0 and 0 < len(self.title.text):
            self.title.text = self.title.text[:-1]
        self.title.render()

    def change_description(self, in_desc):
        self.description = [""]
        desc_len = len(in_desc)
        max_char = 50  # How many characters per line
        for each_line in range(0, desc_len, max_char):
            self.description += [each_line]

    def change_icon_color(self, new_color):
        self.icon.color = new_color

    def change_icon_location(self, x, y):
        self.icon.rect.x = x
        self.icon.rect.y = y
        self.icon.shadow_rect.x = x + self.icon.width // 3
        self.icon.shadow_rect.y = y + self.icon.height // 3
        self.icon.center = self.icon.rect.center

    def change_icon_radius(self, new_radius):
        self.icon.radius = new_radius

    def change_icon_border(self, new_border):
        # Also known as "change_icon_edges"
        self.icon.border = new_border

    def change_id(self, new_id):
        self.id = new_id

    def add_point(self, in_point, line_color):
        # Add associated points to connect to this one
        self.associated += [in_point]
        self.line_color += [line_color]

    def remove_point(self, in_point):
        point_index = self.associated.index(in_point)
        del self.associated[point_index]
        del self.line_color[point_index]

    def update(self):
        pass

    def render(self, screen, x_offset, y_offset):
        self.icon.render(screen, x_offset, y_offset)

    def render_lines(self, screen, x_offset, y_offset):
        if 0 < len(self.associated):
            for li in range(len(self.associated)):
                # Line Shadow
                pygame.draw.line(screen, DARK_GREY,
                                 (self.icon.center[0] + x_offset + 1,
                                  self.icon.center[1] + y_offset + 1),
                                 (self.associated[li].icon.center[0] + x_offset + 1,
                                  self.associated[li].icon.center[1] + y_offset + 1), 2)

                # Actual Line
                pygame.draw.line(screen, self.line_color[li],
                                 (self.icon.center[0] + x_offset, self.icon.center[1] + y_offset),
                                 (self.associated[li].icon.center[0] + x_offset,
                                  self.associated[li].icon.center[1] + y_offset), 2)


class Description:
    def __init__(self):
        self.pages = [""]
        self.char_per_line = 40
        self.font_size = 40
        self.blink_timer = 0
        self.current_page = []

    def add_page(self):
        self.pages += [""]

    def write_page(self, page_num, letter_num):
        if 0 <= page_num < len(self.pages) and 0 < letter_num and \
                len(self.pages[page_num]) < (12 * self.char_per_line):
            self.pages[page_num] += chr(letter_num)
        elif letter_num < 0:
            self.pages[page_num] += " "
        else:
            self.erase_write(page_num)
        self.split_text(page_num)

    def erase_write(self, page_num):
        if 0 <= page_num < len(self.pages) and \
                0 < len(self.pages[page_num]):
            self.pages[page_num] = self.pages[page_num][:-1]
            self.split_text(page_num)

    def split_text(self, page_num):
        line_list = []
        check_text = Text("", (self.char_per_line, len(line_list) *
                               self.font_size * 4 / 5), self.font_size,
                          "impact", BLACK, None)
        for each_char in self.pages[page_num]:
            if check_text.text_rect.width < 1280 - self.font_size:
                check_text.text += each_char
                check_text.render()
            else:
                line_list += [check_text.text]
                check_text.text = each_char
                check_text.render()
        self.current_page = line_list + [check_text.text]

    def render_page(self, screen, page_num):
        line_iter = 0
        end_rect = None

        for each_line in self.current_page:
            text = Text(each_line, (0, 0), self.font_size, "impact",
                        BLACK, None)
            screen.blit(text.text_img, (10, line_iter * (self.font_size + 20)))
            end_rect = pygame.Rect(text.text_rect.width + 15,
                                           line_iter * (self.font_size + 20),
                                           self.font_size / 8, self.font_size)
            line_iter += 1

        # Render typing bar
        if 0 < pygame.time.get_ticks() - self.blink_timer < 700:
            if end_rect:
                pygame.draw.rect(screen, BLACK, end_rect)
            else:
                pygame.draw.rect(screen,
                                 BLACK,
                                 [10, 5,
                                  self.font_size / 8, self.font_size])

        if 1400 < pygame.time.get_ticks() - self.blink_timer:
            self.blink_timer = pygame.time.get_ticks()

        # Old rendering with an integer limit
        """if 0 <= page_num < len(self.pages):
            pos_iter = 0
            total_words = 13 * self.char_per_line
            end_rect = None

            for text_index in range(0,
                                    total_words -
                                    self.char_per_line,
                                    self.char_per_line):
                text = Text(self.pages[page_num][text_index:text_index +
                                                 self.char_per_line],
                            (pos_iter + self.char_per_line, text_index),
                            self.font_size, "impact", BLACK, None)
                screen.blit(text.text_img, (10,
                                            text.text_rect.y + 20))
                pos_iter += 1

                if 0 < len(self.pages[page_num][
                           text_index:text_index + self.char_per_line]) <= \
                        self.char_per_line:
                    end_rect = pygame.Rect(text.text_rect.width + 20,
                                           text.text_rect.y +
                                           (text.text_rect.height / 2),
                                           self.font_size / 4, self.font_size)

            # Render typing bar
            if 0 < pygame.time.get_ticks() - self.blink_timer < 700:
                if end_rect:
                    pygame.draw.rect(screen, BLACK, end_rect)
                else:
                    pygame.draw.rect(screen,
                                     BLACK,
                                     [10, 5,
                                      self.font_size / 4, self.font_size])

            if 1400 < pygame.time.get_ticks() - self.blink_timer:
                self.blink_timer = pygame.time.get_ticks()"""


class Icon:
    def __init__(self, in_color, location, width, height):
        self.color = in_color
        self.rect = pygame.Rect(location[0], location[1],
                                width, height)
        self.center = self.rect.center
        self.height = height
        self.width = width
        self.border = 0
        # We add a third of the width/height to proportionally scale shadows
        self.shadow_rect = pygame.Rect(location[0] + width // 3,
                                       location[1] + height // 3,
                                       width, height)

    def render(self, screen, x_offset, y_offset):
        # Icon shadow
        pygame.draw.rect(screen, DARK_GREY, [self.shadow_rect.x + x_offset,
                                             self.shadow_rect.y + y_offset,
                                             self.shadow_rect.width, self.shadow_rect.height],
                         border_radius=self.border)

        # Actual icon/button
        pygame.draw.rect(screen, self.color, [self.rect.x + x_offset,
                                              self.rect.y + y_offset,
                                              self.rect.width, self.rect.height],
                         border_radius=self.border)


class Circle:
    def __init__(self, in_color, location, in_radius):
        self.color = in_color
        self.center = location
        self.radius = in_radius

        self.display_options = False

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)


class Rect:
    def __init__(self, in_color, location, width, height):
        self.color = in_color
        self.center = (location[0] - (width / 2),
                       location[1] - (height / 2))
        self.height = height
        self.width = width
        self.rect = pygame.Rect(location[0], location[1],
                                width, height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


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
                    scene.save_map()
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
                scene.save_map()
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
    start_scene = Map(start_game.memory)
    # Initialize the first scene/starting scene shown to the player
    start_game.run(game_width, game_height, start_scene)  # Run the game loop
    """The game loop will be stuck at this line (start_game.run) until the
    while loop (while self.running:) is no longer true. When self.running is
    False, the program will move onto the next line to quit"""

    pygame.quit()  # Quit the game/pygame instance
