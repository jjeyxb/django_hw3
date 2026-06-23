from django import forms
from django.utils import timezone
from .models import MoodRecord

class MoodRecordForm(forms.ModelForm):
    class Meta:
        model = MoodRecord
        # 這裡不包含 'user'，因為使用者應該由系統自動綁定，不能讓人在網頁上自己選
        fields = ['created_at', 'mood', 'reason']
        
        # 幫欄位加上 Bootstrap 的 CSS class，讓表單保持美觀
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '今天發生了什麼事呢？'}),
        }

    # 自訂驗證邏輯 1：確保時間不能是未來的時間
    def clean_created_at(self):
        created_at = self.cleaned_data.get('created_at')
        if created_at and created_at > timezone.now():
            # 如果發現是未來時間，就拋出驗證錯誤
            raise forms.ValidationError("時光旅人你好！但紀錄時間不能設定為未來的時間喔！")
        return created_at

    # 自訂驗證邏輯 2：如果心情是生氣，強制要求填寫原因
    def clean(self):
        # 呼叫父類別的 clean 方法取得所有已驗證的資料
        cleaned_data = super().clean()
        mood = cleaned_data.get('mood')
        reason = cleaned_data.get('reason')
        
        if mood == 'angry' and not reason:
            # 針對特定的欄位 (reason) 加入錯誤提示
            self.add_error('reason', "既然生氣了，就把原因寫下來發洩一下吧！(此心情必填原因)")
            
        return cleaned_data