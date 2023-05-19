from django.shortcuts import render
import markdown
import random

from . import util

def md_to_html(title):
    data = util.get_entry(title)
    md = markdown.Markdown()
    if data == None:
        return None
    else:
        return md.convert(data)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request,title):
    html_content=md_to_html(title)
    if html_content==None:
        return render(request, "encyclopedia/error.html",{
            "message":"This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })

def search(request):
    if request.method=="POST":
        userinp = request.POST['q']
        html_data = md_to_html(userinp)
        if html_data is not None:
            return render(request, "encyclopedia/entry.html",{
            "title":userinp,
            "content":html_data
            })
        else:
            allentries = util.list_entries()
            recommend = []
            for i in allentries:
                if userinp.lower() in i.lower():
                    recommend.append(i)
            return render(request, "encyclopedia/search.html" ,{
                "recommendation" : recommend
            })

def new_page(request):
    if request.method == "GET":
        return render(request,"encyclopedia/new.html")
    else:
        title = request.POST['title']
        content =request.POST['content']
        titleexist = util.get_entry(title)
        if titleexist is not None:
            return render(request, "encyclopedia/error.html",{
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = md_to_html(title)
            return render(request,"encyclopedia/entry.html",{
                "title":title,
                "content":html_content
            })

def edit(request):
    if request.method == 'POST':
        title=request.POST['entry_title']
        content=util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "content":content
        
        })
    
def save_edit(request):
    if request.method=="POST":
        title = request.POST['title']
        content=request.POST['content']
        util.save_entry(title,content)
        html_content = md_to_html(title)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })

def randm(request):
    allentries=util.list_entries()
    random_entry=random.choice(allentries)
    html_content = md_to_html(random_entry)
    return render(request,"encyclopedia/entry.html",{
        "title":random_entry,
        "content":html_content
    })
   
 