Summary:	Secure Remote Password protocol
Summary(pl):	Protokó³ SRP (bezpieczny system autoryzacji).
Name:		srp
Version:	1.5.1
Release:	1
License:	SRP Open Source
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
URL:		http://srp.stanford.edu/srp/
Source0:	http://srp.stanford.edu/srp/%{name}-%{version}.tar.gz
Source1:	srp-passwd.pamd
Patch0:		srp-1.5.1-base.patch
Patch1:		srp-1.5.1-telnetautoconffix.patch
Patch2:		srp-libkrypto.patch
Patch3:		srp-1.5.1-sharedlibwrap-patch
Patch4:		srp-1.5.1-pam_eps.patch
Patch5:		srp-1.5.1-pam.patch
BuildRequires:	gmp-devel
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SRP stands for the Secure Remote Password protocol, and it represents a new
mechanism for performing password-based authentication and key exchange over
potentially insecure networks.  SRP offers both security and convenience
improvements over authentication techniques currently in use.

%description -l pl
SRP oznacza protokó³ Secure Remote Password i reprezentuje nowy mechanizm
autentyfikacji bazuj±cej na has³ach oraz wymianê kluczy przez potencjalnie
niebezpieczne sieci. SRP oferuje zarówno bezpieczeñstwo i ulepszenia
w stosunku do innych aktualnie dostêpnych technik autentyfikacji.

%package lib
Summary:        Shared SRP library.
Summary(pl):    Wspó³dzielona biblioteka SRP.
Group:          Libraries
Group(pl):      Biblioteki

%description lib
Shared SRP library.

%description lib -l pl
Wspó³dzielona biblioteka SRP.

%package devel
Summary:        Headers files and development SRP library.
Summary(pl):    Pliki nag³ówkowe i biblioteki do programowania
Group:          Development/Libraries
Group(pl):      Programowanie/Biblioteki
Requires:       srp-lib = %{version}

%description devel
Headers files and development SRP library.

%description devel -l pl
Pliki nag³ówkowe i biblioteki SRP.

%package static
Summary:        Static SRP library
Summary(pl):    Biblioteka statyczna SRP
Group:          Development/Libraries
Group(pl):      Programowanie/Biblioteki
Requires:       srp-devel = %{version}

%description static
Static SRP library.

%description -l pl static
Statyczna biblioteka SRP.

%package telnet
Summary:	Telnet client with SRP and IPv6 support 
Summary(pl):	Klient telnetu ze wsparciem dla SRP i IPv6.
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Obsoletes:	srp-telnet < %{version}, srp-telnet > %{version}
Requires:	%{name} = %{version}

%description telnet
Telnet client with Secure Remote Password protocol and IPv6 support.

%description telnet -l pl
Klient telnet ze wsparciem dla protoko³u Secure Remote Password i IPv6.

%package telnetd
Summary:	Telnet server with SRP and IPv6 support 
Summary(pl):	Serwer telnetu ze wsparciem dla SRP i IPv6.
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Obsoletes:	srp-telnetd < %{version}, srp-telnetd > %{version}
Requires:	srp

%description telnetd
Telnet server with Secure Remote Password protocol and IPv6 support.

%description telnetd -l pl
Serwer telnet ze wsparciem dla protoko³u Secure Remote Password i IPv6.

%package ftp
Summary:	FTP client with SRP support 
Summary(pl):	Klient FTP ze wsparciem dla SRP.
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Obsoletes:	srp-ftp < %{version}, srp-ftp > %{version}

%description ftp
FTP client with Secure Remote Password protocol support.

%description -l pl ftp
Klient FTP ze wsparciem dla protoko³u Secure Remote Password.

%package ftpd
Summary:	FTP server with SRP support. 
Summary(pl):	Serwer FTP ze wsparciem dla SRP.
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Obsoletes:	srp-ftpd < %{version}, srp-ftpd > %{version}
Requires:	srp

%description ftpd
FTP server with Secure Remote Password protocol support.

%description -l pl ftpd
Serwer FTP ze wsparciem dla protoko³u Secure Remote Password.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
for directory in base libkrypto libsrp telnet; do
 cd $directory && libtoolize -c -f; aclocal && autoheader \
 	       && autoconf && automake; cd ..
done
aclocal && autoheader && autoconf && automake
%configure \
	--with-inet6 \
	--with-srp \
	--with-cast \
	--with-libcrack
	# PAM support in passwd.srp is broken (it probably
	# doesn't use pass specified by user.
	# --with-libpam
	# PLD still doesn't have des library !
	# --with-des
	# This library can be used instead of gmp
	#  --with-cryptolib
	# SPX requires kerberos ;-(
	# --with-spx
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,sysconfig}
install %{SOURCE1}		$RPM_BUILD_ROOT/etc/pam.d/passwd.srp
touch				$RPM_BUILD_ROOT/etc/tpasswd
%{__make} install	       DESTDIR="$RPM_BUILD_ROOT"
mv $RPM_BUILD_ROOT/bin/login	$RPM_BUILD_ROOT/bin/login.srp
mv $RPM_BUILD_ROOT/bin/su	$RPM_BUILD_ROOT/bin/su.srp
mv $RPM_BUILD_ROOT/bin/passwd	$RPM_BUILD_ROOT%{_bindir}/passwd.srp
mv $RPM_BUILD_ROOT/bin/tconf	$RPM_BUILD_ROOT%{_sbindir}/tconf

mv $RPM_BUILD_ROOT%{_bindir}/ftp	$RPM_BUILD_ROOT%{_bindir}/ftp.srp
mv $RPM_BUILD_ROOT%{_bindir}/telnet     $RPM_BUILD_ROOT%{_bindir}/telnet.srp

mv $RPM_BUILD_ROOT%{_sbindir}/ftpd      $RPM_BUILD_ROOT%{_sbindir}/ftpd.srp
mv $RPM_BUILD_ROOT%{_sbindir}/telnetd   $RPM_BUILD_ROOT%{_sbindir}/telnetd.srp

gzip -9nf docs/* inst/INSTALL*

%clean
rm -rf $RPM_BUILD_ROOT

%post   lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{srp.ps,draft*}.gz inst/INSTALL*
%attr( 755,root,root) /bin/login.srp
%attr(4755,root,root) /bin/su.srp
%attr(755,root,root)  %{_sbindir}/tconf
%attr(4755,root,root) %{_bindir}/passwd.srp
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/tpasswd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/*
# Pam modules are required by main srp package so we don't split them
%attr(755,root,root) /lib/security/*.so

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
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
