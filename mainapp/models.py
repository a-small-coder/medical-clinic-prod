import json

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from django.utils import timezone

User = get_user_model()
male = 'male'
female = "female"
any_gender = 'any'
GENDER_CHOICES = [
    (male, 'мужской'),
    (female, 'женский'),
    (any_gender, 'любой'),
]

OFFICE = 'OFFICE'
AT_HOME = "AT_HOME"
ADDRESS_TYPE = [
    (OFFICE, 'В офисе'),
    (AT_HOME, 'Выезд на дом'),
]

IN_PROCESSING = 'IN_PROCESSING'
CONFIRMED = "CONFIRMED"
WAIT_PAYMENT = "WAIT_PAYMENT"
PAID = "PAID"
WAIT_RESULTS = "WAIT_RESULTS"
COMPLETED = "COMPLETED"
CANCELED = "CANCELED"
ORDER_STATUSES = [
    (IN_PROCESSING, 'В обработке'),
    (WAIT_PAYMENT, 'В ожидании оплаты'),
    (PAID, 'Оплачен'),
    (WAIT_RESULTS, 'В ожидании результатов'),
    (COMPLETED, 'Завершен'),
    (CANCELED, 'Отменен'),
]


# ================================================================================
# =============================Navigation=========================================
# ================================================================================
class NavigationCategory(models.Model):
    category = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category


class SubNavigationCategory(models.Model):
    navigation_category = models.ForeignKey(NavigationCategory, verbose_name='Имя категории', on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=255, verbose_name='Имя подкатегории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.sub_category} | {self.navigation_category}"


# ================================================================================
# ==============================Other=============================================
# ================================================================================
class SearchGroup(models.Model):
    title = models.CharField(max_length=255, verbose_name='Группа исследований')
    slug = models.SlugField(unique=True)
    complex_type = models.ForeignKey(
        "ComplexType", verbose_name='Основной тип комплексов анализов', on_delete=models.CASCADE, null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.complex_type})"


class AboutUsCategory(models.Model):

    category = models.CharField(max_length=127, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category


class AboutUsContentBlock(models.Model):

    category = models.ForeignKey(AboutUsCategory, verbose_name='Принадлежит категории:', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок блока')
    text = models.TextField(verbose_name='Основной текст:')

    def __str__(self):
        return f'${self.title} | ${self.category}'


class OurAchievements(models.Model):

    title = models.CharField(max_length=63, verbose_name='Заголовок')
    text = models.CharField(max_length=127, verbose_name='Краткое описание')
    icon = models.ImageField(verbose_name='Иконка', upload_to='achievements')
    in_archive = models.BooleanField(verbose_name='В архиве', default=False)

    def __str__(self):
        return self.title


class ComplexType(models.Model):

    complex_type = models.CharField(max_length=255, verbose_name="Тип комплекса")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.complex_type


# ================================================================================
# ==============================Products=========================================
# ================================================================================
class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    title_min = models.CharField(max_length=40, verbose_name="Краткое название")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена ', default=0.00)
    preview_description = models.TextField(
        verbose_name='Краткое описание (до 100 знаков)', default='Описание появится позже'
    )
    slug = models.SlugField(unique=True,)

    def __str__(self):
        return self.title_min


class AnalyzeComplex(Product):

    complex_type = models.ForeignKey(ComplexType, verbose_name="Тип комплекса", on_delete=models.CASCADE)
    gender = models.CharField(max_length=32, choices=GENDER_CHOICES, verbose_name="Гендер ", default=any_gender)
    is_popular = models.BooleanField(default=False, verbose_name="Популярный товар")
    in_top_five_list = models.BooleanField(
        default=False, verbose_name='Входит в Топ-5 косплексов (добавить на слайдер компексов)'
    )
    on_main_page = models.BooleanField(default=False, verbose_name='Добавить на главный слайдер')
    big_image = models.ImageField(
        verbose_name='Изображение для главного слайдера главной странице', null=True,
        blank=True, upload_to='complexes/main-slider')
    small_image = models.ImageField(
        verbose_name='Изображение для слайдера комплексов на главной странице', null=True,
        blank=True, upload_to='complexes/complex-slider')

    def __str__(self):
        return f"{self.id} | {self.complex_type} | {self.title_min}"

    def save(self, *args, **kwargs):
        if self.id:
            print(Analyze.objects.filter(complex=self))
            self.price = sum([cproduct.price for cproduct in Analyze.objects.filter(complex=self)])
        super().save(*args, **kwargs)


class Analyze(Product):
    complex = models.ForeignKey(AnalyzeComplex, verbose_name="Входит в комплекс", on_delete=models.PROTECT, null=True,
                                blank=True)
    search_group = models.ForeignKey(SearchGroup, verbose_name='В ходит в группу исследований',
                                     on_delete=models.PROTECT)
    gender = models.CharField(max_length=32, choices=GENDER_CHOICES, verbose_name="Гендер ", default=any_gender)
    time = models.CharField(max_length=31, verbose_name='Срок исполнения')
    is_popular = models.BooleanField(default=False, verbose_name="Популярный товар")
    vendor_code = models.CharField(verbose_name='Артикул', max_length=63)
    is_unic = models.BooleanField(default=False, verbose_name='Уникальный анализ')
    small_image = models.ImageField(
        verbose_name='Изображение для уникальных анализов на главной странице',
        null=True, blank=True, upload_to='analyzes')

    def __str__(self):
        return f"{self.title_min} ({self.search_group})"


class AnalyzeContentBlock(models.Model):
    DESCRIPTION = 'DESCRIPTION'
    PREPARATIONS = "PREPARATIONS"
    INDICATIONS_FOR_USE = 'INDICATIONS_FOR_USE'
    FEEDBACK = 'FEEDBACK'
    CONTENT_CATEGORY_CHOICES = [
        (DESCRIPTION, 'Описание'),
        (PREPARATIONS, 'Подготовка'),
        (INDICATIONS_FOR_USE, 'Показания к применению'),
        (FEEDBACK, 'Интерпретация результатов'),
    ]
    analyze = models.ForeignKey(Analyze, on_delete=models.CASCADE, verbose_name='Для анализа')
    analyze_content_category = models.CharField(
        max_length=32, verbose_name='Категория блока', choices=CONTENT_CATEGORY_CHOICES, default=DESCRIPTION
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок блока')
    text = models.TextField(verbose_name='Текст блока', default="")
    pos = models.PositiveIntegerField(verbose_name='Позиция вывода на странице (от 1 до 10)', default=1)

    def __str__(self):
        return f"{self.analyze} | {self.analyze_content_category} | {self.title}"


# ================================================================================
# ===============================Cart=============================================
# ================================================================================
class CartItem(models.Model):
    cart = models.ForeignKey(
        'Cart', on_delete=models.CASCADE,
        verbose_name='Корзина', related_name='cart_items')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество товара')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0.00)

    def __str__(self):
        return "Товар: {} (для корзины)".format(self.product.title_min)

    @property
    def get_final_price(self):
        total = self.product.price * self.qty
        return total

    def save(self, *args, **kwargs):
        if self.id:
            self.final_price = self.get_final_price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey(
        'Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0.00)
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество товара')

    def __str__(self):
        return f"{str(self.id)} | {self.owner}"

    def save(self, *args, **kwargs):
        if self.id:
            self.total_price = self.get_cart_total
            self.qty = self.get_cart_items_count
        super().save(*args, **kwargs)

    @property
    def get_cart_total(self):
        orders_items = self.cart_items.all()
        total = sum([item.get_final_price for item in orders_items])
        return total

    @property
    def get_cart_items_count(self):
        orders_items = self.cart_items.all()
        total = sum([item.qty for item in orders_items])
        return total

    def put_in_order(self):
        self.in_order = True
        self.for_anonymous_user = False
        self.save()


class Customer(models.Model):

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=127, verbose_name='Имя', null=True, default=None)
    second_name = models.CharField(max_length=127, verbose_name='Фамилия', null=True, default=None)
    father_name = models.CharField(max_length=127, verbose_name='Отчество', null=True, default=None)
    phone = models.CharField(max_length=20, verbose_name='Номер', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    def __str__(self):
        if not (self.first_name and self.second_name):
            return self.user.username
        return "Покупатель {} {}".format(self.first_name, self.second_name)

    @property
    def get_full_name(self):
        return f'{self.second_name} {self.first_name} {self.father_name}'


class Order(models.Model):

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.PROTECT)
    cart = models.ForeignKey(Cart, verbose_name='Товары', on_delete=models.PROTECT)

    email = models.EmailField(verbose_name='почта для рассылки оповещений', null=True, default=None)
    phone = models.CharField(max_length=127, verbose_name='Номер телефона', null=True, default=None)
    customer_full_name = models.CharField(max_length=127, verbose_name='ФИО покупателя', null=True, default=None)

    place = models.CharField(max_length=255, verbose_name='Адрес', null=True)
    place_type = models.CharField(max_length=8, choices=ADDRESS_TYPE, default=None, verbose_name='Тип адреса')
    status = models.CharField(max_length=32, choices=ORDER_STATUSES, default=IN_PROCESSING, verbose_name='Статус')
    date_create = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    date_done = models.DateTimeField(verbose_name='Дата завершения (автоматически)', null=True, default=None, blank=True)

    def __str__(self):
        return f'Заказ №{self.id} {self.customer}'

    def save(self, *args, **kwargs):
        if self.status == "COMPLETED" or self.status == "CANCELED":
            self.date_done = timezone.now()
        super(Order, self).save(*args, **kwargs)
