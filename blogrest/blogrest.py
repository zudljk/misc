#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask, abort, request, make_response, jsonify, render_template, redirect, url_for
from os import open, path, remove, rmdir, mkdir
import markdown
from bleach import clean
import StringIO

app = Flask(__name__)

raw_base = '/home/ubuntu/workspace/blog'

NOT_IMPLEMENTED = '<html><head></head><body>Not implemented yet.</body></html>'

@app.route("/<page>/", methods=['DELETE'])
def deleteDir(page):
    try:
        rmdir(path.join(raw_base,page))
        return jsonResponse({'message': page+' deleted'})
    except OSError as e:
        return jsonResponse(e)

@app.route("/<page>/<subpage>", methods=['DELETE'])
def deleteFile(page, subpage):
    try:
        remove(path.join(raw_base,page,subpage+".md"))
        return jsonResponse({ 'message': path.join(page,subpage+".md")+" deleted."})
    except OSError as e:
        return jsonResponse(e)

@app.route("/<page>/", methods=['POST','PUT'])
def createDir(page):
    try:
        mkdir(raw_base+"/"+page)
        return jsonResponse({ 'message': page+" created."})
    except OSError as e:
        return jsonResponse(e)

@app.route("/<page>/<subpage>", methods=['POST','PUT'])
def createFile(page, subpage):
    try:
        file = request.files[subpage]
        if not file.filename.endsWith('.md') or (not request.headers['Content-Type'] and not request.headers['Content-Type'] == 'text/plain'):
            raise Exception('File type not allowed')
        file.save(path.join(raw_base,page,subpage+'.md'))
        return jsonResponse({'message':'File '+page+'/'+subpage+' created'})
    except Exception as e:
        return jsonResponse(e)

@app.route('/', methods=['GET'])
def init():
    return getDefaultHTMLPage()

@app.route('/<page>/', methods=['GET'])
def getPage(page):
    if request.headers['Accept'] == 'text/html':
        return getPageIndex(page)
    else:
        return getPageList(page)

@app.route('/<page>/<subpage>', methods=['GET'])
def getSubPage(page, subpage):
    try:
        if request.headers['Accept'] == 'text/html':
            return getHtmlPage(page, subpage)
        else:
            return redirect('/'+path.join('blog',page,subpage))
    except Exception as e:
        return jsonResponse(e)
        
def getDefaultHTMLPage(): 
    return NOT_IMPLEMENTED
    
def getHtmlPage(page, subpage):
    templatename = request.cookies.get('template') 
    if not templatename:
        templatename = 'default'
    stringio = StringIO.StringIO()
    markdown.markdownFromFile(input=path.join(raw_base,page,subpage+'.md'), output=stringio)
    return render_template(templatename+'.html', content=clean(stringio.getvalue()))

def getPageList(page): 
    return NOT_IMPLEMENTED

def getPageIndex(page): 
    return NOT_IMPLEMENTED

def jsonResponse(answer, code=200):
    if isinstance(answer, BaseException):
        code = 400
        if answer.errno == 2:
            code = 404
        return jsonResponse({'message': answer}, code)
    r = make_response(jsonify(**answer), code)
    r.headers['Content-type'] = 'application/json'
    return r

if __name__ == '__main__':
    app.run(debug=True)