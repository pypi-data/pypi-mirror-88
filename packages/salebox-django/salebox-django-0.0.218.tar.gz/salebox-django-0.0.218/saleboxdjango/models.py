from random import randint
import datetime
import pytz
import time
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models import Avg
from django.utils.timezone import now
from django.utils.translation import get_language

from mptt.models import MPTTModel, TreeForeignKey
from saleboxdjango.lib.common import get_rating_display, json_to_datetime_local, json_to_datetime_utc


CHECKOUT_STATUS_CHOICES = (
    (10, 'New: Pending send to gateway'),
    (20, 'Pending: Awaiting gateway response'),
    (30, 'Success: Pending POST to Salebox'),
    (31, 'Success: Successfully POSTed to Salebox'),
    (40, 'Rejected: Gateway rejected payment'),
    (50, 'Timeout: Gateway did not respond in an acceptable time period')
)

class Analytic(models.Model):
    key = models.UUIDField(db_index=True, editable=False)
    first_seen = models.DateTimeField(auto_now_add=True, db_index=True)
    last_seen = models.DateTimeField(auto_now=True)
    page_views = models.IntegerField(default=1)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    ip_country = models.CharField(max_length=5, blank=True, null=True, verbose_name="Country")
    ip_city = models.CharField(max_length=32, blank=True, null=True, verbose_name="City")
    ip_tz = models.CharField(max_length=32, blank=True, null=True, verbose_name="Timezone")
    ip_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitude")
    ip_lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitude")
    ua_browser_family = models.CharField(max_length=32, blank=True, null=True, verbose_name="Browser family")
    ua_browser_version = models.CharField(max_length=20, blank=True, null=True, verbose_name="Browser version")
    ua_os_family = models.CharField(max_length=20, blank=True, null=True, verbose_name="OS family")
    ua_os_version = models.CharField(max_length=20, blank=True, null=True, verbose_name="OS version")
    ua_device_family = models.CharField(max_length=32, blank=True, null=True, verbose_name="Device family")
    ua_device_brand = models.CharField(max_length=20, blank=True, null=True, verbose_name="Device brand")
    ua_device_model = models.CharField(max_length=20, blank=True, null=True, verbose_name="Device model")
    ua_is_mobile = models.BooleanField(null=True, verbose_name="Is mobile?")
    ua_is_tablet = models.BooleanField(null=True, verbose_name="Is tablet?")
    ua_is_touch_capable = models.BooleanField(null=True, verbose_name="Is touchscreen?")
    ua_is_pc = models.BooleanField(null=True, verbose_name="Is PC?")
    ua_is_bot = models.BooleanField(null=True, verbose_name="Is bot?")
    language = models.CharField(max_length=10, blank=True, null=True)
    screen_width = models.IntegerField(blank=True, null=True)
    screen_height = models.IntegerField(blank=True, null=True)

class Attribute(models.Model):
    code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']
        verbose_name = 'Product Attribute'

    def delete(self):
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.clear()

class AttributeItem(models.Model):
    attribute = models.ForeignKey(Attribute, blank=True, null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    delete_dt = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value

    class Meta:
        ordering = ['value']
        verbose_name = 'Product Attribute Item'

    def delete(self):
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.clear()

class BasketWishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    session = models.CharField(max_length=32, blank=True, null=True)
    basket_flag = models.BooleanField(default=True)
    variant = models.ForeignKey('ProductVariant', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    weight = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.session is None and self.user is None:
            self.session = '.'
        super().save(*args, **kwargs)

class CallbackStore(models.Model):
    ip_address = models.GenericIPAddressField()
    method = models.CharField(max_length=7)
    post = JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

class CheckoutStoreManager(models.Manager):
    def apply_timeout(self):
        """
        here we timeout checkout stores that have overrun a
        time limit and no message has been received from the
        payment gateway

        example config:

        SALEBOX = {
            ...
            'GATEWAY': {
                'TIMEOUT': {
                    'DEFAULT': 60 * 60 * 24 * 2,
                    'PAYMENT_METHODS': {
                        1: 60 * 30, # 30 minutes
                        12: 60 * 60 * 6, # 6 hours
                    }
                }
            }
            ...
        }
        """

        # get values from the config
        sb = getattr(settings, 'SALEBOX', {})
        gw = getattr(sb, 'GATEWAY', {})
        to = getattr(gw, 'TIMEOUT', {})
        default_timeout = getattr(to, 'DEFAULT', 60 * 60 * 24 * 3)
        payment_methods = getattr(to, 'PAYMENT_METHODS', {})

        # perform default timeout
        cutoff = now() - datetime.timedelta(seconds=default_timeout)
        checkouts_closed = CheckoutStore \
                            .objects \
                            .filter(status__lt=30) \
                            .filter(created__lt=cutoff) \
                            .update(status=50)

        # find all open checkouts older than the minimum cutoff
        try:
            min_seconds = min([payment_methods[k] for k in payment_methods])
            cutoff = now() - datetime.timedelta(seconds=min_seconds)
            open_checkouts = CheckoutStore \
                                .objects \
                                .filter(status__lt=30) \
                                .filter(created__lt=cutoff)

            # loop through those checkouts, timing out those that need it
            for oc in open_checkouts:
                try:
                    method_id = oc.data['payment_method']['id']
                    ttl = payment_methods[method_id]
                    if oc.created + datetime.timedelta(seconds=ttl) < now():
                        oc.status = 50
                        oc.save()
                        checkouts_closed += 1
                except:
                    pass
        except:
            pass

        # if any checkout stores were timed out, recalculate
        # the checkout stock levels
        if checkouts_closed > 0:
            CheckoutStore.objects.update_checked_out_stock()

    def update_checked_out_stock(self):
        stock = {}

        # find the quantities of stock checked-out
        stores = CheckoutStore \
                    .objects \
                    .filter(status__lt=31)
        for store in stores:
            for item in store.data['basket']['items']:
                variant_id = item['variant']['id']
                if variant_id not in stock:
                    stock[variant_id] = 0
                stock[variant_id] += item['qty']

        # update the positive quantities in the DB
        variants = ProductVariant \
                    .objects \
                    .filter(id__in=list(stock.keys()))
        for pv in variants:
            if pv.stock_checked_out != stock[pv.id]:
                pv.set_stock_checked_out(stock[pv.id])

        # update the zero quantities in the DB
        variants = ProductVariant \
                    .objects \
                    .exclude(id__in=list(stock.keys())) \
                    .exclude(stock_checked_out=0)
        for pv in variants:
            pv.set_stock_checked_out(0)

class CheckoutStore(models.Model):
    objects = CheckoutStoreManager()

    uuid = models.UUIDField(db_index=True)
    visible_id = models.CharField(max_length=14, unique=True)
    user = models.IntegerField(blank=True, null=True)
    gateway_code = models.CharField(max_length=12)
    status = models.IntegerField(choices=CHECKOUT_STATUS_CHOICES)
    data = JSONField()
    payment_received = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # create a uuid if none exists
        if self.uuid is None:
            self.uuid = str(uuid.uuid4())

        # create a visible_id if none exists
        if self.visible_id is None:
            self.visible_id = '%.2f' % time.time()
            self.visible_id = self.visible_id.replace('.', '')
            chars = 'BCDFGHJKLMNPQRSTWXY'
            while len(self.visible_id) < 14:
                self.visible_id = '%s%s' % (
                    self.visible_id,
                    chars[randint(1, len(chars)) - 1]
                )

        # save
        super().save(*args, **kwargs)

        # update checked-out stock levels
        CheckoutStore.objects.update_checked_out_stock()

    def set_status(self, status):
        if self.status != status:
            # set the payment_recieved datetime if applicable
            if status == 30:
                if settings.SALEBOX['CHECKOUT']['TRANSACTION_DATE'] == 'payment':
                    self.payment_received = datetime.datetime.now(tz=pytz.utc)

            # update the status
            self.status = status
            self.save()

class CheckoutStoreUpdate(models.Model):
    store = models.ForeignKey(CheckoutStore, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CHECKOUT_STATUS_CHOICES)
    data = JSONField()
    created = models.DateTimeField(auto_now_add=True)

class Country(models.Model):
    code = models.CharField(max_length=2, blank=True, null=True)
    default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Countries'

class CountryState(models.Model):
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, blank=True, null=True)
    full_code = models.CharField(max_length=8, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_code

    class Meta:
        ordering = ['full_code']
        verbose_name_plural = 'Country States'

class DiscountGroup(models.Model):
    GROUP_TYPE_CHOICES = (
        ('S', 'Seasonal'),
        ('M', 'Manual')
    )
    FIELD_CHOICES = (
        (0, 'Inactive'),
        (1, 'Active, not required'),
        (2, 'Active, required'),
    )
    ROUNDING_CHOICES = (
        ('none', 'No rounding'),
        ('up_major_1', 'Round UP to nearest major unit'),
        ('up_major_5', 'Round UP to nearest major unit multiple of 5'),
        ('up_major_10', 'Round UP to nearest major unit multiple of 10'),
    )
    name = models.CharField(max_length=25)
    group_type = models.CharField(max_length=1, default='M', choices=GROUP_TYPE_CHOICES)
    operational_flag = models.BooleanField(default=False)
    active_flag = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Discount Group'

    def delete(self):
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.clear()

class DiscountRuleset(models.Model):
    TYPE_CHOICES = (
        ('flat_percent', 'Flat Percentage'),
    )
    group = models.ForeignKey(DiscountGroup, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    discount_type = models.CharField(default='flat_percent', max_length=12, choices=TYPE_CHOICES)
    value = models.IntegerField(null=True, blank=True)
    start_dt = models.DateTimeField(null=True, blank=True)
    end_dt = models.DateTimeField(null=True, blank=True)
    product_variant = models.ManyToManyField('ProductVariant', blank=True)
    operational_flag = models.BooleanField(default=True)
    active_flag = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Discount Ruleset'

    def delete(self):
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.clear()

class Event(models.Model):
    event = models.CharField(max_length=50)
    transaction_guid = models.CharField(max_length=20, blank=True, null=True)
    salebox_member_id = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    processed_flag = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        # do not add duplicates
        if self.id is None:
            duplicate = Event \
                            .objects \
                            .filter(event=self.event) \
                            .filter(transaction_guid=self.transaction_guid) \
                            .filter(salebox_member_id=self.salebox_member_id) \
                            .filter(processed_flag=False) \
                            .count() > 0
            if duplicate:
                return
        super().save(*args, **kwargs)

class LastUpdate(models.Model):
    code = models.CharField(max_length=36)
    value = models.FloatField(default=0.0)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']
        verbose_name = 'Last Update'

class MemberGroup(models.Model):
    name = models.CharField(max_length=50)
    flat_discount_percentage = models.FloatField(default=0)
    can_be_parent = models.BooleanField(default=True)
    default_group = models.BooleanField(default=False)
    active_flag = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Member Group'

    def delete(self):
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.clear()

class Member(models.Model):
    TITLE_CHOICES = (
        (1, 'Mr'),
        (2, 'Mrs'),
        (3, 'Miss'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unspecified'),
    )
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('R', 'Resigned'),
        ('S', 'Suspended'),
        ('T', 'Terminated'),
    )
    # id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(MemberGroup, null=True, blank=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('Member', null=True, blank=True, on_delete=models.CASCADE)
    guid = models.CharField(max_length=25, db_index=True)
    salebox_member_id = models.UUIDField(
        blank=True,
        db_index=True,
        editable=True,
        null=True
    )
    gender = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_CHOICES)
    title = models.IntegerField(blank=True, null=True, choices=TITLE_CHOICES)
    name_first = models.CharField(max_length=20, blank=True, null=True)
    name_last = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address_1 = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    address_3 = models.CharField(max_length=255, blank=True, null=True)
    address_4 = models.CharField(max_length=255, blank=True, null=True)
    address_5 = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=12, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    country_state = models.ForeignKey(CountryState, blank=True, null=True, on_delete=models.CASCADE)
    phone_1 = models.CharField(max_length=20, blank=True, null=True)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    id_card = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=1, default='A', choices=STATUS_CHOICES)
    active_flag = models.BooleanField(default=True)
    join_date = models.DateField(blank=True, null=True)
    string_1 = models.CharField(max_length=255, blank=True, null=True)
    string_2 = models.CharField(max_length=255, blank=True, null=True)
    string_3 = models.CharField(max_length=255, blank=True, null=True)
    string_4 = models.CharField(max_length=255, blank=True, null=True)
    string_5 = models.CharField(max_length=255, blank=True, null=True)
    string_6 = models.CharField(max_length=255, blank=True, null=True)
    string_7 = models.CharField(max_length=255, blank=True, null=True)
    string_8 = models.CharField(max_length=255, blank=True, null=True)
    string_9 = models.CharField(max_length=255, blank=True, null=True)
    string_10 = models.CharField(max_length=255, blank=True, null=True)
    string_11 = models.CharField(max_length=255, blank=True, null=True)
    string_12 = models.CharField(max_length=255, blank=True, null=True)
    string_13 = models.CharField(max_length=255, blank=True, null=True)
    string_14 = models.CharField(max_length=255, blank=True, null=True)
    boolean_1 = models.BooleanField(default=False)
    boolean_2 = models.BooleanField(default=False)
    boolean_3 = models.BooleanField(default=False)
    boolean_4 = models.BooleanField(default=False)
    boolean_5 = models.BooleanField(default=False)
    boolean_6 = models.BooleanField(default=False)
    group_when_created = models.ForeignKey(MemberGroup, blank=True, null=True, related_name='group_when_created', on_delete=models.CASCADE)

    salebox_transactionhistory_request_dt = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    salebox_transactionhistory_count = models.IntegerField(default=0)
    salebox_transactionhistory_data = JSONField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.guid

    class Meta:
        ordering = ['guid']
        verbose_name = 'Member'

    def delete(self):
        pass

    def transactionhistory_request_sync(self):
        self.salebox_transactionhistory_request_dt = datetime.datetime.now()
        self.save()

    def transactionhistory_update_data(self, transaction_list):
        for t in transaction_list:
            del t['member']
        self.salebox_transactionhistory_data = transaction_list
        self.salebox_transactionhistory_count = len(transaction_list)
        self.salebox_transactionhistory_request_dt = None
        self.save()

    def transactionhistory_get_data(self):
        transactions = self.salebox_transactionhistory_data
        for t in transactions:
            t['dt'] = json_to_datetime_local(t['dt'])
            t['basket_size'] = 0
            for b in t['basket']:
                try:
                    pv = ProductVariant \
                            .objects \
                            .filter(id=b['product_variant']['id']) \
                            .select_related('product', 'product__category') \
                            .first()
                    b['product_variant'] = pv
                    b['product'] = pv.product
                    b['category'] = pv.product.category
                except:
                    pass
                t['basket_size'] += b['quantity']

        return transactions

    def transactionhistory_get_single_transaction(self, pos_guid):
        pos_guid = pos_guid.lower()
        for t in self.salebox_transactionhistory_data:
            if t['pos_guid'].lower() == pos_guid:
                return t

        return None

class ProductCategory(MPTTModel):
    short_name = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    image = models.CharField(max_length=70, blank=True, null=True)
    local_image = models.CharField(max_length=25, blank=True, null=True)
    seasonal_flag = models.BooleanField(default=False)
    slug = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    slug_path = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    active_flag = models.BooleanField(default=True)
    i18n = JSONField(default=dict)
    boolean_1 = models.BooleanField(default=False)
    boolean_2 = models.BooleanField(default=False)
    boolean_3 = models.BooleanField(default=False)
    boolean_4 = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def delete(self):
        pass

    def get_trans_for_lang(self, lang, field, fallback_to_primary=True, non_primary_fallback=None):
        if not hasattr(self, field):
            return '[BAD FIELD NAME]'

        i18n = self.i18n.get(lang, {})
        if field in i18n:
            return i18n[field]

        # fallback
        if fallback_to_primary:
            return getattr(self, field)
        else:
            return non_primary_fallback

    def get_trans(self, field, fallback_to_primary=True, non_primary_fallback=None):
        return self.get_trans_for_lang(get_language(), field, fallback_to_primary, non_primary_fallback)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        root = self.get_root()
        nodes = root.get_descendants(include_self=True)
        for node in nodes:
            slugs = node.get_ancestors(include_self=True).values_list('slug', flat=True)
            slugs = ['' if s is None else s for s in slugs]
            slug_path = '/'.join(slugs)
            if node.slug_path != slug_path:
                ProductCategory.objects.filter(id=node.id).update(slug_path=slug_path)
        cache.clear()

class Product(models.Model):
    SOLD_BY_CHOICES = (
        ('item', 'item'),
        # ('volume', 'volume'),
        ('weight', 'weight'),
    )
    category = models.ForeignKey(ProductCategory, blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    attribute_1 = models.ManyToManyField(AttributeItem, related_name='product_attr_1', blank=True)
    attribute_2 = models.ManyToManyField(AttributeItem, related_name='product_attr_2', blank=True)
    attribute_3 = models.ManyToManyField(AttributeItem, related_name='product_attr_3', blank=True)
    attribute_4 = models.ManyToManyField(AttributeItem, related_name='product_attr_4', blank=True)
    attribute_5 = models.ManyToManyField(AttributeItem, related_name='product_attr_5', blank=True)
    attribute_6 = models.ManyToManyField(AttributeItem, related_name='product_attr_6', blank=True)
    attribute_7 = models.ManyToManyField(AttributeItem, related_name='product_attr_7', blank=True)
    attribute_8 = models.ManyToManyField(AttributeItem, related_name='product_attr_8', blank=True)
    attribute_9 = models.ManyToManyField(AttributeItem, related_name='product_attr_9', blank=True)
    attribute_10 = models.ManyToManyField(AttributeItem, related_name='product_attr_10', blank=True)
    string_1 = models.CharField(max_length=150, blank=True, null=True)
    string_2 = models.CharField(max_length=150, blank=True, null=True)
    string_3 = models.CharField(max_length=150, blank=True, null=True)
    string_4 = models.CharField(max_length=150, blank=True, null=True)
    boolean_1 = models.BooleanField(default=False)
    boolean_2 = models.BooleanField(default=False)
    boolean_3 = models.BooleanField(default=False)
    boolean_4 = models.BooleanField(default=False)
    sold_by = models.CharField(max_length=6, choices=SOLD_BY_CHOICES, default='item')
    vat_applicable = models.BooleanField(default=True)
    image = models.CharField(max_length=70, blank=True, null=True)
    local_image = models.CharField(max_length=25, blank=True, null=True)
    inventory_type = models.CharField(max_length=1, default='T')
    # season = models.ForeignKey(OrganizationSeason, null=True, blank=True)
    slug = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    bestseller_rank = models.IntegerField(default=0)
    active_flag = models.BooleanField(default=True)
    i18n = JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    # local values
    rating_score = models.IntegerField(default=0)
    rating_vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'

    def delete(self):
        pass

    def get_trans_for_lang(self, lang, field, fallback_to_primary=True, non_primary_fallback=None):
        if not hasattr(self, field):
            return '[BAD FIELD NAME]'

        i18n = self.i18n.get(lang, {})
        if field in i18n:
            return i18n[field]

        # fallback
        if fallback_to_primary:
            return getattr(self, field)
        else:
            return non_primary_fallback

    def get_trans(self, field, fallback_to_primary=True, non_primary_fallback=None):
        return self.get_trans_for_lang(get_language(), field, fallback_to_primary, non_primary_fallback)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.clear()

    def update_rating(self):
        variant_ids = ProductVariant \
                        .objects \
                        .filter(product=self) \
                        .values_list('id', flat=True)

        self.rating_score = 0
        self.rating_vote_count = ProductVariantRating \
                                    .objects \
                                    .filter(variant__in=variant_ids) \
                                    .count()

        if self.rating_vote_count > 0:
            self.rating_score = ProductVariantRating \
                                    .objects \
                                    .filter(variant__in=variant_ids) \
                                    .aggregate(rating=Avg('rating'))['rating']

        self.save()

class ProductVariant(models.Model):
    SHELF_EXPIRY_CHOICES = (
        ('none', 'No shelf expiry date'),
        ('manual', 'Enter shelf expiry date manually'),
        ('delivery', 'Calculate from delivery date'),
        ('manufacture', 'Calculate from manufacture date'),
    )
    SIZE_UOM_CHOICES = (
        ('', 'n/a'),
        ('g', 'g'),
        ('kg', 'kg'),
        ('ml', 'ml'),
    )
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True, default='')
    bo_name = models.CharField(max_length=200, blank=True, default='')
    plu = models.CharField(max_length=25, blank=True, default='')
    sku = models.CharField(max_length=25, blank=True, default='')
    color = models.CharField(max_length=50, blank=True, default='')
    size = models.CharField(max_length=20, blank=True, default='')
    size_order = models.FloatField(default=0)
    size_uom = models.CharField(max_length=2, choices=SIZE_UOM_CHOICES, blank=True, default='')
    price = models.IntegerField(null=True)
    sale_price = models.IntegerField(default=0)
    sale_percent = models.IntegerField(default=0)
    barcode = models.CharField(max_length=50, blank=True, default='')
    available_to_order = models.BooleanField(default=True)
    available_on_pos = models.BooleanField(default=True)
    available_on_ecom = models.BooleanField(default=True)
    shelf_expiry_type = models.CharField(max_length=12, default='manual')
    shelf_life_days = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    image = models.CharField(max_length=70, blank=True, null=True)
    local_image = models.CharField(max_length=20, blank=True, null=True)
    unique_string = models.CharField(max_length=255, blank=True)
    shipping_weight = models.IntegerField(blank=True, null=True)
    loyalty_points = models.FloatField(blank=True, null=True)
    member_discount_applicable = models.BooleanField(default=True)
    string_1 = models.CharField(max_length=255, blank=True, null=True)
    string_2 = models.CharField(max_length=255, blank=True, null=True)
    string_3 = models.CharField(max_length=255, blank=True, null=True)
    string_4 = models.CharField(max_length=255, blank=True, null=True)
    string_5 = models.CharField(max_length=255, blank=True, null=True)
    warehouse_location = models.CharField(max_length=50, blank=True, null=True)
    int_1 = models.IntegerField(blank=True, null=True)
    int_2 = models.IntegerField(blank=True, null=True)
    int_3 = models.IntegerField(blank=True, null=True)
    int_4 = models.IntegerField(blank=True, null=True)
    date_1 = models.DateField(blank=True, null=True)
    date_2 = models.DateField(blank=True, null=True)
    boolean_1 = models.BooleanField(default=False)
    boolean_2 = models.BooleanField(default=False)
    boolean_3 = models.BooleanField(default=False)
    boolean_4 = models.BooleanField(default=False)
    attribute_1 = models.ManyToManyField(AttributeItem, related_name='variant_attr_1', blank=True)
    attribute_2 = models.ManyToManyField(AttributeItem, related_name='variant_attr_2', blank=True)
    attribute_3 = models.ManyToManyField(AttributeItem, related_name='variant_attr_3', blank=True)
    attribute_4 = models.ManyToManyField(AttributeItem, related_name='variant_attr_4', blank=True)
    attribute_5 = models.ManyToManyField(AttributeItem, related_name='variant_attr_5', blank=True)
    attribute_6 = models.ManyToManyField(AttributeItem, related_name='variant_attr_6', blank=True)
    attribute_7 = models.ManyToManyField(AttributeItem, related_name='variant_attr_7', blank=True)
    attribute_8 = models.ManyToManyField(AttributeItem, related_name='variant_attr_8', blank=True)
    attribute_9 = models.ManyToManyField(AttributeItem, related_name='variant_attr_9', blank=True)
    attribute_10 = models.ManyToManyField(AttributeItem, related_name='variant_attr_10', blank=True)
    active_flag = models.BooleanField(default=True)
    ecommerce_description = models.TextField(blank=True, null=True)
    ecommerce_low_stock_threshold = models.IntegerField(default=10)
    bestseller_rank = models.IntegerField(default=0)
    default_image = models.CharField(max_length=35, blank=True, null=True)
    i18n = JSONField(default=dict)
    preorder_flag = models.BooleanField(default=False)
    stock_count = models.IntegerField(default=0)
    stock_checked_out = models.IntegerField(default=0)
    stock_total = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    # local values
    rating_score = models.IntegerField(default=0)
    rating_vote_count = models.IntegerField(default=0)
    name_sorted = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name or ''

    class Meta:
        ordering = ['id']
        indexes = (
            models.Index(fields=('bestseller_rank', 'name_sorted')),
            models.Index(fields=('-bestseller_rank', 'name_sorted')),
            models.Index(fields=('sale_price', 'name_sorted')),
            models.Index(fields=('-sale_price', 'name_sorted')),
            models.Index(fields=('rating_score', 'name_sorted')),
            models.Index(fields=('-rating_score', 'name_sorted')),
        )
        verbose_name = 'Product Variant'

        # CREATE INDEX <name_of_index> ON saleboxdjango_productvariant (col_a ASC, col_b DESC)

    def delete(self):
        pass

    def get_trans_for_lang(self, lang, field, fallback_to_primary=True, non_primary_fallback=None):
        if not hasattr(self, field):
            return '[BAD FIELD NAME]'

        i18n = self.i18n.get(lang, {})
        if field in i18n:
            return i18n[field]

        # fallback
        if fallback_to_primary:
            return getattr(self, field)
        else:
            return non_primary_fallback

    def get_trans(self, field, fallback_to_primary=True, non_primary_fallback=None):
        return self.get_trans_for_lang(get_language(), field, fallback_to_primary, non_primary_fallback)

    def rating_display(self):
        return get_rating_display(self.rating_score, self.rating_vote_count)

    def save(self, *args, **kwargs):
        self.default_image = None

        # attempt to use first variant image
        pvi = ProductVariantImage \
                .objects \
                .filter(variant=self) \
                .filter(local_img__isnull=False) \
                .filter(active_flag=True) \
                .order_by('order') \
                .first()
        if pvi is not None:
            self.default_image = 'pvi/%s' % pvi.local_img

        # fallback to POS image if that exists
        if self.default_image is None and self.local_image is not None:
            self.default_image = 'pospv/%s' % self.local_image

        # set stock_total
        self.stock_total = max((self.stock_count - self.stock_checked_out), 0)

        # remove basket/wishlist item if variant now unavailable
        if not self.available_on_ecom or not self.active_flag:
            BasketWishlist.objects.filter(variant=self).delete()

        # save
        super(ProductVariant, self).save(*args, **kwargs)
        cache.clear()

    def set_stock_checked_out(self, qty=0):
        if self.id:
            ProductVariant \
                .objects \
                .filter(id=self.id) \
                .update(
                    stock_checked_out=qty,
                    stock_total=max((self.stock_count - qty), 0)
                )

    def update_rating(self):
        self.rating_score = 0
        self.rating_vote_count = \
            ProductVariantRating \
                .objects \
                .filter(variant=self) \
                .count()

        if self.rating_vote_count > 0:
            self.rating_score = \
                ProductVariantRating \
                    .objects \
                    .filter(variant=self) \
                    .aggregate(rating=Avg('rating'))['rating']

        self.save()
        self.product.update_rating()

class ProductVariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    img = models.CharField(max_length=100, default='')
    local_img = models.CharField(max_length=25, blank=True, null=True)
    img_height = models.IntegerField(default=0)
    img_width = models.IntegerField(default=0)
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    active_flag = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order',)

    def save(self, *args, **kwargs):
        super(ProductVariantImage, self).save(*args, **kwargs)
        self.variant.save()

class ProductVariantRating(models.Model):
    variant = models.ForeignKey('ProductVariant', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=50)
    review = models.TextField(blank=True, null=True)
    review_qc_flag = models.BooleanField(default=False)
    active_flag = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Variant Rating'

    def delete(self, *args, **kwargs):
        variant = self.variant
        super().delete(*args, **kwargs)
        variant.update_rating()

    def save(self, *args, **kwargs):
        if self.review is not None:
            self.review = self.review.strip()
            if len(self.review) == 0:
                self.review = None
        super().save(*args, **kwargs)
        self.variant.update_rating()

    def rating_10(self):
        try:
            return round(self.rating / 10)
        except:
            return None

    def rating_5(self):
        try:
            return round(self.rating / 20)
        except:
            return None

class SaleboxUser(AbstractUser):
    salebox_member_id = models.UUIDField(blank=True, db_index=True, editable=True, null=True)
    salebox_member_sync = JSONField(blank=True, null=True)
    salebox_last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def create_salebox_member_id(self):
        if self.salebox_member_id is None:
            self.salebox_member_id = str(uuid.uuid4())
            self.save()

    def get_member(self):
        if self.salebox_member_id is None:
            return None

        return Member \
                .objects \
                .filter(salebox_member_id=self.salebox_member_id) \
                .first()

    def set_salebox_member_sync(self, key, value):
        if self.salebox_member_sync is None:
            self.salebox_member_sync = {}
        self.salebox_member_sync[key] = value
        self.save()

class Translation(models.Model):
    language_code = models.CharField(max_length=7)
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['language_code', 'key']
        verbose_name = 'Translation'

    def delete(self):
        super().delete(*args, **kwargs)
        cache.clear()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.clear()

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)
    address_group = models.CharField(max_length=10, default='default')
    full_name = models.CharField(max_length=150)
    address_1 = models.CharField(max_length=150)
    address_2 = models.CharField(max_length=150, blank=True, null=True)
    address_3 = models.CharField(max_length=150, blank=True, null=True)
    address_4 = models.CharField(max_length=150, blank=True, null=True)
    address_5 = models.CharField(max_length=150, blank=True, null=True)
    country_state = models.ForeignKey(CountryState, blank=True, null=True, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    postcode = models.CharField(max_length=12, blank=True, null=True)
    phone_1 = models.CharField(max_length=20, blank=True, null=True)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    string_1 = models.CharField(max_length=255, blank=True, null=True)
    string_2 = models.CharField(max_length=255, blank=True, null=True)
    tax_id = models.CharField(max_length=36, blank=True, null=True)
    active_flag = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s, %s...' % (self.full_name, self.address_1)

    class Meta:
        ordering = ['-default', 'full_name', 'address_1']
        verbose_name = 'User Address'

    def delete(self, *args, **kwargs):
        user = self.user
        address_group = self.address_group
        super().delete(*args, **kwargs)
        self.ensure_one_default_exists(user, address_group)

    def save(self, *args, **kwargs):
        if self.tax_id is not None:
            self.tax_id = self.tax_id.strip()
            if len(self.tax_id) == 0:
                self.tax_id = None
        super().save(*args, **kwargs)
        self.ensure_one_default_exists(self.user, self.address_group)

    def ensure_one_default_exists(self, user, address_group):
        addresses = UserAddress \
                        .objects \
                        .filter(user=user) \
                        .filter(address_group=address_group) \
                        .order_by('-last_update')

        if len(addresses) > 0:
            default_count = 0

            # ensure in inactive addresses are marked as default
            for a in addresses.all():
                if not a.active_flag and a.default:
                    UserAddress.objects.filter(id=a.id).update(default=False)

            # ensure we have a maximum of one default
            for a in addresses.all():
                if a.default:
                    default_count += 1
                    if default_count > 1:
                        UserAddress.objects.filter(id=a.id).update(default=False)

            # if we don't have a default, set one
            if default_count == 0:
                for a in addresses.all():
                    if a.active_flag:
                        UserAddress.objects.filter(id=a.id).update(default=True)
                        break
