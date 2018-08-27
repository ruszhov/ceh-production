from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.forms.formsets import formset_factory
from .forms import *
from django.shortcuts import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.views.generic import UpdateView, ListView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import xlwt

from django.http import HttpResponse

import logging.config

# Create your views here.

from .models import PrintOrder
from .forms import NewOrderForm
from .filters import PrintOrderFilter

def home(request):
    my_orders = PrintOrder.objects.all().select_related('name_of_camp', 'material', 'manager', 'status', 'created_by', 'updated_by').order_by('-created')
    all_orders = PrintOrderFilter(request.GET, queryset=my_orders)
    # print(all_orders)
    page = request.GET.get('page', 1)
    username = auth.get_user(request).username

    paginator = Paginator(all_orders.qs, 500)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request, 'home.html', locals())

@login_required
def new_campaign(request):
    campaigns = CampaignName.objects.all()
    if request.method == "POST":
        # print(request.POST)
        form_nc = NewCampaignForm(request.POST)
        if form_nc.is_valid():
            new_campaign = form_nc.save()
            return redirect('new_order')
    else:
        form_nc = NewCampaignForm()
    return render(request, 'new_campaign.html', locals())

@login_required
def new_order(request):
    order_formset = formset_factory(NewOrderForm)
    if request.method == 'POST':
        formset = order_formset(request.POST)
        if formset.is_valid():
            for form in formset:
                new_order = form.save(commit=False)
                new_order.created_by = request.user
                new_order.save()
            return redirect('home')
    else:
        formset = order_formset()
    return render(request, 'new_order.html', {'formset':formset})

@login_required
def order_edit(request, pk):
    post = get_object_or_404(PrintOrder, pk=pk)
    if request.method == "POST":
        form = NewOrderForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            # messages.success(request, 'Дані успішно збережено', extra_tags='alert alert-success')
            # return render(request, 'home.html', locals())
            return redirect('home')
    else:
        form = NewOrderForm(instance=post)
    return render(request, 'edit_order.html', locals())

@login_required
def status_edit(request, pk):
    edit_status = get_object_or_404(PrintOrder, pk=pk)
    if request.method == "POST":
        form_ns = EditStatusForm(request.POST, instance=edit_status)
        if form_ns.is_valid():
            edit_status = form_ns.save(commit=False)
            edit_status.updated_by = request.user
            edit_status.updated = timezone.now()
            edit_status.save()
            # messages.success(request, 'Дані успішно збережено', extra_tags='alert alert-success')
            # return render(request, 'home.html', locals())
            return redirect('home')
    else:
        form_ns = EditStatusForm(instance=edit_status)
    return render(request, 'edit_status.html', {'form':form_ns})

@login_required
def description_edit(request, pk):
    edit_description = get_object_or_404(PrintOrder, pk=pk)
    if request.method == "POST":
        form_nd = EditDescForm(request.POST, instance=edit_description)
        if form_nd.is_valid():
            edit_description = form_nd.save(commit=False)
            edit_description.save()
            return redirect('home')
    else:
        form_nd = EditDescForm(instance=edit_description)
    return render(request, 'edit_description.html', {'form':form_nd})


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=mymodel.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("MyModel")
    
    row_num = 0
    
    columns = [
        (u"ID", 2000),
        (u"Title", 6000),
        (u"Description", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for obj in queryset:
        row_num += 1
        row = [
            obj.pk,
            obj.title,
            obj.description,
        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
    
export_users_xls.short_description = u"Export XLS"