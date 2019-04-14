from pyswip import *
import xml.etree.ElementTree as ET

from pyswip import *
import xml.etree.ElementTree as ET
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading
import time

app = []
global flag
flag = -1

def SBC():

	def py_read(*a):
		global flag
		while True:
			if flag != -1:
				break
		if a[0] == 1:
			if flag == 1:
				flag = -1
				return True
			else:
				flag = -1
				return False
		if a[0] == 0:
			flag = -1
			return False
		else:
			a[0].unify(flag)
		flag = -1
		return True

	def py_write(a):
	    app.updateLabel(a)

	registerForeign(py_write, arity = 1)
	registerForeign(py_read, arity = 1)

	tree = ET.parse('sbcTema2.xml')

	root = tree.getroot()

	text = ''

	p = Prolog()

	for fact in root.findall('./facts/food/*'):
		for animal in fact.findall('./*'):
			text = fact.tag + '(' + animal.text + ')'
			print(text)
			p.assertz(text)

	for fact in root.findall('./facts/originates'):
		text = 'originates(' + fact.find('animal').text + ',' + fact.find('provenience').text + ')'
		print(text)
		p.assertz(text)


	for rule in root.iter('rule'):

		text = rule.find('then').find('rel').text + '('
		for par in rule.findall('./then/p'):
			text += par.text + ','
		text = text[:-1] + ') :- '
		for r in rule.findall('./and'):
			if r.find('rel') is not None:
				text += r.find('rel').text + '('
				for par in r.findall('./p') :
					text += par.text + ','
				if r.find('p') is not None:
					text = text[:-1] + '),'
				else:
					text = text

		text = text[:-1]
		print(text)
		p.assertz(text)
	p.assertz('is_true(X, Y) :- py_write(X), py_read(Y), assertz(remember(X, Y))')
	p.asserta('remember(false, false)')

	for q in p.query('qanimal(X, Y, F)'):
		print(q['X'], q['Y'], q['F'])
		app.updateLabel('Your thinking about:' + q['X'] + ' ' + 'It comes from:' + q['Y']  + ' ' + 'And is:' +  q['F'])

def callback1(instance):
	global flag
	print('The button <%s> is being pressed' % instance.text)
	flag = 1
def callback2(instance):
	global flag
	print('The button <%s> is being pressed' % instance.text)
	flag = 0

class MyApp(App):
	def build(self):
		layout = BoxLayout(orientation='vertical')
		self.l = Label(text='Hello world')
		layout.add_widget(self.l);
		layout2 = BoxLayout(orientation='horizontal')
		layout.add_widget(layout2);
		btn1 = Button(text='Yes')
		btn2 = Button(text='No')
		btn1.bind(on_press=callback1)
		btn2.bind(on_press=callback2)
		layout2.add_widget(btn1)
		layout2.add_widget(btn2)
		return layout
	def updateLabel(self, text):
		self.l.text = str(text)
		print text


class myThread (threading.Thread):

	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		print "Starting " + self.name
		app.run()
		print "Exiting " + self.name

app = MyApp()

# Create new threads
thread = myThread(1, "GUI")

# Start new Threads
thread.start()
time.sleep(1)
SBC()
