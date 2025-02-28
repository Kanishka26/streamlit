#st.write("i am writing using write method")
#st.title("this is title")
#st.header("this is header")
#st.subheader("this is subheader")
#st.markdown("<h1>heading</h1>",unsafe_allow_html=True)
#st.markdown("<marquee>New</marquee>",unsafe_allow_html=True)
#st.image("./img/images.jpeg",caption="this is image")

#st.checkbox("checkbox")
#st.button("signin")
#st.radio("Gender",options=['Male','Female'])
#st.selectbox("Country",options=['India','USA','UK'])


import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
def connect_db():
    conn=sqlite3.connect("mydb.db")
    return conn


def create_table():
    conn=connect_db()
    cur=conn.cursor()
    cur.execute("create table if not exists student(name text,password text,roll int,branch text)")
    conn.commit()
    conn.close()


def searchRecord(roll):
    conn=connect_db()
    cur=conn.cursor()
    cur.execute("select * from student where roll=?",(roll,))

    data=cur.fetchall()
    conn.close()
    return data


def deleteRecord(roll):
    conn=connect_db()
    cur=conn.cursor()
    cur.execute("delete from student where roll=?",(roll,))
    conn.commit()
    conn.close()


def repass():
    conn=connect_db()
    cur=conn.cursor()
    r=st.number_input("Enter Rollno",format="%d",value=int(0),key="roll")
    p=st.text_input("Enter New Password",type="password",key="pass")
    rp=st.text_input("Retype Password",type="password",key="repass")
    if st.button("Reset"):
        if(p==rp):
            cur.execute("update student set password=? where roll=?",(p,r))
            conn.commit()
            conn.close()
            st.success("Password Reset Successfully")
        else:
            st.error("Password Mismatch")
            conn.close()


def addRecord(data):
    st.success("Record Added Successfully")
    conn=connect_db()
    cur=conn.cursor()
    try:
         cur.execute("insert into student(name,password,roll,branch) values(?,?,?,?)",data)
         conn.commit()
         conn.close()
    except sqlite3.IntegrityError:
        st.error("Rollno already exists")
        conn.close()


def viewrecord():
    conn=connect_db()
    cur=conn.cursor()
    cur.execute("select * from student")
    data=cur.fetchall()
    conn.close()
    return data


def display():
    data=viewrecord()
    st.table(data)
    
def signup():
    st.title("Signup Form")
    name=st.text_input("Enter Name")
    password=st.text_input("Enter Password",type="password")
    retypepass=st.text_input("Retype Password",type="password")
    roll=st.number_input("Enter Rollno",format="%d",value=int(0))
    Branch=st.selectbox("Branch",options=['CSE','ECE','IT','AI/ML','MECH'])
    if st.button("SignUp"):
        if password!=retypepass:
            st.error("Password Mismatch")
        else:
            
            addRecord((name,password,roll,Branch))
    if st.button("Reset password"):
        repass()



create_table()


with st.sidebar:
    selected=option_menu('Select from here',['Signup','Display all record','Search Record','Delete Record'])

if selected=='Signup':
    signup()

elif selected=='Display all record':
    display()  

elif selected=='Search Record':
    roll = st.number_input("Enter roll number to be searched", format="%d", value=int(0))
    if st.button("Search"):
        data = searchRecord(roll)
        if data:
            st.table(data)
        else:
            st.error("Record not found")

elif selected=='Delete Record':
    roll = st.number_input("Enter roll number to be deleted", format="%d", value=int(0))
    if st.button("Delete"):
        deleteRecord(roll)
        st.success("Record deleted successfully")
    else:
        st.error("Record not found")
        


