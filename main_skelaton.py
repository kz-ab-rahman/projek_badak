import time
import random

auto_mode = 0
auto_push = 0

input('email login')
print('select Inbox')

counter = 0
while True:
    if auto_mode:
        if counter == 0:
            input('\nenter criteria: ')
        else:
            pass
        counter += 1
    else:
        input('\nenter criteria: ')

    print('\nsearching for email...')
    time.sleep(3)
    found = random.choice((True, False))
    if found:
        print('email found')
        time.sleep(3)
        if auto_mode:
            push = auto_push
        else:
            push = input('pushData data to database? ')

        if int(push):
            print('pushing data to database...')
            time.sleep(3)
    else:
        print('no email found')

    if auto_mode:
        print('next email check in 3 sec')
        time.sleep(3)
        continue

    # autoMode will never reach this point
    loop = input('search again? 0-No, 1-Yes:')

    if int(loop):
        pass
    else:
        break
