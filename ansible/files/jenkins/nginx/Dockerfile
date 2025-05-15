FROM gear2000/nginx
MAINTAINER Gary Leong <gwleong@gmail.com>

RUN apt-get update && apt-get install -y vim ack-grep 

RUN openssl req -newkey rsa:1024 -new -x509 -subj "/C=US/ST=California/L=SanFrancisco/O=Dis/CN=dev.example.com" -days 1024 -nodes -out /etc/ssl/certs/nginx.crt -keyout /etc/ssl/private/nginx.key

RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

RUN rm -rf /etc/nginx/sites-enabled/* 
ADD sites-enabled/ /etc/nginx/sites-enabled/
ADD nginx.conf /etc/nginx/

EXPOSE 443 80 

CMD ["nginx", "-g", "daemon off;"]
