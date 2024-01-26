from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone


    
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {"latest_question_list" : latest_question_list}
    
#     return render(request, "polls/index.html", context)

# def detail(request, question_id):
#     '''
#     主キーがquestion_idに対応するQuestionデータを取り出す。対応するデータがなければ、404エラーを出す
#     '''
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('Question does not exist')
        
#     # ショートカットバージョン
#     question = get_object_or_404(Question, pk=question_id)
    
#     return render(request, 'polls/detail.html', {'question': question})
    

# def result(request, question_id):
    
#     question = get_object_or_404(Question, pk=question_id)
    # return render(request, "polls/results.html", {"question" : question})


# DetailViewは特定の1つのオブジェクトの詳細情報を表示する場合に使い
# ListViewはオブジェクトのリストを表示する場合（例えばブログの記事一覧など）に使う
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    #  ListView では、自動的に生成されるコンテキスト変数は question_list になります。これを上書きするには、 
    # context_object_name 属性を与え、 latest_question_list を代わりに使用すると指定します
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        # filter(pub_date__lte=timezone.now()): pub_dateが現在以下lte(less than or equal to（以下）のものを取得
        # order_by("-pub_date"): -pub_dateはpub_date列の降順で取得
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

# DetailView には question という変数が自動的に渡されます。
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_object(self):
        """URLで指定された質問が公開されている場合のみオブジェクトを返す。
        get_object は DetailView において特別な意味を持つメソッド名であり、
        この名前を使用することで Django はビューがリクエストを処理する際にこのメソッドを呼び出します。
        もし DetailView を使用している場合、このメソッドをオーバーライドすることでオブジェクトの取得方法をカスタマイズできます。
        """
        return get_object_or_404(Question, pk=self.kwargs.get('pk'), pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    
def vote(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                "question" : question,
                "error_message" : "You didn't select a choice"
            }
        )
        
    else:
        
        selected_choice.votes += 1
        selected_choice.save()
        
        # フォームデータの重複送信を防いだり、urlをGETに適した形にするためにリダイレクトを行う
        # reverse関数で絶対パスや特定のディレクトリ構造で直接コードに書くこと(ハードコード)を防ぐ
        # URL の名前 や ビューの関数 を URL に変換する関数
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))