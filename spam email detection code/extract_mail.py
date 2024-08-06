# -*- coding: utf-8 -*-
"""
@author: Zizo
"""

import imaplib
import email
import yaml
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/emails', methods=['GET'])
def get_emails():
    with open("credentials.yml") as f:
        content = f.read()

    my_credentials = yaml.load(content, Loader=yaml.FullLoader)

    user, password = my_credentials["user"], my_credentials["password"]

    imap_url = 'imap.gmail.com'

    mail1 = imaplib.IMAP4_SSL(imap_url)

    mail1.login(user, password)

    mail1.select('Inbox')

    key = 'FROM'
    value = 'janomarwa@gmail.com'
    _, data = mail1.search(None, key, value)
    mail_id_list = data[0].split()
    msgs = []
    for num in mail_id_list:
        typ, data = mail1.fetch(num, '(RFC822)')
        msgs.append(data)

    email_data = []
    # Use only the last message fetched
    for response_part in msgs[-1]:
        if isinstance(response_part, tuple):
            my_msg = email.message_from_bytes(response_part[1])
            email_item = {
                "subject": my_msg['subject'],
                "body": None
            }
            for part in my_msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_item["body"] = part.get_payload()
            email_data.append(email_item)

    return jsonify(email_data)


if __name__ == '__main__':
    app.run(debug=True)
