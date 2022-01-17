from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
import hashlib
from http import cookies


session = {}

class Registration(APIView):
    def post(self, request):
        # функции авторизации

        login = request.data.get('login')
        password = request.data.get('password')
        print(login)
        print(password)

        hash_log = hashlib.sha512(login.encode())
        hex_log = hash_log.hexdigest()
        print(hex_log)

        hash_pass = hashlib.sha512(password.encode())
        hex_pass = hash_pass.hexdigest()
        print(hex_pass)



        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO reg(login, password) VALUES (%s, %s)', [str(hex_log), str(hex_pass)])
            #raw = cursor.fetchone()
            #print(type(raw))

        resp = {'status': 'ok'}
        return JsonResponse(resp)


class Authorization(APIView):
    def post(self, request):
        #функция автроизации
        login = request.data.get('login')
        password = request.data.get('password')

        hash_log = hashlib.sha512(login.encode())
        hex_log = hash_log.hexdigest()
        print(hex_log)

        hash_pass = hashlib.sha512(password.encode())
        hex_pass = hash_pass.hexdigest()
        print(hex_pass)


        with connection.cursor() as cursor:
            cursor.execute('SELECT id, login, password FROM reg Where login = (%s) and password = (%s);', [str(hex_log), str(hex_pass)])
            raw = cursor.fetchone()
            print(raw)

        if raw != None:
            id = raw[0]

            hash_id = hashlib.sha512(str(id).encode())
            hex_id = hash_id.hexdigest()
            #session = {str(hex_id) : str(id)}
            session[str(hex_id)] = str(id)
            print(session)


            resp = HttpResponse('Авторизация прошла успешно')
            # время действия куки 2ч
            resp.set_cookie('cookie', str(hex_id), max_age=60*5)

            return resp

        else:
            resp = HttpResponse('Не верно введены логин или пароль')
            return resp


class TestSession(APIView):
    def get(self, request):

        if 'cookie' in request.COOKIES:
            if  session[str(request.COOKIES['cookie'])] :
                print('такая сессия есть!')
                value = request.COOKIES['cookie']
                print(value)
                response = HttpResponse('Отображаем нужную информацию')
                return response
        else:
            response = HttpResponse('Вы не авторизованы')
            return response







