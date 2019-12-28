import pygame
import pygame.gfxdraw


class Textbox:
    def __init__(self, x, y, width, height, name, bk_color=(150, 150, 150),
                 border_thx=6, border_color=(0, 0, 0), active_color=(255, 255, 255), text_size=20, text_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.bk_color = bk_color
        self.border_thx = border_thx
        self.border_color = border_color
        self.active_color = active_color
        self.active = False
        self.text = ""
        self.text_size = text_size
        self.text_color = text_color
        self.font = pygame.font.Font("fonts\\Montserrat-Medium.otf", text_size)
        self.name = name

    def draw(self, surface):
        if self.active:
            self.image.fill(self.active_color)
        else:
            self.image.fill(self.bk_color)
        border = pygame.Rect(self.x - self.border_thx/2,
                             self.y - self.border_thx/2, self.width + self.border_thx, self.height + self.border_thx)
        pygame.gfxdraw.box(surface, border, self.border_color)
        text = self.font.render(self.text, False, self.text_color)
        if self.active:
            self.image.blit(text, ((self.width + self.border_thx)/2 - text.get_width() /
                                2, self.height/2 - text.get_height()/2))
        else:
            self.image.blit(text, (10, self.height/2 - text.get_height()/2))
        surface.blit(self.image, self.pos)
        
        title = pygame.font.Font("fonts\\Montserrat-Black.otf", self.text_size).render(self.name, False, self.text_color)
        surface.blit(title, (self.x - self.border_thx + self.width/2 - title.get_width()/2, self.y - self.height))
    def addText(self, key):
        valid = False
        if key <= 0:
            return valid
        if (chr(key) >= 'a' and chr(key) <= 'z') or (chr(key) >= 'A' and chr(key) <= 'Z') or chr(key) is ' ':
            appText = list(self.text)
            appText.append(chr(key))
            self.text = ''.join(appText)
            valid = True
        elif key is 8 and len(self.text) is not 0:
            appText = list(self.text)
            appText.pop()
            self.text = ''.join(appText)
        elif key is 27 or chr(key) is '\r':
            self.active = False
        return valid


    def isClicked(self, mouse):
        if mouse[0] >= self.x and mouse[0] <= self.x + self.width and mouse[1] >= self.y and mouse[1] <= self.y + self.height:
            self.active = True
        else:
            self.active = False


class NumBox(Textbox):
    def __init__(self, x, y, width, height, name, bk_color=(150, 150, 150),
                 border_thx=6, border_color=(0, 0, 0), active_color=(255, 255, 255), text_size=20, text_color=(0, 0, 0)):
        super().__init__(x, y, width, height, name, bk_color=(150, 150, 150),
                         border_thx=6, border_color=(0, 0, 0), active_color=(255, 255, 255), text_size=20, text_color=(0, 0, 0))
        self.decimal = False

    def addText(self, key):
        if key <= 0:
            return
        if chr(key) >= '0' and chr(key) <= '9':
            appText = list(self.text)
            appText.append(chr(key))
            self.text = ''.join(appText)
        elif key is 8 and len(self.text) is not 0:
            appText = list(self.text)
            if appText[len(appText) - 1] is '.':
                self.decimal = False
            appText.pop()
            self.text = ''.join(appText)
        elif key is 27 or chr(key) is '\r':
            self.active = False
        elif chr(key) is '.' and self.decimal is not True:
            appText = list(self.text)
            appText.append(chr(key))
            self.text = ''.join(appText)
            self.decimal = True
        elif chr(key) is '-' and self.text is "":
            appText = list(self.text)
            appText.append(chr(key))
            self.text = ''.join(appText)

class Button(Textbox):
    def __init__(self, x, y, width, height, name, bk_color=(150, 150, 150),
                 border_thx=2, border_color=(0, 0, 0), active_color=(255, 255, 255), text_size=28, text_color=(0, 0, 0)):
        super().__init__(x, y, width, height, name, bk_color=(150, 150, 150),
                         border_thx=2, border_color=(0, 0, 0), active_color=(255, 255, 255), text_size=28, text_color=(0, 0, 0))
        self.active = False
        self.text = name
    def draw(self, surface):
        if self.active:
            self.image.fill(self.active_color)
        else:
            self.image.fill(self.bk_color)
        border = pygame.Rect(self.x - self.border_thx/2,
                             self.y - self.border_thx/2, self.width + self.border_thx, self.height + self.border_thx)
        pygame.gfxdraw.box(surface, border, self.border_color)
        text = self.font.render(self.text, False, self.text_color)
        self.image.blit(text, (10, self.height/2 - text.get_height()/2))
        surface.blit(self.image, self.pos)