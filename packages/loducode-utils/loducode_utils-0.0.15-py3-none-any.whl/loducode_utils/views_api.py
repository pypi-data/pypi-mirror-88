import json
import random
import string

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import renderers, status
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.translation import ugettext_lazy as _
from rest_framework.compat import coreapi, coreschema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView, exception_handler

from loducode_utils.tasks import send_mail_task


class ObtainCustomAuthToken(ObtainAuthToken):
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            description="""{RETRIEVE}""".format(
                RETRIEVE=_("Service to log in using token, with username and password"),
            ),
            encoding="application/json",
        )


ObtainCustomAuthToken.__doc__ = """{RETRIEVE}
""".format(
    RETRIEVE=_("Service to log in using token, with username and password"),
)


class LogoutView(APIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        response_data = {'message': _('has closed session correctly')}
        return Response(response_data, status=status.HTTP_200_OK,
                        content_type="application/json")


LogoutView.__doc__ = """{RETRIEVE}""".format(
    RETRIEVE=_("Service to log out."),
)

class ForgetPasswordView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.JSONRenderer,)
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
            ],
            description="""{RETRIEVE}""".format(
                RETRIEVE=_('Service to forget password. ** {"username": "user1"} **'),
            ),
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        user_detail = User.objects.filter(username=username).first()
        if user_detail:
            new_password = ''.join(
                random.choices(string.ascii_letters + string.digits, k=8))
            first = None
            user_detail.set_password(new_password)
            user_detail.save()
            if user_detail.first_name:
                if " " in user_detail.first_name:
                    first = (user_detail.first_name).split(" ")[0]
                else:
                    first = user_detail.first_name
            if first:
                message = "{FIRST} {MESSAGE} {NEW}".format(
                    MESSAGE=_("Your new password is:"),
                    NEW=_(new_password),
                    FIRST=first
                )
            else:
                message = "{MESSAGE} {NEW}".format(
                    MESSAGE=_("Your new password is:"),
                    NEW=_(new_password)
                )
            try:
                user_detail.auth_token.delete()
            except:
                pass
            send_mail_task.delay(
                email=user_detail.email,
                subject= _("Your new password is:"),
                message=message
            )
            return Response({"message": _('the new password has been send to Email.')},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"message": _('the new password has been send to Email.')},
                            status=status.HTTP_202_ACCEPTED)

ForgetPasswordView.__doc__ = """{RETRIEVE}""".format(
    RETRIEVE=_('Service to forget password. ** {"username": "user1"} **'),
)

def handler500(exception, context):
    response = exception_handler(exception, context)
    try:
        detail = response.data['detail']
    except:
        try:
            detail = exception.message
        except:
            try:
                detail = response.data
            except:
                detail = str(exception).replace("`", "'")
    try:
        status_code = response.status_code
    except:
        status_code = 500
    response = HttpResponse(
        json.dumps({'message': detail}),
        content_type="application/json",
        status=status_code
    )
    return response