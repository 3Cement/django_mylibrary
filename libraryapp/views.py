from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
import datetime
from .models import Author, Book, Genre, Language, Tag, FavouriteBook
from .forms import AuthorForm, BookForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    # Available books (status = 'a')
    #num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    num_tags = Tag.objects.all().count()
    num_genres = Genre.objects.count()
    num_languages = Language.objects.count()
    num_polish = Book.objects.filter(language__name__contains="polish").count()
    num_english = Book.objects.filter(language__name__contains="english").count()
    num_paperbacks = Book.objects.filter(book_format__exact='p').count()
    num_ebooks = Book.objects.filter(book_format__exact='e').count()
    num_audiobooks = Book.objects.filter(book_format__exact='a').count()
    read_in_2018 = Book.objects.filter(read_date__year=2018).count()
    read_in_2017 = Book.objects.filter(read_date__year=2017).count()
    read_before_2017 = Book.objects.filter(read_date__year__range=(1991, 2016)).count()
    no_date = Book.objects.filter(read_date__isnull=True).count()
    read_before = read_before_2017+no_date
    #num_favourites
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_authors':num_authors,
        		'num_tags':num_tags, 'num_genres':num_genres,
        		'num_languages':num_languages, 'num_polish':num_polish,
        		'num_english':num_english, 'num_paperbacks':num_paperbacks,
        		'num_ebooks':num_ebooks, 'num_audiobooks':num_audiobooks,
        		'read_in_2018':read_in_2018, 'read_in_2017':read_in_2017,
        		'read_before':read_before, 'num_visits':num_visits},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class TagDetailView(generic.DetailView):
    model = Tag

class TagListView(generic.ListView):
    model = Tag
    paginate_by = 10

class FavouriteBookDetailView(generic.DetailView):
    model = FavouriteBook

class FavouriteBookListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view current user favorite books. """
    model = FavouriteBook
    permission_required = 'libraryapp.can_mark_as_favourite'
    template_name ='libraryapp/favouritebook_list.html'
    paginate_by = 10

    def get_queryset(self):
        return FavouriteBook.objects.filter(liking=self.request.user)

class FavouriteBookAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view all users favorite books. """
    model = FavouriteBook
    permission_required = 'libraryapp.can_view_all_favourites'
    template_name ='libraryapp/favouritebook_list_all.html'
    paginate_by = 10

    def get_queryset(self):
        return FavouriteBook.objects.all()

def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Author has been created!'))
            return redirect('authors')
        else:
            form = AuthorForm()
            messages.success(request, ('You AuthorForm is invalid'))
            return redirect('authors')
    else:
        form = AuthorForm()
    return render(request, 'libraryapp/author_form.html', {'form': form})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Book has been created!'))
            return redirect('books')
        else:
            form = BookForm()
            messages.success(request, ('You BookForm is invalid'))
            return redirect('books')
    else:
        form = BookForm()
    return render(request, 'libraryapp/book_form.html', { 'form': form, },)

'''
class AuthorCreate(PermissionRequiredMixin, CreatePopupMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name'] 
    permission_required = 'libraryapp.can_edit'
'''
class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name']
    permission_required = 'libraryapp.can_edit'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'libraryapp.can_edit'
'''
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'tag', 'genre', 'language', 'book_format', 'read_date']
    permission_required = 'libraryapp.can_edit'
'''
class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'libraryapp.can_edit'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'libraryapp.can_edit'

class TagCreate(PermissionRequiredMixin, CreatePopupMixin, CreateView):
    model = Tag
    fields = ['name'] 
    permission_required = 'libraryapp.can_edit'

class TagUpdate(PermissionRequiredMixin, UpdateView):
    model = Tag
    fields = ['name'] 
    permission_required = 'libraryapp.can_edit'
    template_name = 'tag_form.html'

class TagDelete(PermissionRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tags')
    permission_required = 'libraryapp.can_edit'
'''
class FavouriteBookCreate(PermissionRequiredMixin, CreatePopupMixin, CreateView):
    model = FavouriteBook
    fields = ['book', 'liking'] 
    permission_required = 'libraryapp.can_mark_as_favourite'
'''
class FavouriteBookDelete(PermissionRequiredMixin, DeleteView):
    model = FavouriteBook
    success_url = reverse_lazy('favbooks')
    permission_required = 'libraryapp.can_mark_as_favourite'

@permission_required('libraryapp.can_mark_as_favourite')
def add_book_to_favourites(request, pk):
    book=get_object_or_404(Book, pk = pk)
    if FavouriteBook.objects.filter(book=book, liking=request.user).exists():
        messages.success(request, ('You already have this book in favorites!'))
        return HttpResponseRedirect(reverse('books') )
    else:
        fav_book = FavouriteBook.objects.create(book=book, liking=request.user)
        messages.success(request, ('Book added to favourites!'))
        return HttpResponseRedirect(reverse('favbooks') )


'''
from .forms import AddToFavourites
#@permission_required('catalog.can_mark_as_favourite')
def add_book_to_favourites(request, pk):
    fav_book=get_object_or_404(Book, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddToFavourites(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #fav_book.liking = form.cleaned_data['user.get_username']
            fav_book.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('favbooks') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddToFavourites()

    return render(request, 'libraryapp/add_book_to_favourites.html', {'form': form, 'favbook':fav_book})
'''


'''
class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name']
    permission_required = 'libraryapp.can_edit'

'''