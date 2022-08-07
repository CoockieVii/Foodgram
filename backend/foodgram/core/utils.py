from django.http.response import HttpResponse


def download(ingredients):
    lines = ['  Ингредиенты: ']
    for ingredient in ingredients:
        name = ingredient['ingredients__name']
        measurement_unit = ingredient['ingredients__measurement_unit']
        amount = ingredient['ingredient_total']
        lines.append(f'{name} ({measurement_unit}) - {amount}')
    content = '\n'.join(lines)
    content_type = 'text/plain,charset=utf8'
    response = HttpResponse(content, content_type=content_type)
    response[
        'Content-Disposition'] = f'attachment; filename=shopping_list.txt'
    return response
