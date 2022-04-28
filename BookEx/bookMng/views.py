from django.shortcuts import render
from .forms import SearchForm

# Create your views here.
# ***********************************************************
# TO CLASS MATES GROUP 5
#  ADD YOUR NEW DEFINITIONS AT THE BOTTOM
# ************************************************************


from django.http import HttpResponse

from .models import MainMenu
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book
from .models import WishList

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,
                  "bookMng/index.html",
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
        return render(request,
                      "bookMng/postbook.html",
                      {
                          'form': form,
                          'item_list': MainMenu.objects.all(),
                          'submitted': submitted
                      }
                      )


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  "bookMng/displaybooks.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    return render(request,
                  "bookMng/book_detail.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  "bookMng/mybooks.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  "bookMng/book_delete.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )


def about_us(request):
    team = {
        'Angel': ['Computer Science', 'https://github.com/AngelV129'],
        'Mychal Salgado': ['Computer Science', 'https://github.com/mycsal'],
        'Portia Wu': ['Computer Science', 'https://github.com/portiawuuu'],
        'Alexander Voisan': ['Computer Science', 'https://github.com/ajcoolman'],
        'Guang Wu': ['Computer Science', 'https://google.com'],
        'Fernando Torres': ['Computer Science', 'https://github.com/TACONACHOLIBRE']
    }
    return render(request, 'bookMng/about_us.html',
                  {
                      'team': team,
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def search_books(request):
    if request.method == 'POST':

        query = request.POST['query']
        books = Book.objects.filter(name__contains=query)

        for b in books:
            b.pic_path = b.picture.url[14:]

        return render(request,
                      'bookMng/search_books.html',
                      {
                          'books': books,
                          'query': query
                      })
    else:
        return render(request, 'bookMng/search_books.html')


@login_required(login_url=reverse_lazy('login'))
def wish_list(request):
    wish_list = WishList.objects.filter(username=request.user)
    books_to_save = []

    for book in wish_list:
        book = Book.objects.get(id=book.book_id)
        book.pic_path = book.picture.url[14:]
        books_to_save.append(book)

    return render(request, 'bookMng/wish_list.html',
                  {
                      'books': books_to_save,
                  })


@login_required(login_url=reverse_lazy('login'))
def add_to_wish_list(request, book_id):
    wish_list.objects.create(book_id=book_id, username=request.user)
    return HttpResponseRedirect('/displaybooks')

@login_required(login_url=reverse_lazy('login'))
def remove_from_wish_list(request, book_id):
    wish_list.objects.get(book_id=book_id).delete()
    return HttpResponseRedirect('/wish_list')

