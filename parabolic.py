#!/usr/bin/python
# coding: utf-8
#
# Une simulation de lancer de pastèque
#
# Largement inspiré de https://fr.wikibooks.org/wiki/Pygame/Concevoir_des_jeux_avec_Pygame

VERSION = "0.1"

try:
    import sys
    import math
    import os
    import pygame
    from pygame.locals import *
    
except ImportError, err:
    print "Impossible de charger le module. %s" % (err)
    sys.exit(2)

def load_png(name):
    """Charge une image et retourne un objet image"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
            print "Impossible de charger l'image : ", fullname
            raise SystemExit, message
    return image, image.get_rect()

class Pasteque(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.initimage, self.initrect = load_png('pasteque.png')
        self.altimage, self.altrect = load_png('pasteque_ecrasee.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.miny = 600
        self.minx = 600
        self.initx = 50
        self.inity = 550
        self.speed = 6
        self.launched = False
        self.godown = False
        self.reset()
        
    def update(self):
        if self.godown and self.rect.centery > self.inity:
            self.launched = False
            self.godown = False
            x, y = self.rect.x, self.rect.y
            self.image, self.rect = self.altimage, self.altrect
            self.rect.x = x
            self.rect.y = y
        if self.launched:
            self.rect.centerx += self.speed
            oldy = self.rect.centery
            x = float(self.rect.centerx)            
            self.rect.centery = 600 - ((-9.8*x**2)/(2*(81**2)*math.cos(1.05)**2)+(math.tan(1.05)*x))
            if self.rect.centery < oldy:
                self.godown = True                        
    
    def launch(self):
        self.launched = True
        
    def reset(self):
        self.launched = False
        self.image, self.rect = self.initimage, self.initrect
        self.rect.centerx = self.initx
        self.rect.centery = self.inity
        
def main():
    # Initialisation de la fenêtre d'affichage
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Lancer de pastèque')

    # Remplissage de l'arrière-plan
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
        
    # Initialisation de la balle
    pasteque = Pasteque()

    # Initialisation des sprites
    pastequesprite = pygame.sprite.RenderPlain(pasteque)

    # Blitter le tout dans la fenêtre
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialisation de l'horloge
    clock = pygame.time.Clock()

    # Boucle d'évènements
    while 1:
        # S'assurer que le jeu ne fonctionne pas à plus de 60 images par secondes
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
				# taper "a" pour lancer
                if event.key == K_a:
                    pasteque.launch()
                # taper "r" pour initialiser
                if event.key == K_r:
                    pasteque.reset()

        screen.blit(background, pasteque.rect, pasteque.rect)
        pastequesprite.update()
        pastequesprite.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()
