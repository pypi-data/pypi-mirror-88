import fire
import toml

class Cli:
    @staticmethod
    def run(config=None):
        from mdblog.config import CONFIG

        print(config)
        if config:
            CONFIG.update(**toml.load(config))
        print(CONFIG)
        import mdblog
        # from mdblog.config import CONFIG
        # print(CONFIG)
        mdblog.start_server()
def main():
    fire.Fire(Cli)
    # Cli.run()
if __name__ == '__main__':
    main()
