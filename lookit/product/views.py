import json
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Sum, Q, Value, Count
from django.db.models.functions import Coalesce
from django.contrib import messages
from cloudinary.uploader import upload, destroy
from django.db.models import (
    Case,
    When,
    Value,
    IntegerField,
    Max,
)
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.db import transaction
from core.decorators import admin_required

from .models import Style, Product, Variant, ProductImages
from cart.models import Cart
from offer.models import Offer
from user.utils import remove_wishlist_item
from django.utils import timezone

from offer.utiils import annotate_offers
from user.utils import annotate_wishlist_products
from .utils import fetch_all_reviews, get_rating_summary


""" ============================================
    ADMIN SIDE
============================================ """


@admin_required
def admin_list_products(request):
    products = Product.objects.annotate(
        total_stock=Coalesce(Sum('variant__stock'), Value(0))
    ).order_by('-is_active', '-created_at')
    styles = Style.objects.all()

    search = request.GET.get('search')
    category = request.GET.get('category')
    style = request.GET.get('style')
    stock_status = request.GET.get('stock')
    price_range = request.GET.get('price')

    if search:
        products = products.filter(Q(name__icontains=search) | Q(uuid__icontains=search))

    if style:
        products = products.filter(style__name=style)

    if category:
        products = products.filter(category=category.lower())

    if stock_status:
        reorder_level = 30
        if stock_status == 'in_stock':
            products = products.filter(total_stock__gt=reorder_level)
        elif stock_status == 'low_stock':
            products = products.filter(total_stock__range=(1, reorder_level))
        elif stock_status == 'out_of_stock':
            products = products.filter(Q(total_stock=0) | Q(total_stock=None))

    if price_range:
        if '-' in price_range:
            min_price, max_price = price_range.split('-')
            products = products.filter(price__range=(min_price, max_price))
        elif "+" in price_range:
            min_price = price_range.split('+')[0]
            products = products.filter(price__gte=min_price)

    # pagination
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, "product/admin/list.html", {"page_obj": page_obj, "styles": styles}
    )


@admin_required
def admin_add_product(request):
    if request.method == "POST":
        # ---retrive-all-post-data-------------------
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        brand = request.POST.get('brand', '').strip()
        base_color = request.POST.get('base_color', '').strip()
        category = request.POST.get('category', '').strip().lower()
        style_name = request.POST.get('style', '').strip()

        material = request.POST.get('material', '').strip()
        fit = request.POST.get('fit', '').strip()
        care_instructions = request.POST.get('care_instructions', '').strip()

        price = request.POST.get('price')

        image = request.FILES.get('image')
        additional_images = request.FILES.getlist('additional_images')
        img_url = None
        image_public_id = None

        # ---check if all required fields exists-----------------------
        field_map = {
            'name': name,
            'description': description,
            'brand': brand,
            'base color': base_color,
            'category': category,
            'style': style_name,
            'price': price,
            'thumbnail image': image,
            'additional images': additional_images,
        }
        missing_fields = [key for key, value in field_map.items() if not value]
        if missing_fields:
            messages.error(request, f"Missing fields: {', '.join(missing_fields)}")
            return redirect('admin-add-product')

        # ---check if product name already exists-----------------------
        if Product.objects.filter(name__iexact=name).exists():
            messages.error(request, f"Product '{name}' already exists.")
            return redirect('admin-add-product')

        # ---price validation-----------------------------------------
        if int(price) <= 0:
            messages.error(request, "Price must be greater than zero.")
            return redirect('admin-add-product')

        # ---category validation--------------------------------------
        ALLOWED_CATEGORIES = ['men', 'women', 'kids', 'unisex']
        if category.lower() not in ALLOWED_CATEGORIES:
            messages.error(request, "Invalid category selected.")
            return redirect('admin-add-product')

        # ---validate style category------------------------------------
        try:
            style = Style.objects.get(name=style_name)
        except Style.DoesNotExist:
            messages.error(request, "Selected style does not exist.")
            return redirect('admin-add-product')

        # ---validate additional images count-----------------------------
        additional_images_count = len(additional_images)
        if additional_images_count < 2:
            messages.error(request, "Please upload at least 2 additional images.")
            return redirect('admin-add-product')
        if additional_images_count > 5:
            messages.error(request, "You can upload a maximum of 5 additional images.")
            return redirect('admin-add-product')

        # ---upload-image-to-cloudinary---------------------------------------
        if image:
            result = upload(
                image,
                folder=f"products/{name}/",
                transformation=[
                    {'width': 1080, 'height': 1080, 'crop': 'limit'},
                    {'quality': 'auto'},
                    {'fetch_format': 'auto'},
                ],
            )
            img_url = result.get('secure_url')
            image_public_id = result['public_id']
            # ---check if file upload succeded--------------------
            if not img_url:
                messages.error(request, "Image upload failed.")
                return redirect('admin-add-product')

        try:
            with transaction.atomic():
                # ---create-new-product-
                product = Product.objects.create(
                    name=name,
                    description=description,
                    brand=brand,
                    base_color=base_color,
                    category=category,
                    style=style,
                    material=material,
                    fit=fit,
                    care_instructions=care_instructions,
                    price=price,
                    image_url=img_url,
                    image_public_id=image_public_id,
                )

                # ---upload-additional-images-------
                if additional_images:
                    for file in additional_images:
                        result = upload(
                            file,
                            folder=f"products/{product.name}/additional-images/",
                            transformation=[
                                {'width': 1080, 'height': 1080, 'crop': 'limit'},
                                {'quality': 'auto'},
                                {'fetch_format': 'auto'},
                            ],
                        )
                        ProductImages.objects.create(
                            product=product,
                            image_url=result['secure_url'],
                            image_public_id=result['public_id'],
                        )
                    messages.success(request, "NEW PRODUCT CREATED")
        except Exception as e:
            messages.error(request, "Something went wrong while creating the product.")
            print("Error creating product:", e)
            return redirect('admin-add-product')

        # if product created
        return redirect('admin-view-product', product_uuid=product.uuid)

    # ---redner-add-product-page------------------------------------------------
    styles = Style.objects.all()
    color_choices = Product.BaseColor.choices
    return render(request, "product/admin/add_product.html", {"styles": styles, "color_choices":color_choices})


@admin_required
def admin_edit_product(request, product_uuid):
    method = request.POST.get('_method', '').upper()

    product = Product.objects.get(uuid=product_uuid)
    if request.method == 'POST' and method == 'PUT':
        # ---retrive-all-data
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        brand = request.POST.get('brand', '').strip()
        base_color = request.POST.get('base_color', '').strip()
        category = request.POST.get('category', '').strip().lower()

        style_name = request.POST.get('style', '').strip()
        style = Style.objects.get(name=style_name)

        material = request.POST.get('material', '').strip()
        fit = request.POST.get('fit', '').strip()
        care_instructions = request.POST.get('care_instructions', '').strip()
        price = request.POST.get('price')

        main_image = request.FILES.get('image')
        image_public_id = product.image_public_id

        additional_images = request.FILES.getlist('additional_images')
        img_url = None

        # ---check if all required fields exists-----------------------
        required_fields = [
            name,
            description,
            brand,
            base_color,
            category,
            style_name,
            price,
        ]
        if not all(required_fields):
            messages.error(request, "Some Required Fields are missing")
            return redirect('admin-edit-product', product_uuid=product_uuid)

        # ---check if product name already exists-----------------------
        if (
            name
            and Product.objects.exclude(uuid=product_uuid)
            .filter(name__iexact=name)
            .exists()
        ):
            messages.error(request, f"Product '{name}' already exists.")
            return redirect('admin-edit-product', product_uuid=product_uuid)

        # ---price validation-----------------------------------------
        if Decimal(price) <= 0:
            messages.error(request, "Price must be greater than zero.")
            return redirect('admin-edit-product', product_uuid=product_uuid)

        # ---category validation--------------------------------------
        ALLOWED_CATEGORIES = ['men', 'women', 'kids', 'unisex']
        if category.lower() not in ALLOWED_CATEGORIES:
            messages.error(request, "Invalid category selected.")
            return redirect('admin-edit-product', product_uuid=product_uuid)

        # ---validate style category------------------------------------
        try:
            style = Style.objects.get(name=style_name)
        except Style.DoesNotExist:
            messages.error(request, "Selected style does not exist.")
            return redirect('admin-edit-product', product_uuid=product_uuid)

        # ---take count of additional images removed-----------------------------
        '''
        in client side edit product form hidden input fields are added to show exising additional 
        images. user can view it's preview and remove it (which will remove the hidden input field). 
        those input field's name is the corresponding db id of additional image. 
        if any hidden input field is missing that means the image is removed.
        '''
        current_additional_images = ProductImages.objects.filter(product=product)
        removed_count = 0
        for current_img in current_additional_images:
            # If hidden input is missing => image removed in UI
            if not request.POST.get(str(current_img.id)):
                removed_count += 1

        # ---validate count of additional images---------------------------------
        count_of_current_additional_images = (
            current_additional_images.count() - removed_count
        )
        count_of_new_images = len(additional_images)
        total_images = count_of_current_additional_images + count_of_new_images

        if total_images > 5:
            messages.error(request, "You can upload a maximum of 5 additional images.")
            return redirect('admin-edit-product', product_uuid=product_uuid)
        if total_images < 2:
            messages.error(request, "Please upload at least 2 additional images.")
            return redirect('admin-edit-product', product_uuid=product_uuid)

        # ---replace main image if changed--------------------------
        if main_image:
            if image_public_id != ' ':
                result = upload(
                    main_image,
                    folder=f"products/{name}/",
                    public_id=product.image_public_id,
                    overwrite=True,
                    transformation=[
                        {'width': 1080, 'height': 1080, 'crop': 'limit'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'},
                    ],
                )
                img_url = result.get('secure_url')
            # ---temporary else block to set image public id for products which have it empty
            else:
                result = upload(
                    main_image,
                    folder=f"products/{name}/",
                    transformation=[
                        {'width': 1080, 'height': 1080, 'crop': 'limit'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'},
                    ],
                )
                image_public_id = result['public_id']
                img_url = result.get('secure_url')
        else:
            img_url = request.POST.get('old_image_url')

        # ---manage-additional-images using hidden input( delete if missing)-----
        for current_img in current_additional_images:
            # If hidden input is missing => image removed in UI
            if not request.POST.get(str(current_img.id)):
                # Remove from Cloudinary using public_id
                destroy(current_img.image_public_id)
                # Remove from db
                current_img.delete()

        # ---manage-additional-images( upload new ones )-------------------------
        if additional_images:
            for file in additional_images:
                result = upload(
                    file,
                    folder=f"products/{name}/additional-images/",
                    transformation=[
                        {'width': 1080, 'height': 1080, 'crop': 'limit'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'},
                    ],
                )
                ProductImages.objects.create(
                    product=product,
                    image_url=result['secure_url'],
                    image_public_id=result['public_id'],
                )
        # ---update-modal-----------------------------
        product = Product.objects.filter(uuid=product_uuid).update(
            name=name,
            description=description,
            brand=brand,
            base_color=base_color,
            category=category,
            style=style,
            material=material,
            fit=fit,
            care_instructions=care_instructions,
            price=price,
            image_url=img_url,
            image_public_id=image_public_id,
        )
        messages.success(request, f"PRODUCT DETAILS UPDATED")
        return redirect('admin-view-product', product_uuid=product_uuid)

    else:
        # ---prefill-and-render-edit-page--------------------------------
        additional_images = ProductImages.objects.filter(product=product)
        styles = Style.objects.all()
        return render(
            request,
            "product/admin/edit_product.html",
            {
                'product': product,
                'styles': styles,
                'additional_images': additional_images,
            },
        )


# --stock_management-------------------------
@admin_required
def admin_manage_stocks(request, product_uuid):
    product = (
        Product.objects.filter(uuid=product_uuid)
        .annotate(total_stock=Coalesce(Sum('variant__stock'), Value(0)))
        .first()
    )

    if request.method == "POST":
        size = request.POST.get('size')
        stock = request.POST.get('stock')

        size_already_exist = Variant.objects.filter(product=product, size=size).exists()
        if size_already_exist:
            messages.error(request, f"SIZE VARIANT ALREADY EXIST")
            return redirect('admin-manage-stocks', product_uuid=product_uuid)

        Variant.objects.create(product=product, size=size, stock=stock)
        messages.success(request, f"NEW VARIANT ADDED")
        return redirect('admin-manage-stocks', product_uuid=product_uuid)

    variants = Variant.objects.filter(product=product).order_by('-updated_at')
    size_choices = Variant.Size.choices
    return render(
        request,
        "product/admin/manage_stocks.html",
        {'product': product, 'variants': variants, 'size_choices': size_choices},
    )


# ---stock_update_ajax----------
@admin_required
def admin_update_stock(request):
    if request.method == "POST":
        # convert json data into python dict
        data = json.loads(request.body)

        variant_id = data.get('variant_id')
        new_stock = data.get('stock')

        # update new stock
        variant = Variant.objects.get(id=variant_id)
        variant.stock = new_stock
        variant.save()

        # fetch total stock of product
        product_id = variant.product.id
        product = Product.objects.filter(id=product_id).aggregate(
            total_stock=Sum('variant__stock')
        )
        total_stock = product['total_stock']

        return JsonResponse(
            {
                "status": "success",
                "message": "Stock updated",
                "new_stock": new_stock,
                "new_total_stock": total_stock,
            }
        )


@admin_required
def admin_delete_variant(request, variant_id):
    if request.method == "POST":
        product_uuid = request.POST.get('product_uuid')
        variant = Variant.objects.get(id=variant_id)
        variant.stock = 0
        variant.save()
        messages.success(request, f"Size {variant.size} Stocks Removed")
        return redirect('admin-manage-stocks', product_uuid=product_uuid)


@admin_required
def admin_view_product(request, product_uuid):
    product = (
        Product.objects.filter(uuid=product_uuid)
        .annotate(
            total_stocks=Coalesce(Sum('variant__stock'), Value(0)),
            total_variants=Coalesce(Count('variant'), Value(0)),
        )
        .first()
    )
    product_images = ProductImages.objects.filter(product__uuid=product_uuid)
    return render(
        request,
        "product/admin/view_product.html",
        {"product": product, "product_images": product_images},
    )


@admin_required
def admin_toggle_product_active(request, product_uuid):
    product = Product.objects.get(uuid=product_uuid)
    product.is_active = not product.is_active
    product.save()
    print(product.is_active)
    if product.is_active:
        messages.success(request, f"PRODUCT RESTORED")
    else:
        messages.success(request, f"PRODUCT DELETED")
    return redirect('admin-view-product', product_uuid=product_uuid)


@admin_required
def admin_list_categories(request):
    styles = Style.objects.all().annotate(product_count=Coalesce(Count('product'), Value(0))).order_by('-product_count').distinct()
    
    #search functionality
    search_key = request.GET.get('search', '')
    if search_key:
        styles = styles.filter(name__icontains=search_key)
    
    # pagination
    paginator = Paginator(styles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/admin/list_categories.html', {"page_obj": page_obj})


@admin_required
def admin_add_style(request):
    if request.method == "POST":
        style_name = request.POST.get('style_name').strip()
        print(f"request came with {style_name}")
        is_style_exist = Style.objects.filter(name__iexact=style_name).exists()
        if is_style_exist:
            messages.error(request, "Style already exist")
            return redirect('admin-category-management')
        style = Style.objects.create(name=style_name)
        messages.success(request, f"CREATED NEW STYLE - {style.name}")
    return redirect('admin-category-management')



@admin_required
def admin_delete_category(request, style_id):
    style = Style.objects.get(id=style_id)
    style.is_deleted = True
    style.save()
    messages.success(request, f"STYLE DELETED - {style.name}")
    return redirect('admin-category-management')


@admin_required
def admin_restore_category(request, style_id):
    style = Style.objects.get(id=style_id)
    style.is_deleted = False
    style.save()
    messages.success(request, f"Restored style - {style.name}")
    return redirect('admin-category-management')


@admin_required
def admin_edit_category(request):
    method = request.POST.get('_method', '').upper()

    if request.method == "POST" and method == 'PUT':
        style_id = request.POST.get('style_id')
        style_name = request.POST.get('style_name').strip()

        style = Style.objects.get(id=style_id)
        style.name = style_name
        style.save()
        messages.success(request, f"EDITED STYLE - {style.name}")
        return redirect('admin-category-management')


""" ============================================
    USER SIDE
============================================ """

def explore(request):
    user = None
    if request.user.is_authenticated:
        user = request.user

    # fetch only products which are active and not out of stock
    products = (
        Product.objects.filter(is_active=True, variant__stock__gt=0)
        .distinct()
    )
    
    # fetch only styles with minimum one product with minimum one stock
    styles = Style.objects.filter(product__variant__stock__gt=0).distinct()

    # ---category page
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category.lower())
        # fetch only styles which have atleast one product in men's category
        styles = styles.filter(product__category=category.lower()).distinct()

    # ---search----------------------------
    search_key = request.GET.get('search')
    if search_key:
        products = products.filter(name__icontains=search_key)

    # ---sort----------------------
    sort_name = request.GET.get('sort_name')
    sort_price = request.GET.get('sort_price')
    order_fields = []
    if sort_price:
        order_fields.append(sort_price)
    if sort_name:
        order_fields.append(sort_name)
    # if both sort exists first order by price then name
    if order_fields:
        products = products.order_by(*order_fields)
    else:
        products = products.order_by('-created_at')

    # ----filter---------------------
    style = request.GET.get('style')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    color = request.GET.get('color')
    size = request.GET.get('size')

    if style:
        products = products.filter(style__name__icontains=style)
    if price_min and price_max:
        products = products.filter(price__range=(price_min, price_max))
    if color:
        products = products.filter(base_color=color)
    if size:
        products = products.filter(variant__size=size.upper())
        
    #annotate offer price to each product
    products = annotate_offers(products)
    
    #annotate in_wishlist status True, if product is on wishlist
    products = annotate_wishlist_products(user, products)

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    color_choices = Product.BaseColor.choices
    size_choices = Variant.Size.choices
    return render(
        request, "product/user/explore.html", {"page_obj": page_obj, "styles": styles, "color_choices":color_choices, "size_choices":size_choices}
    )


def product_details(request, product_uuid):
    # --fetch product----------------------------
    product = (
        Product.objects.filter(uuid=product_uuid)
        .annotate(
            total_stock=Coalesce(Sum('variant__stock'), 0),
            total_additional_images=Coalesce(Count('productimages'), 0),
        )
        .first()
    )

    # --invalid uuid-------------------------------------
    if not product:
        print("product uuid is invalid or null, uuid = ", product_uuid)
        messages.error(request, "Something went wrong!")
        return redirect('explore')

    # ---manual ordering for sizes----
    size_order = Case(
        When(size='S', then=Value(1)),
        When(size='M', then=Value(2)),
        When(size='L', then=Value(3)),
        When(size='XL', then=Value(4)),
        When(size='XXL', then=Value(5)),
        default=Value(99),
        output_field=IntegerField(),
    )
    # ---fetch all available sizes of this product-----------------------
    variants = Variant.objects.filter(product=product, stock__gt=0).order_by(size_order)

    # ---redirect to product listing page if product is not active-------
    if not product.is_active:
        messages.error(request, "PRODUCT IS UNAVAILABLE")
        return redirect('explore')

    # ---fetch additional product images--------------------------
    product_images = ProductImages.objects.filter(product=product)

    # ---fetch related products---------------------------------------------------------------
    related_products = (
        Product.objects.filter(
            category=product.category, is_active=True, variant__stock__gt=0
        )
        .distinct()
        .exclude(id=product.id)
    )
    #---annotate offer price to each related product----
    related_products = annotate_offers(related_products)
    
    # --fetch offers---------------------
    today = timezone.now().date()
    max_product_offer = (
        Offer.objects.filter(
            products=product,
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
        )
        .aggregate(maximum_offer=Max('discount'))
        .get('maximum_offer', '')
    )
    max_category_offer = (
        Offer.objects.filter(
            style=product.style,
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
        )
        .aggregate(maximum_offer=Max('discount'))
        .get('maximum_offer', '')
    )
    offer_discount = None
    category_offer = False
    offer = None

    if max_category_offer and max_product_offer:
        if max_category_offer > max_product_offer:
            offer_discount = max_category_offer
            category_offer = True
        else:
            offer_discount = max_product_offer
    elif max_category_offer:
        offer_discount = max_category_offer
        category_offer = True
    elif max_product_offer:
        offer_discount = max_product_offer

    # --calculate offer price----------------------------------
    offer_price = None
    if offer_discount:
        discount_amount = (product.price * offer_discount) / 100
        offer_price = product.price - discount_amount
        offer = {
            'percentage': offer_discount,
            'price': offer_price,
            'category_offer': category_offer,
        }
    #--rating summary-----
    rating_summary = get_rating_summary(product.id)    
    
    #---fetch all review--------------------------------------------
    reviews = fetch_all_reviews(product.id)

    return render(
        request,
        "product/user/product_details.html",
        {
            "product": product,
            'offer': offer,
            'additional_product_images': product_images,
            'variants': variants,
            "related_products": related_products,
            "reviews": reviews,
            "rating_summary":rating_summary,
        },
    )


def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=product_id)

        # restrict if not authenticated
        if not user.is_authenticated:
            messages.error(request, f"PLEASE LOGIN TO USE CART")
            return redirect('product-details', product_uuid=product.uuid)

        # if size not selected
        if not variant_id:
            messages.error(request, "PLEASE SELECT A SIZE")
            return redirect('product-details', product_uuid=product.uuid)

        # check if product is active
        if not product.is_active:
            messages.error(request, "Product Is Currently Unavailble")
            return redirect('explore')

        # if product already in cart increase quantity
        variant_in_cart = Cart.objects.filter(user=user, variant_id=variant_id).first()
        if variant_in_cart:
            variant_in_cart.quantity += int(quantity)
            if variant_in_cart.quantity > 4:
                variant_in_cart.quantity = 4
                msg = "Product already in cart — maximum 4 quantity allowed."
            else:
                msg = "Product already in cart — quantity updated."

            messages.success(request, msg)
            variant_in_cart.save()

            return redirect('product-details', product_uuid=product.uuid)

        # --stock validation---
        stock_mismatch = None
        variant = Variant.objects.get(id=variant_id)
        if int(variant.stock) == 0:
            messages.error(
                request,
                f"{variant.product.name} ( Size-{variant.size} ) Is Currently Out Of Stock.",
            )
            return redirect('product-details', product_uuid=product.uuid)
        elif int(variant.stock) < int(quantity):
            stock_mismatch = f"Product Added to Cart. (note: only {variant.stock} stocks are available.)"
            quantity = variant.stock

        try:
            Cart.objects.create(user=user, variant_id=variant_id, quantity=quantity)
            # --when product moved to cart remove from wishlist if it exist there--
            remove_wishlist_item(user, product_id)

            if stock_mismatch:
                messages.success(request, stock_mismatch)
            else:
                messages.success(request, "Product Added to Cart")
        except Exception as e:
            print(e)
            messages.error(request, e)

    return redirect('product-details', product_uuid=product.uuid)
