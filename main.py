from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.event import EventDispatcher



class PongBall(Widget):
    # velocity of the ball
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class GameOverEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_game_over')
        super(GameOverEventDispatcher, self).__init__(**kwargs)

    def define_game_over(self, value):
        # when define_game_over is called, the 'on_game_over' event will be
        # dispatched with the value
        self.dispatch('on_game_over', value)

    def on_game_over(self, *args):
        print 'entrou no dispatch do game over', args


class PongGame(Widget):
    ball = ObjectProperty(None)

    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off on top and on bottom
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
            if self.player2.score > 3:
                self.game_over_callback(self.player2.score, 'Player 2 Wins!')
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            if self.player1.score > 3:
                self.game_over_callback(self.player1.score, 'Player 1 Wins!')


    def on_touch_move(self, touch):
        if touch.x < self.width /3:
            self.player1.center_y = touch.y
        if touch.x > self. width - self.width/3:
            self.player2.center_y = touch.y


    def game_over_callback(value, *args):
        """
        calls event dispatcher to do something
        """
        ev_disp = GameOverEventDispatcher()
        ev_disp.define_game_over(args)


class PongApp(App):
    def build(self):
        sound = SoundLoader.load('resources/sound.mp3')
        if sound:
            # print("Sound found at %s" % sound.source)
            # print("Sound is %.3f seconds" % sound.length)
            sound.play()

    def set_state(self, state):
        if state == 'main_game':
            self.root.current = 'main_game'
            game = self.root.pong_game
            game.serve_ball()
            Clock.schedule_interval(game.update, 1.0/60.0)


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speedup = 1.1
            offset = 0.02 * Vector(0, ball.center_y-self.center_y)
            ball.velocity = speedup * (offset - ball.velocity)


if __name__ == '__main__':
    PongApp().run()
