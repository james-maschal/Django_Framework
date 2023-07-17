# Django Framework Deployment For JNS





**All commands were written to be used with Red Hat Enterprise Linux 9.1**


- Install git if not already installed `sudo yum install git`
- Clone this repository to /opt/ as root
    - Permissions for all files within and including /opt/django_framework/ should be:
        - Files: rw-r--r--
        - Directories: rwxr-xr-x
        - Everything should be owned by root:root

- Open /opt/django_framework/mysite/template.ini
    - Add a [username] and [password] you will use for your mysql account.
    - Add the IP or hostname of your database connection
    - Add the database port (should be 3306 for MySQL)
    - Add the domain name of the server you will serve the application from.
    - Save as "info.ini"

- Open /opt/django_framework/jns.conf
    - *This is the VirtualHost config file for Apache*
    - Change the ServerName to the domain name of your server.

- Create a python venv in /opt/django_framework/venv/ as root
    - *Python Version used: 3.9.14

- Within venv:
    - `pip install django`
    - `pip install pymysql`
    - `pip install cryptography`

- Pip list should look like:

```
Package      Version
------------ -------
asgiref      3.6.0
cffi         1.15.1
cryptography 39.0.0
Django       4.1.6
pip          21.2.3
pycparser    2.21
PyMySQL      1.0.2
setuptools   53.0.0
sqlparse     0.4.3
```



- Install mysql-server using linux repositories `sudo yum install mysql-server`

- Start mysql server `sudo systemctl start mysqld.service`

- Within mysql:

    - `CREATE USER [username] IDENTIFIED BY '[password]';`
    - `CREATE DATABASE fibercritical;`
    - `CREATE DATABASE int_reclaim;`
    - `CREATE DATABASE temperature;`
    - `GRANT ALL ON fibercritical.* TO [username];`
    - `GRANT ALL ON int_reclaim.* TO [username];`
    - `GRANT ALL ON temperature.* TO [username];`



- Install mod_wsgi with `sudo yum install mod_wsgi`

- Install apache with `sudo yum install httpd`

- Copy /opt/django_framework/jns.conf to the extra configuration file location for Apache (for RHEL, it is /etc/httpd/conf.d/)

- Verify Apache can connect to your databse with `sudo getsebool httpd_can_network_connect_db` and `sudo getsebool httpd_can_network_connect`
    - If this is set to "off", enter `sudo setsebool -P httpd_can_network_connect_db on` and `sudo setsebool -P httpd_can_network_connect on`

- Start Apache server with "`sudo systemctl start httpd.service`"

- Ensure any firewall allows access over port 80/tcp and 3306/tcp.
    - On RHEL, this may be done with:
         - `sudo firewall-cmd --add-port=80/tcp --permanent`
         - `sudo firewall-cmd --add-port=3306/tcp --permanent`

- Within /opt/django_framework python venv: 
    - `sudo /opt/django_framework/venv/python manage.py makemigrations jns`
        - (this shouldn't do anything, but just in case.)
    - `sudo /opt/django_framework/venv/python manage.py migrate`
    - `sudo /opt/django_framework/venv/python manage.py migrate --database=int_reclaim`
    - `sudo /opt/django_framework/venv/python manage.py migrate --database=temperature`

- Within /opt/django_framework/jns/templates/jns/netbox_results.html
    - replace "YOUR-SERVER-HERE" in the HTTPS link with your server FQDN
