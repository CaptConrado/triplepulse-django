from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import simplejson
from models import PinboardPost
from TriplePulse.settings import POSTS_ROOT

def pinboard_posts(request):
    if request.GET.get('page'):
        page = request.GET['page']
    else:
        page = 1
    posts = PinboardPost.objects.select_related().filter(page__published = True).reverse()
    paginator = Paginator(posts, 50)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)


    return_value=[]
    for post in posts.object_list:
        return_value.append({
            'title': post.page.get_title(),
            'url' : '/' + POSTS_ROOT + post.page.get_path(),
            'category': post.category.name,
            'image' : {
                'height' : str(post.image_size.height) + 'px',
                'width' : str(post.image_size.width) + 'px',
                'url' : post.image.url,
                }
            })
    return_value = {'has_next' : posts.has_next(), 'posts' : return_value}

    return HttpResponse(simplejson.dumps(return_value))
#    return HttpResponse(serializers.serialize('json', posts))
