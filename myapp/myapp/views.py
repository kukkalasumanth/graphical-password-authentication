from django.http import HttpResponse
import pickle
import pyautogui as pag
from django.shortcuts import render, redirect
import random,math
import smtplib


def index(request):
   if request.method == "POST":
      if 'login' in request.POST:
         return redirect('login')

      elif 'register' in request.POST:
         return redirect('register')
      else:
         try:
            pickle_in = open("dict.pickle", "rb")
            users_dict = pickle.load(pickle_in)
            users_dict.clear()

            pickle_out = open("dict.pickle", "wb")
            pickle.dump(users_dict, pickle_out)
            pickle_out.close()

            pag.alert(text="All users data are reset now!", title="Alert!")
         except:
            pass

   return render(request=request,template_name='index.html')


def login(request):
   login_flag = False

   if request.method == "POST":
      username = request.POST.get("loginusername")
      password = request.POST.get("loginpassword")
      msg = ""
      try:
         pickle_in = open("dict.pickle", "rb")
         all_users_data = pickle.load(pickle_in)

         for i in all_users_data:
            if username == all_users_data[i].get("username"):
               passq=all_users_data[i].get("password")
               if password == all_users_data[i].get("password"):
                  msg = "login success"
                  login_flag = True
                  request.session["login_username"] = username
                  request.session["login_password"] = password
                  request.session["login_vibgyor_pattern"] = all_users_data[i].get("vibgyor_pattern")
                  request.session["login_listindex"] = all_users_data[i].get("listindex")
                  break
               else:
                  msg = "please check your pass"
            else:
               msg = "please create account first"

         if (login_flag):
            return redirect('login_level_2')
         elif 'forgot_password' in request.POST:
            if(passq==password):
               return redirect('login_level_2')
            return redirect('forgot_password')
         else:
            pag.alert(text=msg, title="Alert!")

      except:
         pass

   return render(request=request, template_name='login.html')
def forgot_password(request):
   digits = "0123456789"
   OTP = ""
   for i in range(6):
      OTP += digits[math.floor(random.random() * 10)]
   global username,listindex,vibgyor_pattern,password,email
   if request.method == "POST":
         if 'send' in request.POST:
            try:
               s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
               s.ehlo()
               s.starttls()
               username = request.session["login_username"]
               s.login("projectmail11912081@gmail.com", "pohgdwfmfsibcdox")
               pickle_in = open("dict.pickle", "rb")
               all_users_data = pickle.load(pickle_in)
               for i in all_users_data:
                  if username == all_users_data[i].get("username"):
                     email = all_users_data[i].get("email")
                     vibgyor_pattern = all_users_data[i].get("vibgyor_pattern")
                     listindex = all_users_data[i].get("listindex")
                     break
               global check
               check=OTP
               s.sendmail("sender_email", str(email), "OTP is " + str(OTP))
               msg = "OTP sent to " + str(email)
               pag.alert(text=msg, title="Send OTP via Email ")
               s.quit()
            except:
               msg = "Please enter the valid email address OR check an internet connection"
               pag.alert(text=msg, title="Send password via Email")
         otp=request.POST.get('otp')
         password = request.POST.get('password')
         password1 = request.POST.get('confirmpassword')
         if 'reset' in request.POST:

            if str(otp) != str(check):
               pag.alert(text="Check your OTP",title="Alert!")
               render(request,template_name='forgot_password.html')
            elif password != password1:
               pag.alert(text="Check your password",title="Alert!")
               return render(request, template_name='forgot_password.html')
            else:
               try:
                  pickle_in = open("dict.pickle", "rb")
                  all_users_data = pickle.load(pickle_in)
                  print(all_users_data)

                  all_users_data[username] = {"email": email, "username": username, "password": password,"vibgyor_pattern": vibgyor_pattern,"listindex": listindex}
                  pickle_out = open("dict.pickle", "wb")
                  pickle.dump(all_users_data, pickle_out)
                  pickle_out.close()

                  pickle_in = open("dict.pickle", "rb")
                  example_dict = pickle.load(pickle_in)
                  print(example_dict)
                  pag.alert(text="Password Reset Successfull",title="Success!")
                  return redirect('login')
               except:
                  pass


   return render(request=request,template_name='forgot_password.html')

def login_level_2(request):
   if request.method == "POST":
      if 'reset' not in request.POST:
         vibgyor_pattern = request.POST.get("my_field")

         login_vibgyor_pattern = request.session["login_vibgyor_pattern"]
         if len(vibgyor_pattern) > 0:
            if vibgyor_pattern == login_vibgyor_pattern:
               return redirect('login_level_3')

            else:
               pag.alert(text="please check your pattern", title="Alert!")
         elif 'forgot_password' in request.POST:
            if (vibgyor_pattern == login_vibgyor_pattern):
               return redirect('login_level_2')
            return redirect('forgot_password_1')

   return render(request=request, template_name='login_level_2.html')
def forgot_password_1(request):
   if request.method=="POST":
      username = request.session["login_username"]
      try:
         s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
         s.ehlo()
         s.starttls()

         s.login("projectmail11912081@gmail.com", "pohgdwfmfsibcdox")
         pickle_in = open("dict.pickle", "rb")
         all_users_data = pickle.load(pickle_in)
         for i in  all_users_data:
            if username==all_users_data[i].get("username"):
               email=all_users_data[i].get("email")
               vibgyor_pattern=all_users_data[i].get("vibgyor_pattern")
               break

         s.sendmail("sender_email",email,"Vigyor Pattern is "+str(vibgyor_pattern))
         msg="pattern sent to " + str(email)
         pag.alert(text=msg,title="Send pattern via Email ")
         return redirect('login_level_2')
         s.quit()

      except:
         msg="Please enter the valid email address OR check an internet connection"
         pag.alert(text=msg,title="Send pattern via Email")
   return render(request=request,template_name='forgot_password_1.html')

def login_level_3(request):
   if request.method == "POST":
      listindex = request.POST.get("listindex")
      login_listindex = request.session["login_listindex"]

      if login_listindex == listindex:
         pag.alert(text="login Successful", title="Alert!")
         return redirect('index')
      elif 'forgot_password' in request.POST:
         if (login_listindex==listindex):
            return redirect('index')
         return redirect('forgot_password_2')
      else:
         pag.alert(text="Please check image sequence!", title="Alert!")

   return render(request=request, template_name='login_level_3.html')

def forgot_password_2(request):
   if request.method=="POST":
      username = request.session["login_username"]
      try:
         s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
         s.ehlo()
         s.starttls()

         s.login("projectmail11912081@gmail.com", "pohgdwfmfsibcdox")
         pickle_in = open("dict.pickle", "rb")
         all_users_data = pickle.load(pickle_in)
         for i in  all_users_data:
            if username==all_users_data[i].get("username"):
               email=all_users_data[i].get("email")
               list_index=all_users_data[i].get("listindex")
               break
         s.sendmail("sender_email",email,"Index of images is "+str(list_index))
         msg="index sent to " + str(email)
         pag.alert(text=msg,title="Send index via Email ")
         return redirect('login_level_3')
         s.quit()

      except:
         msg="Please enter the valid email address OR check an internet connection"
         pag.alert(text=msg,title="Send index via Email")
   return render(request=request,template_name='forgot_password_1.html')

def register(request):
   if request.method == "POST":
      email = request.POST.get("email")
      username = request.POST.get("username")
      password = request.POST.get("password")
      password2 = request.POST.get("password2")
      request.session["email"]=email
      request.session["username"] = username
      request.session["password"] = password

      if password == password2:
         return redirect('register_level_2')
      else:
         pag.alert(text="Please check your password!", title="Alert!")
         return render(request=request, template_name='register.html')

   return render(request=request, template_name='register.html')


def register_level_2(request):
   if request.method == "POST":
      if 'reset' not in request.POST:
         vibgyor_pattern = request.POST.get("my_field")
         request.session["vibgyor_pattern"] = vibgyor_pattern

         if len(vibgyor_pattern) < 7 or len(vibgyor_pattern) == 0:
            pag.alert(text="Please Select Color Pattern from 7 given colors.", title="Alert!")

         if len(vibgyor_pattern) > 0 and len(vibgyor_pattern)==7:
                return redirect('register_level_3')


   return render(request=request, template_name='register_level_2.html')


def register_level_3(request):
   all_users_data = {}
   if request.method == "POST":
      listindex = request.POST.get("listindex")
      email=request.session["email"]
      username = request.session["username"]
      password = request.session["password"]
      vibgyor_pattern = request.session["vibgyor_pattern"]

      try:
         pickle_in = open("dict.pickle", "rb")
         all_users_data = pickle.load(pickle_in)
         print(all_users_data)
      except:
         pass

      print(username)
      print(password)
      print(vibgyor_pattern)

      all_users_data[username] = {"email":email,"username": username, "password": password, "vibgyor_pattern": vibgyor_pattern,
                                  "listindex": listindex}

      pickle_out = open("dict.pickle", "wb")
      pickle.dump(all_users_data, pickle_out)
      pickle_out.close()

      pickle_in = open("dict.pickle", "rb")
      example_dict = pickle.load(pickle_in)
      print(example_dict)

      pag.alert(text="Your Registration is successful.", title="Alert!")

      return redirect('index')

   return render(request=request, template_name='register_level_3.html')

