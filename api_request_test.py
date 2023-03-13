import requests

# r = requests.get('http://127.0.0.1:8000/api/Post/1/')
#
# print(r.status_code)
# print("_____________")
# print(r.headers['content-type'])
# print("_____________")
# print(r.encoding)
# print("_____________")
# print(r.text)
# print("_____________")
# print(r.json())
# print("_____________")

r = requests.delete('http://127.0.0.1:8000/api/Post/100/')

print(r.status_code)
print("_____________")
