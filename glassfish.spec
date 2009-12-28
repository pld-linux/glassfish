#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%include	/usr/lib/rpm/macros.java

Summary:	JavaEE 6 aplication server
Name:		glassfish
Version:	3
Release:	0.1
License:	GPL
Group:		Libraries/Java
# Source0:	http://download.java.net/glassfish/v3/release/glassfish-v3.zip
Source0:	%{name}-v%{version}.zip
# NoSource0-md5:	537b1c6574316ebc4dc69ba6dd26e213
NoSource:	0
Source1:	%{name}
Source2:	%{name}.init
URL:		https://glassfish.dev.java.net/
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-sun-jre >= 1.6.0.17
Provides:	group(glassfish)
Provides:	user(glassfish)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Glassfish is lightweight, flexible, and open-source java application server.
It is full implementation of JavaEE 6.

%prep
%setup -q -n %{name}v%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sysconfdir}/%{name},/etc/rc.d/init.d,%{_sbindir},/var/lib/%{name}/domains}

cp -a glassfish/{bin,lib,modules,osgi} $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a glassfish/config/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -a glassfish/domains/* $RPM_BUILD_ROOT/var/lib/%{name}/domains

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

sed -i 's,@DATADIR@,%{_datadir},' $RPM_BUILD_ROOT%{_sbindir}/%{name}

ln -s %{_sysconfdir}/%{name} $RPM_BUILD_ROOT%{_datadir}/%{name}/config
ln -s /var/lib/%{name}/domains $RPM_BUILD_ROOT%{_datadir}/%{name}/domains

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 244 %{name}
%useradd -u 244 -d /var/lib/%{name} -g %{name} -c "Glassfish user" %{name}

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc glassfish/docs glassfish/legal
%{_datadir}/%{name}
%dir %config(noreplace) %attr(770,root,glassfish) %verify(not md5 mtime size) %{_sysconfdir}/%{name}
%config(noreplace) %attr(660,root,glassfish) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%defattr(660,root,glassfish,770)
/var/lib/%{name}
