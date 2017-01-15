from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Q

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
	if validate_sessid(sessid):
		if pid is None:
			event = "1006 Free spots"
			return response("ok", FreeSpotListSerializer(event, FreeSpot.objects.all()))
		else:
			event = "1007 Free spots"
			try:
				parking = get_object_or_404(Parking, id=pid)
				spots = Spot.objects.filter(parking_id=parking)
				freespots = FreeSpot.objects.filter(spot_id=spots)
			except Exception as e:
				return response("error", "9004 Application error: %s" % str(e))
			return response("ok", FreeSpotListSerializer(event, freespots))
	else:
		return session_expired()


def wallet(rq, sessid):
	event = "1008 Wallet"
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		return response("ok", WalletSerializer(event, get_object_or_404(Wallet, owner_id=session.user)))
	else:
		return session_expired()


def withdraw(rq, sessid):
	event = "3001 Withdrawal"
	if validate_sessid(sessid):
		try:
			amount = float(rq.GET.get("amount", None))
		except Exception:
			amount = None
		if amount:
			session = get_object_or_404(Session, session_hash=sessid)
			wallet = get_object_or_404(Wallet, owner_id=session.user)
			if amount > wallet.balance:
				return response("error", "9007 Insufficient funds")
			if query_payment_method(wallet, amount):
				return response("ok", WithdrawalSerializer(event, wallet, amount))
			else:
				return response("error", "9008 Not accepted by remote payment system")
		else:
			return response("error", "9009 No amount given")
	else:
		return session_expired()


def transaction(rq, sessid):
	event = "1009 Transaction list"
	if validate_sessid(sessid):
		try:
			session = get_object_or_404(Session, session_hash=sessid)
			wallet = get_object_or_404(Wallet, owner_id=session.user)
			transactions = Transaction.objects.filter(wallet_id=wallet)
		except Exception as e:
			return response("error", "9004 Application error: %s" % str(e))
		else:
			return response("ok", TransactionListSerializer(event, transactions))
	else:
		return session_expired()


def car(rq, sessid):
	event = "1010 Car list"
	if validate_sessid(sessid):
		try:
			session = get_object_or_404(Session, session_hash=sessid)
			cars = Car.objects.filter(owner_id=session.user)
		except Exception as e:
			return response("error", "9004 Application error: %s" % str(e))
		else:
			return response("ok", CarListSerializer(event, cars))
	else:
		return session_expired()


def car_add(rq, sessid, plate=None):
	event = "2002 Car added"
	if validate_sessid(sessid):
		if plate:
			try:
				session = get_object_or_404(Session, session_hash=sessid)
				car = Car(
					owner_id=session.user,
					plate=plate
				)
				car.save()
			except Exception as e:
				return response("error", "9004 Application error: %s" % str(e))
			else:
				return response("ok", CarSerializer(event, car))
		else:
			return response("error", "9005 No license plate given")
	else:
		return session_expired()


def code(rq, sessid, cid=None):
	event = "1011 Code"
	if validate_sessid(sessid):
		if cid:
			return response("ok", CodeSerializer(event, get_object_or_404(Code, pk=cid)))
		else:
			return response("error", "9006 No code ID")
	else:
		return session_expired()


def reservation(rq, sessid):
	return response("error", "0000 Not implemented yet")


def reservation_prolong(rq, sessid, rid=None):
	return response("error", "0000 Not implemented yet")


def search(rq, sessid):
	event = "1013 Search results"
	if validate_sessid(sessid):
		try:
			q = rq.GET.get("q", None)
			time_start = rq.GET.get("from", None)
			time_end = rq.GET.get("to", None)
			if None in (q, time_start, time_end):
				return response("error", "9010 Parameter missing")
			parkings = Parking.objects.get(Q(name__icontains=q) | Q(address__icontains=q))
			spots = Spot.objects.filter(parking_id=parkings)
			freespots = FreeSpot.objects.filter(
				Q(spot_id=spots) & 
				Q(time_start__lte=datetime.fromtimestamp(float(time_start))) & 
				Q(time_end__gte=datetime.fromtimestamp(float(time_end)))
			)
			if not (spots and freespots):
				return response("error", "9011 No spots found")
		except Exception as e:
			return response("error", "9004 Application error: %s" % str(e))
		else:
			return response("ok", SearchSerializer(event, freespots, spots))

	else:
		return session_expired()


def notifications(rq, sessid):
	event = "1014 Notifications"
	if validate_sessid(sessid):
		notifs = [
			{
				"time": 0,
				"message": "Test notification."
			}
		]
		return response("ok", NotificationListSerializer(event, notifs))
	else:
		return session_expired()


def payment(rq, wid=None):
	return response("error", "0000 Not implemented yet")


def open(rq, data=None):
	return response("error", "0000 Not implemented yet")