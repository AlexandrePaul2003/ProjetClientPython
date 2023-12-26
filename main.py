import select
import socket
import tkinter
from tkinter import *
from struct import *


def demandNewName():
    global nouvelle
    nouvelle = Toplevel(root)
    nouvelle.title("Nouvelle fenêtre")

    nouvelle.geometry("400x300")
    lbl1 = Label(nouvelle, text="Nouveau nom")
    lbl1.grid(row=0, column=0)
    but1 = Button(nouvelle, text="ok", command=lambda: changeName(e1.get()))
    but1.grid(row=1, column=1)
    e1 = Entry(nouvelle, width=10)
    e1.grid(row=2, column=0)


def changeName(newName):
    nouvelle.destroy()
    try:
        if len(newName) < 20:
            newName = newName.ljust(20, " ")
            donnee = pack("ii21s", 29, 0, newName.encode())
            client_socket.send(donnee)
            print("envoyé :" + str(newName))
            donnee = " "
            client_socket.setblocking(True)
            donnee = client_socket.recv(1024)
            client_socket.setblocking(False)
            print(donnee)
            type, isError, nom = unpack("ii40s", donnee)
            print("unpacked")
            print(type)
            print(isError)
            if isError == 0:
                lblNom.config(text="Bienvenue : " + newName.rstrip() + " !")
            else:
                if type == -1 & isError == 1:
                    # todo fenetre d'erreur
                    lblNom.config(text="Bienvenue : " + nom.decode().rstrip() + " !")

    except:
        print("An exception occurred")


def comm():
    print("in the after")
    main()


def getCannals():
    canaux = ""
    donnee = pack("ii", 8, 1)
    client_socket.send(donnee)









def printNewCanals(canaux):
    i = 1
    for canal in canaux.split('|'):
        names[i] = canal.replace('\u00B2',' ')
        names[i] = names[i].rstrip()
        lbl = Label(root, text=canal)
        lbl.grid(row=i, column=0)
        but1 = Button(root, text="Rejoindre", command=lambda nom=canal: joinCanal(nom))
        but1.grid(row=i, column=1)
        i += 1


def joinCanal(name):
    global nbrCanauxRejoin
    print(name)
    name = name.ljust(20, ' ')
    donnee = pack("ii21s", 29, 2, name.encode())
    client_socket.send(donnee)
    client_socket.setblocking(True)
    donnees = client_socket.recv(1024)
    client_socket.setblocking(False)
    type, isError = unpack('ii', donnees[0:8])
    print(type)
    print(isError)
    if type == -1 and isError == 0:
        createWindow(name)
    else:
        if isError == 1 and type == -1:
            print("if de merde")
            # afaire : ecran d'erreur avec l'erreur
        else:
            print("ta mère")
            # afaire : redigier la reception et afficher l'erreur


def findCanalIndice(actualnom):

    print("nom des canaux : ")
    if len(actualnom) == 21:
        actualnom = list(actualnom)
        actualnom[len(actualnom) - 1] = ' '
        actualnom = ''.join(actualnom)
    print(str(len(nom)))
    for i in range(0, len(nomCanaux)):

        canaux=nomCanaux[i]
        if len(canaux)==21:
            canaux = list(canaux)
            canaux[len(canaux) - 1] = ' '
            canaux = ''.join(canaux)

        canaux=canaux.rstrip()
        print(canaux)
        print(str(len(canaux)))
        if canaux == actualnom:
            return i

    return -1


def sendMessage(canal, message):
    print(canal)
    print(message)
    if len(message) < 120:
        donnee = pack("ii21s121s", 150, 3, canal.ljust(20, ' ').encode(), message.ljust(120, ' ').encode())
        client_socket.send(donnee)


def quitServer():
    pass


def main(nom):
    global root
    root = Tk()
    root.title("test")
    root.geometry("1920x1080")
    global lblNom
    lblNom = Label(root, text="Bienvenue : " + nom + " !")
    lblNom.grid(row=0, column=0)
    menubar = Menu(root)
    actualiser_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Actualiser", command=getCannals)

    # Création du deuxième menu
    changer_nom_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Changer Nom", command=lambda: demandNewName())
    creer_canal_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Creer un canal", command=lambda: demandCanalName())
    quitter = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Quitter le server", command=lambda: quitServer())

    root.config(menu=menubar)
    tmp = root.after(1000, recepServer())
    recepServer()
    print("finishing")
    root.mainloop()
    print("fin")

def demandCanalName():
    global nouvelleCanal
    nouvelleCanal = Toplevel(root)
    nouvelleCanal.title("Nouvelle fenêtre")

    nouvelleCanal.geometry("400x300")
    lbl1 = Label(nouvelleCanal, text="Nouveau nom")
    lbl1.grid(row=0, column=0)
    but1 = Button(nouvelleCanal, text="ok", command=lambda: createCanal(e1.get()))
    but1.grid(row=1, column=1)
    e1 = Entry(nouvelleCanal, width=10)
    e1.grid(row=2, column=0)

def createCanal(newName):

    nouvelleCanal.destroy()
    try:
        if len(newName) < 20:
            newName = newName.ljust(20, " ")
            donnee = pack("ii21s", 29, 2, newName.encode())
            client_socket.send(donnee)
            print("envoyé :" + str(newName))
            donnee = " "
            client_socket.setblocking(True)
            donnees = client_socket.recv(1024)
            client_socket.setblocking(False)
            type, isError = unpack('ii', donnees[0:8])
            print(type)
            print(isError)
            if type == -1 and isError == 0:
                createWindow(newName)
            else:
                if isError == 1 and type == -1:
                    print("if de merde")
                    # afaire : ecran d'erreur avec l'erreur
                else:
                    print("ta mère")
                    # afaire : redigier la reception et afficher l'erreur

    except:
        print("An exception occurred")


def quitCanal(nom):
    indice = findCanalIndice(nom.rstrip())
    if indice>-1:
        windowCanal[indice].destroy()
        nom=nom.ljust(20,' ')
        print("quitting canal " + nom)
        donnee=pack('ii21s',29,7,nom.encode())
        client_socket.send(donnee)
        nomCanaux[0]=" "
        nMessCanaux[0]=" "
        roleCanaux[0]=" "
        frameCanal[0]=" "
        windowCanal[0]=" "
    else :
        print(nom+ " " + str(len(nom)))
        print("canal non trouvé")


def createWindow(newName):
    global nbrCanauxRejoin
    print("canaux : ")
    print(nbrCanauxRejoin)
    nomCanaux[nbrCanauxRejoin] = newName.rstrip()
    nMessCanaux[nbrCanauxRejoin] = 0
    roleCanaux[nbrCanauxRejoin] = 0  # 0 pour membre 1 pour opérateur
    windowCanal[nbrCanauxRejoin] = Toplevel(root)
    windowCanal[nbrCanauxRejoin].title(newName)
    windowCanal[nbrCanauxRejoin].geometry("400x300")
    sendBarre = Frame(windowCanal[nbrCanauxRejoin])
    sendBarre.grid(row=1, column=0)
    sendBarre.pack(side=BOTTOM)
    frameCanal[nbrCanauxRejoin] = Frame(windowCanal[nbrCanauxRejoin])
    frameCanal[nbrCanauxRejoin].pack(anchor="nw")
    but = Button(sendBarre, text="Quitter", command=lambda nom=newName: quitCanal(nom))
    but.grid(row=0, column=0)
    but1 = Button(sendBarre, text="Envoyer", command=lambda nom=newName: sendMessage(nom.rstrip(), e1.get()))
    but1.grid(row=0, column=1)
    e1 = Entry(sendBarre, width=100)
    e1.grid(row=0, column=2)
    nbrCanauxRejoin += 1
def messageReceived(donnees):
    print("treating message")
    print(donnees)
    sender,canal, message = unpack('20s20s120s', donnees[4:164])
    print("unpacked")
    sender= sender.decode('utf-8')
    sender=sender.rstrip()
    canal = canal.decode('utf-8')
    message = message.decode('utf-8')
    message=message.rstrip()
    canal = canal.rstrip()
    print("info msg")
    print(canal)
    print(sender)
    print(message)
    indice = findCanalIndice(canal)
    if (indice < 0):
        # afaire : erreur
        print("canal non trouvé")
    else:
        print("affichage...")
        print(indice)
        affichage = sender +" : " +message
        lblMess = Label(frameCanal[indice], text=affichage)
        print("debug1")
        nMessCanaux[indice] += 1
        print("debug2")
        print(nMessCanaux[indice])
        lblMess.grid(row=nMessCanaux[indice], column=0) #problème avec la frame
        print("debug3")
        #nMessCanaux[indice] += 1
        print("debug4")


def recepServer():
    # root.after_cancel(tmp)
    sockets_list = [client_socket]
    sockets, _, _ = select.select(sockets_list, sockets_list, sockets_list, 1)
    for s in sockets:
        print('reception')
        donnees = client_socket.recv(1024)
        print("donne : "+str(donnees))
        # type=1
        try:
            type = unpack('i', donnees[:calcsize('i')])[0]
            print("unpacked")
            if type == 1:
                print("receiving canals")
                Ctaille = unpack('i', donnees[4:8])[0]
                print("taille: " + str(Ctaille))
                #donnees = client_socket.recv(1024)
                canaux = unpack(f"{Ctaille-1}s", donnees[8:8+Ctaille-1])[0].decode('utf-8')
                print("debug 1")
                if(Ctaille!=0):
                    printNewCanals(canaux)
            elif type == 7:
                print("receiving message")
                messageReceived(donnees)
                print('tg')
            else:
                print("erreur switch")
        except:
            print("exception dealt with")
        # recu = unpack("i21s",donnees)

    tmp = root.after(1000, recepServer)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 6000)

client_socket.connect(server_address)
nom = client_socket.recv(1024).decode()
nom = nom.rstrip()
client_socket.setblocking(False)
global nbrCanauxRejoin
global nomCanaux
global nMessCanaux
global roleCanaux
global frameCanal
global windowCanal
nbrCanauxRejoin = 0
nomCanaux = {}
nMessCanaux = {}
roleCanaux = {}
frameCanal = {}
windowCanal = {}
names = {}

main(nom)

# premier_int, deuxieme_int = unpack("i21s", donnee[:calcsize("ii")])
# client_socket.close()
