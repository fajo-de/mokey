
Name:		mokey
Version:	1.1.0
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
install -m 0644 -t "$RPM_BUILD_ROOT"/etc/sysconfig			instfiles/mokey.sysconfig
install -m 0640 -t "$RPM_BUILD_ROOT"/etc/mokey				mokey.toml.sample

# install templates
/bin/cp -rdp server/templates "$RPM_BUILD_ROOT"/usr/share/mokey/

# rename some files
mv "$RPM_BUILD_ROOT"/etc/sysconfig/mokey{.sysconfig,}
mv "$RPM_BUILD_ROOT"/etc/mokey/mokey.toml{.sample,}

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
* Mon Jul 14 2025 dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com> - 0.6.5.19+9b59a6ba
- Merge pull request #5 from fajo-de/dependabot/go_modules/golang.org/x/net-0.3
- Bump golang.org/x/net from 0.29.0 to 0.38.0

* Mon Jul 14 2025 dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com> - 0.6.5.17+bb04428b
- Merge pull request #6 from fajo-de/dependabot/go_modules/github.com/redis/go-
- Bump github.com/redis/go-redis/v9 from 9.7.0 to 9.7.3

* Mon Jul 14 2025 dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com> - 0.6.5.15+06a8ee6e
- Merge pull request #4 from fajo-de/dependabot/go_modules/golang.org/x/crypto-
- Bump golang.org/x/crypto from 0.28.0 to 0.35.0

* Mon Jul 14 2025 Andrew E. Bruno <aebruno2@buffalo.edu> - 0.6.5.13+1068fdfb
- Merge remote-tracking branch 'upstream/main'
- Merge pull request #151 from cmd-ntrf/goreleaser (upstream/main)
- Upgrade goreleaser to version 2
- Bump version (tag: v0.6.5)
- Merge pull request #148 from ubccr/fix-92
- Merge pull request #147 from ubccr/bump-deps

* Mon Jul 14 2025 F. John <falk.john@fajo.de> - 0.6.4.13+5d5d6262
- Merge pull request #3 from fajo-de/merge-hide-invalid-username-error
- Merge commit '44cd95e045852d5a94de064bf246cc4c9a4e4eb0' into merge-hide-inval
- Add support for hiding invalid username error.
- Remove erroneous script tag
- Bump deps.
- Update changelog (tag: v0.6.4)
- Update goipa
- Fix static builds
- Upgrade deps
- Merge pull request #138 from ngwilson/update-containers
- Updated docker config to use rocky 9 and cgroup host config

* Mon Jul 14 2025 F. John <falk.john@fajo.de> - 0.6.3.14+338e5767
- Merge pull request #2 from fajo-de/fix-dependancy-vulns
- upgrade vulnerable dependencies - golang.org/x/net v0.38.0 - golang.org/x/cry

* Mon Jul 14 2025 F. John <falk.john@fajo.de> - 0.6.3.12+ecf06ae8
- Merge pull request #1 from fajo-de/add-sample-config
- added sample configuration file (origin/add-sample-config)

* Tue Feb 13 2024 Falk John <falk.john@fajo.de> - 0.6.3.10+af39416b
- - cleanup modules

* Tue Feb 13 2024 Falk John <falk.john@fajo.de> - 0.6.3.9+01642bb2
- - set read/write fiber buffer

* Tue Feb 13 2024 Falk John <falk.john@fajo.de> - 0.6.3.8+55a02c50
- - updated README - added/updated screenshots

* Tue Feb 13 2024 Falk John <falk.john@fajo.de> - 0.6.3.7+1ff16347
- - fork based on ubccr/mokey v0.6.3 - switched to go 1.17 - migrated to use ve

