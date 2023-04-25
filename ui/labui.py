import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import Qt
import pymysql
import pymysql.cursors

connection = pymysql.connect(host='localhost', user='root', password='catcat',
                             database='dblab1', charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
dbname = 'dblab1'

# NOTE general functions


def execQry(form, qry: str):
    with connection.cursor() as cursor:
        try:
            cursor.execute(qry)
            form.sqlExecResult.setText("Result: Success.")
            return cursor.fetchall()  # type: ignore
        except Exception as e:
            form.sqlExecResult.setText(str(e))
            return []


def getTableCols(tablename):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '{}' AND table_schema = 'dblab1';".format(tablename))
        result = cursor.fetchall()
        rtn = []
        print("Parse column name references: ", result)
        for i in result:
            rtn.append(i.get('COLUMN_NAME'))
        return rtn


def getTableColsByItem(item) -> list:
    result = []
    for i in item:
        result.append(i)
    print("Col Parsed to: ", result)
    return result

# NOTE right panel part


def alterDB(form, new_dbname: str):
    global connection
    try:
        connection = pymysql.connect(host='localhost', user='root', password='catcat',
                                     database=new_dbname, charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        global dbname
        dbname = new_dbname
        form.dbStatusLabel.setText('Current DB: ' + new_dbname)
        refreshTables(form, new_dbname)
    except:
        connection = pymysql.connect(host='localhost', user='root', password='catcat',
                                     database=dbname, charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)


def refreshTables(form, dbname):
    result = execQry(form, 'SHOW TABLES FROM ' + dbname)
    tblname_merged = [list(t.values())[0] for t in result]
    form.tableCBox1.clear()
    form.tableCBox2.clear()
    form.tableCBox3.clear()
    form.tableCBox1.addItems(tblname_merged)
    form.tableCBox2.addItems(tblname_merged)
    form.tableCBox3.addItems(tblname_merged)


def loadtoRView(form, tablename: str, view, limits: int):
    content = execQry(form, "select * from " + tablename +
                      " limit {}".format(limits))
    table_column = getTableColsByItem(content[0])

    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(table_column)
    for row, linedata in enumerate(content):
        for col, colstr in enumerate(table_column):
            itemdata = linedata[colstr]
            item = QStandardItem(
                str(itemdata)) if itemdata != None else QStandardItem('')
            model.setItem(row, col, item)

    view.setModel(model)
    view.horizontalHeader().setStretchLastSection(True)
    view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


# NOTE main panel part


def constructSql(form):
    ct1 = ['' for _ in range(0, 8)]
    if form.IDChk.checkState() == Qt.CheckState.Checked:
        ct1[0] = form.IDEdit.text()
    if form.nameChk.checkState() == Qt.CheckState.Checked:
        ct1[1] = form.nameEdit.text()
    if form.ageChk.checkState() == Qt.CheckState.Checked:
        ct1[2] = form.ageAEdit.text()
        ct1[3] = form.ageBEdit.text()
    if form.genderChk.checkState() == Qt.CheckState.Checked:
        ct1[4] = form.genderEdit.text()
    if form.classChk.checkState() == Qt.CheckState.Checked:
        ct1[5] = form.classEdit.text()
    print("Constructed ct1: \n", ct1)

    ct2 = ['' for _ in range(0, 3)]
    if form.courseIDChk.checkState() == Qt.CheckState.Checked:
        ct2[0] = form.courseIDEdit.text()
    if form.coursenameChk.checkState() == Qt.CheckState.Checked:
        ct2[1] = form.coursenameEdit.text()
    if form.creditChk.checkState() == Qt.CheckState.Checked:
        ct2[2] = form.creditEdit.text()
    print("Constructed ct2: \n", ct2)

    ct3 = ['' for _ in range(0, 2)]
    if form.scoreChk.checkState() == Qt.CheckState.Checked:
        ct3[0] = form.scoreAEdit.text()
        ct3[1] = form.scoreBEdit.text()
    print("Constructed ct3: \n", ct3)

    querySql = genSQLcmd(ct1, ct2, ct3)
    form.sqlDisplay.clear()
    form.sqlDisplay.appendPlainText(querySql)


def genSQLcmd(c1: list, c2: list, c3: list) -> str:
    act1, act2, act3 = False, False, False
    for i in c1:
        if (i != ''):
            act1 = True
    for i in c2:
        if (i != ''):
            act2 = True
    for i in c3:
        if (i != ''):
            act3 = True

    cs1 = []
    if c1[0] != '':
        cs1.append("student.Sid like '{}'".format(c1[0]))
    if c1[1] != '':
        cs1.append("Sname like '{}'".format(c1[1]))
    if c1[2] != '':
        cs1.append('Sage >= {}'.format(c1[2]))
    if c1[3] != '':
        cs1.append('Sage <= {}'.format(c1[3]))
    if c1[4] != '':
        cs1.append("Ssex = '{}'".format(c1[4]))
    if c1[5] != '':
        cs1.append("SClass like '{}'".format(c1[5]))

    cs2 = []
    if c2[0] != '':
        cs2.append("course.Cid like '{}'".format(c2[0]))
    if c2[1] != '':
        cs2.append("Cname like '{}'".format(c2[1]))
    if c2[2] != '':
        cs2.append("Credit = '{}'".format(c2[2]))

    cs3 = []
    if c3[0] != '':
        cs3.append("Score >= '{}'".format(c3[0]))
    if c3[1] != '':
        cs3.append("Score <= '{}'".format(c3[1]))

    base = ''
    # base student
    if act1 == True and act2 == False and act3 == False:
        base = "SELECT * FROM student"
    if act1 == True and act2 == True and act3 == False:
        base = "SELECT * FROM student JOIN course"
    if act1 == True and act2 == False and act3 == True:
        base = "SELECT student.*, score.Cid, score.Score FROM student JOIN score ON student.Sid = score.Sid"
    if act1 == True and act2 == True and act3 == True:
        base = "SELECT student.*, course.*, score.Score FROM student JOIN course JOIN score " \
               "ON student.Sid = score.Sid and course.Cid = score.Cid"
    # base course
    if act1 == False and act2 == True and act3 == False:
        base = "SELECT * FROM course"
    if act1 == False and act2 == True and act3 == True:
        base = "SELECT course.*, score.Sid, score.Score FROM course JOIN score ON course.Cid = score.Cid"
    # base score
    if act1 == False and act2 == False and act3 == True:
        base = "SELECT * FROM score"

    if cs1 == [] and cs2 == [] and cs3 == []:
        return base
    else:
        return base + " WHERE " + " AND ".join(
            ["(" + s + ")" for s in cs1] + ["(" + s + ")" for s in cs2] + ["(" + s + ")" for s in cs3]) 


def procSqlResult(form, result):
    # print("Result: ", result)

    if result != None and result != () and result != []:
        tablecol = getTableColsByItem(result[0])
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(tablecol)
        for row, linedata in enumerate(result):  # type: ignore
            for col, colstr in enumerate(tablecol):
                itemdata = linedata[colstr]
                item = QStandardItem(
                    str(itemdata)) if itemdata != None else QStandardItem('')
                model.setItem(row, col, item)

        form.sqlResult.setModel(model)
        form.sqlResult.horizontalHeader().setStretchLastSection(True)
        form.sqlResult.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    elif result == () or result == None:
        form.sqlExecResult.setText("Warning: Empty result!")
        return
    else:
        return


def main():
    Form, Window = uic.loadUiType("./main/ui/labui.ui")
    demoapp = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()

    # init right panel
    form.dbStatusLabel.setText('Current DB: dblab1')
    form.dbSelCBox.addItems([list(_db.values())[0]
                            for _db in execQry(form, 'SHOW DATABASES')])
    refreshTables(form, dbname)
    form.dbSelBtn.clicked.connect(
        lambda: alterDB(form, form.dbSelCBox.currentText()))

    # init btns
    form.constructBtn.clicked.connect(lambda: constructSql(form))
    form.loadBtn_Table1.clicked.connect(
        lambda: loadtoRView(form, form.tableCBox1.currentText(), form.tableView_Table1, 5000))
    form.loadBtn_Table2.clicked.connect(
        lambda: loadtoRView(form, form.tableCBox2.currentText(), form.tableView_Table2, 5000))
    form.loadBtn_Table3.clicked.connect(
        lambda: loadtoRView(form, form.tableCBox3.currentText(), form.tableView_Table3, 5000))
    form.execBtn.clicked.connect(
        lambda: procSqlResult(form, execQry(form, form.sqlDisplay.toPlainText())))

    sys.exit(demoapp.exec())


if __name__ == "__main__":
    main()
