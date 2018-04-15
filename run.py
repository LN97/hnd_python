import sys
import config

from quiz import create_app

def main():
    create_app(config, env={}).run(host=config.HOST, port=config.PORT, debug=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
