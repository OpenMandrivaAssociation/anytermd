Summary:	Anyterm Daemon
Name:		anytermd
Version:	1.1.29
Release:	%mkrel 3
License:	GPLv2
Group:		System/Servers
URL:		http://anyterm.org
Source0:	http://anyterm.org/download/anyterm-%{version}.tbz2
Source1:	anytermd.init
Source2:	anytermd.sysconfig
Patch0:		anyterm-1.1.28-respect-LDFLAGS.patch
Patch1:		anyterm-1.1.29-gcc-4.4.patch
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
%patch0 -p0
%patch1 -p0

cp %{SOURCE1} anytermd.init
cp %{SOURCE2} anytermd.sysconfig

%build
%serverbuild

%make GCC_FLAGS="%optflags -pthread -fPIC -D_REENTRANT" LDFLAGS="%ldflags"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/lib/anytermd

install -m0755 anytermd %{buildroot}%{_sbindir}/anytermd
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
