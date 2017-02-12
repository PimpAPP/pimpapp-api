import pymongo

client = pymongo.MongoClient("mongodb://recopimp:********@ds025399.mlab.com:25399/recopimp")
db = client['recopimp']

join_dict = {}

for catador in db['carroceiros'].find():
    join_dict[catador["id"]] = catador

for tel_info in db['telephones'].find():
    del tel_info['_id']
    join_dict[tel_info['catador_id']].update(tel_info)

#from pprint import pprint
#pprint(join_dict)

headers = [
'id',
'user_id',
'catador_id',
'catador_user_id',
'name',
'allow_public_edition',
'carrocaPimpada',
'catador_type',
'created_on',
'email',
'internet1',
'internet2',
'miniBio',
'moderation_status',
'motorizedVehicle',
'observations',
'operator_telephone1',
'operator_telephone2',
'socialNetwork',
'telephone1',
'telephone2',
'whatsapp1',
'whatsapp2',
]

print(';'.join(headers))
for _, register in join_dict.items():
    print(';'.join([str(register[key]) if register[key] else '' for key in headers]))
