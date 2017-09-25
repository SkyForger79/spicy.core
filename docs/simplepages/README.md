# spicy.core.simplepages 


## Назначение

Модуль предоставляет способ добавления, удаления, редактирования станиц сайта через админку, без модификации html-кода 
напрямую. При совместном использовании с [другими модулями Spicy](https://github.com/spicycms), позволяет настраивать динамичные страницы сайта, такие как списки новостей, статей, каталоги, настраивать на них пажинацию, фильтрацию.

В админке под этот модуль отводится раздел Страницы. Здесь можно просмотреть существующие шаблоны в пункте "Все простые страницы" и создать новые (пункт "Создать простую страницу"), используя встроенный html редактор.

## Для редактора сайта
Модули Spicy, такие как spicy.categories, spicy.feedback, spicy.document, имеют шаблонные теги, которые вы можете использовать в страницах для построения динамического контента.

### Пример шаблон для отображения списка новостей по категории
1) Создайте категорию ``Новости``, со слагом ``news``
2) Отредактируйте несколько документов, чтобы они имели категорию ``Новости``
3) Создайте простую страницу и добавьте в самый верх строчку: ``{% load categories %}``
4) В теле этой страницы, где вы хотите расположить блок новостей, добавьте:

```
{% category "news" "webapp" "document" 4 as dc %}
    New - {{ dc.title }}, date of publication - {{ dc.pub_date }}. <a href="{{ dc.get_absolute_url }}">Learn more...</a>
{% endcategory %}
```
Такой код выведет 4 документа с категорией ``Новости`` (``"news"``), между тегами {% category %} и {% endcategory %} в цикле будут прокручены эти документы, и доступны по имени ``dc``.

### Пример фильтрации документов
Выполните шаги 1-3 из [предыдущего примера](./README.md#Пример-шаблон-для-отображения-списка-новостей-по-категории), а затем разместите в коде вашей страницы:
```
{% category "news" "webapp" "document" 4 as dc where owner=request.user %}
    New - {{ dc.title }}, date of publication - {{ dc.pub_date }}. <a href="{{ dc.get_absolute_url }}">Learn more...</a>
{% endcategory %}
```
Этот код, как и предыдущий выведет 4 новости по категории ``Новости``, но дополнительно отфильтрует их по автору - ``owner``, равному текущему пользователю.

## Структура каталога с шаблонами simplepages:

	simplepages/templates/
	└── spicy.core.simplepages
	    ├── admin
	    │   ├── ... admin templates
	    ├── default.html
	    └── simplepages
	        ├── errors.403.html
	        ├── errors.404.html
	        └── errors.500.html
	   		└── Дополнительные шаблоны, которые могут быть шаблонами документов     

## Для Django-разработчика:

### Добавление модуля в проект
Используя сборку SpicyCMS, для подключения spicy.core.simplepages достаточно добавить его в settings.py:

    INSTALLED_APPS = [
    	...
    	'spicy.core.simplepages',
    ]

Теперь в админпанели появится пункт Страницы, где вы сможете управлять простыми страницами сайта. 

При добавлении новых страниц через файловую систему (а не через админку), нужно выполнять обновление простых страниц, чтобы SpicyCMS увидела новые файлы в директории simplepages (при этом происходит рестарт проекта).

### Кастомизация модели простой страницы
По умолчанию за основную модель простой страницы берется simplepages.DefaultSimplePage.
Она повторяет код simplepages.AbstractSimplePage и наследует такое содержимое по умолчанию::

```
 {% extends current_base %}
 {% block content %}\n
 <!-- Page content here-->\n'
 {% endblock %}
```

Вы можете реализовать свою модель для простой страницы, для этого, создайте свою модель, унаследовав ее от ``simplepages.AbstractSimplePage``, при этом важно указать ``Meta.abstract = False``:

	# yourapp.models.py
	from spicy.core.simplepages.abs import AbstractSimplePage
	
	class CustomSimplePage(AbstractSimplePage):
		# your code here
		
		class Meta:
			abstract = False
			
Также укажите в settings.py настройку, чтобы SpicyCMS использовала вашу модель в качестве простой страницы:

	# yourapp.settings.py
	USE_DEFAULT_SIMPLE_PAGE_MODEL = False
	SIMPLE_PAGE_MODEL = 'yourapp.models.CustomSimplePage
	
Теперь выполните ``manage.py syncdb``, чтобы Django создала таблицу для ваших простых страниц в базе данных.
