from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.views.generic import CreateView,ListView,DetailView,DeleteView,TemplateView,FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin

from . import forms
from . import models 
from coupon.decorators import generator_required,validator_required

# Create your views here.
decorators= [login_required,generator_required]
class RedeemView(TemplateView):
    template_name='coupon/coupon_validate_form.html'


class GeneratorSignupView(CreateView):
    model = models.User
    form_class = forms.GeneratorSignUpForm
    template_name='signup_form.html'
    success_url =reverse_lazy('login')

    def get_context_data(self,**kwargs):
        kwargs['user_type']='generator'
        return super().get_context_data()

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('coupon:cafe_list')

class ValidatorSignupView(CreateView):
        model = models.User
        form_class = forms.ValidatorSignUpForm
        template_name='signup_form.html'
        success_url =reverse_lazy('login')

        def get_context_data(self,**kwargs):
            kwargs['user_type']='generator'
            return super().get_context_data()

        def form_valid(self, form):
            user = form.save()
            login(self.request, user)
            return redirect('coupon:cafe_list')

class CafeList(ListView):
	"""docstring for Cafe"""
	model= models.Cafe


class CouponList(ListView,LoginRequiredMixin,SelectRelatedMixin):
    """docstring for CouponList"""
    model=models.Coupon
    select_related = ("user")
        
	
class CafeDetail(DetailView):
	model= models.Cafe

class CreateCafe(CreateView):
        model=models.Cafe
        fields=('cafeName','cafeAddress')

        # @method_decorator(decorators)
        def form_valid(self,form):
            self.object= form.save(commit=False)
            self.object.generate_cafe_code()
            self.object.save()
            return super().form_valid(form)

        def get_suucess_url(self,**kwargs):
            return reverse_lazy('home')



class CreateCoupon(CreateView):
        model=models.Coupon
        form_class= forms.CouponForm
        redirect_field_name = 'coupon/cafe_detail.html'
        template_name='coupon/coupon_generate_form.html'


        @method_decorator(decorators)
        def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.user = self.request.user

            self.object.generate_coupon_id(self)
            self.object.save()
            return super().form_valid(form)

        def get_success_url(self, **kwargs):         
            if  kwargs != None:
                return reverse_lazy('coupon:send_sms', kwargs = {'id': self.coupon_id,'cafe':self.cafe.cafeName,'discount':self.discount,'validity':self.end_date,'mobile_no':self.mob_number})
            else:
                return reverse_lazy('coupon:cafe_detail', args = (self.cafe.pk,))


def send_sms_api(request, **kwargs):
    

    message = "Lucky Offer. Here's a discount coupon of " + str(kwargs.get("discount"))+" % from" + kwargs.get("cafe") +"valid till "+ kwargs.get("validity")
    mobile_number=kwargs.get("mob_number")
    payload = {
        'sender': 'discount',
        'route': '4',
        'country': '91',
        'authkey': 'authkey',
        'message': message,
        'mobiles': mobile_number
            }
    r = requests.get('http://api.msg91.com/api/sendhttp.php', params=payload)

    if(r.status_code==200):
        
        messages.success(request, 'Message sent successfully.')
        
        
        json = {
            'success': True,
            'message': message
        }
        return JsonResponse(json)
        

    error = "Error sending sms. Status code: {}".r.status_code
    json = {
        'success': False,
        'error': error
    }
    
    return JsonResponse(json)



@login_required
@validator_required
def validation(request,*args,**kwargs):

        entry = Cafe.objects.get(cafeCode=kwargs.get("cafeCoupon")[:5])
        if Cafe.filter(pk=entry.pk).exists():
            checkCode= Coupon.objects.get(coupon_id=kwargs.get("cafeCoupon"))
            if Coupon.filter(pk=checkCode.pk,is_validated=False).exclude(end_date__lte=timezone.now()).exists():
                checkCode.is_validated=True
                checkCode.save()
                message=" discount applied :" + str(checkCode.discount)
                return HttpResponse(message)
            elif Coupon.filter(pk=checkCode.pk,is_validated=True).exclude(end_date__lte=timezone.now()).exists():
                return HttpResponse("Coupon Used")
        else:
            return HttpResponse("Invalid Coupon")

        return HttpResponse("Coupon does not belong to this cafe.")




# class DeleteCoupon( SelectRelatedMixin, generic.DeleteView):
#     model = models.Coupon
#     select_related = ("user", "cafe")
#     success_url = reverse_lazy("coupon:cafe_list")
#     @method_decorator(decorators)

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user_id=self.request.user.id)

#     def delete(self, *args, **kwargs):
#         messages.success(self.request, "Coupon Deleted")
#         return super().delete(*args, **kwargs)

# class SuggestionView(FormView):
#     form_class = TaskForm 
#     success_url = "/"
#     template_name = "todo/suggest.html"

#     def form_valid(self, form):
#         print(self.request.POST['name'])
#         print(self.request.POST['title'])
#         return super(SuggestionView, self).form_valid(form)

class RedeemView(TemplateView):
    template_name='coupon/coupon_validate_form.html'

def check_coupon(request):
    if request.method=='GET':
        coupon_form=forms.ValidateForm(data=request.GET)

        if coupon_form.is_valid():
            coupon=coupon_form.save()
            entry = Cafe.objects.get(cafeCode=coupon[:5])
            if Cafe.filter(pk=entry.pk).exists():
                checkCode= Coupon.objects.get(coupon_id=coupon)
                if Coupon.filter(pk=checkCode.pk,is_validated=False).exclude(end_date__lte=timezone.now()).exists():
                    checkCode.is_validated=True
                    checkCode.save()
                    message=" discount applied :" + str(checkCode.discount)
                    return HttpResponse(message)
                elif Coupon.filter(pk=checkCode.pk,is_validated=True).exclude(end_date__lte=timezone.now()).exists():
                    return HttpResponse("Coupon Used")
            else:
                return HttpResponse("Invalid Coupon")

            return HttpResponse("Coupon does not belong to this cafe.")



            # return reverse_lazy('coupon:validate',kwargs={'cafeCoupon':coupon.coupon_id})

    else:
        coupon_form=forms.ValidateForm()