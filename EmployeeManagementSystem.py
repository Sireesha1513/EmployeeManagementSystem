from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector
000000000000000000000000000000




root = Tk()
root.title("Employee Management System")
root.geometry("1500x900")
root.iconbitmap("employee.ico")
root["bg"] = "black"

def close():
    result = messagebox.showinfo("confirm","Do you want to Close")
    if result:
        root.destroy()
    else:
        pass

def employee_data():
    if  identry.get() == "" or nameentry.get() == "" or phoneentry.get() == "" or rolecombobox.get() == "" or gendercombobox.get() == "" or  salaryentry.get() == "":
        messagebox.showerror("Error","All fields are required")
    else:
        try:
            
            con = mysql.connector.connect(host = "localhost",user = "root",password = "Siri@1315")
            cursor = con.cursor()

            query = "CREATE DATABASE IF NOT EXISTS employee_db"
            cursor.execute(query)

            query = "USE employee_db"
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS ems (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Phone VARCHAR(15) NOT NULL,
            Role VARCHAR(50) NOT NULL,
            Gender VARCHAR(10) NOT NULL,
            Salary DECIMAL(10, 2) NOT NULL)"""
            cursor.execute(query)

            query = """INSERT INTO ems (Id, Name, Phone, Role, Gender, Salary ) VALUES (%s, %s, %s, %s, %s, %s)"""

            data = (
            identry.get(),
            nameentry.get(),
            phoneentry.get(),
            rolecombobox.get(),
            gendercombobox.get(),
            salaryentry.get()
        

tga        )

            cursor.execute(query,data)
            con.commit()
            employeeTable.insert("", "end", values=data)
            messagebox.showinfo("Success", "employee_data  Inserted Successfully")
        
        except Exception as e:
            
            messagebox.showerror("Error", f"Error inserting data: {e}")
            return

def show():

    con = mysql.connector.connect(host="localhost", user="root", password="Siri@1315",database = "employee_db")
    mycursor = con.cursor()
    query = "SELECT * FROM ems"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    employeeTable.delete(*employeeTable.get_children())
    if rows:
        for row in rows:
            employeeTable.insert("",END,values = row)
    messagebox.showinfo("information","All rows are displayed")

def delete():
    
    selected_item = employeeTable.selection()
    
    if not selected_item:
        messagebox.showwarning("Select Row", "Please select a row to delete.")
        return

    
    selected_values = employeeTable.item(selected_item, 'values')
    Id = selected_values[0]  

    
    con = mysql.connector.connect(host="localhost", user="root", passwd="Siri@1315", database="employee_db")
    cursor = con.cursor()

    
    delete_query = "DELETE FROM ems WHERE Id = %s"

    try:
        
        mycursor.execute(delete_query, (Id,))
        con.commit()

        
        employeeTable.delete(selected_item)

        messagebox.showinfo("Success", f"employee_data with Id. {Id} deleted successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Error deleting data: {e}")

def new_emp():
    identry.delete(0,END)
    nameentry.delete(0,END)
    phoneentry.delete(0,END)
    rolecombobox.set("Select  role")
    gendercombobox.set("Select gender")
    salaryentry.delete(0,END)

def delete_all():
    result = messagebox.askyesno("Confirm","Are you sure to delete all")
    if result:
        try:
            con = mysql.connector.connect(host="localhost", user="root", passwd="Siri@1315", database="employee_db")
            cursor = con.cursor()
            
            query = "DELETE FROM ems"
            cursor.execute(query)
            con.commit()

            for item in employeeTable.get_children():
                employeeTable.delete(item)
                messagebox.showinfo("success","all records are deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")

    else:
        pass

def search():
    
    selected_column = searchby.get()
    searchvalue = searchentry.get()

    

    for item in employeeTable.get_children():
        employeeTable.delete(item)
        

    try:
        con = mysql.connector.connect(host="localhost", user="root", passwd="Siri@1315", database="employee_db")
        cursor = con.cursor()

        query = "DESCRIBE ems"
        cursor.execute(query)
        columns = []
        result = cursor.fetchall()
        
        for  column in result:
            columns.append(column[0])

        query = f"SELECT * FROM ems WHERE {selected_column} = %s"
        cursor.execute(query,(searchvalue,))
        result = cursor.fetchall()

        if not result:
            messagebox.showinfo("information","Data was not found")

        for item in result:
            employeeTable.insert("",END,values = item)

    except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")

def select(e):
    index=employeeTable.focus()
    if not index:
        return
    content=employeeTable.item(index)
    data=content['values']

    if not data or len(data) < 6:
        messagebox.showerror("Error", "Row data is incomplete or missing.")
        return
    identry.delete(0, END)
    nameentry.delete(0, END)
    phoneentry.delete(0, END)
    rolecombobox.set("Select  role")
    gendercombobox.set("Select  gender")
    salaryentry.delete(0, END)
    
    identry.insert(0, data[0])
    nameentry.insert(0, data[1])
    phoneentry.insert(0, data[2])
    rolecombobox.set(data[3])
    gendercombobox.set(data[4])
    salaryentry.insert(0, data[5])


def update():
    index = employeeTable.focus()
    if not index:
        messagebox.showwarning('No Selection', 'Please select a record to update.')
        return

    content = employeeTable.item(index)
    listdata = content['values']

    if not listdata or len(listdata) < 6:  
        messagebox.showerror("Error", "Row data is incomplete or missing.")
        return

    try:
        id = listdata[0]  
        Name = nameentry.get()
        Phone = phoneentry.get()
        Gender = gendercombobox.get()
        Role = rolecombobox.get()
        Salary = salaryentry.get()
        newdata = (Name, Phone, Gender, Role, Salary)

        if listdata[1:6] == list(newdata):
            messagebox.showerror("No Changes Made", "No changes detected. Please make updates before saving.")
            return

        con = mysql.connector.connect(host='localhost', user='root', password='Siri@1315', database='employee_db')
        cur = con.cursor()

        update_query = """
        UPDATE ems
        SET Name = %s, Phone = %s, Gender = %s, Role = %s, Salary = %s
        WHERE id = %s
        """
        cur.execute(update_query, (*newdata, id))
        con.commit()

        employeeTable.item(index, values=(id, Name, Phone, Gender, Role, Salary))

        messagebox.showinfo("Success", f"Employee with ID {id} updated successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Error updating data: {e}")

    finally:
        con.close()
    

            
        
        
            
    
        
        

            
        
            

        
    
    
    



        



        
        
        
        
        
        
        
        

            


                                






headinglabel = Label(root,text  = "Mindtree software solutions",font=("anton",40,"bold"),bg = "black",fg = "cornflowerblue")
headinglabel.pack(fill = X)
                     
                     

lefframe = Frame(root, bg="black")
lefframe.place(x=0, y=100, width=350, height=535)

idlabel = Label(lefframe, text="Id", font=("arial", 13, "bold"), bg="black", fg="white")
idlabel.grid(row=0, column=0, padx=20, pady=30, sticky="W")
identry = Entry(lefframe, font=("arial", 13, "bold"), bg="white", fg="black", width=20)
identry.grid(row=0, column=1, padx=20, pady=30, sticky="W")

namelabel = Label(lefframe, text="Name", font=("arial", 13, "bold"), bg="black", fg="white")
namelabel.grid(row=1, column=0, padx=20, pady=30, sticky="W")
nameentry = Entry(lefframe, font=("arial", 13, "bold"), bg="white", fg="black", width=20)
nameentry.grid(row=1, column=1, padx=20, pady=30, sticky="W")

phonelabel = Label(lefframe, text="Phone", font=("arial", 13, "bold"), bg="black", fg="white")
phonelabel.grid(row=2, column=0, padx=20, pady=30, sticky="W")
phoneentry = Entry(lefframe, font=("arial", 13, "bold"), bg="white", fg="black", width=20)
phoneentry.grid(row=2, column=1, padx=20, pady=30, sticky="W")

rolelabel = Label(lefframe, text="Role", font=("arial", 13, "bold"), bg="black", fg="white")
rolelabel.grid(row=3, column=0, padx=20, pady=30, sticky="W")
rolecombobox = ttk.Combobox(lefframe, font=("arial", 13, "bold"), width=20, state="readonly")
rolecombobox["values"] = ("Manager", "Developer", "Tester", "HR", "Intern")
rolecombobox.grid(row=3, column=1, padx=20, pady=30, sticky="W")
rolecombobox.set("Select role")

genderlabel = Label(lefframe, text="Gender", font=("arial", 13, "bold"), bg="black", fg="white")
genderlabel.grid(row=4, column=0, padx=20, pady=30, sticky="W")
gendercombobox = ttk.Combobox(lefframe, font=("arial", 13, "bold"), width=20, state="readonly")
gendercombobox["values"] = ("male", "female")
gendercombobox.grid(row=4, column=1, padx=20, pady=30, sticky="W")
gendercombobox.set("Select gender")

salarylabel = Label(lefframe, text="Salary", font=("arial", 13, "bold"), bg="black", fg="white")
salarylabel.grid(row=5, column=0, padx=20, pady=30, sticky="W")
salaryentry = Entry(lefframe, font=("arial", 13, "bold"), bg="white", fg="black", width=20)
salaryentry.grid(row=5, column=1, padx=20, pady=30, sticky="W")


searchframe = Frame(root, bg = "black", relief=RIDGE)
searchframe.place(x=360, y=100, width=1200)
searchby = ttk.Combobox(searchframe,font = ("arial",15,"bold"), values=("Id", "Name", "Phone", "Salary", "Gender", "Role"), width=15)
searchby.grid(row=0, column=0)
searchby.set("Select A Option")

searchentry = Entry(searchframe,font = ("arial",12,"bold"),width = 11,bg = "orange",fg = "white")
searchentry.grid(row=0, column=1)

search = Button(searchframe, text="Search", width=25, font=("Arial", 15, "bold") ,bg="cornflowerblue", fg="white",command = search,cursor = "hand2")
search.grid(row=0, column=2,sticky = "W")

showall = Button(searchframe, text="Show All", width=25, font=("Arial", 15, "bold"), bg="cornflowerblue", fg="white",command = show,cursor = "hand2")
showall.grid(row=0, column=3,sticky = "W")

close = Button(searchframe, text="Close", width=16, font=("Arial", 15, "bold"), bg="cornflowerblue", fg="white",command = close,cursor = "hand2")
close.grid(row=0, column=4,sticky = "W")

rightFrame = Frame(root, bg="black")
rightFrame.place(x=370, y=150, width=1100, height=480)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

employeeTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary'),
                             xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set, show="headings")

scrollBarX.config(command=employeeTable.xview)
scrollBarY.config(command=employeeTable.yview)
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
employeeTable.bind("<<TreeviewSelect>>",select)
employeeTable.pack(fill=BOTH, expand=1)

employeeTable.heading("Id", text="Id")
employeeTable.heading("Name", text="Name")
employeeTable.heading("Phone", text="Phone")
employeeTable.heading("Gender", text="Gender")
employeeTable.heading("Role", text="Role")
employeeTable.heading("Salary", text="Salary")

employeeTable.column("Id", width=50, anchor=CENTER)
employeeTable.column("Name", width=70, anchor=W)
employeeTable.column("Phone", width=100, anchor=W)
employeeTable.column("Gender", width=80, anchor=CENTER)
employeeTable.column("Role", width=100, anchor=W)
employeeTable.column("Salary", width=100, anchor=CENTER)

employeeTable["show"] = "headings"
employeeTable.pack(fill=BOTH, expand=1)

style = ttk.Style()
style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), background='white', fieldbackground='white')
style.configure('Treeview.Heading', font=('arial', 15, 'bold'), foreground='blue')


downframe = Frame(root, bg="cornflowerblue")
downframe.place(x=0, y=650)

new_button = Button(downframe, text="New Employee", font=("arial", 16, "bold"), width=22, bg="cornflowerblue", fg="white",command = new_emp,cursor = "hand2")
new_button.grid(row=0, column=1, padx=10, pady=20)

add_button = Button(downframe, text="Add Employee", font=("arial", 14, "bold"), width=22, bg="cornflowerblue", fg="white",command = employee_data,cursor = "hand2")
add_button.grid(row=0, column=2, padx=10, pady=20)

update_button = Button(downframe, text="Update Employee", font=("arial", 14, "bold"), width=22, bg="cornflowerblue", fg="white",command = update)
update_button.grid(row=0, column=3, padx=10, pady=20)

delete_button = Button(downframe, text="Delete Employee", font=("arial", 14, "bold"), width=22, bg="cornflowerblue", fg="white",command = delete,cursor = "hand2")
delete_button.grid(row=0, column=4, padx=10, pady=20)

delete_all_button = Button(downframe, text="Delete All", font=("arial", 14, "bold"), width=20, bg="cornflowerblue", fg="white",command = delete_all,cursor = "hand2")
delete_all_button.grid(row=0, column=5, padx=10, pady=20)

root.mainloop()
