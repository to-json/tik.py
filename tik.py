#!/usr/bin/env python3
from jira import JIRA
from jira import JIRAError
import browser_cookie3
import argparse
import os
import sys
import configparser
from IPython import embed

# i'd rather these not be wierd globals but, then we'd have to pass jira
# to everything. could do something with an object and initializer, but, no.

config = configparser.ConfigParser()
conf_path = os.path.dirname(__file__) + '/tik.ini'
config.read(conf_path)
fields = config.items('fields')
browser = config.get('other', 'browser')
jira_url = config.get('other', 'jira_url')

cookies = getattr(browser_cookie3, browser)()
jira = JIRA({'cookies': cookies, 
                'server': jira_url})

# Buncha named functions because then i can read the dispatch code
# Most of these did not need functions, but, idgaf

def add_comment(ticket, comment):
    jira.add_comment(ticket, comment)

def display_comments(ticket):
    print("Comments:")
    for i, comment in enumerate(jira.comments(ticket)):
        print(comment.author.displayName + ": " + comment.body)

def transition(ticket, state):
    jira.transition_issue(ticket, state)

# This function is a mess
def interactive_transition(ticket):
    transitions = [(i, t['id'], t['name']) for i, t in enumerate(jira.transitions(ticket))]
    for t in transitions:
        print(str(t[0]) + ": " + str(t[2]))

    target = None
    while not (target and target.isdigit()):
        target = input("? ")

    try:
        transition(ticket, transitions[int(target)][1])
    except JIRAError as e:
        print(e.text)
        print("Unable to transition to that state, open ticket in a browser(y/n)?")
        answer = None
        while not (answer and (answer == 'y' or answer == 'n')):
            answer = input("? ")
        if answer == 'y':
            open_ticket(ticket)
        else:
            exit()

# This shit...
# So jira has these fields whose names are not attached to them, and instead
# they are called customfield_<integer>, and not all of them apply to every
# ticket. This function does awfulness iterating over a list of fields from 
# the config to print the fields if they exist. It's a seperate function for 
# my repl-testing convenience

def display_extended_fields(ticket, fields):
    for field in fields:
        field_accessor = "customfield_" + field[1]
        if hasattr(ticket.fields, field_accessor):
            print("{0}: {1}".format(field[0], 
                                    getattr(ticket.fields, field_accessor)))

def assignee(ticket):
    if ticket.fields.assignee:
        return ticket.fields.assignee.displayName
    else:
        return 'None'

def display_ticket_full(ticket, fields):
    '''Shows a ticket with it's comments.''' # Separated because Reasons
    print(ticket.key + ": " + ticket.fields.summary)
    print("Assignee: {0} --- Status: {1} --- Type: {2}"
            .format(assignee(ticket),
                    ticket.fields.status.name,
                    ticket.fields.issuetype.name))
    print("Description:\n" + ticket.fields.description)
    print()
    display_extended_fields(ticket, fields)
    print()
    display_comments(ticket)

def open_ticket(ticket):
    os.execl('/usr/bin/open', 'open', ticket.permalink())

def main():
    # Argparse fun
    parser = argparse.ArgumentParser()
    parser.add_argument("ticket", help="ticket to interact with", type=str)
    parser.add_argument("-c", "--comment", help="comment on a ticket", 
                        nargs="?", const=False)
    parser.add_argument("-f", "--file", 
                        help="load a file in order write as a comment")
    parser.add_argument("-t", "--transition", help="transition a ticket", 
                        nargs="?", const=False)
    parser.add_argument("-d", "--display", help="display a ticket",
                        action='store_true')
    parser.add_argument("-o", "--open", help="transition a ticket",
                        action='store_true')
    parser.add_argument("-e", "--embed", help="load an ipython console",
                        action='store_true')
    args = parser.parse_args()

    ticket = jira.issue(args.ticket)
    # This all depends on some kinda absurd punning where, by explicitly
    # setting a given arg to 'False' instead of it's default 'None', i can
    # dispatch on the kind of non-thing that arg is, coupled with some poorly
    # documented bullshit in argparse about how there are actually 2 'defaults'
    # for every arg, the 'default' and the 'const', where the const is used if
    # the flag is supplied but an argument is not passed to the flag

    action_taken = None
    if args.comment:
        add_comment(ticket, args.comment)
        display_comments(ticket)
        action_taken = 1
    elif args.comment == False:
        if args.file:
            with open(args.file, 'r') as file:
                data = file.read()
                add_comment(ticket, data)
        elif not sys.stdin.isatty():
            data = "{code}" + sys.stdin.read() + "{code}"
            add_comment(ticket, data)
        else:
            display_comments(ticket)
        action_taken = 1
    elif args.transition:
        transition(ticket, args.transition)
        action_taken = 1
    elif args.transition == False:
        interactive_transition(ticket)
        action_taken = 1
    elif args.embed:
        embed()


    if args.display:
        if action_taken:
            ticket = jira.issue(args.ticket)
        display_ticket_full(ticket, fields)
    if args.open:
        open_ticket(ticket)

if __name__ == "__main__":
    main()
