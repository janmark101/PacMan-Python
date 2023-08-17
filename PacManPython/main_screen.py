import pygame

class Button():
    def __init__(self,image,center,screen):
        self.screen = screen
        self.normal_button_image = image
        self.center = center
        self.png = image
        self.x = self.center[0]
        self.y = self.center[1]
        self.png_size = self.png.get_size()
        self.png_rect =self.png.get_rect()
        self.png_rect = self.png_rect.move(self.x,self.y)

    def enlarge_png(self,mouse_pos_x,mouse_pos_y,image,x,y):
        if self.center[0] <= mouse_pos_x <= self.center[0] + self.png.get_width() and \
                self.center[1] <= mouse_pos_y <= self.center[1] + self.png.get_height():
            self.png = pygame.image.load(image)
            self.center = (self.x-x, self.y-y)
        else:
            self.png = self.normal_button_image
            self.center = (self.x, self.y)

    def show_logo(self):
        pac_man_logo = pygame.image.load("Logo/pacman_logo.png")
        pac_man_bg_image = pygame.transform.scale(pygame.image.load("Logo/pac_man_bg_image.png"), (340, 140))
        self.screen.blit(pac_man_logo,(140,100))
        self.screen.blit(pac_man_bg_image,(230,600))

    def show_button(self):
        self.screen.blit(self.png, (self.center))