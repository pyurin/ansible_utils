#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime, sys, json, requests
from telebot import formatting as tgf
from telegram_config import *

MAX_LINES_TO_PROCESS = 2

def format_telegram_message(text):
    msg_data = {}
    msg_data['chat_id'] = TELEGRAM_CHAT_ID
    msg_data['text'] = text
    msg_data['parse_mode'] = 'HTML'

    logit(f'MSG: {msg_data}')

    return json.dumps(msg_data)

def format_alert(alert_json):
    # Get alert information
    title = alert_json['rule']['description'] if 'description' in alert_json['rule'] else ''
    description = alert_json['full_log'] if 'full_log' in alert_json else ''
    description.replace("\\n", "\n")
    alert_level = alert_json['rule']['level'] if 'level' in alert_json['rule'] else ''
    groups = ', '.join(alert_json['rule']['groups']) if 'groups' in alert_json['rule'] else ''
    rule_id = alert_json['rule']['id'] if 'rule' in alert_json else ''
    agent_name = alert_json['agent']['name'] if 'name' in alert_json['agent'] else ''
    agent_id = alert_json['agent']['id'] if 'id' in alert_json['agent'] else ''


    # Format message with markdown
    nl = "\n"
    return f"""
<b>{title}</b>
{f"<b>Groups:</b> {tgf.escape_html(groups)}" if len(groups) > 0 else ''}
{f'<b>Rule:</b> {tgf.escape_html(str(rule_id))} (Level {tgf.escape_html(str(alert_level))})'}
{f'<b>Agent:</b> {tgf.escape_html(agent_name)} ({tgf.escape_html(agent_id)})' if len(agent_name) > 0 else ''}
<i>{tgf.escape_html(description)}</i>
    """


def logit(s):
    with open('/var/ossec/logs/integrations.log', 'a') as f:
        f.write(f"{datetime.datetime.now()} {s}\n")

def send_telegram_message(text):
    msg_data = format_telegram_message(text)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    hook_url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
    response = requests.post(hook_url, headers=headers, data=msg_data)

    # Debug information
    logit(f'RESPONSE: {response.status_code} {response.text}')


def process_log_line(data):
    send_telegram_message(format_alert(data))

def read_logs():
    alert_file = open(sys.argv[1])
    line = alert_file.read()
    process_log_line(json.loads(line))
    alert_file.close()

logit(f"Executed with args: {sys.argv[1:]}")
read_logs()
logit("Processing finished")
sys.exit(0)