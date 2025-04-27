from django.shortcuts import render
from shop.models import ProductReview
from shop.forms import UserProfile
from itertools import groupby


def all_reviews(request):
    reviews = ProductReview.objects.select_related('product', 'user').order_by('product', '-created_at')
    grouped_reviews = {
        product: list(reviews) for product, reviews in groupby(reviews, key=lambda x: x.product)
    }

    for review in reviews:
        review.stars_gold = range(review.rating)
        review.stars_gray = range(5 - review.rating)
        try:
            review.user_profile = UserProfile.objects.get(user=review.user)
        except UserProfile.DoesNotExist:
            review.user_profile = None

    context = {"grouped_reviews": grouped_reviews, 'user': request.user}
    return render(request, 'shop/reviews/all_reviews.html', context)
