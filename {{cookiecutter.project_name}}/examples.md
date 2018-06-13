# API Examples

## Create User

```bash
curl 
    -d '{"username":"{{cookiecutter.username}}", "email": "{{cookiecutter.email}}", "password":"secretPW123"}' 
    -X POST http://127.0.0.1:8000/api/create-user/ 
    -H "Content-Type: application/json"
```

```json
{
    "id":1,
    "username":"{{cookiecutter.username}}",
    "email":"{{cookiecutter.email}}",
    "token":"ourToken101"
}
```

## Get/Create Token

```bash
curl 
    -d '{"username":"{{cookiecutter.username}}", "password":"secretPW123"}' 
    -X POST http://127.0.0.1:8000/api/token-auth/ 
    -H "Content-Type: application/json"
```

```json
{
    "token":"ourToken101"
}
```

## Get Protected Resourse

```bash
curl 
    -X GET http://127.0.0.1:8000/api/users/{{cookiecutter.username}}/ 
    -H "Content-Type: application/json" 
    -H "Authorization: Token ourToken101"
```
```json
{
    "id":1,
    "username":"{{cookiecutter.username}}",
    "email":"{{cookiecutter.email}}"
}
```

```bash
curl 
    -X GET http://127.0.0.1:8000/api/users/{{cookiecutter.username}}/ 
    -H "Content-Type: application/json" 
    -H "Authorization: Token someOtherToken"
```


```json
{
    "detail":"You do not have permission to perform this action."
}
```