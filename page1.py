import random
import string
from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import messagebox


conn = sqlite3.connect('MyElections.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS poll(name TEXT)")

def Pollpage():
    win.destroy()
    win2 = Tk()
    win2.geometry('350x500')
    win2.title('eVote')
    win2.config(bg = '#7F00FF')
    win2.resizable(0,0)
    #to insert background image
    bgImage = PhotoImage(file = 'eVote3.png')
    labell = Label( win2, image = bgImage)
    labell.place(x = 0,y = 0)
    txtlabel =Label(win2,text='Vote for any one person!', font='Courier 15 bold italic').place(x= 30, y=90)
    vote=StringVar()
    
    def vote():
        addvote=vote.get()
        print(addvote)
        pd.execute('update poll set votes=votes+1 where name=?',(addvote,))
        pd.commit()
        messagebox.showinfo('Success!','You have voted')
        win2.destroy()
        initall_page()
##it is at this point you connect to login db and remove user!!!
    
    votebtn= Button(win2,text='Vote',command=vote, bg='Azure', width=10, font=12).place(x=240,y=430)
    vote=StringVar()
    names=[]
    print(plname)
    pd=sqlite3.connect(plname+'.db') #poll database
    pollcursor=pd.cursor() #poll cursor
    pollcursor.execute('select name from poll')
    data=pollcursor.fetchall()
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        names.append(ndata)
    print(names)
    placey = 130
    for i in range(len(names)):
        placey+= 35
        Radiobutton(win2, text=names[i], value=names[i], variable=vote).place(y=placey,x=35)
    
    homebtn= Button(win2, text="Main Menu", command=lambda: reload_page1(win2) )
    homebtn.place(x=275, y=0)
    win2.mainloop()
    

def Polls():
    win22.destroy()
    global win
    win = Tk()
    win.geometry('350x500')
    win.title('eVote')
    win.config(bg = '#7F00FF')
    win.resizable(0,0)
    #to insert background image
    bgImage = PhotoImage(file = 'eVote22.png')
    label1 = Label( win, image = bgImage)
    label1.place(x = 0,y = 0)

    psel=StringVar()
    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames = [
        "-select-"]
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)

    def proceed():
        global plname
        plname = psel.get()
        if plname=='-select-':
                return messagebox.showerror('Error','select poll')
        else:
            Pollpage()
        

    poll_list= ttk.Combobox(win, value=pollnames, state='readonly', textvariable=psel)
    poll_list.config(width= 30, )
    poll_list.current(0)
    poll_list.place(x= 20, y = 170)

    proceedbtn = Button(win, text="proceed", command=proceed)
    proceedbtn.config(width= 10,)
    proceedbtn.place(x= 250, y =170 )
    
    poll_label =Label(win, text='Select Poll', font='Courier 15 bold italic')
    poll_label.config(bg='#7F00FF', fg='WHITE')
    poll_label.place(x= 110, y=120)
    homebtn= Button(win, text="Main Menu", command=lambda: reload_page1(win) )
    homebtn.place(x=275, y=0)

    win.mainloop()


def Mypolls():
    win23.destroy()
    global win1
    win1 = Tk()
    win1.geometry('350x500')
    win1.title('eVote')
    win1.config(bg = '#7F00FF')
    win1.resizable(0,0)
    #to insert background image
    bgImage = PhotoImage(file = 'eVote3.png')
    labell = Label( win1, image = bgImage)
    labell.place(x = 0,y = 0)

    def CreatePoll():
        def regpoll():
            global pollcursor
            pname=pollname_entry.get()
            can_name=cname_entry.get()
            if pname=='':
                return messagebox.showerror('Error','Enter poll name')
            elif can_name=='':
                return messagebox.showerror('Error','Enter candidates')
            else:
                candidates=can_name.split(',') #candidate list
                cursor.execute('insert into poll (name) values (?);',(pname,))
                conn.commit()
                polldb = sqlite3.connect(pname+'.db') #to create poll database
                pollcursor=polldb.cursor()
                pollcursor.execute("CREATE TABLE IF NOT EXISTS poll(name TEXT,votes INTEGER)")
                for i in range(len(candidates)):
                    data=(candidates[i], 0)#to enter candiadate name and intial vote
                    pollcursor.execute('insert into poll (name,votes) values (?, ?)',data)
                    polldb.commit()
                polldb.close()
                messagebox.showinfo('Success!','Poll Created')
                cr.destroy()


        cr=Toplevel()
        cr.geometry('400x400')
        cr.title('Create a new poll')
        Label(cr,text='Poll Details',font='Helvetica 12 bold').place(x = 160, y=40)
        pollname = Label(cr,text='Poll name:', font= 12).place(x = 10, y=83 )
        pollname_entry = Entry(cr,width=45,)
        pollname_entry.place(x= 90, y= 85)
        txtlabel =Label(cr,text='(eg: presidential elections)').place(x=100,y=110)
        cname = Label(cr,text='Candidates:', font= 12).place(x=0,y=140)
        cname_entry =Entry(cr,width=45,)
        cname_entry.place(x=90,y=142) 
        txtlabel2 =Label(cr,text='Note: Enter the candidate names one by one by putting commas').place(x=49,y=175)
        txtlabel3 = Label(cr,text='eg: candidate1,candate2,candidate3....').place(x=49,y=190)
        proceedbtn =Button(cr,text='Proceed',command=regpoll).place(x=300,y=250)

        
    
    def PollResult():
        def result():
            sel = sele.get()
            if sel=='-select-':
                return messagebox.showerror('Error','Select Poll')
            else:
                poll_results.destroy()
                win1.destroy()
                res=Tk() #result-page
                res.geometry('350x500')
                res.title('Results!')
                res.config(bg = '#7F00FF')
                res.resizable(0,0)
                bgImage = PhotoImage(file = 'e.png')
                label1 = Label( res, image = bgImage)
                label1.place(x = 0,y = 0)
                homebtn= Button(res, text="Main Menu", command=lambda: reload_page1(res) )
                homebtn.place(x=275, y=0)

                textlabel = Label(res,text='Here is the Result!', font='Courier 17 bold italic', bg='#7F00FF',fg='white').place(y=70,x=40)
                con=sqlite3.connect(sel+'.db')
                pcursor=con.cursor()
                pcursor.execute('select * from poll')
                r=pcursor.fetchall() #data-raw
                placey = 130
                for i in range(len(r)):
                    data=r[i]
                    placey+=30
                    reslabel = Label(res,text=f'{data[0]}: {str(data[1])} votes', font='Courier 12 bold italic', bg ='#7F00FF', fg='white').place(x = 120, y=placey)
                res.mainloop()

        cursor.execute('select name from poll')
        data=cursor.fetchall()
        pollnames = [
            "-select-"]
        for i in range(len(data)):
            data1=data[i]
            ndata=data1[0]
            pollnames.append(ndata) 

        sele=StringVar()
        poll_results=Toplevel()
        poll_results.geometry('300x200')
        poll_results.title('Voting System')
        txtlabel = Label(poll_results,text='Select Poll',font='Helvetica 12 bold').place(y=30,x=100)
        poll_list= ttk.Combobox(poll_results, value=pollnames, state='readonly', textvariable=sele)
        poll_list.config(width= 40, )
        poll_list.current(0)
        poll_list.place(x= 20, y = 50)
        
        resultbtn = Button(poll_results, text="View Result", command=result)
        resultbtn.config(width= 10,)
        resultbtn.place(x= 200, y =100 )
        
    
        

    def Viewpolls():
        win1.destroy()
        view = Tk()
        view.geometry('350x500')
        view.title('View Polls')
        view.config(bg = '#7F00FF')
        view.resizable(0,0)

        #to insert background image
        bgImage = PhotoImage(file = 'e.png')
        label1 = Label( view, image = bgImage)
        label1.place(x = 0,y = 0)

        txt =Label(view, text='Polls', font='Courier 17 bold italic')
        txt.config(bg='#7F00FF', fg='black')
        txt.place(x= 150, y=80)
        homebtn= Button(view, text="Main Menu", command=lambda: reload_page1(view) )
        homebtn.place(x=275, y=0)


        cursor.execute('select name from poll')
        data=cursor.fetchall()
        placey= 120
        
        for i in range(len(data)):
            placey+=35
            data1=data[i]
            polls = Label(view,text=f'{data1[0]} election', font='Courier 14 bold', bg ='#7F00FF', fg='black').place(x = 90, y=placey)
        

        view.mainloop()

    createbtn = Button(win1, text= 'Create Poll', bg='Azure', width=14, font=12, command=CreatePoll)
    createbtn.place(x=120, y=150)
    resultbtn = Button(win1, text= 'Poll Result', bg='Azure', width=14, font=12, command=PollResult)
    resultbtn.place(x=120, y=200)
    viewbtn = Button(win1, text= 'View My Polls', bg='Azure', width=14, font=12, command=Viewpolls)
    viewbtn.place(x=120, y=250)
    homebtn= Button(win1, text="Main Menu", command=lambda: reload_page1(win1) )
    homebtn.place(x=275, y=0)
    regbtn = Button(win1, text= 'Register New User', bg='Azure', width=14, font=12, command=create_voter)
    regbtn.place(x=120, y=300)
    win1.mainloop()

def reload_page1(page):
    page.destroy()
    initall_page()

def initall_page():
    global root
    root = Tk()
    root.geometry('350x500')
    root.title('eVote')
    root.config(bg = '#7F00FF')
    root.resizable(0,0)

    #to insert background image
    bgImage = PhotoImage(file = 'e.png')
    label1 = Label( root, image = bgImage)
    label1.place(x = 0,y = 0)

    #buttons
    PollsButton = Button(root, text= 'Polls', bg='Azure', width=14, font=12, command= login_page)
    PollsButton.place(x=150, y=150)
    MyPollsButton = Button(root, text= 'MyPolls', bg='Azure', width=14, font=12, command=adminlogin)
    MyPollsButton.place(x=150, y=200)
    
    root.mainloop()
def create_voter ():
    win1.destroy()
    root1 = Tk()
    root1.title('eVote')
    root1.geometry('350x500')
    root1.config(bg='#7F00FF')
    root1.resizable(0,0)

    bgImage = PhotoImage(file = 'eVote3.png')
    label1 = Label(root1, image = bgImage)
    label1.place(x = 0,y = 0)

    conn = sqlite3.connect('evoters.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    name TEXT,
                    age INTEGER,
                    email TEXT,
                    phone_no INTEGER,
                    address TEXT,
                    pvc TEXT)""")

    def register():
        votername = name.get()
        voterage = age.get()
        voteremail = email.get()
        voterphone_no = phone_no.get()
        voteraddress = address.get()

        if votername  == "" or voterage == '' or voteremail == '' or voterphone_no == '' or voteraddress == '':
            messagebox.showwarning('Warning', 'Fill in the necessary details')
        else:
            conn = sqlite3.connect('evoters.db')
            cursor = conn.cursor()
            cursor.execute('SELECT name, phone_no FROM users WHERE name=? AND phone_no=?', (votername, voterphone_no))
            rows = cursor.fetchall()
            if(rows):
                messagebox.showwarning('Warning', 'This user already exists')
            else:
                voterpvc = generate_pvc()
                conn = sqlite3.connect('evoters.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users(name,age,email,phone_no,address, pvc) values(?,?,?,?,?,?)', (votername, voterage, voteremail, voterphone_no, voteraddress, voterpvc))
                conn.commit()
                
                messagebox.showinfo('Info', 'Your PVC number is \n'+voterpvc)
            conn.close()

    def generate_pvc():
        s = 10
        pvc = ''.join(random.choices(string.digits, k=s))
        real = str(pvc+'pvc')
        return real
        

    name = Entry(root1, width=30, font='Helvetica 10 bold')
    name.place(x=130, y=80)
    age = Entry(width=30,font='Helvetica 10 bold')
    age.place(x=130, y=115)
    email = Entry(width=30,font='Helvetica 10 bold')
    email.place(x=130, y=150)
    phone_no = Entry(width=30,font='Helvetica 10 bold')
    phone_no.place(x=130, y=185)
    address = Entry(width=30,font='Helvetica 10 bold')
    address.place(x=130, y=220)

    txtlabel = Label(root1,text='Name:',font='Helvetica 12 bold', bg='#bababa').place(y=80,x=50)
    txtlabel = Label(root1,text='Age:',font='Helvetica 12 bold', bg='#bababa').place(y=115,x=50)
    txtlabel = Label(root1,text='Email:',font='Helvetica 12 bold', bg='#bababa').place(y=150,x=50)
    txtlabel = Label(root1,text='Phone No:',font='Helvetica 12 bold', bg='#bababa').place(y=185,x=41)
    txtlabel = Label(root1,text='Address:',font='Helvetica 12 bold', bg='#bababa').place(y=220,x=50)

    regbtn = Button(root1, text="Register", command=register)
    regbtn.config(width= 10,)
    regbtn.place(x= 200, y=300)
    homebtn= Button(root1, text="Main Menu", command=lambda: reload_page1(root1) )
    homebtn.place(x=275, y=0)

    root1.mainloop()


def login_page():
    root.destroy()
    global win22
    win22 = Tk()
    win22.title('eVote')
    win22.geometry('350x500')
    win22.config(bg='#7F00FF',)
    win22.resizable(0,0)

    bgImage = PhotoImage(file = 'e.png')
    label1 = Label(win22, image = bgImage)
    label1.place(x = 0,y = 0)
    homebtn= Button(win22, text="Main Menu", command=lambda: reload_page1(win22) )
    homebtn.place(x=275, y=0)

    def login():
        votername = name.get()
        voterpvc = pvc.get()
        conn = sqlite3.connect('evoters.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, pvc FROM users WHERE name=? AND pvc=?', (votername, voterpvc))
        rows = cursor.fetchall()
        print(rows)
        if rows:
            Polls()
        else:
            messagebox.showwarning('Alert', 'You have to first register')
        conn.commit()
        cursor.close()
        conn.close()

    name = Entry(win22, width=29, font='Helvetica 10 bold')
    name.place(x=134, y=180)
    pvc = Entry(width=28,font='Helvetica 10 bold')
    pvc.place(x=139, y=220)

    txtlabel = Label(win22,text='Name:',font='Helvetica 12 bold', bg='#7F00FF').place(y=180,x=80)
    txtlabel = Label(win22,text='PVC Number:',font='Helvetica 12 bold', bg='#7F00FF').place(y=220,x=30)


    logbtn = Button(win22, text="Login", command=login)
    logbtn.config(width= 10,)
    logbtn.place(x= 200, y=300)


    win22.mainloop()

def adminlogin():
    root.destroy()
    global win23
    win23 = Tk()
    win23.title('Admin Login')
    win23.geometry('350x500')
    win23.config(bg='#7F00FF')

    bgImage = PhotoImage(file = 'evote3.png')
    label1 = Label(win23, image = bgImage)
    label1.place(x = 0,y = 0)
    homebtn= Button(win23, text="Main Menu", command=lambda: reload_page1(win23) )
    homebtn.place(x=275, y=0)

    admins = {
        'root': 'admin'
    }

    def login():
        adname = name.get()
        adpass = password.get()
        status = False
        for i, j in admins.items():
            if adname == i and adpass == j:
                status = True
        if status:
            Mypolls()
        else:
            messagebox.showwarning('Alert', 'You are not an admin and don\'t have access to this page')

    name = Entry(win23, width=30, font='Helvetica 10 bold')
    name.place(x=150, y=180)
    password = Entry(width=30,font='Helvetica 10 bold', show="*")
    password.place(x=150, y=220)

    txtlabel = Label(win23,text='Name:',font='Helvetica 12 bold', bg='#bababa').place(y=180,x=85)
    txtlabel = Label(win23,text='Password:',font='Helvetica 12 bold', bg='#bababa').place(y=220,x=55)


    logbtn = Button(win23, text="Login", command=login)
    logbtn.config(width= 10,)
    logbtn.place(x= 200, y=300)


    win23.mainloop()


initall_page()