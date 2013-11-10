Sportovní centrum
=================

Implementace analýzy sportovního centra do předmětu SAN. Projekt je naprogramován v jazyce Python a frameworku Django 1.6.

Instalace
----------

Je potřeba mít nainstalovaný "Python 2.6.x a vyšší". Dále balíčkový systém "pip" (případně easy_install) a ideálně i virtualenviroments pro Python ( https://pypi.python.org/pypi/virtualenv ).

Stáhněte reposítář k sobě do počítače přes git nebo jako archiv přes Github a rozbalte. Následující postup je pro uživatele Linuxu.

1. Spusťte terminál
2. (nepovinné) Vytvořte si nový virtualenvironemt a aktivujte jej.
3. Nainstalujte všechny závislosti pomocí ``` pip install -r requirements.txt ``` (je potřeba rootosvkých práv, pokud nepracujete ve virtualenv)
4. Vytvořte první databázi příkazem ``` python manage.py syncdb --settings=sportcentrum.settings.base ``` . Vytvořte i administrátorský účet.

Spuštění
--------

V terminálu s pracovní cestou v adresáři projektu zadejte příkaz ``` python manage.py runserver --settings=sportcentrum.settings.base ``` . Aplikace by poté měla být dostupná na adrese 127.0.0.1:8000. (adresa a port se vypíše v terminálu po spuštění)

Když vytvoříte nového uživatele, pošle se mu aktivační email. Kvůli nastavování SMTP a problémy se servery a doménami, z kterých se maily posílají, se výstup emailu zobrazí jako textový výpis v terminálu (konzoli), kde jste spouštěli django server.

Dostupná je taky online verze na adrese [http://sportcentrum.apellia.cz/](http://sportcentrum.apellia.cz/)