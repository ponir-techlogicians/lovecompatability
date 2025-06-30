import json
from collections import Counter
from django.db.models import Count, F, Q, Value
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from geopy.distance import geodesic

from lovecompitability import settings
from lovecompitability.settings import LANGUAGE_SESSION_KEY
from .models import CompatibilityResult
import stripe
from django.utils.translation import activate, get_language

from .query_helper import filter_and_count
from .utils import get_name_compatibility_with_5steps, get_name_compatibility, split_names_safe, GLOBAL_STROKE_DICT

stripe.api_key = settings.STRIPE_SECRET_KEY

def set_language_view(request):
    if request.method == "POST":
        language = request.POST.get("language")
        print(language)
        if language in dict(settings.LANGUAGES):  # Ensure valid language
            activate(language)  # Apply the language
            request.session['django_language'] = language  # Store in session
            response = redirect(request.META.get("HTTP_REFERER", "/"))
            response.set_cookie('django_language', language)  # Store in cookie
            return response
    return redirect("/")

# Stroke dictionary for each letter
# stroke_dict = {
#     'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
#     'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
#     'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
#     'Y': 3, 'Z': 3
# }
#
#
# def get_strokes_for_word(word: str) -> list:
#     """Convert a word into a list of stroke counts for each letter."""
#     return [stroke_dict[ch] for ch in word.upper() if ch in stroke_dict]
#
#
# def interleave_tokens(name1: str, name2: str) -> list:
#     """Interleave words from two names, filling missing words with '0'."""
#     tokens1 = name1.split()
#     tokens2 = name2.split()
#
#     max_len = max(len(tokens1), len(tokens2))
#     merged_tokens = []
#
#     for i in range(max_len):
#         merged_tokens.append(tokens1[i] if i < len(tokens1) else "0")
#         merged_tokens.append(tokens2[i] if i < len(tokens2) else "0")
#
#     return merged_tokens
#
#
# def adjacency_sum(arr: list) -> list:
#     """Reduce the list by summing adjacent numbers until two digits remain."""
#     while len(arr) > 2:
#         arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
#     return arr
#
#
# def get_name_compatibility(name1: str, name2: str) -> int:
#     """Calculate the compatibility score between two names."""
#     merged_tokens = interleave_tokens(name1, name2)
#     stroke_list = [stroke for token in merged_tokens for stroke in get_strokes_for_word(token)]
#     final_two = adjacency_sum(stroke_list)
#     return int("".join(map(str, final_two)))
#
#
# def split_names(name1, name2):
#     words1 = name1.split()  # Split name1 into words
#     words2 = name2.split()  # Split name2 into words
#
#     merged = []
#     max_len = max(len(words1), len(words2))
#
#     # Merge names in an alternating pattern
#     for i in range(max_len):
#         if i < len(words1):
#             merged.append(words1[i])
#         if i < len(words2):
#             merged.append(words2[i])
#
#     # Ensure the final list has exactly 6 elements, filling with "_"
#     if len(merged) <= 4:
#         while len(merged) <= 4:
#             merged.append("_")
#         return merged[:4]
#     if len(merged) > 4:
#         while len(merged) < 6:
#             merged.append("_")
#         return merged[:6]
        # Return exactly 6 elements


def save_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        result_id = data.get("result_id")
        print(f"Received location: {latitude}, {longitude}")
        CompatibilityResult.objects.filter(id=result_id).update(latitude=latitude, longitude=longitude)
        return JsonResponse({"message": "Location saved successfully"})
    return JsonResponse({"error": "Invalid request"}, status=400)



def auto_suggest_names(request):
    raw_query = request.GET.get('query', '').strip().lower()
    if not raw_query:
        return JsonResponse({'suggestions': []})

    # Split on spaces so "jo sm" still works
    query_parts = raw_query.split()

    # Pull only the two name fields from records with coords
    results = CompatibilityResult.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).values_list('name1', 'name2')

    unique_names = set()
    for name1, name2 in results:
        for name in (name1, name2):
            name_lower = name.lower()
            # also consider the version without any spaces
            name_nospace = name_lower.replace(" ", "")

            for q in query_parts:
                # match if q is in any word, or in the full nospace string
                if (
                    any(q in part for part in name_lower.split()) or
                    q in name_nospace
                ):
                    unique_names.add(name)
                    break

    suggestions = list(unique_names)[:10]
    return JsonResponse({'suggestions': suggestions})
@csrf_exempt
def create_checkout_session(request):
    # success_url = request.GET.get("success_url", "https://yourwebsite.com/success")
    # cancel_url = request.GET.get("cancel_url", "https://yourwebsite.com/cancel")
    #
    # session = stripe.checkout.Session.create(
    #     payment_method_types=["card"],
    #     line_items=[
    #         {
    #             "price_data": {
    #                 "currency": "usd",
    #                 "product_data": {"name": "Fixed Payment"},
    #                 "unit_amount": 300,  # $3 in cents
    #             },
    #             "quantity": 1,
    #         }
    #     ],
    #     mode="payment",
    #     success_url=success_url,
    #     cancel_url=cancel_url,
    # )
    #
    # return JsonResponse({"session_id": session.id})

    try:
        intent = stripe.PaymentIntent.create(
            amount=300,  # Amount in cents ($10)
            currency="usd",
        )
        return JsonResponse({'client_secret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def post(self, request, *args, **kwargs):
        name1 = request.POST.get("name1", "").strip()
        name2 = request.POST.get("name2", "").strip()
        latitude = request.POST.get("latitude")  # Get latitude from form
        longitude = request.POST.get("longitude")  # Get longitude from form

        compatibility_score = get_name_compatibility(name1, name2)

        # Save to database
        CompatibilityResult.objects.create(
            name1=name1,
            name2=name2,
            compatibility_score=compatibility_score,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None
        )

        return self.get(request)

    def get(self, request, *args, **kwargs):
        # Retrieve past results
        past_results = CompatibilityResult.objects.order_by('-created_at')[:10]

        # Count occurrences of each name separately
        name1_counts = (
            CompatibilityResult.objects.values("name1")
            .annotate(count=Count("name1"))
        )
        name2_counts = (
            CompatibilityResult.objects.values("name2")
            .annotate(count=Count("name2"))
        )

        # Merge both counts using Counter
        name_counter = Counter()
        for entry in name1_counts:
            name_counter[entry["name1"]] += entry["count"]
        for entry in name2_counts:
            name_counter[entry["name2"]] += entry["count"]

        # Get the 10 most common names
        top_names = name_counter.most_common(10)

        context = self.get_context_data()
        context["past_results"] = past_results
        context["top_names"] = top_names  # Send top names to template
        return render(request, self.template_name, context)


class CalculateView(TemplateView):
    template_name = "calculate.html"

    def post(self, request, *args, **kwargs):

        if get_language() == 'ko' or get_language() == 'hu' or get_language()=='vi':
            # Korean name format
            name1_first = request.POST.get("name1_first", "").strip()
            name1_middle = request.POST.get("name1_middle", "").strip()
            name1_last = request.POST.get("name1_last", "").strip()
            name2_first = request.POST.get("name2_first", "").strip()
            name2_middle = request.POST.get("name2_middle", "").strip()
            name2_last = request.POST.get("name2_last", "").strip()

            name1 = f"{name1_first} {name1_middle} {name1_last}".strip() if name1_middle else f"{name1_first} {name1_last}".strip()
            name2 = f"{name2_first} {name2_middle} {name2_last}".strip() if name2_middle else f"{name2_first} {name2_last}".strip()
        else:
            # Other languages format
            name1_first = request.POST.get("name1_first", "").strip()
            name1_middle = request.POST.get("name1_middle", "").strip()
            name1_last = request.POST.get("name1_last", "").strip()
            name2_first = request.POST.get("name2_first", "").strip()
            name2_middle = request.POST.get("name2_middle", "").strip()
            name2_last = request.POST.get("name2_last", "").strip()

            name1 = f"{name1_first} {name1_middle} {name1_last}".strip() if name1_middle else f"{name1_first} {name1_last}".strip()
            name2 = f"{name2_first} {name2_middle} {name2_last}".strip() if name2_middle else f"{name2_first} {name2_last}".strip()

        # name1 = request.POST.get("name1", "").strip()
        # name2 = request.POST.get("name2", "").strip()
        latitude = request.POST.get("latitude")  # Get latitude from form
        longitude = request.POST.get("longitude")  # Get longitude from form

        # compatibility_score = get_name_compatibility(name1, name2)
        compatibility_score,steps = get_name_compatibility_with_5steps(name1, name2)

        # Save to database
        result = CompatibilityResult.objects.create(
            name1=name1,
            name2=name2,
            compatibility_score=compatibility_score,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None
        )
        # context = self.get_context_data()
        # context['compatibility_score'] = compatibility_score
        # context['name1'] = name1
        # context['name2'] = name2
        # name_parts = split_names(name1, name2)
        # context['name_parts'] = name_parts
        # context['result'] = result
        # return render(request, 'result.html', context)

        return redirect(result.get_absolute_url())

    def get(self, request, *args, **kwargs):

        current_language = get_language()
        print(f"Current language: {current_language}")
        
        # Retrieve past results
        past_results = CompatibilityResult.objects.order_by('-created_at')[:10]

        # Count occurrences of each name separately
        name1_counts = (
            CompatibilityResult.objects.values("name1")
            .annotate(count=Count("name1"))
        )
        name2_counts = (
            CompatibilityResult.objects.values("name2")
            .annotate(count=Count("name2"))
        )

        # Merge both counts using Counter
        name_counter = Counter()
        for entry in name1_counts:
            name_counter[entry["name1"]] += entry["count"]
        for entry in name2_counts:
            name_counter[entry["name2"]] += entry["count"]

        # Get the 10 most common names
        top_names = name_counter.most_common(10)

        context = self.get_context_data()
        context["past_results"] = past_results
        context["top_names"] = top_names  # Send top names to template
        context["LANGUAGES"] = settings.LANGUAGES
        return render(request, self.template_name, context)


class ResultDetailView(DetailView):
    model = CompatibilityResult
    template_name = "result.html"
    context_object_name = "result"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = self.get_object()
        context['compatibility_score'] = result.compatibility_score
        context['name1'] = result.name1
        context['name2'] = result.name2
        context['name_parts'] = split_names_safe(result.name1, result.name2)
        context['result'] = result
        compatibility_score, steps = get_name_compatibility_with_5steps(result.name1, result.name2)
        print(steps)
        stroke_dict = GLOBAL_STROKE_DICT.get(get_language())
        context['stroke_dict'] = stroke_dict
        context['steps'] = steps
        return context

class SearchView(TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "").strip()
        latitude = request.GET.get("latitude", None)
        longitude = request.GET.get("longitude", None)
        radius_input = request.GET.get("radius", None)  # Radius in KM

        results = CompatibilityResult.objects.all()
        mention_count = 0

        # if query:
        #     # results = results.filter(Q(name1__icontains=query) | Q(name2__icontains=query))
        #     results = results.filter(Q(name1=query) | Q(name2=query))

        if latitude and longitude and radius_input:
            try:
                user_location = (float(latitude), float(longitude))
                radius = 1
                if radius_input == '1':
                    radius = 1
                if radius_input == '2':
                    radius = 50
                if radius_input == '3':
                    radius = 200
                if radius_input == '4':
                    radius = 99999999999

                radius = float(radius)

                # Apply distance filter
                filtered_results = []

                for record in results:
                    if record.latitude and record.longitude:
                        record_location = (record.latitude, record.longitude)
                        distance = geodesic(user_location, record_location).km
                        # print(distance,radius)
                        if distance <= radius:
                            filtered_results.append(record)
                            if query.lower() == record.name1.lower():
                                mention_count += 1
                            if query.lower() == record.name2.lower():
                                mention_count += 1

                results = filtered_results  # Override results with filtered data
            except ValueError:
                pass  # Ignore errors if input is incorrect



        name_counter = Counter()
        for result in results:
            if result.name1 == result.name2:
                # same name, count once
                name_counter[result.name1] += 1
            else:
                # two different names, count both
                name_counter[result.name1] += 1
                name_counter[result.name2] += 1

        # Get sorted names
        sorted_names = name_counter.most_common()
        print('sorted names',sorted_names)

        # Calculate ranks with same rank for equal mentions
        ranked_names = []
        current_rank = 1
        current_count = None
        skip_ranks = 0

        for idx, (name, count) in enumerate(sorted_names):
            if count != current_count:
                current_rank = idx + 1
                current_count = count

            ranked_names.append((name, count, current_rank))

        # Get top 10 with ranks
        top_names = ranked_names[:10]

        # Get rank of the query
        search_rank = None
        query_lower = query.lower()
        for idx, (name, count, rank) in enumerate(ranked_names):
            if name.lower() == query_lower:
                search_rank = idx+1
                break
        # print(results)
        context = {
            "results": results,
            "search_key": query,
            "mention_count": mention_count,
            "top_names" : [(name, count) for name, count, rank in top_names],
            "top_names_with_ranks": top_names,
            "radius_input": radius_input,
            "search_rank":search_rank,
            "lat" : latitude if latitude else None,
            "lon" : longitude if longitude else None,
        }

        return render(request, self.template_name, context)


class ListView(TemplateView):
    template_name = "list.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("key", "").strip()
        latitude = request.GET.get("lat", None)
        longitude = request.GET.get("lon", None)
        radius_input = request.GET.get("radius", None)
        success = request.GET.get("success", None)
        results = CompatibilityResult.objects.all()
        mention_count = 0
        # Filter by Name
        if query:
            # results = results.filter(Q(name1__icontains=query) | Q(name2__icontains=query))
            results = results.filter(Q(name1=query) | Q(name2=query))

        # Filter by Location Radius
        if latitude and longitude and radius_input:
            try:
                user_location = (float(latitude), float(longitude))
                radius = 1
                if radius_input == '1':
                    radius = 1
                if radius_input == '2':
                    radius = 50
                if radius_input == '3':
                    radius = 200
                if radius_input == '4':
                    radius = 99999999999

                radius = float(radius)

                # Apply distance filter
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

                results = filtered_results  # Override results with filtered data
            except ValueError:
                pass  # Ignore errors if input is incorrect
        context = {
            "results": results,
            "search_key": query,
            "mention_count": mention_count,
            "radius_input" : radius_input,
            "lat" : latitude if latitude else None,
            "lon" : longitude if longitude else None,
            "STRIPE_PUBLISHABLE_KEY":settings.STRIPE_PUBLISHABLE_KEY,
            "success":success
        }

        print(f"Filtered results: {len(results)}")

        return render(request, self.template_name, context)




class SearchBasicView(TemplateView):
    template_name = "search_basic.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "").strip()
        latitude = request.GET.get("latitude", None)
        longitude = request.GET.get("longitude", None)
        radius = request.GET.get("radius", None)  # Radius in KM

        results = CompatibilityResult.objects.all()

        # Filter by Name
        if query:
            results = results.filter(Q(name1__icontains=query) | Q(name2__icontains=query))

        # Filter by Location Radius
        if latitude and longitude and radius:
            try:
                user_location = (float(latitude), float(longitude))
                radius = float(radius)

                # Apply distance filter
                filtered_results = []
                for record in results:
                    if record.latitude and record.longitude:
                        record_location = (record.latitude, record.longitude)
                        distance = geodesic(user_location, record_location).km
                        if distance <= radius:
                            filtered_results.append(record)

                results = filtered_results  # Override results with filtered data
            except ValueError:
                pass  # Ignore errors if input is incorrect

        # Count mentions of the search key
        total_mentions = 0
        mentioned_with = {}

        if query:
            # Count occurrences where the search key appears as name1 or name2
            total_mentions = CompatibilityResult.objects.filter(
                Q(name1=query) | Q(name2=query)
            ).count()

            # Count names mentioned with the search key separately
            name1_counts = (
                CompatibilityResult.objects.filter(name1=query)
                .values(name=F("name2"))
                .annotate(count=Count("name2"))
            )

            name2_counts = (
                CompatibilityResult.objects.filter(name2=query)
                .values(name=F("name1"))
                .annotate(count=Count("name1"))
            )

            # Merge the results manually
            mentioned_with = {}
            for entry in name1_counts:
                mentioned_with[entry["name"]] = entry["count"]

            for entry in name2_counts:
                if entry["name"] in mentioned_with:
                    mentioned_with[entry["name"]] += entry["count"]
                else:
                    mentioned_with[entry["name"]] = entry["count"]

            # Convert to sorted list
            mentioned_with = sorted(
                [{"mentioned_name": k, "count": v} for k, v in mentioned_with.items()],
                key=lambda x: x["count"],
                reverse=True,
            )

        context = {
            "results": results,
            "search_key": query,
            "total_mentions": total_mentions,
            "mentioned_with": mentioned_with,
        }

        return render(request, self.template_name, context)


