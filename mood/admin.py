from django.contrib import admin
from .models import MoodRecord

# 使用裝飾器註冊模型，並自訂後台顯示方式
@admin.register(MoodRecord)
class MoodRecordAdmin(admin.ModelAdmin):
    # 1. 自訂列表顯示欄位：在後台列表一眼看出這些資訊
    list_display = ('user', 'mood', 'created_at', 'reason')
    
    # 2. 新增過濾器：在後台右側增加側邊欄，可以依照「心情」或「時間」快速篩選
    list_filter = ('mood', 'created_at')
    
    # 3. 新增搜尋列：可以用「使用者帳號」或「備註原因」來搜尋特定紀錄
    search_fields = ('user__username', 'reason')
    
    # 4. 依照時間由新到舊排序
    ordering = ('-created_at',)