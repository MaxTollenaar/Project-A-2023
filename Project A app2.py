from datetime import date
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox
import psycopg2
import time

# code voor functies
datum = date.today()
t = time.localtime()
tijdstip = time.strftime("%H:%M:%S", t)

id1_list = []

def create_id1(id1_list):
    laatste_getal = len(id1_list)
    ident = laatste_getal + 1
    id1_list.append(id)
    return ident

def accept():
    modnaam = comboExample.get()
    modopmerking = opmerking.get('1.0', END)
    if modnaam == '':
        showinfo(title='Error', message="Selecteer moderator")
    else:
        con = psycopg2.connect(
            host='localhost',  # De host waarop je database runt
            database='stationzuil',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='Max1803'  # Wachtwoord die je opgaf bij installatie
            # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
        )
        cur = con.cursor()
        cur.execute(
            "SELECT id FROM moderator WHERE moderatornaam = (%s)", (modnaam,))
        modID = create_id1(id1_list)
        cur.execute(
            "INSERT INTO beoordeling (goedkeuring, datum, tijd, moderatorid, opmerking) VALUES (%s, %s, %s, %s, %s)",
            (True, datum, tijdstip, modID, modopmerking))
        con.commit()
        cur.execute(
            "SELECT beoordelingid FROM beoordeling WHERE goedkeuring = (%s) AND datum = (%s) AND tijd = (%s) AND moderatorid = (%s) AND opmerking = (%s)",
            (True, datum, tijdstip, modID, modopmerking))
        beoordelingID = (cur.fetchone()[0])
        cur.execute(
            "UPDATE bericht SET beoordelingid = (%s) WHERE bericht.id = (%s)", (beoordelingID, berichtid)
        )
        con.commit()


        showinfo(title='Melding', message="Bericht is succesvol, en wordt geaccepteerd\nVolgend bericht wordt nu getoond")
        opmerking.delete('1.0', END)
        nieuwbericht()

        cur.close()
        con.close()


def reject():
    modnaam = comboExample.get()
    modopmerking = opmerking.get('1.0', END)
    if modnaam == '':
        showinfo(title='Error', message="Selecteer een moderator")
    elif len(modopmerking) <= 1:
        showinfo(title='Error', message="Reden geven voor afkeuren bericht")
    else:
        con = psycopg2.connect(
            host='localhost',  # De host waarop je database runt
            database='stationzuil',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='Max1803'  # Wachtwoord die je opgaf bij installatie
            # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
        )
        cur = con.cursor()
        cur.execute(
            "SELECT id FROM moderator WHERE moderatornaam = (%s)", (modnaam,))
        modID = create_id1(id1_list)
        cur.execute(
            "INSERT INTO beoordeling (goedkeuring, datum, tijd, moderatorid, opmerking) VALUES (%s, %s, %s, %s, %s)",
            (False, datum, tijdstip, modID, modopmerking))
        con.commit()
        cur.execute(
            "SELECT beoordelingid FROM beoordeling WHERE goedkeuring = (%s) AND datum = (%s) AND tijd = (%s) AND moderatorid = (%s) AND opmerking = (%s)",
            (False, datum, tijdstip, modID, modopmerking))
        beoordelingID = (cur.fetchone()[0])
        cur.execute(
            "UPDATE bericht SET beoordelingid = (%s) WHERE bericht.id = (%s)", (beoordelingID, berichtid)
        )
        con.commit()

        showinfo(title='Melding', message="Bericht is succesvol afgewezen\nVolgend bericht wordt nu getoond")
        opmerking.delete('1.0', END)
        nieuwbericht()

        cur.close()
        con.close()


def nieuwbericht():
    global berichtid
    global bericht
    con = psycopg2.connect(
        host='localhost',  # De host waarop je database runt
        database='stationzuil',  # Database naam
        user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
        password='Max1803'  # Wachtwoord die je opgaf bij installatie
        # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
    )

    cur = con.cursor()
    cur.execute(
        "SELECT bericht.id, bericht.tekst, bericht.naam, bericht.beoordelingid FROM bericht WHERE bericht.beoordelingid IS NULL ORDER BY datum")

    result = cur.fetchone()
    if result:
        naam = result[2]
        bericht = result[1].rstrip()
        berichtid = result[0]
        naamlabel2.config(text=naam)
        berichtlabel2.config(text=bericht)
    else:
        showinfo(title='Melding', message="Alle berichten zijn beoordeeld.\nApp wordt gesloten")

    cur.close()
    con.close()

hoofdscherm = Tk()
hoofdscherm.title("NS Moderator Scherm")
hoofdscherm.geometry("500x600")
hoofdscherm.config(bg='#fff700')

bericht_beoordelen = Label(hoofdscherm, text="Bericht beoordelen", font=("NS Sans", 20), bg='#0000FF', fg='#FFFFFF')
bericht_beoordelen.grid(column=0, row=0, columnspan=20, sticky=W)
bericht_beoordelen.place(x=150, y=1)

tekst = Label(hoofdscherm, text="Moderator", font=('Helvetica',12, 'bold italic'), bg='#0000FF', fg='#FFFFFF')
tekst.grid(column=0, row=3, sticky=W)
tekst.place(x=180, y=68, width=163)

comboExample = Combobox(hoofdscherm,
                        values=[
                            "Max", ], font=("NS Sans", 10), state="readonly")
comboExample.grid(column=1, row=3, sticky=W)
comboExample.place(x=180, y=90)

naamlabel = Label(hoofdscherm, text="Naam:", font=('Helvetica',12, 'bold italic'), bg='#0000FF', fg='#FFFFFF')
naamlabel.grid(column=0, row=5, sticky=W)
naamlabel.place(x=110, y=138, width=140)

berichtlabel = Label(hoofdscherm, text="Bericht:", font=('Helvetica',12, 'bold italic'), bg='#0000FF', fg='#FFFFFF')
berichtlabel.grid(column=0, row=6, sticky=W + N)
berichtlabel.place(x=280, y=138, width=140)

opmerkinglabel = Label(hoofdscherm, text="Commentaar:", font=('Helvetica',12, 'bold italic'), bg='#0000FF', fg='#FFFFFF')
opmerkinglabel.grid(column=0, row=8, sticky=W + N)
opmerkinglabel.place(x=180, y=260, width=166)

# Hier komt de echte naam te staan
naamlabel2 = Label(hoofdscherm, text='', font=('Helvetica',12, 'bold italic'), bg='white', fg='black')
naamlabel2.grid(column=1, row=5, sticky=W, columnspan=2)
naamlabel2.place(x=110, y=160, width=140)

# Hier komt hetechte bericht te staan
berichtlabel2 =Label(hoofdscherm, text='', font=('Helvetica',12, 'bold italic'), bg='white', fg='black',
                      wraplength=180)
berichtlabel2.grid(column=1, row=5, sticky=W)
berichtlabel2.place(x= 280, y=160, width=140)

# Hier wordt opmerking van de mod opgenomen
opmerking = Text(hoofdscherm, font=('Helvetica',12, 'bold italic'), width=18, height=5)
opmerking.grid(column=1, row=8, sticky=W)
opmerking.place(x=180, y=283)

acceptbutton = Button(hoofdscherm, text="Accept", font=('Helvetica',10, 'bold italic'), bg='#0000FF', fg='#FFFFFF', width=8, command=lambda: accept())
acceptbutton.grid(column=1, row=10, sticky=E)
acceptbutton.place(x=180, y=390)

rejectbutton = Button(hoofdscherm, text="Reject", font=('Helvetica',10, 'bold italic'), bg='#0000FF', fg='#FFFFFF', width=8, command=lambda: reject())
rejectbutton.grid(column=1, row=10, sticky=W)
rejectbutton.place(x=270, y=390)


nieuwbericht()
hoofdscherm.mainloop()