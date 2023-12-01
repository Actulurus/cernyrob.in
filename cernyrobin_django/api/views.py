from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api.models import System, Kafka

from api.yt_transcriptor import main as yt_transcriptor

import datetime

GENERATE_RATE_LIMIT = 60 * 60 * 24 * 7 - 60 * 60 * 6 # 7 days minus six hours to prevent it from shifting too far forward

def kafka(request, subdomain):
    return HttpResponse("Hello, world. You're at the api index.")

def kafka_get(request, subdomain):
    response = {"code": 200, "message": "OK"}

    video_url = request.GET.get("video_url")

    if not video_url:
        response["code"] = 400
        response["message"] = "Bad request"

        return JsonResponse(response)

    video_url = video_url.replace("\"", "")

    try:
        kafka = Kafka.objects.get(video_url=video_url)

        response["code"] = 200
        response["message"] = "OK"
        response["data"] = {
            "answers": kafka.answers,
            "transcript": kafka.transcript,
            "language": kafka.language,
        }

        return JsonResponse(response)
    except Kafka.DoesNotExist:
        response["code"] = 404
        response["message"] = "Not found"

        return JsonResponse(response)
    except Exception as e:
        print(e)
        response["code"] = 500
        response["message"] = "Internal server error"

        return JsonResponse(response)

def kafka_list(request, subdomain):
    response = {"code": 200, "message": "OK", "list": {}}

    try:
        for kafka in Kafka.objects.all():
            response["list"]["video_url"] = {
                "answers": kafka.answers,
                "transcript": kafka.transcript,
                "language": kafka.language,
            }
    except Exception as e:
        print(e)
        response["code"] = 500
        response["list"] = {}
        response["message"] = "Internal server error"

    return JsonResponse(response)

def kafka_answer(request, subdomain):
    response = {"code": 200, "message": "OK"}

    video_url = request.GET.get("video_url")
    language = request.GET.get("language")

    if not video_url:
        response["code"] = 400
        response["message"] = "Bad request"

        return JsonResponse(response)
    
    if not language:
        language = "cs-CZ"

    video_url = video_url.replace("\"", "")

    try:
        # Always use a rate limit when dealing with OpenAI API requests!

        system_data = System.objects.get_or_create(key="SYSTEM_DATA")
        
        if (datetime.datetime.now().replace(tzinfo=None) - system_data[0].last_generated.replace(tzinfo=None)).total_seconds() < GENERATE_RATE_LIMIT:
            response["code"] = 429
            response["message"] = "Rate limit exceeded"

            return JsonResponse(response)
        
        system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None)
        system_data[0].save()

        answers, transcript = yt_transcriptor.run(video_url, language)

        # Save to database
        kafka, created = Kafka.objects.get_or_create(video_url=video_url)

        kafka.answers = answers
        kafka.transcript = transcript
        kafka.language = language
        kafka.save()

        response["code"] = 200
        response["message"] = "OK"
        response["data"] = {
            "answers": answers,
            "transcript": transcript,
            "language": language,
        }

        return JsonResponse(response)
    except Exception as e:
        print(e)
        response["code"] = 500
        response["message"] = "Internal server error"

        return JsonResponse(response)

