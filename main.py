import constants
import pygame


def setup(screen):
    pass


def update(screen):
    screen.fill(constants.COLOR_BACKGROUND)
    pass


def on_mouse_button_down(pos, button):
    pass


def on_mouse_button_up(pos, button):
    pass


def main():
    pygame.init()
    screen = pygame.display.set_mode(constants.SIZE)
    setup(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_button_down(event.pos, event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                on_mouse_button_up(event.pos, event.button)

        update(screen)
        pygame.display.flip()


main()
