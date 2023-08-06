Pygame Physics
==============

A simple way to manage physics in pygame.

The Physics() object contains all the info you need.

::

    p = Physics(

        # rect is a pygame.Rect object that represents the object on screen
        rect,

        # All of these values are vectors (x, y) where the x/y represent pixels per second
        initVelocity=(0, 0),
        initAcceleration=(0, 0),
        initAngularVelocity=0,
        initAngularAcceleration=0,
        friction=0,  # friction in pixels per second (for both x and y directions)
        angularFriction=0,  # degrees per second
    )