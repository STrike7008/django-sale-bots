from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          product=item['product'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             cart.clear()
#             return render(request, 'shop/orders/created.html', {'order': order})
#         return render(request, 'shop/orders/create.html', {'cart': cart, 'form': form})
#     else:
#         form = OrderCreateForm()
#         return render(request, 'shop/orders/create.html', {'cart': cart, 'form': form})

def grn_course():
    import requests
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH'
    response = requests.get(url)
    data = response.json()
    return round(float(data['price']))

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()

            subject = 'Ваше замовлення успішно прийнято'
            message = f"""
            <html>
                <body>
                    <p style="font-size: 18px;">Доброго дня <b>{order.first_name}</b>!</p>
                    <p style="font-size: 18px;">Ваш номер замовленя: <strong>{order.id}</strong>.</p>
                    <i style="font-size: 18px;">Сплатити потрібно після підтвердження вашого замовлення*</i>
            """
            for item in cart:
                grn = int(item['price'])* grn_course()
                message += f"""
                    <p style="font-size: 16px;">Ціна: <strong>$ {item['price']}({grn}грн)</strong> x {item['product']}</p>
                """
            message += """
                    <p style="font-size: 18px;">Дякуємо, що ви з нами!</p>
                    <p style="font-size: 18px;">З повагою, Sale-bots!</p>
                </body>
            </html>
            """

            recipient_email = order.email

            from django.core.mail import send_mail

            send_mail(
                subject,
                message,
                'sale-bots@ukr.net',
                [recipient_email],
                fail_silently=False,
                html_message=message,
            )

            return render(request, 'shop/orders/created.html', {'order': order})
        return render(request, 'shop/orders/create.html', {'cart': cart, 'form': form})
    else:
        form = OrderCreateForm()
        return render(request, 'shop/orders/create.html', {'cart': cart, 'form': form})
