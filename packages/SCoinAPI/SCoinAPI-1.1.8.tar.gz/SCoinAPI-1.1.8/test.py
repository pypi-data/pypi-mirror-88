# from SCoinAPI import centralbank
from SCoinAPI.SCoinAPI import centralbank

cb = centralbank.Central_Bank()
# res = ck.send_token('nUjymFTzrJcuqizbswdKACJtpRwMZtEkwXzQDxBk','cb','marmotbank',40)
# res = ck.set_central_bank('marmotbank','jiayingfengtingweijie')
# res = ck.create_did('marmotbank','jiayingfengtingweijie')
# res = ck.get_balance('marmotbank')
# res = cb.get_balance('marmotbank')
# print(res)
res = cb.remove_layer1('marmotbank','fengtingjiayingweijie')

# import requests
# link = 'http://52.44.57.177:8888/'
# headers = {
#     'Content-Type': 'application/json',
#     'X-API-key': 'fengtingjiayingweijie'
# }
# data = {
#     "sen": "marmotbank",
#     "rev": "marmotbank-backend-wyne",
#     "method": "2",
#     "description": "Light token", 
#     "txn": ['ZNKWBHWRXWB9GXOABXJPSQIUSWEKTOYHWMDYMLCLHWEQEBROYGAS9FAVBISEXTICGJSQGNSZMQZIZ9999', 'BLMYVPS9CJJSHQISSBFKDVUBQPKFWXMUIKUCXCNIDPKOHWNP9IZFCPJAWTAISPQCUQJAGKBQSKEKZ9999']
# }
# res = requests.post(link+'send_tokens',headers=headers,data=data)
print(res)