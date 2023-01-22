import random
from tkinter import *
from datetime import date, datetime
from tkinter.messagebox import showinfo
import psycopg2
import pandas as pd
import pandas.io.sql as psql
import time
import requests
import json


def tonen(stad):
    r = requests.get(f'https://weerlive.nl/api/json-data-10min.php?key=bed022b9d9&locatie={stad}')
    weer_data = json.loads(r.text)
    return weer_data["liveweer"][0]


def bericht_ophalen():
    connection = psycopg2.connect(dbname='stationzuil', user='postgres', password='Max1803')
    berichten = pd.read_sql(
        "SELECT tekst, naam FROM bericht tekst WHERE tekst.tijd IS NOT NULL AND tekst.datum IS NOT NULL"
        " ORDER BY tekst.datum DESC, tekst.tijd DESC LIMIT 5", connection)
    return berichten


print(bericht_ophalen())


def station_naam():
    con = psycopg2.connect(
        host='localhost',  # De host waarop je database runt
        database='stationzuil',  # Database naam
        user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
        password='Max1803'  # Wachtwoord die je opgaf bij installatie
        # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
    )
    cur = con.cursor()
    cur.execute("SELECT station_city FROM bericht tekst WHERE tekst.tijd IS NOT NULL AND tekst.datum IS NOT NULL "
                "ORDER BY tekst.datum DESC, tekst.tijd DESC LIMIT 1")
    locatie = cur.fetchone()
    return locatie


def faciliteit_fiets():
    con = psycopg2.connect(
        host='localhost',  # De host waarop je database runt
        database='stationzuil',  # Database naam
        user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
        password='Max1803'  # Wachtwoord die je opgaf bij installatie
        # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
    )
    cur = con.cursor()
    cur.execute("SELECT station_city FROM bericht tekst WHERE tekst.tijd IS NOT NULL AND tekst.datum IS NOT NULL "
                "ORDER BY tekst.datum DESC, tekst.tijd DESC LIMIT 1")
    locatie = cur.fetchone()

    cur = con.cursor()
    cur.execute("SELECT ov_bike, elevator, toilet, park_and_ride "
                "FROM station_service Alkmaar WHERE station_city = (%s)", locatie)
    stationid = cur.fetchone()
    x = {
        'Fiets': stationid[0],
        'Lift': stationid[1],
        'Toilet': stationid[2],
        'Park&Ride': stationid[3]
    }

    if (x["Fiets"]):
        return "Fiets"


def faciliteit_lift():
    con = psycopg2.connect(
        host='localhost',  # De host waarop je database runt
        database='stationzuil',  # Database naam
        user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
        password='Max1803'  # Wachtwoord die je opgaf bij installatie
        # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
    )
    cur = con.cursor()
    cur.execute("SELECT station_city FROM bericht tekst WHERE tekst.tijd IS NOT NULL AND tekst.datum IS NOT NULL "
                "ORDER BY tekst.datum DESC, tekst.tijd DESC LIMIT 1")
    locatie = cur.fetchone()

    cur = con.cursor()
    cur.execute("SELECT ov_bike, elevator, toilet, park_and_ride "
                "FROM station_service Alkmaar WHERE station_city = (%s)", locatie)
    stationid = cur.fetchone()
    x = {
        'Fiets': stationid[0],
        'Lift': stationid[1],
        'Toilet': stationid[2],
        'Park&Ride': stationid[3]
    }

    if (x["Lift"]):
        return "Lift"


def faciliteit_toilet():
    con = psycopg2.connect(
        host='localhost',  # De host waarop je database runt
        database='stationzuil',  # Database naam
        user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
        password='Max1803'  # Wachtwoord die je opgaf bij installatie
        # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
    )
    cur = con.cursor()
    cur.execute("SELECT station_city FROM bericht tekst WHERE tekst.tijd IS NOT NULL AND tekst.datum IS NOT NULL "
                "ORDER BY tekst.datum DESC, tekst.tijd DESC LIMIT 1")
    locatie = cur.fetchone()

    cur = con.cursor()
    cur.execute("SELECT ov_bike, elevator, toilet, park_and_ride "
                "FROM station_service Alkmaar WHERE station_city = (%s)", locatie)
    stationid = cur.fetchone()
    x = {
        'Fiets': stationid[0],
        'Lift': stationid[1],
        'Toilet': stationid[2],
        'Park&Ride': stationid[3]
    }

    if (x["Toilet"]):
        return "Toilet"


def faciliteit_park():
    con = psycopg2.connect(
        host='localhost',  # De host waarop je database runt
        database='stationzuil',  # Database naam
        user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
        password='Max1803'  # Wachtwoord die je opgaf bij installatie
        # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
    )
    cur = con.cursor()
    cur.execute("SELECT station_city FROM bericht tekst WHERE tekst.tijd IS NOT NULL AND tekst.datum IS NOT NULL "
                "ORDER BY tekst.datum DESC, tekst.tijd DESC LIMIT 1")
    locatie = cur.fetchone()

    cur = con.cursor()
    cur.execute("SELECT ov_bike, elevator, toilet, park_and_ride "
                "FROM station_service Alkmaar WHERE station_city = (%s)", locatie)
    stationid = cur.fetchone()
    x = {
        'Fiets': stationid[0],
        'Lift': stationid[1],
        'Toilet': stationid[2],
        'Park&Ride': stationid[3]
    }

    if (x["Park&Ride"]):
        return "Park&Ride"


print(faciliteit_fiets())
print(faciliteit_lift())
print(faciliteit_toilet())
print(faciliteit_park())

weer_data = tonen(station_naam())

hoofdscherm = Tk()
hoofdscherm.title("Stationshalscherm")
hoofdscherm.geometry("950x600")
hoofdscherm.configure(bg='#fff700')
stad_naam = Label(master=hoofdscherm,
                  text=(station_naam()),
                  background='#0000cc',
                  foreground='#FFFFFF',
                  font=('Helvetica', 16, 'bold italic'),
                  width=74,
                  height=3)
stad_naam.place(x=150, y=0)

labelBericht = Label(master=hoofdscherm,
                     text='Aanwezige faciliteiten:',
                     foreground='#FFFFFF',
                     background='#0000cc',
                     font=('Helvetica', 12, 'bold italic'))
labelBericht.place(x=150, y=154)

labelBericht = Label(master=hoofdscherm,
                     text=faciliteit_fiets(),
                     foreground='#000000',
                     background='#fff700',
                     font=('Helvetica', 12, 'bold italic'))
labelBericht.place(x=150, y=185)

labelBericht = Label(master=hoofdscherm,
                     text=faciliteit_lift(),
                     foreground='#000000',
                     background='#fff700',
                     font=('Helvetica', 12, 'bold italic'))
labelBericht.place(x=250, y=185)

labelBericht = Label(master=hoofdscherm,
                     text=faciliteit_toilet(),
                     foreground='#000000',
                     background='#fff700',
                     font=('Helvetica', 12, 'bold italic'))
labelBericht.place(x=350, y=185)

labelBericht = Label(master=hoofdscherm,
                     text=faciliteit_park(),
                     foreground='#000000',
                     background='#fff700',
                     font=('Helvetica', 12, 'bold italic'))
labelBericht.place(x=450, y=185)

actuele_berichten = Label(master=hoofdscherm,
                          text=(bericht_ophalen()),
                          background='#fff700',
                          foreground='#000000',
                          font=('Helvetica', 16, 'bold italic'),
                          width=80,
                          height=6)
actuele_berichten.place(x=150, y=400)

nsLogo = Label(master=hoofdscherm,
               text=f"De temperatuur is momenteel {weer_data['temp']} graden\n{weer_data['verw']}",
               background='#0000cc',
               foreground='#000000',
               font=('Helvetica', 16, 'bold italic'),
               width=74,
               height=3)
nsLogo.place(x=150, y=75)

naam = Label(master=hoofdscherm, )
naam.place(x=150, y=245, width=650, height=30)

hoofdscherm.mainloop()
