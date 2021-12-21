from django import template
from  website.models import Blog


register = template.Library()





@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Blog.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}   