import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))
# nl2br은 줄바꿈 문자를 <br> 로 바꾸어 준다. 
# fenced_code는 위에서 살펴본 마크다운의 소스코드 표현을 위해 필요하다.

