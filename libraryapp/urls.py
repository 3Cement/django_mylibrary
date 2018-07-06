from django.urls import path
from . import views
from django.conf.urls import url
#from libraryapp.views import author_create, book_create

urlpatterns = [
	path('', views.index, name='index'),
	path('books/', views.BookListView.as_view(), name='books'),
	path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    #path('book/create/', views.BookCreate.as_view(), name='book_form'),
    path('book/create/', views.book_create, name='book_form'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    #path('author/create/', views.AuthorCreate.as_view(), name='author_form'),
	path('author/create/', views.author_create, name='author_form'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

    path('favbooks/', views.FavouriteBookListView.as_view(), name='favbooks'),
    path('favbook/<int:pk>', views.FavouriteBookDetailView.as_view(), name='favbook-detail'),
    path('all-favbooks/', views.FavouriteBookAllListView.as_view(), name='all-favbooks'),
    path('book/<int:pk>/addfav/', views.add_book_to_favourites, name='add_book_to_favourites'),
    #path('favbooks/create/', views.FavouriteBookCreate.as_view(), name='favouritebook_form'),
    path('favbooks/<int:pk>/delete/', views.FavouriteBookDelete.as_view(), name='favouritebook_delete'),

    path('tags/', views.TagListView.as_view(), name='tags'),
    path('tag/<int:pk>', views.TagDetailView.as_view(), name='tag-detail'),
    path('tag/create/', views.TagCreate.as_view(), name='tag_form'),
    path('tag/<int:pk>/update/', views.TagUpdate.as_view(), name='tag_update'),
    path('tag/<int:pk>/delete/', views.TagDelete.as_view(), name='tag_delete'),
]
'''
urlpatterns = [
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_form'),
	url(r'^author/update/(?P<pk>.*)/$', views.AuthorUpdate.as_view(), name='author_update'),
]
'''