Summary:	Anyterm Daemon
Name:		anytermd
Version:	1.1.27
Release:	%mkrel 2
License:	GPLv2
Group:		System/Servers
URL:		http://anyterm.org
Source0:	http://anyterm.org/download/anyterm-%{version}.tbz2
Source1:	anytermd.init
Source2:	anytermd.sysconfig
Requires:	openssl
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	boost-devel
BuildRequires:	librote-devel
BuildRequires:	mailcap
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is the Anyterm daemon terminal emulator.

%prep

%setup -q -n anyterm-%{version}

cp %{SOURCE1} anytermd.init
cp %{SOURCE2} anytermd.sysconfig

%build
%serverbuild

pushd daemon
%make GCC_FLAGS="$CFLAGS -pthread -fPIC -D_REENTRANT" OPTIMISE_FLAGS="$CFLAGS -fPIC -D_REENTRANT"
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/lib/anytermd

install -m0755 daemon/anytermd %{buildroot}%{_sbindir}/anytermd
install -m0755 anytermd.init %{buildroot}%{_initrddir}/anytermd
install -m0644 anytermd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/anytermd

%post
%_post_service anytermd

%preun
%_preun_service anytermd

%pre
%_pre_useradd anytermd /var/lib/anytermd /bin/false

%postun
%_postun_userdel anytermd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README
%attr(0755,root,root) %{_initrddir}/anytermd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/anytermd
%attr(0755,root,root) %{_sbindir}/anytermd
%attr(0755,anytermd,anytermd) %dir /var/lib/anytermd

