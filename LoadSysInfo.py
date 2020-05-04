# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:04:52 2020

@author: 7504560
"""
import tkinter as tk
import subprocess
import os.path
import os
import time
import get_assertion
import get_binaryToken
import ListUpdateAttachment
import base64
import re

root= tk.Tk()
canvas1 = tk.Canvas(root, width = 500, height = 300)
canvas1.pack()
currentDirectory = os.getcwd()

path=currentDirectory+'/out.txt'
# print(path)

def hello (): 
    result = subprocess.Popen(['powershell', 'systeminfo /fo CSV | ConvertFrom-Csv | convertto-json', '|', 'tee', 'out.txt'])
    loop=True
    while (loop==True):
        if os.path.isfile(path):
            process=subprocess.Popen(["powershell","whoami"],stdout=subprocess.PIPE);
            oracle_id=str(process.communicate()[0])
            oracle_id =(re.findall(r'\d+', oracle_id))[0]
            lines=''
            time.sleep(5)
            result=get_assertion.cert()
            if result=="error":
                label1 = tk.Label(root, text= "Failed", fg='red', font=('helvetica', 12, 'bold'))
                canvas1.create_window(250, 200, window=label1)
            token=get_binaryToken.binaryToken(result)
            if token=="error":
                label1 = tk.Label(root, text= "Failed", fg='red', font=('helvetica', 12, 'bold'))
                canvas1.create_window(250, 200, window=label1)  
            spoidcrl=get_binaryToken.spoidcrl(token)
            if spoidcrl=="error":
                label1 = tk.Label(root, text= "Failed", fg='red', font=('helvetica', 12, 'bold'))
                canvas1.create_window(250, 200, window=label1)  
            item_id=ListUpdateAttachment.updateList(spoidcrl,oracle_id)
            if item_id=="error":
                label1 = tk.Label(root, text= "Failed", fg='red', font=('helvetica', 12, 'bold'))
                canvas1.create_window(250, 200, window=label1)  
            with open(path,encoding="utf-16-le") as myfile:
                lines = myfile.readlines()
                system_info=' '.join(lines)
                attachment = str(base64.b64encode(system_info.encode()))
                ListUpdateAttachment.sendAttachment(item_id,attachment,spoidcrl)
                if item_id=="error":
                    label1 = tk.Label(root, text= "Failed", fg='red', font=('helvetica', 12, 'bold'))
                    canvas1.create_window(250, 200, window=label1)  
                label1 = tk.Label(root, text= "System Information updated Successfully!", fg='green', font=('helvetica', 12, 'bold'))
                canvas1.create_window(250, 200, window=label1)
            os.remove(path)
            loop=False
        else:
            loop=True
    
    
button1 = tk.Button(text='Click Me',command=hello, bg='brown',fg='white')
canvas1.create_window(250, 150, window=button1)

root.mainloop()