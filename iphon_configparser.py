import configparser

def parser():
	c = configparser.ConfigParser(allow_no_value=True, interpolation=None, delimiters=('=',))
	c.optionxform = str
	return c