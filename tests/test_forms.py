from django.test import TestCase
import datetime
from django.utils import timezone
from libraryapp.forms import AuthorForm, BookForm
from libraryapp.models import Author, Book, Genre, Language, Tag, FavouriteBook

class AuthorFormTest(TestCase):

    def test_author_form_first_name_field_label(self):
        form = AuthorForm()        
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'Name')

    def test_author_form_last_name_field_label(self):
        form = AuthorForm()        
        self.assertTrue(form.fields['last_name'].label == None or form.fields['last_name'].label == 'Surname')

    def test_author_data(self):
        print('Author Name/Surname TEST Lounched')
        first_name = 'Andrzej'
        last_name = 'Sapkowski'
        form_data = {'first_name': first_name, 'last_name': last_name}
        form = AuthorForm(data=form_data)        
        self.assertTrue(form.is_valid())

class BookFormTest(TestCase):

    def test_read_date_field_label(self):
        form = BookForm()
        self.assertTrue(form.fields['read_date'].label == None or form.fields['read_date'].label == 'Read date')

    def test_read_date_field_help_text(self):
        form = BookForm()
        self.assertEqual(form.fields['read_date'].help_text,'Enter a read date in the past')
  
    def test_read_date_in_the_past(self):
        print('BookForm in past TEST Lounched')
        test_title = 'TestBookPast'
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        date = datetime.date.today() - datetime.timedelta(days=2)
        form_data = {'title': test_title, 'author': test_author.id, 'read_date': date}
        form = BookForm(data=form_data)
        print(form.errors)        
        self.assertTrue(form.is_valid())

    def test_read_date_in_the_future(self):
        print('BookForm in future TEST Lounched')
        test_title = 'TestBookPast'
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        date = datetime.date.today() + datetime.timedelta(days=2)
        form_data = {'title': test_title, 'author': test_author.id, 'read_date': date}
        form = BookForm(data=form_data)
        print(form.errors)        
        self.assertFalse(form.is_valid())