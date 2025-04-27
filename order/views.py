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
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: #fff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); padding: 20px;">
                        <h2 style="font-size: 24px; color: #333; text-align: center;">Ваше замовлення успішно прийнято</h2>
                        <p style="font-size: 18px; color: #333;">Доброго дня <b>{order.first_name}</b>!</p>
                        <p style="font-size: 18px; color: #333;">Ваш номер замовлення: <strong>{order.id}</strong>.</p>
                        <i style="font-size: 18px; color: #666;">Сплатити потрібно після підтвердження вашого замовлення*</i>
                        <hr style="border: 1px solid #eee; margin: 20px 0;">
                        <h3 style="font-size: 20px; color: #333;">Деталі вашого замовлення:</h3>
                        <ul style="list-style: none; padding: 0;">
            """

            total = 0
            for item in cart:
                grn = int(item['price']) * grn_course()
                item_total = grn * item['quantity']
                total += item_total
                message += f"""
                            <li style="font-size: 16px; color: #333; margin-bottom: 10px;">
                                <strong>{item['product']}</strong> - <strong>{item['price']} $ ({grn} грн)</strong>
                            </li>
                """

            message += f"""
                        </ul>
                        <hr style="border: 1px solid #eee; margin: 20px 0;">
                        <p style="font-size: 24px; font-weight: bold; color: #333;">Загальна вартість: <b>{total} грн</b></p>
                        <i style="font-size: 16px; color: #666;">Загальна вартість на дату замовлення*</i>
                        <p style="font-size: 18px; color: #333;">Дякуємо, що ви з нами!</p>
                        <p style="font-size: 18px; color: #333;">З повагою, <b>Sale-bots!</b></p>
                        <hr style="border: 1px solid #eee; margin: 20px 0;">
                        <p style="text-align: center;">
                            <a href="#" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 18px;">
                                Повернутися на сайт
                            </a>
                        </p>
                    </div>
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

            return render(request, 'shop/orders/created.html', {'order': order, "email": order.email})
        return render(request, 'shop/orders/create.html', {'cart': cart, 'form': form})
    else:
        form = OrderCreateForm()
        return render(request, 'shop/orders/create.html', {'cart': cart, 'form': form})
