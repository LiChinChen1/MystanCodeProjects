"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

The package drawing graphics for breakout game.

1. Init-
    - Create a graphical window, with some extra space
    - Background
    - Game start - welcome_img
    - Loading page
    - Paddle
    - A filled ball in the graphical window
    - Initial velocity for the ball
    - Bricks
    - Score counter
    - Life icon
    - Buff text
    - Game time
    - Game over
    - Reset or End game

2. game_start -
    - Create game start page.

3. loading_page-
    - Clear all object in game start page.
    - Loading Animation
    - Remove loading page
    - Call start_game()

4. start_game-
    - Create start game page
    - Initialize our mouse listeners

5. end_game-
    - Clear start_game object
    - Clear remains bricks
    - Check Win or Lose
    - Show game over page
    - Show Play again or not
    - call play_again()

6. play_again-
    - check user click yes or no
    - show end page.

7. change_paddle-
    - change the paddle width

8. paddle_move-
    - paddle move when mouse moved.

9. ball_move-
    - play ball when game start

10. create_gift-
    - Random gift color or None
    - Create gift.

11. getter -
    - get_ball_dx : get dx
    - get_ball_dy : get dy
    - get_bricks_row : BRICK_ROWS
    - get_bricks_cols : BRICK_COLS

12. setter -
    - set_ball_dx : set dx
    - set_ball_dy : set dy

"""
from campy.gui.events.timer import pause
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel, GLine
from campy.graphics.gimage import GImage
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from random import random, randint

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Height of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 150      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball

LOADING_BAR_HEIGHT = 40  # Height of the loading bar (in pixels)
LABEL_COLOR = "White"
SCORE_SIZE = 15


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout',):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Background img
        self.background_img = GImage("background_img.png")

        # Game start - welcome_img
        self.game_name = GLabel(" - The Breakout Game -")
        self.game_name.font = f"Dialog-20-bold"
        self.game_name.color = LABEL_COLOR

        self.welcome_label = GLabel(" Click to Start !!")
        self.welcome_label.font = f"Dialog-15-bold"
        self.welcome_label.color = LABEL_COLOR

        # Loading page.
        self.loading_gate = True
        self.loading_word = GLabel("Loading...")
        self.loading_word.font = f"Dialog-15-bold"
        self.loading_word.color = LABEL_COLOR

        # Frame of Loading bar.
        self.loading_bar_empty = GRect(self.window.width/2, LOADING_BAR_HEIGHT)
        self.loading_bar_empty.color = LABEL_COLOR

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height, x=(window_width-paddle_width)/2, y=window_height-paddle_offset)
        self.paddle.filled = True

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2, x=(window_width-ball_radius*2)/2, y=(window_height-ball_radius*2)/2)
        self.ball.filled = True
        self.ball.fill_color = "LightGreen"

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Default of bricks
        self.brick_rows = BRICK_ROWS
        self.brick_cols = BRICK_COLS
        self.brick_width = BRICK_WIDTH
        self.brick_height = BRICK_HEIGHT
        self.brick_offset = BRICK_OFFSET
        self.brick_spacing = BRICK_SPACING
        self.brick_color = ("Aquamarine", "Aquamarine", "CadetBlue", "CadetBlue",
                            "CornflowerBlue", "CornflowerBlue", "DarkCyan", "DarkCyan",
                            "DarkCyan", "DarkCyan")

        # Create Score counter
        self._score = 0
        self.score_size = int(SCORE_SIZE)
        self.score_label = GLabel(f"Score: {self._score}")
        self.score_label.font = f"Dialog-{self.score_size}-bold"
        self.score_label.color = LABEL_COLOR

        self.score_plus = GLabel(f"Hit!: +10")
        self.score_plus.font = f"Dialog-{int(self.ball.width)}-bold"
        self.score_plus.color = "Gold"

        # Create Buff text
        self.buff_plus = GLabel(f"")
        self.buff_plus.font = f"Verdana-{int(self.ball.width)}-bold"
        self.buff_plus.color = "Gold"

        # Create life icon
        self._life = GLabel(f"--")
        self._life.font = f"Dialog-{ball_radius}-bold"
        self._life.color = "red"

        # Create game time
        self._time = GLabel(f"00:00")
        self._time.font = f"Dialog-{ball_radius*5}-bold"
        self._time.color = "lightgray"

        # Create game over
        self.game_over_label = GLabel(f" - Game Over - ")
        self.game_over_label.font = f"Dialog-{int(ball_radius*1.5)}-bold"
        self.game_over_label.color = LABEL_COLOR

        self.game_over = GLabel(f"--")
        self.game_over.font = f"Dialog-{int(ball_radius*3.5)}-bold"
        self.game_over.color = "lightgray"

        # Reset or End game
        self.split_line = GLine(x0=window_width / 10 * 1, x1=window_width / 10 * 9,
                                y0=window_height / 100 * 70, y1=window_height / 100 * 70)
        self.split_line.color = "lightgray"

        self.reset_label = GLabel(f"PLAY AGAIN ?")
        self.reset_label.font = f"Dialog-{int(ball_radius * 1.5)}-bold"
        self.reset_label.color = "lightgray"

        self.reset_button_yes = GLabel(f" YES ")
        self.reset_button_yes.font = f"Dialog-{int(ball_radius * 1.3)}-bold"
        self.reset_button_yes.color = "lightgray"

        self.reset_button_no = GLabel(f" NO ")
        self.reset_button_no.font = f"Dialog-{int(ball_radius * 1.3)}-bold"
        self.reset_button_no.color = "lightgray"

        self.final_label = GLabel(f" No way! \n \n You Only Live Once !")
        self.final_label.font = f"Dialog-{int(ball_radius * 2)}-bold"
        self.final_label.color = "white"

    def game_start(self):

        self.window.add(self.background_img, x=0, y=0)

        self.window.add(self.game_name, x=(self.window.width - self.game_name.width) / 2,
                        y=(self.window.height - self.game_name.height) / 2)

        self.window.add(self.welcome_label, x=(self.window.width - self.welcome_label.width) / 2,
                        y=(self.window.height - self.welcome_label.height) / 2 + 40)

    def loading_page(self, event):

        if self.loading_gate:
            if event.x > -float('Inf'):
                self.loading_gate = False

            # Clear Game Name
            self.window.remove(self.welcome_label)
            self.window.remove(self.game_name)

            # Create Loading Bar
            self.window.add(self.loading_word, x=self.window.width / 4,
                            y=(self.window.height - LOADING_BAR_HEIGHT) // 2 - 30)

            self.window.add(self.loading_bar_empty, x=self.window.width / 4,
                            y=(self.window.height - self.loading_bar_empty.height) // 2)

            # Loading Animation
            i = 0
            while True:
                if i >= self.window.width/2:
                    break
                else:
                    self.loading_bar = GRect(i, self.loading_bar_empty.height)
                    self.loading_bar.filled = True
                    self.loading_bar.fill_color = LABEL_COLOR
                    self.window.add(self.loading_bar, x=self.window.width / 4,
                                    y=(self.window.height - self.loading_bar.height) // 2)
                    i += randint(1, 20)

                    pause(100)
                    self.window.remove(self.loading_bar)

            # Remove loading page
            self.window.remove(self.loading_bar_empty)
            self.window.remove(self.loading_word)

            # Start game
            self.start_game()

    def start_game(self):

        # Create a object
        self.window.add(self.paddle)
        self.window.add(self.score_label, x=5, y=self.score_size * 2)
        self.window.add(self._life, x=self.window.width - self._life.width - 10, y=self.window.height-10)
        self.window.add(self._time, x=(self.window.width - self._time.width)/2, y=(self.window.height + self._time.height*2)/2)
        self.window.add(self.ball)

        # Initialize our mouse listeners
        onmouseclicked(self.ball_move)
        onmousemoved(self.paddle_move)

        # Set bricks
        all_bricks_width = 0
        all_brick_height = self.brick_offset

        for i in range(self.brick_cols):
            for j in range(self.brick_rows):
                self.bricks = GRect(self.brick_width, self.brick_height, x=all_bricks_width, y=all_brick_height)
                self.bricks.filled = True
                self.bricks.color = self.brick_color[i]
                self.bricks.fill_color = self.brick_color[i]
                self.window.add(self.bricks)
                all_bricks_width += self.brick_width + self.brick_spacing
            all_brick_height += self.brick_height + self.brick_spacing
            all_bricks_width = 0

    def end_game(self, remain_bricks):

        # Clear start_game object
        self.window.remove(self._time)
        self.window.remove(self._life)
        self.window.remove(self.score_label)
        self.window.remove(self.ball)
        self.window.remove(self.paddle)
        self.window.remove(self.score_plus)

        # Clear remains bricks
        all_bricks_width = 0
        all_brick_height = self.brick_offset

        for i in range(self.brick_cols):
            for j in range(self.brick_rows):
                remain_brick = self.window.get_object_at(x=all_bricks_width, y=all_brick_height)
                self.window.remove(remain_brick)
                all_bricks_width += self.brick_width + self.brick_spacing
            all_brick_height += self.brick_height + self.brick_spacing
            all_bricks_width = 0

        # Add background back.
        self.window.add(self.background_img)

        # Check Win or Lose
        if remain_bricks > 0:
            self.game_over.text = f" You Lose ! "
            self.game_over.color = "IndianRed"
        else:
            self.game_over.text = f" You Win ! "
            self.game_over.color = "LIGHTGreen"

        # Show game over page
        self.window.add(self.game_over_label,
                        x=(self.window.width - self.game_over_label.width) / 2,
                        y=(self.window.height / 100) * 35)

        self.window.add(self.game_over,
                        x=(self.window.width - self.game_over.width)/2,
                        y=(self.window.height / 100) * 50)

        self.window.add(self.score_label,
                        x=(self.window.width - self.score_label.width) / 2,
                        y=(self.window.height / 100) * 60)

        self.window.add(self.split_line)

        # Show Play again or not
        self.window.add(self.reset_label,
                        x=(self.window.width - self.reset_label.width) / 2,
                        y=(self.window.height / 100) * 80)

        self.window.add(self.reset_button_yes,
                        x=(self.window.width/5) + self.reset_button_yes.width / 2,
                        y=(self.window.height / 100) * 90)

        self.window.add(self.reset_button_no,
                        x=(self.window.width/5)*3 + self.reset_button_no.width / 2,
                        y=(self.window.height / 100) * 90)

        # # Check play again or not
        # if onmouseclicked(self.play_again) == 'yes':
        #     print(f"graphics/end_game/onmouseclicked/yes")
        #     return True
        # elif onmouseclicked(self.play_again) == 'no':
        #     print(f"graphics/end_game/onmouseclicked/no")
        #     return False

    def play_again(self, event):
        check = self.window.get_object_at(event.x, event.y)

        if check is not None or check is not self.background_img:
            if check is self.reset_button_yes:
                self.window.remove(self.game_over)
                self.window.remove(self.game_over_label)
                self.window.remove(self.score_label)
                self.window.remove(self.split_line)
                self.window.remove(self.reset_label)
                self.window.remove(self.reset_button_yes)
                self.window.remove(self.reset_button_no)

                print(f"graphics/play_again/onmouseclicked/yes")
                self.window.add(self.final_label,
                                x=self.window.width / 10,
                                y=self.window.height/2 * 1.1)
                pause(1000)
                quit()
                # self.main_game(FRAME_RATE=self.frame_rate, NUM_LIVES=self.num_lives, GAME_TIME=self.game_time)

            elif check is self.reset_button_no:
                print(f"graphics/play_again/onmouseclicked/no")
                quit()

    def change_paddle(self, width_power=1, height_power=1):
        self.window.remove(self.paddle)
        self.paddle = GRect(min(self.paddle.width * width_power, self.window.width*.9),
                            self.paddle.height * height_power,
                            x=self.paddle.x,
                            y=self.paddle.y)
        self.paddle.filled = True
        self.paddle.fill_color = self.paddle.fill_color
        self.window.add(self.paddle)

    def paddle_move(self, event):
        self.paddle.x = event.x - self.paddle.width / 2
        if self.paddle.x <= 0:
            self.paddle.x = 0
        elif self.paddle.x + self.paddle.width >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width

    def ball_move(self, event):
        # if self.__dx == 0 and self.__dy == 0:
        self.__dx = randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random() > 0.5:
            self.__dx = -self.__dx

    def create_gift(self, touch):

        gift = GRect(BALL_RADIUS * 2, BALL_RADIUS * 2, x=touch.x, y=touch.y)
        gift.filled = True

        # Random color
        if random() > 0.95:
            gift_color = "LIGHTPINK"
        elif random() > 0.90:
            gift_color = "LIGHTBLUE"
        elif random() > 0.85:
            gift_color = "YELLOW"
        elif random() > 0.80:
            gift_color = "LIGHTGREEN"
        elif random() > 0.75:
            gift_color = "BLACK"
        elif random() > 0.70:
            gift_color = "GRAY"
        elif random() > 0.65:
            gift_color = "GoldenRod"
        else:
            gift_color = ""

        # Return Gift
        if gift_color != "":
            gift.fill_color = gift_color
            return gift
        else:
            return None

    def get_ball_dx(self):
        return self.__dx

    def get_ball_dy(self):
        return self.__dy

    def set_ball_dx(self, dx):
        self.__dx = dx

    def set_ball_dy(self, dy):
        self.__dy = dy

    @staticmethod
    def get_bricks_row():
        return BRICK_ROWS

    @staticmethod
    def get_bricks_cols():
        return BRICK_COLS

