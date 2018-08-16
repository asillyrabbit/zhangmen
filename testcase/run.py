#! python3
import unittest
import HTMLTestReportCN
import os

# 测试用例存放路径
case_path = 'E:/autotest/zhangmen/testcase/' 

# 构造测试集
discover = unittest.defaultTestLoader.discover(case_path, pattern="tes*.py")  

# 执行用例集
if __name__ == '__main__':
    #确定生成报告的路径
    filePath ='E:/autotest/zhangmen/testreport/HTMLTestReportCN.html'
    fp = open(filePath,'wb')
    #生成报告的Title,描述
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=fp,
        title='自动化测试报告',
        #description='详细测试用例结果',
        tester=u'聂军'
        )
    # 运行测试用例
    runner.run(discover)
    