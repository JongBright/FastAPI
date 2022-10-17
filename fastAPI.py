import uvicorn
from fastapi import FastAPI
import sqlite3



#connect to database
cur = sqlite3.connect('database.db')
#create table
cur.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, site TEXT UNIQUE, password TEXT)")




app = FastAPI()

#home
@app.get("/")
async def root():
    return "Database server running, port 5049 ..."

@app.get("/db-api/")
async def api():
    return "Database api running ..."



#get all passwords
@app.get("/db-api/passwords/")
async def getPasswords():
    data = cur.execute("SELECT * FROM passwords").fetchall()
    if data:
        passwords = []
        for d in data:
            item = {"id":d[0], "site":d[1], "password":d[2]}
            passwords.append(item)
        return {"status":"success", "message":"passwords fetch successful!", "data":passwords}
    return {"status":"error", "message":"passwords not found!"}


#get a specific password
@app.get("/db-api/passwords/password")
async def getPassword(site:str):
    data = cur.execute("SELECT * FROM passwords WHERE site = ?", (site,)).fetchone()
    password = {"id":data[0], "site":data[1], "password":data[2]}
    if password:
        return {"status":"success", "message":"password fetch successful!", "data":password}
    return {"status":"error", "message":"password not found!"}


#add a password
@app.post("/db-api/passwords/add-password/")
async def addPassword(site:str, new_password:str):
    cur.execute("INSERT INTO passwords VALUES (NULL,?,?)", (site, new_password))
    cur.commit()
    new_data = {"id":"","site":site,"password":new_password}
    if new_data:
        return {"status":"success", "message":"password added successfully!", "data":new_data}
    return {"status":"error", "message":"password not added!"}


#update a password
@app.put("/db-api/passwords/update-password/")
async def addPassword(site:str, updated_password:str):
    cur.execute("UPDATE passwords SET password = ? WHERE site = ?", (updated_password, site))
    cur.commit()
    new_data = {"id":"","site":site,"password":updated_password}
    if new_data:
        return {"status":"success", "message":"password updated successfully!", "data":new_data}
    return {"status":"error", "message":"password not updated!"}


#delete a password
@app.delete("/db-api/passwords/delete-password/")
async def addPassword(site:str):
    cur.execute("DELETE FROM passwords WHERE site = ?", (site,))
    cur.commit()
    return {"status":"success", "message":"password deleted successfully!", "data":""}












if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
