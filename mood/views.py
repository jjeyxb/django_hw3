from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import MoodRecord
from .forms import MoodRecordForm
# --- 這裡加上處理會員系統需要的內建工具 ---
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import MoodRecordSerializer

# ==========================================
# 加上 @login_required(login_url='login') 裝飾器
# 意思是：如果沒登入，就自動幫我把使用者導向名字叫 'login' 的網址
# ==========================================

@login_required(login_url='login')
def index(request):
    # 🌟 關鍵修改：從 .all() 改成 .filter(user=request.user)
    # 這樣就「只會抓出目前登入者」的心情紀錄，完美實現資料隔離！
    records = MoodRecord.objects.filter(user=request.user).order_by('-created_at')
    context = {'records': records}
    return render(request, 'mood/index.html', context)

@login_required(login_url='login')
def add_mood(request):
    if request.method == 'POST':
        form = MoodRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            # 因為已經強制登入，所以可以直接把這筆紀錄綁定給當前使用者
            record.user = request.user 
            record.save()
            return redirect('index')
    else:
        form = MoodRecordForm()
    return render(request, 'mood/add_mood.html', {'form': form})

@login_required(login_url='login')
def delete_mood(request, pk):
    # 🌟 關鍵修改：加上 user=request.user 條件
    # 防止駭客知道別人紀錄的 ID，偷偷在網址輸入 /delete/5/ 把別人的資料刪掉
    record = get_object_or_404(MoodRecord, id=pk, user=request.user)
    record.delete()
    return redirect('index')

@login_required(login_url='login')
def statistics(request):
    labels = []
    data = []
    for code, name in MoodRecord.MOOD_CHOICES:
        # 🌟 關鍵修改：統計圖表也必須只計算「自己的」紀錄
        count = MoodRecord.objects.filter(mood=code, user=request.user).count()
        labels.append(name)
        data.append(count)
        
    context = {'labels': labels, 'data': data}
    return render(request, 'mood/statistics.html', context)

# --- 會員系統視圖 ---

# 1. 註冊功能
def register(request):
    if request.method == 'POST':
        # 使用 Django 內建的帳號建立表單
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # 將新使用者存入資料庫
            login(request, user) # 註冊成功後自動幫他登入
            return redirect('index') # 跳回首頁
    else:
        form = UserCreationForm()
    return render(request, 'mood/register.html', {'form': form})

# 2. 登入功能
def login_view(request):
    if request.method == 'POST':
        # AuthenticationForm 專門用來處理登入帳密驗證
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() # 取得通過驗證的使用者
            login(request, user) # 執行登入動作
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'mood/login.html', {'form': form})

# 3. 登出功能
def logout_view(request):
    logout(request) # 清除瀏覽器的登入記憶
    return redirect('login') # 登出後導向登入頁面

# ==========================================
# REST API 專區
# ==========================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) # 依然維持嚴格的權限控管，必須登入才能打 API
def mood_api(request):
    # 【方法 1】GET：取得所有紀錄
    if request.method == 'GET':
        # 只撈出目前登入者的資料，達成資料隔離
        records = MoodRecord.objects.filter(user=request.user).order_by('-created_at')
        # many=True 代表我們要翻譯的是「多筆」資料 (QuerySet)
        serializer = MoodRecordSerializer(records, many=True)
        return Response(serializer.data)

    # 【方法 2】POST：新增一筆紀錄
    elif request.method == 'POST':
        # 接收外部傳來的 JSON 資料
        serializer = MoodRecordSerializer(data=request.data)
        
        # 驗證資料是否合法 (例如有沒有填寫必填的心情欄位)
        if serializer.is_valid():
            # 儲存時，將這筆資料與當前發送請求的使用者綁定
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        # 如果資料不合法，回傳 400 錯誤與錯誤訊息
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)