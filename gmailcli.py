#!/usr/bin/env python3

import argparse
import json
import sys
from argparse import RawTextHelpFormatter

from gmail import gmail, history
from gmail.textwrap import wrap_long, wrap_short


def main() -> None:
    parser = argparse.ArgumentParser(
        description=wrap_long(
            "Interactive command-line interface to access the Gmail API. It"
            " allows to issue API calls by concatenating their method names"
            " with an underscore. E.g., to call the method"
            " 'users.messages.list', you just have to write 'messages_list'"
            " followed by the arguments the method takes, e.g.,"
            ' labelIds=["INBOX"]. The answer from the Gmail server will be'
            " printed to the screen, either the API call response or an error."
        ),
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-p",
        "--profile",
        metavar="NAME",
        help=wrap_short(
            "profile name to store Gmail access token and command history file"
            f" under '{gmail.get_profile_dir()}'"
        ),
        required=True,
    )

    # Parse arguments
    args = parser.parse_args()
    profile_name = args.profile

    (creds, err) = gmail.authenticate(profile_name)
    if err:
        sys.exit(1)
    profile_dir = gmail.get_profile_dir(profile_name)
    history.init(profile_dir)
    print("Type Ctrl-D to quit")
    while True:
        try:
            line = input(">>> ")
            (response, err) = gmail.execute(creds, line)
            if not err:
                print(
                    json.dumps(
                        response, indent=2, ensure_ascii=False, sort_keys=True
                    )
                )

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")

        except EOFError:
            print()
            break


if __name__ == "__main__":
    main()
