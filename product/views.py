from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from product.models import *
from product.forms import *

# ********************************* CRUD Category ************************************


@login_required(login_url="login")
def createCategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกข้อมูลสำเร็จ")
            return redirect("categoryList")
        else:
            messages.error(request, "บันทึกข้อมูลล้มเหลว")
            return redirect("createCategory")
    else:
        form = CategoryForm()
    context = {"form": form, }
    return render(request, "product/category/createCategory.html", context)

@login_required(login_url="login")
def editCategory(request, id):
    if request.method == "POST":
        category = get_object_or_404(Category, id=id)
        form = CategoryForm(data=request.POST or None, files=request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "อัพเดทข้อมูลสำเร็จ")
            return redirect("categoryList")
        else:
            messages.error(request, "อัพเดทข้อมูลล้มเหลว")
            return redirect("editCategory")
    else:
        category = Category.objects.get(id=id)
        form = CategoryForm(initial=category.__dict__)
    context = {
        "form": form,
        "category": category
    }
    return render(request, "product/category/editCategory.html", context)


@login_required(login_url="login")
def deleteCategory(request, id):
    if request.method == "POST":
        category = get_object_or_404(Category, id=id)
        response_data = {}
        try:
            if category.product_set.exists():
                response_data["success"] = False
                response_data["message"] = "เนื่องจากมีการเชื่อมโยงข้อมูลกับตารางอื่น"
            else:
                category.delete()
                response_data["success"] = True
        except Exception as e:
            response_data["success"] = False
            response_data["message"] = "เกิดข้อผิดพลาดในการลบข้อมูล: " + str(e)
        return JsonResponse(response_data)


def categoryList(request):
    category = Category.objects.all().order_by('id').reverse()
    count = category.count()  # นับจำนวนรายการใน QuerySet
    context = {
        "category": category,
        "count": count,
    }
    return render(request, "product/category/categoryList.html", context)


def search_category(request):
    search = request.GET.get('search')
    if search:
        category = Category.objects.filter(title__icontains=search)
        if not category:
            messages.error(request, 'ไม่พบข้อมูลหมวดหมู่สินค้ากำลังค้นหา')
            return redirect('categoryList')
    else:
        return redirect('categoryList')
    context = {'category': category}
    return render(request, "product/category/categoryList.html", context)




# *******************************************************************************

# ********************************* CRUD Product ************************************
@login_required(login_url="login")
def createProduct(request):
    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกข้อมูลสินค้าสำเร็จ")
            return redirect("productList")
        else:
            id = request.POST.get('id')
            if Product.objects.filter(id=id).exists():
                messages.error(request, "รหัสสินค้าซ้ำกับที่มีอยู่ในระบบ")
                return redirect("createProduct")
    else:
        form = ProductsForm()
    context = {"form": form}
    return render(request, "product/createProduct.html", context)


@login_required(login_url="login")
def editProduct(request, id):
    if request.method == "POST":
        products = get_object_or_404(Product, id=id)
        form = ProductsForm(data=request.POST or None, files=request.FILES, instance=products)
        if form.is_valid():
            form.save()
            messages.success(request, "อัพเดทสินค้าสำเร็จ")
            return redirect("productList")
        else:
            messages.error(request, "อัพเดทข้อมูลสินค้าล้มเหลว")
            return redirect("editProduct")
    else:
        products = Product.objects.get(id=id)
        form = ProductsForm(instance=products)
    context = {"form": form, "products": products}
    return render(request, "product/editProduct.html", context)


@login_required(login_url="login")
def deleteProduct(request, id):
    products = get_object_or_404(Product, id=id)
    products.delete()
    return redirect("productList")


def productList(request):
    # ดึงข้อมูลสินค้าที่ต้องการที่แสดงผลทั้งหมด
    products = Product.objects.all().order_by('id').reverse()
    count = products.count()  # นับจำนวนรายการใน QuerySet
    context = {
        "products": products,
        "count": count,
    }
    return render(request, "product/productList.html", context)


def productDetail(request, id):
    products = get_object_or_404(Product, id=id)
    context = {"products": products}
    return render(request, "product/productDetail.html", context)


def search_product(request):
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(Q(title__icontains=search) | Q(id=search) | Q(category__title__icontains=search))
        if not products:
            messages.error(request, 'ไม่พบข้อมูลสินค้าที่กำลังค้นหา')
            return redirect('productList')
    else:
        return redirect('productList')
    context = {'products': products}
    return render(request, "product/productList.html", context)

# *******************************************************************************

# ********************************* Show Product ************************************
# หมวดหมู่สินค้าทองคำ


def category(request):
    category = Category.objects.all()
    context = {"category": category}
    return render(request, "product/show/category.html", context)


# แหวนทองคำ
def goldRing(request):
    products = Product.objects.filter(category=1)
    context = {"products": products, }
    return render(request, "product/show/goldRing.html", context)


# สร้อยข้อมือทองคำ
def goldBracelet(request):
    products = Product.objects.filter(category=2)
    context = {"products": products, }
    return render(request, "product/show/goldBracelet.html", context)


# สร้อยคอทองคำ
def goldNecklace(request):
    products = Product.objects.filter(category=3)
    context = {"products": products, }
    return render(request, "product/show/goldNecklace.html", context)


# กำไลทองทองคำ
def goldBangle(request):
    products = Product.objects.filter(category=4)
    context = {"products": products, }
    return render(request, "product/show/goldBangle.html", context)


# ต่างหูทองคำ
def goldEarrings(request):
    products = Product.objects.filter(category=5)
    context = {"products": products, }
    return render(request, "product/show/goldEarrings.html", context)


# ทองคำแท่ง
def goldBars(request):
    products = Product.objects.filter(category=6)
    context = {"products": products, }
    return render(request, "product/show/goldBars.html", context)
