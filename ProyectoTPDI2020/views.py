from django.http import HttpResponse
import datetime
import pymongo
from django.template import Template, Context
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def makeConnection():
    connection = pymongo.MongoClient('mongodb://localhost:27017/', connect=False, maxPoolSize=None)
    db = connection.clinicadm
    return db

def ingreso(request, ingresovalido = "True"):
    doc = loader.get_template("ingreso.html")

    ctx = {
        'ingresovalido' : ingresovalido
    }

    doc = doc.render(ctx) 

    return HttpResponse(doc)

def edit(request,tablename,tableid,makeedit = None):
    query = makeConnection()[tablename].find_one({'Id': str(tableid)},projection={'_id' : 0})
    query = dict(query)
    if makeedit == None:
        ctx = {
            "query" : query,
            "tablename" : tablename,
            "tableid" : tableid,
            "makeedit" : makeedit
        }

        doc = loader.get_template("edit.html")

        doc = doc.render(ctx)

        response = HttpResponse(doc)
    else:
        payload = {
            "$set":{}
        }
        for item in request.POST:
            payload['$set'][item] = request.POST[item]

        result = makeConnection()[tablename].update_one({'Id': str(tableid)},payload)

        response = redirect('/table/'+tablename+'/editSuccess=True')

    return response

def add(request,tablename,makeadd = None):
    query = makeConnection()[tablename].find_one({},projection={'_id' : 0})
    query = dict(query)

    if makeadd == None:
        ctx = {
            "query" : query,
            "tablename" : tablename,
            "makeadd" : makeadd
        }

        doc = loader.get_template("add.html")

        doc = doc.render(ctx)

        response = HttpResponse(doc)
    else:
        payload = {}
        for item in request.POST:
            payload[item] = request.POST[item]

        result = makeConnection()[tablename].insert_one(payload)

        response = redirect('/table/'+tablename+'/addSuccess=True')

    return response


def delete(request,tablename,tableid):
    query = makeConnection()[tablename].delete_one({'Id': str(tableid)})

    if query.deleted_count > 0:
        response = redirect('/table/'+tablename+'/deleteSuccess=True')
    else:
        response = redirect('/table/'+tablename+'/deleteSuccess=False')
    
    return response

def table(request, tablename, edited = None, deleted = None, added = None):
    doc = loader.get_template("table.html")

    listDB = makeConnection()[tablename].find({},projection={'_id':0})
    listDB = list(listDB)

    ctx = {
        "listDB" : listDB,
        "fieldCount" : len(listDB) + 2,
        "deleted" : deleted,
        "edited" : edited,
        "added" : added,
        "tablename" : tablename
    }

    doc = doc.render(ctx) 

    return HttpResponse(doc)

def controlLogin(request):
    nombreUsuario = request.POST['nombre']
    contra = request.POST['contra']

    listDB = makeConnection()['usuarios'].find_one({'NombreUsuario' : nombreUsuario}, projection={'_id': 0, 'NombreUsuario': 1, 'Contraseña': 1})

    if listDB:
        if listDB['Contraseña'] != contra:
            response = redirect('/ingreso/loginSuccess=False')
        else:
            response = redirect('/controlpanelAdmin')
    else:
        response = redirect('/ingreso/loginSuccess=False')

    return response

def controlpanelAdmin(request):
    doc = loader.get_template('controlpaneladmin.html')
    doc = doc.render({})
    return HttpResponse(doc)

