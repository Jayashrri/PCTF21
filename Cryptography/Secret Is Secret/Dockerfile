FROM php:7.4.5-apache

RUN apt-get update && apt-get upgrade -y && apt-get install sudo

RUN useradd -m p_ctf && \
    echo "root:rootPassword" | chpasswd && \
    echo "p_ctf:randomPassword" | chpasswd

RUN echo -e "admin1     bm90V29ya2luZw==\nadmin2       aXRzQXNlY3JldA==\nadmin3      d3JvbmdQYXNzd29yZA==" >> /etc/passwd && chmod 600 /etc/shadow

RUN mkdir /var/www/html/webadmin

COPY index.html /var/www/html

COPY hacker.jpeg /var/www/html

COPY index.php /var/www/html/webadmin

RUN chmod -R 655 /var

USER p_ctf

WORKDIR /home/p_ctf


