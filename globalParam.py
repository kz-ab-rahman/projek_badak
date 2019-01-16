#!python3
import time

workPath = 'C:\\Users\\mabrahma\\Documents\\projek_badak\\'
rawEmailPath = workPath+'raw_email\\'
masterOrderPath = workPath+'master_csv\\'
dailyOrderPath = workPath+'daily_csv\\'
dailyOrderDataFile = dailyOrderPath+time.strftime("%b%d-%Y")+'_order_data.csv'
dailyFoodDataFile = dailyOrderPath+time.strftime("%b%d-%Y")+'_food_data.csv'
restaurantDataFile = masterOrderPath+'restaurant.csv'
orderDataFile = masterOrderPath+'order_data.csv'
foodDataFile = masterOrderPath+'food_data.csv'
incomingDateFormat = '%d/%m/%Y %I:%M %p' #http://strftime.org/
pickupToDeliveryGap = 15 #minutes
validArgList = ['main.py', 'debug', 'runloop', 'updatecsvmaster', 'updatecsvdaily', 'genmsg']

#email related parameters
usernm = 'hippofooddelivery@gmail.com'
serverName = 'imap.gmail.com'
emailFolder = 'Inbox'
checkInterval = 10 #sec
okSubject= ["New order has been placed",
            "New order lunch Set has been placed",
            "Hello",
            "Hippo Fast Food Delivery",]

#regex. https://regex101.com/
regexInOrder = 'Number: <\/strong>\s?([^<]+).*Place Time: <\/strong>\s?([^<]+)<\/p><hr(?: \/|><p)>(.*)(?:Tax Total|Delivery (?:Charge|Fee)).*Created on :<\/strong> ([^<]+)<\/p><p>([^<]+).*Information :<\/strong><\/p><p>(.*)<br(?: \/)?>\s?(.*)<br(?: \/)?>\s?(.*)<br(?: \/)?>(.*)<br(?: \/)?>'
regexInFood = 'Details<\/strong> : (.+)\s\((?:RM)?([^)]+).*Qty<\/strong> : ([^<]+).*Notes <\/strong>:\s?([^<]+)'
regexInFastFood = 'Nama</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Phone</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Alamat</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Nama Restoran</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Menu</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Masa Penghantaran</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*recieved at ([^ ]+) (.*)'

#list of request supported by Virtual Admin
rdReqList = ['status', 'msgkedai', 'msgrider', 'rider', 'help']
wrReqList = ['cancel', 'donepickup', 'donedeliver', 'updateaddress', 'updatefood', 'updatephone', 'setrider']

#mouse position for theBridge
newMsgPixColor = (255,255,255)
newMsgPos = (1340,930)
replyBoxPos = (1500,1000)
reqBoxPos = (80,45)
resBoxPos = (85,70)


#print(dailyOrderDataFile)