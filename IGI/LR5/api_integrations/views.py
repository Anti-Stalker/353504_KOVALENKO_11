from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages

def api_dashboard(request):
    return render(request, 'api_integrations/dashboard.html')

def get_weather(request):
    city = request.GET.get('city', 'Minsk')
    api_key = settings.OPENWEATHERMAP_API_KEY
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            return JsonResponse({'success': True, 'data': weather_data})
        else:
            return JsonResponse({'success': False, 'error': 'Город не найден'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def search_books(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'success': False, 'error': 'Введите поисковый запрос'})
    
    url = f'http://openlibrary.org/search.json?title={query}&limit=5'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            books = []
            for book in data.get('docs', [])[:5]:
                book_data = {
                    'title': book.get('title', 'Название неизвестно'),
                    'author': book.get('author_name', ['Автор неизвестен'])[0] if book.get('author_name') else 'Автор неизвестен',
                    'first_publish_year': book.get('first_publish_year', 'Год неизвестен'),
                    'isbn': book.get('isbn', ['ISBN неизвестен'])[0] if book.get('isbn') else 'ISBN неизвестен',
                    'cover_id': book.get('cover_i', None)
                }
                books.append(book_data)
            return JsonResponse({'success': True, 'data': books})
        else:
            return JsonResponse({'success': False, 'error': 'Ошибка при поиске книг'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def api_integrations(request):
    context = {}
    
    # Get random dog image
    try:
        dog_response = requests.get('https://dog.ceo/api/breeds/image/random')
        if dog_response.status_code == 200:
            context['dog_image'] = dog_response.json()['message']
        else:
            messages.error(request, 'Не удалось получить изображение собаки')
    except Exception as e:
        messages.error(request, f'Ошибка при получении изображения собаки: {str(e)}')
    
    # Get random joke
    try:
        joke_response = requests.get('https://official-joke-api.appspot.com/random_joke')
        if joke_response.status_code == 200:
            joke_data = joke_response.json()
            context['joke'] = {
                'setup': joke_data['setup'],
                'punchline': joke_data['punchline']
            }
        else:
            messages.error(request, 'Не удалось получить шутку')
    except Exception as e:
        messages.error(request, f'Ошибка при получении шутки: {str(e)}')
    
    return render(request, 'api_integrations/api_page.html', context)

def refresh_dog(request):
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        if response.status_code == 200:
            return JsonResponse({'success': True, 'image_url': response.json()['message']})
        return JsonResponse({'success': False, 'error': 'Failed to fetch dog image'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def refresh_joke(request):
    try:
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        if response.status_code == 200:
            joke_data = response.json()
            return JsonResponse({
                'success': True,
                'setup': joke_data['setup'],
                'punchline': joke_data['punchline']
            })
        return JsonResponse({'success': False, 'error': 'Failed to fetch joke'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def api_page(request):
    context = {}
    
    # Get cat fact
    try:
        cat_response = requests.get('https://catfact.ninja/fact')
        if cat_response.status_code == 200:
            context['cat_fact'] = cat_response.json()['fact']
        else:
            messages.error(request, 'Не удалось получить факт о кошках')
    except Exception as e:
        messages.error(request, f'Ошибка при получении факта о кошках: {str(e)}')
    
    # Get nationality prediction for a default name
    try:
        name_response = requests.get('https://api.nationalize.io/?name=alex')
        if name_response.status_code == 200:
            data = name_response.json()
            if data['country']:
                context['nationality'] = {
                    'name': 'Alex',
                    'countries': [
                        {
                            'country_id': country['country_id'],
                            'probability': round(country['probability'] * 100, 2)
                        }
                        for country in data['country'][:3]  # Take top 3 countries
                    ]
                }
        else:
            messages.error(request, 'Не удалось получить предсказание национальности')
    except Exception as e:
        messages.error(request, f'Ошибка при получении предсказания национальности: {str(e)}')
    
    return render(request, 'api_integrations/api_page.html', context)

def get_new_cat_fact(request):
    try:
        response = requests.get('https://catfact.ninja/fact')
        if response.status_code == 200:
            return JsonResponse({
                'success': True,
                'fact': response.json()['fact']
            })
        return JsonResponse({
            'success': False,
            'error': 'Не удалось получить факт о кошках'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def predict_nationality(request):
    name = request.GET.get('name', 'alex')
    try:
        response = requests.get(f'https://api.nationalize.io/?name={name}')
        if response.status_code == 200:
            data = response.json()
            if data['country']:
                return JsonResponse({
                    'success': True,
                    'nationality': {
                        'name': name.capitalize(),
                        'countries': [
                            {
                                'country_id': country['country_id'],
                                'probability': round(country['probability'] * 100, 2)
                            }
                            for country in data['country'][:3]  # Take top 3 countries
                        ]
                    }
                })
        return JsonResponse({
            'success': False,
            'error': 'Не удалось определить национальность'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
