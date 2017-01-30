import sys
import cx_Oracle

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QWidget):
    def execSql(self):
        con = cx_Oracle.connect('o_cst/o_cst@fmml')
        cur = con.cursor()
        print(self.sqlEdit.toPlainText())
        #cur.execute("""select 1 * level col1, 2 * level col2, 3 * level col3, 4 * level col4, 5 * level col5 from dual connect by level <= 10""")
        cur.execute(self.sqlEdit.toPlainText())
        data = cur.fetchall()

        colcnt = len(data[0])
        rowcnt = len(data)
        self.tablewidget.clear()
        self.tablewidget.setColumnCount(colcnt)
        self.tablewidget.setRowCount(rowcnt)

        #ヘッダー設定
        coldata = cur.description
        horHeaders = []
        for c in coldata:
            horHeaders.append(c[0])
            print(c[0])

        self.tablewidget.setHorizontalHeaderLabels(horHeaders)

        #テーブルの中身作成
        for n in range(rowcnt):
            for m in range(colcnt):
                item = QTableWidgetItem(str(data[n][m]))
                self.tablewidget.setItem(n, m, item)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.calcButton = QPushButton("&Exec")
        self.calcButton.clicked.connect(self.execSql)

        self.sqlEdit = QTextEdit()
        self.sqlEdit.setText("""select 1 * level col1, 2 * level col2, 3 * level col3, 4 * level col4, 5 * level col5 from dual connect by level <= 10""")
        self.Highlighter = Highlighter(self.sqlEdit.document())



        self.tablewidget = QTableWidget(10, 10)
        sizePolicy1 = self.sqlEdit.sizePolicy()
        sizePolicy2 = self.tablewidget.sizePolicy()
        sizePolicy1.setVerticalStretch(1)
        sizePolicy2.setVerticalStretch(2)
        self.sqlEdit.setSizePolicy(sizePolicy1)
        self.tablewidget.setSizePolicy(sizePolicy2)

        vLayout = QVBoxLayout()
        vLayout.addWidget(QLabel("sql"))
        vLayout.addWidget(self.sqlEdit)
        vLayout.addWidget(self.calcButton)
        vLayout.addWidget(self.tablewidget)

        self.setLayout(vLayout)
        self.setWindowTitle("execSql")

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)

        keywordPatterns = ["\\bselect\\b", "\\bfrom\\b", "\\bwhere\\b",
                "\\bgroup\\b", "\\bby\\b", "\\border\\b",
                "\\bconnect\\b", "\\bpartition\\b", "\\bover\\b",
                "\\bsum\\b", "\\blevel\\b", "\\bkeep\\b",
                ]

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegExp("\".*\""), quotationFormat))

        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(Qt.blue)
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
