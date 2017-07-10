import numpy as np

class Stalker:
    def __init__(self, target_name):
        self.target_name = target_name

    def update(self, players):
        target = next((p for p in players if p['name'] == self.target_name), None)
        if target:
            return target['dir']
        else:
            return None

def game_stats_to_vector(stats):
    players = stats["players"]

    players = players[:10]

    vector = np.zeros()
    vector[0] = stats["myPlayerSkinBlock"]
    i = 1
    for player in players:
        vector[i] = int(player["deathWasCertain"])
        vector[i + 1] = player["dir"]
        vector[i + 2] = int(player["isMyPlayer"])
        vector[i + 3] = player["pos"][0]
        vector[i + 4] = player["pos"][1]
        i += 5

        trails = player["trails"][0]["trail"]
        trails = trails[:10]
        for j in range(len(trails)):
            vector[i + 2 * j] = trails[j][0]
            vector[i + 2 * j + 1] = trails[j][1]
        i += 20

    blocks = stats["blocks"]
    x, y = stats["myPlayerPos"]

    d = {}

    for block in blocks:
        cur = block["currentBlock"]
        if cur >= 15:
            cur -= 15
        elif 2 <= cur < 15:
            cur -= 2

        d[(block["x"], block["y"])] = cur

    x_lower = x - 20
    x_upper = x + 20
    y_lower = y - 20
    y_upper = y + 20

    for k in range(x_lower, x_upper + 1):
        for l in range(y_lower, y_upper + 1):
            if (k, l) in d:
                vector[i] = d[(k, l)]
            else:
                vector[i] = -1

            i += 1


"""
myPlayerSkinBlock

10 players
each player
* deathwascertain
* dir
* ismyplayer
* pos
* 10 trails

10 trails
each trail
* 2 coordinates

each pos
* 2 coordinates

1600 blocks
each block
* currentBlock

1 + 10 * (1 + 1 + 1 + 2 + 10 * 2) + 1681 * 1
1 + 10 * 25 + 1681
1932
