# To set-up detemine in a VPS

apt-get update
apt-get upgrade

dpkg-reconfigure locales
# │    [*] en_GB ISO-8859-1                                                                                                                ▒   │ 
# │    [*] en_GB.ISO-8859-15 ISO-8859-15                                                                                                   ▒   │ 
# │    [*] en_GB.UTF-8 UTF-8
# default -   en_GB.UTF-8    
apt-get install apache2-mpm-prefork sqlite3 python-pysqlite2 python-amara subversion-tools python-django xvfb libapache2-mod-python pdftk xmlstarlet enscript ghostscript less
adduser bms
# change the su passwd

apt-get install chkrootkit
apt-get install logcheck

#Logcheck configuration is done in the file /etc/logcheck/logcheck.conf.
#To change the email address to which reports are sent, change the line:
#        SENDMAILTO="root"
#to:
#        SENDMAILTO="emailaddress@some.domain.tld"


ln -s /usr/share/python-support/python-django/django/contrib/admin/media /var/www/
mkdir /home/www-data
chown www-data.www-data /home/www-data/
cd /home/www-data/
su www-data
svn checkout https://determine.googlecode.com/svn/trunk/ determine --username bms@barwap.com
nano ./determine/django/determine/settings.py
# change SECRET_KEY = ''
exit
ln -s /home/www-data/determine/django/determine /usr/lib/python2.5/site-packages/
rm /etc/apache2/sites-available/default
ln -s /home/www-data/determine/other/apache/default /etc/apache2/sites-available/default
wget http://www.barwap.com/files/2009/May/10/wkhtmltopdf
chmod +x ./wkhtmltopdf
mv ./wkhtmltopdf /usr/bin/
ln -s /home/www-data/determine/other/scripts/determine-make-pdf.sh /usr/bin
su www-data
cd /home/www-data/determine/django/determine/
python ./manage.py syncdb
# answer no
python ./manage.py loaddata ./flatpages.xml
exit
/etc/init.d/apache2 restart
ln -s /home/www-data/determine/django/determine/site_media /var/www/
apt-get install python-lxml 
/etc/init.d/apache2 restart
dpkg-reconfigure exim4-config
nano .forward
# Set to forward email address
su bms
cd /home/bms
nano .forward
# Set to forward email address

exit
apt-get install denyhosts
nano /var/lib/denyhosts/allowed-hosts

##  Never block
## 87.74.83.14

/etc/init.d/denyhosts stop
denyhosts purge

nano /etc/hosts.allow
#ALL : 87.74.83.14

# Add crontabe for tmp-clean.sh
# Add the following in to file and crontab file
# "7 * * * * /home/www-data/determine/other/scripts/tmp-clean.sh >>/dev/null 2>&1"

