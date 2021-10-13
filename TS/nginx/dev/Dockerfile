FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/sites-enabled
COPY enable/default.conf /etc/nginx/sites-enabled/default.conf
COPY default.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
