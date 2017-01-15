from time import time, mktime
from datetime import datetime
from base64 import b64encode
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
	event = "2001 Spot freed"
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		spot = get_object_or_404(Spot, pk=sid)
		if spot.owner_id == session.user:
			try:
				freespot = FreeSpot(
					spot_id=spot,
					time_start=datetime.fromtimestamp(float(rq.GET.get("from"))),
					time_end=datetime.fromtimestamp(float(rq.GET.get("to")))
				)
				freespot.save()
			except Exception as e:
				return response("error", "9004 Application error: %s" % str(e))
			else:
				return response("ok", FreeSpotSerializer(event, freespot))
		else:
			return response("error", "9012 Not an owner")
	else:
		return session_expired()


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
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		spot = rq.GET.get("spot", None)
		time_start = rq.GET.get("from", None)
		time_end = rq.GET.get("to", None)
		if None in (spot, time_start, time_end):
			event = "1012 Reservation list"
			return response("ok", ReservationListSerializer(event, Reservation.objects.filter(user_id=session.user)))
		else:
			try:
				spot_obj = get_object_or_404(Spot, id=spot)
				reservation = Reservation(
					user_id=session.user,
					spot_id=spot_obj,
					time_start=datetime.fromtimestamp(float(time_start)),
					time_end=datetime.fromtimestamp(float(time_end))
				)
				reservation.save()
				spot_obj.user_id = session.user
				spot_obj.save()
				code = Code(
					parking_id = spot_obj.parking_id,
					data=b64encode("PID:%d\\Open allowed.\\%X" % (spot_obj.parking_id.id, int(time()))),
					active=True
				)
				code.save()
			except Exception as e:
				return response("error", "9004 Application error: %s" % str(e))
			else:
				event = "2003 Reservation created"
				return response("ok", ReservationSerializer(event, reservation, code))
	else:
		return session_expired()


def reservation_prolong(rq, sessid, rid=None):
	event = "2004 Reservation prolonged"
	if validate_sessid(sessid):
		if rid:
			reservation = get_object_or_404(Reservation, pk=rid)
			time_end = rq.GET.get("to", None)
			if time_end:
				try:
					reservation.time_end = datetime.fromtimestamp(float(time_end))
					reservation.save()
				except Exception as e:
					return response("error", "9004 Application error: %s" % str(e))
				else:
					return response("ok", ProlongationSerializer(event, reservation))
			else:
				return response("error", "9013 No new time")
		else:
			return response("error", "9014 No reservation ID.")
	else:
		return session_expired()


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
			return response("ok", SearchSerializer(event, freespots))

	else:
		return session_expired()


def notifications(rq, sessid):
	event = "1014 Notifications"
	if validate_sessid(sessid):
		# try:
			session = get_object_or_404(Session, session_hash=sessid)
			notifs = []

			# check processed transactions
			wallet = get_object_or_404(Wallet, owner_id=session.user)
			try:
				transactions = Transaction.objects.filter(
					Q(wallet_id=wallet) &
					Q(time__gte=datetime.fromtimestamp(time()-12*3600))
				)
			except Exception:
				transactions = []
			for t in transactions:
				notif = { "time":mktime(t.time.utctimetuple()) }
				notif["message"] = "Your transaction of %f PLN was registered" % t.amount
				notifs.append(notif)

			# check reservations
			try:
				reservations = Reservation.objects.filter(user_id=session.user)
				print reservations
			except Exception as e:
				reservations = []
			
			for r in reservations:
				print r
				if mktime(r.time_end.utctimetuple()) <= time()+1800:
					notif = { "time":mktime(r.time_end.utctimetuple()) }
					notif["message"] = "Your reservation on %s is ending in %dmin" % (r.spot_id.parking_id.name, int((mktime(r.time_end.utctimetuple())-time())/60))
					notifs.append(notif)
		# except Exception as e:
			# return response("error", "9004 Application error: %s" % str(e))
		# else:
			return response("ok", NotificationListSerializer(event, notifs))
	else:
		return session_expired()


def payment(rq, wid=None):
	event = "3002 Payment"
	if wid:
		wallet = get_object_or_404(Wallet, pk=wid)
		amount = rq.GET.get("amount", None)
		if amount:
			try:
				amount = float(amount)
				transaction = Transaction(
					wallet_id=wallet,
					amount=amount,
					time=datetime.fromtimestamp(time()),
					method_id=TransactionMethod.objects.get(name="PayPal")
				)
				transaction.save()
				wallet.balance = wallet.balance + amount
				wallet.save()
			except Exception as e:
				return response("error", "9004 Application error: %s" % str(e))
			else:
				return response("ok", TransactionSerializer(event, transaction))
		else:
			return response("error", "9017 No amount")
	else:
		response("error", "9018 No wallet ID")


def open(rq, data=None):
	event = "4001 Open"
	if data:
		code = get_object_or_404(Code, data=data)
		if code.active:
			try:
				code.active = False
				code.save()
			except Exception as e:
				return response("error", "9004 Application error: %s" % str(e))
			else:
				return response("ok", OpenSerializer(event, True))
		else:
			return response("error", "9016 Code inactive")
	else:
		return response("error", "9015 No data")


def heartbeat(rq):
	start = time()
	event = "5001 Heartbeat"

	# remove expired reservations and create freespots for them
	try:
		reservations = Reservation.objects.filter(time_end__lte=datetime.fromtimestamp(time()))
		for r in reservations:
			r.spot_id.user_id = None
			r.spot_id.save()
			if not r.spot_id.owner_id:
				freespot = FreeSpot(
					spot_id=r.spot_id,
					time_start=None,
					time_end=None
				)
				freespot.save()
			r.delete()
	except Exception as e:
		return response("error", "9021 Reservation expiration error: %s" % str(e))

	# remove expired freespots
	try:
		freespots = FreeSpot.objects.filter(time_end__lte=datetime.fromtimestamp(time()))
		for f in freespots:
			f.delete()
	except Exception as e:
		return response("error", "9020 FreeSpot expiration error: %s" % str(e))

	# expire sessions
	try:
		sessions = Session.objects.all()
		for s in sessions:
			if mktime(s.last_activity.utctimetuple()) < time()-3600:
				s.active = False
				s.save()
	except Exception as e:
		return response("error", "9019 Session expiration error: %s" % str(e))

	return response("ok", HeartbeatSerializer(event, start))