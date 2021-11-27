import json
import random
import re
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

room = [
    ' ________________________________________________________________________________ ',
    '|                                                                                |',
    '|                                                                                |',
    '|                    xxxx.xx.xxxx.xxxxxx                                         |',
    '|                    xxx......xxx.xx...x                                         |',
    '|                    xx..xxxx........x.x                                         |',
    '|                    xx.xx...xxx.xxx.x.x                                         |',
    '|                    xx.xx.x.xxx.....x.x                                         |',
    '|                    xx.xx.....xxxxx...x                                         |',
    '|                    xx...xxxx.......xxx                                         |',
    '|                    xx.x.xx..3xxx....xx                                         |',
    '|                    x.......xxx...xx..x                                         |',
    '|                    x.x.xx......x.....x                                         |',
    '|                    x...x...xxx.xx.xxxxxxxxxx                                   |',
    '|                    x.xxx.x.xx..x.....xx.....xxxx                               |',
    '|                    x..xxxx....x....x..x.x.x.xxxxxxxxxxxxx                      |',
    '|                    xx......xxx..xx..x...x.x...xxxxxx.....xxxxxxxxxxxxxxx       |',
    '|                    x..x.xx.x4.....x..xx.x...x.....x..xxx.xx....xx...x...xx     |',
    '|                    xx...x....xxxx.xx..x.xxxx....x..x.....x..xx.x..x...x..xx    |',
    '|                    xxxxx..x.x...x.xxx.x......xx.xx.xx.x........x.x.......Cx    |',
    '|                    xx.......x.x.x.....xxxxx.xxx....xx....x....x....x..xx.xx    |',
    '|                    x..x.xx.xx.....xx.xxx.........xxxx.xx....x.x.x......x.xx    |',
    '|                    xx.......xx.xx.x..xx..xxx.xxx....x...Bx.xx.x........x.xx    |',
    '|                    x....x..xx..xx...xxx6.....xx...x..x.xxx.......xxxxx...xx    |',
    '|                    x.xxxx.xx.......xxxxx.xxx.....x.........xx..........x..x    |',
    '|                    xx.xxx.....xxxxxxxx...xxxx.xx...xxxxx.x.....xx...x.....x    |',
    '|   xxxxxxxxxxxxxxxxxxx.xxxxx.x.................x........x..x..x........xxxxx    |',
    '|  xxxxx..xx....xx............xxxxxx..xxx.xxxx.xx.xx...Axxx......x..xx......xx   |',
    '|   xxx1.....xx.xx.x.xx.x.xx...xx....xxxx.xx....x.xxx.xxxx..xx.x.......xxx...x   |',
    '|     xx...x.........x..x....x....xx..5.x....x.xx.................xxxxxx..xx.x   |',
    '|      xxx...xxx..x...x....x.xxx.xxxxxx.xxxxx..xxxx.xxxxxx.xx.xx......xxx.xx.xx  |',
    '|       xx.x.x....x.x..xxxx..xxx.....xx.xx....x.......xx........xxx.x........xx  |',
    '|        x...x....x.........xx...xxx.xx.....xxx7xx.xx.xx...x.xx...D.x..xxx....x  |',
    '|        xxxxx.xx.xxxx.xxxxxx..x.........xx..xx............x.....xxx...xx..xx.x  |',
    '|         xxxx.....xxx.xxxxxxx........xx........xx.xxxxxxx.xx.xx..x..x........x  |',
    '|           xxxx.......xxxxxxxxxxxx.x.xxxxxx.xx....xxxx....xxx.xx.x.......xExx   |',
    '|            xxxx...xxxxx      xxxx.x........xxxxx.xxx...xGxx......xxx.x..xxx    |',
    '|             xxx.x.xxxx         xx...x.x..x.xxx...xxx.x.x.xx.xx.....x...xxx     |',
    '|              xx..2xxxx          xxxx...x....xx8x.xxx.x...xx.....xx.xxxxx       |',
    '|                xxxxxxx           xxx.x.xxxx.xx...........xxx.xx...Fxxx         |',
    '|                   xx              xx...x....xxxxxxxxxxxx........xxxx           |',
    '|                                    xxxx..x.......xx......xxxxxxxxx             |',
    '|                                     xxxx...xx.xx.xxxx.xx.xxxxxxx               |',
    '|                                      xxxxx......x.........xxxx                 |',
    '|                                       xx...x...xx.xxx.....                     |',
    '|                                        x.9..............xx                     |',
    '|                                         xxxxxx.xx.xx.x.xx                      |',
    '|                                          xxxx........x.x                       |',
    '|                                           xxx.xx...xxx.x                       |',
    '|                                            xx....x.....x                       |',
    '|                                              xxxxx.xx.xx                       |',
    '|                                                xxx0...xx                       |',
    '|                                                  xxxx...                       |',
    '|                                                     xxxxxx                     |',
    '|                                                         xx                     |',
    '|                                                                                |',
    '|________________________________________________________________________________|',
]

room_outline = [
    ' ________________________________________________________________________________ ',
    '|                                                                                |',
    '|                        |  |    |                                               |',
    '|                    xxxx|xx|xxxx|xxxxxx                                         |',
    '|                    x   ↓  ↓    ↓     x                                         |',
    '|                    x                 x                                         |',
    '|                    x                 x                                         |',
    '|                    x                 x                                         |',
    '|                    x                 x                                         |',
    '|                    x                 x                                         |',
    '|                    x        ✘        x                                         |',
    '|                    x                 x                                         |',
    '|                    x                 x                                         |',
    '|                    x                  xxxxxx                                   |',
    '|                    x                        xxxx                               |',
    '|                    x                            xxxxxxxxx                      |',
    '|                    x                                     xxxxxxxxxxxxxxx       |',
    '|                    x        ✘                                           xx     |',
    '|                    x                                                      x    |',
    '|                    x                                                     ✘x    |',
    '|                    x                                                      x    |',
    '|                    x                                                      x    |',
    '|                    x                                    ✘                 x    |',
    '|                    x                   ✘                                  x    |',
    '|                    x                                                      x    |',
    '|                    x                                                      x    |',
    '|   xxxxxxxxxxxxxxxxx                                                       x    |',
    '|  x                                                   ✘                     x   |',
    '|   xx ✘                                                                     x   |',
    '|     x                               ✘                                      x   |',
    '|      x                                                                      x  |',
    '|       x                                                                     x  |',
    '|        x                                     ✘                  ✘           x  |',
    '|        x                                                                    x  |',
    '|         xx                                                                  x  |',
    '|           x            xxxxxx                                            ✘ x   |',
    '|            x          x      xx                         ✘                 x    |',
    '|             x        x         x                                        xx     |',
    '|              xx  ✘   x          x             ✘                       xx       |',
    '|                xxx  xx           x                                ✘ xx         |',
    '|                   xx              x                               xx           |',
    '|                                    x                            xx             |',
    '|                                     x                         xx               |',
    '|                                      x                    xxxx                 |',
    '|                                       x                  ←---                  |',
    '|                                        x ✘               x                     |',
    '|                                         x               x                      |',
    '|                                          x             x                       |',
    '|                                           x            x                       |',
    '|                                            xx          x                       |',
    '|                                              xx        x                       |',
    '|                                                xx ✘    x                       |',
    '|                                                  xxx    ←---                   |',
    '|                                                     xxxx x                     |',
    '|                                                         xx                     |',
    '|                                                                                |',
    '|________________________________________________________________________________|',
]

sam_i_am = {
    '1': {
        'name': 'El Paso',
        'pop': '679,813',
        'song_display': 'Marty Robbins - El Paso',
        'song_link': 'https://youtu.be/KAO7vs_Q9is',
        'start_end_row_col': [12, 14, 13, 25],
        'punch_char': '∏',
        'peoples': [
            ['mansos', 'Tampachoa (Mansos)'],
            ['mescalero-apache', 'Mescalero Apache'],
            ['tigua', 'Tigua (Tiwa)'],
            ['piro', 'Piro'],
            ['lipan-apache', 'Ndé Kónitsąąíí Gokíyaa (Lipan Apache)'],
            ['sumas', 'Sumas'],
            ['chiricahua-apache', 'Chiricahua Apache'],
        ],
    },
    '2': {
        'name': 'Terlingua',
        'pop': '110',
        'song_display': 'Shapes Have Fangs - Terlingua',
        'song_link': 'https://youtu.be/COIB5q792wk',
        'start_end_row_col': [15, 17, 27, 38],
        'punch_char': '∃',
        'peoples': [
            ['chiso', 'Chiso'],
            ['mescalero-apache', 'Mescalero Apache'],
            ['pescado', 'Pescado'],
            ['lipan-apache', 'Ndé Kónitsąąíí Gokíyaa (Lipan Apache)'],
            ['jumanos', 'Jumanos'],
        ],
    },
    '3': {
        'name': 'Amarillo',
        'pop': '198,955',
        'song_display': 'J Balvin - Amarillo',
        'song_link': 'https://youtu.be/KHAgoT4FZbc',
        'start_end_row_col': [5, 8, 13, 25],
        'punch_char': '∑',
        'peoples': [
            ['n%ca%89m%ca%89n%ca%89%ca%89-comanche', 'Nʉmʉnʉʉ (Comanche)'],
            ['kiowa', '[Gáuigú (Kiowa)'],
        ],
    },
    '4': {
        'name': 'Lubbock',
        'pop': '253,851',
        'song_display': 'Koe Wetzel - Lubbock',
        'song_link': 'https://youtu.be/X90m-jQ-ufY',
        'start_end_row_col': [5, 8, 40, 53],
        'punch_char': '♠',
        'peoples': [
            ['n%ca%89m%ca%89n%ca%89%ca%89-comanche', 'Nʉmʉnʉʉ (Comanche)'],
        ],
    },
    '5': {
        'name': 'San Angelo',
        'pop': '100,031',
        'song_display': 'Aerial East - San Angelo',
        'song_link': 'https://www.youtube.com/watch?v=cZVstDN-fAg',
        'start_end_row_col': [9, 11, 27, 38],
        'punch_char': '♣',
        'peoples': [
            ['n%ca%89m%ca%89n%ca%89%ca%89-comanche', 'Nʉmʉnʉʉ (Comanche)'],
            ['lipan-apache', 'Ndé Kónitsąąíí Gokíyaa (Lipan Apache)'],
            ['jumanos', 'Jumanos'],
            ['kiikaapoi-kickapoo', 'Kiikaapoi (Kickapoo)'],
        ],
    },
    '6': {
        'name': 'Abilene',
        'pop': '124,156',
        'song_display': 'Buck Owens - Abilene',
        'song_link': 'https://www.youtube.com/watch?v=r3CQ8pBSP1w',
        'start_end_row_col': [9, 11, 0, 11],
        'punch_char': '♥',
        'peoples': [
            ['n%ca%89m%ca%89n%ca%89%ca%89-comanche', 'Nʉmʉnʉʉ (Comanche)'],
            ['jumanos', 'Jumanos'],
            ['kiikaapoi-kickapoo', 'Kiikaapoi (Kickapoo)'],
        ],
    },
    '7': {
        'name': 'Luckenbach',
        'pop': '3',
        'song_display': 'Waylon Jennings - Luckenbach, Texas (Back to the Basics of Love)',
        'song_link': 'https://www.youtube.com/watch?v=Ti6QV90X-Sk',
        'start_end_row_col': [18, 20, 0, 53],
        'punch_char': '♦',
        'peoples': [
            ['n%ca%89m%ca%89n%ca%89%ca%89-comanche', 'Nʉmʉnʉʉ (Comanche)'],
            ['coahuiltecan', 'Coahuiltecan'],
            ['lipan-apache', 'Ndé Kónitsąąíí Gokíyaa (Lipan Apache)'],
            ['tonkawa-2', 'Tonkawa'],
            ['jumanos', 'Jumanos'],
            ['kiikaapoi-kickapoo', 'Kiikaapoi (Kickapoo)'],
        ],
    },
    '8': {
        'name': 'San Antonio',
        'pop': '1,508,000',
        'song_display': 'Bob Wills & His Texas Playboys - San Antonio Rose',
        'song_link': 'https://www.youtube.com/watch?v=e9H8uZEJtnA',
        'start_end_row_col': [12, 14, 40, 53],
        'punch_char': '*',
        'peoples': [
            ['coahuiltecan', 'Coahuiltecan'],
            ['lipan-apache', 'Ndé Kónitsąąíí Gokíyaa (Lipan Apache)'],
            ['tonkawa-2', 'Tonkawa'],
            ['jumanos', 'Jumanos'],
        ],
    },
    '9': {
        'name': 'Laredo',
        'pop': '259,151',
        'song_display': 'Band of Horses - Laredo',
        'song_link': 'https://www.youtube.com/watch?v=YH8QICzCO8g',
        'start_end_row_col': [15, 17, 13, 25],
        'punch_char': '~',
        'peoples': [
            ['coahuiltecan', 'Coahuiltecan'],
            ['lipan-apache', 'Ndé Kónitsąąíí Gokíyaa (Lipan Apache)'],
            ['alazapas', 'Alazapas'],
        ]
    },
    '0': {
        'name': 'Brownsville',
        'pop': '182,271',
        'song_display': 'Bob Dylan - Brownsville Girl',
        'song_link': 'https://youtu.be/9FaUx-Re8i0',
        'start_end_row_col': [9, 11, 13, 25],
        'punch_char': '╋',
        'extra_song_display': 'Furry Lewis - I\'m Going to Brownsville',
        'extra_song_link': 'https://www.youtube.com/watch?v=vvDGmcFTJAk',
        'peoples': [
            ['estokgna', 'Esto’k Gna (CarrizoComecrudo)'],
            ['coahuiltecan', 'Coahuiltecan'],
            ['lipan-apache', 'Ndé Kónitsąąíí Gokíyaa (Lipan Apache)'],
            ['rayados-borrados', 'Rayados (Borrados)'],
        ],
    },
    'A': {
        'name': 'Temple',
        'pop': '74,762',
        'song_display': 'Little Joe Y La Familia - Las Nubes',
        'song_link': 'https://www.youtube.com/watch?v=d-xu_UOJzPY',
        'start_end_row_col': [15, 17, 0, 11],
        'punch_char': '█',
        'peoples': [
            ['waco', 'Waco'],
            ['tonkawa-2', 'Tonkawa'],
            ['jumanos', 'Jumanos'],
        ],
    },
    'B': {
        'name': 'Dallas',
        'pop': '1,331,000',
        'song_display': 'Silver Jews - Dallas',
        'song_link': 'https://www.youtube.com/watch?v=U0IgWuSiFDk',
        'start_end_row_col': [9, 11, 40, 53],
        'punch_char': '◤',
        'peoples': [
            ['wichita', 'Wichita'],
            ['tawakoni', 'Tawakoni'],
            ['jumanos', 'Jumanos'],
            ['kiikaapoi-kickapoo', 'Kiikaapoi (Kickapoo)'],
        ],
    },
    'C': {
        'name': 'Texarkana',
        'pop': '36,688',
        'song_display': 'Bob Wills & His Texas Playboys - Texarkana Baby',
        'song_link': 'https://www.youtube.com/watch?v=JiiGU3hgB2Q',
        'start_end_row_col': [5, 8, 0, 11],
        'punch_char': '$',
        'peoples': [
            ['quapaw', 'O-ga-xpa Ma-zhoⁿ (O-ga-xpa)'],
            ['caddo', 'Caddo'],
            ['osage', '𐓏𐒰𐓓𐒰𐓓𐒷  𐒼𐓂𐓊𐒻  𐓆𐒻𐒿𐒷  𐓀𐒰^𐓓𐒰^(Osage)'],
        ],
    },
    'D': {
        'name': 'Huntsville',
        'pop': '41,592',
        'song_display': 'Merle Haggard – Huntsville',
        'song_link': 'https://www.youtube.com/watch?v=Svrlhq5gtuo',
        'start_end_row_col': [12, 14, 27, 38],
        'punch_char': '¥',
        'peoples': [
            ['bidai', 'Bidai'],
            ['koasati-coushatta', 'Koasati (Coushatta)'],
            ['tonkawa-2', 'Tonkawa'],
        ],
    },
    'E': {
        'name': 'Beaumont',
        'pop': '118,151',
        'song_display': 'Bob Wills & His Texas Playboys - Beaumont Rag',
        'song_link': 'https://www.youtube.com/watch?v=VoXWkbEXqXs',
        'start_end_row_col': [5, 8, 27, 38],
        'punch_char': '╳',
        'peoples': [
            ['atakapa-2', 'Atakapa-Ishak'],
            ['koasati-coushatta', 'Koasati (Coushatta)'],
            ['akokisa', 'Akokisa'],
        ],
    },
    'F': {
        'name': 'Galveston',
        'pop': '50,241',
        'song_display': 'Why Bonnie - Galveston',
        'song_link': 'https://www.youtube.com/watch?v=LOdS2IpU-1E',
        'start_end_row_col': [12, 14, 0, 11],
        'punch_char': 'Ƨ',
        'peoples': [
            ['karankawa-2', 'Karankawa'],
            ['estokgna/', 'Esto’k Gna (CarrizoComecrudo)'],
            ['atakapa-2', 'Atakapa-Ishak'],
            ['coahuiltecan', 'Coahuiltecan'],
            ['akokisa', 'Akokisa'],
        ],
    },
    'G': {
        'name': 'La Grange',
        'pop': '4,667',
        'song_display': 'ZZ Top - La Grange',
        'song_link': 'https://www.youtube.com/watch?v=rG6b8gjMEkw',
        'start_end_row_col': [15, 17, 40, 53],
        'punch_char': '¶',
        'peoples': [
            ['sanan', 'Sana'],
            ['coahuiltecan', 'Coahuiltecan'],
            ['tonkawa-2', 'Tonkawa'],
            ['jumanos', 'Jumanos'],
        ],
    }
}

punch_card_orig = [
    ' ____________________________________________________ ',
    '|                                                    |',
    "|                SINGIN' ACROSS TEXAS                |",
    '|     Find the 17 cities that have songs written     |',
    '|         about them in our four acre maze.          |',
    '|____________________________________________________|',
    '|           |             |            |             |',
    '| Texarkana |  Amarillo   |  Beaumont  |   Lubock    |',
    '|___________|_____________|____________|_____________|',
    '|           |             |            |             |',
    '|  Abilene  | Brownsville | San Angelo |   Dallas    |',
    '|___________|_____________|____________|_____________|',
    '|           |             |            |             |',
    '| Galveston |   El Paso   | Huntsville | San Antonio |',
    '|___________|_____________|____________|_____________|',
    '|           |             |            |             |',
    '|  Temple   |   Laredo    | Terlingua  |  La Grange  |',
    '|___________|_____________|____________|_____________|',
    '|                                                    |',
    '|                     Luckenbach                     |',
    '|____________________________________________________|',
    '                                                      ',
]

north_stars = [
    '               .                    ',
    '    .  .                  .         ',
    '                                    ',
    '                 ✦                  ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
]

east_stars = [
    '                                   .',
    '                                    ',
    '          .       .           .     ',
    '         .             .            ',
    '                    .               ',
    '                          .         ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
]

south_stars = [
    '.   . .   .   .  .          .       ',
    '              .         .       .   ',
    '               .        .           ',
    '                .          .        ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
]

west_stars = [
    '.   .              .        .     . ',
    '  . .                               ',
    '                     .            . ',
    '                   .    .           ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
    '                                    ',
]


def calc_punch_card_display(bg_farm_str, sr, er, sc, ec, punch_card, punch_it):
    pcd = print_screen(punch_card_orig)
    r = 20
    while r >= 0:
        c = 53
        while c >= 0:
            if punch_it and sr <= r <= er and sc <= c <= ec:
                pcd = pcd[:55 * r + c] + str.format(
                    '<a href="javascript:{{}}" onclick="document.the_form.punch_spot.value=\'{}-{}\';document.the_form.submit();return false;">',
                    r, c) + pcd[55 * r + c] + '</a>' + pcd[55 * r + c + 1:]
            else:
                for punch_card_mark in punch_card.values():
                    if r == int(punch_card_mark[0]) and c == int(punch_card_mark[1]):
                        pcd = pcd[:55 * r + c] + str.format('</code><code style="color: rgba({});">',
                                                            bg_farm_str) + punch_card_mark[2] + '</code><code>' + pcd[
                                                                                                                  55 * r + c + 1:]
            c -= 1
        r -= 1

    pcd = '<pre style="line-height: 1; background-color: rgba(242, 241, 239, 1); text-black;"><code>' + pcd + '</code></pre>'
    return pcd


@app.route('/ending', methods=['GET'])
def ending():
    cookie_state = request.cookies.get('state')
    if cookie_state is None or (request.method == 'POST' and 'reset' in request.form):
        steps = 0
    else:
        json_decoder = json.JSONDecoder()
        state = json_decoder.decode(cookie_state)

        steps = state['steps']
    bg_farm_str, fg_farm_str = get_colors(steps)
    return render_template('ending.html', bg_farm=bg_farm_str, fg_farm=fg_farm_str)


@app.route('/', methods=['GET', 'POST'])
def index():
    card_title2 = ''
    cookie_state = request.cookies.get('state')
    if cookie_state is None or (request.method == 'POST' and 'reset' in request.form):
        card_title2 = 'Y\'all have fun!'
        steps = 0
        cardinal = 2
        player_row = 1
        player_col = 25
        punch_card = {}
        won = False
        welcome_modal = True
    else:
        json_decoder = json.JSONDecoder()
        state = json_decoder.decode(cookie_state)

        steps = state['steps']
        cardinal = state['cardinal']
        player_row = state['player_row']
        player_col = state['player_col']
        punch_card = state['punch_card']
        won = state['won']
        welcome_modal = False

    if request.method == 'POST':
        if 'direction' in request.form:
            steps += 1
            direction = request.form['direction']

            card_title2, cardinal, player_row, player_col = move(cardinal, player_row, player_col, direction)

    if cardinal == 0:
        spun_row, spun_col, spun_room = player_row, player_col, room
    elif cardinal == 1:
        spun_row, spun_col, spun_room = spin_room(player_row, player_col, room, 'e')
    elif cardinal == 2:
        spun_row, spun_col, spun_room = spin_room(player_row, player_col, room, 'e')
        spun_row, spun_col, spun_room = spin_room(spun_row, spun_col, spun_room, 'e')
    else:
        spun_row, spun_col, spun_room = spin_room(player_row, player_col, room, 'q')

    card_title, screen = time_of_day(steps, cardinal, spun_row, spun_col, spun_room)
    wall_ahead(screen, spun_row, spun_col, spun_room)
    mark_treasure(screen, spun_row, spun_col, spun_room)
    side_walls(screen, spun_row, spun_col, spun_room)
    display = print_screen(screen)

    bg_farm_str, fg_farm_str = get_colors(steps)

    card_title += '<br>'
    card_title = location(card_title, player_col, player_row)
    card_title = cardinal_str(card_title, cardinal)

    punch_card, treasure, punch_card_display = check_for_treasure(player_col, player_row, punch_card, bg_farm_str,
                                                                  request)

    if not won and len(punch_card) == 17 and [player_row, player_col] in [
        [2, 25], [2, 28], [2, 33], [44, 60], [52, 58]
    ]:
        won = True

    show_exit_message = (not won) and len(punch_card) == 17

    room_str = debug_room(cardinal, player_col, player_row)

    resp = make_response(render_template('main.html', card_title=card_title, display=display, room=room_str,
                                         treasure=treasure, fg_farm=fg_farm_str, bg_farm=bg_farm_str,
                                         punch_card_display=punch_card_display, show_exit_message=show_exit_message,
                                         won=won, card_title2=card_title2, empty_room=print_screen(room_outline),
                                         welcome_modal=welcome_modal))

    state = {
        'steps': steps,
        'cardinal': cardinal,
        'player_row': player_row,
        'player_col': player_col,
        'punch_card': punch_card,
        'won': won
    }

    json_encoder = json.JSONEncoder()
    resp.set_cookie('state', json_encoder.encode(state))

    return resp


def check_for_treasure(player_col, player_row, punch_card, bg_farm_str, request):
    start_end_row_col = [-1, -1, -1, -1]
    punch_it = False

    marker = re.search('[0-9A-G]', room[player_row][player_col])
    if marker is not None:
        data = sam_i_am[marker[0]]
        start_end_row_col = data['start_end_row_col']

        if 'punch_spot' in request.form:
            if request.form['punch_spot'] != '':
                punch_card[marker[0]] = request.form['punch_spot'].split('-')
                punch_card[marker[0]].append(data['punch_char'])

        extra_song_display = ''
        extra_song_link = ''
        if 'extra_song_display' in data:
            extra_song_display = 'Furry Lewis - I\'m Going to Brownsville'
            extra_song_link = 'https://www.youtube.com/watch?v=vvDGmcFTJAk'

        punch_it = (marker[0] not in punch_card)
        treasure = render_template('treasure.html', name=data['name'], pop=data['pop'],
                                   song_display=data['song_display'], song_link=data['song_link'], punch_it=punch_it,
                                   extra_song_display=extra_song_display, extra_song_link=extra_song_link,
                                   peoples=data['peoples'])
    else:
        treasure = ''

    sr, er, sc, ec = start_end_row_col
    punch_card_display = calc_punch_card_display(bg_farm_str, sr, er, sc, ec, punch_card, punch_it)

    return punch_card, treasure, punch_card_display


def location(card_title, player_col, player_row):
    card_title += "You're "
    if player_row / (len(room) - 4) < .33:
        card_title += 'north'
    elif player_row / (len(room) - 4) >= .66:
        card_title += 'south'
    if player_col / (len(room[0]) - 4) < .33:
        card_title += 'west'
    elif player_col / (len(room[0]) - 4) >= .66:
        card_title += 'east'

    if (player_row / (len(room) - 4) >= .33) and (player_row / (len(room) - 4) < .66) and (
            player_col / (len(room[0]) - 4) >= .33) and (player_col / (len(room[0]) - 4) < .66):
        card_title += 'central'
    card_title += '<br>'
    return card_title


def cardinal_str(card_title, cardinal):
    if cardinal == 0:
        card_title += "lookin' north."
    elif cardinal == 1:
        card_title += "lookin' east."
    elif cardinal == 2:
        card_title += "lookin' south."
    else:
        card_title += "lookin' west."
    return card_title


def debug_room(cardinal, player_col, player_row):
    if cardinal == 0:
        player_char = '△'
    elif cardinal == 1:
        player_char = '▷'
    elif cardinal == 2:
        player_char = '▽'
    else:
        player_char = '◁'

    room_copy = [[]] * len(room)
    for r in range(len(room)):
        room_copy[r] = room[r]
    room_copy[player_row] = room[player_row][:player_col] + player_char + room[player_row][player_col + 1:]

    start_row = player_row - 1
    if start_row < 0:
        start_row = 0
    elif start_row > (len(room_copy) - 3):
        start_row = len(room_copy) - 3
    start_col = player_col - 3
    if start_col < 0:
        start_col = 0
    elif start_col > (len(room_copy[0]) - 7):
        start_col = len(room_copy[0]) - 7

    room_subset = []
    for r in range(3):
        line = room_copy[start_row + r][start_col:start_col + 7]
        line = re.sub('[0-9A-G]', '✘', str(line))
        room_subset.append(line.replace('.', ' ').replace('x', '#'))

    return print_screen(room_subset)


def time_of_day(steps, cardinal, player_row, player_col, room):
    distance = screen_height
    for i in range(player_row):
        if re.search('[_|. 0-9A-Z]', room[player_row - 1 - i][player_col]) is None:
            distance = 1 + i
            break

    if cardinal == 0:
        stars = north_stars
    elif cardinal == 1:
        stars = east_stars
    elif cardinal == 2:
        stars = south_stars
    else:
        stars = west_stars

    screen = screen_init()
    for r in range(len(stars)):
        if r > distance:
            break
        line = stars[r]
        chars = []
        for c in range(len(stars[0])):
            chars.append(line[c])
        screen[r] = chars

    if steps >= 800:
        card_title = 'It\'s evening.<br>'
    elif steps >= 320:
        card_title = 'It\'s dusk.<br>'
    else:
        screen = screen_init()
        card_title = 'It\'s afternoon.<br>'

    return card_title, screen


def get_colors(steps):
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
        fg_farm.append(str(int(fg_farm1[i]) + (int(fg_farm2[i]) - int(fg_farm1[i])) * (steps % 400) // 400))
        bg_farm.append(str(int(bg_farm1[i]) + (int(bg_farm2[i]) - int(bg_farm1[i])) * (steps % 400) // 400))
    fg_farm_str = ','.join(fg_farm)
    bg_farm_str = ','.join(bg_farm)
    return bg_farm_str, fg_farm_str


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

    if room[new_row][new_col] in ['_', '|']:
        return 'Nothing that a-way.', new_cardinal, current_row, current_col
    elif hit_wall(room[new_row][new_col]):
        return 'Naw.', new_cardinal, current_row, current_col
    return '', new_cardinal, new_row, new_col


def hit_wall(map_char):
    return re.search('[_|. 0-9A-Z]', map_char) is None


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
    distances = []
    for i in range(player_row):
        if hit_wall(room[player_row - i - 1][player_col]):
            break
        if re.search('[0-9A-Z]', room[player_row - i - 1][player_col]) is not None:
            distances.append(i + 1)

    for distance in distances:
        if distance >= screen_height // 2 + 1:
            return

        r = screen_height - distance
        screen[r][screen_len // 2 - 1] = '*'
        screen[r][screen_len // 2] = '*'
        if distance <= (screen_len // 8 - 3):
            screen[r][screen_len // 2 - 2] = '*'
            screen[r][screen_len // 2 + 1] = '*'


def side_walls(screen, player_row, player_col, room):
    left_wall = ''
    right_wall = ''

    for r in range(player_row + 1):
        if hit_wall(room[player_row - r][player_col - 1]):
            left_wall += room[player_row - r][player_col - 1]
        elif r == 0 and hit_wall(room[player_row - 1][player_col]):
            break
        else:
            left_wall += ' '
        if hit_wall(room[player_row - r - 1][player_col]):
            break

    for r in range(player_row + 1):
        if hit_wall(room[player_row - r][player_col + 1]):
            right_wall += room[player_row - r][player_col + 1]
        elif r == 0 and hit_wall(room[player_row - 1][player_col]):
            break
        else:
            right_wall += ' '
        if hit_wall(room[player_row - r - 1][player_col]):
            break

    if re.search('[^ ]', left_wall):
        for c in range(len(left_wall)):
            for r in range(len(screen) - (c * 2)):
                wall_char = left_wall[c]
                if wall_char == 'x':
                    wall_char = random.choice(['|', '/', '\\'])
                screen[r + c][(c * 2)] = wall_char
                screen[r + c][(c * 2) + 1] = wall_char

    if re.search('[^ ]', right_wall):
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
