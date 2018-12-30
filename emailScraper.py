#!python3

import email, time, hashlib
import globalParam

"""
getNewEmail: search for new email with specified email subject
input: mail (email obj)
return: emailList (list containing email ID for new email(s))
"""
def getNewEmail(mail):
    typ, data = mail.search(None,'UnSeen') #search for ALL unread email
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
    for emailID in emailList:
        result, emailData = mail.fetch(emailID,'RFC822')
        rawEmail = emailData[0][1].decode("utf-8")
        emailMsg = email.message_from_string(rawEmail)
        #parse email header and catch sender's address
        parser = email.parser.HeaderParser()
        headers = parser.parsestr(emailMsg.as_string())
        senderAddress = email.utils.parseaddr(headers['From'])
        #if sender is not hippofood@gmail.com, skip.
        if senderAddress[1] != 'hippofood@gmail.com':
            #print('not from hippo')
            continue #ignore (skip to next emailID) if email not from hippo
        else:
            #print('this is from hippo')
            pass #proceed to the next line
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
                    fileName = 'new_order_'+timeStamp+'.html.txt'
                    with open(globalParam.rawEmailPath+fileName, "w") as text_file:
                        print(payload, file=text_file)
                    newOrderFileList.append(fileName)
            else:
                pass

        #mail.store(emailID,'-FLAGS','\Seen') #debug: unset 'Seen' flag
    return newOrderFileList

