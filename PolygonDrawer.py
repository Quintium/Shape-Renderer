import pygame, sys
from Polygon import Line, Polygon, Rectangle, Circle

# create screen
pygame.init()
pygame.display.set_caption("Polygon Drawer")
screen = pygame.display.set_mode((800, 800))

# set up program
points = []
mode = "select"
polygon = None
outlineColor = (0, 0, 0)
fillColor = (255, 0, 0)

while True:
    events = pygame.event.get()
    screen.fill((255, 255, 255))

    if mode == "select":
        # draw lines between currently selected points and rectangle at current mouse position
        for i in range(len(points) - 1):
            line = Line(points[i], points[i + 1])
            line.draw(screen, outlineColor)
        if points:
            line = Line(points[-1], pygame.mouse.get_pos())
            line.draw(screen, outlineColor)
        rectangle = Rectangle(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5, 10, 10)
        rectangle.outline(screen, outlineColor)
        
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                # when clicked, add point to polygon
                points.append(pygame.mouse.get_pos())
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                # when space pressed, create polygon out of selected points
                polygon = Polygon(points)
                mode = "draw"
    else:
        # fill polygon
        polygon.fill(screen, fillColor)
        polygon.outline(screen, outlineColor)

    # check for quits
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()