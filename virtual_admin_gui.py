#!python3

import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
import global_param
import msg_generator
import backend_core


class VirtualAdmin(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.request = None
        self.order_id = None
        self.data = None
        self.output = None

        self.title("Virtual Admin")
        self.geometry('%dx%d+%d+%d' % (440, 400, 0, 0))

        self.bind('<Return>', self.click_button)  # bind the enter key to click_button

        self.reqLabel = Label(self, text="Request")
        self.reqLabel.grid(column=0, row=0)
        self.reqBox = tk.Entry(self, width=56)
        self.reqBox.grid(column=1, row=0)

        self.resLabel = Label(self, text="Response")
        self.resLabel.grid(column=0, row=1)
        self.resBox = scrolledtext.ScrolledText(self, width=40, height=23)
        self.resBox.grid(column=1, row=1)

        self.goButton = tk.Button(self, text="GO")
        self.goButton.bind('<Button-1>', self.click_button)
        self.goButton.grid(column=2, row=0)

    def click_button(self, event):
        """
        capture request and run
        """
        try:
            self.request = self.reqBox.get()
        except:
            self.request = ''
        finally:
            self.reqBox.delete(0, END)  # clear req box for next incoming req
            self.run_and_output()

    def run_and_output(self):
        """
        process request and dump the result on "response" box
        """
        if not self.request.isalnum():  # if request not alphanumerics
            self.output = "*ERROR*: request is not alphanumeric"
        else:  # if alphanumeric
            self.request = self.request.lower()  # make all lower case
            request_list = self.request.split()  # split each work into list
            if len(request_list) > 3:
                request_list = request_list[:3]  # if request is more than 3 words, strip out the rest.
            if len(request_list) == 0:
                self.request = ''
            if len(request_list) >= 1:
                self.request = request_list[0]
            if len(request_list) >= 2:
                self.order_id = request_list[1]
            if len(request_list) == 3:
                self.data = request_list[2]

            if self.request in global_param.valid_req_list:
                self.process_request()
                self.output = 'DUMMY RESPONSE: ' + self.request.upper()
            elif self.request == '':
                pass
            else:
                self.output = "*ERROR*: '" + self.request + "' request is not recognized"

        self.resBox.delete(1.0, END)  # clear res box
        self.resBox.insert(INSERT, self.output)  # display the output

    def process_request(self):
        return


print("Virtual Admin GUI is running in this terminal")
app = VirtualAdmin()
app.mainloop()
