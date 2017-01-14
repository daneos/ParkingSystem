from datetime import datetime
from django.shortcuts import get_object_or_404

from rest.models import *
from rest.serializers import *
from rest.utils import *


def register(rq):
	event = "0001 User registered"
	try:
		user = User(
			name=rq.GET.get("name"),
			surname=rq.GET.get("surname"),
			address=rq.GET.get("address"),
			phone=rq.GET.get("phone"),
			email=rq.GET.get("email"),
			password=rq.GET.get("p")
		)
		user.save()
	except Exception:
		return response("error", "9003 Not registered")
	else:
		return response("ok", IdSerializer(event, user))


def login(rq):
	event = "0002 Logged in"
	user = User.objects.get(email=rq.GET.get("u", None))
	if user.password == rq.GET.get("p", None):
		session = Session(user=user)
		session.save()
		return response("ok", SessionSerializer(event, session))
	else:
		return response("error", "9002 Login unsuccessful")

def logout(rq, sessid):
	event = "0003 Logged out"
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		session.active = False
		session.save()
		return response("ok", EventSerializer(event))
	else:
		return session_expired()

def user(rq, sessid, uid=None):
	if validate_sessid(sessid):
		if uid is None:
			event = "1001 User list"
			return response("ok", UserListSerializer(event, User.objects.all()))
		else:
			event = "1002 User"
			return response("ok", UserSerializer(event, get_object_or_404(User, pk=uid)))
	else:
		return session_expired()
