from functools import wraps
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger('api')

def api_auth_required(view_func):
    """
    Декоратор для проверки аутентификации пользователя при доступе к API.
    Также проверяет наличие API-ключа в заголовках запроса.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Проверяем аутентификацию
        if not request.user.is_authenticated:
            logger.warning(f'Попытка неавторизованного доступа к API: {request.path}')
            return JsonResponse({
                'error': 'Unauthorized',
                'message': 'Для доступа к API необходима аутентификация'
            }, status=401)

        # Проверяем API-ключ
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            logger.warning(f'Попытка доступа к API без ключа: {request.user.username}')
            return JsonResponse({
                'error': 'Forbidden',
                'message': 'Отсутствует API-ключ в заголовках запроса'
            }, status=403)

        # Проверяем rate limiting
        if hasattr(request.user, 'api_requests_count'):
            if request.user.api_requests_count > 1000:  # Лимит запросов в день
                logger.error(f'Превышен лимит API запросов: {request.user.username}')
                return JsonResponse({
                    'error': 'Too Many Requests',
                    'message': 'Превышен дневной лимит запросов к API'
                }, status=429)

        try:
            response = view_func(request, *args, **kwargs)
            logger.info(f'Успешный API запрос: {request.user.username} - {request.path}')
            return response
        except PermissionDenied as e:
            logger.error(f'Отказано в доступе к API: {request.user.username} - {str(e)}')
            return JsonResponse({
                'error': 'Forbidden',
                'message': str(e)
            }, status=403)
        except Exception as e:
            logger.error(f'Ошибка API: {request.user.username} - {str(e)}')
            return JsonResponse({
                'error': 'Internal Server Error',
                'message': 'Внутренняя ошибка сервера'
            }, status=500)

    return wrapper 