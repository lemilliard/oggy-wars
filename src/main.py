from math import atan2, pi, radians, cos, sin

import kivy
from kivy.graphics.transformation import Matrix
from kivy.utils import boundary

from model import shooter
from model.bullet import Bullet

kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty, Clock

from model.shooter import Shooter

class Game(Widget):
    shooter1 = ObjectProperty(Shooter())
    shooter2 = ObjectProperty(Shooter())
    bullet = None

    def init(self, dt):
        self.shooter1.init_canon1()
        self.shooter2.init_canon2()
        return False


    def on_touch_down(self, touch):
        if touch.x < self.width / 2:
            if not self.shooter1.collide_point(*touch.pos):
                if touch.x > self.shooter1.right:
                    # if the current touch is already in the 'rotate' mode, rotate the tower.
                    dx = touch.x - self.shooter1.center_x
                    dy = touch.y - self.shooter1.center_y
                    angle = boundary(atan2(dy, dx) * 180 / pi, -80, 80)

                    angle_change = self.shooter1.shooter_canon.rotation - angle
                    rotation_matrix = Matrix().rotate(-radians(angle_change), 0, 0, 1)
                    self.shooter1.shooter_canon.apply_transform(rotation_matrix, post_multiply=True, anchor=(0, 15))
                    self.fire()
                return False
            else:
                touch.ud['shooter_touch'] = True
                return True
        else:
            if not self.shooter2.collide_point(*touch.pos):
                if touch.x < self.shooter2.x:
                    # if the current touch is already in the 'rotate' mode, rotate the tower.
                    dx = touch.x - self.shooter2.center_x
                    dy = touch.y - self.shooter2.center_y
                    angle = boundary(atan2(dy, -1 * dx) * 180 / pi, -80, 80)

                    angle_change = self.shooter2.shooter_canon.rotation + angle
                    # self.angle = -radians(angle_change)
                    rotation_matrix = Matrix().rotate(-radians(angle_change), 0, 0, 1)
                    self.shooter2.shooter_canon.apply_transform(rotation_matrix, post_multiply=True, anchor=(100, 15))
                    self.shooter2.fire()
                return False
            else:
                touch.ud['shooter_touch'] = True
                return True


    def fire(self):
        # if self.bullet:
            # if there is already a bullet existing (which means it's flying around or exploding somewhere)
            # don't fire.
            # return

        # create a bullet, calculate the start position and fire it.
        tower_angle = radians(self.shooter1.shooter_canon.rotation)
        tower_position = self.shooter1.pos
        bullet_position = (
        tower_position[0] + 48 + cos(tower_angle) * 130, tower_position[1] + 70 + sin(tower_angle) * 130)
        self.bullet = Bullet(angle=tower_angle)
        self.bullet.center = bullet_position
        self.add_widget(self.bullet)
        self.bullet.fire()

    def on_touch_move(self, touch):
        ud = touch.ud

        if touch.x < self.width / 2:
            if 'shooter_touch' in ud:
                tmp = self.shooter1.center_y
                self.shooter1.center_y += touch.y - self.shooter1.center_y
                self.shooter1.shooter_canon.center_y += touch.y -tmp
        else:
            if 'shooter_touch' in ud:
                tmp = self.shooter2.center_y
                self.shooter2.center_y += touch.y - self.shooter2.center_y
                self.shooter2.shooter_canon.center_y += touch.y -tmp

class GameApp(App):
    def build(self):
        game = Game()
        Clock.schedule_interval(game.init, 0.01)
        return game


if __name__ == '__main__':
    GameApp().run()
