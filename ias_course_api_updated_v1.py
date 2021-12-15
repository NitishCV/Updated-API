import requests
import pandas as pd
import json
import datetime
from natsort import natsorted
import numpy as np
import configparser
import ast
import re
import dateutil.parser as parser
from requests.structures import CaseInsensitiveDict
from iteration_utilities import unique_everseen
import os
import glob
import shutil
import pdb
import sys

json_template_schema = """{
   "content_module":[],
   "title":"",
   "subtitle":"",
   "description":"",
   "learn_type":{},
   "created_by":{},
   "updated_by":{},
   "created_at":"",
   "updated_at":"",
   "status":"approved",
   "content":"",
   "internal_status":"approved",
   "partner":{},
   "basic_information":{
      "medium":{},
      "instruction_type":{},
      "embedded_video_url":"",
      "live_class":false,
      "human_interaction":false,
      "personalized_teaching":false,
      "post_course_interaction":false,
      "international_faculty":false,
      "image":{},
      "video":null
   },
   
   "detail_information":{
      "level":null,
      "enrollment_start_date":null,
      "enrollment_end_date":null,
      "duration":{
      "total_video_content_in_hrs": null,
      "total_duration_in_hrs": "",
      "recommended_effort_per_week": null,
      "avg_session_duration_with_instructor": null,
      "total_video_content_unit":"",
      "total_duration_unit": ""
    },
      "batches":[],
      "languages":{},
      "accessibilities":[],
      "availabilities":[],
      "subtitles":[]
   },
   
   "pricing":{
    "pricing_type": "",
    "currency": "",
    "regular_price": null,
    "sale_price": null,
    "schedule_of_sale_price": null,
    "additional_details": null,
    "course_financing_options": false,
    "display_price": false,
    "indian_students": {
        "program_fee": null,
        "payment_deadline": "",
        "GST": false
    },
    "indian_student_installments": [
        {
            "installment_amount": null,
            "payment_deadline": ""
        }
    ],
    "international_students": {
        "program_fee": null,
        "payment_deadline": ""
    },
    "international_student_installments": [
        {
            "installment_amount": null,
            "payment_deadline": ""
        }
    ]
    },
   "provider_information":{
      "provider":{}, "provider_url": null },
   "what_will_learn":[
      {
         "option":""
      }
   ],
   "target_students":[
      {
         "option":""
      }
   ],
   "prerequisites":[
      {
         "option":""
      }
   ],
   "Instructors":[
      {
         "name":"Not Available",
         "designation":"Not Available",
         "instructor_bio":"Not Available",
         "linkedin_url":null,
         "facebook_url":null,
         "twitter_url":null,
         "instructor_image":null
      }
   ],
   "reviews":[
      {
         "reviewer_name":"Not Available",
         "review_date":"",
         "review":"",
         "rating":"",
         "photo":null
      }
   ],
   "hands_on_training":{},
   "placements":null,
   "corporate_sponsors":[],
   "accreditations":[],
   "topics":[],
   "skills":[],
   "faq":[],
   "course_details":{},
   "additional_batches" :[]
}"""

#
# admin
# response = requests.post("https://backend.careervira.com/admin/login",data = { 'email' : 'latesh@ajency.in', 'password' : 'Coursera#123' , 'Content-Type' : "application/json"}).json()["data"]
# instruction_type = requests.get("https://backend.careervira.com/learn-contents", headers = {"Authorization": f"Bearer {response['token']}"}).json()
response = requests.post(
    "https://backend.careervira.com/admin/login",
    data={
        # "email": "coursera@careervira.com",
        "email": "latesh@ajency.in",
        # "password": "Coursera#123",
        "password": "Ajency#123",
        "Content-Type": "application/json",
    },
).json()["data"]
# Batch-Type

batch_type = requests.get(
    "https://backend.careervira.com/batch-types",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# time-zones
time_zones = requests.get("https://backend.careervira.com/time-zones",
                          headers={"Authorization": f"Bearer {response['token']}"}, ).json()
# instruction_type
instruction_type = requests.get(
    "https://backend.careervira.com/instruction-types",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# learn_type
learn_type = requests.get(
    "https://backend.careervira.com/learn-types",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# category
category = requests.get(
    "https://backend.careervira.com/categories",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# availabilities
availabilities = requests.get(
    "https://backend.careervira.com/availabilities",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()


# subtitle = requests.get(
# "https://backend.careervira.com/subtitle",
# headers={"Authorization": f"Bearer {response['token']}"},
# ).json()
# created_by
created_by = '[{"id":79, "firstname":"Coursera", "lastname":"", "username":"coursera@careervira.com", "email":"coursera@careervira.com", "resetPasswordToken":null, "registrationToken":null, "isActive":true, "blocked":false}]'
# updated_by
updated_by = '[{"id":79, "firstname":"Coursera", "lastname":"", "username":"coursera@careervira.com", "email":"coursera@careervira.com", "resetPasswordToken":null, "registrationToken":null, "isActive":true, "blocked":false}]'
# accessibilities
accessibilities = requests.get(
    "https://backend.careervira.com/accessibilities",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# topics
topics = requests.get(
    "https://backend.careervira.com/topics",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# subcategories
subcategories = requests.get(
    "https://backend.careervira.com/sub-categories",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# learning-medium
learningmedium = requests.get(
    "https://backend.careervira.com/learning-mediums",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# skills
skills = requests.get(
    "https://backend.careervira.com/skills",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# providers
providers = requests.get(
    "https://backend.careervira.com/providers",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# languages
languages = requests.get(
    "https://backend.careervira.com/languages",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# mediums
mediums = requests.get(
    "https://backend.careervira.com/mediums",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# levels
levels = requests.get(
    "https://backend.careervira.com/levels",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
# partners
partners = requests.get(
    "https://backend.careervira.com/partners",
    headers={"Authorization": f"Bearer {response['token']}"},
).json()
null = None
# subtitle = [{"id":1,"name":"English","created_by":{"id":1,"firstname":"Robiul","lastname":"Hoque","username":"robiul@ajency.in","email":"robiul@ajency.in","resetPasswordToken":"63460f9ba9fa1ca0624d5381d095c79571b5da37","registrationToken":null,"isActive":true,"blocked":null},"updated_by":{"id":1,"firstname":"Robiul","lastname":"Hoque","username":"robiul@ajency.in","email":"robiul@ajency.in","resetPasswordToken":"63460f9ba9fa1ca0624d5381d095c79571b5da37","registrationToken":null,"isActive":true,"blocked":null},"created_at":"2020-09-30T11:29:16.603Z","updated_at":"2020-09-30T11:29:16.612Z","iso_code":null},{"id":2,"name":"Hindi","created_by":{"id":1,"firstname":"Robiul","lastname":"Hoque","username":"robiul@ajency.in","email":"robiul@ajency.in","resetPasswordToken":"63460f9ba9fa1ca0624d5381d095c79571b5da37","registrationToken":null,"isActive":true,"blocked":null},"updated_by":{"id":1,"firstname":"Robiul","lastname":"Hoque","username":"robiul@ajency.in","email":"robiul@ajency.in","resetPasswordToken":"63460f9ba9fa1ca0624d5381d095c79571b5da37","registrationToken":null,"isActive":true,"blocked":null},"created_at":"2020-09-30T11:29:24.038Z","updated_at":"2020-09-30T11:29:24.043Z","iso_code":null}]
subtitles_temp = [{"id": 1, "name": "English", "created_by": {"id": 1, "firstname": "Robiul", "lastname": "Hoque", "username": "robiul@ajency.in"}, "updated_by": {"id": 1, "firstname": "Robiul", "lastname": "Hoque", "username": "robiul@ajency.in"}, "created_at": "2020-09-30T11:29:16.603Z", "updated_at": "2020-09-30T11:29:16.612Z", "iso_code": null},
                  {"id": 2, "name": "Hindi", "created_by": {"id": 1, "firstname": "Robiul", "lastname": "Hoque", "username": "robiul@ajency.in"}, "updated_by": {"id": 1, "firstname": "Robiul", "lastname": "Hoque", "username": "robiul@ajency.in"}, "created_at": "2020-09-30T11:29:24.038Z", "updated_at": "2020-09-30T11:29:24.043Z", "iso_code": null}]
config_raw_file = (
    "[instruction_type]"
    + "\n"
    + "instruction_type="
    + str(instruction_type)
    + "\n"
    + "[learn_type]"
    + "\n"
    + "learn_type="
    + str(learn_type)
    + "\n"
    + "[category]"
    + "\n"
    + "category="
    + str(category)
    + "\n"
    + "[availabilities]"
    + "\n"
    + "availabilities="
    + str(availabilities)
    + "\n"
    + "[created_by]"
    + "\n"
    + "created_by="
    + str(created_by)
    + "\n"
    + "[updated_by]"
    + "\n"
    + "updated_by="
    + str(updated_by)
    + "\n"
    + "[accessibilities]"
    + "\n"
    + "accessibilities="
    + str(accessibilities)
    + "\n"
    + "[topics]"
    + "\n"
    + "topics="
    + str(topics)
    + "\n"
    + "[subcategories]"
    + "\n"
    + "subcategories="
    + str(subcategories)
    + "\n"
    + "[skills]"
    + "\n"
    + "skills="
    + str(skills)
    + "\n"
    + "[providers]"
    + "\n"
    + "providers="
    + str(providers)
    + "\n"
    + "[languages]"
    + "\n"
    + "languages="
    + str(languages)
    + "\n"
    + "[medium]"
    + "\n"
    + "medium="
    + str(mediums)
    + "\n"
    + "[level]"
    + "\n"
    + "level="
    + str(levels)
    + "\n"
    + "[partner]"
    + "\n"
    + "partner="
    + str(partners)
    + "\n"
    + "[subtitles]"
    + "\n"
    + "subtitle="
    + str(subtitles_temp)
    + "\n"
    + "[learningmedium]"
    + "\n"
    + "learningmedium="
    + str(learningmedium)
    + "\n"
    + "[batch_type]"
    + "\n"
    + "batch_type="
    + str(batch_type)
    + "\n"
    + "[time_zones]"
    + "\n"
    + "time_zones="
    + str(time_zones)
)
with open("config_courses.ini", "w", encoding="utf-8") as f:
    f.write(str(config_raw_file))

config = configparser.RawConfigParser()
config.read("config_courses.ini", encoding="utf-8")

path = os.getcwd()
path = path + "/s3_downloaded_files/final-data/"
csv_files = glob.glob(os.path.join(path, "*.csv"))
if len(csv_files) >= 1:
    for csv_files in csv_files:
        df = pd.read_csv(csv_files)
        # print('read_file')
        # df = pd.read_csv(r'C:\Users\aishu\Desktop\IAS\iimidr_testing.csv',encoding='cp1252')
        df = df.replace(np.nan, "", regex=True)

        def get_required_data(json_key, string_val, output):
            try:
                string_val = json.loads(
                    str(string_val).replace("'", '"').replace("'", '"')
                )
            except:
                string_val = ast.literal_eval(string_val)

            if json_key == 'learning_mediums':
                for each in string_val:
                    if (
                        each.get("default_display_label", "").lower().strip()
                        == output.lower().strip()
                    ):
                        return each
            if output != "" and json_key not in ["partner", "languages", "partner"]:
                if len(string_val) == 1:
                    return string_val[0]
                if json_key in ["learn_type", "Others"]:
                    for each in string_val:
                        if (
                            each.get("default_display_label",
                                     "").lower().strip()
                            == output.lower().strip()
                        ):
                            return each
                        # if each.get("id", ""):
                            # print("---", each)
                            # return each

                for each in string_val:
                    if (
                        each.get("default_display_label", "").lower().strip()
                        == json_key.lower().strip()
                    ):
                        return each

                if json_key in ["availabilities", "medium", "instruction_type", "accessibilities"]:
                    for each in string_val:
                        if (
                            each.get("default_display_label",
                                     "").lower().strip()
                            == output.lower().strip()
                        ):
                            return each
                if json_key in ["subtitles"]:
                    output = data.get('subtitle_languages', '')
                    for each in string_val:
                        if (
                            each.get("name", "").lower(
                            ).strip() == output.lower().strip()
                            or each.get("Name", "").lower().strip()
                            == output.lower().strip()
                        ):
                            return each

            if output != "" and json_key in ["topics", "skills"]:
                for each in string_val:
                    if (
                        each.get("default_display_label", "").lower().strip()
                        == output.lower().strip()
                    ):
                        return each

            if output != "" and json_key in ["languages"]:
                for each in string_val:
                    if (
                        each.get("name", "").lower(
                        ).strip() == output.lower().strip()
                        or each.get("Name", "").lower().strip()
                        == output.lower().strip()
                    ):
                        return each

            if output != "" and json_key in ["partner"]:
                for each in string_val:
                    if (
                        each.get("name", "").lower(
                        ).strip() == output.lower().strip()
                        or each.get("Name", "").lower().strip()
                        == output.lower().strip()
                    ):
                        return each
            return None

        def save_image(url):
            # save image into the local directory
            # print(url)
            filename = None
            if url != "":
                # import urllib.request
                filename = url.split("/")[-1]
                r = requests.get(url, stream=True)
                r.raw.decode_content = True
                with open(filename, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
                # urllib.request.urlretrieve(url, filename)
            return filename

        # image upload into strapi

        def image_upload(filename, response):
            url = "https://backend.careervira.com/upload"
            files = {"files": (filename, open(filename, "rb"), "image/jpg")}
            response2 = requests.post(
                url,
                headers={"Authorization": f"Bearer {response['token']}"},
                files=files,
            )
            # pdb.set_trace()
            response2 = json.loads(response2.text)
            return response2[0]

        def pdf_upload(filename, response):
            url = "https://backend.careervira.com/upload"
            files = {"files": (filename, open(
                filename, "rb"), "application/pdf")}
            response2 = requests.post(
                url,
                headers={"Authorization": f"Bearer {response['token']}"},
                files=files,
            )
            # pdb.set_trace()
            response2 = json.loads(response2.text)
            return response2[0]

        def process_mandatoryfields():
            for nextitem, nextvalue in json_template[key].items():
                if isinstance(nextitem, str) and key in dict_keys and nextvalue == "":
                    # pdb.set_trace()
                    result[key][nextitem] = row.get(key, "")

                if nextvalue == [] or nextvalue == {}:
                    if nextvalue == [] and data.get(nextitem, "") != "":
                        string_val = config.get(nextitem, nextitem)
                        data_temp = get_required_data(
                            nextitem, string_val, data.get(nextitem, "")
                        )
                        result[key][nextitem] = [data_temp]

                    elif nextitem != "image":
                        try:
                            string_val = config.get(nextitem, nextitem)
                            data_temp = get_required_data(
                                nextitem, string_val, data.get(nextitem, "")
                            )
                            if nextitem == "languages":
                                result[key][nextitem] = [data_temp]
                            else:
                                result[key][nextitem] = data_temp
                        except:
                            pass
                    if nextitem in "image":
                        filename = save_image(data.get("cover_image", ""))
                        if filename != None:
                            image_response = image_upload(filename, response)
                            result[key][nextitem] = image_response
                if nextitem == "duration":
                    for duration_key, duration_value in json_template[key][
                        "duration"
                    ].items():
                        if duration_key in [
                            "total_video_content_in_hrs",
                            "total_duration_in_hrs",
                            "recommended_effort_per_week",
                            "avg_session_duration_with_instructor",
                            "total_video_content_unit",
                            "total_duration_unit",
                        ]:
                            if duration_key == "total_duration_in_hrs":
                                result[key][nextitem][duration_key] = data.get(
                                    "total_duration", None
                                )
                            else:
                                result[key][nextitem][duration_key] = data.get(
                                    duration_key, None
                                )
                        else:
                            result[key][nextitem][duration_key] = data.get(
                                duration_key, ""
                            )

                if nextitem == "medium":
                    string_val = config.get(nextitem, nextitem)
                    result[key][nextitem] = get_required_data(
                        nextitem, string_val, data.get("delivery_method", "")
                    )
                if nextitem == "instruction_type":
                    string_val = config.get(nextitem, nextitem)
                    if (
                        data.get("instruction_type") == "Not Available"
                        or "not available"
                    ):
                        result[key][nextitem] = get_required_data(
                            nextitem, string_val, "others"
                        )
                    else:
                        result[key][nextitem] = get_required_data(
                            nextitem, string_val, data.get(
                                "instruction_type", "")
                        )
                if nextitem in [
                    "live_class",
                    "human_interaction",
                    "personalized_teaching",
                    "post_course_interaction",
                    "international_faculty",
                ]:
                    if data.get(key, "") != "":
                        result[key][nextitem] = data.get(key, "")

                if nextitem in [
                    "level",
                    "enrollment_start_date",
                    "enrollment_end_date",
                ]:
                    if data.get(key, "") != "":
                        result[key][nextitem] = data.get(key, "")
                    else:
                        result[key][nextitem] = None
                if nextitem in ["embedded_video_url"]:
                    result[key][nextitem] = row.get(nextitem, "")

        def process_content_manger(result):
            content_manger = natsorted(
                [i for i in dict_keys if i.startswith("content_module")])
            content_manger_check = [data.get(i, '') for i in content_manger]
            while '' in content_manger_check:
                content_manger_check.remove('')
            if len(content_manger_check) >= 1:
                content_manger_key = natsorted(
                    set([i.split("|")[1] for i in content_manger]))
                content_manger_data = []
                for range in content_manger_key:
                    count = str(range)
                    content_manger_sub_key = natsorted(
                        [i for i in dict_keys if i.startswith("content_module|" + count + "|subheading_")])
                    heading = data.get(
                        "content_module|" + range + "|heading", "",
                    )
                    sub_heading = []
                    for sub_key in content_manger_sub_key:
                        sub_key_value = data.get(sub_key, '')
                        sub_heading.append({"subheading": sub_key_value})
                    content_manger_data.append(
                        {"heading": heading, "subheading": sub_heading})
                result['content_module'] = content_manger_data

        def process_sponsor_details(result):
            if key == 'corporate_sponsors':
                corporate_sponsor_records = natsorted(
                    [i for i in dict_keys if i.startswith("corporate_sponsor")])

                corporate_sponsor_records_key = natsorted(
                    set([i.split("|")[1] for i in corporate_sponsor_records]))
                corporate_sponsor_records_check = [
                    data.get(i, '') for i in corporate_sponsor_records]
                while '' in corporate_sponsor_records_check:
                    corporate_sponsor_records_check.remove('')
                if len(corporate_sponsor_records_check) >= 1:
                    corporate_sponsor_record = []
                    for range in corporate_sponsor_records_key:
                        filename = save_image(
                            data.get("corporate_sponsor|" + range + "|logo", ""))
                        image_response = ''
                        if filename != None:
                            image_response = image_upload(filename, response)
                        corporate_sponsor_record.append({"name": data.get(
                            "corporate_sponsor|" + range + "|name", ""), "logo": image_response})
                    result['corporate_sponsors'] = corporate_sponsor_record
            if key == 'accreditations':
                accreditations_records = natsorted(
                    [i for i in dict_keys if i.startswith("accreditation")])

                accreditations_records_key = natsorted(
                    set([i.split("|")[1] for i in accreditations_records]))
                accreditations_records_check = [
                    data.get(i, '') for i in accreditations_records]
                while '' in accreditations_records_check:
                    accreditations_records_check.remove('')
                if len(accreditations_records_check) >= 1:
                    accreditations_record = []
                    for range in accreditations_records_key:
                        filename = save_image(
                            data.get("accreditation|" + range + "|logo", ""))
                        image_response = ''
                        if filename != None:
                            image_response = image_upload(filename, response)
                        accreditations_record.append({"name": data.get("accreditation|" + range + "|name", ""),
                                                     "logo": image_response, "description": data.get("accreditation|" + range + "|description", "")})
                    result['accreditations'] = accreditations_record

        current_date = datetime.datetime.now().isoformat()[:-3] + "Z"
        null = None
        for index, row in df.iterrows():
            try:
                json_template = json.loads(json_template_schema)
                data = row
                dict_keys = data.keys()
                result = json_template
                for key, values in json_template.items():
                    # Fields covered  - title , subtitle , description , content
                    if key in ['topics', 'skills']:
                        string_val = config.get(key, key)
                        temp = get_required_data(
                            key, string_val, data.get(key, ""))
                        result[key] = [temp]

                    if key == 'content_module':
                        process_content_manger(result)

                    if key in ['corporate_sponsors', 'accreditations']:
                        process_sponsor_details(result)

                    # if key in "syllabus":
                        # filename = save_image(data.get("syllabus", ""))
                        # if filename != None:
                        # image_response = pdf_upload(filename, response)
                        # result[key] = image_response

                    if values == "" and key not in ["created_at", "updated_at"]:
                        result[key] = row.get(key, "")
                    if key == "subtitle":
                        result[key] = data.get("short_description")
                    if key in ["created_by", "updated_by"]:
                        string_val = config.get(key, key)
                        string_val = json.loads(
                            str(string_val).replace("'", '"').replace("'", '"')
                        )
                        result[key] = string_val
                    if key in ["created_at", "updated_at"]:
                        result[key] = current_date

                    if values == {} and key not in ["created_by", "updated_by", "hands_on_training", "course_details", "syllabus"]:
                        string_val = config.get(key, key)
                        if key in ["learn_type"]:

                            temp = get_required_data(
                                key, string_val, data.get(key, ""))
                            temp = temp.get("id")
                            if temp is None:
                                temp = get_required_data(
                                    "Others", string_val, data.get(key, "")
                                )
                                temp = temp.get("id")
                            result[key] = temp
                        elif key in ["partner", "institute"]:
                            temp = get_required_data(
                                key, string_val, data.get(key, ""))
                            result[key] = temp
                        else:
                            temp = get_required_data(
                                key, string_val, data.get(key, ""))
                            result[key] = temp

                    if key in ["basic_information", "detail_information"]:
                        process_mandatoryfields()

                    if key in ["pricing"]:
                        for nextitem, nextvalue in json_template[key].items():
                            if nextitem in [
                                "currency",
                                "regular_price",
                                "sale_price",
                                "schedule_of_sale_price",
                                "additional_details",
                                "finance_option",
                                "finance_details",
                                "display_price",
                            ]:
                                result[key][nextitem] = row.get(nextitem, None)
                            # else:
                                # result[key][nextitem] = row.get(nextitem, False)
                            if nextitem in ['course_financing_options']:
                                result[key]["course_financing_options"] = row.get(
                                    'course_financing_available', False)
                            if nextitem in ['additional_details']:
                                result[key]["additional_details"] = row.get(
                                    'additional_pricing_details', None)
                            if nextitem in ['indian_students', 'international_students']:
                                for loopitem, loopvalue in json_template[key][nextitem].items():
                                    if loopitem == 'program_fee':
                                        result[key][nextitem][loopitem] = row.get(
                                            nextitem+'_program_fee', None)
                                    if loopitem == 'payment_deadline':
                                        date_temp = row.get(
                                            nextitem+'_payment_deadline', None)
                                        if date_temp != "":
                                            date_temp = parser.parse(date_temp)
                                            date_temp = date_temp.strftime(
                                                "%Y-%m-%d")
                                        result[key][nextitem][loopitem] = date_temp
                                    if loopitem == 'GST':
                                        result[key][nextitem][loopitem] = row.get(
                                            nextitem+'_GST_included', None)

                                check = result[key][nextitem][loopitem]
                                sample = {"program_fee": None,
                                          "payment_deadline": "", "GST": False}
                                sample1 = {"program_fee": '',
                                           "payment_deadline": "", "GST": False}
                                if check == sample or check == sample1 or check == '':
                                    result[key][nextitem] = None
                            if nextitem in ['indian_student_installments']:
                                indian_student = natsorted(
                                    [i for i in dict_keys if i.startswith("indian_student_installments")])

                                indian_student_key = natsorted(
                                    set([i.split("|")[1] for i in indian_student]))
                                indian_student_data = []
                                for range in indian_student_key:
                                    installment_amount = data.get(
                                        "indian_student_installments|" + range + "|installment_amount", "",
                                    )
                                    payment_deadline = data.get(
                                        "indian_student_installments|" + range + "|payment_deadline", "",
                                    )
                                    if payment_deadline != "":
                                        payment_deadline = parser.parse(
                                            payment_deadline)
                                        payment_deadline = payment_deadline.strftime(
                                            "%Y-%m-%d")
                                    indian_student_data.append(
                                        {"installment_amount": installment_amount, "payment_deadline": payment_deadline})
                                result[key][nextitem] = indian_student_data

                                check = result[key][nextitem]
                                check = list(unique_everseen(check))
                                sample = [
                                    {"installment_amount": None, "payment_deadline": ""}]
                                sample1 = [
                                    {"installment_amount": '', "payment_deadline": ""}]
                                if check == sample or check == sample1 or check == '':
                                    result[key][nextitem] = []
                            if nextitem in ['international_student_installments']:
                                international_student = natsorted(
                                    [i for i in dict_keys if i.startswith("international_student_installments")])

                                international_student_key = natsorted(
                                    set([i.split("|")[1] for i in indian_student]))
                                international_student_installments = []
                                for range in international_student_key:
                                    installment_amount = data.get(
                                        "international_student_installments|" + range + "|installment_amount", "",
                                    )
                                    payment_deadline = data.get(
                                        "international_student_installments|" + range + "|payment_deadline", "",
                                    )
                                    if payment_deadline != "":
                                        payment_deadline = parser.parse(
                                            payment_deadline)
                                        payment_deadline = payment_deadline.strftime(
                                            "%Y-%m-%d")
                                    international_student_installments.append(
                                        {"installment_amount": installment_amount, "payment_deadline": payment_deadline})
                                result[key][nextitem] = international_student_installments
                                check = result[key][nextitem]
                                check = list(unique_everseen(check))
                                sample = [
                                    {"installment_amount": None, "payment_deadline": ""}]
                                sample1 = [
                                    {"installment_amount": '', "payment_deadline": ""}]
                                if check == sample or check == sample1 or check == '':
                                    result[key][nextitem] = []

                    if key in ["provider_information"]:
                        string_val = config.get("providers", "providers")
                        if string_val:
                            string_val = ast.literal_eval(string_val.strip())
                            result[key]["provider"] = string_val[0]
                            result[key]["provider_url"] = data.get(
                                "partner_course_url", None
                            )

                    if key in [
                        "what_will_learn",
                        "target_students",
                        "prerequisites",
                        "skills_gained",
                    ]:
                        splited_value = []

                        if data.get(key, "") != "":
                            for split in data.get(key, "").split("|"):
                                temp_dick = {}
                                temp_dick = {"option": split.strip()}
                                splited_value.append(temp_dick)

                            result[key] = splited_value

                    if key in ["Instructors"]:
                        instructor = natsorted(
                            [i for i in dict_keys if i.startswith(
                                "instructor")]
                        )
                        instructor_key = natsorted(
                            set([i.split("|")[1] for i in instructor])
                        )
                        instructor_data = []
                        for range in instructor_key:
                            row_instructor = {
                                "name": data.get(
                                    "instructor|" + range + "|name", "Not Available"
                                ),
                                "designation": data.get(
                                    "instructor|" + range + "|designation",
                                    "Not Available",
                                ),
                                "instructor_bio": data.get(
                                    "instructor|" + range + "|bio", "Not Available"
                                ),
                                "linkedin_url": data.get(
                                    "instructor|" + range + "|linkedin_url", None
                                ),
                                "facebook_url": data.get(
                                    "instructor|" + range + "|facebook_url", None
                                ),
                                "twitter_url": data.get(
                                    "instructor|" + range + "|twitter_url", None
                                ),
                                "instructor_image": data.get(
                                    "instructor|" + range + "|instructor_image", None
                                ),
                            }
                            instructor_data.append(row_instructor)
                        result[key] = instructor_data
                    if key in ["reviews"]:
                        review = natsorted(
                            [i for i in dict_keys if i.startswith("review")]
                        )
                        review_key = natsorted(
                            set([i.split("|")[1] for i in review]))
                        reviewer_data = []
                        for range in review_key:
                            date_temp = data.get(
                                "review|" + range + "|review_date", "")
                            if date_temp != "":
                                date_temp = parser.parse(date_temp)
                                date_temp = date_temp.strftime("%Y-%m-%d")
                            else:
                                date_temp = parser.parse(current_date)
                                date_temp = date_temp.strftime("%Y-%m-%d")
                            row_review = {
                                "reviewer_name": data.get(
                                    "review|" + range + "|reviewer_name",
                                    "Not Available",
                                ),
                                "review_date": date_temp,
                                "review": data.get(
                                    "review|" + range + "|review", "Not Available"
                                ),
                                "rating": data.get("review|" + range + "|rating", 1),
                                "photo": None,
                            }
                            reviewer_data.append(row_review)
                        result[key] = reviewer_data

                    if key in ["hands_on_training", "placements"]:
                        if key == 'hands_on_training':
                            learning_medium = []
                            string_val = config.get(
                                'learningmedium', 'learningmedium')

                            for le_medium in data.get('learning_mediums', '').split('|'):
                                temp = get_required_data(
                                    'learning_mediums', string_val, le_medium)
                                if temp != None:
                                    learning_medium.append(temp)
                            result[key] = {"virtual_labs": data.get('virtual_labs', False), "case_based_learning": data.get(
                                'case_based_learning', False), "capstone_project": data.get('capstone_project', False), "learning_mediums": learning_medium}

                            check = result[key]
                            sample = {"virtual_labs": '', "case_based_learning": "",
                                      "capstone_project": '', 'learning_mediums': ''}
                            sample1 = {"virtual_labs": '', "case_based_learning": "",
                                       "capstone_project": '', 'learning_mediums': []}
                            if check == sample or check == sample1 or check == '':
                                result[key] = {}
                        if data.get(key, "") != "":
                            result[key] = data.get(key, None)

                    if key in ["faq"]:
                        faq = natsorted(
                            [i for i in dict_keys if i.startswith("Faq")]
                        )
                        faq_key = natsorted(
                            set([i.split("|")[1] for i in faq])
                        )
                        faq_data = []
                        for range in faq_key:
                            row_faq = {
                                "question": data.get(
                                    "Faq|" + range + "|question", ""
                                ),
                                "answer": data.get(
                                    "Faq|" + range + "|answer",
                                    "",
                                ),
                            }
                            faq_data.append(row_faq)
                        result[key] = faq_data
                        check = result[key]
                        check = list(unique_everseen(check))
                        sample = [{"question": '', "answer": ""}]
                        sample1 = [{"question": None, "question": None}]
                        if check == sample or check == sample1 or check == '':
                            result[key] = []
                    if key in ['course_details']:
                        course_start_date = data.get('course_start_date', "")
                        course_end_date = data.get('course_end_date', "")
                        course_details_enrollment_end_date = data.get(
                            'course_details_enrollment_end_date', "")
                        course_details_enrollment_start_date = data.get(
                            'course_details_enrollment_start_date', "")
                        if course_start_date != "":
                            course_start_date = parser.parse(course_start_date)
                            course_start_date = course_start_date.strftime(
                                "%Y-%m-%d")
                        if course_end_date != "":
                            course_end_date = parser.parse(course_end_date)
                            course_end_date = course_end_date.strftime(
                                "%Y-%m-%d")
                        if course_details_enrollment_end_date != "":
                            course_details_enrollment_end_date = parser.parse(
                                course_details_enrollment_end_date)
                            course_details_enrollment_end_date = course_details_enrollment_end_date.strftime(
                                "%Y-%m-%d")
                        if course_details_enrollment_start_date != "":
                            course_details_enrollment_start_date = parser.parse(
                                course_details_enrollment_start_date)
                            course_details_enrollment_start_date = course_details_enrollment_start_date.strftime(
                                "%Y-%m-%d")
                        string_val = config.get("time_zones", "time_zones")
                        time_zone_result = ''
                        course_batch_type = ''
                        if string_val:
                            try:
                                time_zone = json.loads(
                                    str(string_val).replace(
                                        "'", '"').replace("'", '"')
                                )
                            except:
                                time_zone = ast.literal_eval(string_val)
                            for each in time_zone:
                                if (
                                    each.get("time_zone_offset",
                                             "").lower().strip()
                                    == data.get('course_details_time_zone', "").lower().strip()
                                ):
                                    time_zone_result = each
                        string_val = config.get("batch_type", "batch_type")
                        if string_val:
                            try:
                                time_zone = json.loads(
                                    str(string_val).replace(
                                        "'", '"').replace("'", '"')
                                )
                            except:
                                time_zone = ast.literal_eval(string_val)
                            for each in time_zone:
                                if (
                                    each.get("value", "").lower().strip()
                                    == data.get('course_batch_type', "").lower().strip()
                                ):
                                    course_batch_type = each
                        # result[key] = { "course_start_date": course_start_date, "course_end_date": course_end_date, "course_batch_size": data.get('course_batch_size',""), "batch_type": course_batch_type, "enrollment_start_date": course_details_enrollment_start_date, "enrollment_end_date": course_details_enrollment_end_date, "course_batch_timings": { "time_zone": time_zone_result, "start_time": data.get('course_details_start_time',""), "end_time": data.get('course_details_end_time',""), } }
                        result[key] = {"course_start_date": course_start_date, "course_end_date": course_end_date, "course_batch_size": data.get(
                            'course_batch_size', ""), "batch_type": course_batch_type, "enrollment_start_date": course_details_enrollment_start_date, "enrollment_end_date": course_details_enrollment_end_date, "course_batch_timings": {"time_zone": time_zone_result, "start_time": '00:00:00', "end_time": '00:30:00', }}
                        check = result[key]
                        sample = {"course_start_date": '', "course_end_date": '', "course_batch_size": '', "batch_type": '', "enrollment_start_date": '',
                                  "enrollment_end_date": '', "course_batch_timings": {"time_zone": '', "start_time": '00:00:00', "end_time": '00:30:00', }}
                        if check == sample or check == '' or check == None:
                            result[key] = {}
                    if key in ['additional_batches']:
                        additional_batch = natsorted(
                            [i for i in dict_keys if i.startswith(
                                "additional_batch")]
                        )
                        additional_batch_key = natsorted(
                            set([i.split("|")[1] for i in additional_batch])
                        )
                        additional_batch_data = []

                        def convert_time(date_extract):
                            if date_extract != "":
                                date_extract = parser.parse(date_extract)
                                date_extract = date_extract.strftime(
                                    "%Y-%m-%d")
                                return date_extract
                            else:
                                return ''
                        for range in additional_batch_key:
                            batch_size = data.get(
                                'additional_batch|'+range+'|batch_size', "")
                            batch_start_date = convert_time(
                                data.get('additional_batch|'+range+'|batch_start_date', ""))
                            batch_end_date = convert_time(
                                data.get('additional_batch|'+range+'|batch_end_date', ""))
                            batch_enrollment_start_date = convert_time(
                                data.get('additional_batch|'+range+'|batch_enrollment_start_date', ""))
                            batch_enrollment_end_date = convert_time(
                                data.get('additional_batch|'+range+'|batch_enrollment_end_date', ""))
                            total_duration = data.get(
                                'additional_batch|'+range+'|total_duration', "")
                            total_duration_unit = data.get(
                                'additional_batch|'+range+'|total_duration_unit', "")
                            pricing_type = data.get(
                                'additional_batch|'+range+'|pricing_type', "")
                            regular_price = data.get(
                                'additional_batch|'+range+'|regular_price', "")
                            sale_price = data.get(
                                'additional_batch|'+range+'|sale_price', "")
                            batch_type = data.get(
                                'additional_batch|'+range+'|batch_type', "")
                            batch_time_zone = data.get(
                                'additional_batch|'+range+'|batch_time_zone', "")
                            batch_start_time = data.get(
                                'additional_batch|'+range+'|batch_start_time', "")
                            batch_end_time = data.get(
                                'additional_batch|'+range+'|batch_end_time', "")
                            string_val = config.get("time_zones", "time_zones")
                            time_zone_result = ''
                            course_batch_type = ''
                            if string_val:
                                try:
                                    time_zone = json.loads(
                                        str(string_val).replace(
                                            "'", '"').replace("'", '"')
                                    )
                                except:
                                    time_zone = ast.literal_eval(string_val)
                                for each in time_zone:
                                    if (
                                        each.get("time_zone_offset",
                                                 "").lower().strip()
                                        == batch_time_zone.lower().strip()
                                    ):
                                        time_zone_result = each
                            string_val = config.get("batch_type", "batch_type")
                            if string_val:
                                try:
                                    time_zone = json.loads(
                                        str(string_val).replace(
                                            "'", '"').replace("'", '"')
                                    )
                                except:
                                    time_zone = ast.literal_eval(string_val)
                                for each in time_zone:
                                    if (
                                        each.get("value", "").lower().strip()
                                        == batch_type.lower().strip()
                                    ):
                                        course_batch_type = each

                            # additional_batch_data.append({ "batch_size": batch_size, "batch_start_date":batch_start_date, "batch_end_date": batch_end_date, "batch": str(range), "batch_enrollment_start_date": batch_enrollment_start_date, "batch_enrollment_end_date": batch_enrollment_end_date, "batch_type": course_batch_type, "total_duration": total_duration, "total_duration_unit": total_duration_unit, "pricing_type": pricing_type, "regular_price": "", "sale_price": sale_price, "batch_time_zone": time_zone_result, "batch_start_time": batch_start_time, "batch_end_time":batch_end_time, })
                            additional_batch_data.append({"batch_size": batch_size, "batch_start_date": batch_start_date, "batch_end_date": batch_end_date, "batch": 'Batch', "batch_enrollment_start_date": batch_enrollment_start_date, "batch_enrollment_end_date": batch_enrollment_end_date, "batch_type": course_batch_type,
                                                         "total_duration": total_duration, "total_duration_unit": total_duration_unit, "pricing_type": pricing_type, "regular_price": "", "sale_price": sale_price, "batch_time_zone": time_zone_result, "batch_start_time": '00:00:00', "batch_end_time": '00:30:00', })
                        result[key] = additional_batch_data

                        check = result[key]
                        check = list(unique_everseen(check))
                        sample = [{"batch_size": '', "batch_start_date": '', "batch_end_date": '', "batch": 'Batch', "batch_enrollment_start_date": '', "batch_enrollment_end_date": '', "batch_type": '',
                                   "total_duration": '', "total_duration_unit": '', "pricing_type": '', "regular_price": "", "sale_price": '', "batch_time_zone": '', "batch_start_time": '00:00:00', "batch_end_time": '00:30:00'}]
                        if check == sample or check == '' or check == None:
                            result[key] = []

                for key, values in json_template.items():
                    for key in [
                        "what_will_learn",
                        "target_students",
                        "prerequisites",
                        "skills_gained",
                    ]:
                        value = result.get(key, "")
                        if value == [{"option": ""}]:
                            result[key] = []

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_type, exc_tb.tb_lineno)
                with open("course_errorfile.txt", "a") as f:
                    f.write(
                        str(e)
                        + "\t"
                        + str(exc_type)
                        + "\t"
                        + str(exc_obj)
                        + "\t"
                        + str(exc_tb.tb_lineno)
                        + "\n"
                    )

            if result != "":
                payload = json.dumps(result)
                url = "https://backend.careervira.com/content-manager/explorer/application::learn-content.learn-content"
                headers = CaseInsensitiveDict()
                headers[
                    "User-Agent"
                ] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
                headers["Accept"] = "*/*"
                headers["Accept-Language"] = "en-US,en;q=0.5"
                headers["Authorization"] = f"Bearer {response['token']}"
                headers[
                    "Content-Type"
                ] = "multipart/form-data; boundary=---------------------------42476643092281311878507590330"
                headers["Origin"] = "https://backend.careervira.com"
                data = f'-----------------------------42476643092281311878507590330\r\nContent-Disposition: form-data; name="data"\r\n\r\n{payload}\r\n-----------------------------42476643092281311878507590330--\r\n'
                try:
                    final_response = requests.post(
                        url, headers=headers, data=data)
                    # print(final_response.text)
                    # pdb.set_trace()
                    if str(final_response.status_code) == "200":
                        print(
                            "<-----------------data pushed website successfully----------------->"
                        )
                    else:
                        with open("website_pushing_errorfile_course.txt", "a") as f:
                            f.write(str(final_response.text) + "\n")
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print("data pushing error", e, exc_type, exc_tb.tb_lineno)
                    with open("issues_errorfile_course.txt", "a") as f:
                        f.write(
                            str(e)
                            + "\t"
                            + str(exc_type)
                            + "\t"
                            + str(exc_obj)
                            + "\t"
                            + str(exc_tb.tb_lineno)
                            + "\n"
                        )
