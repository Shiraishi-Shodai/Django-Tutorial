from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
# 質問テーブル
class Question(models.Model):
    # question_textとpub_dateはデータベースの列名になる
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently ?",
    )
    
    def was_published_recently(self):
        '''
        投稿日(pub_date)が過去24時間以内であるかどうかを判定
        '''
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

# 投票テーブル
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 対応するQuestionのデータが削除されると、このデータも削除される
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.choice_text
