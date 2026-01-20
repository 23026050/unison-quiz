from django.shortcuts import render
from .models import Question
import random

def quiz_view(request):
    # 登録された全問題を取得
    all_questions = list(Question.objects.all())
    
    # まだデータがない場合の処理
    if not all_questions:
        return render(request, 'quiz/index.html', {'error': '問題が登録されていません。'})

    # ランダムに1問選ぶ
    question = random.choice(all_questions)
    
    # 正解とダミーを混ぜてシャッフル
    choices = [question.title, question.dummy_choice1, question.dummy_choice2]
    random.shuffle(choices)

    return render(request, 'quiz/index.html', {
        'question': question,
        'choices': choices,
    })