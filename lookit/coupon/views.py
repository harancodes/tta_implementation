from django.shortcuts import render, redirect
from core.decorators import admin_required
from django.contrib import messages
from datetime import datetime, date
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import Coupon
from coupon.utils import update_coupon_usage_remaining
from django.db import transaction
from .utils import annotate_coupon_status

# Create your views here.
@admin_required
def admin_list_coupon(request):
    coupons = Coupon.objects.all().order_by('-created_at')
    
    search = request.GET.get('search')
    discount_type = request.GET.get('discount_type','').upper()
    status = request.GET.get('status','')
    
    #--search filter-------------------------------------
    if search:
        coupons = coupons.filter(code__icontains = search)
    
    #--other filters----------------------------------------
    if discount_type:
        coupons = coupons.filter(discount_type=discount_type)
        
    #find and annotate status field to each coupon
    coupons = annotate_coupon_status(coupons)
    print("status = ",status)
    if status:
        coupons = coupons.filter(status=status)
    
    #--create pagination object-----
    paginator = Paginator(coupons, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'coupon/admin/list.html',{'page_obj':page_obj})


@admin_required
def admin_add_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        discount_type = request.POST.get('discount_type', '').strip()
        discount_value = request.POST.get('discount_value', '').strip()
        min_purchase_amount = request.POST.get('min_purchase_amount', '').strip()
        usage_limit = request.POST.get('usage_limit', '').strip()
        status = request.POST.get('status', '').strip()
        start_date = request.POST.get('start_date', '').strip()
        end_date = request.POST.get('end_date', '').strip()
        print("usage limit ", usage_limit)
        # --validation check: ensure all required fields exist--
        required_fields = {
            'code': code,
            'discount_type': discount_type,
            'discount_value': discount_value,
            'min_purchase_amount': min_purchase_amount,
            'start_date': start_date,
            'end_date': end_date,
        }
        missing_fields = [
            field for field, value in required_fields.items() if not value
        ]
        if missing_fields:
            messages.error(
                request, f"Missing required fields: {', '.join(missing_fields)}"
            )
            return redirect('admin-add-coupon')
        
        #--coupon code validations--------------------------------------------
        if 3 > len(code) > 50:
            messages.error(
                request, "Coupon code must be between 3 and 50 characters long"
            )
            return redirect('admin-add-coupon')
        
        if " " in code:
            messages.error(request, "Coupon code cannot contain spaces")
            return redirect('admin-add-coupon')
        
        #--date validations-----------------------------------------
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date < date.today():
            messages.error(request, "Start date cannot be before today.")
            return redirect('admin-add-coupon')

        if end_date and end_date < start_date:
            messages.error(request, "End date cannot be before start date.")
            return redirect('admin-add-coupon')
        
        #---percentage discount value validation---------------------------------
        if discount_type == 'PERCENTAGE' and float(discount_value) > 90:
            messages.error(request, "Maximum allowed discount percentage is 90%.")
            return redirect('admin-add-coupon')
        
        #--set default values-------------------
        if not usage_limit:
            print(usage_limit)
            usage_limit = -1 #(-1 for unlimited)
            
        if not status:
            is_active = False
        else:
            is_active = True
        
        try:
            Coupon.objects.create(
                code=code,
                discount_type=discount_type,
                discount_value=discount_value,
                min_purchase_amount=min_purchase_amount,
                usage_limit=usage_limit,
                is_active=is_active,
                start_date=start_date,
                end_date=end_date,
            )
            messages.success(request, "Coupon Created Successfully")
            return redirect('admin-list-coupons')
        except Exception as e:
            print("Error: ", e)
            messages.error(request, "Something went wrong")
            return redirect('admin-add-coupon')

    return render(request, "coupon/admin/add_coupon.html")


@admin_required
def admin_edit_coupon(request, code):
    method = request.POST.get('_method', '').upper()
    
    if request.method == 'POST' and method == "PUT":
        code = request.POST.get('code', '').strip().upper()
        discount_type = request.POST.get('discount_type', '').strip()
        discount_value = request.POST.get('discount_value', '').strip()
        min_purchase_amount = request.POST.get('min_purchase_amount', '').strip()
        usage_limit = request.POST.get('usage_limit', '').strip()
        status = request.POST.get('status', '').strip()
        start_date = request.POST.get('start_date', '').strip()
        end_date = request.POST.get('end_date', '').strip()

        # --validation check: ensure all required fields exist--
        required_fields = {
            'code': code,
            'discount_type': discount_type,
            'discount_value': discount_value,
            'min_purchase_amount': min_purchase_amount,
            'start_date': start_date,
            'end_date': end_date,
        }
        missing_fields = [
            field for field, value in required_fields.items() if not value
        ]
        if missing_fields:
            messages.error(
                request, f"Missing required fields: {', '.join(missing_fields)}"
            )
            return redirect('admin-edit-coupon', code = code)
        
        #--coupon code validations--------------------------------------------
        if 3 > len(code) > 50:
            messages.error(
                request, "Coupon code must be between 3 and 50 characters long"
            )
            return redirect('admin-edit-coupon', code = code)
        
        if " " in code:
            messages.error(request, "Coupon code cannot contain spaces")
            return redirect('admin-edit-coupon', code = code)
        
        #--date validations-----------------------------------------
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if end_date and end_date < start_date:
            messages.error(request, "End date cannot be before start date.")
            return redirect('admin-edit-coupon', code = code)
        
        #---percentage discount value validation---------------------------------
        if discount_type == 'PERCENTAGE' and float(discount_value) > 90:
            messages.error(request, "Maximum allowed discount percentage is 90%.")
            return redirect('admin-edit-coupon', code=code)
        
        #--set default values-------------------
        if not usage_limit:
            print(usage_limit)
            usage_limit = -1 #(-1 for unlimited)
            
        if not status:
            is_active = False
        else:
            is_active = True
        
        try:
            with transaction.atomic():
                
                #function to handle coupon usage remaining count logic
                update_coupon_usage_remaining(code, usage_limit)
                
                Coupon.objects.filter(code=code).update(
                    discount_type=discount_type,
                    discount_value=discount_value,
                    min_purchase_amount=min_purchase_amount,
                    usage_limit=usage_limit,
                    is_active=is_active,
                    start_date=start_date,
                    end_date=end_date,
                )

                messages.success(request, f"Coupon {code} Updated Successfully")
                return redirect('admin-list-coupons')
        except Exception as e:
            print("Error: ", e)
            messages.error(request, "Something went wrong")
            return redirect('admin-edit-coupon', code = code)
    
    coupon = get_object_or_404(Coupon, code=code.upper())
    return render(request, "coupon/admin/edit_coupon.html", {'coupon':coupon})
