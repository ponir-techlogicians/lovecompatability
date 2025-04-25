import base64
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from lovecompitability import settings
from .helper import validate_with_apple, validate_with_google, parse_apple_datetime
from .models import CompatibilityResult, SubscriptionUser
from .serializers import CompatibilityResultSerializer
from .utils import get_name_compatibility, split_names, get_name_compatibility_with_steps, \
    get_name_compatibility_with_5steps
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from geopy.distance import geodesic
from collections import Counter
from django.db.models import Q, Count
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class CalculateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        name1 = request.data.get("name1", "").strip()
        name2 = request.data.get("name2", "").strip()
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if not name1 or not name2:
            return Response({"error": "Both names are required."}, status=status.HTTP_400_BAD_REQUEST)

        # compatibility_score = get_name_compatibility(name1, name2)
        compatibility_score, steps = get_name_compatibility_with_5steps(name1, name2)
        print(compatibility_score)
        print("Compatibility Score:", compatibility_score)
        print("Steps:")
        for i, step in enumerate(steps):
            print(f"Step {i}: {step}")

        result = CompatibilityResult.objects.create(
            name1=name1,
            name2=name2,
            compatibility_score=compatibility_score,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None
        )

        serializer = CompatibilityResultSerializer(result)
        serializer.data['steps'] = steps
        return Response({'data':serializer.data,'steps':steps}, status=status.HTTP_201_CREATED)


class ResultDetailAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            result = CompatibilityResult.objects.get(pk=id)
        except CompatibilityResult.DoesNotExist:
            return Response({"error": "Result not found."}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "compatibility_score": result.compatibility_score,
            "name1": result.name1,
            "name2": result.name2,
            "name_parts": split_names(result.name1, result.name2),
            "result": CompatibilityResultSerializer(result).data
        }

        return Response(data, status=status.HTTP_200_OK)


class SaveLocationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        result_id = data.get("result_id")

        if not result_id:
            return Response({"error": "result_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = CompatibilityResult.objects.filter(id=result_id).update(latitude=latitude, longitude=longitude)

        if updated_count == 0:
            return Response({"error": "Result not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Location saved successfully."}, status=status.HTTP_200_OK)


class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "").strip()
        latitude = request.GET.get("latitude", None)
        longitude = request.GET.get("longitude", None)
        radius_input = request.GET.get("radius", None)

        results = CompatibilityResult.objects.all()
        mention_count = 0

        # Filter by Name
        if query:
            results = results.filter(Q(name1=query) | Q(name2=query))

        # Filter by Location Radius
        if latitude and longitude and radius_input:
            try:
                user_location = (float(latitude), float(longitude))
                radius_map = {'1': 1, '2': 50, '3': 200, '4': 99999999999}
                radius = float(radius_map.get(radius_input, 1))

                filtered_results = []
                for record in results:
                    if record.latitude and record.longitude:
                        record_location = (record.latitude, record.longitude)
                        distance = geodesic(user_location, record_location).km
                        if distance <= radius:
                            filtered_results.append(record)
                            if query.lower() == record.name1.lower():
                                mention_count += 1
                            if query.lower() == record.name2.lower():
                                mention_count += 1
                results = filtered_results
            except ValueError:
                pass

        name1_counts = CompatibilityResult.objects.values("name1").annotate(count=Count("name1"))
        name2_counts = CompatibilityResult.objects.values("name2").annotate(count=Count("name2"))

        name_counter = Counter()
        for entry in name1_counts:
            name_counter[entry["name1"]] += entry["count"]
        for entry in name2_counts:
            name_counter[entry["name2"]] += entry["count"]

        top_names = name_counter.most_common(10)

        data = {
            "results": CompatibilityResultSerializer(results, many=True).data,
            "search_key": query,
            "mention_count": mention_count,
            "top_names": top_names,
            "radius_input": radius_input,
            "lat": latitude if latitude else None,
            "lon": longitude if longitude else None,
        }

        return Response(data, status=status.HTTP_200_OK)

class ListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get("user_id", None)
        user = SubscriptionUser.objects.filter(id=user_id).first()
        limit = user.limit
        if user_id:
            if limit == 0:
                return Response({'success':False,'reason':'not_limit'},status=status.HTTP_400_BAD_REQUEST)

            if user.is_expired():
                return Response({'success':False,'reason':'expired'},status=status.HTTP_400_BAD_REQUEST)

            query = request.GET.get("key", "").strip()
            latitude = request.GET.get("lat", None)
            longitude = request.GET.get("lon", None)
            radius_input = request.GET.get("radius", None)
            success = request.GET.get("success", None)

            results = CompatibilityResult.objects.all()
            mention_count = 0

            # Filter by Name
            if query:
                results = results.filter(Q(name1=query) | Q(name2=query))

            # Filter by Location Radius
            if latitude and longitude and radius_input:
                try:
                    user_location = (float(latitude), float(longitude))
                    radius_map = {'1': 1, '2': 50, '3': 200, '4': 99999999999}
                    radius = float(radius_map.get(radius_input, 1))

                    filtered_results = []
                    for record in results:
                        if record.latitude and record.longitude:
                            record_location = (record.latitude, record.longitude)
                            distance = geodesic(user_location, record_location).km
                            if distance <= radius:
                                filtered_results.append(record)
                                if query.lower() == record.name1.lower():
                                    mention_count += 1
                                if query.lower() == record.name2.lower():
                                    mention_count += 1
                    results = filtered_results
                except ValueError:
                    pass

            data = {
                "results": CompatibilityResultSerializer(results, many=True).data,
                "search_key": query,
                "mention_count": mention_count,
                "radius_input": radius_input,
                "lat": latitude if latitude else None,
                "lon": longitude if longitude else None,
                "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
                "success": success
            }
            user.limit -= 1
            user.save()
            return Response(data, status=status.HTTP_200_OK)

class CreatePaymentIntentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:

            amount = request.data.get('amount', 300)
            currency = request.data.get('currency', 'usd')

            # Create the PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                description='Payment for service',
            )

            # Return the client secret in the response so the client can handle it
            return Response({
                'client_secret': payment_intent.client_secret,
                'payment_intent_id': payment_intent.id
            }, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:
            # Handle any Stripe-related errors
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class UsageLeftView(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get("user_id", None)
        user = SubscriptionUser.objects.filter(id=user_id).first()
        limit = user.limit
        if user_id:
            return Response({'success':True,'limit':limit},status=status.HTTP_200_OK)

class SubscriptionValidationView(APIView):
    def post(self, request):
        platform = request.data.get('platform')

        if platform == 'apple':
            receipt_data = request.data.get('receipt_data')
            receipt_info = validate_with_apple(receipt_data)
            print(receipt_info)
            if not receipt_info:
                return Response({'error': 'Invalid Apple receipt'}, status=status.HTTP_400_BAD_REQUEST)

            unique_id = receipt_info['original_transaction_id']
            product_id = receipt_info['product_id']
            expires_str = receipt_info.get('expires_date')
            expiry =  parse_apple_datetime(expires_str) if expires_str else None
            auto_renew = receipt_info.get('auto_renew_status', False)

        elif platform == 'google':
            token = request.data.get('receipt_data')
            package_name = request.data.get('package_name')
            subscription_id = request.data.get('subscription_id')

            purchase_info = validate_with_google(package_name, subscription_id, token)

            if not purchase_info:
                return Response({'error': 'Invalid Google receipt'}, status=status.HTTP_400_BAD_REQUEST)

            unique_id = purchase_info['purchaseToken']
            product_id = subscription_id
            expiry = make_aware(parse_datetime(purchase_info['expiryTime']))
            auto_renew = purchase_info.get('autoRenewing', False)

        else:
            return Response({'error': 'Unsupported platform'}, status=status.HTTP_400_BAD_REQUEST)

        sub_user, created = SubscriptionUser.objects.update_or_create(
            unique_subscription_id=unique_id,
            defaults={
                'platform': platform,
                'product_id': product_id,
                'expiration_date': expiry,
                'auto_renewing': auto_renew,
                'limit': 3
            }
        )

        return Response({
            'status': 'ok',
            'user_id': sub_user.id,
            'is_new': created
        })

class RestorPurchaseView(APIView):

    def post(self, request):
        platform = request.data.get('platform')
        if platform == 'apple':
            receipt_data = request.data.get('receipt_data')
            receipt_info = validate_with_apple(receipt_data)
            print(receipt_info)
            if not receipt_info:
                return Response({'error': 'Invalid Apple receipt'}, status=status.HTTP_400_BAD_REQUEST)
            unique_id = receipt_info['original_transaction_id']
        elif platform == 'google':
            token = request.data.get('receipt_data')
            package_name = request.data.get('package_name')
            subscription_id = request.data.get('subscription_id')

            purchase_info = validate_with_google(package_name, subscription_id, token)

            if not purchase_info:
                return Response({'error': 'Invalid Google receipt'}, status=status.HTTP_400_BAD_REQUEST)

            unique_id = purchase_info['purchaseToken']
        else:
            return Response({'error': 'Unsupported platform'}, status=status.HTTP_400_BAD_REQUEST)

        sub_user = SubscriptionUser.objects.filter(
            unique_subscription_id=unique_id,
        )
        if sub_user.exists():
            return Response({
                    'status': 'ok',
                    'user_id': sub_user.first().id,
                    'limit': sub_user.first().limit,
                })
        else:
            return Response({
                    'status': 'not_found',
                })

class GooglePlayBillingNotification(APIView):
    def post(self, request, *args, **kwargs):
        try:
            response = request.data
            data_string = response['message']['data']
            decoded_bytes = base64.b64decode(data_string)
            decoded_string = json.loads(decoded_bytes.decode('utf-8'))

            if 'subscriptionNotification' in decoded_string:
                notification = decoded_string['subscriptionNotification']
                purchase_token = notification['purchaseToken']
                notification_type = notification['notificationType']

                if notification_type in [3, 13,2]:
                    user = SubscriptionUser.objects.filter(unique_subscription_id=purchase_token)
                    if user.exists():
                        user = user.last()
                        if notification_type == 2:
                            user.limit = 3
                            user.status = 'active'
                        else:
                            user.status = 'cancelled'
                        user.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class IosBillingNotification(APIView):
    def post(self, request, *args, **kwargs):
        try:
            response = request.data
            if response.get('notification_type') == 'DID_CHANGE_RENEWAL_STATUS' and response.get('auto_renew_status') == 'false':
                original_transaction_id = response['original_transaction_id']
                user = SubscriptionUser.objects.filter(unique_subscription_id=original_transaction_id)
                if user.exists():
                    user = user.last()
                    user.status = 'cancelled'
                    user.save()
            if response.get('notification_type') == 'DID_RENEW':
                original_transaction_id = response['original_transaction_id']
                user = SubscriptionUser.objects.filter(unique_subscription_id=original_transaction_id)
                if user.exists():
                    user = user.last()
                    user.status = 'active'
                    user.limit = 3
                    user.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
