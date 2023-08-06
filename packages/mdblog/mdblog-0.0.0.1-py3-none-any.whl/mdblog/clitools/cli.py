import fire
import toml
from mdblog.config import CONFIG
class Cli:
    @staticmethod
    def run(config=None):
        if config:
            CONFIG.update(**toml.load(config))
        from mdblog import start_server
        start_server()
def main():
    fire.Fire(Cli)

if __name__ == '__main__':
    main()
