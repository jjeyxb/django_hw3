from django.db import models
from django.utils import timezone
# 1. 引入 Django 內建的使用者模型
from django.contrib.auth.models import User 

class MoodRecord(models.Model):
    MOOD_CHOICES = [
        ('happy', '開心 😄'),
        ('calm', '平靜 😐'),
        ('anxious', '焦慮 😰'),
        ('sad', '低落 😢'),
        ('angry', '生氣 😡'),
    ]

    # 2. 新增這行：將紀錄綁定到特定的 User。
    # on_delete=models.CASCADE 代表如果這個使用者被刪除，他所有的心情紀錄也會跟著被刪除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="使用者")
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name="紀錄時間")
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, verbose_name="今日心情")
    reason = models.TextField(blank=True, null=True, verbose_name="原因與備註")

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')} - {self.get_mood_display()}"