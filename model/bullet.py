from math import pi, tan

import kivy
from kivy.animation import Animation
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.utils import boundary
from kivy.vector import Vector


class Bullet(Widget):
    angle = NumericProperty(0)

    def fire(self):
        destination = self.calc_destination(self.angle)
        speed = 100
        self.animation = self.create_animation(speed, destination)

        # start the animation
        self.animation.start(self)

    def create_animation(self, speed, destination):
        time = Vector(self.center).distance(destination) / (speed * +70.0)
        return Animation(x=destination[0], y=destination[1], duration=time, transition='linear')

    def calc_destination(self, angle):
        # calculate the path until the bullet hits the edge of the screen
        win = self.get_parent_window()
        # the following "magic numbers" are based on the dimensions of the
        # cutting of the image 'overlay.png'
        left = 150.0 * win.width / 1920.0
        right = win.width - 236.0 * win.width / 1920.0
        top = win.height - 50.0 * win.height / 1920.0
        bottom = 96.0 * win.height / 1920.0

        bullet_x_to_right = right - self.center_x
        bullet_x_to_left = left - self.center_x
        bullet_y_to_top = top - self.center_y
        bullet_y_to_bottom = bottom - self.center_y

        destination_x = 0
        destination_y = 0

        # this is a little bit ugly, but I couldn't find a nicer way in the hurry
        if 0 <= self.angle < pi / 2:
            # 1st quadrant
            if self.angle == 0:
                destination_x = bullet_x_to_right
                destination_y = 0
            else:
                destination_x = boundary(bullet_y_to_top / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_right, bullet_y_to_bottom, bullet_y_to_top)

        elif pi / 2 <= self.angle < pi:
            # 2nd quadrant
            if self.angle == pi / 2:
                destination_x = 0
                destination_y = bullet_y_to_top
            else:
                destination_x = boundary(bullet_y_to_top / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_left, bullet_y_to_bottom, bullet_y_to_top)

        elif pi <= self.angle < 3 * pi / 2:
            # 3rd quadrant
            if self.angle == pi:
                destination_x = bullet_x_to_left
                destination_y = 0
            else:
                destination_x = boundary(bullet_y_to_bottom / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_left, bullet_y_to_bottom, bullet_y_to_top)

        elif self.angle >= 3 * pi / 2:
            # 4th quadrant
            if self.angle == 3 * pi / 2:
                destination_x = 0
                destination_y = bullet_y_to_bottom
            else:
                destination_x = boundary(bullet_y_to_bottom / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_right, bullet_y_to_bottom, bullet_y_to_top)

        # because all of the calculations above were relative, add the bullet position to it.
        destination_x += self.center_x
        destination_y += self.center_y

        return (destination_x, destination_y)