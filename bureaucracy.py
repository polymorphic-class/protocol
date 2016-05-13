from collections import defaultdict

class InventoryGrouping(object):
    def __init__(self, groups, droplets):
        self.groups = groups
        self.droplets = droplets

    def generate(self):
        groups = defaultdict(list)

        for g in self.groups:
            groups[g]

        for d in self.droplets:
            groups[d.group].append(d.name)

        return groups
