"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

The Breakout game.
    - Start Game:
        1. Click to start game
        2. Wait loading bar until 100%

    - Game Rule:
        0. User have NUM_LIVES chance to play the game.
        1. User will play ball by click mouse.
        2. User will control paddle by mouse move.
        3. If "User have no chance" or "All bricks be removed" or "Time out", game over.

    - Ball Touch:
        1. Window frame(except the floor) : the ball will rebound.
        2. The floor : the ball will back to start position, and lose one chance,
        3. Paddle :
            1. Padddle still, the ball will rebound.
            2. Paddle moves in the same direction as Ball, ball will speed up at x-axis way.
            3. Paddle moves in the same direction as Ball, ball will speed down at x-axis way.
            3-1. If Paddle moves faster than Ball, may be ball will moves at opposite direction.
        4. Bricks:
            1. The ball will rebound and bricks touched will be removed.
            2. When the bricks be removed, it may drop gifts by different color.

    - Gift:
        1. Gifts of different colors have different Buff.
        2. If Paddle get the gift, the buff will take effect.
"""

from campy.gui.events.timer import pause
from breakoutgraphics_extention import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked
from campy.graphics.gcolor import GColor

from random import random, randint

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 5			# Number of attempts
GAME_TIME = 90         # Game time (second)


def main():
    # Add the animation loop here!
    game_time = 0

    graphics = BreakoutGraphics(title="Bricks")
    main_game(graphics)

def main_game(graphics):

    dx = 0
    dy = 0
    paddle_x1 = paddle_x2 = paddle_dx = 0
    touch = None
    gift = None
    num_lives = 0
    time = 0
    background_y = 0
    score_plus_y = buff_plus_y = 0
    score_plus = 10
    reason = buff_name = "Hit! "

    # Set life icon
    graphics._life.text = rep("❤", NUM_LIVES)
    graphics._life.x = graphics.window.width - graphics._life.width - 10

    # Set Timer
    game_time = GAME_TIME
    time_minute = int(round((game_time - time) // 60, 0))
    time_sec = min(int(round((game_time - time) % 60, 0)), 59)
    graphics._time.x = (graphics.window.width - graphics._time.width) / 2

    if time_sec < 10:
        graphics._time.text = f"{time_minute}:0{time_sec}"
    else:
        graphics._time.text = f"{time_minute}:{time_sec}"

    # Start Gamer
    graphics.game_start()
    onmouseclicked(graphics.loading_page)

    # 因為 window.width 設計的關係，磚塊Rows大於Cols時，磚塊會在視窗外面
    if graphics.get_bricks_row() > graphics.get_bricks_cols():
        remain_bricks = graphics.get_bricks_cols() ** 2
    else:
        remain_bricks = graphics.get_bricks_row() * graphics.get_bricks_cols()

    while True:
        # Background Animation
        if graphics.window.height - graphics.background_img.height <= graphics.background_img.y:
            graphics.background_img.y -= 1
        else:
            graphics.background_img.y = 0

        if num_lives < NUM_LIVES and remain_bricks > 0 and game_time - time > 0:
            # Start the ball
            if dx == 0 and dy == 0:
                dx = graphics.get_ball_dx()
                dy = graphics.get_ball_dy()

            else:
                # Ball move
                graphics.ball.move(dx=dx, dy=dy)

                # Paddle move speed. (per 0.5 sec)
                time_diff_2 = round((game_time - time) % 60 * 10 % 1, 2) * 50
                if time_diff_2 % 2 == 1:
                    paddle_x2 = graphics.paddle.x + graphics.paddle.width / 2
                else:
                    paddle_x1 = graphics.paddle.x + graphics.paddle.width / 2
                    paddle_dx = (paddle_x1 - paddle_x2) / graphics.window.width * 100

                # window rebound
                if graphics.ball.x < 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                    dx = -dx
                if graphics.ball.y < 0:
                    dy = -dy

                # bricks rebound (不能用切點，會把自己消除掉 !!)
                points = [graphics.window.get_object_at(graphics.ball.x, graphics.ball.y),
                          graphics.window.get_object_at(graphics.ball.x + graphics.ball.width, graphics.ball.y),
                          graphics.window.get_object_at(graphics.ball.x, graphics.ball.y + graphics.ball.height),
                          graphics.window.get_object_at(graphics.ball.x + graphics.ball.width, graphics.ball.y + graphics.ball.height)
                          ]

                new_points = [0, 0, 0, 0]

                # To Avoid Sensor mistake (eg. background, score_plus)
                for i in range(4):
                    if points[i] is graphics.background_img or points[i] is graphics.score_plus:
                        new_points[i] = None
                    else:
                        new_points[i] = points[i]

                # To define upper sensor or lower sensor, and using "OR" to find touch point and decide the order.
                touch_upper = new_points[0] or new_points[1]
                touch_lower = new_points[2] or new_points[3]
                touch = touch_upper or touch_lower

                # If paddle and ball move by the same direction, the ball speed up, otherwise speed down.
                if touch is graphics.paddle:
                    dx = min(max(dx + paddle_dx, -6), 6)

                # Ball Touch bricks
                if touch is not None:
                    if touch is not graphics.paddle \
                            and touch is not graphics.score_label \
                            and touch is not graphics._life \
                            and touch is not graphics._time\
                            and touch is not graphics.score_plus\
                            and touch is not graphics.background_img\
                            and touch is not gift\
                            and touch is not graphics.buff_plus:

                        # Random gift
                        if gift is None:
                            create_gift = graphics.create_gift(touch)
                            if create_gift is not None:
                                gift = create_gift
                                graphics.window.add(gift)

                        # To Control there is only one gift on the window
                        if gift is not None:
                            if gift.y >= graphics.window.height:
                                create_gift = graphics.create_gift(touch)
                                if create_gift is not None:
                                    gift = create_gift
                                    graphics.window.add(gift)

                        # Score plus
                        # print(touch.color, touch.fill_color)
                        if graphics.paddle.fill_color.rgb == touch.fill_color.rgb:
                            score_plus += 10
                            reason = "Same Color! "

                        score_plus_y = 0
                        graphics.score_plus.text = f"{reason}: + {score_plus}"
                        graphics.window.add(graphics.score_plus, x=touch.x, y=touch.y - 1)

                        # Score
                        graphics._score += score_plus
                        graphics.score_label.text = f"Score: {graphics._score}"
                        score_plus = 10
                        reason = "Hit! "

                        # rebound and minus a remain_brick
                        graphics.window.remove(touch)
                        remain_bricks -= 1
                        if touch_lower is not None:
                            if touch_lower.y >= touch.y:
                                dy = -dy
                        else:
                            dy = abs(dy)

                        # Change paddle color
                        paddle_color = graphics.brick_color[randint(1, len(graphics.brick_color) - 1)]
                        graphics.paddle.fill_color = paddle_color
                        graphics.paddle.color = graphics.paddle.fill_color

                    # if touch is graphics.paddle:
                    #     if dy > 0:
                    #         dy = -dy
                    #         graphics.ball.y = graphics.paddle.y - graphics.ball.height

                    # Upper-side of the ball touch paddle
                    if touch_upper is graphics.paddle:
                        graphics.ball.y = graphics.paddle.y + graphics.paddle.height

                    # Lower-side of the ball touch paddle
                    if touch_lower is graphics.paddle:
                        graphics.ball.y = graphics.paddle.y - graphics.ball.height
                        dy = -dy

            # Gift move
            if gift is not None:
                gift.move(dx=0, dy=3)

            # Get the gift
            if gift is not None:
                if graphics.paddle.y <= gift.y + gift.height <= graphics.paddle.y + graphics.paddle.height \
                        and graphics.paddle.x <= gift.x + gift.width/2 <= graphics.paddle.x + graphics.paddle.width:

                    graphics.window.remove(gift)

                    # Gift Bonus
                    if compare_color(gift.fill_color.rgb, "LIGHTPINK"):
                        num_lives -= 1
                        # life count
                        graphics._life.text = rep("❤", NUM_LIVES - num_lives)
                        graphics._life.x = graphics.window.width - graphics._life.width - 10
                        buff_name = " + Life! "

                    elif compare_color(gift.fill_color.rgb, "LIGHTBLUE"):
                        graphics.change_paddle(1.5)
                        graphics.paddle.fill_color = gift.fill_color
                        buff_name = " Lengthen! "

                    elif compare_color(gift.fill_color.rgb, "YELLOW"):
                        if dy != 0:
                            dy = min(abs(dy) + 5, 15) * dy/max(abs(dy), -float("inf"))
                        buff_name = " Speed! "

                    elif compare_color(gift.fill_color.rgb, "LIGHTGREEN"):
                        reason = "Green Buff! "
                        score_plus *= 20
                        buff_name = " Bonus! "

                    elif compare_color(gift.fill_color.rgb, "BLACK"):
                        graphics.change_paddle(0.75)
                        buff_name = " Shorten! "

                    elif compare_color(gift.fill_color.rgb, "GRAY"):
                        graphics._score = int(round(graphics._score / 2, 0))
                        buff_name = " Half Score! "

                    elif compare_color(gift.fill_color.rgb, "GoldenRod"):
                        if dy != 0:
                            dy = max(dy / 2, 3) * dy/max(abs(dy), -float("inf"))
                        buff_name = " Slow! "

                    buff_plus_y = 0
                    graphics.buff_plus.text = f"{buff_name}"
                    graphics.buff_plus.color = gift.fill_color

                    if gift.x + graphics.buff_plus.width >= graphics.window.width:
                        gift.x = graphics.window.width - graphics.buff_plus.width

                    graphics.window.add(graphics.buff_plus, x=int(gift.x), y=int(gift.y) - 6)

                    gift = None

            # tiktok
            time += FRAME_RATE / 1000
            time_minute = int(round((game_time - time) // 60, 0))
            time_sec = min(int(round((game_time - time) % 60, 0)), 59)

            if time_sec < 10:
                graphics._time.text = f"{time_minute}:0{time_sec}"
            else:
                graphics._time.text = f"{time_minute}:{time_sec}"

            graphics._time.x = (graphics.window.width - graphics._time.width) / 2

            # Score plus animation
            score_plus_y -= 0.2
            graphics.score_plus.y += score_plus_y
            if score_plus_y == -6:
                score_plus_y = 0
                graphics.window.remove(graphics.score_plus)

            # Buff plus move
            if graphics.buff_plus is not None:
                graphics.buff_plus.move(dx=0, dy=-0.01)

            # Buff plus animation
            buff_plus_y -= 0.5
            graphics.buff_plus.y += 1
            if buff_plus_y == -10:
                buff_plus_y = 0
                graphics.window.remove(graphics.buff_plus)

            # Touch the floor.
            if graphics.ball.y + graphics.ball.height >= graphics.window.height:
                dx = 0
                dy = 0
                graphics.set_ball_dx(0)
                graphics.set_ball_dy(0)

                graphics.ball.x = (graphics.window.width - graphics.ball.width) / 2
                graphics.ball.y = (graphics.window.height - graphics.ball.height) / 2

                # life count
                num_lives += 1
                graphics._life.text = rep("❤", NUM_LIVES - num_lives)
                graphics._life.x = graphics.window.width - graphics._life.width - 10

            pause(FRAME_RATE)

        else:
            pause(FRAME_RATE * 10)
            graphics.end_game(remain_bricks)
            onmouseclicked(graphics.play_again)
            break


def rep(text, n):
    new_text = ""
    for i in range(n):
        new_text += text
    return new_text


def compare_color(object1_rgb, color):
    a = GColor.normalize(color)
    print(f"{a}, {a.rgb}, ")
    if object1_rgb == a.rgb:
        return True
    return False


if __name__ == '__main__':
    main()
