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

