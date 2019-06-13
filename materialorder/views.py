from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.forms.formsets import formset_factory
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth

from django.contrib.auth.models import User
from .filters import MaterialOrderFilter
from django.http import HttpResponseRedirect

def materialorder(request):
    materialorder_list =  MaterialOrder.objects.all().select_related('provider', 'material', 'paint', 'other', 'created_by', 'updated_by').order_by('-created')
    material_filter = MaterialOrderFilter(request.GET, queryset=materialorder_list)
    # materialorder_list = material_filter.qs
    username = auth.get_user(request).username

    paginator = Paginator(material_filter.qs, 500)
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    args = {'paginator' : paginator, 'material_filter' : material_filter, 'orders' : orders}

    return render(request, 'materialorder/materialorder.html', args)

@login_required
def materialorder_new(request):

	# if request.method == "POST":
	# 	input_material_form = NewMaterialForm(request.POST or None)
	# 	print (request.POST)
	# 	if input_material_form.is_valid():
	# 		form = input_material_form.save()
	# 		return redirect('materialorder')
	# else:
	# 	form = NewMaterialForm()

	provider_form = NewProviderForm(request.POST or None)
	if request.method == "POST" and provider_form.is_valid():
		form_p = provider_form.save()
		return redirect('materialorder_new')
	else:
		form_p = NewProviderForm()

	material_in_form = NewMaterialInForm(request.POST or None)
	if request.method == "POST" and material_in_form.is_valid():
		form_m_in = material_in_form.save()
		return redirect('materialorder_new')
	else:
		form_m_in = NewMaterialInForm()

	paint_in_form = NewPaintInForm(request.POST or None)
	if request.method == "POST" and paint_in_form.is_valid():
		form_p_in = paint_in_form.save()
		return redirect('materialorder_new')
	else:
		form_p_in = NewPaintInForm()

	other_in_form = NewOtherInForm(request.POST or None)
	if request.method == "POST" and other_in_form.is_valid():
		form_o_in = other_in_form.save()
		return redirect('materialorder_new')
	else:
		form_o_in = NewOtherInForm()
		
	material_formset = formset_factory(NewMaterialForm)
	if request.method == 'POST':
		formset = material_formset(request.POST)
		if formset.is_valid():
			for form in formset:
				new_order = form.save(commit=False)
				new_order.created_by = request.user
				new_order.save()
			return redirect('materialorder')
	else:
		formset = material_formset()

	return render(request, 'materialorder/new_order.html', locals())

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
def materialorder_edit(request, pk):
    edit_material_order = get_object_or_404(MaterialOrder, pk=pk)

    provider_form = NewProviderForm(request.POST or None)
    if request.method == "POST" and provider_form.is_valid():
        form_p = provider_form.save()
        return redirect('materialorder_edit', pk=pk)
    else:
        form_p = NewProviderForm()

    material_in_form = NewMaterialInForm(request.POST or None)
    if request.method == "POST" and material_in_form.is_valid():
        form_m_in = material_in_form.save()
        return redirect('materialorder_edit', pk=pk)
    else:
        form_m_in = NewMaterialInForm()

    paint_in_form = NewPaintInForm(request.POST or None)
    if request.method == "POST" and paint_in_form.is_valid():
        form_p_in = paint_in_form.save()
        return redirect('materialorder_edit', pk=pk)
    else:
        form_p_in = NewPaintInForm()

    other_in_form = NewOtherInForm(request.POST or None)
    if request.method == "POST" and other_in_form.is_valid():
        form_o_in = other_in_form.save()
        return redirect('materialorder_edit', pk=pk)
    else:
        form_o_in = NewOtherInForm()

    if request.method == "POST":
        edit_material_order_form = NewMaterialForm(request.POST, instance=edit_material_order)
        if edit_material_order_form.is_valid():
            edit_material_order = edit_material_order_form.save(commit=False)
            edit_material_order.updated_by = request.user
            # print(request.user)
            edit_material_order.save()
            return redirect('materialorder')
    else:
        edit_material_order_form = NewMaterialForm(instance=edit_material_order)
    return render(request, 'materialorder/edit_order.html', locals())

# @login_required
# def paid_status(request, pk):
#     paid_status = get_object_or_404(MaterialOrder, pk=pk)
#     if request.method == "POST":
#         form_ps = PaidStatusForm(request.POST, instance=paid_status)
#         if form_ps.is_valid():
#             paid_status = form_ps.save(commit=False)
#             paid_status.updated_by = request.user
#             paid_status.updated = timezone.now()
#             paid_status.save()
#             return redirect('materialorder')
#     else:
#         form_ps = PaidStatusForm(instance=paid_status)
#     return render(request, 'materialorder/paid_status.html', locals())

@login_required
def paid_status(request, pk):
    paid_status = get_object_or_404(MaterialOrder, pk=pk)
    redirect_to = request.GET.get('next', '')
    # print('THIS IS URL: ' + redirect_to)
    if request.method == "POST":
        form_ps = PaidStatusForm(request.POST, instance=paid_status)
        if form_ps.is_valid():
            paid_status = form_ps.save(commit=False)
            paid_status.updated_by = request.user
            paid_status.updated = timezone.now()
            paid_status.save()
            # messages.success(request, 'Дані успішно збережено', extra_tags='alert alert-success')
            # return render(request, 'home.html', locals())
            # return redirect('materialorder')
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            # next_u = request.POST.get('next', '/')
            # print(next_u)
            # return HttpResponseRedirect(next_u)
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
            return HttpResponseRedirect(redirect_to)
    else:
        form_ps = PaidStatusForm(instance=paid_status)
    return render(request, 'materialorder/paid_status.html', locals())
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    