from django.db import models


class BooksAuthor(models.Model):
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = "books_author"


class BooksBook(models.Model):
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField(unique=True)
    media_type = models.CharField(max_length=16)
    title = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "books_book"


class BooksBookAuthors(models.Model):
    book = models.ForeignKey(BooksBook, models.DO_NOTHING)
    author = models.ForeignKey(BooksAuthor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "books_book_authors"
        unique_together = (("book", "author"),)


class BooksBookBookshelves(models.Model):
    book = models.ForeignKey(BooksBook, models.DO_NOTHING)
    bookshelf = models.ForeignKey("BooksBookshelf", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "books_book_bookshelves"
        unique_together = (("book", "bookshelf"),)


class BooksBookLanguages(models.Model):
    book = models.ForeignKey(BooksBook, models.DO_NOTHING)
    language = models.ForeignKey("BooksLanguage", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "books_book_languages"
        unique_together = (("book", "language"),)


class BooksBookSubjects(models.Model):
    book = models.ForeignKey(BooksBook, models.DO_NOTHING)
    subject = models.ForeignKey("BooksSubject", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "books_book_subjects"
        unique_together = (("book", "subject"),)


class BooksBookshelf(models.Model):
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = "books_bookshelf"


class BooksFormat(models.Model):
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(BooksBook, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "books_format"


class BooksLanguage(models.Model):
    code = models.CharField(unique=True, max_length=4)

    class Meta:
        managed = False
        db_table = "books_language"


class BooksSubject(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = "books_subject"

    def __str__(self):
        return super().__str__()
