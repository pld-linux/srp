# TODO: everything
Summary:	Secure Remote Password protocol
Summary(pl.UTF-8):	Protokół SRP (bezpieczny system autoryzacji)
Name:		srp
Version:	2.1.1
Release:	0.2
License:	SRP Open Source
Group:		Applications/Networking
Source0:	http://srp.stanford.edu/source/%{name}-%{version}.tar.gz
# Source0-md5:	23e843f3e35927fa8613edd7e4265c71
Patch0:		%{name}-shared.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-cflags.patch
URL:		http://srp.stanford.edu/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pam >= 0.77.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SRP stands for the Secure Remote Password protocol, and it represents
a new mechanism for performing password-based authentication and key
exchange over potentially insecure networks. SRP offers both security
and convenience improvements over authentication techniques currently
in use.

%description -l pl.UTF-8
SRP oznacza protokół Secure Remote Password i reprezentuje nowy
mechanizm autentyfikacji bazującej na hasłach oraz wymianę kluczy
przez potencjalnie niebezpieczne sieci. SRP oferuje zarówno
bezpieczeństwo i ulepszenia w stosunku do innych aktualnie dostępnych
technik autentyfikacji.

%package libs
Summary:	Shared SRP libraries
Summary(pl.UTF-8):	Współdzielone biblioteki SRP
Group:		Libraries

%description libs
Shared SRP libraries.

%description libs -l pl.UTF-8
Współdzielone biblioteki SRP.

%package devel
Summary:	Headers files for SRP libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek SRP
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	openssl-devel

%description devel
Headers files for SRP libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek SRP.

%package static
Summary:	Static SRP libraries
Summary(pl.UTF-8):	Statyczne biblioteki SRP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SRP libraries.

%description static -l pl.UTF-8
Statyczne biblioteki SRP.

%package telnet
Summary:	Telnet client with SRP and IPv6 support
Summary(pl.UTF-8):	Klient protokołu telnet ze wsparciem dla SRP i IPv6
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description telnet
Telnet client with Secure Remote Password protocol and IPv6 support.

%description telnet -l pl.UTF-8
Klient protokołu telnet ze wsparciem dla protokołu Secure Remote
Password i IPv6.

%package telnetd
Summary:	Telnet server with SRP and IPv6 support
Summary(pl.UTF-8):	Serwer protokołu telnet ze wsparciem dla SRP i IPv6
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description telnetd
Telnet server with Secure Remote Password protocol and IPv6 support.

%description telnetd -l pl.UTF-8
Serwer protokołu telnet ze wsparciem dla protokołu Secure Remote
Password i IPv6.

%package ftp
Summary:	FTP client with SRP support
Summary(pl.UTF-8):	Klient FTP ze wsparciem dla SRP
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description ftp
FTP client with Secure Remote Password protocol support.

%description ftp -l pl.UTF-8
Klient FTP ze wsparciem dla protokołu Secure Remote Password.

%package ftpd
Summary:	FTP server with SRP support
Summary(pl.UTF-8):	Serwer FTP ze wsparciem dla SRP
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description ftpd
FTP server with Secure Remote Password protocol support.

%description ftpd -l pl.UTF-8
Serwer FTP ze wsparciem dla protokołu Secure Remote Password.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd libsrp
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../libkrypto
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../telnet
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../ftp
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
automake -a -c --foreign
cd ../base
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
automake -a -c --foreign
cd ..
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	LIBTERM="-ltinfo" \
	MAILSPOOL=/var/mail \
	MAILFILE=Mail \
	UTMPDIR=/var/run \
	WTMPDIR=/var/log \
	FAILLOGDIR=/var/log \
	LASTLOGDIR=/var/log \
	--enable-shadowgrp \
	--with-cast \
	--with-engine \
	--with-libcrack \
	--with-openssl \
	--with-pam \
	--with-srp \
	--with-zlib

	# --with-inet6  - requires non-existing "support.h" in telnet/telnet/commands.c
	# ??? [needs check] PAM support in passwd.srp is broken (it probably
	# doesn't use pass specified by user.
	# --with-spx	- SPX requires kerberos ;-(
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{pam.d,rc.d/init.d,sysconfig},/bin,/sbin}

#install %{SOURCE1}			$RPM_BUILD_ROOT/etc/pam.d/passwd.srp
touch $RPM_BUILD_ROOT%{_sysconfdir}/tpasswd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SECUREDIR=/%{_lib}/security \
	FAKEROOT=$RPM_BUILD_ROOT \
	suidbins= \
	suidubins=

install base/src/su $RPM_BUILD_ROOT/bin/su
install base/src/passwd $RPM_BUILD_ROOT%{_bindir}/passwd

mv -f $RPM_BUILD_ROOT/bin/su		$RPM_BUILD_ROOT/bin/su.srp
mv -f $RPM_BUILD_ROOT%{_bindir}/login	$RPM_BUILD_ROOT/bin/login.srp
mv -f $RPM_BUILD_ROOT%{_bindir}/passwd	$RPM_BUILD_ROOT%{_bindir}/passwd.srp
mv -f $RPM_BUILD_ROOT%{_bindir}/tconf	$RPM_BUILD_ROOT%{_sbindir}/tconf

mv -f $RPM_BUILD_ROOT%{_bindir}/ftp	$RPM_BUILD_ROOT%{_bindir}/ftp.srp
mv -f $RPM_BUILD_ROOT%{_bindir}/telnet	$RPM_BUILD_ROOT%{_bindir}/telnet.srp

mv -f $RPM_BUILD_ROOT%{_sbindir}/ftpd	$RPM_BUILD_ROOT%{_sbindir}/ftpd.srp
mv -f $RPM_BUILD_ROOT%{_sbindir}/telnetd $RPM_BUILD_ROOT%{_sbindir}/telnetd.srp

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/* inst/INSTALL*
%attr(755,root,root) /bin/login.srp
%attr(4755,root,root) /bin/su.srp
%attr(755,root,root) %{_sbindir}/tconf
%attr(4755,root,root) %{_bindir}/passwd.srp
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tpasswd
#%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/*
# Pam modules are required by main srp package so we don't split them
%attr(4755,root,root) /sbin/eps_chkpwd
%attr(755,root,root) /%{_lib}/security/pam_eps_*.so

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files telnet
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/telnet.srp

%files telnetd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/telnetd.srp

%files ftp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ftp.srp

%files ftpd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ftpd.srp
