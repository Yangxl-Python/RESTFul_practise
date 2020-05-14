from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Press(BaseModel):
    press_name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)

    class Meta:
        db_table = 'bz_press'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name


class Author(BaseModel):
    author_name = models.CharField(max_length=128)
    age = models.SmallIntegerField()

    class Meta:
        db_table = 'bz_author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name


class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)
    author = models.OneToOneField(to=Author,
                                  on_delete=models.CASCADE,
                                  related_name='detail')

    class Meta:
        db_table = 'bz_author_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.author.author_name}的详情'


class Books(BaseModel):
    book_name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    authors = models.ManyToManyField(to=Author,
                                     db_constraint=False,
                                     related_name='books')
    publish = models.ForeignKey(to=Press,
                                on_delete=models.CASCADE,
                                db_constraint=False,
                                related_name='books')

    @property
    def authors_info(self):
        return self.authors.values('author_name', 'age', 'detail__phone')

    @property
    def publish_name(self):
        return self.publish.press_name

    class Meta:
        db_table = 'bz_books'
        verbose_name = '图书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name
