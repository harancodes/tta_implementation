from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
from django.core.paginator import Paginator
from product.models import Style, Product
from offer.models import Offer
from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder
from .utiils import annotate_offer_status


# Create your views here.
def admin_list_offers(request):
    offers = (
        Offer.objects.all()
        .order_by('-created_at')
        .annotate(product_count=Count('products'))
    )
    
    search = request.GET.get('search')
    scope = request.GET.get('scope')
    status = request.GET.get('status')
    
    #--search filter-----------------------------------
    if search:
        offers = offers.filter(name__icontains = search)
        
    #--scope filter-----------------------
    if scope:
        offers = offers.filter(scope=scope)
         
    #annotate offer status (active, upcoming, limit reached, inactive)
    offers = annotate_offer_status(offers)
    
    #--status filter----------------------------
    if status:
        offers = offers.filter(status=status)

    # --create pagination object-----
    paginator = Paginator(offers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'offer/list.html', {'page_obj': page_obj})


def admin_add_offer(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        scope = request.POST.get('scope', '').strip()

        style_name = request.POST.get('style', '').strip()
        selected_products = request.POST.getlist('selected_products')

        discount = request.POST.get('discount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        status = request.POST.get('status')
        is_active = True if status == 'on' else False

        # Required fields dictionary
        required_fields = {
            "Offer Name": name,
            "Scope": scope,
            "Discount Percentage": discount,
            "Start Date": start_date,
            "End Date": end_date,
        }

        # -- Required field vaidation ----------------------------------------------------
        missing_fields = [
            field for field, value in required_fields.items() if not value
        ]
        if missing_fields:
            messages.error(
                request, "Missing required fields: " + ", ".join(missing_fields)
            )
            return redirect('admin-add-offer')
        
        #---discount validation----------------------------------------------
        if not (1 <= float(discount) <= 90):
            messages.error(request, "Discount needs to be between 1% and 90%")
            return redirect('admin-add-offer')
        
        #--date validations-----------------------------------------
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date < date.today():
            messages.error(request, "Start date cannot be before today.")
            return redirect('admin-add-offer')

        if end_date and end_date < start_date:
            messages.error(request, "End date cannot be before start date.")
            return redirect('admin-add-offer')

        if scope == 'category':
            print("it is category")
            # -- Style Validation------------
            style_exists = Style.objects.filter(name=style_name).exists()
            if style_name and not style_exists:
                messages.error(request, "Invalid Selected Style")
                return redirect('admin-add-offer')

            try:
                style = Style.objects.get(name=style_name)
                Offer.objects.create(
                    name=name,
                    scope=Offer.Scopes.CATEGORY_BASED,
                    style=style,
                    discount=discount,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=is_active,
                )
                messages.success(request, "Offer Created Successfully")

                return redirect('admin-list-offers')
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong")
                return redirect('admin-add-offer')

        elif scope == 'product':
            #---atleast one product needed valiation---------------------------
            if len(selected_products) == 0:
                messages.error(request, "Please select atleast one product to continue")
                return redirect('admin-add-offer')
            
            try:
                offer = Offer.objects.create(
                    name=name,
                    scope=Offer.Scopes.PRODUCT_BASED,
                    discount=discount,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=is_active,
                )
                for product_id in selected_products:
                    offer.products.add(product_id)

                messages.success(request, "Offer Created Successfully")
                return redirect('admin-list-offers')
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong")
                return redirect('admin-add-offer')

    styles = Style.objects.all()
    products = list(Product.objects.values('id', 'name', 'image_url', 'price'))
    context = {
        'products_json': json.dumps(products, cls=DjangoJSONEncoder),
        'styles': styles,
        'products': products,
    }
    return render(request, 'offer/add_offer.html', context)


def admin_edit_offer(request, offer_uuid):
    method = request.POST.get('_method', '').upper()
    offer = Offer.objects.get(uuid=offer_uuid)

    if request.method == 'POST' and method == 'PUT':
        name = request.POST.get('name', '').strip()
        scope = request.POST.get('scope', '').strip()

        style_name = request.POST.get('style', '').strip()
        selected_products = request.POST.getlist('selected_products')

        discount = request.POST.get('discount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        status = request.POST.get('status')
        is_active = True if status == 'on' else False

        # Required fields dictionary
        required_fields = {
            "Offer Name": name,
            "Scope": scope,
            "Discount Percentage": discount,
            "Start Date": start_date,
            "End Date": end_date,
        }

        # -- Required field vaidation ----------------------------------------------------
        missing_fields = [
            field for field, value in required_fields.items() if not value
        ]
        if missing_fields:
            messages.error(
                request, "Missing required fields: " + ", ".join(missing_fields)
            )
            return redirect('admin-edit-offer', offer_uuid=offer_uuid)
        
        #---discount validation----------------------------------------------
        if not (1 <= float(discount) <= 90):
            messages.error(request, "Discount needs to be between 1% and 90%")
            return redirect('admin-edit-offer', offer_uuid=offer_uuid)
        
        #--date validations-----------------------------------------
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if end_date and end_date < start_date:
            messages.error(request, "End date cannot be before start date.")
            return redirect('admin-edit-offer', offer_uuid=offer_uuid)

        if scope == 'category':
            # -- Style Validation------------
            style_exists = Style.objects.filter(name=style_name).exists()
            if style_name and not style_exists:
                messages.error(request, "Invalid Selected Style")
                return redirect('admin-edit-offer', offer_uuid=offer_uuid)

            try:
                style = Style.objects.get(name=style_name)
                Offer.objects.filter(uuid=offer_uuid).update(
                    name=name,
                    scope=Offer.Scopes.CATEGORY_BASED,
                    style=style,
                    discount=discount,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=is_active,
                )
                messages.success(request, "Offer Updated Successfully")

                return redirect('admin-list-offers')
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong")
                return redirect('admin-edit-offer', offer_uuid=offer_uuid)

        elif scope == 'product':
            print(discount)
            #---atleast one product needed valiation---------------------------
            if len(selected_products) == 0:
                messages.error(request, "Please select atleast one product to continue")
                return redirect('admin-edit-offer', offer_uuid=offer_uuid)
            try:
                offer.name = name
                offer.scope = Offer.Scopes.PRODUCT_BASED
                offer.discount = discount
                offer.start_date = start_date
                offer.end_date = end_date
                offer.is_active = is_active
                offer.products.set(selected_products)
                offer.save()

                messages.success(request, "Offer Updated Successfully")
                return redirect('admin-list-offers')
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong")
                return redirect('admin-edit-offer', offer_uuid=offer_uuid)

    existing_selected_products = offer.products.all()
    styles = Style.objects.all()
    products = list(Product.objects.values('id', 'name', 'image_url', 'price'))

    context = {
        'offer': offer,
        'selected_products': existing_selected_products,
        'products_json': json.dumps(products, cls=DjangoJSONEncoder),
        'styles': styles,
        'products': products,
    }
    return render(request, 'offer/edit_offer.html', context)
