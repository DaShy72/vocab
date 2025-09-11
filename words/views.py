from django.shortcuts import render, get_object_or_404, redirect
from .models import Word, LearnedWord, QuickCard, Dict
from django.db.models import Q
import random
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from difflib import get_close_matches
from django.db.models.functions import TruncDate
from django.db.models import Count

def parse_definitions(text):
    if text:
        results = []
        senses = text.split("||")
        for sense in senses:
            if "|" in sense:
                definition, examples_str = sense.split("|", 1)
                definition = definition.strip()
                examples = [ex.strip() for ex in examples_str.split(';') if ex.strip()]
                results.append({
                    "definition": definition,
                    "examples": examples
                })
        return results



def success_page(request, message, redirect_url):

    return render(request, "words/success2.html", {
        "message": message,
        "redirect_url": redirect_url
    })



def remove_card_success(request):
    return success_page(request, "Слово удалено из быстрых карточек.", "/cards/")



@login_required
def word_list(request):
    query = request.GET.get('q')
    words = Word.objects.all()

    if query:
        words = words.filter(
            Q(word__iexact=query) |
            Q(word__istartswith=query) |
            Q(part_of_speech__iexact=query) |
            Q(level__iexact=query)

        )

    paginator = Paginator(words, 48)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'words/word_list.html', {'page_obj': page_obj})

@login_required
def dictionary(request):
    query = request.GET.get('q')

    if query:
        dict = Dict.objects.filter(
            Q(word_eng__iexact=query) |
            Q(word_eng__istartswith=query) |
            Q(translation__iexact=query) |
            Q(translation__istartswith=query)
        )

        if not dict.exists():
            words = Dict.objects.values_list("word_eng", flat=True)
            matches = get_close_matches(query, words, n=5, cutoff=0.7)  # n=5 вариантов, похожесть 70%
            if matches:
                dict = Dict.objects.filter(word_eng__in=matches)

        return render(request, 'words/dictionary.html', {'dict': dict})


    return render(request, 'words/dictionary.html')

@login_required
def word_detail(request, pk):
    word = get_object_or_404(Word, pk=pk)
    definitions = parse_definitions(word.definition_examples)
    dict = Dict.objects.filter(word_eng=word.word, pos=word.part_of_speech).first()
    learned = LearnedWord.objects.filter(word=word.id, user=request.user).exists()
    quick = QuickCard.objects.filter(word=word.id, user=request.user).exists()


    if request.method == 'POST':
        if 'mark_learned' in request.POST:
            if not LearnedWord.objects.filter(word=word, user=request.user).exists():
                LearnedWord.objects.get_or_create(word=word, user=request.user)
            return success_page(request, "Words marks as learned", "/")

        if "send_to_quick_card" in request.POST:
            return redirect('words:fill_up_card', pk=pk)


    return render(request, 'words/word_detail.html', {
        'word': word,
        'definitions': definitions,
        'dict': dict,
        'learned': learned,
        'quick': quick,

    })

@login_required
def fill_up_card(request, pk):
    word = get_object_or_404(Word, pk=pk)

    if request.method == 'POST':
        if 'save_translation' in request.POST:
            translation = request.POST.get('translation')
            if not QuickCard.objects.filter(word=word, user=request.user).exists():
                if translation is not None:
                    QuickCard.objects.create(word=word, translation=translation, user=request.user)
        return success_page(request, "Words added in quick card", "/")
    return render(request, 'words/fill_up_card.html', context={'word': word})

@login_required
def random_word(request):
    words = list(Word.objects.all())
    if not words:
        return redirect('words:word_list')

    word = random.choice(words)
    return redirect('words:word_detail', pk=word.pk)

@login_required
def learned_list(request):
    if request.method == 'POST':
        learned_id = request.POST.get('unmark')
        if learned_id:
            LearnedWord.objects.filter(id=learned_id, user=request.user).delete()
            return redirect('words:learned_list')

    learned_words = LearnedWord.objects.select_related('word').filter(user=request.user).order_by('-learned_at')
    paginator = Paginator(learned_words, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = learned_words.count()
    return render(request, 'words/learned_list.html', {'page_obj': page_obj, 'count': count})


@login_required
def quick_card(request):
    cards = QuickCard.objects.select_related('word').filter(user=request.user)
    count = cards.count()

    if request.method == 'POST':
        all_cards = request.POST.get('all_cards')
        if all_cards:
            return redirect('words:quick_card')

        data = request.POST.get('unmark')
        card_id = 0
        word = 0
        if data:
            data = data.split(',')
            card_id = int(data[0])
            word = int(data[1])
        if card_id:
            QuickCard.objects.filter(id=card_id, user=request.user).delete()
            if not LearnedWord.objects.filter(word_id=word, user=request.user).exists():
                LearnedWord.objects.get_or_create(word_id=word, user=request.user)
            return redirect('words:quick_card')


    return render(request, 'words/quick_card.html', context={'quick_card': cards, 'count': count})


@login_required
def statistics(request):
    word_count = LearnedWord.objects.select_related('word').filter(user=request.user).count()
    noun = LearnedWord.objects.select_related('word').filter(user=request.user, word__part_of_speech='noun').count()
    verb = LearnedWord.objects.select_related('word').filter(user=request.user, word__part_of_speech='verb').count()
    adjective = LearnedWord.objects.select_related('word').filter(user=request.user, word__part_of_speech='adjective').count()
    adverb = LearnedWord.objects.select_related('word').filter(user=request.user, word__part_of_speech='adverb').count()
    pronoun = LearnedWord.objects.select_related('word').filter(user=request.user, word__part_of_speech='pronoun').count()
    other = word_count - (noun+verb+adverb+adjective+pronoun)

    stats = (
        LearnedWord.objects.filter(user=request.user)
        .annotate(date=TruncDate('learned_at'))
        .values('date')
        .annotate(total=Count('id'))
        .order_by('date')
    )
    dates = [item["date"].strftime("%Y-%m-%d") for item in stats]
    counts = [item["total"] for item in stats]

    return render(request, 'words/statistics.html', context={"word_count": word_count,
                                                                            'noun': noun,
                                                                            'verb': verb,
                                                                            'adjective': adjective,
                                                                            "adverb": adverb,
                                                                            'pronoun': pronoun,
                                                                            'other': other,
                                                             'dates': dates,
                                                             'counts': counts})
