web: daphne -b 0.0.0.0 -p 8001 TicTacToe.asgi:application
worker: python manage.py runworker --settings=TicTacToe.settings -v2 channel_layer