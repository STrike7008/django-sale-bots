from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, ProductReview
from cart.forms import CartAddProductForm
from .forms import RegisterForm, UserProfile, UserProfileForm, ProductReviewForm


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2
    return {'cats1': all[:half], 'cats2': all[half:]}

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category, 'categories': categories, 'products': products, 'is_blog': True}
    return render(request, "shop/list.html", context)


# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     return render(request, "shop/detail.html", {"product": product, "cart_product_form": CartAddProductForm()})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = ProductReview.objects.filter(product=product).order_by('-created_at')

    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', id=id, slug=slug)
    else:
        review_form = ProductReviewForm()

    for review in reviews:
        review.stars_gold = range(review.rating)
        review.stars_gray = range(5 - review.rating)
        try:
            review.user_profile = UserProfile.objects.get(user=review.user)
        except UserProfile.DoesNotExist:
            review.user_profile = None

    context = {
        "product": product,
        "reviews": reviews,
        "review_form": review_form,
        "cart_product_form": CartAddProductForm(),
        "user": request.user
    }
    return render(request, "shop/detail.html", context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, "registration/registration_user.html", {'form': form})

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'registration/profile.html', context)

@login_required
def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "registration/update_profile.html", {'form': form})



def search(request):
    query = request.GET.get('query', '').strip()
    products = Product.objects.filter(
        Q(description__icontains=query) | Q(name__icontains=query)
    ) if query else Product.objects.none()
    context = {
        'products': products,
        'query': query,
    }
    context.update(get_categories())
    return render(request, "shop/list.html", context)


from itertools import groupby


def all_reviews(request):
    reviews = ProductReview.objects.select_related('product', 'user').order_by('product', '-created_at')
    grouped_reviews = {
        product: list(reviews) for product, reviews in groupby(reviews, key=lambda x: x.product)
    }

    for review in reviews:
        review.stars_gold = range(review.rating)
        review.stars_gray = range(5 - review.rating)

        user_profile = UserProfile.objects.get(user=review.user)
        review.user_avatar = user_profile.avatar.url if user_profile.avatar else None

    context = {"grouped_reviews": grouped_reviews}
    return render(request, 'shop/reviews/all_reviews.html', context)