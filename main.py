import os
import sys
from datetime import datetime, timezone, timedelta

import pytz
from canvasapi import Canvas
from dateutil import parser

import creds

# datetime object with the current time in the current time zone
dt_now = datetime.now(timezone.utc)
tz_dt = dt_now.astimezone()

# Canvas object
canvas = Canvas(creds.api_url, creds.api_key)


# gets the pending assignments within a given number of hours
def pending_assignments(within_x_hours):
    x = int(within_x_hours)
    if x < 0:
        raise SystemExit('Cannot get pending assignments within a negative value for hours')
    pending_ass = canvas.get_todo_items()
    ass_list = []
    for assignment in pending_ass:
        if assignment.type != 'grading':
            ass_name = assignment.assignment['name']
            due_str = assignment.assignment['due_at']

            parsed = parser.parse(due_str).astimezone(pytz.timezone('US/Eastern'))
            ass_due_at = parsed.strftime("%b %d %Y %I:%M %p")
            delta = parsed - dt_now
            if delta <= timedelta(hours=x):
                ass_list.append(f'{ass_name} is due in {delta} @ {ass_due_at}')
    return ass_list


# formats the message
def msg_formatter(in_list, within_x_hours):
    output = ['Hello ' + creds.your_name + '-']
    if len(in_list) == 0:
        output.append(f'You have nothing due in the next {within_x_hours} hours!')
    else:
        output.append(f"Here's what's coming up for the next {within_x_hours} hours:")
        for x in in_list:
            output.append(x)
    return output


def main():
    # if given no command line arguments, set value to 36
    if len(sys.argv) <= 1:
        val = 36
    # else, set value to the command line argument
    else:
        val = sys.argv[1]
    # print all messages in the list, with a line seperator between each element
    print(*msg_formatter(pending_assignments(val), val), sep=os.linesep)


if __name__ == '__main__':
    main()
