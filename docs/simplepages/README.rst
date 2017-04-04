spicy.core.simplepages 
**********************

Simplepages(в будущем - custompages) - шаблоны страниц, доступные в качестве шаблонов документов.
В админ.панели под это отводится раздел Страницы.
Здесь можно просмотреть существующие шаблоны в пункте "Все простые страницы" и создать новые (пункт"Создать простую страницу"), используя встроенный html редактор.


Структура каталога с шаблонами simplepages::

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

Для django-разработчика:

В случае, если в файлe settings.py явно не указано USE_DEFAULT_SIMPLE_PAGE_MODEL=False и не указано значение settings.SIMPLE_PAGE_MODEL, тогда за основную модель простой страницы берется simplepages.DefaultSimplePage.
Она повторяет код simplepages.AbstractSimplePage и наследует такое содержимое по умолчанию::

 {% extends current_base %}
 {% block content %}\n
 <!-- Page content here-->\n'
 {% endblock %}

Вероятно будет удобным в будущем вынести этот код из simplepages.abs.EditableTemplateModel
и выделить ему переменную в settings.py и в defaults.py
