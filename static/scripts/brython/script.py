#!/bin/env python
# -*- coding: utf-8 -*-
from browser import window, alert,document
from browser import document as doc
from browser import ajax
locat = window.location
json = window.JSON
jq = window.jQuery
b64 = window.Base64
last_id = -1;
content_index = 0
selected_tag = ["-1"]
def get_complete(req):
  global last_id
  global content_index
  data = json.parse(str(req.text))
  print(len(data['item']))
  for i in range(0,len(data['item'])):
    add_html = "<li>"
    add_html += "<h2>" + data['item'][i].main_comment + "</h2>"
    add_html += "<p>" + data['item'][i].url + "</p>"
    add_html += "<p>" + data['item'][i].sub_comment + "</p>"
    add_html += "<p class = 'shikoiine' id = '"+str(data['item'][i].ID)+"'>shikoiine:" + str(data['item'][i].shikoiine) + "</p>"
    add_html += "<p class = 'naerune' id = '"+str(data['item'][i].ID)+"'>naerune:" + str(data['item'][i].naerune) + "</p>"
    add_html += "<p class = 'guilty' id = '"+str(data['item'][i].ID)+"'>guilty:" + str(data['item'][i].guilty) + "</p>"
    add_html += "<p>ID:" + str(data['item'][i].ID) + "</p>"
    last_id = data['item'][i].ID
    for tag_index in range(0,len(data['item'][i].tag)):
      add_html += "<p class='tag'>" + data['item'][i].tag[tag_index] + "</p>"
    add_html += "</li>"
    doc["contents_list"].html += add_html
#    jq(".shikoiine").on("click",post)
    jq(".tag").on("click",tag_select)
    
    content_index += 1

#    if req.status==200 or req.status==0:
#        doc["result"].html = req.text
#        print("aaaaa"+req.text)
#    else:
#        doc["result"].html = "error "+req.text
#        print(req.text)
  pass

def post_complete(req):
#  print(req.text)
  global last_id
  global content_index
  jq('#last').off('inview')
  doc.getElementById("close").click()
  content_index = 0
  last_id = -1
  doc["contents_list"].html = ""
  jq('#last').on('inview', callback)

def err_msg():
    doc["result"].html = "server didn't reply after %s seconds" %timeout

timeout = 4
def get(url,param={}):
    req = ajax.ajax()
    req.bind('complete',get_complete)
    req.set_timeout(timeout,err_msg)
    send_param = url
    for i in param.keys():
      if(isinstance(param[i],list)):
        for j in param[i]:
          send_param += i + "," + b64.encode(j) + ","
      else:
        send_param += i + "," + b64.encode(param[i]) + ","
    print("send_param="+send_param)
    req.open('GET',send_param,True)
    req.send()

def post(ev):
    url = "http://t0d0.jp:8889/api"
    req = ajax.ajax()
    req.bind('complete',post_complete)
    req.set_timeout(timeout,err_msg)

    req.open('POST',url,True)
    req.set_header('content-type','application/x-www-form-urlencoded')

    req.send({
      'main_comment':b64.encode(doc['main_comment'].value),
      'sub_comment':b64.encode(doc['sub_comment'].value),
      'url':b64.encode(doc['url'].value),
      'tag':b64.encode(doc['tag'].value)
    })
    doc['main_comment'].value = ""
    doc['sub_comment'].value = ""
    doc['url'].value = ""
    doc['tag'].value = ""
    print("ポストしたよ")
    return(0)
    
def list_reset():
  global last_id
  global content_index
  doc["contents_list"].html = ""
  jq('#last').off('inview')
  content_index = 0
  last_id = -1
  jq('#last').on('inview',callback)


def tag_select(ev):
  global selected_tag
  if selected_tag[0] == "-1":
    selected_tag = [ev.target.text]
  else:
    selected_tag.append(ev.target.text)
  list_reset()
  print(selected_tag)

def callback(event, isInView):
  global last_id
  global selected_tag
  if(isInView):
    print("見えた")
    get("http://t0d0.jp:8889/api/",{"id":last_id,"tag":selected_tag})#-1でnone指定

  else:
    print("消えた")

jq('#last').on('inview', callback)
jq('.shikotta-button').on('click',post)
