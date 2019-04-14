from pyswip import *
import xml.etree.ElementTree as ET

def py_read(*a):
	in1 = input("PyInput:")
	if a[0] == 1:
		if in1 == 1:
			return True
		else:
			return False
	if a[0] == 0:
		return False
	else:
		a[0].unify(in1)
	return True

def py_write(a):
    print a

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
