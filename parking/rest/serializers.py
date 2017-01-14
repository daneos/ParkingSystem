from time import mktime
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