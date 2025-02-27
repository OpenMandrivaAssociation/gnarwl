%define name gnarwl
%define sname damnit
%define version 3.6
%define mansec 8
%define homedir /var/lib/%{name}
%define useradd_prg /usr/sbin/useradd
%define useradd_arg -r -s /bin/false -c "Email autoreply agent" -d %{homedir} %{name}


Name: %{name}
Summary: An email autoresponder with LDAP support
Version: %{version}
Release: %mkrel 1
License: GPL
Group: System/Servers
Source: %{name}-%{version}.tgz
BuildRequires: libgdbm-devel, libldap-devel, groff
BuildRoot: %_tmppath/%{name}-%{version}-buildroot
URL: https://www.oss.billiton.de/

%description
Gnarwl is an email autoresponder, intended to be a successor to the old
vacation(1) program. With gnarwl users are no longer required to have
full blown system accounts, but may store their autoreply text compfortably
within an LDAP database.


%prep

%setup

%build
./configure --prefix=/usr --sysconfdir=%{_sysconfdir} --with-homedir=%{homedir}
make

%install
%__rm -rf $RPM_BUILD_ROOT
%__mkdir -p $RPM_BUILD_ROOT/%{_bindir}
%__mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
%__mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man%{mansec}
%__mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
%__mkdir -p $RPM_BUILD_ROOT/%{homedir}/block
%__mkdir -p $RPM_BUILD_ROOT/%{homedir}/bin
%__cp src/%{name} $RPM_BUILD_ROOT/%{_bindir}
%__cp src/%{sname} $RPM_BUILD_ROOT/%{_sbindir}
%__cp data/header.txt $RPM_BUILD_ROOT/%{homedir}
%__cp data/footer.txt $RPM_BUILD_ROOT/%{homedir}
%__cp data/gnarwl.cfg $RPM_BUILD_ROOT/%{_sysconfdir}
%__strip $RPM_BUILD_ROOT/%{_bindir}/%{name}
%__strip $RPM_BUILD_ROOT/%{_sbindir}/%{sname}
echo \|%{_bindir}/%{name} > $RPM_BUILD_ROOT/%{homedir}/.forward 
cat data/badheaders.txt | src/%{sname} -a $RPM_BUILD_ROOT/%{homedir}/badheaders.db
cat data/blacklist.txt | src/%{sname} -a $RPM_BUILD_ROOT/%{homedir}/blacklist.db

%files
%defattr(0644,root,root)
%doc doc/FAQ
%doc doc/INSTALL
%doc doc/LICENSE
%doc doc/AUTHORS 
%doc doc/HISTORY 
%doc doc/README
%doc doc/README.upgrade
%doc doc/ISPEnv.schema 
%doc doc/ISPEnv2.schema 
%doc doc/example.ldif
%defattr(0755,root,root)
%{_bindir}/%{name}
%{_sbindir}/%{sname}
%defattr(-,gnarwl,root)
%{homedir}
%defattr(0400,gnarwl,root)
%config %{_sysconfdir}/%{name}.cfg

%clean
%__rm -rf $RPM_BUILD_ROOT

%pre
if ! %__grep %{name} /etc/passwd > /dev/null; then
  echo "Creating system account \"%{name}\"" ;
  %{useradd_prg} %{useradd_arg} ;
fi
