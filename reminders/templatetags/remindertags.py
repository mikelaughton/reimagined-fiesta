from django import template
register = template.Library()

@register.filter(name='starout')
def starout(value):
	''' Expects 'string', returns 's****g' '''
	v_space_list = value.split(" ")
	star = lambda x: x[0] + "*"*len(x[1:-1]) + x[-1]
	starred_out = [star(v) for v in v_space_list]
	return " ".join(starred_out)
