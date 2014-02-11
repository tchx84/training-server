## Training Server

This project is a complementary project to One Laptop Per Child Australia and
Sugar Labs Training Activity. This projects aims to help us understand how users
progress during their training, using the Training Activity.

The Activity can be found at https://github.com/walterbender/training

## Setup

0. Install server dependencies:

    ```
    $yum install git openssl mysql-server python python-pip MySQL-python tornado
    $pip install db-migrate
    ```

1. Create training user:

    ```
    $useradd --user-group --shell /sbin/nologin --comment "training server" training
    ```

2. Get the server bits:

    ```
    $cd /opt/
    $git clone git@github.com:tchx84/training-server.git training
    $cd training/
    $chown training:training server.py deliverer.py misc/deliverer.sh
    ```

3. Create the SSL certificates:

    ```
    $./misc/generate.sh
    $mv *.crt etc/training.crt
    $mv *.key etc/training.key
    ```

4. Create configuration file:

    ```
    $cp etc/training.cfg.example etc/training.cfg
    $vim etc/training.cfg
    ```

5. Create custom templates:

   ```
   $cp data/body.text.example data/body.text
   $cp data/confirmation.text.example data/confirmation.text
   $cp data/subject.text.example data/subject.text
   ```

6. Create the database:

    ```
    $service mysqld start
    $mysql -u root -p < misc/init.sql
    $cd migrations/
    $db-migrate 
    ```

7. Enable delivery job:

    ```
    $cp etc/deliverer.cron.example /etc/cron.d/training-deliverer
    ```

8. Enable server service:

   ```
   $cp etc/training.service.example /etc/systemd/system/training.service
   $service training start
   ```

## More information

If you are only interested in using this server I recommend you to read the
wiki documentation at http://wiki.sugarlabs.org/go/TrainingServer
