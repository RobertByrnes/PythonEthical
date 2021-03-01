#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import urlparse


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "http://www.envirosample.online/login.manager.php"
response = request(target_url)
parsed_html = BeautifulSoup(response.content, features="lxml")
forms_list = parsed_html.findAll("form")

for form in forms_list:
    action = form.get("action")
    if action:
        post_url = urlparse.urljoin(target_url, action)
    else:
        post_url = target_url
    method = form.get("method")
    inputs_list = form.findAll("input")
    post_data = {}
    for input_tag in inputs_list:
        input_name = input_tag.get("name")
        input_type = input_tag.get("type")
        input_value = input_tag.get("value")
        if input_type == "text":
            input_value = 'test'
        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)
    print(result.content)
