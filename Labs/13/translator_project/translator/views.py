from django.shortcuts import render
from django.http import JsonResponse
from .models import Dictionary

def index(request):
    return render(request, 'translator/index.html')

def translate_word(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        english_word = request.POST.get('word', '').strip().lower()
        
        if not english_word:
            return JsonResponse({'error': 'Введите слово для перевода'})
        
        try:
            # Ищем слово в базе данных
            translation = Dictionary.objects.get(english_word=english_word)
            return JsonResponse({
                'success': True,
                'english_word': translation.english_word,
                'russian_translation': translation.russian_translation
            })
        except Dictionary.DoesNotExist:
            # Если слова нет в базе, используем простой словарь
            simple_dict = {
                'hello': 'привет',
                'world': 'мир',
                'cat': 'кот',
                'dog': 'собака',
                'house': 'дом',
                'book': 'книга',
                'computer': 'компьютер',
                'programming': 'программирование',
                'python': 'питон',
                'django': 'джанго',
                'translate': 'переводить',
                'word': 'слово',
                'language': 'язык',
                'english': 'английский',
                'russian': 'русский',
                'good': 'хороший',
                'bad': 'плохой',
                'big': 'большой',
                'small': 'маленький'
            }
            
            if english_word in simple_dict:
                return JsonResponse({
                    'success': True,
                    'english_word': english_word,
                    'russian_translation': simple_dict[english_word],
                    'from_simple_dict': True
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Слово "{english_word}" не найдено в словаре'
                })
    
    return JsonResponse({'error': 'Неверный запрос'})

def add_word(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        english_word = request.POST.get('english_word', '').strip().lower()
        russian_translation = request.POST.get('russian_translation', '').strip()
        
        if not english_word or not russian_translation:
            return JsonResponse({'error': 'Заполните все поля'})
        
        try:
            # Проверяем, существует ли уже такое слово
            Dictionary.objects.get(english_word=english_word)
            return JsonResponse({'error': 'Это слово уже есть в словаре'})
        except Dictionary.DoesNotExist:
            # Добавляем новое слово
            new_word = Dictionary.objects.create(
                english_word=english_word,
                russian_translation=russian_translation
            )
            return JsonResponse({
                'success': True,
                'message': f'Слово "{english_word}" добавлено в словарь'
            })
    
    return JsonResponse({'error': 'Неверный запрос'})