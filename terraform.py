import re

class TerraformState(object):
    def __init__(self, state):
        self.state = state

    @property
    def droplet_names(self):
        return self.state['modules'][0]['resources'].iterkeys()

    @property
    def droplets(self):
        return [
            Droplet(self.state['modules'][0]['resources'][k])
                for k in self.droplet_names
        ]


class Droplet(object):
    def __init__(self, droplet_json):
        self.attributes = droplet_json['primary']['attributes']

    @property
    def name(self):
        return self.attributes['name']

    @property
    def public_ip(self):
        return self.attributes['ipv4_address']

    @property
    def private_ip(self):
        return self.attributes['ipv4_address_private']

    @property
    def group(self):
        return Translator(self).group


class Translator(object):
    def __init__(self, name):
        self.name = name
        self.pattern = re.compile("([a-zA-Z]+)([0-9]+)")

    @property
    def group(self):
        pieces = self.name.split('-')
        return self.pattern.match(pieces[1]).group(1)


class DropletGroups(object):
    def __init__(self, droplets):
        self.droplets = droplets

    @property
    def groups(self):
        return [
            Translator(d.name).group
                for d in self.droplets
        ]
