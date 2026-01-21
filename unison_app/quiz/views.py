import random
from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Song

def quiz_view(request):
    unanswered_ids = request.session.get('unanswered_ids')
    
    if unanswered_ids is None:
        unanswered_ids = list(Song.objects.values_list('id', flat=True))
        random.shuffle(unanswered_ids)
        request.session['unanswered_ids'] = unanswered_ids
        request.session['total_songs'] = len(unanswered_ids)
        request.session['current_count'] = 0
        # 正解数を初期化
        request.session['correct_answer_count'] = 0

    if not unanswered_ids:
        total = request.session.get('total_songs', 0)
        # セッションから正解数を取得
        correct_count = request.session.get('correct_answer_count', 0)
        request.session['unanswered_ids'] = None 
        # 終了画面に正解数を渡す
        return render(request, 'quiz/finished.html', {
            'total': total,
            'correct_count': correct_count
        })

    # (以下、既存の処理と同じ)
    current_song_id = unanswered_ids.pop(0)
    request.session['unanswered_ids'] = unanswered_ids
    request.session['current_count'] += 1

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
        user_choice_id = int(request.POST.get('song_id'))
        correct_song_id = int(request.POST.get('question_id'))
        
        if user_choice_id == correct_song_id:
            # 正解の場合、セッションの正解数を +1 する
            request.session['correct_answer_count'] = request.session.get('correct_answer_count', 0) + 1
            return redirect('quiz')
        else:
            # 不正解の場合（既存の処理）
            question_song = get_object_or_404(Song, id=correct_song_id)
            selected_song = get_object_or_404(Song, id=user_choice_id)
            return render(request, 'quiz/result.html', {
                'is_correct': False,
                'question_song': question_song,
                'selected_song': selected_song,
            })
    return redirect('quiz')

def reset_quiz(request):
    request.session['unanswered_ids'] = None
    request.session['current_count'] = 0
    request.session['correct_answer_count'] = 0 # リセット時も初期化
    return redirect('quiz')