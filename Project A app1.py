import random
from tkinter import *
from datetime import date, datetime
from tkinter.messagebox import showinfo
import psycopg2
import time

id_list = []

def create_id(id_list):
    laatste_getal = len(id_list)
    ident = laatste_getal + 1
    id_list.append(id)
    return ident


def clicked():
    global con
    naam1 = naam.get()
    bericht1 = bericht.get("1.0",END)
    print(naam1, bericht1)

    if len(naam1) == 0:
        naam1 = 'Anoniem'
    if len(bericht1) > 140:  # Input van gebruiker is te lang
        showinfo(title='Melding', message="Uw bericht is te lang!")
    elif len(bericht1) <= 0:  # Input van gebruiker is te kort
        showinfo(title='Melding', message="Uw bericht is te kort!")
    else:  # input van gebruiker is goed\
        showinfo(title='Melding', message="Uw bericht is verzonden en wordt beoordeeld!")

        datum = date.today()
        t = time.localtime()
        tijd = time.strftime("%H:%M:%S", t)

        stationlijst = (
'Arnhem',
'Almere',
'Amersfoort',
'Almelo',
'Alkmaar',
'Apeldoorn',
'Assen',
'Amsterdam',
'Boxtel',
'Breda',
'Dordrecht',
'Delft',
'Deventer',
'Enschede',
'Gouda',
'Groningen',
'Den Haag',
'Hengelo',
'Haarlem',
'Helmond',
'Hoorn',
'Heerlen',
'Den Bosch',
'Hilversum',
'Leiden',
'Lelystad',
'Leeuwarden',
'Maastricht',
'Nijmegen',
'Oss',
'Roermond',
'Roosendaal',
'Sittard',
'Tilburg',
'Utrecht',
'Venlo',
'Vlissingen',
'Zaandam',
'Zwolle',
'Zutphen',
)
        stationnaam = random.choice(stationlijst)

        con = psycopg2.connect(
            host='localhost',  # De host waarop je database runt
            database='stationzuil',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='Max1803'  # Wachtwoord die je opgaf bij installatie
            # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
        )

    cur = con.cursor()

    cur.execute("INSERT INTO bericht (id, tekst, datum, naam, station_city, tijd) VALUES (%s, %s, %s, %s, %s, %s)",
            (create_id(id_list), bericht1, datum, naam1, stationnaam, tijd))
    con.commit()
    # Cursor en connectie sluiten (en committen)
    cur.close()
    con.close()

    naam.delete(0, END)
    bericht.delete("1.0", END)

hoofdscherm = Tk()
hoofdscherm.title("Ns zuil")
hoofdscherm.geometry("950x600")
hoofdscherm.config(bg='#fff700')
nsLogo = Label(master=hoofdscherm,
              text='Feedback scherm',
              background='#0000cc',
              foreground='#FFFFFF',
              font=('Elephant', 18),
              width=74,
              height=3)
nsLogo.pack()

labelBericht = Label(master=hoofdscherm,
                    text='Laat hier uw mening achter. (Max. 140 karakters)',
                    foreground='#222373',
                    font=('Helvetica',12, 'bold italic'))
labelBericht.place(x=150, y=100)

labelNaam = Label(master=hoofdscherm,
                    text='Gelieve hier uw naam invullen (niet verplicht)',
                    foreground='#222373',
                    font=('Helvetica',12, 'bold italic'))
labelNaam.place(x=150, y=380)

naam = Entry(master=hoofdscherm)
naam.place(x=150, y=410, width=650, height=30)


bericht = Text(master=hoofdscherm, width=50, height=7)
bericht.place(x=150, y=130, width=650)

button = Button(master=hoofdscherm, text='Verzend',background='#0000cc', foreground='#FEFFF7', command=clicked)
button.place(x=380, y=295, width=200)

hoofdscherm.mainloop()