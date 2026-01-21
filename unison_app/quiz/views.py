import random
from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Song

def quiz_view(request):
    # 1. セッションから「未解答の曲IDリスト」を取得。なければ全曲IDを入れる
    unanswered_ids = request.session.get('unanswered_ids')
    
    if unanswered_ids is None:
        # 初回アクセス時：全曲のIDリストを作成してシャッフル
        unanswered_ids = list(Song.objects.values_list('id', flat=True))
        random.shuffle(unanswered_ids)
        request.session['unanswered_ids'] = unanswered_ids
        request.session['total_songs'] = len(unanswered_ids)
        request.session['current_count'] = 0

    # 2. 全問解き終わった場合の処理
    if not unanswered_ids:
        total = request.session.get('total_songs', 0)
        # 終わったらセッションをクリアして終了画面へ（またはリセット）
        request.session['unanswered_ids'] = None 
        return render(request, 'quiz/finished.html', {'total': total})

    # 3. リストの先頭から1曲取り出す（ポップ）
    current_song_id = unanswered_ids.pop(0)
    request.session['unanswered_ids'] = unanswered_ids # 更新して保存
    request.session['current_count'] += 1 # カウントアップ

    # 表示用のデータを取得
    question_song = get_object_or_404(Song, id=current_song_id)
    all_albums = Album.objects.prefetch_related('songs').all()

    return render(request, 'quiz/quiz.html', {
        'question_song': question_song,
        'all_albums': all_albums,
        'current_count': request.session['current_count'],
        'total_songs': request.session['total_songs'],
    })
def check_answer(request):
    if request.method == 'POST':
        user_choice_id = int(request.POST.get('song_id'))      # ユーザーが選んだ曲のID
        correct_song_id = int(request.POST.get('question_id')) # 正解の曲のID
        
        # 1. 正解だった場合
        if user_choice_id == correct_song_id:
            # 次の問題へリダイレクト（quizビューが呼ばれ、次の曲がセットされる）
            return redirect('quiz')
        
        # 2. 不正解だった場合
        else:
            # データの取得
            question_song = get_object_or_404(Song, id=correct_song_id)
            selected_song = get_object_or_404(Song, id=user_choice_id)
            
            # 結果画面を表示（is_correctは常にFalseになる）
            return render(request, 'quiz/result.html', {
                'is_correct': False,
                'question_song': question_song,
                'selected_song': selected_song,
            })
            
    return redirect('quiz')

def reset_quiz(request):
    # セッションのデータを消去して、クイズのトップページへ戻す
    request.session['unanswered_ids'] = None
    request.session['current_count'] = 0
    return redirect('quiz')