from django import template


register = template.Library()

@register.filter(name='zip')
def ziper(a, b):
    return zip(a,b)

# @register.filter(name='DL-dict')
# def double_list_to_dict(double_list):

#     list_1 = double_list[0]
#     list_2 = double_list[1]
#     return zip(a,b)