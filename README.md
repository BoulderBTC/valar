Valar
=====

Watching over middle earth since....forever

Note:  The hosts found in settings.py should be set in /etc/hosts or you should use an ip instead

In order for email notifications to work you need a settings.py file.
Put this in valar/ next to views.py

    gmail_user  = 'gmail username'
    gmail_password = 'gmail application specific password'
    toaddrs = ['recipient1@example.com', 'recipient2@example.com']
    email_sender = "youruser@gmail.com"
    hosts = [
      'hostname1',
      'hostname2',
    ]
