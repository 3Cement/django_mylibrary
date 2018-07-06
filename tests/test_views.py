from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse
from libraryapp.models import Author, Book, Genre, Language, Tag, FavouriteBook
from django.contrib.auth.models import User #Required to assign User as a borrower
from django.contrib.auth.models import Permission 

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('AuthorListViewTest launched')
        #Create 13 authors for pagination tests
        number_of_authors = 13
        for author_num in range(number_of_authors):
            Author.objects.create(first_name='Christian %s' % author_num, last_name = 'Surname %s' % author_num,)
           
    def test_view_url_exists_at_desired_location(self): 
        resp = self.client.get('/libraryapp/authors/') 
        self.assertEqual(resp.status_code, 200)  
           
    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)
        
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'libraryapp/author_list.html')
        
    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['author_list']) == 10)

    def test_lists_all_authors(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['author_list']) == 3)
        
class FavouriteBookByUserListViewTest(TestCase):

    def setUp(self):
        print('FavouriteBookByUserListViewTest launched')
        #Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345') 
        test_user2.save()
        test_user3 = User.objects.create_user(username='testuser3', password='12345') 
        test_user3.save()

        #Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_tag = Tag.objects.create(name="Humor")
        test_book_format = "e"
        test_read_date = timezone.now() - datetime.timedelta(days=20)
        test_book = Book.objects.create(title='Book Title', summary = 'My book summary',
                                        author=test_author, language=test_language,
                                        genre=test_genre, book_format=test_book_format,
                                        read_date=test_read_date)
        # Create tag as a post-step
        tag_objects_for_book = Tag.objects.all()
        test_book.tag.set(tag_objects_for_book) #Direct assignment of many-to-many types not allowed.
        test_book.save()

        #Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            if book_copy % 2:
                the_liker=test_user1
            else:
                the_liker=test_user2
            FavouriteBook.objects.create(book=test_book, liking=the_liker)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('favbooks'))
        self.assertRedirects(resp, '/accounts/login/?next=/libraryapp/favbooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('favbooks'))
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        #Check we used correct template
        self.assertTemplateUsed(resp, 'libraryapp/favouritebook_list.html')

    def test_that_test_user3_have_no_favourite_books(self):
        login = self.client.login(username='testuser3', password='12345')
        resp = self.client.get(reverse('favbooks'))
        #Check that initially test user 3 don't have any favourite books
        self.assertTrue('favouritebook_list' in resp.context)
        self.assertEqual( len(resp.context['favouritebook_list']),0)

    def test_only_favourite_books_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('favbooks'))
        
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        
        #Check that now we have borrowed books in the list
        resp = self.client.get(reverse('favbooks'))
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        
        self.assertTrue('favouritebook_list' in resp.context)
        
        #Confirm all books belong to testuser1 and are on loan
        for bookitem in resp.context['favouritebook_list']:
            self.assertEqual(resp.context['user'], bookitem.liking)

class CreateFavouriteBookViewTest(TestCase):

    def setUp(self):
        print('CreateFavouriteBookViewTest launched')
        #Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()
        permission = Permission.objects.get(name='Set book as favourite')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        #Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_tag = Tag.objects.create(name="Humor")
        test_book_format = "e"
        test_read_date = timezone.now() - datetime.timedelta(days=20)
        test_book = Book.objects.create(title='Book Title', summary = 'My book summary',
                                        author=test_author, language=test_language,
                                        genre=test_genre, book_format=test_book_format,
                                        read_date=test_read_date)
        # Create tag as a post-step
        tag_objects_for_book = Tag.objects.all()
        test_book.tag.set(tag_objects_for_book) #Direct assignment of many-to-many types not allowed.
        test_book.save()

        #Create a FavouriteBook object for test_user1
        self.test_favouritebook1=FavouriteBook.objects.create(book=test_book, liking=test_user1)

        #Create a FavouriteBook object for test_user2
        self.test_favouritebook2=FavouriteBook.objects.create(book=test_book, liking=test_user2)
  
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('add_book_to_favourites', kwargs={'pk':self.test_favouritebook1.pk,}) )
        #Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/accounts/login/') )
       
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('add_book_to_favourites', kwargs={'pk':self.test_favouritebook1.pk,}) )
        
        #Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/accounts/login/') )

class CreateBookViewTest(TestCase):

    def setUp(self):
        print('CreateBookReadDateTest launched')
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        permission = Permission.objects.get(name='Edit book')
        test_user1.user_permissions.add(permission) 
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        permission = Permission.objects.get(name='Edit book')
        test_user2.user_permissions.add(permission) 
        test_user2.save()
        print('user created')

        #Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_tag = Tag.objects.create(name="Humor")
        test_book_format = "e"
        test_read_date_past = datetime.date.today() - datetime.timedelta(days=20)

        self.test_book1 = Book.objects.create(title='Book Title1', summary = 'My book summary',
                                        author=test_author, language=test_language,
                                        genre=test_genre, book_format=test_book_format,
                                        read_date=test_read_date_past)
        # Create tag as a post-step
        tag_objects_for_book = Tag.objects.all()
        self.test_book1.tag.set(tag_objects_for_book) #Direct assignment of many-to-many types not allowed.
        self.test_book1.save()

        test_read_date_future = datetime.date.today() + datetime.timedelta(days=20)
        self.test_book2 = Book.objects.create(title='Book Title2', summary = 'My book summary',
                                        author=test_author, language=test_language,
                                        genre=test_genre, book_format=test_book_format,
                                        read_date=test_read_date_future)
        # Create tag as a post-step
        tag_objects_for_book = Tag.objects.all()
        self.test_book2.tag.set(tag_objects_for_book) #Direct assignment of many-to-many types not allowed.
        self.test_book2.save()
        print(self.test_book2.read_date)

    def test_if_book_form_view_date_is_really_20_days_in_future(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('book_update', kwargs={'pk':self.test_book2.pk,}) )
        self.assertEqual( resp.status_code,200)

        test_read_date_future = datetime.date.today() + datetime.timedelta(days=20)
        self.assertEqual(resp.context['form'].initial['read_date'], test_read_date_future )
        #self.assertFormError(resp, 'form', 'read_date', 'Read date cannot be in the future - MODELS.')