import tkinter as tk
from tkinter import ttk, messagebox, filedialog 
import sqlite3
import load_database

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
		self.frame = tk.LabelFrame(self.window,text="Fields of data",width=4)
		self.frame.grid(row=0,column=1,pady=0,padx=10)

		self.labels_entries_empty = {label:"" for label in self.labels_entries}
		for i,label in enumerate(self.labels_entries):
			if label=="ID":
				continue
			tk.Label(self.frame,text=label + " :").grid(row=i-1,column=0,padx=5,pady=3)

	def design_entries(self):
		
		self.dict_entries = {entry:"" for entry in self.labels_entries if entry!="ID"}
		self.text_variables = {entry:tk.StringVar() for entry in self.dict_entries}
		for i,entry in enumerate(self.dict_entries.keys()):
			self.dict_entries[entry] = tk.Entry(self.frame,textvariable=self.text_variables[entry])
			self.dict_entries[entry].grid(row=i,column=1,padx=5,pady=3)
		self.change_state_entries("disable")

	def design_menu(self):
		menu = tk.Menu(self.window)
		self.window.config(menu=menu)
		menu_inicio = tk.Menu(menu,tearoff=0)
		menu_inicio.add_command(label="Connect with Database",command=self.connecting_db)
		menu_inicio.add_command(label="Delete database",command=self.delete_db)
		menu_inicio.add_command(label="Exit",command=self.exit)
		menu.add_cascade(label="File",menu=menu_inicio)

	def design_treeview_and_buttons(self):

		self.button_new = ttk.Button(self.window,text="NEW",width=20,state=tk.DISABLED,command=self.add_new_register)
		#self.refresh_button = ttk.Button(self.window,text="REFRESH",width=20,state=tk.DISABLED)
		self.button_clear = ttk.Button(self.window,text="CLEAR CONTENTS",width=20,state=tk.DISABLED,command=self.clear_contents)

		self.button_new.grid(row=4,column=0,pady=5,padx=10)
		#self.refresh_button.grid(row=4,column=1,pady=5,padx=20)
		self.button_clear.grid(row=4,column=2,pady=5,padx=10)

		self.tree = ttk.Treeview(self.window,height=10,column=self.labels_entries)

		self.tree.grid(row=5,column=0,columnspan=4,padx=5,pady=5,sticky=tk.W + tk.E),
		self.tree.column("#0",width=0,stretch=tk.NO) 
		width = 100
		for i,label in enumerate(self.labels_entries):
		 	self.tree.heading(label,text=label)
		 	self.tree.column(label,width=10,anchor="c")

		self.button_delete = ttk.Button(self.window,text="DELETE",width=20,state=tk.DISABLED,command=self.delete_elements)
		self.button_edit = ttk.Button(self.window,text="EDIT",width=20,state=tk.DISABLED,command=self.edit_row)
		self.button_accept = ttk.Button(self.window,text="ACCEPT",width=20,state=tk.DISABLED,command=self.accept_changes)

		self.button_delete.grid(row=6,column=0,pady=5,padx=10)
		self.button_edit.grid(row=6,column=1,pady=5,padx=10)
		self.button_accept.grid(row=6,column=2,pady=5,padx=10)

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
				self.delete_rows_tree()
			except Exception as e:
				messagebox.showerror("Error","An error occurs when deleting the table: " + "\n{e}.")
			finally:
				self.change_state_buttons("disable")

	def connecting_db(self):
		try:
			query = "SELECT * FROM " + TABLE_NAME
			self.run_query(query)
			#data.sort(reverse=True)
			messagebox.showinfo("Connection","The connection has been correctly performed with table " + TABLE_NAME)
			self.load_data_treeview()
			self.change_state_buttons("able")
			self.change_state_entries("able")
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
					self.change_state_entries("able")
					load_database.load_db()
					self.load_data_treeview()
				except Exception as e:
					messagebox.showerror("Error",e)
					self.change_state_buttons("disable")
					self.change_state_entries("disable")

	def change_state_buttons(self,type_change):
		self.buttons = [self.button_accept,self.button_new,self.button_clear,self.button_edit,self.button_delete]
		if type_change == "disable":
			for i in range(len(self.buttons)):
				self.buttons[i]["state"] = tk.DISABLED
		elif type_change == "able":
			for i in range(1,len(self.buttons)):
				self.buttons[i]["state"] = tk.ACTIVE
			self.buttons[0]["state"] = tk.DISABLED
		else:
			pass

	def change_state_entries(self,type_change):
		if type_change == "able":
			for entry in self.dict_entries.values():
				entry["state"] = tk.NORMAL
		elif type_change == "disable":
			for entry in self.dict_entries.values():
				entry["state"] = tk.DISABLED

	def delete_rows_tree(self):
		for row in self.tree.get_children():
			self.tree.delete(row)

	def load_data_treeview(self):
		query = "SELECT * FROM " + TABLE_NAME
		data = self.run_query(query)
		self.delete_rows_tree()
		for row in data:
			self.tree.insert("",tk.END,values=row)

	def add_new_register(self):
		vacios = []
		for name,entry in self.dict_entries.items():
			if self.dict_entries[name].get() == "":
				vacios.append(name)

		if len(vacios)!=0:
			msg = "Los siguientes campos no pueden estar vacios: \n\n" + "\n".join(vacios)
			messagebox.showinfo("Alerta!",msg)
			return

		if not self.dict_entries["Age"].get().isnumeric():
			messagebox.showinfo("Alerta!","El campo 'Age' debe contener un valor numerico.")
			return 

		query = "INSERT INTO DATA(NAME,SURNAME,AGE,ADDRESS) VALUES(?,?,?,?)"
		parameters = [entry.get() for entry in self.dict_entries.values()]
		self.run_query(query,parameters)
		self.load_data_treeview()
		messagebox.showinfo("Informacion",f"El registro {parameters} ha sido guardado correctamente en la base de datos.")

	def accept_changes(self):
		try:
			selected_item = self.tree.selection()
			if len(selected_item) > 1:
				messagebox.showinfo("Warning","No se puede editar mas de un elemento a la vez.")
				return
			id_registro = self.tree.item(selected_item)['values'][0]
			for name,var in self.text_variables.items():
				parameter = [var.get()]
				query = f"UPDATE DATA SET {name.upper()} = ? where id = {id_registro}"
				self.run_query(query,parameter)
			self.load_data_treeview()
			self.clear_entries()
			messagebox.showinfo("Info","Se ha actualizado el registro correctamente.")
		except Exception as e:
			messagebox.showerror("Error",e)
			
	def edit_row(self):
		try:
			self.button_new["state"] = tk.DISABLED
			self.button_delete["state"] = tk.DISABLED
			self.button_accept["state"] = tk.ACTIVE
			self.tree.bind("<ButtonRelease-1>",self.show)
		except Exception as e:
			messagebox.showerror("Error","Ha ocurrido el siguiente error: " + str(e))

	def show(self,event):
		
		selected_item = self.tree.selection()
		if len(selected_item) > 1:
			return
		print(selected_item)
		row = self.tree.item(selected_item)["values"]		
		for i,value in enumerate(row[1:],start=1):
			self.text_variables[self.labels_entries[i]].set(value)

	def delete_elements(self):
		self.selected_items = self.tree.selection()
		if len(self.selected_items)==0:
			return
		ids_for_delete = []
		for item in self.selected_items:
			id_element = self.tree.item(item)["values"][0]
			ids_for_delete.append(id_element)
		print(ids_for_delete)

		for id_item in ids_for_delete:
			query = "DELETE FROM DATA WHERE ID = " + str(id_item)
			self.run_query(query)
		self.load_data_treeview()


	def clear_contents(self):
		self.clear_entries()
		self.tree.unbind("<ButtonRelease-1>")
		self.change_state_buttons("able")

	def clear_entries(self):
		for entry in self.dict_entries.values():
			entry.delete(0,tk.END)

	def run_query(self,query,parameters=()):
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute(query,parameters)
			conn.commit()
			result = cursor.fetchall()
			cursor.close()
		return result

crud = Crud()