from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
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
from django.http import JsonResponse



# import json
# from django.core.serializers.json import DjangoJSONEncoder

import xlwt

from django.http import HttpResponse

import logging.config

# Create your views here.

from .models import PrintOrder, DoneSteps
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
    redirect_to = request.GET.get('next', '')
    print('THIS IS URL: ' + redirect_to)
    if request.method == "POST":
        form = NewOrderForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            # messages.success(request, 'Дані успішно збережено', extra_tags='alert alert-success')
            # return render(request, 'home.html', locals())
            return redirect(redirect_to)
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

# def check_print_status(request):
#     if request.method == "GET":
#         print_status = request.GET["print_status"]

#         statuses = PrintStatus.objects.all()
#         # statuses = json.dumps(all_statuses) 
#         print(statuses)
#         for share in statuses:
#             print (share.status)

#         if print_status in statuses:
#             return HttpResponse("ok", content_type='text/html')
#         else:
#             return HttpResponse("no", content_type='text/html')
#     return HttpResponse("no", content_type='text/html')

# @login_required
# def description_edit(request, pk):
#     # orders = PrintOrder.objects.filter(pk=pk).select_related('tmp_updated_by').order_by('-created')
#     field_name = 'number'
#     edit_description = PrintOrder.objects.filter(pk=pk).select_related('tmp_updated_by').order_by('-created')
#     field_value = getattr(edit_description, field_name)
#     if request.method == "POST":
#         form_nd = EditDescForm(request.POST, instance=edit_description)
#         if form_nd.is_valid():
#             edit_description = form_nd.save(commit=False)
#             # edit_description.tmp_updated_by = request.user
#             edit_description.save()
#             return redirect('home')
#     else:
#         form_nd = EditDescForm(instance=edit_description)
#
#     return render(request, 'edit_description.html', locals())

@login_required
def description_edit(request, pk):
    comments = DoneSteps.objects.filter(print_order_id = pk).order_by('-created_on')
    edit_description = get_object_or_404(PrintOrder, pk=pk)
    redirect_to = request.GET.get('next', '')
    number_value = getattr(edit_description, 'number')
    if request.method == "POST":
        form_nd = EditDescForm(request.POST, instance=edit_description)
        if form_nd.is_valid():
            edit_description = form_nd.save(commit=False)
            edit_description.save()
            return redirect(redirect_to)
    else:
        form_nd = EditDescForm(instance=edit_description)
    return render(request, 'edit_description.html', {'form_nd':form_nd, 'edit_description':edit_description, 'comments': comments, 'number_value':number_value})

class AddCommentView(LoginRequiredMixin, CreateView):
    model = DoneSteps
    form_class = EditDoneStepsForm
    context_object_name = "comment_record"
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        self.object = None
        self.contact = get_object_or_404(PrintOrder, id=request.POST.get('editdescription'))
        self.nmb = int(request.POST.get('nmb'))
        # print(self.contact)
        form = self.get_form()
        # print(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
           

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.created_by = self.request.user
        comment.updated_by = self.request.user
        comment.print_order = self.contact
        comment.tmp_number = self.nmb
        comment.save()
        # print(comment)
        return JsonResponse({
            "comment_id": comment.id, "tmp_number": comment.tmp_number,
            "created_on": comment.created_on,
            "created_by": comment.created_by.username,
            "updated_by": comment.updated_by.username
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['tmp_number'].errors})

class DeleteCommentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(DoneSteps, id=request.POST.get("comment_id"))
        if request.user == self.object.created_by:
            self.object.delete()
            data = {"cid": request.POST.get("comment_id"), "val": request.POST.get("")}
            return JsonResponse(data)

        data = {'error': "Ви не маєте прав на видалення цього коментаря."}
        return JsonResponse(data)


class UpdateCommentView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.comment_obj = get_object_or_404(DoneSteps, id=request.POST.get("commentid"))
        self.nmb = int(request.POST.get('comment'))
        if request.user == self.comment_obj.created_by or request.user.is_superuser:
            form = EditDoneStepsForm(request.POST, instance=self.comment_obj)
            if form.is_valid():
                return self.form_valid(form)

            return self.form_invalid(form)

        data = {'error': "Ви не можете редагувати кількість виконаного іншого користувача."}
        return JsonResponse(data)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.updated_by = self.request.user
        comment.tmp_number = self.nmb
        comment.updated = timezone.now()
        comment.save(update_fields=["tmp_number", "updated_by", "updated"])
        # print(comment)
        return JsonResponse({
            "comment_id": comment.id, "tmp_number": comment.tmp_number,
            "created_on": comment.created_on,
            "updated_on": comment.updated,
            "created_by": comment.created_by.username,
            "updated_by": comment.updated_by.username,

        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['tmp_number'].errors})

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