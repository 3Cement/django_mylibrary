from django.test import TestCase

# Create your tests here.

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

    def test_author_name_and_surname(self):
        print('Author Name/Surname TEST Lounched')
        first_name = 'Andrzej'
        last_name = 'Sapkowski'
        form_data = {'first_name': first_name, 'last_name': last_name}
        form = AuthorForm(data=form_data)        
        self.assertTrue(form.is_valid())
'''
    def test_author_surname(self):
        print('Author Surname TEST Lounched')
        last_name = 'Sapkowski'
        form_data = {'last_name': last_name}
        form = AuthorForm(data=form_data)        
        self.assertTrue(form.is_valid())'''

class BookFormTest(TestCase):

    def test_read_date_field_label(self):
        form = BookForm()
        self.assertTrue(form.fields['read_date'].label == None or form.fields['read_date'].label == 'Read date')

    def test_read_date_field_help_text(self):
        form = BookForm()
        self.assertEqual(form.fields['read_date'].help_text,'Enter a read date in the past')
  
    def test_read_date_in_the_past(self):
        title = 'TestBookPast'
        author = 'TestAuthorPast'
        date = datetime.date.today() - datetime.timedelta(days=2)
        form_data = {'title': title, 'author': author, 'read_date': date}
        form = BookForm(data=form_data)        
        self.assertTrue(form.is_valid())

    def test_read_date_in_the_future(self):
        title = 'TestBookFuture'
        author = 'TestAuthorFuture'
        date = datetime.date.today() + datetime.timedelta(days=2)
        form_data = {'title': title, 'author': author, 'read_date': date}
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())