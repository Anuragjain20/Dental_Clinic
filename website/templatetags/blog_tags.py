from django import template
from  website.models import Blog
import markdown as md
from django.template.defaultfilters import stringfilter

register = template.Library()



@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Blog.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}   