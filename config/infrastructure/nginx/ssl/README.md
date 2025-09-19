# SSL Certificates

This directory should contain SSL certificates for HTTPS support.

## Required Files:
- `cert.pem` - SSL certificate
- `key.pem` - SSL private key

## For Development:
You can generate self-signed certificates using:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

## For Production:
Use certificates from a trusted Certificate Authority (CA) like Let's Encrypt.

## Note:
The nginx configuration is currently set to HTTP only. To enable HTTPS, uncomment the HTTPS server block in nginx.conf and place the certificates in this directory.



