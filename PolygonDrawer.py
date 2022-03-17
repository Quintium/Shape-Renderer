import pygame, sys, datetime
from Graphics import Line, Polygon, Rectangle, Circle

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
ctrlPressed = False
freeDraw = False

while True:
    events = pygame.event.get()

    if mode == "select":
        screen.fill((255, 255, 255))

        # draw lines between currently selected points
        for i in range(len(points) - 1):
            line = Line(points[i], points[i + 1])
            line.draw(screen, outlineColor)
            
        if points:
            line = Line(points[-1], pygame.mouse.get_pos())
            line.draw(screen, outlineColor)

        # draw rectangle at current mouse position
        rectangle = Rectangle(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5, 10, 10)
        rectangle.outline(screen, outlineColor)
        
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                # activate free draw if clicked while control is pressed
                if ctrlPressed:
                    freeDraw = True
                else:
                    # when clicked, add point to polygon
                    points.append(pygame.mouse.get_pos())

            if e.type == pygame.MOUSEBUTTONUP:
                freeDraw = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    # when space pressed, create polygon out of selected points
                    polygon = Polygon(points)

                    # draw polygon
                    screen.fill((255, 255, 255))
                    polygon.fill(screen, fillColor)
                    polygon.outline(screen, outlineColor)

                    mode = "draw"

                if e.key == pygame.K_LCTRL:
                    ctrlPressed = True

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LCTRL:
                    ctrlPressed = False

        # when free draw activate, add points constantly if they are different from the previous one
        if freeDraw and (not points or points[-1] != pygame.mouse.get_pos()):
            points.append(pygame.mouse.get_pos())
        

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