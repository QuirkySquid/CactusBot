# CactusBot!

from user import User
from json import load


class Cactus(User):
    def __init__(self, autorestart=True, **kwargs):
        super(Cactus, self).__init__(**kwargs)
        self.debug = kwargs.get('debug', False)
        self.autorestart = autorestart

    def load_config(self, filename):
        """Load configuration."""
        with open(filename) as config:
            self.config = load(config)
            self.channel_data = self.login(**self.config)
            self.username = self.channel_data['username']

            self.connect_to_channel(self.username)

    def run(self, config_file="config.json"):
        """Run bot."""
        try:
            self.load_config(filename=config_file)
            self.logger.info("Authenticated as: {}.".format(self.username))
        except KeyboardInterrupt:
            self.logger.info("Removing thorns... done.")
            self.logger.info("CactusBot deactivated.")
        except Exception:
            self.logger.critical("Oh no, I crashed!")
            if self.autorestart:
                self.logger.info("Restarting...")
                self.run(config_file=config_file)

cactus = Cactus(debug=True, autorestart=False)
cactus.run()
