from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from .models import Ad
from cdn import views as cdn

import re

def is_valid_string(s):
    pattern = re.compile("^[a-zA-Z0-9_ ]*$")
    match = pattern.match(s)

    return bool(match)

def get_ad(id):
    try:
        return Ad.objects.get(ad_id=id)
    except Ad.DoesNotExist:
        return None
    
def get_ads_by_owner(owner_name):
    return Ad.objects.filter(owner_name=owner_name)

def get_random_ad():
    all_active_ads = Ad.objects.filter(status="active")

    return all_active_ads.order_by('?').first()

def get_all_ads():
    return Ad.objects.all()

def get_pending_ads():
    return Ad.objects.filter(status="pending")

def get_ad_json(ad):
    return {
        "ad_id": ad.ad_id,
        "owner_name": ad.owner_name,
        "name": ad.name,
        "status": ad.status,
        "link": ad.link,
        "image_link": ad.image_link
    }

def create_ad(owner_name, name, image_file, link):
    image_link = cdn.upload_image(image_file)

    ad = Ad(owner_name=owner_name, name=name, image_link=image_link, link=link)

    ad.save()

    return ad

def delete_ad(id):
    ad = get_ad(id)

    if ad is not None:
        image_path = ad.image_link
        image_name = image_path.split("/")[-1]

        cdn.delete_image(image_name)
        ad.delete()

def get_owner_name(request):
    user = request.user.username

    if user is not None and user != "" and user != "AnonymousUser" and user != "anonymous":
        return user
    else:
        return None

def my_ads(request, subdomain):
    if request.method == "GET":
        owner_name = get_owner_name(request)

        if owner_name is not None:
            context = {
                "ads": get_ads_by_owner(owner_name),
            }

            return render(request, "ads/view.html", context)

        return JsonResponse({"error": "you must be logged in"}, status=400)

    return JsonResponse({"error": "GET method required"}, status=400)

def manage(request, subdomain):
    return render(request, "ads/manage.html")

def manage_submit(request, subdomain):
    if request.method == "POST":
        owner_name = get_owner_name(request)
        
        if owner_name is not None and request.FILES["image_file"]:
            name = request.POST.get("name")
            image_file = request.FILES["image_file"]
            link = request.POST.get("link")

            if name is not None and image_file is not None and link is not None:
                # Validate if image file is an image

                if len(name) > 30:
                    return JsonResponse({"error": "name cannot be longer than 30 characters"}, status=400)
                
                if len(link) > 400:
                    return JsonResponse({"error": "link cannot be longer than 400 characters"}, status=400)

                if not link.startswith("http://") and not link.startswith("https://"):
                    link = "https://" + link

                if not is_valid_string(name):
                    return JsonResponse({"error": "name can only contain letters and numbers"}, status=400)

                ad = create_ad(owner_name, name, image_file, link)

                return redirect("/me/")

            return JsonResponse({"error": "name, image_file and link required"}, status=400)

        return JsonResponse({"error": "you must be logged in"}, status=400)

def manage_delete(request, subdomain):
    if request.method == "GET":
        owner_name = get_owner_name(request)

        if owner_name is not None:
            id = request.GET.get("id")

            if id is not None:
                id = int(id)

                if id is None:
                    return JsonResponse({"error": "id is not a number"})
                
                ad = get_ad(id)

                if ad is not None:
                    if ad.owner_name == owner_name:
                        delete_ad(id)

                        return redirect("/me/")

                    return JsonResponse({"error": "you are not the owner of this ad"}, status=400)

                return JsonResponse({"error": "ad not found"}, status=404)

            return JsonResponse({"error": "id required"}, status=400)

        return JsonResponse({"error": "you must be logged in"}, status=400)

def ad(request, subdomain):
    if request.method == "GET":
        id = request.GET.get("id")

        if id is not None:
            id = int(id)

            if id is None:
                return JsonResponse({"error": "id is not a number"})
            ad = get_ad(id)

            if ad is not None:
                return JsonResponse(get_ad_json(ad))

            return JsonResponse({"error": "ad not found"}, status=404)

        return JsonResponse({"error": "id required"}, status=400)
    
def get_ads(length=3):
    context = {
        "ads_left": [],
        "ads_right": [],
    }

    for i in range(length):
        def add_random(t):
            ad = get_random_ad()

            if ad is None:
                return

            t.append(
                {
                    "name": ad.name,
                    "link": ad.link,
                    "image_link": ad.image_link,
                }
            )

        add_random(context["ads_left"])
        add_random(context["ads_right"])

    return context

def admin_pending(request, subdomain):
    if request.method == "GET":
        if request.user.is_staff == False:
            return JsonResponse({"error": "you must be an admin"}, status=400)
        
        context = {
            "ads": get_pending_ads(),
        }

        return render(request, "ads/admin_pending.html", context)

    return JsonResponse({"error": "GET method required"}, status=400)

def admin_accept(request, subdomain):
    if request.method == "GET":
        if request.user.is_staff == False:
            return JsonResponse({"error": "you must be an admin"}, status=400)
        
        id = request.GET.get("id")

        if id is not None:
            id = int(id)

            if id is None:
                return JsonResponse({"error": "id is not a number"})
            ad = get_ad(id)

            if ad is not None:
                ad.status = "active"
                ad.save()

                return redirect("/pending/")

            return JsonResponse({"error": "ad not found"}, status=404)

        return JsonResponse({"error": "id required"}, status=400)

    return JsonResponse({"error": "GET method required"}, status=400)

def admin_reject(request, subdomain):
    if request.method == "GET":
        if request.user.is_staff == False:
            return JsonResponse({"error": "you must be an admin"}, status=400)
        
        id = request.GET.get("id")

        if id is not None:
            id = int(id)

            if id is None:
                return JsonResponse({"error": "id is not a number"})
            ad = get_ad(id)

            if ad is not None:
                ad.status = "rejected"
                ad.save()

                return redirect("/pending/")

            return JsonResponse({"error": "ad not found"}, status=404)

        return JsonResponse({"error": "id required"}, status=400)

    return JsonResponse({"error": "GET method required"}, status=400)