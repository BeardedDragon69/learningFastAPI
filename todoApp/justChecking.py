from jose import jwt


SECRET_KEY ="5d2a96f5a3c09d21bed21b7f11c9e94a70f943b3d381d4f7906a5e51de8165c8"
ALGORITHM = "HS256"

payload = {'sub':  'user123'}
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print(token)


decodedToken = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

print(decodedToken)
