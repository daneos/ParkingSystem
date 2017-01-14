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
		wallet = Wallet(
			owner_id=user,
			balance=0
		)
		wallet.save()
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


def parking(rq, sessid):
	event = "1003 Parking list"
	if validate_sessid(sessid):
		return response("ok", ParkingListSerializer(event, Parking.objects.all()))
	else:
		return session_expired()


def transactionmethod(rq, sessid):
	event = "1004 Transaction methods"
	if validate_sessid(sessid):
		return response("ok", TransactionMethodListSerializer(event, TransactionMethod.objects.all()))
	else:
		return session_expired()

def spot_my(rq, sessid):
	event = "1005 Owned spots"
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		user = session.user
		try:
			spots = Spot.objects.filter(owner_id=user)
		except Exception as e:
			return response("error", "9004 Application error: %s" % str(e))
		else:
			return response("ok", SpotListSerializer(event, spots))
	else:
		return session_expired()

def spot_free(rq, sessid, sid=None):
	return response("error", "0000 Not implemented yet")

def freespot(rq, sessid, pid=None):
	return response("error", "0000 Not implemented yet")

def wallet(rq, sessid):
	event = "1008 Wallet"
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		return response("ok", WalletSerializer(event, get_object_or_404(Wallet, owner_id=session.user)))
	else:
		return session_expired()

def withdraw(rq, sessid):
	return response("error", "0000 Not implemented yet")

def transaction(rq, sessid):
	return response("error", "0000 Not implemented yet")

def car(rq, sessid):
	return response("error", "0000 Not implemented yet")

def car_add(rq, sessid, plate=None):
	return response("error", "0000 Not implemented yet")

def code(rq, sessid, cid=None):
	return response("error", "0000 Not implemented yet")

def reservation(rq, sessid):
	return response("error", "0000 Not implemented yet")

def reservation_prolong(rq, sessid, rid=None):
	return response("error", "0000 Not implemented yet")

def search(rq, sessid):
	return response("error", "0000 Not implemented yet")

def notifications(rq, sessid):
	return response("error", "0000 Not implemented yet")

def payment(rq, wid=None):
	return response("error", "0000 Not implemented yet")

def entrance_open(rq, data=None):
	return response("error", "0000 Not implemented yet")