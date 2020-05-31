import configparser

def parser():
	c = configparser.ConfigParser(allow_no_value=True, interpolation=None, delimiters=('=',))
	c.optionxform = str
	return c

def parse(filename_str):
	p = parser()
	p.read(filename_str, encoding='utf-8')
	return p