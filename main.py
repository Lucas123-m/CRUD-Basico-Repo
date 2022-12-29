import tkinter as tk
from tkinter import ttk, messagebox, filedialog 
import sqlite3

DB_PATH = "main_db.db"

class Crud:
	labels_entries = ["ID","Name","Surname","Age","Address"]

	def __init__(self):
		self.window = tk.Tk()
		self.design_window(self.window)
		self.window.mainloop()

	def design_window(self,window):
		self.design_menu()

		window.title("Prueba")
		self.design_labels()

	def design_labels(self):
		frame = tk.LabelFrame(window,text="Fields of data",width=10)
		frame.grid(row=0,column=1,pady=5,padx=10)

		for i,label in enumerate(labels_entries):
			tk.Label(frame,text=label + " :").grid(row=i,column=0,padx=5,pady=3)

	def design_entries(self):
		entries = ["ID","name","surname","age","addres"]
		dict_entries = {entry:"" for entry in entries}

		for i,entry in enumerate(entries):
			dict_entries[entry] = tk.Entry(frame)
			dict_entries[entry].grid(row=i,column=1,padx=5,pady=3)

	def design_menu(self):
		menu = tk.Menu(self.window)
		window.config(menu=menu)
		menu_inicio = tk.Menu(menu,tearoff=0)
		menu_inicio.add_command(label="Connect with Database",command=self.conectar_bbdd)

		menu.add_cascade(label="File",menu=menu_inicio)

	def design_treeview_and_buttons(self):

		ttk.Button(window,text="NEW",width=20).grid(row=i+1,column=0,pady=5)
		ttk.Button(window,text="SAVE",width=20).grid(row=i+1,column=1,pady=5)
		ttk.Button(window,text="CANCEL",width=20).grid(row=i+1,column=2,pady=5)

		self.tree = ttk.Treeview(window,height=10,column=(0,1,2,3))

		self.tree.grid(row=i+2,column=0,columnspan=4,padx=5,pady=5,sticky=tk.W + tk.E),
		
		for i,column_name in enumerate(labels_entries):
			print(i)
			self.tree.heading("#" + str(i),text=column_name,anchor=tk.CENTER)
			self.tree.column("#" + str(i),anchor=tk.CENTER)

		ttk.Button(window,text="DELETE",width=20).grid(row=8,column=1,pady=5,padx=100)
		ttk.Button(window,text="EDIT",width=20).grid(row=8,column=2,pady=5)

	def conectar_bbdd(self):
		try:
			query = "SELECT * FROM DATA"
			data = self.run_query(query)
			messagebox.showinfo("Connection","The connection was correctly performed.")
			for row in data:
				self.tree.insert("",0,text=row[0],values=[row[1],row[2],row[3],row[4]])

		except Exception as e:
			msg = "An error occurs when connecting the database: " + f"\n{e}"
			messagebox.showerror("Error",msg)
			respuesta = messagebox.askyesno(title="Connection",message="Do you want to create a new table?")
			if respuesta:
				try:
					query = "CREATE TABLE DATA "  
					query += "(ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME VARCHAR(70),SURNAME VARCHAR(70),AGE INT,ADDRESS VARCHAR(100))"
					self.run_query(query)
					print("Ok")
				except Exception as e:
					messagebox.showerror("Error",e)
					

	def run_query(self,query,parameters=()):
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute(query,parameters)
			conn.commit()
			result = cursor.fetchall()
			cursor.close()
		return result

crud = Crud()