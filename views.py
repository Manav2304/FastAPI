from django.conf import settings
from django.shortcuts import render, redirect
import requests
import json
import uuid
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import hmac

# Cashfree API credentials
CASHFREE_APP_ID = '33221729445f634e544edbc48c712233'
CASHFREE_SECRET_KEY = 'acf53bda8c05d4a3d23dea5b003404d9e0584706'
CASHFREE_MODE = 'TEST'  # or 'PROD' for production mode

# generate signature using secret key
def generate_signature(message):
    signature = hmac.new(CASHFREE_SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

CASHFREE_ORDER_AMOUNT = 'your_cashfree_order_amount'
CASHFREE_ORDER_ID = 'your_cashfree_order_id'
CASHFREE_ORDER_CURRENCY = 'your_cashfree_order_currency'

def initiate_payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        # Step 1: Create payment order
        order_id = 'order' + str(uuid.uuid1())
        order_data = {
            'orderId': order_id,
            'orderAmount': str(amount),
            'orderCurrency': 'INR',
            'orderNote': 'Test order',
            'customerName': name,
            'customerEmail': email,
            'customerPhone': phone,
            'returnUrl': 'http://localhost:8000/payment_status/',
        }

        # Step 2: Convert order data to JSON
        order_data_json = json.dumps(order_data)

        # Step 3: Generate signature for order data
        message = CASHFREE_APP_ID + '|' + order_id + '|' + str(amount) + '|' + 'INR' + '|' + name + '|' + email + '|' + phone + '||||||' + CASHFREE_SECRET_KEY
        signature = generate_signature(message)

        # Step 4: Add signature to order data
        payload = {
            'appId': CASHFREE_APP_ID,
            'orderId': order_id,
            'orderAmount': str(amount),
            'orderCurrency': 'INR',
            'orderNote': 'Test order',
            'customerName': name,
            'customerEmail': email,
            'customerPhone': phone,
            'returnUrl': 'http://localhost:8000/payment_status/',
            'notifyUrl': 'http://localhost:8000/payment_status/',
            'signature': signature,
        }

        # Step 5: Send payment request to Cashfree API
        url = 'https://test.cashfree.com/api/v2/cftoken/order'
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, json=payload)
        response_data = json.loads(response.content.decode('utf-8'))

        # Step 6: Redirect user to Cashfree payment page
        if response_data['status'] == 'OK':
            payment_link = response_data['paymentLink']
            return redirect(payment_link)
        else:
            # handle payment request error
            pass

    return render(request, 'payment.html')


@csrf_exempt
def payment_status(request):
    if request.method == 'POST':
        response_data = json.loads(request.body.decode('utf-8'))
        signature = response_data['signature']
        status = response_data['txStatus']
        order_id = response_data['orderId']
        order_amount = response_data['orderAmount']

        # Verify signature
        message = CASHFREE_ORDER_ID + '|' + CASHFREE_ORDER_AMOUNT + '|' + CASHFREE_ORDER_CURRENCY + '|' + status + '|' + CASHFREE_SECRET_KEY
        calculated_signature = generate_signature(message)

        if signature == calculated_signature:
            # Payment status is valid
            if status == 'SUCCESS':
                # Update order status in database
                # Redirect user to success page
                return HttpResponse('Payment successful')
            else:
                # Update order status in database
                # Redirect user to error page
                return HttpResponse('Payment failed')
        else:
            # Signature verification failed
            return HttpResponse('Invalid signature')
    else:
        return HttpResponse('Bad request')

