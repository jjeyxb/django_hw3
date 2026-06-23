from rest_framework import serializers
from .models import MoodRecord

class MoodRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodRecord
        # 定義哪些欄位要開放給 API 讀取與寫入
        fields = ['id', 'user', 'created_at', 'mood', 'reason']
        
        # 為了維持 V2 的權限安全，user 欄位設定為唯讀，不可透過 API 竄改
        read_only_fields = ['user']