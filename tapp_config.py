"""
Configuration helpers for TAPPs. Config file and record management are here,
as well as logging and redis.
Database configuration is done in sqlalchemy_models, since it has the content to test with.
"""
from os.path import expanduser

try:
    from ConfigParser import ConfigParser, NoOptionError
except ImportError:
    from configparser import ConfigParser, NoOptionError

import logging
import os
import redis

__all__ = ['get_config', 'setup_logging', 'setup_redis']


def get_config(name=__name__):
    """
    Get a configuration parser for a given TAPP name.
    Reads config.ini files only, not in-database configuration records.

    :param name: The tapp name to get a configuration for.
    :rtype: ConfigParser
    :return: A config parser matching the given name
    """
    cfg = ConfigParser()
    path = os.environ.get('%s_CONFIG_FILE' % name.upper(), '/etc/tapp/%s_cfg.ini' % name)
    cfg.read(path)
    return cfg


def setup_logging(name, cfg=None):
    """
    Create a logger, based on the given configuration.
    Accepts LOGFILE and LOGLEVEL settings.

    :param name: the name of the tapp to log
    :param cfg: The configuration object with logging info.
    :return: The session and the engine as a list (in that order)
    """
    logname = "%s_tapp.log" % name
    logfile = cfg.get('log', 'LOGFILE') if cfg is not None and \
        cfg.get('log', 'LOGFILE') is not None else 'server.log'
    loglevel = cfg.get('log', 'LOGLEVEL') if cfg is not None and \
        cfg.get('log', 'LOGLEVEL') is not None else logging.INFO
    logging.basicConfig(filename=logfile, level=loglevel)
    return logging.getLogger(name)


def setup_redis():
    """
    Setup redis for use in a TAPP. For now this is extremely dumb,
    and takes no configuration.

    :rtype: Strictredis
    :return: A redis connection to use.
    """
    red = redis.StrictRedis()
    return red
