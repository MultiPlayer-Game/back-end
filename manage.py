#!/usr/bin/env python
import os
import sys
# import pusher

# pusher_client = pusher.Pusher(
#   app_id="957206",
#   key="07213da62d31ac848d3c",
#   secret="adc0e78f434f774480fe",
#   cluster="mt1",
#   ssl=True
# )

# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adv_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
