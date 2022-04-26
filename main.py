#!/usr/bin/env python
# coding: utf-8

# In[2]:


#--------------------------------------------------------------------------------------------------------------
# IMPORT PACKAGES
#--------------------------------------------------------------------------------------------------------------

#default packages
import pandas as pd
import numpy as np

#ml model
#import transformers
import torch, re
import numpy as np
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

#gui
import tkinter as tk
from tkinter import ttk, Text, IntVar
from tkinter.messagebox import showinfo, showinfo, showerror
from tkinter import *
from tkinter.ttk import *
import webbrowser
from functools import partial
from tkinter.ttk import *

from tkinter import *
import webbrowser

#--------------------------------------------------------------------------------------------------------------
# FUNCTION TO RUN THE MACHINE LEARNING PROGRAM
#--------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------
# GUI WINDOW CONFIGURATION
#--------------------------------------------------------------------------------------------------------------

root = tk.Tk()
root.title('Text Classification for PNC DEMO')
root.tk.call("source", "./Files/Sun-Valley-ttk-theme-master/sun-valley.tcl")
root.tk.call("set_theme", "light")
screenw = root.winfo_screenwidth()
screenh = root.winfo_screenheight()
centerx = int(screenw / 2 - screenw / 2)
centery = int(screenh / 2 - 350 / 2)
root.geometry(f'{int(screenw)}x{int(screenh)}+{centerx}+{centery}')
root.resizable(False, False)


x, y = 0, 0
rmax, cmax = 10, 20

for r in range(rmax):
    root.rowconfigure(r, weight=1)
for c in range(cmax):
    root.columnconfigure(c, weight=1)

    
labeled = pd.DataFrame(columns=['Complaint', 'Department'])
mislabeled = pd.DataFrame(columns=['Complaint', 'Department'])
    
def create_frame(master):
    
    nframe=tk.Frame(root)
    nframe.config(bg="#fafafa")
    for r in range(rmax):
        nframe.rowconfigure(r, weight=1)
    for c in range(cmax):
        nframe.columnconfigure(c, weight=1)
        
    # VARIABLE DECLARATIONS
    customercomplaint = tk.StringVar()
    correcteddept = tk.StringVar()
    group1 = IntVar()
    group2 = IntVar()
    
    
    
    def capstoneproject(COMPLAINT):
        """
        Allows user to test their own complain in the Text-Classification using BERT  created by University of Pittsburgh's Master of Quantitative Economics Capstone Team- Joseph Karbowski, Micheal Gobreski, Shivangee Makharia
    
        Inputs:
        ---
        COMPLAINT is a string which is natural text of a customer complaint for PNC Banking
    
        Returns:
        ---
        The predicted department that will address customer complaint
    
        See Also:
        ---
        https://github.com/ShivMakh/Text-Classification-using-BERT
    
        """
    
        path = './Files/Model/'
    
        tokenizer = DistilBertTokenizer.from_pretrained(path, do_lower_case=True)
        model = DistilBertForSequenceClassification.from_pretrained(
            path, output_attentions=False, output_hidden_states=False)
    
        input = COMPLAINT
    
        input = input.lower()
        input = input.strip()
        input = ''.join([i for i in input if not i.isdigit()])
        input = re.sub('[\W_]', ' ', input)
        
        
        import spacy
        from spacy.lang.en.stop_words import STOP_WORDS as en_stop
        import nltk
        from nltk.tokenize import word_tokenize
        nltk.download('punkt')
    
        stop_words = list(en_stop) + ['ll', 've']
        tokens = word_tokenize(input)
        tokenized = [w for w in tokens if not w in stop_words]
        input = ' '.join(tokenized)
    
        input = tokenizer(input, return_tensors='pt')
        output = model(input['input_ids'], attention_mask=input['attention_mask'])
        _, predicted_values = torch.max(output[0], 1)
        predicted_values = predicted_values.numpy()[0]
        predicted_values = np.where(
            predicted_values == 0, 'Banking Services',
            np.where(
                predicted_values == 1, 'Card Services',
                np.where(
                    predicted_values == 2, 'Credit Reporting',
                    np.where(predicted_values == 3, 'Debt Collection',
                             np.where(predicted_values == 4, 'Loans',
                                      'Mortgage')))))
        return str(predicted_values)



    ##################################################################
    ## DO NOT TOUCH (ref to fix: https://www.tutorialspoint.com/how-to-create-a-hyperlink-with-a-label-in-tkinter )
    #Define a callback function
    """def callback(url):
        webbrowser.open_new_tab(url)


    #Create a Label to display the link
    link = tk.Label(nframe,
                 text="Documentation",
                 font=('Arial', 10),
                 fg="blue",
                 cursor="hand2")
    link.grid(row=rmax, column=y)
    link.bind(
        "<Button-1>", lambda e: callback(
            "https://github.com/ShivMakh/Text-Classification-using-BERT"))"""
    ###################################################################    
    def closewindow():
        """
        Append new customer complaints to csv files and closes window
        """
        global labeled
        global mislabeled
        labeled.to_csv('labeled.csv', mode='a', index=False, header=False)
        mislabeled.to_csv('mislabeled.csv', mode='a', index=False, header=False)
        root.destroy()


    def appendnewcomplaint(file, text, dept):
        """
        Adds new complaints to temporaty dataframe
        """
        tempdf = pd.DataFrame({'Complaint': [text], 'Department': [dept]})
        return file.append(tempdf)

    """
    def change_theme():
        #Switches window between light and dark more


        # NOTE: The theme's real name is sun-valley-<mode>
        if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
            root.tk.call("set_theme", "light")
            frame.config(bg='#fafafa')
        else:
            root.tk.call("set_theme", "dark")
            frame.config(bg='#1c1c1c')
    """
    def followupyes():
        """
        Clears the window and restarts program to allow user to add another complaint if they confirm that they have another complaint
        """

        global frame

        frame.destroy()
        frame=create_frame(root)

        frame.grid(row=x, column=y, rowspan=rmax, columnspan=cmax, sticky='news')



    def followup():
        """
        Asks user if they have another complaint to submit
        """

        followupquestion.grid(row=x + 5, column=y+2, columnspan=10)
        followupyes.grid(row=x + 5, column=y + 13, columnspan=2)
        followupno.grid(row=x + 5, column=y + 16, columnspan=3)


    def feedbackyes():
        """
        Adds complaint to the temp labeled dataframe if user says that classificaiton is correct, then will follow up with user
        """ 

        global labeled
        
        labeled = appendnewcomplaint(labeled,
                                     text=customercomplaint.get(),
                                     dept=capstoneproject(customercomplaint.get()))
        confirmyes = ttk.Label(
            frame,
            text=
            f'Okay, your complaint has been submited to {capstoneproject(customercomplaint.get())}. We will address this as soon as possible!'
        )
        confirmyes.grid(row=x + 4, column=y+1, columnspan=cmax, sticky='news')
        frame.after(10, followup)


    def feedbackno(event):
        """
        Asks for the correct department from user if classifications then will add complaint and corrected department to the temp mislabeled dataframe if user says that classificaiton is incorrect
        """

        global mislabeled
        mislabeled = appendnewcomplaint(mislabeled,
                                        text=customercomplaint.get(),
                                        dept=askcorrectdep.get())
        confirm = ttk.Label(
        frame,
        text=
        f'Okay, your complaint has been submited to {askcorrectdep.get()}. We will address this as soon as possible!')
        confirm.grid(row=x + 4, column=y+1, columnspan=cmax, sticky='news')
        frame.after(10, followup)


    def feedback():
        """
        Asks user if the classification is correct
        """
        getfeedback.grid(row=x + 3, column=y+1, columnspan=9)
        getfeedbackyes.grid(row=x + 3, column=y + 11, columnspan=2)
        getfeedbackno.grid(row=x + 3, column=y + 14, columnspan=5)
        askcorrectdep.grid(row=x + 3, column=cmax - 1, sticky='news')


    def submitcustomercomplaint():
        """
        Displays the department classification and then will ask user if it is accurate
        """
        reportMLpredition = ttk.Label(
            frame, text=f'This is for {capstoneproject(customercomplaint.get())}.')
        reportMLpredition.grid(row=x + 2, column=y, columnspan=cmax)
        frame.after(10, feedback)

    #create 
    apptitle = ttk.Label(nframe,text="PNC Complaint Portal", font=('Arial', 20), style='TLabel')
    #switchthemebutton = ttk.Checkbutton(nframe,text="Switch",style="Switch.TCheckbutton",command=change_theme)
    exitwindow = ttk.Button(nframe, text='Exit', command=closewindow)
    askcomplaint = ttk.Label(nframe, text='What is your complaint?')
    customercomplaint_entry = ttk.Entry(nframe,
                                    textvariable=customercomplaint,
                                    width=60)
    submitcomplainttextbutton = ttk.Button(nframe,
                                       text='Enter',
                                       style='Accent.TButton',
                                       command=submitcustomercomplaint,
                                       width=10)
    
    #starting widgets
    apptitle.grid(row=x, column=y + 1, columnspan=cmax - 1)
    #switchthemebutton.grid(row=x, column=cmax, padx=5, pady=10)
    askcomplaint.grid(row=x + 1, column=y, columnspan=8)
    customercomplaint_entry.grid(row=x + 1, column=y + 8, columnspan=12)
    submitcomplainttextbutton.grid(row=x + 1, column=cmax)
    exitwindow.grid(row=rmax, column=cmax)

    followupquestion = ttk.Label(nframe, text='Do you have another complaint?')
    followupyes = ttk.Radiobutton(nframe,
                                  text='Yes',
                                  variable=group2,
                                  value=1,
                                  command=followupyes)

    followupno = ttk.Radiobutton(nframe,
                                 text='No, Close this window',
                                 variable=group2,
                                 value=0,
                                 command=closewindow)

    getfeedback = ttk.Label(nframe, text='Is this the correct department?')
    getfeedbackyes = ttk.Radiobutton(nframe,
                                     text='Yes',
                                     variable=group1,
                                     value=1,
                                     command=feedbackyes)
    getfeedbackno = ttk.Radiobutton(nframe,
                                    text='No, this is for: ',
                                    variable=group1,
                                    value=0)

    askcorrectdep = ttk.Combobox(nframe, textvariable=correcteddept)
    askcorrectdep['values'] = ('Credit Reporting', 'Debt Collection',
                               'Card Services', 'Banking Services', 'Loans',
                               'Mortgage', 'Other')
    askcorrectdep['state'] = 'readonly'
    askcorrectdep.bind('<<ComboboxSelected>>', feedbackno)
    

    #define some widget configuration
    group1.set(2)  #for neither radio button to be defaulted
    group2.set(2)  #for neither radio button to be defaulted    
    customercomplaint_entry.delete(0, END)    
    customercomplaint_entry.focus_set()  #make cursor start on the entry point

    return nframe

frame=create_frame(root)
frame.grid(row=x, column=y, rowspan=rmax, columnspan=cmax, sticky='news')
root.mainloop()