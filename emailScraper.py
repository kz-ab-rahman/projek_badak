#!python3

import email, time, hashlib, re
import globalParam
from datetime import datetime,timezone

"""
getNewEmail: search for new email with specified email subject
input: mail (email obj)
return: emailList (list containing email ID for new email(s))
"""
def getNewEmail(mail, searchMode, since, before):
    """
    searchMode: 1-search for all unread email
                2-specify since and before dates
                3-get all today's email
                4-get all yesterday's email
                5-get email from specific sender
    """
    #print(f"since={since}\nbefore={before}")
    if searchMode == 1:
        criteria = 'UnSeen'
    elif searchMode == 2 or 3:
        criteria = '''(SINCE "'''+since+'''" BEFORE "'''+before+'''")'''
    else:
        criteria = 'Seen'

    print(f"criteria={criteria}")
    typ, data = mail.search(None,criteria) #search for ALL email meeting the criteria
    emailList = data[0].split()
    return emailList

"""
getNewOrder: extract order info from email, save to .txt file
input: mail (email obj), emailList (list of emailID of new order email)
output: newOrderFileList (list of .txt file containing new order)
"""
def getNewOrder(mail,emailList):
    newOrderFileList = []
    md5Old=''
    newEmailNum = len(emailList)
    for num, emailID in enumerate(emailList):
        print('Processing...'+str(num+1)+' of '+str(newEmailNum))
        result, emailData = mail.fetch(emailID,'RFC822')
        rawEmail = emailData[0][1].decode("utf-8")
        emailMsg = email.message_from_string(rawEmail)
        #sender = emailMsg['from']
        subject = emailMsg['subject']
        utcTime = emailMsg['date']
        #convert timezone from UTC -> local
        utcTimeObj = datetime.strptime(utcTime,'%a, %d %b %Y %H:%M:%S %z')
        localTimeObj = utcTimeObj.replace(tzinfo=timezone.utc).astimezone(tz=None)
        receivedTime = localTimeObj.strftime('%d/%m/%Y %I:%M %p')

        for i, item in enumerate(globalParam.okSubject):
            if subject.find(item) != -1: #check if the subject has what we're looking for
                proceed = True
                orderType = i
                #print(receivedTime,subject)
                break
            else:
                proceed = False

        if not proceed:
            continue #ignore (skip to next emailID)

        #Should only reach here is proceed == True
        for part in emailMsg.walk():
            if part.get_content_type() == 'text/html':
                payload = part.get_payload() #get_payload returns str
                #use md5 checksum of each email to skip duplicate
                md5New = hashlib.md5(payload.encode('utf-8')).hexdigest()
                #print('new md5='+md5New)
                #print('old md5='+md5Old)
                if md5New == md5Old: #catch duplicated email
                    #print('\nSKIP\n')
                    pass
                else:
                    md5Old = md5New
                    time.sleep(1) #delay 1sec to ensure unique filename bcoz we use time as filename
                    timeStamp = time.strftime("%d%m%Y")+"."+time.strftime("%H%M%S")
                    if orderType == 3: #fast food
                        pattern = "(\d+)" #get the formID
                        match = re.search(pattern,subject)
                        formID = match.group(1)
                        fileName = 'type3'+'_'+timeStamp+'_formID'+formID+'.html.txt'
                    else:
                        fileName = 'type'+str(orderType)+'_'+timeStamp+'.html.txt'

                    with open(globalParam.rawEmailPath+fileName, "w") as text_file:
                        print(payload+'recieved at '+receivedTime, file=text_file)

                    newOrderFileList.append(fileName)
            else:
                pass

        #mail.store(emailID,'-FLAGS','\Seen') #debug: unset 'Seen' flag
    return newOrderFileList

