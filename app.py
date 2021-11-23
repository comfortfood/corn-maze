import random
import re
from flask import Flask, render_template, request

app = Flask(__name__)

room = [
    '--------------------------------------------------------------------------------',
    '-                                                                              -',
    '-                   xxxx.xx.xxxx.xxxxxx                                        -',
    '-                   xxx......xxx.xx...x                                        -',
    '-                   xx..xxxx........x.x                                        -',
    '-                   xx.xx...xxx.xxx.x.x                                        -',
    '-                   xx.xx.x.xxx.....x.x                                        -',
    '-                   xx.xx.....xxxxx...x                                        -',
    '-                   xx...xxxx.......xxx                                        -',
    '-                   xx.x.xx..3xxx....xx                                        -',
    '-                   x.......xxx...xx..x                                        -',
    '-                   x.x.xx......x.....x                                        -',
    '-                   x...x...xxx.xx.xxxxxxxxxx                                  -',
    '-                   x.xxx.x.xx..x.....xx.....xxxx                              -',
    '-                   x..xxxx....x....x..x.x.x.xxxxxxxxxxxxx                     -',
    '-                   xx......xxx..xx..x...x.x...xxxxxx.....xxxxxxxxxxxxxxx      -',
    '-                   x..x.xx.x4.....x..xx.x...x.....x..xxx.xx....xx...x...xx    -',
    '-                   xx...x....xxxx.xx..x.xxxx....x..x.....x..xx.x..x...x..xx   -',
    '-                   xxxxx..x.x...x.xxx.x......xx.xx.xx.x........x.x.......Cx   -',
    '-                   xx.......x.x.x.....xxxxx.xxx....xx....x....x....x..xx.xx   -',
    '-                   x..x.xx.xx.....xx.xxx.........xxxx.xx....x.x.x......x.xx   -',
    '-                   xx.......xx.xx.x..xx..xxx.xxx....x...Bx.xx.x........x.xx   -',
    '-                   x....x..xx..xx...xxx6.....xx...x..x.xxx.......xxxxx...xx   -',
    '-                   x.xxxx.xx.......xxxxx.xxx.....x.........xx..........x..x   -',
    '-                   xx.xxx.....xxxxxxxx...xxxx.xx...xxxxx.x.....xx...x.....x   -',
    '-  xxxxxxxxxxxxxxxxxxx.xxxxx.x.................x........x..x..x........xxxxx   -',
    '- xxxxx..xx....xx............xxxxxx..xxx.xxxx.xx.xx...Axxx......x..xx......xx  -',
    '-  xxx1.....xx.xx.x.xx.x.xx...xx....xxxx.xx....x.xxx.xxxx..xx.x.......xxx...x  -',
    '-    xx...x.........x..x....x....xx..5.x....x.xx.................xxxxxx..xx.x  -',
    '-     xxx...xxx..x...x....x.xxx.xxxxxx.xxxxx..xxxx.xxxxxx.xx.xx......xxx.xx.xx -',
    '-      xx.x.x....x.x..xxxx..xxx.....xx.xx....x.......xx........xxx.x........xx -',
    '-       x...x....x.........xx...xxx.xx.....xxx7xx.xx.xx...x.xx...D.x..xxx....x -',
    '-       xxxxx.xx.xxxx.xxxxxx..x.........xx..xx............x.....xxx...xx..xx.x -',
    '-        xxxx.....xxx.xxxxxxx........xx........xx.xxxxxxx.xx.xx..x..x........x -',
    '-          xxxx.......xxxxxxxxxxxx.x.xxxxxx.xx....xxxx....xxx.xx.x.......xExx  -',
    '-           xxxx...xxxxx      xxxx.x........xxxxx.xxx...xGxx......xxx.x..xxx   -',
    '-            xxx.x.xxxx         xx...x.x..x.xxx...xxx.x.x.xx.xx.....x...xxx    -',
    '-             xx..2xxxx          xxxx...x....xx8x.xxx.x...xx.....xx.xxxxx      -',
    '-               xxxxxxx           xxx.x.xxxx.xx...........xxx.xx...Fxxx        -',
    '-                  xx              xx...x....xxxxxxxxxxxx........xxxx          -',
    '-                                   xxxx..x.......xx......xxxxxxxxx            -',
    '-                                    xxxx...xx.xx.xxxx.xx.xxxxxxx              -',
    '-                                     xxxxx......x.........xxxx                -',
    '-                                      xx...x...xx.xxx.....                    -',
    '-                                       x.9..............xx                    -',
    '-                                        xxxxxx.xx.xx.x.xx                     -',
    '-                                         xxxx........x.x                      -',
    '-                                          xxx.xx...xxx.x                      -',
    '-                                           xx....x.....x                      -',
    '-                                             xxxxx.xx.xx                      -',
    '-                                               xxx0...xx                      -',
    '-                                                 xxxx...                      -',
    '-                                                    xxxxxx                    -',
    '-                                                        xx                    -',
    '-                                                                              -',
    '--------------------------------------------------------------------------------',
]


@app.route('/', methods=['GET', 'POST'])
def index():
    card_title = 'Y\'all have a good time!<br>'
    cardinal = 2
    player_row = 2
    player_col = 24
    steps = 0

    if request.method == 'POST':
        steps = int(request.form['steps']) + 1
        direction = request.form['direction']
        cardinal = int(request.form['cardinal'])
        player_row = int(request.form['player_row'])
        player_col = int(request.form['player_col'])

        card_title, cardinal, player_row, player_col = move(cardinal, player_row, player_col, direction)

    if cardinal == 0:
        spun_row, spun_col, spun_room = player_row, player_col, room
        player_char = '△'
    elif cardinal == 1:
        spun_row, spun_col, spun_room = spin_room(player_row, player_col, room, 'e')
        player_char = '▷'
    elif cardinal == 2:
        spun_row, spun_col, spun_room = spin_room(player_row, player_col, room, 'e')
        spun_row, spun_col, spun_room = spin_room(spun_row, spun_col, spun_room, 'e')
        player_char = '▽'
    else:
        spun_row, spun_col, spun_room = spin_room(player_row, player_col, room, 'q')
        player_char = '◁'

    screen = screen_init()
    wall_ahead(screen, spun_row, spun_col, spun_room)
    mark_treasure(screen, spun_row, spun_col, spun_room)
    side_walls(screen, spun_row, spun_col, spun_room)
    display = print_screen(screen)

    roomCopy = [[]] * len(room)
    for r in range(len(room)):
        roomCopy[r] = room[r]
    roomCopy[player_row] = room[player_row][:player_col] + player_char + room[player_row][player_col + 1:]
    roomStr = print_screen(roomCopy)

    if steps >= 800:
        card_title += '<br>Evening.<br>'
    elif steps >= 320:
        card_title += '<br>Dusk.<br>'
    else:
        card_title += '<br>Afternoon.<br>'

    if steps >= 800:
        fg_farm1 = ['108', '122', '137', '1']
        bg_farm1 = ['8', '14', '44', '1']
        fg_farm2 = ['108', '122', '137', '1']
        bg_farm2 = ['8', '14', '44', '1']
    elif steps >= 400:
        fg_farm1 = ['253', '227', '167', '1']
        bg_farm1 = ['231', '109', '137', '1']
        fg_farm2 = ['108', '122', '137', '1']
        bg_farm2 = ['8', '14', '44', '1']
    else:
        fg_farm1 = ['245', '230', '83', '1']
        bg_farm1 = ['3', '138', '255', '1']
        fg_farm2 = ['253', '227', '167', '1']
        bg_farm2 = ['231', '109', '137', '1']

    fg_farm = []
    bg_farm = []
    for i in range(4):
        fg_farm.append(str(int(fg_farm1[i]) + (int(fg_farm2[i]) - int(fg_farm1[i])) * (steps % 400) / 400))
        bg_farm.append(str(int(bg_farm1[i]) + (int(bg_farm2[i]) - int(bg_farm1[i])) * (steps % 400) / 400))

    fg_farm_str = ','.join(fg_farm)
    bg_farm_str = ','.join(bg_farm)

    if player_row / (len(room) - 4) < .33:
        card_title += 'North'
    elif player_row / (len(room) - 4) >= .66:
        card_title += 'South'

    if player_col / (len(room[0]) - 4) < .33:
        card_title += ' West'
    elif player_col / (len(room[0]) - 4) >= .66:
        card_title += ' East'

    if (player_row / (len(room) - 4) >= .33) and (player_row / (len(room) - 4) < .66) and (
            player_col / (len(room[0]) - 4) >= .33) and (player_col / (len(room[0]) - 4) < .66):
        card_title += 'Central'

    card_title += '.<br>'

    if cardinal == 0:
        card_title += "Headed North."
    elif cardinal == 1:
        card_title += "Headed East."
    elif cardinal == 2:
        card_title += "Headed South."
    else:
        card_title += "Headed West."

    if re.search('[0-9A-Z]', room[player_row][player_col]) is not None:
        treasure = render_template('treasure.html')
    else:
        treasure = ''

    return render_template('index.html', card_title=card_title, display=display, cardinal=cardinal,
                           player_row=player_row, player_col=player_col, room=roomStr, treasure=treasure,
                           fg_farm=fg_farm_str, bg_farm=bg_farm_str, steps=steps)


def move(current_cardinal, current_row, current_col, direction):
    new_cardinal = current_cardinal
    new_row = current_row
    new_col = current_col

    if current_cardinal == 1:
        if direction == 'w':
            direction = 'd'
        elif direction == 'a':
            direction = 'w'
        elif direction == 's':
            direction = 'a'
        elif direction == 'd':
            direction = 's'
    elif current_cardinal == 2:
        if direction == 'w':
            direction = 's'
        elif direction == 'a':
            direction = 'd'
        elif direction == 's':
            direction = 'w'
        elif direction == 'd':
            direction = 'a'
    elif current_cardinal == 3:
        if direction == 'w':
            direction = 'a'
        elif direction == 'a':
            direction = 's'
        elif direction == 's':
            direction = 'd'
        elif direction == 'd':
            direction = 'w'

    if direction == 'q':
        if current_cardinal == 0:
            new_cardinal = 3
        else:
            new_cardinal -= 1
    if direction == 'e':
        if current_cardinal == 3:
            new_cardinal = 0
        else:
            new_cardinal += 1
    elif direction == 'w':
        new_row -= 1
    elif direction == 'a':
        new_col -= 1
    elif direction == 's':
        new_row += 1
    elif direction == 'd':
        new_col += 1

    if hit_wall(room[new_row][new_col]):
        return 'Corn.<br>', new_cardinal, current_row, current_col

    return '', new_cardinal, new_row, new_col


def hit_wall(map_char):
    return re.search('[. 0-9A-Z]', map_char) is None


def spin_room(current_row, current_col, current_room, direction):
    new_row = current_row
    new_col = current_col
    new_room = []
    for c in range(len(current_room[0])):
        row = []
        new_room.append(row)
        for r in range(len(current_room)):
            if direction == 'q':
                row.append(current_room[len(current_room) - 1 - r][c])
            elif direction == 'e':
                row.append(current_room[r][len(current_room[0]) - 1 - c])

    if direction == 'e':
        new_row = len(current_room[0]) - 1 - current_col
        new_col = current_row
    elif direction == 'q':
        new_row = current_col
        new_col = len(current_room) - 1 - current_row

    return new_row, new_col, new_room


screen_height = 10
screen_len = 36

brick_len = 4
gap_len = 2
brick_height = 1
brick_offset = (brick_len + gap_len) // 2
pattern = ''
for i in range(brick_len):
    pattern += 'x'
for i in range(gap_len):
    pattern += ' '


def screen_init():
    screen = []
    for r in range(screen_height):
        row = []
        screen.append(row)
        for c in range(screen_len):
            row.append(' ')
    return screen


def wall_ahead(screen, player_row, player_col, room):
    distance = 0
    wall_goes_left = False
    wall_goes_right = False
    for i in range(player_row):
        if hit_wall(room[player_row - 1 - i][player_col]):
            distance = 1 + i
            wall_goes_left = hit_wall(room[player_row - distance][player_col - 1]) or hit_wall(
                room[player_row - i][player_col - 1])
            wall_goes_right = hit_wall(room[player_row - distance][player_col + 1]) or hit_wall(
                room[player_row - i][player_col + 1])
            break

    if distance == 0:
        return

    max_center_wall_len = len(screen[0]) - (distance - 1) * 4

    if distance == screen_height // 2:
        for c in range(max_center_wall_len):
            if (c < 7 or c > max_center_wall_len - 12) and not wall_goes_left and not wall_goes_right:
                continue
            if c < 2 and not wall_goes_left:
                continue
            if c > max_center_wall_len - 3 and not wall_goes_right:
                continue
            screen[distance - 1][c + distance * 2] = random.choice(['|', '/', '\\'])
        return

    for r in range(screen_height):
        if r < distance or r >= screen_height - distance:
            continue
        for c in range(max_center_wall_len):
            if (c < 11 or c > max_center_wall_len - 12) and not wall_goes_left and not wall_goes_right:
                continue
            if c < 2 and not wall_goes_left:
                continue
            if c > max_center_wall_len - 3 and not wall_goes_right:
                continue
            if r == distance and random.randint(1, 10) > 5:
                continue
            screen[r][c + (distance - 1) * 2] = random.choice(['|', '/', '\\'])


def mark_treasure(screen, player_row, player_col, room):
    distance = 0
    for i in range(player_row + 1):
        if hit_wall(room[player_row - i][player_col]):
            return
        if re.search('[0-9A-Z]', room[player_row - i][player_col]) is not None:
            distance = i
            break

    if distance >= screen_height // 2:
        return

    r = screen_height - distance - 1
    screen[r][screen_len // 2 - 1] = '*'
    screen[r][screen_len // 2] = '*'


def side_walls(screen, player_row, player_col, room):
    left_wall = ''
    right_wall = ''

    for r in range(player_row + 1):
        if hit_wall(room[player_row - r][player_col - 1]):
            left_wall += room[player_row - r][player_col - 1]
        else:
            left_wall += ' '
        if hit_wall(room[player_row - r - 1][player_col]):
            break

    for r in range(player_row + 1):
        if hit_wall(room[player_row - r][player_col + 1]):
            right_wall += room[player_row - r][player_col + 1]
        else:
            right_wall += ' '
        if hit_wall(room[player_row - r - 1][player_col]):
            break

    for c in range(len(left_wall)):
        for r in range(len(screen) - (c * 2)):
            wall_char = left_wall[c]
            if wall_char == 'x':
                wall_char = random.choice(['|', '/', '\\'])
            screen[r + c][(c * 2)] = wall_char
            screen[r + c][(c * 2) + 1] = wall_char

    for c in range(len(right_wall)):
        for r in range(len(screen) - (c * 2)):
            wall_char = right_wall[c]
            if wall_char == 'x':
                wall_char = random.choice(['|', '/', '\\'])
            screen[r + c][len(screen[0]) - 1 - (c * 2)] = wall_char
            screen[r + c][len(screen[0]) - 1 - (c * 2) - 1] = wall_char


def print_screen(screen):
    display = ''
    for r in range(len(screen)):
        for c in range(len(screen[r])):
            display += screen[r][c]
        display += '\n'
    return display


if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
