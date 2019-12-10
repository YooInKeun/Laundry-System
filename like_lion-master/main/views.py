from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.db.models import Q
from . import views
from . import models
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from main.forms import CustomerForm, OrderForm, CustomerForm2, SearchForm
from django.contrib import messages
import csv
#from .resources import RequestResource
from django.http import HttpResponse
from django.contrib import messages
from twilio.rest import Client
from .forms import SendMessageForm
from accounts.models import User
from .models import Customer, Request
# in create


class WashView(TemplateView):
    template_name = "main/wash.html"

wash = WashView.as_view()


class CustomerView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "main/customer.html"

    def form_valid(self, form):
        post = form.save(commit = False)
        post.nickname = self.request.user
        post.save() 
        
        return redirect('main:wash')


customer = CustomerView.as_view()



class MessageView(ListView):
    template_name = "main/message.html"
    redirect_authenticated_user = True
    model = Customer

    def get_queryset(self):
        word = self.request.GET.getlist('word')
        queryset = super(MessageView, self).get_queryset()
        if word:
            queryset.filter(
                Q(phone_num__contains=word) |
                Q(name__contains=word)
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessageView, self).get_context_data(
            object_list=None, **kwargs)
        context['form'] = SearchForm()
        return context

    def get(self, request, *args, **kwargs):
        return super(MessageView, self).get(request, *args, **kwargs)


message = MessageView.as_view()


class ManageView(TemplateView):
    template_name = "main/manage.html"


manageView = ManageView.as_view()


def manage(request):
    request_info = Request.objects.all().select_related("phone_num")
    request_context = {'request_info': request_info}

    return render(request, 'main/manage.html', request_context)


def main(request):
    requests = Request.objects.all()
    return render(request, 'main/main.html', {'requests': requests})

def process(request, pk):
    processed_request = Request.objects.get(request_num=pk)
    processed_request.status = "처리 완료"
    processed_request.save()
    requests = Request.objects.all()
    return render(request, 'main/main.html', {'requests': requests})

def end_process(request, pk):
    end_processed_request = Request.objects.get(request_num=pk)
    end_processed_request.status = "수거 완료"
    end_processed_request.save()
    requests = Request.objects.all()
    return render(request, 'main/main.html', {'requests': requests})


def getOrder(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST, request.FILES)   
        if order_form.is_valid():
            order_info = Post(**form.cleaned_data)
            order_info.save()
            return HttpResponse("finish")

    elif request.method == 'GET':
        customer = CustomerForm2()
        order = OrderForm()
        return render(request, 'main/wash.html', {'customer': customer, 'order': order})
    else:
        pass


def searchCustomer(request):
    if request.method == "POST":
        form = CustomerForm2(request.POST)
        if form.is_valid():
            customer_list = Customer.objects.filter(
                phone_num=form.cleaned_data['phone_num'], name=form.cleaned_data['name'])
            print(customer_list)
            if len(customer_list) != 0:
                order = OrderForm()
                return render(request, 'main/wash2.html', {'customer': customer_list, 'order': order})
            else:
                context = 'g'
                form = CustomerForm2()
                return render(request, 'main/wash.html', {'customer': customer_list, 'customer': form, 'context': context})
    else:
        return render(request, 'main/wash.html', {'customer': customer_list, 'context': '회원 정보를 찾을 수 없습니다.'})
    # print(customer_list)


def saveCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="noname.csv"'

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))

    join_model = Request.objects.select_related('phone_num')

    writer.writerow([
        str(u"요청번호"),
        str(u"고객번호"),
        str(u"고객이름"),
        str(u"의류"),
        str(u"서비스 종류"),
        str(u"서비스 상태"),
        str(u"요청 날짜"),
        str(u"예상 날짜"),
        str(u"완료 날짜"),
        str(u"찾아간 날짜"),
        str(u"요청사항"),
        str(u"가격"),
        str(u"주소"),
        str(u"가입날짜"),
    ])

    for record in join_model:
        row = []
        row.append(record.request_num)
        row.append(record.phone_num.phone_num)
        row.append(record.phone_num.name)
        row.append(record.clothe.clothe)
        row.append(record.service.service)
        row.append(record.status)
        row.append(str(record.rqst_date))
        row.append(str(record.est_date))
        row.append(str(record.fin_date))
        row.append(str(record.rtrn_date))
        row.append(record.requirements)
        row.append(str(record.price))
        row.append(record.phone_num.address)
        row.append(record.phone_num.created_date)
        print(row)
        writer.writerow(row)

    return response


def message(request):
    form_class = SendMessageForm

    send_message_form = form_class(request.POST or None)
    if request.method == 'POST':

        #send_message_form = SendMessageForm(request.POST)

        if send_message_form.is_valid():
            account_sid = 'AC155820cd778430b90f0b858fb5635d9b'
            auth_token = '888b211e0bfd4cf40237999b30cfad8b'
            client = Client(account_sid, auth_token)

            customer_name = request.POST.get('customer_name')
            customer_number = request.POST.get('customer_number')
            input_number = '+82' + customer_number[1:]

            #category = request.POST.get('category')
            category = send_message_form.cleaned_data.get('category')
            input_message = request.POST.get('input_message')

            message = client.messages.create(
                body=customer_name + "님 " + input_message,
                from_='+12015819428',
                to=input_number
            )
            print(message.sid)
    # GET
    else:
        message = MessageView.as_view()

    context = {
        'form': send_message_form,
    }

    return render(request, 'main/message.html', context)
