#!python3

import email
import time
import hashlib
import re
import global_param
from datetime import datetime, timezone


def get_new_email(mail, search_mode, since, before, sender):
    """
    search_mode: 1-search for all unread email
                 2-specify since and before dates
                 3-get all today's email
                 4-get all yesterday's email
                 5-get email from specific sender
    """
    # print(f"since={since}\nbefore={before}")
    if search_mode == 1:
        criteria = 'UnSeen'
    elif search_mode == 2 or 3 or 4:
        criteria = '''(SINCE "'''+since+'''" BEFORE "'''+before+'''")'''
    else:
        criteria = 'Seen'

    print(f"criteria={criteria}")
    typ, data = mail.search(None, criteria)  # search for ALL email meeting the criteria
    email_list = data[0].split()
    return email_list


def get_new_order(mail, email_list):
    new_order_file_list = []
    md5_old = ''
    new_email_total = len(email_list)
    for num, email_id in enumerate(email_list):
        print('Processing...'+str(num+1)+' of '+str(new_email_total))
        if global_param.debug:
            print(f"DEBUG: email_id = {email_id}")
        result, email_data = mail.fetch(email_id, 'RFC822')
        raw_email = email_data[0][1].decode("utf-8")
        email_msg = email.message_from_string(raw_email)
        if global_param.debug:
            print("DEBUG: email_msg =")
            print(email_msg)
        sender = email_msg['from']
        subject = email_msg['subject']
        utc_time = email_msg['date']
        if global_param.debug:
            print(f"DEBUG: sender = {sender}")
            print(f"DEBUG: subject = {subject}")
            print(f"DEBUG: utc_time = {utc_time}")
        # convert timezone from UTC -> local
        utc_time_list = utc_time.split(" ")  # split the time into list first
        if len(utc_time_list) > 6:
            utc_time_list = utc_time_list[:6]  # strip off anything after 5th items.
            utc_time = " ".join(utc_time_list)  # rejoin the list into str
        utc_time_obj = datetime.strptime(utc_time, '%a, %d %b %Y %H:%M:%S %z')
        local_time_obj = utc_time_obj.replace(tzinfo=timezone.utc).astimezone(tz=None)
        received_time = local_time_obj.strftime('%d/%m/%Y %I:%M %p')
        if global_param.debug:
            print(f"DEBUG: received_time = {received_time}")

        proceed = False
        order_type = -1
        for i, item in enumerate(global_param.ok_subject):
            if subject.find(item) != -1:  # check if the subject has what we're looking for
                proceed = True
                order_type = i
                # print(received_time,subject)
                break
            else:
                proceed = False

        if not proceed:
            continue  # ignore (skip to next email_id)

        # Should only reach here is proceed == True
        for part in email_msg.walk():
            if part.get_content_type() == 'text/html':
                payload = part.get_payload()  # get_payload returns str
                # use md5 checksum of each email to skip duplicate
                md5_new = hashlib.md5(payload.encode('utf-8')).hexdigest()
                # print('new md5='+md5_new)
                # print('old md5='+md5_old)
                if md5_new == md5_old:  # catch duplicated email
                    # print('\nSKIP\n')
                    pass
                else:
                    md5_old = md5_new
                    time.sleep(1)  # delay 1sec to ensure unique filename bcoz we use time as filename
                    time_stamp = time.strftime("%d%m%Y")+"."+time.strftime("%H%M%S")
                    if order_type == 3:  # fast food
                        pattern = r'(\d+)'  # get the form_id
                        match = re.search(pattern, subject)
                        form_id = match.group(1)
                        file_name = 'type3'+'_'+time_stamp+'_formID'+form_id+'.html.txt'
                    else:
                        file_name = 'type'+str(order_type)+'_'+time_stamp+'.html.txt'

                    with open(global_param.raw_email_path + file_name, "w") as text_file:
                        print(payload+'received at '+received_time, file=text_file)

                    new_order_file_list.append(file_name)
            else:
                pass

        # mail.store(email_id,'-FLAGS','\Seen') #debug: unset 'Seen' flag
    return new_order_file_list


"""
if __name__ == '__main__':
    search_mode = 0
    since =
    before =

    mail = imaplib.IMAP4_SSL(global_param.server_name)
    password = getpass.getpass("Enter password: ")

    mail.login(global_param.username, password)
    status, messages = mail.select(global_param.email_folder)

    email_list = get_new_email(mail, search_mode, since, before)
"""
