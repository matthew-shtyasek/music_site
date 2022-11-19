from django.contrib import messages


def parse(request, form):
    for error in form.errors.values():
        try:
            message = str(error).split('<li>', maxsplit=1)[1].split('</li>')[0]
            if message == 'Обязательное поле.':
                message = 'Не все поля заполнены'
            messages.add_message(request, messages.ERROR, message)
        except:
            pass

    for message in form.error_messages.values():
        messages.add_message(request, messages.ERROR, message)