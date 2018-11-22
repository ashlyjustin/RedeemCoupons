from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from django.urls import reverse
from django.core.validators import RegexValidator
# Create your models here.
class User(AbstractUser):
	is_generator = models.BooleanField(default=False)
	is_validator = models.BooleanField(default=False)


	def __str__(self):
		return self.username

class Cafe(models.Model):
	"""docstring for Coupon"""
	
	cafeName= models.CharField(max_length=255,unique=True)
	cafeCode= models.CharField(max_length=10,unique=True,null=False)
	cafeAddress=models.CharField(max_length=255,blank=True,null=True)
	
	def generate_cafe_code(self):
		x=self.cafeName[:3]
		self.cafeCode=x+str(uuid.uuid4().hex)[:2]
		self.save()

	def get_absolute_url(self):
		return reverse("coupon:cafe_detail",kwargs={'pk':self.pk,'cafeName':self.cafeName})

	def __str__(self):
		return self.cafeName

class Coupon(models.Model):
		user = models.ForeignKey(User,on_delete=models.CASCADE)
		cafe=models.ForeignKey(Cafe,related_name='cafe',on_delete=models.CASCADE)

		start_date=models.DateTimeField(default=timezone.now())
		end_date=models.DateTimeField()
		discount=models.IntegerField()

		phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
		mob_number = models.CharField(validators=[phone_regex], max_length=17) 
		coupon_id=models.IntegerField(max_length=10)
		is_validated= models.BooleanField(default=False)

		def generate_coupon_id(self):
			x=self.cafe.cafeCode
			self.coupon_id=x+str(uuid.uuid4().hex)[:5]
			self.save()

		def get_absolute_url(self):
			return reverse("coupon:coupon_list",kwargs={'user':self.user.username})

    # 	return reverse('coupon:send_sms', kwargs = {'id': self.coupon_id,'cafe':self.cafe.cafeName,'discount':self.discount,'validity':self.end_date,'mobile_no':self.mobile_no})