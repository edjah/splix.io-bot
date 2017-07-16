from body import SplixBot
from brain import game_update_to_vector
import argparse

parser = argparse.ArgumentParser(
    description='record a log of a game'
)
parser.add_argument('logfile',
    type=str,
    nargs='?',
    default='game.log'
)

if __name__ == '__main__':
    args = parser.parse_args()
    bot = SplixBot()
    bot.join(pause_at_start=False)
    i = 0
    with open(args.logfile, 'w') as f:
        while True:
            try:
                update = bot.get_game_update()
                if update.get('dead'):
                    bot.driver.quit()
                    break
                if update.get('players'):
                    my_dir = update['players'][0]['dir']
                    vec = game_update_to_vector(update)
                    print('{}: {}'.format(i, my_dir))
                    f.write('{},{}\n'.format(','.join(map(str, vec)), my_dir))
                i += 1
            except KeyboardInterrupt:
                bot.driver.quit()
