""" Command line configuration parser """
import sys
import argparse

import dynamic_dynamodb


def parse(configuration):
    """ Parse command line options

    :type configuration: dict
    :param configuration: Dictionary with all options and defaults
    """
    parser = argparse.ArgumentParser(
        description='Dynamic DynamoDB - Auto provisioning AWS DynamoDB')
    parser.add_argument('-c', '--config',
        help='Read configuration from a configuration file')
    parser.add_argument('--dry-run',
        action='store_true',
        help='Run without making any changes to your DynamoDB table')
    parser.add_argument('--daemon',
        help='Run Dynamic DynamoDB as a daemon [start|stop|restart]')
    parser.add_argument('--check-interval',
        type=int,
        help="""How many seconds should we wait between
                the checks (default: 300)""")
    parser.add_argument('--log-file',
        help='Send output to the given log file')
    parser.add_argument('--version',
        action='store_true',
        help='Print current version number')
    parser.add_argument('--aws-access-key-id',
        help="Override Boto configuration with the following AWS access key")
    parser.add_argument('--aws-secret-access-key',
        help="Override Boto configuration with the following AWS secret key")
    dynamodb_ag = parser.add_argument_group('DynamoDB settings')
    dynamodb_ag.add_argument('-r', '--region',
        help='AWS region to operate in (default: us-east-1')
    dynamodb_ag.add_argument('-t', '--table-name',
        help='How many percent should we decrease the read units with?')
    r_scaling_ag = parser.add_argument_group('Read units scaling properties')
    r_scaling_ag.add_argument('--reads-upper-threshold',
        type=int,
        help="""Scale up the reads with --increase-reads-with percent if
                the currently consumed read units reaches this many
                percent (default: 90)""")
    r_scaling_ag.add_argument('--reads-lower-threshold',
        type=int,
        help="""Scale down the reads with --decrease-reads-with percent if the
                currently consumed read units is as low as this
                percentage (default: 30)""")
    r_scaling_ag.add_argument('--increase-reads-with',
        type=int,
        help="""How many percent should we increase the read
                units with? (default: 50, max: 100)""")
    r_scaling_ag.add_argument('--decrease-reads-with',
        type=int,
        help="""How many percent should we decrease the
                read units with? (default: 50)""")
    r_scaling_ag.add_argument('--min-provisioned-reads',
        type=int,
        help="""Minimum number of provisioned reads""")
    r_scaling_ag.add_argument('--max-provisioned-reads',
        type=int,
        help="""Maximum number of provisioned reads""")
    w_scaling_ag = parser.add_argument_group('Write units scaling properties')
    w_scaling_ag.add_argument('--writes-upper-threshold',
        type=int,
        help="""Scale up the writes with --increase-writes-with percent
                if the currently consumed write units reaches this
                many percent (default: 90)""")
    w_scaling_ag.add_argument('--writes-lower-threshold',
        type=int,
        help="""Scale down the writes with --decrease-writes-with percent
                if the currently consumed write units is as low as this
                percentage (default: 30)""")
    w_scaling_ag.add_argument('--increase-writes-with',
        type=int,
        help="""How many percent should we increase the write
                units with? (default: 50, max: 100)""")
    w_scaling_ag.add_argument('--decrease-writes-with',
        type=int,
        help="""How many percent should we decrease the write
                units with? (default: 50)""")
    w_scaling_ag.add_argument('--min-provisioned-writes',
        type=int,
        help="""Minimum number of provisioned writes""")
    w_scaling_ag.add_argument('--max-provisioned-writes',
        type=int,
        help="""Maximum number of provisioned writes""")
    args = parser.parse_args()

    # Print the version and quit
    if args.version:
        print 'Dynamic DynamoDB version: {0}'.format(dynamic_dynamodb.version())
        sys.exit(0)

    # Replace any new values in the configuration
    for arg in args.__dict__:
        print '{0}: {1}'.format(arg, args.__dict__.get(arg))
        if args.__dict__.get(arg) is not None:
            configuration[arg] = args.__dict__.get(arg)
