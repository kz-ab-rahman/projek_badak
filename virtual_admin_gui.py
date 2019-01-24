#!python3

import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
import global_param


class VirtualAdmin(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Virtual Admin")
        self.geometry('%dx%d+%d+%d' % (440, 400, 0, 0))

        self.bind('<Return>', self.click_button)  # bind the enter key to click_button

        self.reqLabel = Label(self, text="Request")
        self.reqLabel.grid(column=0, row=0)
        self.reqBox = tk.Entry(self, width=56)
        self.reqBox.grid(column=1, row=0)

        self.resLabel = Label(self, text="Response")
        self.resLabel.grid(column=0, row=1)
        self.resBox = scrolledtext.ScrolledText(self,width=40,height=23)
        self.resBox.grid(column=1, row=1)

        self.goButton = tk.Button(self, text="GO")
        self.goButton.bind('<Button-1>', self.click_button)
        self.goButton.grid(column=2, row=0)

    def click_button(self, event):
        """
        capture request and run
        """
        try:
            request = self.reqBox.get()
        except:
            request = ' '
        finally:
            self.reqBox.delete(0, END)  # clear req box for next incoming req
            self.run_and_output(request)

    def run_and_output(self, request):
        """
        process request and dump the result on "response" box
        """
        if not request.isalnum():  # if request not alpanumeric
            output = "*ERROR*: request is not alphanumeric"
        else:  # if alphanumeric
            request = request.lower()  # make all lower case
            requestList = request.split()  # split each work into list
            if len(requestList) > 3:
                requestList = requestList[:3]  # if request is more than 3 words, strip out the rest.
            if len(requestList) == 0:
                request = ''
            if len(requestList) >= 1:
                request = requestList[0]
            if len(requestList) >= 2:
                orderID = requestList[1]
            if len(requestList) == 3:
                misc = requestList[2]

            if request in global_param.rdReqList:
                output = 'READ: '+request.upper()
            elif request in global_param.wrReqList:
                output = 'WRITE: '+request.upper()
            elif request == '':
                pass
            else:
                output = "*ERROR*: '"+request+"' request is not recognized"

        self.resBox.delete(1.0, END)  # clear res box
        self.resBox.insert(INSERT, output)  # display the output


print("Virtual Admin GUI is running in this terminal")
app = VirtualAdmin()
app.mainloop()
