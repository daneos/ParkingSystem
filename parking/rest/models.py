import uuid
from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	phone = models.CharField(max_length=20)
	email = models.EmailField()
	password = models.CharField(max_length=40)

	def __str__(self):
		return "User id:%d %s %s" % (self.id, self.name, self.surname)


class Parking(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)

	def __str__(self):
		return "Parking id:%d %s %s" % (self.id, self.name, self.address)


class TransactionMethod(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return "TransactionMethod id:%d %s" % (self.id, self.name)


class Spot(models.Model):
	id = models.AutoField(primary_key=True)
	parking_id = models.ForeignKey(Parking, on_delete=models.CASCADE)
	owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	cost = models.FloatField()

	def __str__(self):
		return "Spot id:%d on parking id:%d" % (self.id, self.parking_id)


class Code(models.Model):
	id = models.AutoField(primary_key=True)
	parking_id = models.ForeignKey(Parking, on_delete=models.CASCADE)
	data = models.CharField(max_length=100)
	active = models.BooleanField()

	def __str__(self):
		return "Code id:%d %s" % (self.id, self.data)


class Car(models.Model):
	id = models.AutoField(primary_key=True)
	plate = models.CharField(max_length=100)
	owner_id = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return "Car id:%d %s" % (self.id, self.plate)


class Wallet(models.Model):
	id = models.AutoField(primary_key=True)
	owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
	balance = models.FloatField()

	def __str__(self):
		return "User id:%d %s %s" % (self.id, self.name, self.surname)


class Reservation(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	spot_id = models.ForeignKey(Spot, on_delete=models.CASCADE)

	def __str__(self):
		return "Reservation id:%d spot id:%d" % (self.id, self.spot_id)


class Transaction(models.Model):
	id = models.AutoField(primary_key=True)
	wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount = models.FloatField()
	time = models.DateTimeField()
	method_id = models.ForeignKey(TransactionMethod, on_delete=models.CASCADE)

	def __str__(self):
		return "Transaction id:%d %f" % (self.id, self.amount)


class FreeSpot(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()
	spot_id = models.ForeignKey(Spot, on_delete=models.CASCADE)

	def __str__(self):
		return "FreeSpot id:%d spot id:%d" % (self.id, self.spot_id)


class Session(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField(auto_now_add=True)
	last_activity = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	session_hash = models.UUIDField(default=uuid.uuid4)

	def __str__(self):
		return "Session id:%d %s" % (self.id, str(self.session_hash))