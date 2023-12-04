from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api.models import System, Kafka, Job

from api.yt_transcriptor import main as yt_transcriptor
from api import get_video_info

import datetime, json, re, threading

GENERATE_RATE_LIMIT = 60 * 60 * 24 * 7 - 60 * 60 * 6 # 7 days minus six hours to prevent it from shifting too far forward
KAFKA_CHANNEL = "https://www.youtube.com/@jankafka1535"
DESCRIPTION_FORMAT = r"Výklad na dálku\s+Otázky k videu:(?:\s+\d+\.\s+.*?)+(?=\n\n|\Z)"

def get_answers(video_url):
    try:
        kafka = Kafka.objects.get(video_url=video_url)

        return kafka.answers
    except Kafka.DoesNotExist:
        return None
    
def get_transcript(video_url):
    try:
        kafka = Kafka.objects.get(video_url=video_url)

        return kafka.transcript
    except Kafka.DoesNotExist:
        return None

def get_last_generated():
    try:
        system_data = System.objects.get_or_create(key="SYSTEM_DATA")

        return system_data[0].last_generated.replace(tzinfo=None).timestamp()
    except System.DoesNotExist:
        return 0
    except Exception as e:
        print(e)
        return 0
    
def id_from_url(url):
    if url.find("watch?v=") != -1:
        id = url.split("watch?v=")[1]
        if id.find("&") != -1:
            id = id.split("&")[0]

        return id
    elif url.find("youtu.be/") != -1:
        id = url.split("youtu.be/")[1]
        if id.find("?") != -1:
            id = id.split("?")[0]

        return id
    
def is_json(js):
    try:
        json.loads(js)
    except:
        return False
    
    return True

def get_all_to_be_displayed():
    all_data = []

    for kafka in Kafka.objects.all():
        if kafka.video_info is None:
            continue
        elif not is_json(kafka.video_info):
            continue
        
        video_info = json.loads(kafka.video_info)

        all_data.append({
                    "video_id": id_from_url(kafka.video_url),
                    "description": video_info["description"],
                    "title": video_info["title"],
                })
    
    return all_data

def generate_answers(video_url, language, runbackground=False):
    response = {"code": 200, "message": "OK"}

    video_info = get_video_info.get_video_info(video_url)

    if video_info is None:
        return HttpResponse("Video not found")
    
    if json.loads(video_info)["author_url"] != KAFKA_CHANNEL:
        return HttpResponse("Invalid video channel")
    
    if not re.search(DESCRIPTION_FORMAT, json.loads(video_info)["description"]):
        return HttpResponse("Invalid video description")

    try:
        # Always use a rate limit when dealing with OpenAI API requests!

        system_data = System.objects.get_or_create(key="SYSTEM_DATA")

        if not system_data[0].last_generated:
            system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None).timestamp()
            system_data[0].save()

        try:
            kafka = Kafka.objects.get(video_url=video_url)

            response["code"] = 200
            response["message"] = "OK"
            response["data"] = {
                "answers": kafka.answers,
                "transcript": kafka.transcript,
                "language": language,
                "video_info": json.loads(kafka.video_info),
                "video_url": video_url,
            }
        except Kafka.DoesNotExist:
            kafka = None
        
        if False and (datetime.datetime.now().replace(tzinfo=None).timestamp() - system_data[0].last_generated) < GENERATE_RATE_LIMIT:
            return HttpResponse("Rate limit exceeded")
        
        system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None).timestamp()
        system_data[0].save()

        job, created = Job.objects.get_or_create(id=id_from_url(video_url))  

        if not created and (datetime.datetime.now().replace(tzinfo=None).timestamp() - job.created.replace(tzinfo=None).timestamp() < 30 * 60):
            job.delete()
            job, created = Job.objects.get_or_create(id=id_from_url(video_url))

        if created:
            job.video_url = video_url
            job.percent_completed = 0
            job.finished = False
            job.save()
        else:
            return HttpResponse("Job already running")

        def run():
            def progress_callback(chunk, max_chunks):
                print("Finished chunk " + str(chunk) + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                job.percent_completed = round((chunk + 1) / max_chunks * 100)
                job.chunks_completed = chunk + 1
                job.total_chunks = max_chunks
                job.save()
            
            answers, transcript = yt_transcriptor.run(video_url, language, callback=progress_callback)

            # Save to database
            kafka, created = Kafka.objects.get_or_create(video_url=video_url)

            kafka.answers = answers
            kafka.transcript = transcript
            kafka.language = language
            kafka.video_info = video_info
            
            kafka.save()

            job.percent_completed = 100
            job.finished = True
            job.save()

            if not runbackground:
                response["code"] = 200
                response["message"] = "OK"
                response["data"] = {
                    "answers": answers,
                    "transcript": transcript,
                    "language": language,
                    "video_info": json.loads(kafka.video_info),
                    "video_url": video_url,
                }

            
                return JsonResponse(data=response)
        
        if runbackground:
            daemon = threading.Thread(target=run, daemon=True)

            daemon.start()

            return HttpResponse(id_from_url(video_url))
        
    except Exception as e:
        print(e)
        response["code"] = 500
        response["message"] = "Internal server error"

        return JsonResponse(data=response)


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
            "video_info": json.loads(kafka.video_info),
            "video_url": video_url,
        }

        return JsonResponse(data=response)
    except Kafka.DoesNotExist:
        response["code"] = 404
        response["message"] = "Not found"

        return JsonResponse(data=response)
    except Exception as e:
        print(e)
        response["code"] = 500
        response["message"] = "Internal server error"

        return JsonResponse(data=response)

def kafka_list(request, subdomain):
    if request.method != "GET":
        return HttpResponse("Bad request")

    response = {"code": 200, "message": "OK", "list": {}}

    try:
        for kafka in Kafka.objects.all():
            response["list"][kafka.video_url] = {
                "answers": kafka.answers,
                "transcript": kafka.transcript,
                "language": kafka.language,
                "video_info": json.loads(kafka.video_info),
                "video_url": kafka.video_url,
            }
    except Exception as e:
        print(e)
        response["code"] = 500
        response["list"] = {}
        response["message"] = "Internal server error"

    return JsonResponse(data=response)

def kafka_answer(request, subdomain):
    video_url = request.GET.get("video_url")
    language = request.GET.get("language")

    if not video_url:
        return HttpResponse("Bad request") # Not returning JSON to prevent bots
    
    if not language:
        language = "cs-CZ"

    video_url = video_url.replace("\"", "")

    return generate_answers(video_url, language)

def kafka_job(request, subdomain):
    if request.method == "GET":
        job_id = request.GET.get("id")

        if not job_id:
            return HttpResponse("Bad request")
        
        try:
            job = Job.objects.get(id=job_id)

            return JsonResponse(data={
                "video_url": job.video_url,
                "percent_completed": job.percent_completed,
                "chunks_completed": job.chunks_completed,
                "total_chunks": job.total_chunks,
                "finished": job.finished,
            })
        except Job.DoesNotExist:
            return HttpResponse("Job not found")
        except Exception as e:
            print(e)
            return HttpResponse("Internal server error")