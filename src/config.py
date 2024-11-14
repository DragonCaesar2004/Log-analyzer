formats = ('markdown', 'adoc',)
one_argument_flags = ('from_date','to_date','format', 'filter_field')
# TODO сделать  тайп алиас, 
log_fields = {'ip_addr':' IP-адрес клиента',
              'user_name':'Имя пользователя',
              'local_time':'Локальное время запроса',
              'method':'Метод запроса',
              'resource':'Это путь к ресурсу на сервере',
              'http_version':'Это версия протокола, используемая для запроса',
              'status_code':'Статус-код ответа сервера',
              'body_bytes_sent':'Количество отправленных байт в теле ответа',
              'http_referer':'Адрес страницы, с которой пришёл запрос',
              'http_user_agent':'Пользовательский агент (информация о браузере или приложении)',
              }