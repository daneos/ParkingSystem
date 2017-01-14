from rest.models import *

def EventSerializer(e):
	data = {}
	data['event'] = e
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

# def RoomSerializer(r, detail_mode=False):
# 	data = {}
# 	data['id'] = r.id
# 	data['name'] = r.name
# 	data['description'] = r.description
# 	if detail_mode:
# 		data['timetable'] = [ TimeSpanSerializer(t) for t in r.timetable.all() ]
# 	return data

def SessionSerializer(e, s):
	data = EventSerializer(e)
	data['session'] = str(s.session_hash)
	return data

# def TimeSpanSerializer(t):
# 	data = {}
# 	data['owner'] = RoomTimetable.objects.get(timespan=t).owner.id
# 	data['time_start'] = str(t.time_start)
# 	data['time_end'] = str(t.time_end)
# 	return data

# def ParkSpotSerializer(p):
# 	data = {}
# 	data['id'] = p.id
# 	data['location'] = p.location
# 	if p.user:
# 		data['user'] = p.user.id
# 	data['spot'] = "free" if p.free else "taken"
# 	return data

# def FoodTicketSerializer(t, detail_mode=False):
# 	data = {}
# 	data['id'] = t.id
# 	data['name'] = t.name
# 	data['thumb'] = t.thumb
# 	if detail_mode:
# 		data['description'] = t.description
# 		data['code'] = t.code
# 	return data

# def GroupSerializer(g):
# 	data = {}
# 	data['id'] = g.id
# 	data['name'] = g.name
# 	membership = GroupMembership.objects.filter(group=g)
# 	data['members'] = [ { 'role': member.role.id, 'user': member.user.id } for member in membership ]
# 	return data

# def TaskSerializer(t, detail_mode=False):
# 	data = {}
# 	data['id'] = t.id
# 	data['name'] = t.name
# 	data['done'] = t.done
# 	data['deadline'] = str(t.deadline)
# 	if detail_mode:
# 		membership = TaskMembership.objects.filter(task=t)
# 		data['time_start'] = str(t.time_start)
# 		data['description'] = t.description
# 		data['members'] = [ { 'user': member.user.id, 'role': member.role.id } for member in membership ]
# 		data['comments'] = [ { 'id': comment.id, 'user': comment.user.id, 'text': comment.text } for comment in t.comments.all() ]
# 	return data

# def RoleSerializer(r):
# 	data = {}
# 	data['id'] = r.id
# 	data['name'] = r.name
# 	data['description'] = r.description
# 	return data

# def EventSerializer(e, detail_mode=False):
# 	data = {}
# 	data['id'] = e.id
# 	data['name'] = e.name
# 	data['time_start'] = str(e.time_start)
# 	data['time_end'] = str(e.time_end)
# 	data['private'] = e.private
# 	if detail_mode:
# 		data['note'] = e.note
# 		if e.place_ext:
# 			data['place_ext'] = e.place_ext
# 		if e.place_int:
# 			data['place_int'] = RoomSerializer(e.place_int)
# 		membership = EventMembership.objects.filter(event=e)
# 		data['members'] = [ { 'user': member.user.id, 'role': member.role.id } for member in membership ]
# 	return data

# def EventTypeSerializer(et):
# 	data = {}
# 	data['id'] = et.id
# 	data['name'] = et.name
# 	return data

# def MessageSerializer(m):
# 	data = {}
# 	data['id'] = m.id
# 	data['from'] = m.from_user_id
# 	data['to'] = m.to_user_id
# 	data['time'] = str(m.time)
# 	data['text'] = m.text
# 	return data