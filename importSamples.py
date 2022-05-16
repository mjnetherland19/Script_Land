import requests
from Tkinter import *
import tkFileDialog
import ttk
import pylightxl as xl
import sys
import re


HOST_URL = "http://localhost:8080/senaite"

Return = "e43b12f2af2142b08d516cf0428a4eca"
Dont_Return = "cecef8ad479a421b99ca453f4c9f8eae"

sixteenS="ae75ee3beadf4711aa9648e52d517a3c"
GEN="5a853fe77df24891b3b9801ca0f249e6"
FITS = "e745da76fd634dffa821fe0e357a69d9"

Fridge1="47513c22d5dd4f40adc52db1d511655b"

# Understanding the below lists: each "sub-list" is comprised of the UID's for the steps in an analysis.
# For example, the first "super-list" 'S' has the steps for 16SBacID. Each sublist's index within the super-list
# corresponds to a turn around time plus one, since the list index starts at zero. 
# Five sub-lits for 1, 2, 3, 4, 5 turn around times.

S=[["efd1717eee954fa2b4382496060d0037","142e58ec350645f0bf3bbc7e7ca3a106","56ce58ec960d434ea2eb9d605d68e058"],
 ["6b1ae0fbea7c457bb87071bc8c320c9a","f72232b191684956bff391d6f8ab1010","2e4f5f72ad2c4735822dc81f40c41791"],
 ["5a91ed6d49cf4c93a63e860bd5f0794e","5d7f5565883a4b2b894e3463c438c20e","d0d90e176895420f875e7756ecef707e"],
 ["e5f6ea13d41744caaa6cf074f8a1b469","e1a2b05ea50a4b57b9e49595da8b87a0", "5c40f02481b746e5bd06cf65cdf79835"],
 ["8f33ddb6e35a441189d6826feb18fbf5", "20afa87bfc774bf0b2f2e9b251d3f34b","1037a4935f4a47b0af81d7bf184269d5"]]

FITs=[["7dddcf6d80a940d7a1d0b40127331b3f","6214c1698ac64c288a92102397438dcc","5a364bad13fe440589e2eac230d0d206"],
 ["f497daeae4fd4114a4a06a704c3fcab8","3c0a186c925a4547ad4e234f9ed39d43","c727d48fb62b4a9d90248d38cd4e9c9c"],
 ["296c39bdd00c4361bc35deaf23348a47","33a8cfdf08534fe99f6ac4aff199e519","fee43664a1d24630995e660878280946"],
 ["259c95d2580745838d17ba76f50999ab","d14c2b05c19648dbbaffc7e93d0b9173","bb9046e4f2594dc9a1d1d98db913492e"],
 ["d639199519d3483e98e0dddbc81ff155","26eabe23bef64d4380aa607a6612ec9e","c311f45e8d494f2bb45d9841a1775ed3"]]

GENNY=[["692c30a855404deba26a8e9a8790e345","68d4df5663b54cfa983f5736eb525c53","d5dfaee68033458bafc05752fd440f34"],
 ["528e6f87aa31418f8f5adc4d46c58b0a","fc832f4e68614307a832e91c93a1adf3","85242e01be8a4f5a8cbc628594ff59e7"],
 ["a383c048ae72468caca69892cac800cc","25c3c016db604857b98a6c9e3e39940e","2e15b82d3576409692d8dedf0919d1ac"],
 ["a10c3e8089134a47821d593fcd48f32c","a2a7fbb7f59842f68d028f6d326ed4dd","115eed05d14846468844419ad49a097b"],
 ["873620937302438abacc1836f7a32022","b49ba42afdb84c0f953b2eee24f084bc","847cb38ac36849b3879578abe0d8c382"]]

def makeData():

    A=[]
 
    wb = xl.readxl("{}".format(pathToExcel), ws=("Sheet1"))
    for row in wb.ws(ws='Sheet1').range('A16:F24'):
        if row[0]=='' or row[1] == '' or row[2] == '' or row[3] == '' or row[4] =='' or row[5]=='':
            continue
        else:
            A.append(row[1:6])

    for x in A:
        pt=x[1].strip().lower()
        analysis=x[2].strip().lower()
        returnn=x[3].strip().lower()
        tat=x[4]
        if tat > 5:
            continue

        #Writes Client Sample ID to dictionary 'data'
        data["ClientSampleID"] = "{}".format(x[0])

        #Writes whether Plate or Tube to dictionary 'data'
        if pt == "plate":
            data["ClientReference"] = "Plate"
        elif pt == "tube":
            data["ClientReference"] = "Tube"

        #Writes Service to Sample Type to dictionary 'data'
        if analysis == "ezbac16sid":
            data["SampleType"] = "{}".format(sixteenS)
            data["Analyses"] = tuple(S[tat-1])
        elif analysis == "ezbacgenid":
            data["SampleType"] = "{}".format(GEN)
            data["Analyses"] = tuple(GENNY[tat-1])
        elif analysis == "ezfunitsid":   
            data["SampleType"] = "{}".format(FITS)
            data["Analyses"] = tuple(FITs[tat-1])

        #Writes whether to return sample to Template in dictionary 'data'
        if returnn == "yes":
            data["Template"] = "{}".format(Return)
        elif returnn =="no":
            data["Template"] = "{}".format(Dont_Return)

        #Establishes connection to client for which samples will be applied
        url = "{}/@@API/senaite/v1/AnalysisRequest/create/{}".format(HOST_URL, data["Client"])
        session.post(url, data=data)

    submit.destroy()
    window.quit()

def resetSubmit():
    submit.destroy()
    B2["state"]="active"
    reset()

def reset():
    E1.delete(0,len(E1.get()))
    listBox1.delete(0,listBox1.size())
    listBox2.delete(0,listBox2.size())
    for x in sorted(title):
        listBox1.insert(END, x.strip('\n'))
    B1["state"]="active"
    listBox1.bind("<<ListboxSelect>>", entry)

def conAdd(event):
    
    global submit
    global root
    global pathToExcel
    
    conselect=listBox1.get(listBox1.curselection()[0])
    data["Contact"]=conuid[contitle.index(conselect)]
 
    root = Tk()
    root.title("File_Selection")
    pathToExcel = tkFileDialog.askopenfilename(title="Files",initialdir="/home/mjnetherland19/Downloads")

    if pathToExcel:
        root.destroy()

        B2["state"]="disabled"
               
        listBox2.insert(END,select)
        listBox2.insert(END,conselect)
        listBox2.insert(END,pathToExcel)

        submit=Tk()
        submit.title("Import or Reset")
        submit.geometry("1100x300")
        submit.option_add('*Font', ("Arial", "30"))
        submit.grid_rowconfigure(1, weight=1)
        labelSubmit = Label(submit, height=2, text="Do you want to Import samples from the selected file or\n Reset your choice and select again?").pack(side=TOP)
        B3=Button(submit, height=2, text="Import", command = makeData).pack(side=LEFT)
        B4=Button(submit, height=2, text="Reset", command = resetSubmit).pack(side=RIGHT)
        submit.protocol("WM_DELETE_WINDOW", resetSubmit)


def entry(event):
    global select
    B1["state"]="disabled"
    select=listBox1.get(listBox1.curselection()[0])
    data["Client"] = uid[title.index(select)]
    listBox1.delete(0,listBox1.size())
    for x in sorted(conClientPair[data["Client"]]):
        listBox1.insert(END, x.strip('\n'))

    listBox1.bind("<<ListboxSelect>>", conAdd)


def searching():
    searched=[]
    listBox1.delete(0,listBox1.size())

    for x in title:
        match=re.search("{}".format(E1.get().lower()), x.lower())
        if match:
            searched.append(x.strip())

    for y in sorted(searched):
        listBox1.insert(END,y)


def get_session(user, password):
    session = requests.Session()
    session.auth = (user, password)
    url = "{}/@@API/senaite/v1/auth".format(HOST_URL)
    response = session.get(url)
    if response.status_code != 200:
        session = None
    return session


if __name__ == "__main__":

    user = "admin"
    password = "admin"

    # Get an authenticated session
    session = get_session(user, password)

    if not session:
        print "Cannot authenticate"
    else:
        i=-1
        conClientPair={}
        contactDict={}

        contactsD="{}/@@API/senaite/v1/contact".format(HOST_URL)
        contacts=session.get(contactsD).text
       
        conuid=re.findall("(?<!_)uid\":\s\"([0-9a-z]{32})", str(contacts))
        contitle=re.findall("(?<=title\":\s\")(.+?)\"", str(contacts))
        conClient=re.findall("(?<=client/)([0-9a-z]{32})",str(contacts))
        
        for x in conClient:
            i+=1
            if x in conClientPair.keys():
                conClientPair[x].append(contitle[i])
            elif x not in conClientPair.keys():
                conClientPair[x]=[contitle[i]]


        #Get list of all clients
        url = "{}/@@API/senaite/v1/client".format(HOST_URL)
        strangs =session.get(url)
        search = strangs.text

        #UID is a unique string for each client
        uid=re.findall("(?<!_)uid\":\s\"([0-9a-z]{32})", str(search))
        title=re.findall("(?<=title\":\s\")(.+?)\"", str(search))
        
        dic={}

        # Starting dictionary to be sent to Senaite for sample import. DateSampled is required for manual sample creation, but
        # it isn't requred for using this script. You can exclude it. If you ever want to use it, just add "DateSampled" : "2020-03-19 15:56:20"
        # Senaite prefers that date format I believe. Similarly, if you ever want to include the client contact, add "Contact": "<client_contact_uid>" to
        # the 'data' dictionary
        data = {
            "StorageLocation" : Fridge1 }

        window = Tk()
        window.title("Import Samples")
        window.geometry("1250x1250")
        window.option_add('*Font', ("Arial", "30"))
        frame=Frame(window)


        scroll=Scrollbar(frame, orient="vertical")
        scroll.pack(side=RIGHT, fill=Y)

        E1=Entry(window)
        
        B1=Button(window, height=2, text="Search", command = searching)
        B2=Button(window, height=2, text="Reset", command = reset)
        
        listBox1 = Listbox(frame, height=10,width=150, yscrollcommand=scroll.set)
        listBox2 = Listbox(window, height=3,width=150)

        text=Text(window,bg='gray87',font=("Arial", "24", 'bold'),height=12,padx=3,spacing1=5,spacing3=5, width=100)
        text.insert(END,"1. Use the search box to narrow down the list of clients.\n   Ex. Searching 'ed' will yield Fred and Eddy.\n")
        text.insert(END,"2. Select a name to then select the client's contact.\n   Contact list corresponds to selected client.\n")
        text.insert(END,"3. After selecting the contact then select the client's\n   excel file from a list of files.\n")
        text.insert(END,"4. The name and file path you've chosen will be shown in the\n   box below the client list.\n")
        text.insert(END,"5. You will then be asked if you wish to import the samples\n   from the excel file chosen or to reset the process.\n")
        text.insert(END,"*Use the Reset button below to reset any and all secetions")
        
        #Adds client names to GUI
        for x in sorted(title):
            listBox1.insert(END, x.strip('\n'))

        E1.pack(side=TOP)
        B1.pack(side=TOP)
        frame.pack()
        listBox1.pack(fill=Y,side=TOP)
        listBox2.pack(side=TOP)
        text.pack(side=TOP)
        B2.pack(side=TOP)

        listBox1.bind("<<ListboxSelect>>", entry)

        window.mainloop()

