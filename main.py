import tkinter as tk
from tkinter import ttk, messagebox, filedialog 
import sqlite3

DB_PATH = "main_db.db"
TABLE_NAME = "DATA"
class Crud:
	labels_entries = ["ID","Name","Surname","Age","Address"]

	def __init__(self):
		self.window = tk.Tk()
		self.design_window(self.window)
		self.window.mainloop()

	def design_window(self,window):
		self.design_menu()
		self.window.title("Prueba")
		self.design_labels()
		self.design_entries()
		self.design_treeview_and_buttons()

	def design_labels(self):
		self.frame = tk.LabelFrame(self.window,text="Fields of data",width=10)
		self.frame.grid(row=0,column=1,pady=5,padx=10)

		for i,label in enumerate(self.labels_entries):
			tk.Label(self.frame,text=label + " :").grid(row=i,column=0,padx=5,pady=3)

	def design_entries(self):
		entries = ["ID","name","surname","age","addres"]
		dict_entries = {entry:"" for entry in entries}

		for i,entry in enumerate(entries):
			dict_entries[entry] = tk.Entry(self.frame)
			dict_entries[entry].grid(row=i,column=1,padx=5,pady=3)

	def design_menu(self):
		menu = tk.Menu(self.window)
		self.window.config(menu=menu)
		menu_inicio = tk.Menu(menu,tearoff=0)
		menu_inicio.add_command(label="Connect with Database",command=self.connecting_db)
		menu_inicio.add_command(label="Delete database",command=self.delete_db)
		menu_inicio.add_command(label="Exit",command=self.exit)
		menu.add_cascade(label="File",menu=menu_inicio)

	def design_treeview_and_buttons(self):

		self.button_new = ttk.Button(self.window,text="NEW",width=20,state=tk.DISABLED)
		self.button_accept = ttk.Button(self.window,text="ACCEPT",width=20,state=tk.DISABLED)
		self.button_cancel = ttk.Button(self.window,text="CANCEL",width=20,state=tk.DISABLED)
		
		self.button_new.grid(row=5,column=0,pady=5)
		self.button_accept.grid(row=5,column=1,pady=5)
		self.button_cancel.grid(row=5,column=2,pady=5)

		self.tree = ttk.Treeview(self.window,height=10,column=("c0","c1","c2","c3"))

		self.tree.grid(row=6,column=0,columnspan=4,padx=5,pady=5,sticky=tk.W + tk.E),
		
		for i,column_name in enumerate(self.labels_entries):
			print(i)
			self.tree.heading("#" + str(i),text=column_name,anchor=tk.CENTER)
			self.tree.column("#" + str(i),anchor=tk.CENTER)

		self.button_delete = ttk.Button(self.window,text="DELETE",width=20,state=tk.DISABLED)
		self.button_edit = ttk.Button(self.window,text="EDIT",width=20,state=tk.DISABLED)

		self.button_delete.grid(row=7,column=1,pady=5,padx=100)
		self.button_edit.grid(row=7,column=2,pady=5)

	def exit(self):
		messagebox.showinfo("Exit application","You are leaving this application.")
		self.window.destroy()

	def delete_db(self):
		response = messagebox.askyesno(title="Deleting",message="Are you sure you want to delete the table?")
		if response:
			try:
				query = "DROP TABLE IF EXISTS " + TABLE_NAME
				print(self.run_query(query))
				messagebox.showinfo("Deleting completed","The table " + TABLE_NAME +" has been deleted.")
			except Exception as e:
				messagebox.showerror("Error","An error occurs when deleting the table: " + "\n{e}.")
			finally:
				self.change_state_buttons("disable")

	def connecting_db(self):
		try:
			query = "SELECT * FROM " + TABLE_NAME
			data = self.run_query(query)
			messagebox.showinfo("Connection","The connection has been correctly performed with table " + TABLE_NAME)
			for row in data:
				self.tree.insert("",0,text=row[0],values=[row[1],row[2],row[3],row[4]])
			self.change_state_buttons("able")
		except Exception as e:
			msg = "An error occurs when connecting the database: " + f"\n{e}"
			messagebox.showerror("Error",msg)
			response = messagebox.askyesno(title="Connection",message="Do you want to create a new table?")
			if response:
				try:
					query = "CREATE TABLE " + TABLE_NAME  
					query += "(ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME VARCHAR(70),SURNAME VARCHAR(70),AGE INT,ADDRESS VARCHAR(100))"
					self.run_query(query)
					messagebox.showinfo("Sucess","The table " + TABLE_NAME + " has been created.")
					self.change_state_buttons("able")
				except Exception as e:
					messagebox.showerror("Error",e)
					self.change_state_buttons("disable")

	def change_state_buttons(self,type_change):
		self.buttons = [self.button_new,self.button_accept,self.button_cancel,self.button_edit,self.button_delete]
		if type_change == "disable":
			for button in self.buttons:
				button["state"] = tk.DISABLED
		elif type_change == "able":
			for button in self.buttons:
				button["state"] = tk.ACTIVE
		else:
			pass

	def delete_rows_tree(self):
		for row in self.tree.get_children():
			self.tree.delete(row)

	def run_query(self,query,parameters=()):
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute(query,parameters)
			conn.commit()
			result = cursor.fetchall()
			cursor.close()
		return result

crud = Crud()