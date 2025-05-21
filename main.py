import basic
import input
import led
from microbit import Button

# Spielfeld (3x3): None = leer, True = Spieler 1, False = Spieler 2
field = [[None for _ in range(3)] for _ in range(3)]

cursor_x = 0
cursor_y = 0
player = True  # True = Spieler 1, False = Spieler 2

# 3×3-Feld auf 5×5 Display abbilden
def map_x(x): return x + 1
def map_y(y): return y + 1

def clear_all():
    basic.clear_screen()

def draw(show_cursor):
    clear_all()
    for y in range(3):
        for x in range(3):
            val = field[y][x]
            if val is True:
                led.plot(map_x(x), map_y(y))
            elif val is False:
                led.unplot(map_x(x), map_y(y))
    if show_cursor and field[cursor_y][cursor_x] is None:
        led.plot(map_x(cursor_x), map_y(cursor_y))

def check_win():
    p = player
    for i in range(3):
        if field[i][0] == field[i][1] == field[i][2] == p: return True
        if field[0][i] == field[1][i] == field[2][i] == p: return True
    if field[0][0] == field[1][1] == field[2][2] == p: return True
    if field[0][2] == field[1][1] == field[2][0] == p: return True
    return False

def check_draw():
    for row in field:
        if None in row:
            return False
    return True

def move_cursor(dx, dy):
    global cursor_x, cursor_y
    cursor_x = max(0, min(2, cursor_x + dx))
    cursor_y = max(0, min(2, cursor_y + dy))

def blink_pattern(times, interval=200):
    for _ in range(times):
        clear_all()
        basic.pause(interval)
        draw(False)
        basic.pause(interval)

def reset_game():
    global field, player, cursor_x, cursor_y
    field = [[None for _ in range(3)] for _ in range(3)]
    player = True
    cursor_x = 0
    cursor_y = 0
    draw(True)

def game_loop():
    global player
    last_blink = input.running_time()
    blink_on = True
    draw(blink_on)

    while True:
        # Cursor blinkt alle ~400 ms
        if input.running_time() - last_blink > 400:
            blink_on = not blink_on
            draw(blink_on)
            last_blink = input.running_time()

        # Cursorsteuerung mit Pins P0–P3
        if input.pin_is_pressed(input.pin0):
            move_cursor(0, -1); draw(blink_on); basic.pause(200)
        if input.pin_is_pressed(input.pin1):
            move_cursor(0, 1); draw(blink_on); basic.pause(200)
        if input.pin_is_pressed(input.pin2):
            move_cursor(-1, 0); draw(blink_on); basic.pause(200)
        if input.pin_is_pressed(input.pin3):
            move_cursor(1, 0); draw(blink_on); basic.pause(200)

        # Button A = Spielzug setzen
        if input.button_is_pressed(Button.A) :
            if field[cursor_y][cursor_x] is None:
                field[cursor_y][cursor_x] = player
                draw(False)
                basic.pause(200)
                if check_win():
                    blink_pattern(6, 150)
                    return
                if check_draw():
                    blink_pattern(4, 100)
                    return
                player = not player
            basic.pause(200)

        # Button B = Spiel zurücksetzen
        if input.button_is_pressed(Button.B):
            reset_game()
            basic.pause(500)

# Spiel starten
reset_game()
game_loop()

