from django.shortcuts import render, \
    HttpResponseRedirect, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user, logout as logout_user \
    , authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import FormView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def logout(req):  # функция, отвечающая за выход пользователя из системы
    logout_user(req)  # встроенная функция
    return render(req, 'succeful.html', {'title': 'Exit'})  # перекидываем пользователя на страницу succeful.html


def login(req):  # функция входа пользователя в систему (код расписан максимально подробно)
    error = None

    if req.method == 'POST':  # Если пользователь захотел войти, то
        username = req.POST['username']  # Вытаскиваем его имя и пароль
        password = req.POST['password']
        user = authenticate(username=username, password=password)  # проверяем, существует ли такой пользователь в базе
        if user is not None:  # если существует, то
            if user.is_active:  # проверяем, активирована ли учетная запись
                login_user(req, user)
                return render(req, 'succeful.html', {'title': 'Login'})
            else:  # если учетка не активирована, то выводим сообщение об ошибке
                error = 'Please check the entered data. ' \
                        'No such account exists. ' \
                        'If you do not have an account, create one.'
        else:  # если пользователя не сущестует, так же выводим сообщение об ошибке
            error = 'Please enter the correct username and password for ' \
                    'a staff account. Note that both fields may ' \
                    'be case-sensitive.'

    form = AuthenticationForm()  # форма, для дизайна

    return render(req, 'log.html', {'form': form,
                                    'error': error})


class Login(FormView):  # класс для входа пользователя в систему
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'log.html'

    def form_valid(self, form):  # проверка валидности формы
        self.user = form.get_user()  # получаем пользователя
        login(self.request)  # пользуемся функцией, функционал которой описан выше
        return super(Login, self).form_valid(
            form)  # переопределяем функцию from_valid, которая отвечает за валидность введенных данных


def registration(req):  # функция регистрации пользователя
    if req.method == 'POST':  # если пользователь хочет зарегаться, то
        form = UserCreationForm(req.POST)  # передаем введенные пользователем данные в форму
        if form.is_valid():  # если данные корректны, то
            user = form.save()  # сохраняем пользователя
            login_user(req, user)  # входим в систему под его именем
            return render(req, 'succeful.html', {'title': 'create account'})
    else:
        form = UserCreationForm()  # Иначе затираем все поля в форме и просим зарегестрироваться заново

    return render(req, 'reg.html', {'form': form})


def deleteaccount(req):  # функция удаления аккаунта пользователя
    user_id = req.user.id  # получаем аккаунт юзера
    if User.objects.filter(id=user_id).exists():  # проверяем, сущестует ли удаляемый пользователь
        account = User.objects.get(id=user_id)  # получаем пользователя из базы данных
        account.delete()  # удаляем пользователя из базы данных
    return render(req, 'main.html', {'title': 'delete account'})  # перекидываем на главную страницу


def edit_post(req, id):  # функция редактирования поста
    if Post.objects.filter(id=id).exists():  # проверяем на существование поста в базе данных
        post = Post.objects.get(id=id)  # если пост существует, то вытаскиваем его из базы данных
        if req.method == 'POST':  # если пользователь хочет отредактировать пост, то получаем данные, которые он
            # отправил на сервер

            post.title = req.POST['title']  # вытаскиваем заголовок поста
            post.text = req.POST['text']  # вытаскиваем текст
            post.save()  # сохраняем пост
            return redirect(f'/post/{id}/')  # перенаправляем пользователя на страницу с постом
        else:

            return render(req, 'createpost.html', {'post': post})  # если пользователь не стал создавать пост,
            # то ничего не делаем
    return render(req, 'createpost.html')


def detail_post(req, id):  # детальный просмотр поста
    if Post.objects.filter(id=id).exists():  # если пост существует, то
        post = Post.objects.get(id=id)  # получаем пост

        post.views += 1  # добавляем количество просмотров к посту
        post.save()  # обновляем данные о посте

        return render(req, 'detail.html', {'post': post
                                           })  # перенаправляем на страницу для просмотра поста
    else:

        return render(req, 'detail.html', {})  # если поста не существует, то перенаправляем на страницу для
        # просмотра поста, не передавая данные о посте(выведется пустая страница, с информацией о том, что такого
        # поста не существует)


# Create your views here.
def main(req):  # главная функция
    posts = Post.objects.all()  # получаем все посты
    paginator = Paginator(posts, 3)  # пагинации на странице
    page = req.GET.get('page')  # страница

    try:  # если все работает без ошибок, то
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)

    return render(req, 'main.html', {'posts': posts,
                                     'page': page})


def search_result(req):  # функция поиска
    query = req.GET.get('q')  # получаем данные запроса поиска
    title_search = Post.objects.filter(title__contains=query)  # поиск по заголовку
    text_search = Post.objects.filter(text__contains=query)  # поиск по тексту
    return render(req, 'search-result.html', {'title_search': title_search,
                                              'text_search': text_search,
                                              'search': query})  # передаем результаты поиска на страницу


def create_post(req):  # функция создания поста
    if req.method == 'POST':  # если пользователь хочет создать пост
        post = Post()  # создаем пустую модель поста
        post.title = req.POST['title']  # добавляем заголовок
        post.text = req.POST['text']  # текст
        post.owner = req.user  # привязываем пользователя
        post.views = 0  # обнуляем количетсво просмотром
        post.save()  # сохраняем пост

        return redirect(f'/post/{post.id}/')  # перенаправляем на адрес детального просмотра поста

    return render(req, 'createpost.html')


def detail_user(req, id):  # детальный просмотр пользователя
    if User.objects.filter(id=id).exists():  # если пользователь существует, то
        user = User.objects.get(id=id)  # получаем пользователя
        posts = Post.objects.filter(owner_id=id)  # получаем все его посты
        return render(req, 'detail-user.html', {'current_user': user,
                                                'posts': posts})  # передаем информацию на страницу(пользователю)
    else:
        return render(req, 'main.html')


def deletepost(req, id):  # удаление постов
    try:  # если все окей,То
        post = Post.objects.get(id=id)  # получаем пост
        post.delete()  # удаляем пост
        return render(req, 'succeful.html', {'title': 'delete'})  # передаем информанцию на страницу(пользователю)
    except:  # если не окей, то ничего не делаем
        pass
