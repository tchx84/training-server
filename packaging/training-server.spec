Name:           training-server
Version:        0.2.0
Release:        1
Summary:        Server for the Training Activity

License:        GPLv2+
URL:            https://github.com/tchx84/training-server
Source0:        %{name}-%{version}.tar.gz

Requires:       python >= 2.7, python-tornado >= 2.2.1, openssl >= 1.0.1, mysql-server >= 5.5, MySQL-python >= 1.2.3 

BuildArch:      noarch

%description
Server for the Training Activity that aims to improve training from trainees feedback

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/opt/training/
cp -r data training migrations misc server.py deliverer.py $RPM_BUILD_ROOT/opt/training/

mkdir $RPM_BUILD_ROOT/opt/training/etc
cp etc/training.cfg.example $RPM_BUILD_ROOT/opt/training/etc/training.cfg.example

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/
cp etc/training.service.example $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/training.service
cp etc/training.delivery.service.example $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/training.delivery.service
cp etc/training.delivery.timer.example $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/training.delivery.timer

%clean
rm -rf $RPM_BUILD_ROOT

%pre
exists=$(getent passwd training > /dev/null)
if [ $? = "0" -a -z "$exists" ]; then
    echo "Using existing user"
else
    useradd --no-create-home \
            --user-group \
            --shell /sbin/nologin \
            --comment "training server" \
            training
    echo "Created new user"
fi

%post
if [ ! -f /opt/training/etc/training.cfg ]; then
    cp /opt/training/etc/training.cfg.example /opt/training/etc/training.cfg
    echo "Created new configuration file"
else
    echo "Using existing configuration file"
fi

if [ ! -f /opt/training/data/body.text ] || [ ! -f /opt/training/data/confirmation.text ] || [! -f /opt/training/data/subject.text]; then
    cp /opt/training/data/body.text.example /opt/training/data/body.text
    cp /opt/training/data/confirmation.text.example /opt/training/data/confirmation.text
    cp /opt/training/data/subject.text.example /opt/training/data/subject.text
    echo "Created new template files"
else
    echo "Using existing template files"
fi

if [ ! -f /opt/training/etc/training.crt ] || [ ! -f /opt/training/etc/training.key ]; then
    /opt/training/misc/generate.sh > /dev/null 2>&1
    mv localhost.crt.example /opt/training/etc/training.crt
    mv localhost.key.example /opt/training/etc/training.key
    echo "Created new certificate and key files"
else
    echo "Using existing certificate and key files"
fi

cd /opt/training/migrations/
db-migrate

%files
%defattr(-,root,root)
%attr(0754, training, training) /opt/training/server.py
%attr(0754, training, training) /opt/training/deliverer.py
%attr(0754, root, root) /opt/training/misc/generate.sh
/opt/training/data/body.text.example
/opt/training/data/confirmation.text.example
/opt/training/data/subject.text.example
/opt/training/etc/training.cfg.example
/opt/training/misc/init.sql
/opt/training/migrations/20140128094940_create_table_trainees.migration
/opt/training/migrations/20140128103530_create_table_tasks.migration
/opt/training/migrations/20140129114932_create_table_confirmations.migration
/opt/training/migrations/20140205112527_add_column_percentage.migration
/opt/training/migrations/20140205114603_add_column_version.migration
/opt/training/migrations/simple-db-migrate.conf
/opt/training/training/__init__.py
/opt/training/training/datastore.py
/opt/training/training/decorators.py
/opt/training/training/deliveryman.py
/opt/training/training/errors.py
/opt/training/training/handlers.py
/opt/training/training/mailman.py
/opt/training/training/report.py
%{_sysconfdir}/systemd/system/training.service
%{_sysconfdir}/systemd/system/training.delivery.service
%{_sysconfdir}/systemd/system/training.delivery.timer

%changelog
* Wed Feb 05 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- Add percentage and version columns

* Mon Feb 03 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- Initial release
