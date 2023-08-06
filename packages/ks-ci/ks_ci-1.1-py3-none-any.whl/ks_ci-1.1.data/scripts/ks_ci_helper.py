#!python

from junitparser import JUnitXml
import argparse
import ks_ci.discord

parser = argparse.ArgumentParser(description='Bundle of ci helpers')
subparsers = parser.add_subparsers(help='sub-command help')
parser_ut2discord = subparsers.add_parser('ut2discord', help='Help for ut2discord command')
parser_ut2discord.add_argument('--junit-report', type=str, required=True, dest='junit_report')
parser_ut2discord.add_argument('--dsc-channel', type=str, required=True, dest='dsc_channel')
parser_ut2discord.add_argument('--bot-token', type=str, required=True, dest='bot_token')

args = parser.parse_args()

discordApi = ks_ci.discord.DiscordAPI(args.dsc_channel, args.bot_token)

xml = JUnitXml.fromfile(args.junit_report)
failures = 0
for suite in xml:
    failures = failures + suite.failures

discordApi.send_message("Number of failed test cases: {}".format(failures))
