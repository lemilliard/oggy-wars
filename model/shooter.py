# module model.shooter
from math import atan2, radians, pi, cos, sin

import kivy
from kivy.graphics.transformation import Matrix

from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.scatter import Scatter
from kivy.utils import boundary

from model.bullet import Bullet

kivy.require('1.1.1')

from kivy.uix.widget import Widget


class Shooter(Widget):
    shooter_canon = ObjectProperty(Scatter())
    bullet = ObjectProperty(Bullet())

    def init_canon1(self):
        self.shooter_canon.center_y = self.center_y
        self.shooter_canon.x = self.center_x

    def init_canon2(self):
        self.shooter_canon.center_y = self.center_y
        self.shooter_canon.x = self.center_x - self.shooter_canon.width

    # def fire(self):
    #     if self.bullet:
    #         # if there is already a bullet existing (which means it's flying around or exploding somewhere)
    #         # don't fire.
    #         return
    #
    #     # create a bullet, calculate the start position and fire it.
    #     tower_angle = radians(self.shooter_canon.rotation)
    #     tower_position = self.pos
    #     bullet_position = (
    #         tower_position[0] + 48 + cos(tower_angle) * 130, tower_position[1] + 70 + sin(tower_angle) * 130)
    #     self.bullet = Bullet(angle=tower_angle)
    #     self.bullet.center = bullet_position
    #     self.add_widget(self.bullet)
    #     self.bullet.fire()

