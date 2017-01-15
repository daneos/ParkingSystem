from time import time, mktime
from rest.models import *

def EventSerializer(e):
	data = {}
	data['event'] = e
	return data

def SessionSerializer(e, s):
	data = EventSerializer(e)
	data['session'] = str(s.session_hash)
	return data

def IdSerializer(e, x):
	data = EventSerializer(e)
	data['id'] = x.id
	return data

def UserListSerializer(e, l):
	data = EventSerializer(e)
	data['users'] = []
	for u in l:
		user = {}
		user['id'] = u.id
		user['name'] = u.name
		data['users'].append(user)
	return data

def UserSerializer(e, u):
	data = EventSerializer(e)
	data['id'] = u.id
	data['name'] = u.name
	data['surname'] = u.surname
	data['address'] = u.address
	data['phone'] = u.phone
	data['email'] = u.email
	return data

def ParkingListSerializer(e, l):
	data = EventSerializer(e)
	data['parkings'] = []
	for p in l:
		parking = {}
		parking['id'] = p.id
		parking['name'] = p.name
		parking['address'] = p.address
		data['parkings'].append(parking)
	return data

def TransactionMethodListSerializer(e, l):
	data = EventSerializer(e)
	data['transactionmethods'] = []
	for tm in l:
		transactionmethod = {}
		transactionmethod['id'] = tm.id
		transactionmethod['name'] = tm.name
		data['transactionmethods'].append(transactionmethod)
	return data

def SpotListSerializer(e, l):
	data = EventSerializer(e)
	data['spots'] = []
	for s in l:
		spot = {}
		spot['id'] = s.id
		spot['parking_id'] = s.parking_id.id
		if s.user_id:
			spot['user_id'] = s.user_id.id
		else:
			spot['user_id'] = None
		spot['cost'] = s.cost
		data['spots'].append(spot)
	return data

def WalletSerializer(e, w):
	data = EventSerializer(e)
	data['id'] = w.id
	data['balance'] = w.balance
	return data

def CarListSerializer(e, l):
	data = EventSerializer(e)
	data['cars'] = []
	for c in l:
		car = {}
		car['id'] = c.id
		car['plate'] = c.plate
		data['cars'].append(car)
	return data

def CarSerializer(e, c):
	data = EventSerializer(e)
	data['id'] = c.id
	data['plate'] = c.plate
	return data

def CodeSerializer(e, c):
	data = EventSerializer(e)
	data['data'] = c.data
	return data

def WithdrawalSerializer(e, w, a):
	data = EventSerializer(e)
	data['id'] = w.id
	data['amount'] = a
	return data

def TransactionListSerializer(e, l):
	data = EventSerializer(e)
	data['transactions'] = []
	for t in l:
		transaction = {}
		transaction['id'] = t.id
		transaction['wallet_id'] = t.wallet_id.id
		transaction['time'] = int(mktime(t.time.utctimetuple()))
		transaction['method_id'] = t.method_id.id
		transaction['amount'] = t.amount
		data['transactions'].append(transaction)
	return data

def NotificationListSerializer(e, l):
	data = EventSerializer(e)
	data['notifications'] = l
	return data

def FreeSpotListSerializer(e, l):
	data = EventSerializer(e)
	data['spots'] = []
	for s in l:
		spot = {}
		spot['id'] = s.id
		spot['spot_id'] = s.spot_id.id
		data['spots'].append(spot)
	return data

def SearchSerializer(e, l):
	data = EventSerializer(e)
	data['spots'] = []
	for f in l:
		spot = {}
		spot['id'] = f.id
		spot['parking_id'] = f.spot_id.parking_id.id
		data['spots'].append(spot)
	return data

def FreeSpotSerializer(e, f):
	data = EventSerializer(e)
	data['id'] = f.id
	data['spot_id'] = f.spot_id.id
	data['time_start'] = int(mktime(f.time_start.utctimetuple()))
	data['time_end'] = int(mktime(f.time_end.utctimetuple()))
	return data

def ReservationListSerializer(e, l):
	data = EventSerializer(e)
	data['reservations'] = []
	for r in l:
		reservation = {}
		reservation['id'] = r.id
		reservation['spot_id'] = r.spot_id.id
		reservation['time_start'] = int(mktime(r.time_start.utctimetuple()))
		reservation['time_end'] = int(mktime(r.time_end.utctimetuple()))
		data['reservations'].append(reservation)
	return data

def ReservationSerializer(e, r, c):
	data = EventSerializer(e)
	data['id'] = r.id
	data['time_start'] = int(mktime(r.time_start.utctimetuple()))
	data['time_end'] = int(mktime(r.time_end.utctimetuple()))
	data['spot_id'] = r.spot_id.id
	data['user_id'] = r.user_id.id
	data['code'] = c.id
	return data

def ProlongationSerializer(e, r):
	data = EventSerializer(e)
	data['id'] = r.id
	data['time_end'] = int(mktime(r.time_end.utctimetuple()))
	return data

def OpenSerializer(e, o):
	data = EventSerializer(e)
	data['open'] = o
	return data

def TransactionSerializer(e, t):
	data = EventSerializer(e)
	data['id'] = t.id
	data['wallet_id'] = t.wallet_id.id
	data['amount'] = t.amount
	return data

def HeartbeatSerializer(e, t):
	data = EventSerializer(e)
	data['time'] = time()-t
	return data