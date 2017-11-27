openssl req -x509 -newkey rsa:2048 -keyout server_private_key.pem -out server_cert.pem -days 355 -nodes
openssl x509 -outform der -in server_cert.pem -out server_cert.der
openssl req -new -x509 -keyout json_server.pem -out json_server.pem -days 365 -nodes
