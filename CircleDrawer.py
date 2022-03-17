import pygame, sys, datetime
from Graphics import Line, Polygon, Rectangle, Circle

# create screen
pygame.init()
pygame.display.set_caption("Circle Drawer")
screen = pygame.display.set_mode((800, 800))

# set up program
points = []
mode = "select"
center = None
circles = []
outlineColor = (0, 0, 0)
fillColor = (255, 0, 0)

while True:
    events = pygame.event.get()
    screen.fill((255, 255, 255))

    # draw all circles
    for circle in circles:
        circle.fill(screen, fillColor)
        circle.outline(screen, outlineColor)

    if mode == "select":
        # draw rectangle at current mouse position
        rectangle = Rectangle(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5, 10, 10)
        rectangle.outline(screen, outlineColor)
        
        for e in events:
            # when clicked, add point as center
            if e.type == pygame.MOUSEBUTTONDOWN:
                center = pygame.mouse.get_pos()
                mode = "drag"
                
    elif mode == "drag":
        # draw circle at mouse position
        radius = max(abs(pygame.mouse.get_pos()[0] - center[0]), abs(pygame.mouse.get_pos()[1] - center[1]))
        circle = Circle(center, radius)
        circle.fill(screen, fillColor)
        circle.outline(screen, outlineColor)
        
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                # when mouse is lifted, add radius
                circles.append(circle)
                mode = "select"

    # check for quits
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # screenshot
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_f:
                pygame.image.save(screen, "Screenshots/Screenshot_" + datetime.datetime.now().strftime(r"%d_%m_%Y_%H_%M_%S") + ".jpg")

    pygame.display.flip()