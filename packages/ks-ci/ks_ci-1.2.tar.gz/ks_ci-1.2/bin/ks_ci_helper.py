#!/usr/bin/python3

from junitparser import JUnitXml
import argparse
import ks_ci.discord

parser = argparse.ArgumentParser(description='Bundle of ci helpers')
subparsers = parser.add_subparsers(help='sub-command help')
parser_ut2discord = subparsers.add_parser('ut2discord', help='Help for ut2discord command')
parser_ut2discord.add_argument('--junit-report', type=str, required=True, dest='junit_report')
parser_ut2discord.add_argument('--dsc-channel', type=str, required=True, dest='dsc_channel')
parser_ut2discord.add_argument('--bot-token', type=str, required=True, dest='bot_token')
parser_ut2discord.add_argument('--rev', type=str, required=True, dest='vcs_rev')

args = parser.parse_args()

discordApi = ks_ci.discord.DiscordAPI(args.dsc_channel, args.bot_token)

xml = JUnitXml.fromfile(args.junit_report)
failures = 0
tests = 0
errors = 0
for suite in xml:
    failures = failures + suite.
    tests = tests + suite.tests
    errors = errors + suite.errors

icon = ":green_heart:"
if failures + errors > 0:
    icon = ":no_entry:"

discordApi.send_message("{} Revision: {}. Total tests: {}, failed: {}, errors: {}.".format(icon, args.vcs_rev, tests, failures, errors))
