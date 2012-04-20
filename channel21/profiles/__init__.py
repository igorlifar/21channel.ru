from django_ulogin.signals import assign

def catch_ulogin_signal(*args, **kwargs):
	user   = kwargs['user']
	json   = kwargs['ulogin_data']

	if kwargs['registered']:
		user.first_name = json['first_name']
		user.last_name = json['last_name']
		user.save()

from django_ulogin.models import ULoginUser

assign.connect(receiver = catch_ulogin_signal, sender = ULoginUser, dispatch_uid = 'customize.models')