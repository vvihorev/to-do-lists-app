from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item

def home_page(request):
    # TODO: support more than one list
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/absolutely-unique-list/')
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
