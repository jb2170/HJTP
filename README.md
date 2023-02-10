# HJTP

Send null-terminated JSON messages between a server and a client

## Examples

Using [SocketCat][SocketCat]

tty1
```
$ ./test/basic-server/main.py
```

tty2
```
$ echo -en '{"method": "get", "filename": ".gitignore"}\0' | socket-write.py inet localhost 8080 2>/dev/null
```
```json
{
  "code": 200,
  "body": "5f5f707963616368655f5f2f0a2f76656e762f0a"
}
```

[SocketCat]: https://github.com/SelfAdjointOperator/SocketCat
