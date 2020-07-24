import os


#os.system('pytest -s test_JM.py')
#os.system('conda activate DataScience && pytest -s test_GM.py')
#os.system('pytest -s test_GO.py')
#Running JM Model Test

os.system('pytest --excelreport=results/report_JM.xls test_JM.py')
os.system('pytest --excelreport=results/report_GM.xls test_GM.py')
os.system('pytest --excelreport=results/report_GO.xls test_GO.py')


os.system('pytest --excelreport=results/report_generic.xls test_generic.py')