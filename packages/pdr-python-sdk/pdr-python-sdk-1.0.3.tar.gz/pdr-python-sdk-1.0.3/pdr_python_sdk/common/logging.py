import os
import logging


def config_logging(level=None, filename=None):
    if filename is None:
        log_dir = '../log'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        filename = '../log/phoenix_app.log'
        if not os.path.exists(filename):
            open(filename, 'w').close()

    if level is None:
        level = 'INFO'

    logging.basicConfig(filename=filename,
                        level=level,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s",
                        datefmt='%Y-%m-%d  %H:%M:%S %a')
