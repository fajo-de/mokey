
Name:		mokey
Version:	1.0.0
Release:	1%{?dist}
Summary:	User self management for FreeIPA

License:	BSD 3-Clause "New" or "Revised" License
URL:		https://github.com/fajo-de/mokey
Source0:	%{name}-%{version}.tar.gz


%description

%global debug_package %{nil}

%prep
%setup -q -n %{name}

%build
go build -v

%install
# remove old root
rm -rf "$RPM_BUILD_ROOT"

if [ "x$RPM_BUILD_ROOT" = "x" ] ; then
	echo "RPM_BUILD_ROOT not set" >&2
	exit 1
fi

# create directories
install -m 0755 -d "$RPM_BUILD_ROOT"/etc/sysconfig
install -m 0750 -d "$RPM_BUILD_ROOT"/etc/mokey
install -m 0750 -d "$RPM_BUILD_ROOT"/etc/mokey/private
install -m 0755 -d "$RPM_BUILD_ROOT"/usr/bin
install -m 0755 -d "$RPM_BUILD_ROOT"/usr/share/mokey
install -m 0755 -d "$RPM_BUILD_ROOT"/usr/share/mokey/templates
install -m 0755 -d "$RPM_BUILD_ROOT"/usr/share/mokey/templates/email
install -m 0755 -d "$RPM_BUILD_ROOT"/usr/share/mokey/templates/static
install -m 0755 -d "$RPM_BUILD_ROOT"/usr/lib/systemd/system

# install files and directories
install -m 0755 -t "$RPM_BUILD_ROOT"/usr/bin				-s mokey
install -m 0644 -t "$RPM_BUILD_ROOT"/usr/lib/systemd/system		instfiles/mokey.service
install -m 0755 -t "$RPM_BUILD_ROOT"/etc/sysconfig			instfiles/mokey.sysconfig
install -m 0640 -t "$RPM_BUILD_ROOT"/etc/mokey				mokey.toml

# install templates
/bin/cp -rdp server/templates "$RPM_BUILD_ROOT"/usr/share/mokey/

# rename some files
mv "$RPM_BUILD_ROOT"/etc/sysconfig/mokey{.sysconfig,}

# change permissions on the templates
find "$RPM_BUILD_ROOT"/usr/share/mokey -type f -exec /bin/chmod 0644 {} \;
 
%files
%license LICENSE
%doc README.md AUTHORS NOTICE
%attr(0750,root,mokey) /etc/mokey
%attr(0750,root,mokey) /etc/mokey/private
%config(noreplace) /etc/mokey/mokey.toml
%config(noreplace) /etc/sysconfig/mokey
/usr/bin/*
/usr/lib/systemd/system/*
/usr/share/mokey

%pre

if ! getent passwd mokey >/dev/null ; then
	groupadd -r mokey
	useradd  -r -g mokey -d /var/lib/mokey -m -s /sbin/nologin -c "Mokey service" mokey
	chmod 0750 /var/lib/mokey
fi

%post

if   [ $1 == 1 ] ; then
	# fresh installation
	systemctl daemon-reload ||:
	chown -Rh root:mokey /etc/mokey/mokey.toml
elif [ $1 == 2 ] ; then
	# update
	systemctl daemon-reload ||:
	systemctl try-restart mokey.service ||:
fi

%preun

if   [ $1 == 0 ] ; then
	# removal
	systemctl disable --now mokey.service ||:
elif [ $1 == 1 ] ; then
	# downgrade
	systemctl daemon-reload ||:
	systemctl try-restart mokey.service ||:
fi

%postun

systemctl daemon-reload ||:

%changelog
* Tue Feb 13 2024 Falk John <falk.john@fajo.de> - 1.0.0-1
- initial release

