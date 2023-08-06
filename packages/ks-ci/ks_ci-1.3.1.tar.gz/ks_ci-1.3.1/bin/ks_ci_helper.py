#!/usr/bin/python3

import argparse
import ks_ci.discord
import ks_ci.junit

parser = argparse.ArgumentParser(description='Bundle of ci helpers')
subparsers = parser.add_subparsers(help='sub-command help')
parser_ut2discord = subparsers.add_parser('junit2discord', help='Help for junit2discord command')
parser_ut2discord.add_argument('--junit-report', type=str, required=True, dest='junit_report')
parser_ut2discord.add_argument('--junit-creator', type=str, required=True, dest='junit_creator')
parser_ut2discord.add_argument('--dsc-channel', type=str, required=True, dest='dsc_channel')
parser_ut2discord.add_argument('--bot-token', type=str, required=True, dest='bot_token')
parser_ut2discord.add_argument('--rev', type=str, required=True, dest='vcs_rev')
parser_ut2discord.add_argument('--desc', type=str, required=True, dest='desc')

args = parser.parse_args()

discordApi = ks_ci.discord.DiscordAPI(args.dsc_channel, args.bot_token)
junit_data = ks_ci.junit.JunitHandler.junitFactory(args.junit_creator)
junit_data.setJunitReport(args.junit_report)
junit_data.parseReport()
discordApi.send_message("{} {} (Revision: {}). {}".format(junit_data.getIcon(), args.desc, args.vcs_rev, junit_data.getCIMessage()))