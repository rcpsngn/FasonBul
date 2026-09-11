import pymysql

# mysqlclient yerine PyMySQL kullanıyoruz (saf Python, 3 farklı bilgisayarda/PyCharm'da
# derleme bağımlılığı olmadan kurulabiliyor). Django'nun mysql backend'i MySQLdb API'si
# bekliyor, PyMySQL bunu kendini MySQLdb gibi tanıtarak sağlıyor.
# Django 4.2+ ayrıca "mysqlclient >= 2.2.1" sürüm kontrolü yapıyor; PyMySQL kendi
# sürümünü (1.x) raporladığı için bu kontrolü geçmesi için sürümü burada taklit ediyoruz.
pymysql.version_info = (2, 2, 4, "final", 0)
pymysql.install_as_MySQLdb()
