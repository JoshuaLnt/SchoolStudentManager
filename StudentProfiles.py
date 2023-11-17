import mysql.connector

DEBUG = False
MYDB = None

def debugToggle(bool=True):
    global DEBUG
    if bool is None: 
        DEBUG = not DEBUG
    else: DEBUG = bool
    s = str(DEBUG)
    print("\n--------------------")
    print("Debugging Mode enabled: "+s)
    print("--------------------\n")

#host and user can only be changed manually
def init(pw=None):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password=pw,
            port=3306,
            database="studentdb"
        )
    except UnboundLocalError:
        mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password=pw,
            port=3306
        )
    global MYDB
    MYDB = mydb
    
def checkDb(pw):
    init(pw)
    mydb = MYDB
    cursor = MYDB.cursor(buffered=True)
    cursor.execute("SHOW DATABASES")

    datab = []
    for x in cursor:
        x = str(x).strip('(),\'')
        datab.append(x)
        if'studentdb' in datab:
            pass
    for y in datab:
        if DEBUG: print(y)
    if('studentdb' not in datab):
        if DEBUG: print("studentdb not found")
        try:
            cursor.execute("CREATE DATABASE studentdb")
            mydb.commit()
            pass
        except Exception as err:  
            print(err)
    else:
        if DEBUG: print("studentdb found")
        pass
    mydb.close()

def checkTable(pw):
    init(pw)
    mydb = MYDB
    cursor = MYDB.cursor(buffered=True)

    cursor.execute("SHOW TABLES")
    datat = []

    for z in cursor:
        z = str(z).strip('(),\'')
        datat.append(z)
        if DEBUG: print("table " + str(z) + " found")
    if 'students' not in datat:
            if DEBUG: print("table not found")
            try:
                cursor.execute("CREATE TABLE students (lastname VARCHAR(255), firstname VARCHAR(255), lang VARCHAR(255), age INT, gradelevel VARCHAR(255), date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
                mydb.commit()
            except Exception as err:  
                print(err)
    mydb.close()

def checkAll(pw):
    checkDb(pw)
    checkTable(pw)
    init(pw)
    cursor = MYDB.cursor(buffered=True)
    cursor.execute("SHOW TABLES")
    

def registerStudent(pw, firstname="", lastname="", language="", age=0, gradelevel="No class yet"):
    checkAll(pw)
    init(pw)
    mydb = MYDB
    cursor = MYDB.cursor(buffered=True)

    sql = "INSERT INTO students (lastname, firstname, lang, age, gradelevel) VALUES (%s, %s, %s, %s, %s)"
    val = (lastname, firstname, language, age, gradelevel)

    cursor.execute(sql, val)
    mydb.commit()

    print(cursor.rowcount, "record inserted.")
    cursor.execute("SELECT * FROM students")
    res = cursor.fetchall()
    for x in res:
        print(x)
    mydb.close()

def findStudents(pw, firstname="", lastname="", language="", age=0,  gradelevel=""):
    checkAll(pw)
    init(pw)
    mydb = MYDB
    cursor = MYDB.cursor(buffered=True)
    cursor.execute("SHOW TABLES")
    sql = "SELECT * FROM students WHERE firstname = %s OR lastname = %s OR lang = %s OR age = %s OR gradelevel =%s"
    val = (firstname, lastname, language, age, gradelevel)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    mydb.close()
    return result

def editEntry(pw, firstname="", lastname="", language="",  gradelevel=""):
    checkAll(pw)
    init(pw)
    mydb = MYDB
    cursor = MYDB.cursor(buffered=True)
    cursor.execute("SHOW TABLES")
    sql = "SELECT * FROM students WHERE firstname =%s AND lastname =%s AND lang =%s AND gradelevel =%s"
    val = (firstname, lastname, language, gradelevel)
    cursor.execute(sql, val)
    mydb.close()

def deleteEntry(pw, firstname="", lastname="", language="",  gradelevel=""):
    checkAll(pw)
    init(pw)
    mydb = MYDB
    cursor = MYDB.cursor(buffered=True)
    cursor.execute("SHOW DATABASES")
    cursor.execute("SHOW TABLES")
    sql = "DELETE FROM students WHERE firstname =%s AND lastname =%s AND lang =%s AND gradelevel =%s"
    val = (firstname, lastname, language, gradelevel)
    cursor.execute(sql, val)
    mydb.commit()
    print("\n--------------------")
    print("Entries containing \nLast Name: "+lastname+" \nFirst Name: "+firstname+" \nLanguage: "+language+" \nClass: "+gradelevel+" \nhave been deleted!")
    print(cursor.rowcount, "record(s) deleted in total")
    print("--------------------\n")
    mydb.close()
    
    

#debugToggle()

registerStudent("1234", "testBoy", "testFam", "Fr", 10)
deleteEntry("1234", "testBoy", "testFam", "Fr", "No class yet")
print(findStudents("1234", "testBoy", "testFam", "Fr", 10))

