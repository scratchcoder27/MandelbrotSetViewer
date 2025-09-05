import pygame

class Button():
    """This is the base class for all the buttons used"""
    def __init__(self, text, textsize, pos: tuple, size: tuple, colour, image=None) -> None:
        '''Accepts the `text`, the `textsize`, the `position`(as a tuple), the  `color` and the `image path`(optional)'''
        self.org_colour = colour
        self.colour = colour
        if image==None:
            self.image = None
            font = pygame.font.SysFont('Consolas', textsize)
            self.text_surf = font.render(text, False, (255, 255, 255))
            self.textwidth, self.textheight = self.text_surf.get_width(), self.text_surf.get_height()
        else:
            self.image = pygame.image.load(image).convert_alpha()
            self.textwidth, self.textheight = self.image.get_width(), self.image.get_height()

        self.button_rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.posx, self.posy = pos[0], pos[1]
        self.width, self.height = size[0], size[1]

    def draw(self, screen : pygame.Surface):
        '''Draws the button. Accepts a screen'''
        pygame.draw.rect(screen, self.colour, self.button_rect, 2, 20)
        tx = self.posx + ((self.width // 2) - (self.textwidth // 2))
        ty = self.posy + ((self.height // 2) - (self.textheight // 2))
        if self.image == None:
            screen.blit(self.text_surf, (tx, ty))
        else:
            screen.blit(self.image, (tx, ty))


    def interact(self):
        pass

    def update(self, mx, my, mouse=False):
        tx = self.posx + self.width
        ty = self.posy + self.height

        if (mx > self.posx) and (mx < tx) and (my > self.posy) and (my < ty):
            self.colour = (200, 200, 200)
            if mouse:
                self.interact()
        else:
            self.colour = self.org_colour

class Slider():
    """This is the base class for all the sliders"""
    def __init__(self, pos:tuple, size:tuple, preset = 50, stylish=False, color1:tuple=(0, 0, 155), color2:tuple=(255, 255, 255)) -> None:
        self.progress = preset
        self.color = (color1, color2)
        self.pos = pos
        self.size = size
        self.coll_dist = 20
        self.style = stylish
        self.coll_rect = pygame.Rect(pos[0] - 10, pos[1] - self.coll_dist, size[0] + 20, size[1]+(self.coll_dist*2))
        self.main_slider_rect = pygame.Rect(pos[0], pos[1], size[0], size[1] - ((size[1] // 3) * 2))
        self.touched = False

    def update(self, mx, my, mouse=False):
        if mouse and self.coll_rect.collidepoint(mx, my):
            self.progress = int((mx - self.pos[0]) / self.size[0] * 100)
            if self.progress > 100:
                self.progress = 100
            elif self.progress < 0:
                self.progress = 0
            self.touched = True
        else:
            self.touched = False
    
    def draw(self, screen:pygame.Surface):
        centerx = self.pos[0] + (self.progress * self.size[0] / 100)
        color = list(self.color[0])
        for i, channel in enumerate(color):
            channel += (self.touched * 10)
            if channel > 255:
                channel = 255
            color[i] = channel
        color = tuple(color)
        if self.style:
            pygame.draw.rect(screen, self.color[0], pygame.Rect(self.main_slider_rect.x, self.main_slider_rect.y, centerx - self.main_slider_rect.x, self.main_slider_rect.h), border_radius=10)
            pygame.draw.rect(screen, self.color[1], pygame.Rect((self.main_slider_rect.x + self.main_slider_rect.w), self.main_slider_rect.y,centerx - (self.main_slider_rect.x + self.main_slider_rect.w), self.main_slider_rect.h), border_radius=10)
        else:
            pygame.draw.rect(screen, self.color[0], self.main_slider_rect, border_radius=10)
        pygame.draw.circle(screen, color, (centerx, self.pos[1] + self.size[1] / 3), (self.size[1] // 3)*2)
    
    def get_progress(self):
        return self.progress

class ToggleButton(Button):
    def __init__(self, pos: tuple, size: tuple, colour) -> None:
        super().__init__("NULL", 35, pos, size, colour)
        self.internalfontfordeletion = pygame.font.SysFont('Consolas', 20)
        self.click_timer = 5
        self.state = False
        self.interact()

    

    def update(self, mx, my, mouse=False):
        if self.click_timer > 0:
            self.click_timer -= 1

        tx = self.posx + self.width
        ty = self.posy + self.height

        if (mx > self.posx) and (mx < tx) and (my > self.posy) and (my < ty):
            if mouse:
                self.interact()
    
    def set_data(self, data : bool):
        self.state = data
    
    def interact(self) -> int:
        if self.click_timer < 1:
            self.state = not self.state
        self.colour = ((255, 0, 0), (0, 255, 0))[int(self.state)]
        self.text_surf = self.internalfontfordeletion.render(("OFF", "ON")[int(self.state)], False, self.colour)
        self.textwidth, self.textheight = self.text_surf.get_width(), self.text_surf.get_height()
        self.click_timer = 25

    def draw(self, screen : pygame.Surface):
        '''Draws the button. Accepts a screen'''
        pygame.draw.rect(screen, self.colour, self.button_rect, 0, 20)
        tx = self.posx + ((self.width // 2) - (self.textwidth // 2))
        ty = self.posy + ((self.height // 2) - (self.textheight // 2))
        screen.blit(self.text_surf, (tx, ty))

if __name__ == "__main__":

    pygame.init() #MAIN INIT

    WIDTH, HEIGHT = 500, 466
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Title Test')
    clock = pygame.time.Clock()

    class TestButton(Button):
        def interact(self):
            pygame.quit()
            exit()
        
    x = TestButton("Close Window", 40, ((WIDTH - 300) // 2, (HEIGHT - 50) // 4), (300, 50), (255, 255, 100))
    s = Slider((((WIDTH - 300) // 2), (HEIGHT - 50) // 1.5), (200, 10), 25, stylish=True)
    tb = ToggleButton(((WIDTH-150)//2, 350), (150, 50), (255, 255, 255))

    t = pygame.font.SysFont('Consolas', 20)
    

    def draw():
        screen.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        mouse = (pygame.mouse.get_pressed()[0])
        x.draw(screen)
        x.update(mx, my, mouse)
        s.draw(screen)
        s.update(mx, my, mouse)
        td = t.render(str(s.progress), True, (255, 255, 255))
        screen.blit(td, (10, 10))
        tb.update(mx, my, mouse)
        tb.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        draw()
        pygame.display.update()
        clock.tick(60)