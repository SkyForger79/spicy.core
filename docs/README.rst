.. spicy.core documentation master file, created by
   sphinx-quickstart on Sat Feb 25 16:19:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Документация spicy.core
***********************
spicy.core представляет из себя набор базовых модулей для организации веб-приложения по сервис-ориентированной архитектуре. Такой подход позволяет решить `ряд проблем <../README.md>`_, возникающих перед разработчиками Django-приложений. 

Проект SpicyCMS, включает в себя spicy.core с его подмодулями, а также может включать дополнительные модули, которые позволят расширить функциональность CMS.   

Подмодули spicy.core
====================
Каждый подмодуль решает типовые задачи, связанные с конкретной частью приложения. 

* `spicy.core.admin <admin/README.rst>`_  - администрирование приложения, управление подключаемыми модулями SpicyCMS

* `spicy.core.profile <profile/README.rst>`_ - управление пользователями, ограничение прав доступа, интеграция с социальными сетями

* `spicy.core.rmanager <rmanager/README.rst>`_ - {TODO краткое назначение}

* `spicy.core.service <service/README.rst>`_ - {TODO краткое назначение}

* `spicy.core.simplepages <simplepages/README.rst>`_ - управление простыми страницами сайта

* `spicy.core.siteskin <siteskin/README.rst>`_ - управление темами сайта

* `spicy.core.trash <trash/README.rst>`_ - хранение истории изменений объектов на сайте

Пример сборки приложения
========================
Вы можете посмотреть `пример приложения <https://gitlab.com/spicycms.com/dev-SpicyCMS_Chief_Editor>`_, основанного на модулях SpicyCMS - `CMS Chief Editor <https://gitlab.com/spicycms.com/dev-SpicyCMS_Chief_Editor>`_. Эта CMS может быть использована для запуска новостного сайта, блога, статичного сайта. 

В этой сборке доступны модули `spicy.document <https://github.com/spicycms/spicy.document>`_, `spicy.categories <https://github.com/spicycms/spicy.categories>`_, `spicy.labels <https://github.com/spicycms/spicy.labels>`_, `spicy.feedback <https://github.com/spicycms/spicy.feedback>`_, `spicy.history <https://github.com/spicycms/spicy.history>`_, и `spicy.menu <https://github.com/spicycms/spicy.menu>`_.
