import redgrease
import configargparse
import re
from pathlib import Path


args = configargparse.ArgParser(
    description="Scans one or more directories for Redis Gears scripts, and "
    "executes them in a Redis Gears instance or cluster. "
    "Can optionally run continiously, montoring and re-loading scripts "
    "whenever changes are detected.",
    default_config_files=['./*.conf', '/etc/redgrease/conf.d/*.conf']
)

args.add_argument(
    'directories',
    nargs='+',
    type=Path,
    help="One or more directories containing Redis Gears scripts to watch",
    )

args.add_argument(
    '-c',
    '--config',
    env_var='CONFIG_FILE',
    metavar="PATH",
    is_config_file=True,
    help="Config file path",
)
args.add_argument(
    '--index-prefix',
    env_var='INDEX_PREFIX',
    metavar="PREFIX",
    required=False,
    type=str,
    default="/redgrease/scripts",
    help="Redis key prefix added to the index of monitored/executed script "
    "files.",
    )
args.add_argument(
    '-r',
    '--recursive',
    env_var='RECURSIVE',
    action='store_true',
    help="Recursively watch subdirectories.",
)
args.add_argument(
    '--script-pattern',
    env_var='SCRIPT_PATTERN',
    metavar="PATTERN",
    required=False,
    type=str,
    default="*.py",
    help="File name pattern (glob-style) that must be matched for scripts to "
    "be loaded.",
)
args.add_argument(
    '--requirements-pattern',
    env_var="REQUIREMENTS_PATTERN",
    metavar="PATTERN",
    required=False,
    type=str,
    default="*requirements*.txt",
    help="File name pattern (glob-style) that must be matched for requirement "
    "files to be loaded.",
)
args.add_argument(
    "--unblocking-pattern",
    env_var="UNBLOCKING_PATTERT",
    metavar="PATTERN",
    required=False,
    type=re.compile,
    default="unblock",
    help="Scripts with file paths that match this regular expression, "
    "will be executed with the 'UNBLOCKING' modifier, i.e. async execution."
)
args.add_argument(
    '-i',
    '--ignore',
    env_var="IGNORE",
    metavar='PATTERN',
    action='append',
    required=False,
    help="Ignore files matching this pattern.",
)
args.add_argument(
    '-w',
    '--watch',
    env_var='WATCH',
    metavar="SECONDS",
    nargs='?',
    type=float,
    default=0.0,
    const=5.0,
    help="If set, the directories will be continously montiored for updates/"
    "modifications to scripts and requirement files, and automatically loaded/"
    "rerun. The flag takes an optional value specifying the  duration, "
    "in seconds, to wait for further updates/modifications to files, before "
    "executing. "
    "This 'hysteresis' period is to prevent malformed scripts to be "
    "unnecessarily loaded during coding. "
    "If no value is supplied, the duration is defaulting to 5 seconds."
)
args.add_argument(
    '-s',
    '--server',
    env_var="SERVER",
    type=str,
    const='redis',
    default='localhost',
    nargs='?',
    help="Redis Gears host server IP or hostname."
)
args.add_argument(
    '-p',
    '--port',
    env_var='PORT',
    type=int,
    default=6379,
    help="Redis Gears host port number"
)
args.add_argument(
    '-log-name',
    env_var='LOG_NAME',
    metavar="NAME",
    type=str,
    help="Log name. Default: '__main__'"
)
args.add_argument(
    '--log-file',
    env_var='LOG_FILE',
    metavar="PATH",
    type=str,
    help="Log to this file name."
)
args.add_argument(
    '--log-no-stdout',
    env_var="LOG_NO_STDOUT",
    dest='log_to_stdout',  # Note: arg is negative, but var is positive
    action='store_false',
    help="Do not log to stdout, if set"
)
args.add_argument(
    '--log-level',
    env_var='LOG_LEVEL',
    metavar="LEVEL",
    choices=['CRITICAL', 'ERROR', 'WARNINING', 'INFO', 'DEBUG', 'NOTSET'],
    default='DEBUG',
    help="Logging level",
)

config = args.parse_args()


def main():
    print(config)
