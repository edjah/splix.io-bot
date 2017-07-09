class Stalker:
    def __init__(self, target_name):
        self.target_name = target_name

    def update(self, players):
        target = next((p for p in players if p['name'] == self.target_name), None)
        if target:
            return target['dir']
        else:
            return None
