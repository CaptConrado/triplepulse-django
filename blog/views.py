from django.shortcuts import render
from cms.models.pagemodel import Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect

def blog_index(request, page_number):
    previews=[]
    posts = Page.objects.all().filter(published=True)
    for post in posts:
        url = post.get_path()
        if 'blog/' in url:
            title = post.get_title()
            placeholders = list(post.placeholders.all())
            content_blocks = []
            for ph in placeholders:
                plugins = list(ph.cmsplugin_set.all().order_by('tree_id', '-rght'))
                for plugin in plugins:
                    content_blocks.append(plugin.render_plugin())
            previews.append({'title' : title, 'url' : '/' + url, 'content_blocks' : content_blocks})
    paginator = Paginator(previews, 5)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect("1")
    except PageNotAnInteger:
        return HttpResponseRedirect("1")

    context = { 'posts' : page.object_list, 'has_next' : page.has_next(), 'has_previous' : page.has_next(), 'previous' : page.previous_page_number(), 'next' : page.next_page_number()}

    return render(request, 'blog-index.html', context)