from telethon import TelegramClient, sync

api_id = '<your API>'
api_hash = '<your API>'
# 149.154.167.50:443

client = TelegramClient('<appname>', api_id, api_hash).start()

# get all the channels that I can access
groups = {d.entity.title : d.entity
            for d in client.get_dialogs()
            if d.is_group}

group_array = ['<your groups>','']

# d.entity est une instance de chat
# print(groups)
# choose the one that I want list users from
for name in group_array:
	group = groups[name]
	print('\n\n\n###### GROUPE : '+name)
	print('- group name : '+str(group.id))
	# get all the users and print them
	for u in client.get_participants(group):
		print(u.id, u.first_name, u.last_name, u.username)