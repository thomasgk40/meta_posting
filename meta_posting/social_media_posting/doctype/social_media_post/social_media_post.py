# Copyright (c) 2024, Printechs and contributors
# For license information, please see license.txt

# import frappe
import frappe
import requests
import json
from urllib.request import urlopen
from frappe.model.document import Document


class SocialMediaPost(Document):
	pass


@frappe.whitelist()
def post_to_social_media(docname):
    #docname="1"
    doc = frappe.get_doc("Social Media Post", docname)
    print(doc.name)
    print(doc.platform)
    print(frappe.utils.get_url())
    imagep=None
    videop=None
    if doc.image:
        imagep=f"http://192.168.1.244{doc.image}"
    if doc.video:
        videop=f"/home/erpnext/frappe-bench/sites/site1.local/public{doc.video}"
    try:
        if doc.platform == "Facebook":
            response = post_to_facebook(doc.facebook_page,doc.content, imagep, videop)
        elif doc.platform == "Instagram":
            response = post_to_instagram(doc.content, doc.image, doc.video)
        else:
            frappe.throw("Platform not supported.")
        
        # Update Status and Response
        doc.reload()
        doc.status = "Posted"
        doc.response_message = json.dumps(response)
        doc.save(ignore_permissions=True)
        
        return {"message": "Post Successful", "response": response}

    except Exception as e:
        doc.status = "Failed"
        doc.response_message = str(e)
        doc.save()
        frappe.log_error(f"Failed to post: {str(e)}")
        return {"message": "Post Failed", "error": str(e)}

def post_to_facebook(facebook_page,content, image=None, video=None):
    doc = frappe.get_doc("Facebook Page", facebook_page)
    ACCESS_TOKEN = doc.access_token #"EAAGkMrffZC7EBOxDcxEvegUkxW2LZBzZA1AHs2dZB96nmoEZBQ0Agui9zuiqWKlM3gbRZAqHvxZA42Qyev2yqmhGmHQH4kklFyvJDY0yGZATdclOfJLXn1gJD71nIVMAK9pzXV0A9ixbJS0tiSZBpsw3Sen8fpMpqYMXRZBgVE4oYgKUeZBnVcl0qrw3ZCbRrT1TzZCOZB1gXlulngJOe0j7ithHZAPuMgZD"
    PAGE_ID = doc.page_id
    print(PAGE_ID)
    print(image)
    print(video)
    url = f"https://graph.facebook.com/v12.0/{PAGE_ID}/feed"
    payload = {"message": content, "access_token": ACCESS_TOKEN}
    
    if image:
        url = f"https://graph.facebook.com/v12.0/{PAGE_ID}/photos"
        files = {'source': urlopen(image).read()}
        response = requests.post(url, data=payload, files=files)
    elif video:
        url = f"https://graph.facebook.com/v12.0/{PAGE_ID}/videos"
        with open(video, 'rb') as video_file: 
            files = { 'source': video_file }
            #files = {'fbuploader_video_file_chunk': video}
            payload = {"title": content, "access_token": ACCESS_TOKEN,"description":"TEST"}
        
            response = requests.post(url, data=payload, files=files)
    else:
        response = requests.post(url, data=payload)
    print(response.json())
    return response.json()

def post_to_instagram(content, image=None, video=None):
    # Add Instagram API logic here (similar to Facebook)
    return "Instagram posting logic here."