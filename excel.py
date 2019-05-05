#! /usr/bin/env python  
# coding=utf-8

'''  
FuncName: Excelhelper.py  
Desc: operate excel  
Author: Anderson  
Weichat: python爱好部落  
'''
import xlwt
import xlrd
import os
from xlutils.copy import copy


class WriteExcel(object):
    """  
    操作excel表格  
    写入excel：1.无文件则自动创建文件，创建新文件和新工作表  
              2.存在文件且存在指定工作表，直接操作该工作表  
              3.存在文件且不存在指定工作表，新建指定工作表并写入该表，不影响已存在工作表数据
    """

    def __init__(self, fileName, sheetName):
        self.fileName = fileName
        self.sheetName = sheetName
        self.style = self.sheetStyle()

    def sheetStyle(self):
        """  
        添加样式：  
        http://nullege.com/codes/search/xlwt.Style  
        https://xlwt.readthedocs.io/en/latest/  
        :return: 各种配置参数  
        """
        # style = xlwt.easyxf('font: color-index red, bold on')
        font = xlwt.Font()  # Create the Font
        # 字体  
        font.name = 'Times New Roman'
        # 粗体  
        # font.bold = True
        # 下划线  
        # font.underline = True
        # 斜体  
        # font.italic = True

        pattern = xlwt.Pattern()  # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN 关模式, SOLID_PATTERN 开模式, or 0x00 through 0x12
        pattern.pattern_fore_colour = 2  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...

        style = xlwt.XFStyle()  # Create the Style 初始化样式
        style.font = font  # Apply the Font to the Style 为样式设置字体
        style.pattern = pattern  # Add Pattern to Style

        return style

    def sheetValue(self, row, col, value, style=False):
        """  
        :param sheetName: 表名, fileName: 文件名, row:行, col：列, value:值, style:格式  
        :return: 对文件的指定表进行写数据操作，支持重复写  
        """
        # xls文件不存在则新创建文件和新创建工作表  
        if os.path.exists(self.fileName) == False:
            writeExcel = xlwt.Workbook()
            # 注意：如果对同一个单元格重复操作，会引发overwrite Exception，想要取消该功能，需要在添加工作表时指定为可覆盖，所以在打开时加cell_overwrite_ok=True解决  
            writeExcel.add_sheet(self.sheetName, cell_overwrite_ok=True)
            # 这里只能保存扩展名为xls的，xlsx的格式不支持  
            writeExcel.save(self.fileName)
        else:
            # open existed xls file 需要 newWb = copy('fileName')  
            # 注意添加参数formatting_info=True，得以保存之前数据的格式  
            readExcel_old = xlrd.open_workbook(self.fileName, formatting_info=True)
            # 判断sheetName的索引，将数据写入该表  
            sheetNames = readExcel_old.sheet_names()
            readExcel_new = copy(readExcel_old)
            # 判断是否存在sheetName，不存在则新建该工作表，不影响其他表数据  
            if self.sheetName not in sheetNames:
                readExcel_new.add_sheet(self.sheetName)
                readExcel_new.save(self.fileName)
                readExcel_new = xlrd.open_workbook(self.fileName, formatting_info=True)
                sheetNames = readExcel_new.sheet_names()
                readExcel_new = copy(readExcel_new)
            else:
                pass
            sheetNameIndex = sheetNames.index(self.sheetName)
            writeExcel = readExcel_new.get_sheet(sheetNameIndex)

            if style:
                writeExcel.write(row, col, value, self.style)
            else:
                writeExcel.write(row, col, value)
                # 这里只能保存扩展名为xls的，xlsx的格式不支持
            readExcel_new.save(self.fileName)


class ReadExcel(object):
    def __init__(self, fileName, sheetName):
        self.fileName = fileName
        self.sheetName = sheetName
        self.sheets = xlrd.open_workbook(fileName, formatting_info=True)
        self.tables = self.sheets.sheet_by_name(self.sheetName)
        self.handele = dict([(sheetName, self.sheets.sheet_by_name(sheetName))
                             for sheetName in self.sheets.sheet_names()])

        # 获取整行的值
    def sheetRowValue(self, row=0):
        if self.sheetName not in self.handele: return None
        return self.tables.row_values(row)

        # 获取整列的值
    def sheetColValue(self, col=0):
        if self.sheetName not in self.handele: return None
        return self.tables.row_values(col)

        # 获取所有表的名称
    def sheetNames(self):
        return self.sheets.sheet_names()

        # 获取单元格的值
    def sheetCellValue(self, row, col):
        if self.sheetName not in self.handele: return None
        return self.tables.cell(row, col).value

        # 获取工作表的行数
    def sheetRowNum(self):
        if self.sheetName not in self.handele: return None
        return self.tables.nrows

        # 获取工作表的列数
    def sheetColNum(self):
        if self.sheetName not in self.handele: return None
        return self.tables.ncols


if __name__ == "__main__":
    fileName = "helper.xlsx"
    sheetName = "Sheet1"

    OpWrite = WriteExcel(fileName, sheetName)
    style = True
    # print "Write new values ok!"
    # print "row    col    value"
    for row in range(10):
        col = row
        value = "anderson"
        OpWrite.sheetValue(row, col, value, style)
        # print "%2s %6s %12s"%(row,col,value)

    OpRead = ReadExcel(fileName, sheetName)
    for i in range(OpRead.sheetRowNum()):
        print(OpRead.sheetRowValue(i))

    print(OpRead.sheetRowValue(1))
    print(OpRead.sheetColValue(2))
    print(OpRead.sheetNames())
    print(OpRead.sheetCellValue(2, 2))
    print(OpRead.sheetRowNum())
    print(OpRead.sheetColNum())
