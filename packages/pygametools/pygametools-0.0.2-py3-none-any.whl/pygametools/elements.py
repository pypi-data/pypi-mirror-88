#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame


class ButtonText:
    def __init__(self, loc: tuple, size: tuple, border: int, colors: tuple, text: pygame.Surface, click_buttons: tuple) -> None:
        """
        Initializes the button.
        :param loc: Tuple (x, y) location (pixels).
        :param size: Tuple (x, y) size (pixels).
        :param border: Pixel width of border.
        :param colors: Tuple (r, g, b) of (idle color, hover color, click color, border color).
        :param text: pygame Surface to display.
        :param click_buttons: Buttons to register as click (1 = LMB, 2 = MMB, 3 = RMB)
        """
        self._loc = loc
        self._size = size
        self._border = border
        self._colors = colors
        self._text = text
        self._text_loc = (loc[0] + (size[0]-text.get_width()) // 2, loc[1] + (size[1]-text.get_height()) // 2)
        self._buttons = click_buttons

    def draw(self, window: pygame.Surface, events: list) -> None:
        """
        Draws button.
        :param window: Window to draw button on.
        :param events: List of pygame events.
        """
        loc = self._loc
        size = self._size
        color = (self._colors[2] if self.clicked(events) else self._colors[1]) if self.hovered() else self._colors[0]

        pygame.draw.rect(window, color, loc+size)
        pygame.draw.rect(window, self._colors[3], loc+size, self._border)
        window.blit(self._text, self._text_loc)

    def clicked(self, events: list) -> bool:
        """
        Checks if button is clicked.
        :param events: List of pygame events.
        """
        click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in self._buttons:
                click = True
                break

        if click and self.hovered():
            return True
        return False

    def hovered(self) -> bool:
        """
        Checks if the user is hovering over the button.
        """
        mouse_pos = pygame.mouse.get_pos()
        loc = self._loc
        size = self._size

        if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
            return True
        return False


class TextInput:
    def __init__(self, loc: tuple, size: tuple, border: int, colors: tuple, font: pygame.font.Font,
        init_text: str = "", label: str = "", password: bool = False, max_len: int = 30, cursor_speed: int = 20) -> None:
        """
        :param loc: Tuple (x, y) location (pixels).
        :param size: Tuple (x, y) size (pixels).
        :param border: Pixel width of border.
        :param colors: Tuple (r, g, b) of (background color, border color, text color).
        :param font: pygame font of text.
        :param init_text: Starting text.
        :param label: Label of text input.
        :param password: Display as password?
        :param max_len: Maximum length of text
        :param cursor_speed: Distance (frames) between flashes.
        """
        self._loc = loc
        self._size = size
        self._border = border
        self._colors = colors
        self._font = font
        self._text = init_text
        self._label = label
        self._password = password
        self._max_len = max_len
        self._cursor_speed = cursor_speed

        self._typing = False
        self._cursor_pos = 0
        self._frame = 0

    def draw(self, window: pygame.Surface, events: list) -> None:
        """
        Draws text input.
        :param window: Surface to draw on.
        :param events: List of pygame events.
        """
        self._frame += 1
        loc = self._loc
        size = self._size

        pygame.draw.rect(window, self._colors[0], loc+size)
        pygame.draw.rect(window, self._colors[1], loc+size, self._border)
        if not self._typing and self._text == "":
            text = self._font.render(self._label, 1, self._colors[2])
        else:
            text = self._font.render(self._text, 1, self._colors[2])
        text_loc = (loc[0] + (size[0]-text.get_width()) // 2, loc[1] + (size[1]-text.get_height()) // 2)
        window.blit(text, text_loc)
        if self._typing and (self._frame // self._cursor_speed) % 2 == 0:
            part_text = self._font.render(self._text[:self._cursor_pos], 1, self._colors[2])
            cursor_x = part_text.get_width() + text_loc[0]
            pygame.draw.line(window, (0, 0, 0), (cursor_x, loc[1]+12), (cursor_x, loc[1]+size[1]-12))

        mouse_pos = pygame.mouse.get_pos()
        mouse_in_border = loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._typing = mouse_in_border
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_TAB, pygame.K_ESCAPE):
                    self._typing = False
                elif event.key == pygame.K_LEFT:
                    self._cursor_pos = max(0, self._cursor_pos-1)
                elif event.key == pygame.K_RIGHT:
                    self._cursor_pos = min(len(self._text), self._cursor_pos+1)
                elif event.key == pygame.K_DELETE:
                    self._text = self._text[:self._cursor_pos] + self._text[self._cursor_pos+1:]
                elif event.key == pygame.K_BACKSPACE:
                    self._text = self._text[:self._cursor_pos-1] + self._text[self._cursor_pos:]
                    self._cursor_pos -= 1
                else:
                    if len(self._text) < self._max_len:
                        char = event.unicode
                        self._text = self._text[:self._cursor_pos] + char + self._text[self._cursor_pos:]
                        self._cursor_pos += 1