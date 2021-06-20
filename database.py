"""
Copyright (C) 2021  Berat Gökgöz

This file is a part of Timetable project.

Timetable is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any
later version.

Timetable is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import psycopg2 as sql
import pandas as pd
import json
import random as rd
from datetime import datetime as dt
from datetime import timedelta

SINGLEQUOTE = "'"
ESCAPEDSINGLEQUOTE = "\\'"

class Connection:

    def __init__(self):
        """Connects to the database."""
        f = open("./secret/dbSecretInfo.json", "r")
        dbSecretInfo = json.load(f)
        f.close()
        self.con = sql.connect(**dbSecretInfo)
        self.cur = self.con.cursor()

    def getPrefixes(self):
        """Gets prefixes from SQL Database."""
        self.cur.execute("SELECT svid, pf FROM prefixes")
        prefixes = self.cur.fetchall()
        return dict(prefixes)


    def getPrefix(self, svid):
        """Gets prefix of the server with given ID from database."""
        try:
            self.cur.execute(f"SELECT pf FROM prefixes WHERE svid = {svid}")
        except:
            self.refresh()
            self.cur.execute(f"SELECT pf FROM prefixes WHERE svid = {svid}")
        resp = self.cur.fetchall()
        return resp[0][0]


    def addServer(self, svid, pf, lang):
        """Adds a server with its prefix to database."""
        try:
            self.cur.execute(f"INSERT INTO prefixes(svid, pf, lang) VALUES ({svid},'{pf.replace(SINGLEQUOTE,ESCAPEDSINGLEQUOTE)}', '{lang}')")
        except:
            self.refresh()
            self.cur.execute(f"INSERT INTO prefixes(svid, pf, lang) VALUES ({svid},'{pf.replace(SINGLEQUOTE,ESCAPEDSINGLEQUOTE)}', '{lang}')")
        self.con.commit()


    def changePrefix(self, svid, pf):
        """Changes a prefix of a server database."""
        try:
            self.cur.execute(f"UPDATE prefixes SET pf = '{pf.replace(SINGLEQUOTE,ESCAPEDSINGLEQUOTE)}' WHERE svid = {svid}")
        except:
            self.refresh()
            self.cur.execute(f"UPDATE prefixes SET pf = '{pf.replace(SINGLEQUOTE,ESCAPEDSINGLEQUOTE)}' WHERE svid = {svid}")
        self.con.commit()


    def delServer(self, svid):
        """Deletes a server from prefixes table in the database."""
        try:
            self.cur.execute(f"DELETE FROM prefixes WHERE svid = {svid}")
        except:
            self.refresh()
            self.cur.execute(f"DELETE FROM prefixes WHERE svid = {svid}")
        self.con.commit()

    def changeLang(self, svid, lang):
        """Changes the language preference for the server."""
        try:
            self.cur.execute(f"UPDATE prefixes SET lang = '{lang}' WHERE svid = {svid}")
        except:
            self.refresh()
            self.cur.execute(f"UPDATE prefixes SET lang = '{lang}' WHERE svid = {svid}")
        self.con.commit()

    def getLang(self, svid):
        """Returns the language for that server."""
        try:
            self.cur.execute(f"SELECT lang FROM prefixes WHERE svid = {svid}")
        except:
            self.refresh()
            self.cur.execute(f"SELECT lang FROM prefixes WHERE svid = {svid}")
        resp = self.cur.fetchall()
        return resp[0][0]

    def getTables(self):
        """Gets all the tables from the database and converts them to Pandas DataFrames."""
        self.cur.execute("SELECT tableid FROM tabledata")
        response = self.cur.fetchall()
        tableDfs = []
        for tableid in response:
            self.cur.execute(f"SELECT * FROM t{tableid[0]}")
            tableResp = self.cur.fetchall()
            columns = [i[0] for i in self.cur.description]
            tableDfs.append(pd.DataFrame(tableResp, columns=columns))
        return tableDfs


    def getTableIds(self):
        """Gets IDs of all tables."""
        self.cur.execute("SELECT tableid FROM tabledata")
        response = self.cur.fetchall()
        return tuple(map(lambda x: x[0], response))


    def getTable(self, tableid):
        """Gets the table with given ID as Pandas.DataFrame."""
        self.cur.execute(f"SELECT * FROM t{tableid}")
        tableResp = self.cur.fetchall()
        columns = [i[0] for i in self.cur.description]
        return pd.DataFrame(tableResp, columns=columns)


    def addTable(self, tabledf, channelid, password, mention):
        """Adds a table to the database by given Pandas.DataFrame, channel id, password and mention."""
        tabledict = tabledf.to_dict("records")
        self.cur.execute("SELECT tableid FROM tabledata")
        tableids = self.cur.fetchall()
        while True:
            randomid = rd.randint(100000,999999)
            if (randomid,) in tableids:
                continue
            else:
                break
        self.cur.execute(f"INSERT INTO tabledata(tableid, channel, password, mention) \
VALUES ({randomid},{channelid},'{password.replace(SINGLEQUOTE,ESCAPEDSINGLEQUOTE)}', '{mention.replace(SINGLEQUOTE,ESCAPEDSINGLEQUOTE)}')")
        columnNames = tuple(map(lambda x: f"t{x}", tabledict[0].keys()))
        sqlQuery1 = []
        for time in columnNames:
            sqlQuery1.append(time.strip()+" VARCHAR")
        self.cur.execute(f"CREATE TABLE t{randomid} ({', '.join(sqlQuery1)})")

        for lesson in tabledict:
            sqlQuery2 = list(map(lambda x: f"'{x}'", tuple(lesson.values())))
            self.cur.execute(f"INSERT INTO t{randomid} ({', '.join(columnNames)}) VALUES ({', '.join(sqlQuery2)})")
        self.con.commit()
        return randomid


    def delTable(self,tableid):
        """Deletes the table with given id from the database."""
        self.cur.execute(f"DELETE FROM tabledata WHERE tableid = {tableid}")
        self.cur.execute(f"DROP TABLE t{tableid}")
        self.con.commit()


    def getTableInfos(self, tableid):
        """Returns a dict of channel id and password of the table with given id."""
        self.cur.execute(f"SELECT channel, password, mention FROM tabledata WHERE tableid = {tableid}")
        resp = self.cur.fetchall()
        returnDict={"channel":resp[0][0], "password":resp[0][1], "mention":resp[0][2]}
        return returnDict


    def changeTableInfo(self, tableid, channelid, password, mention):
        """Changes the table info(channel id and password) of the table."""
        self.cur.execute(f"UPDATE tabledata SET channel = {channelid} WHERE tableid = {tableid}")
        self.cur.execute(f"UPDATE tabledata SET password = '{password.replace(SINGLEQUOTE,ESCAPEDSINGLEQUOTE)}' WHERE tableid = {tableid}")
        self.cur.execute(f"UPDATE tabledata SET mention = '{mention.replace(SINGLEQUOTE, ESCAPEDSINGLEQUOTE)}' WHERE tableid = {tableid}")
        self.con.commit()


    def run(self, command):
        """Runs the given command. It's made to use with eval command."""
        self.cur.execute(command)
        self.con.commit()
        resp = self.cur.fetchall()
        return resp


    def getReminders(self):
        """Gets the reminder from the database."""
        self.cur.execute("SELECT * FROM reminders")
        resp = self.cur.fetchall()
        dictionary = {}
        for r in resp:
            dictionary[r[0]] = (r[1], r[2], r[3], r[4])
        return dictionary


    def addReminder(self, date, time, channel, event):
        """Adds a reminder to the database."""
        self.cur.execute("SELECT rid FROM reminders")
        reminderIds = self.cur.fetchall()
        while True:
            randomid = rd.randint(100000,999999)
            if (randomid,) in reminderIds:
                continue
            else:
                break
        self.cur.execute(f"INSERT INTO reminders VALUES({randomid}, '{date}', '{time}', {channel}, '{event.replace(SINGLEQUOTE, ESCAPEDSINGLEQUOTE)}')")
        self.con.commit()
        return randomid


    def delReminder(self, rid):
        """Deletes the reminder with the given ID from the database."""
        self.cur.execute(f"DELETE FROM reminders WHERE rid = {rid}")
        self.con.commit()


    # Will be used when bot is approved in top.gg
    def addVotedUser(self, uid):
        """Adds a voted user for next 5 days if not in database."""
        self.cur.execute(f"DELETE FROM votes WHERE uid={uid}")
        timestamp = dt.utcnow() + timedelta(days=5)
        timestamp = int(timestamp.timestamp())
        self.cur.execute(f"INSERT INTO votes VALUES ({uid}, {timestamp})")
        self.con.commit()


    def checkVotedUser(self, uid):
        """Checks a user if voted in last 5 days."""
        self.cur.execute(f"SELECT validuntil FROM votes WHERE uid={uid}")
        resp = self.cur.fetchall()
        if len(resp) < 1:
            return False
        if resp[0][0] >= int(dt.utcnow().timestamp()):
            return True
        elif resp[0][0] < int(dt.utcnow().timestamp()):
            return False
    def refresh(self):
        self.con.close()
        f = open("./secret/dbSecretInfo.json", "r")
        dbSecretInfo = json.load(f)
        f.close()
        self.con = sql.connect(**dbSecretInfo)
        self.cur = self.con.cursor()

    def disconnect(self):
        """Disconnects."""
        self.con.close()
