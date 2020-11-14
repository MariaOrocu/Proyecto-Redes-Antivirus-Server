# !/usr/bin/python3
import socket, pickle
import os
import tkinter
from _thread import *
from threading import *
from tkinter import *
from tkinter import ttk
import pymysql



UPDATE_RATE = 3000
_mysql_server = "163.178.107.10"
_mysql_database = "redes_2_proyecto_1"
_mysql_server_port = 3306
_mysql_user = "laboratorios"
_mysql_password = "KmZpo.2796"
def todos():
    bd=pymysql.connect(
        host=_mysql_server,
        user=_mysql_user,
        password=_mysql_password,
        db=_mysql_database
        )
    fcursor=bd.cursor()
    
    fcursor.execute("SELECT * FROM firmas")
    contador=0

    salida=fcursor.fetchall()
    lista=[]
    bd.close()
    for x in salida:
        lista.append(x[1])
    return lista
def todos_usuarios():
    bd=pymysql.connect(
        host=_mysql_server,
        user=_mysql_user,
        password=_mysql_password,
        db=_mysql_database
        )
    fcursor=bd.cursor()
    
    fcursor.execute("SELECT * FROM usuario")
    contador=0

    salida=fcursor.fetchall()
    lista=[]
    bd.close()
    for x in salida:
        lista.append(x[1])
    return lista
mostrar_archivos():
    bd=pymysql.connect(
        host=_mysql_server,
        user=_mysql_user,
        password=_mysql_password,
        db=_mysql_database
        )
    fcursor=bd.cursor(nombre)
    
    bd=pymysql.connect(
        host=_mysql_server,
        user=_mysql_user,
        password=_mysql_password,
        db=_mysql_database
        )
    fcursor=bd.cursor()

    pregunta_id=fcursor.execute("SELECT id FROM usuario WHERE nombre='"+nombre+"'")
    bd.close()
    

    salida=fcursor.fetchall()
    lista=[]
    bd.close()
    for x in salida:
        lista.append(x[1])
    return lista
#lista=list(todos())
lista_n=[]
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1234
#ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server\n'))
    data = connection.recv(2048)
    lista_n.append(data.decode('utf-8'))
    while True:
        data2 = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8') + data2.decode('utf-8')
        if data2.decode('utf-8')=='exit':
            break
        connection.sendall(str.encode(reply))
        arr = (todos())
        data_string = pickle.dumps(arr)
        connection.sendall(data_string)
        datos=connection.recv(4096)
        datos_arr=pickle.loads(datos)
        if len(datos_arr)>0:
            guarda_virus(datos_arr, data.decode('utf-8'))
        else:
            print('acabalo')
        connection.send(str.encode('finalizado'))
    connection.close()

def guarda_virus(lista, nombre):
    bd=pymysql.connect(
        host=_mysql_server,
        user=_mysql_user,
        password=_mysql_password,
        db=_mysql_database
        )
    fcursor=bd.cursor()

    pregunta_id=fcursor.execute("SELECT id FROM usuario WHERE nombre='"+nombre+"'")
    bd.close()

    fcursor2=bd.cursor()
    for m in lista():
        sql="INSERT INTO archivos_con_virus(firma_archivo, id_usuario) VALUES ('{0}','{1}')".format(m,pregunta_id)

        try:
            fcursor.execute(sql)
            bd.commit()
            #messagebox.showinfo(message="registrado correctamente", title="success")
        except:
            bd.rollback()
            #messagebox.showinfo(message="no registrado", title="error")

        bd.close()
    
class Application(tkinter.Frame):
    """ GUI """
    def __init__(self, master):
        """ Initialize the Frame"""
        tkinter.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.updater()
 
    def create_widgets(self):
        """Create button. """
#         import os # import at top
#         import subprocess # doing nothing
        # Router
        self.button1 = tkinter.Button(self, command=mostrar_archivos)
        self.listbox = tkinter.Listbox(self)
        self.listbox2 = tkinter.Listbox(self)
        self.label=tkinter.Label(self, text="Eliga un usuario para ver sus archivos con virus")
        self.combo=ttk.Combobox(self, state="readonly")
        self.combo.set("Elige una opcion")
        self.combo["values"]=todos_usuarios()
        self.button1["text"] = "Router"
        self.button1["fg"] = "white"
        self.button1.grid(row=0, column=5, rowspan=1, columnspan=2)
        self.label.grid(row=0, column=15, rowspan=1, columnspan=2)
        self.listbox.grid(row=1, column=5, rowspan=1, columnspan=2)
        self.listbox1.grid(row=2, column=5, rowspan=1, columnspan=2)
        self.combo.grid(row=1, column=15, rowspan=1, columnspan=2)
    def update_button1(self):
        # Ping
        todos()
    
        self.listbox.delete(0, tkinter.END)
        
        #for list in self.listbox
            
        """hostname = "192.168.0.1"
        response = os.system("ping -n 1 " + hostname)
        # response
        if response == 0:
            self.button1["bg"] = "blue"
        else:
            self.button1["bg"] = "red"
         """
        self.listbox.insert(0, *lista_n)
    def updater(self):
        self.update_button1()
        self.after(UPDATE_RATE, self.updater)

def run():
    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client, ))
    ServerSocket.close()
    #ThreadCount += 1
    #print('Thread Number: ' + str(ThreadCount))

root = tkinter.Tk()
root.title("antivirus")
root.geometry("500x500")
app = Application(root)
control_thread=Thread(target=run, daemon=True)
control_thread.start()
root.mainloop()

#todos()
