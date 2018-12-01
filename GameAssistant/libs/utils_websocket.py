# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,HttpResponseForbidden
from django.urls import reverse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from GameAssistant.libs.utils_session import get_ws_id_from_session

def ws_push(ws_type, ws_msg):
    def _ws_push(func):
        def wrapper(request, *callback_args, **callback_kwargs):
            try:
                ws_id = get_ws_id_from_session(request)
                response = func(request, *callback_args, **callback_kwargs)
                if (response.status_code == 200) or (response.status_code == 302):
                    if ws_id:
                        layer = get_channel_layer()
                        async_to_sync(layer.group_send)(
                            ws_id,
                            {
                            'type': ws_type,
                            'message': str(ws_msg)
                            }
                        )

                return response
            except Exception as e:
                return HttpResponseBadRequest('Unknown error while running utils.ws_push! Details: {0}'.format(e))
        return wrapper
    return _ws_push