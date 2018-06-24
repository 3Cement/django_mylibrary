from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class Tag(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200, help_text="Enter a the book's tags (e.g. Businnes, Food, Programming, Training, Running etc.)")
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('tag-detail', args=[str(self.id)])


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(max_length=200, help_text="Enter a one book genre (e.g. Finances, Sport, Health etc.)")
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200, help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book', blank=True)
    tag = models.ManyToManyField(Tag, help_text='Select a tags for this book', blank=True)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
    formats = (
    	('p', 'Paperback'),
    	('e', 'Ebook'),
    	('a', 'Audiobook'),
    	)
    book_format = models.CharField(max_length=1, choices=formats, blank=True, default='p', help_text='Book format')
    read_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Book object."""
        return self.title


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["last_name","first_name"]
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Author object."""
        return '{0}, {1}'.format(self.last_name,self.first_name)

class FavouriteBook(models.Model):
    """Model representing a user fovourite book (i.e. that can be choosen from the library)."""
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    liking = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    #Model.validate_unique(exclude=pk)

    class Meta:
        ordering = ['-id']
        permissions = (("can_view_all_favourites", "See favourites"),
                     ("can_edit", "Edit book"),
                     ("can_mark_as_favourite", "Set book as favourite"),)
        unique_together = (('book', 'liking'),)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('favbook-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Favourite Book object"""
        return '{0} ({1})'.format(self.id, self.book)