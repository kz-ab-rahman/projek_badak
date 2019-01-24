#!python3

import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
import global_param
import msg_generator


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
            request_list = request.split()  # split each work into list
            if len(request_list) > 3:
                request_list = request_list[:3]  # if request is more than 3 words, strip out the rest.
            if len(request_list) == 0:
                request = ''
            if len(request_list) >= 1:
                request = request_list[0]
            if len(request_list) >= 2:
                order_id = request_list[1]
            if len(request_list) == 3:
                data = request_list[2]

            if request in global_param.rdReqList:
                self.read_request(request, order_id)
                output = 'READ: '+request.upper()
            elif request in global_param.wrReqList:
                self.write_request(request, order_id, data)
                output = 'WRITE: '+request.upper()
            elif request == '':
                pass
            else:
                output = "*ERROR*: '"+request+"' request is not recognized"

        self.resBox.delete(1.0, END)  # clear res box
        self.resBox.insert(INSERT, output)  # display the output

    def read_request(self, request, order_id):
        # open today.csv for reading
        # extract the line that has the order id
        # remap the line to masterOrderList and masterFoodList
        if request == 'msg2shop':
            response = msg_generator.gen_text_msg('shop', master_order_list, master_food_list,
                                                   order_num, rider_name)
        elif request == 'msg2rider':
            response = msg_generator.gen_text_msg('rider', master_order_list, master_food_list,
                                                   order_num, rider_name)

        return response

    def write_request(self, request, order_id, data):
        return


print("Virtual Admin GUI is running in this terminal")
app = VirtualAdmin()
app.mainloop()
