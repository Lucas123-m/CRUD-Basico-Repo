import sqlite3
from tkinter import messagebox
CSV_PATH = r"C:\Users\Tec\Desktop\Lucas\Busqueda de conocimiento\Autoaprendizaje\Python\Autodidacta\proyectos\2022\taxables.csv"
DB_PATH = "main_db.db"
def load_db():
	try:
		with open(CSV_PATH) as f:
			for line in f:
				if len(line)==1:
					continue
				line = line.strip().split(",")
				for i in range(len(line)):
					line[i] = line[i].strip()
					if "," in line[i]:
						line[i] = line[i].replace(",",";")
					line[i] = line[i].strip('"')

				parameters = line[1:5]
				print(parameters)
				query = "INSERT INTO DATA(NAME,SURNAME,AGE,ADDRESS) VALUES(?,?,?,?)"
				run_query(query,parameters)

	except Exception as e:
		messagebox.showerror("Error",e)

def run_query(query,parameters=()):
	with sqlite3.connect(DB_PATH) as conn:
		cursor = conn.cursor()
		cursor.execute(query,parameters)
		conn.commit()
		res = cursor.fetchall()
		cursor.close()
	return res



if __name__=="__main__":
	load_db()

