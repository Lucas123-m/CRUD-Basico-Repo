import tkinter as tk
from tkinter import ttk, messagebox, filedialog 
import sqlite3

DB_PATH = "main_db.db"

class Crud:
	def __init__(self):
		self.ventana = tk.Tk()
		self.diseñar_ventana(self.ventana)
		self.ventana.mainloop()

	def diseñar_ventana(self,ventana):

		menu = tk.Menu(self.ventana)
		ventana.config(menu=menu)
		menu_inicio = tk.Menu(menu,tearoff=0)
		menu_inicio.add_command(label="Conectar con base de datos",command=self.conectar_bbdd)

		menu.add_cascade(label="Acciones",menu=menu_inicio)

		ventana.title("Prueba")
		labels_entries = ["ID","Name","Surname","Age","Address",]

		frame = tk.LabelFrame(ventana,text="Fields of data",width=10)
		frame.grid(row=0,column=1,pady=5,padx=10)

		for i,label in enumerate(labels_entries):
			tk.Label(frame,text=label + " :").grid(row=i,column=0,padx=5,pady=3)

		label_alert = tk.Label(ventana,text="Hola a todos").grid(row=i+1,column=1,pady=5)

		entries = ["ID","name","surname","age","addres"]
		dict_entries = {entry:"" for entry in entries}

		for i,entry in enumerate(entries):
			dict_entries[entry] = tk.Entry(frame)
			dict_entries[entry].grid(row=i,column=1,padx=5,pady=3)

		self.tree = ttk.Treeview(ventana,height=10,column=(0,1,2,3))

		self.tree.grid(row=i+2,column=0,columnspan=4,padx=5,pady=5,sticky=tk.W + tk.E),
		
		for i,column_name in enumerate(labels_entries):
			self.tree.heading("#" + str(i),text=column_name,anchor=tk.CENTER)

		ttk.Button(ventana,text="DELETE",width=20).grid(row=7,column=0,pady=5)
		ttk.Button(ventana,text="EDIT",width=20).grid(row=7,column=2,pady=5)

	def conectar_bbdd(self):
		try:
			query = "SELECT * FROM DATA"
			data = self.run_query(query)
			for row in data:
				self.tree.insert("",0,text=row[0],values=[row[1],row[2],row[3]])
			messagebox.showinfo("Conexion","Se ha conectado con la base de datos correctamente.")
		except Exception as e:
			msg = "Se ha producido el siguiente error al conectar con la tabla de la base de datos." + f"\n{e}"
			messagebox.showerror("Error",msg)
			respuesta = messagebox.askyesno(title="Conexion",message="Desea crear una nueva tabla?")
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

	def hola(self):
		print("hola")

crud = Crud()