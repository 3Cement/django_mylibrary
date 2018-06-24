from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from libraryapp.forms import AuthorForm

class AuthorFormTest(TestCase):

    def test_author_form_first_name_field_label(self):
        form = AuthorForm()        
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'Name')

    def test_author_form_last_name_field_label(self):
        form = AuthorForm()        
        self.assertTrue(form.fields['last_name'].label == None or form.fields['last_name'].label == 'Surname')
'''
    def test_author_form_first_name_field_widget(self):
        form = AuthorForm()        
        self.assertTrue(form.fields['first_name'].placeholder == None or form.fields['first_name'].placeholder == 'write author name')
'''
'''
    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text,'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())
'''