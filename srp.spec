Summary:	Secure Remote Password protocol
Summary(pl):	ProtokÛ≥ SRP (bezpieczny system autoryzacji)
Name:		srp
Version:	1.5.1
Release:	1
License:	SRP Open Source
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
URL:		http://srp.stanford.edu/srp/
Source0:	http://srp.stanford.edu/srp/%{name}-%{version}.tar.gz
Source1:	%{name}-passwd.pamd
Patch0:		%{name}-1.5.1-base.patch
Patch1:		%{name}-1.5.1-telnetautoconffix.patch
Patch2:		%{name}-libkrypto.patch
Patch3:		%{name}-1.5.1-sharedlibwrap-patch
Patch4:		%{name}-1.5.1-pam_eps.patch
Patch5:		%{name}-1.5.1-pam.patch
BuildRequires:	gmp-devel
BuildRequires:	pam-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SRP stands for the Secure Remote Password protocol, and it represents
a new mechanism for performing password-based authentication and key
exchange over potentially insecure networks. SRP offers both security
and convenience improvements over authentication techniques currently
in use.

%description -l pl
SRP oznacza protokÛ≥ Secure Remote Password i reprezentuje nowy
mechanizm autentyfikacji bazuj±cej na has≥ach oraz wymianÍ kluczy
przez potencjalnie niebezpieczne sieci. SRP oferuje zarÛwno
bezpieczeÒstwo i ulepszenia w stosunku do innych aktualnie dostÍpnych
technik autentyfikacji.

%package lib
Summary:	Shared SRP library
Summary(pl):	WspÛ≥dzielona biblioteka SRP
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	‚…¬Ã…œ‘≈À…
Group(uk):	‚¶¬Ã¶œ‘≈À…

%description lib
Shared SRP library.

%description lib -l pl
WspÛ≥dzielona biblioteka SRP.

%package devel
Summary:	Headers files and development SRP library
Summary(pl):	Pliki nag≥Ûwkowe i biblioteki do programowania
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name}-lib = %{version}

%description devel
Headers files and development SRP library.

%description devel -l pl
Pliki nag≥Ûwkowe i biblioteki SRP.

%package static
Summary:	Static SRP library
Summary(pl):	Biblioteka statyczna SRP
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name}-devel = %{version}

%description static
Static SRP library.

%description static -l pl
Statyczna biblioteka SRP.

%package telnet
Summary:	Telnet client with SRP and IPv6 support 
Summary(pl):	Klient telnetu ze wsparciem dla SRP i IPv6
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Requires:	%{name} = %{version}

%description telnet
Telnet client with Secure Remote Password protocol and IPv6 support.

%description telnet -l pl
Klient telnet ze wsparciem dla protoko≥u Secure Remote Password i
IPv6.

%package telnetd
Summary:	Telnet server with SRP and IPv6 support 
Summary(pl):	Serwer telnetu ze wsparciem dla SRP i IPv6
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}

%description telnetd
Telnet server with Secure Remote Password protocol and IPv6 support.

%description telnetd -l pl
Serwer telnet ze wsparciem dla protoko≥u Secure Remote Password i
IPv6.

%package ftp
Summary:	FTP client with SRP support 
Summary(pl):	Klient FTP ze wsparciem dla SRP
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}

%description ftp
FTP client with Secure Remote Password protocol support.

%description ftp -l pl
Klient FTP ze wsparciem dla protoko≥u Secure Remote Password.

%package ftpd
Summary:	FTP server with SRP support
Summary(pl):	Serwer FTP ze wsparciem dla SRP
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}

%description ftpd
FTP server with Secure Remote Password protocol support.

%description ftpd -l pl
Serwer FTP ze wsparciem dla protoko≥u Secure Remote Password.

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
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,sysconfig}
install %{SOURCE1}			$RPM_BUILD_ROOT/etc/pam.d/passwd.srp
touch $RPM_BUILD_ROOT%{_sysconfdir}/tpasswd
%{__make} install DESTDIR="$RPM_BUILD_ROOT"
mv -f $RPM_BUILD_ROOT/bin/login		$RPM_BUILD_ROOT/bin/login.srp
mv -f $RPM_BUILD_ROOT/bin/su		$RPM_BUILD_ROOT/bin/su.srp
mv -f $RPM_BUILD_ROOT/bin/passwd	$RPM_BUILD_ROOT%{_bindir}/passwd.srp
mv -f $RPM_BUILD_ROOT/bin/tconf		$RPM_BUILD_ROOT%{_sbindir}/tconf

mv -f $RPM_BUILD_ROOT%{_bindir}/ftp	$RPM_BUILD_ROOT%{_bindir}/ftp.srp
mv -f $RPM_BUILD_ROOT%{_bindir}/telnet	$RPM_BUILD_ROOT%{_bindir}/telnet.srp

mv -f $RPM_BUILD_ROOT%{_sbindir}/ftpd	$RPM_BUILD_ROOT%{_sbindir}/ftpd.srp
mv -f $RPM_BUILD_ROOT%{_sbindir}/telnetd $RPM_BUILD_ROOT%{_sbindir}/telnetd.srp

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
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/tpasswd
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
