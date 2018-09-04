#TODO: connect all button events
# e.g. file select, set up different views (perhaps add large overhead frames,
# buttons set visibility)
# also have buttons disable clicked button after click
# add range select to panel A

import sys
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class App(QWidget):

		def __init__(self):
			super().__init__()

			# Housekeeping, name the window and set its size
			self.setWindowTitle('Software Reliability Tool')		
			self.setGeometry(25,25,1000,810)

			# Display name inside the tool
			titleLabel = QLabel(
				'Software Reliability Assessment in Python',self) 	
			titleLabel.setGeometry(0,0,500,50)							
			titleLabel.setFont(QFont("Arial",14))							
			titleLabel.setIndent(15)										
			titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

			# Create "tabs" - qt natively has tabs, but will use buttons for now
			menuButtonA = QPushButton('Select, Analyze, and Filter Data',self)
			menuButtonA.setGeometry(0,50,250,35)
			menuButtonA.setFont(QFont("Arial",12))

			menuButtonB = QPushButton('Set Up and Apply Models',self)
			menuButtonB.setGeometry(250,50,250,35)
			menuButtonB.setFont(QFont("Arial",12))

			menuButtonC = QPushButton('Query Model Results',self)
			menuButtonC.setGeometry(500,50,250,35)
			menuButtonC.setFont(QFont("Arial",12))

			menuButtonD = QPushButton('Evaluate Models',self)
			menuButtonD.setGeometry(750,50,250,35)
			menuButtonD.setFont(QFont("Arial",12))

			# Connecting the menu buttons
			menuButtonA.clicked.connect(partial(self.showMenu, 0))
			menuButtonB.clicked.connect(partial(self.showMenu, 1))
			menuButtonC.clicked.connect(partial(self.showMenu, 2))
			menuButtonD.clicked.connect(partial(self.showMenu, 3))

##			# Begin panel A.
			# Side panel frame for 'select/analyze/filter' option
			self.menuAFrame = QFrame(self)
			self.menuAFrame.setFrameStyle(QFrame().Panel | QFrame().Raised)
			self.menuAFrame.setLineWidth(2)
			self.menuAFrame.setGeometry(10,95,300,705)

			# Title labeling.
			menuALabel = QLabel(
				'Select, Analyze, and Subset Failure Data',self.menuAFrame)
			menuALabel.setFont(QFont("Arial",14))	
			menuALabel.setWordWrap(True)
			menuALabel.setGeometry(20,20,260,50)
			menuALabel.setAlignment(Qt.AlignCenter)

			# File select, limit to xlsx or csv, update menuAFLabel after
			menuAFButton = QPushButton('Select File',self.menuAFrame)
			menuAFButton.setGeometry(40,85,220,35)

			# Will be file name, added self for other file reference
			self.menuAFLabel = QLabel('No File Selected',self.menuAFrame)
			self.menuAFLabel.setFont(QFont("Arial",10,-1,True))
			self.menuAFLabel.setGeometry(0,125,300,20)
			self.menuAFLabel.setAlignment(Qt.AlignCenter)

			# Drop-down label
			menuAViewLabel = QLabel(
				'Choose a view of the failure data.',self.menuAFrame)
			menuAViewLabel.setFont(QFont("Arial",10))
			menuAViewLabel.setGeometry(0,165,300,20)
			menuAViewLabel.setAlignment(Qt.AlignCenter)

			# Drop-down to select view
			menuAViewBox = QComboBox(self.menuAFrame)
			menuAViewBox.setGeometry(40,185,220,30)
			menuAViewBox.addItem('Times Between Failures')
			menuAViewBox.addItem('Cumulative Failures')
			menuAViewBox.addItem('Failure Intensity')

			# Pick how to draw data, draw radio buttons; setup exclusive group
			menuAViewLabel = QLabel(
				'Draw plot with points, lines, or both?',self.menuAFrame)
			menuAViewLabel.setFont(QFont("Arial",10))
			menuAViewLabel.setGeometry(40,250,220,30)
			menuAViewLabel.setAlignment(Qt.AlignCenter)
			menuAViewLabel.setWordWrap(True)

			# Set up exclusive radio button group
			menuAPlotGroupA = QGroupBox(self.menuAFrame)
			menuAPlotGroupA.setGeometry(40,250,215,50)

			# Supply the actual radio buttons
			menuAPlotRA = QRadioButton('Both',menuAPlotGroupA)
			menuAPlotRA.setGeometry(5,12,71,50)
			menuAPlotRB = QRadioButton('Points',menuAPlotGroupA)
			menuAPlotRB.setGeometry(73,12,71,50)
			menuAPlotRC = QRadioButton('Lines',menuAPlotGroupA)
			menuAPlotRC.setGeometry(146,12,71,50)
			menuAPlotRA.setChecked(True)

			# Label for picking plotting
			menuAViewLabel = QLabel(
				'Plot Data or Trend Test?',self.menuAFrame)
			menuAViewLabel.setFont(QFont("Arial",10))
			menuAViewLabel.setGeometry(40,295,220,30)
			menuAViewLabel.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
			menuAViewLabel.setWordWrap(True)

			# Data / Trend test radio buttons
			menuAPlotGroupB = QGroupBox(self.menuAFrame)
			menuAPlotGroupB.setGeometry(40,300,220,50)

			menuASelectRA = QRadioButton('Data',menuAPlotGroupB)
			menuASelectRA.setGeometry(20,12,71,50)
			menuASelectRB = QRadioButton('Trend Test',menuAPlotGroupB)
			menuASelectRB.setGeometry(100,12,100,50)
			menuASelectRA.setChecked(True)

			menuAGrowthLabel = QLabel(
				'Does data show reliability growth?',self.menuAFrame)
			menuAGrowthLabel.setFont(QFont("Arial",10))
			menuAGrowthLabel.setGeometry(40,370,220,30)
			menuAGrowthLabel.setAlignment(Qt.AlignCenter)

			# Drop-down to reliability display, labeled above
			menuAGrowthBox = QComboBox(self.menuAFrame)
			menuAGrowthBox.setGeometry(40,395,220,30)
			menuAGrowthBox.addItem('Laplace Test')
			menuAGrowthBox.addItem('Running Arithmetic Average')

			# Drop-down for reliability display

			menuAConfidenceLabel = QLabel(
				'Laplace Test Confidence',self.menuAFrame)
			menuAConfidenceLabel.setFont(QFont("Arial",10))
			menuAConfidenceLabel.setGeometry(40,440,215,30)
			menuAConfidenceLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			menuAConfidenceLabel.setWordWrap(True)

			menuAConfidenceLevel = QDoubleSpinBox(self.menuAFrame)
			menuAConfidenceLevel.setRange(0,1)
			menuAConfidenceLevel.setSingleStep(.01)
			menuAConfidenceLevel.setValue(.9)
			menuAConfidenceLevel.setGeometry(200,440,55,30)

			# Select save file Type // TODO: remove this, add all to save dlg
			menuAPlotGroupC = QGroupBox(self.menuAFrame)
			menuAPlotGroupC.setGeometry(40,465,125,75)

			menuASaveRA = QRadioButton('JPG',menuAPlotGroupC)
			menuASaveRA.setGeometry(5,12,60,50)
			menuASaveRB = QRadioButton('PDF',menuAPlotGroupC)
			menuASaveRB.setGeometry(5,37,60,50)
			menuASaveRC = QRadioButton('PNG',menuAPlotGroupC)
			menuASaveRC.setGeometry(65,12,60,50)
			menuASaveRD = QRadioButton('TIFF',menuAPlotGroupC)
			menuASaveRD.setGeometry(65,37,60,50)
			menuASaveRA.setChecked(True)

			# Button to save
			menuAFSaver = QPushButton('Save Display',self.menuAFrame)
			menuAFSaver.setGeometry(165,500,90,30)

			#Label data range
			menuARangeLabel = QLabel(
				'Subset data by data range:',self.menuAFrame)
			menuARangeLabel.setFont(QFont("Arial",12))
			menuARangeLabel.setGeometry(0,560,300,30)
			menuARangeLabel.setAlignment(Qt.AlignCenter)
			menuARangeLabel.setWordWrap(True)

			#Label minmax/to
			menuARangeLabel = QLabel(
				'to',self.menuAFrame)
			menuARangeLabel.setFont(QFont("Arial",10, -1, 1))
			menuARangeLabel.setGeometry(0,600,300,30)
			menuARangeLabel.setAlignment(Qt.AlignCenter)
			menuARangeLabel.setWordWrap(True)

			# Minimum for data range, has function attached for maximum
			self.menuAMin = QSpinBox(self.menuAFrame)
			self.menuAMin.setRange(1,5)
			self.menuAMin.setValue(1)
			self.menuAMin.setGeometry(80,600,55,30)

			# Maximum for data range, has function attached for minimum
			self.menuAMax = QSpinBox(self.menuAFrame)
			self.menuAMax.setRange(1,5)
			self.menuAMax.setValue(5)
			self.menuAMax.setGeometry(165,600,55,30)

			self.menuAMin.valueChanged.connect(self.rangeMinChange)
			self.menuAMax.valueChanged.connect(self.rangeMaxChange)

##			# Start panel B
			self.menuBFrame = QFrame(self)
			self.menuBFrame.setFrameStyle(QFrame().Panel | QFrame().Raised)
			self.menuBFrame.setLineWidth(2)
			self.menuBFrame.setGeometry(10,95,300,705)

			# Labeling
			menuBLabel = QLabel(
				'Configure and Apply Models',self.menuBFrame)
			menuBLabel.setFont(QFont("Arial",14))	
			menuBLabel.setWordWrap(True)
			menuBLabel.setGeometry(0,20,300,25)
			menuBLabel.setAlignment(Qt.AlignCenter)

			menuBPredictL = QLabel(
				'Specify failure prediction numbers' ,self.menuBFrame)
			menuBPredictL.setFont(QFont("Arial",10))
			menuBPredictL.setGeometry(0,25,300,55)
			menuBPredictL.setWordWrap(True)
			menuBPredictL.setAlignment(Qt.AlignCenter)

			menuBPredictLB = QLabel(
				'Number of future failures to predict:' ,self.menuBFrame)
			menuBPredictLB.setFont(QFont("Arial",10))
			menuBPredictLB.setGeometry(10,55,215,55)
			menuBPredictLB.setWordWrap(True)
			menuBPredictLB.setAlignment(Qt.AlignCenter)

			# Counter to check future failures, connect later when f.w. is done
			menuBPredict = QSpinBox(self.menuBFrame)
			menuBPredict.setValue(0)
			menuBPredict.setGeometry(230,67,55,30)

			# Models text
			menuBPredictL = QLabel(
				'Choose models to run or exclude.' ,self.menuBFrame)
			menuBPredictL.setFont(QFont("Arial",10))
			menuBPredictL.setGeometry(20,90,300,55)
			menuBPredictL.setWordWrap(True)
			menuBPredictL.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

			# Edit this later: select data set
			menuBDataSetB = QLineEdit(
				'Open a data set to run models', self.menuBFrame)
			menuBDataSetB.setFont(QFont("Arial",12))
			menuBDataSetB.setGeometry(20,130,260,25)

			# Run models button
			menuBRunButton = QPushButton(
				'Run Selected Models',self.menuBFrame)
			menuBRunButton.setGeometry(20,160,165,25)
			menuBRunButton.setFont(QFont("Arial",12))	

			# Display Label
			menuBDispLabel = QLabel(
				'Display Model Results',self.menuBFrame)
			menuBDispLabel.setFont(QFont("Arial",14))	
			menuBDispLabel.setWordWrap(True)
			menuBDispLabel.setGeometry(10,205,290,25)
			menuBDispLabel.setAlignment(Qt.AlignLeft)

			menuBDispLabelB = QLabel(
				'Choose model result sets to display.',self.menuBFrame)
			menuBDispLabelB.setFont(QFont("Arial",10))	
			menuBDispLabelB.setWordWrap(True)
			menuBDispLabelB.setGeometry(20,230,290,25)
			menuBDispLabelB.setAlignment(Qt.AlignLeft)

			# Also edit this later: select data set, second time
			menuBDataSetB = QLineEdit(
				'No model results to display.', self.menuBFrame)
			menuBDataSetB.setFont(QFont("Arial",12))
			menuBDataSetB.setGeometry(20,250,260,25)

			# Choose plot type, label and menu
			menuBTypeLabel = QLabel(
				'Pick the plot type for model results.',self.menuBFrame)
			menuBTypeLabel.setFont(QFont("Arial",10))	
			menuBTypeLabel.setWordWrap(True)
			menuBTypeLabel.setGeometry(20,290,290,25)
			menuBTypeLabel.setAlignment(Qt.AlignLeft)

			# Drop-down for plot type
			menuBPlotBox = QComboBox(self.menuBFrame)
			menuBPlotBox.setGeometry(20,310,260,30)
			menuBPlotBox.addItem('Times Between Failures')
			menuBPlotBox.addItem('Cumulative Failures')
			menuBPlotBox.addItem('Failure Intensity')
			menuBPlotBox.addItem('Reliability Growth')

			# Plot extension duration label/box
			menuBExtendLabel = QLabel(
				'Curve duration extension, past prediction point:',
				self.menuBFrame)
			menuBExtendLabel.setFont(QFont("Arial",10))	
			menuBExtendLabel.setWordWrap(True)
			menuBExtendLabel.setGeometry(20,350,170,30)
			menuBExtendLabel.setAlignment(Qt.AlignLeft)

			# Edit maximum value later
			menuBExtend = QSpinBox(self.menuBFrame)
			menuBExtend.setMaximum(100000000000)
			menuBExtend.setSingleStep(100)
			menuBExtend.setValue(100)
			menuBExtend.setGeometry(180,350,100,30)

			# Check boxes for data on plot
			menuBDataCheck = QCheckBox('Show data', self.menuBFrame)
			menuBDataCheck.setChecked(True) # Use setCheckState for tri-state
			menuBDataCheck.setGeometry(20,390,100,30)

			menuBEndCheck = QCheckBox('Show data end', self.menuBFrame)
			menuBEndCheck.setChecked(True)
			menuBEndCheck.setGeometry(150,390,150,30)

			# Radio buttons for pts/lines/both
			menuBExtendLabel = QLabel(
				'Draw plot with data points, lines, or both?',
				self.menuBFrame)
			menuBExtendLabel.setFont(QFont("Arial",10))	
			menuBExtendLabel.setWordWrap(True)
			menuBExtendLabel.setGeometry(0,420,300,30)
			menuBExtendLabel.setAlignment(Qt.AlignCenter)

			menuBPlotGroupA = QGroupBox(self.menuBFrame)
			menuBPlotGroupA.setGeometry(40,420,220,50)

			menuBPlotRA = QRadioButton('Both',menuBPlotGroupA)
			menuBPlotRA.setGeometry(5,12,71,50)
			menuBPlotRB = QRadioButton('Points',menuBPlotGroupA)
			menuBPlotRB.setGeometry(73,12,71,50)
			menuBPlotRC = QRadioButton('Lines',menuBPlotGroupA)
			menuBPlotRC.setGeometry(146,12,71,50)
			menuBPlotRA.setChecked(True)

			# Select save file Type // TODO: remove this, add all to save dlg
			menuBPlotGroupB = QGroupBox(self.menuBFrame)
			menuBPlotGroupB.setGeometry(40,465,125,75)

			menuBSaveRA = QRadioButton('JPG',menuBPlotGroupB)
			menuBSaveRA.setGeometry(5,12,60,50)
			menuBSaveRB = QRadioButton('PDF',menuBPlotGroupB)
			menuBSaveRB.setGeometry(5,37,60,50)
			menuBSaveRC = QRadioButton('PNG',menuBPlotGroupB)
			menuBSaveRC.setGeometry(65,12,60,50)
			menuBSaveRD = QRadioButton('TIFF',menuBPlotGroupB)
			menuBSaveRD.setGeometry(65,37,60,50)
			menuBSaveRA.setChecked(True)

			menuBFSaver = QPushButton('Save Display',self.menuBFrame)
			menuBFSaver.setGeometry(165,500,90,30)

##			# Start panel C

			self.menuCFrame = QFrame(self)
			self.menuCFrame.setFrameStyle(QFrame().Panel | QFrame().Raised)
			self.menuCFrame.setLineWidth(2)
			self.menuCFrame.setGeometry(10,95,300,705)

			# Labeling
			menuCLabel = QLabel(
				'Predictions From Results',self.menuCFrame)
			menuCLabel.setFont(QFont("Arial",14))	
			menuCLabel.setWordWrap(True)
			menuCLabel.setGeometry(0,20,300,25)
			menuCLabel.setAlignment(Qt.AlignCenter)

			# Choose display model
			menuCDispLabelA = QLabel(
				'Choose model result sets to display.',self.menuCFrame)
			menuCDispLabelA.setFont(QFont("Arial",10))	
			menuCDispLabelA.setWordWrap(True)
			menuCDispLabelA.setGeometry(20,60,290,25)
			menuCDispLabelA.setAlignment(Qt.AlignLeft)

			# Also edit this later: select data set, third? time
			menuCDataSet = QLineEdit(
				'No model results to display.', self.menuCFrame)
			menuCDataSet.setFont(QFont("Arial",12))
			menuCDataSet.setGeometry(20,80,260,25)

			menuCDispLabelB = QLabel(
				'Time to observe next failures:',self.menuCFrame)
			menuCDispLabelB.setFont(QFont("Arial",12))	
			menuCDispLabelB.setGeometry(20,120,290,25)
			menuCDispLabelB.setAlignment(Qt.AlignLeft)

			menuCDispLabelC = QLabel(
				'Specify the number of failures to be observed:'
				,self.menuCFrame)
			menuCDispLabelC.setFont(QFont("Arial",10))	
			menuCDispLabelC.setWordWrap(True)
			menuCDispLabelC.setGeometry(20,145,165,30)
			menuCDispLabelC.setAlignment(Qt.AlignLeft)

			# Counter for next failures observed, label above
			menuCFailures = QSpinBox(self.menuCFrame)
			menuCFailures.setMinimum(1)
			menuCFailures.setGeometry(195,145,85,30)

			menuCDispLabelD = QLabel(
				'Determine failures using extra time:', self.menuCFrame)
			menuCDispLabelD.setFont(QFont("Arial",12))	
			menuCDispLabelD.setGeometry(20,190,250,30)
			menuCDispLabelD.setAlignment(Qt.AlignLeft)

			menuCDispLabelE = QLabel(
				'Specify the amount of additional time to run:'
				,self.menuCFrame)
			menuCDispLabelE.setFont(QFont("Arial",10))	
			menuCDispLabelE.setWordWrap(True)
			menuCDispLabelE.setGeometry(20,215,165,30)
			menuCDispLabelE.setAlignment(Qt.AlignLeft)

			# Counter for next failures observed, label above
			menuCExtraTime = QSpinBox(self.menuCFrame)
			menuCExtraTime.setMinimum(1)
			menuCExtraTime.setGeometry(195,215,85,30)

			#D etermine time with reliability
			menuCDispLabelF = QLabel(
				'Determine test time given reliability:', self.menuCFrame)
			menuCDispLabelF.setFont(QFont("Arial",12))	
			menuCDispLabelF.setGeometry(20,260,250,30)
			menuCDispLabelF.setAlignment(Qt.AlignLeft)

			menuCDispLabelG = QLabel(
				'Specify the desired reliability:'
				,self.menuCFrame)
			menuCDispLabelG.setFont(QFont("Arial",10))	
			menuCDispLabelG.setWordWrap(True)
			menuCDispLabelG.setGeometry(20,285,165,30)
			menuCDispLabelG.setAlignment(Qt.AlignLeft)

			# Counter for reliability, label above
			menuCReliability = QDoubleSpinBox(self.menuCFrame)
			menuCReliability.setRange(0,1)
			menuCReliability.setSingleStep(.01)
			menuCReliability.setValue(.8)
			menuCReliability.setGeometry(195,285,85,30)
			
			menuCDispLabelH = QLabel(
				'Specify the interval to calculate reliability:'
				,self.menuCFrame)
			menuCDispLabelH.setFont(QFont("Arial",10))	
			menuCDispLabelH.setWordWrap(True)
			menuCDispLabelH.setGeometry(20,325,165,30)
			menuCDispLabelH.setAlignment(Qt.AlignLeft)

			menuCInterval = QSpinBox(self.menuCFrame)
			menuCInterval.setGeometry(195,325,85,30)

			# Select save file Type // TODO: remove this, add all to save dlg
			menuCPlotGroup = QGroupBox(self.menuCFrame)
			menuCPlotGroup.setGeometry(50,365,200,50)

			menuCSaveRA = QRadioButton('CSV',menuCPlotGroup)
			menuCSaveRA.setGeometry(5,12,60,50)
			menuCSaveRB = QRadioButton('PDF',menuCPlotGroup)
			menuCSaveRB.setGeometry(120,12,60,50)
			menuCSaveRA.setChecked(True)

			menuCFSaver = QPushButton('Save Predictions',self.menuCFrame)
			menuCFSaver.setGeometry(50,425,200,30)

##			# Start panel D
			self.menuDFrame = QFrame(self)
			self.menuDFrame.setFrameStyle(QFrame().Panel | QFrame().Raised)
			self.menuDFrame.setLineWidth(2)
			self.menuDFrame.setGeometry(10,95,300,705)

			# Title label
			menuDLabel = QLabel(
				'Evaluate Fit and Applicability',self.menuDFrame)
			menuDLabel.setFont(QFont("Arial",14))	
			menuDLabel.setWordWrap(True)
			menuDLabel.setGeometry(0,20,300,25)
			menuDLabel.setAlignment(Qt.AlignCenter)

			# Description labels
			menuDLabelB = QLabel(
				'Choose the models to evaluate results from.',self.menuDFrame)
			menuDLabelB.setFont(QFont("Arial",10))	
			menuDLabelB.setWordWrap(True)
			menuDLabelB.setGeometry(20,60,300,25)

			# Edit this later: select data set
			menuDDataSet = QLineEdit(
				'Open a data set to run models', self.menuDFrame)
			menuDDataSet.setFont(QFont("Arial",12))
			menuDDataSet.setGeometry(20,85,260,25)

			# Description label for percentage
			menuDLabelC = QLabel(
				'Specify PSSE percent data.',self.menuDFrame)
			menuDLabelC.setFont(QFont("Arial",10))	
			menuDLabelC.setWordWrap(True)
			menuDLabelC.setGeometry(20,135,300,25)

			# Spin box for data percentage
			menuDPercentage = QDoubleSpinBox(self.menuDFrame)
			menuDPercentage.setRange(0,1)
			menuDPercentage.setSingleStep(.01)
			menuDPercentage.setValue(.9)
			menuDPercentage.setGeometry(195,133,85,30)

			# Select save file Type // TODO: remove this, add all to save dlg
			menuDPlotGroup = QGroupBox(self.menuDFrame)
			menuDPlotGroup.setGeometry(50,150,200,50)

			menuDSaveRA = QRadioButton('CSV',menuDPlotGroup)
			menuDSaveRA.setGeometry(5,12,60,50)
			menuDSaveRB = QRadioButton('PDF',menuDPlotGroup)
			menuDSaveRB.setGeometry(120,12,60,50)
			menuDSaveRA.setChecked(True)

			menuDFSaver = QPushButton('Save Evaluations',self.menuDFrame)
			menuDFSaver.setGeometry(50,210,200,30)

##			# Finalize

			self.show()
			self.showMenu(0)

		# There's probably a better way to do this
		# Functions for the four menu buttons
		def showMenu(self, id):
			self.menuAFrame.setVisible(id == 0)
			self.menuBFrame.setVisible(id == 1)
			self.menuCFrame.setVisible(id == 2)
			self.menuDFrame.setVisible(id == 3)

		def rangeMinChange(self, i):
			self.menuAMax.setRange(i,5)

		def rangeMaxChange(self, i):
			self.menuAMin.setRange(1,i)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())