%define	svn	20121124

Summary:	Anyterm Daemon
Name:		anytermd
Version:	1.1.29
Release:	4.%{svn}.1
License:	GPLv2
Group:		System/Servers
URL:		http://anyterm.org
Source0:	http://anyterm.org/download/anyterm-%{version}-%{svn}.tar.bz2
Source1:	anytermd.init
Source2:	anytermd.sysconfig
Patch0:		anyterm-1.1.28-respect-LDFLAGS.patch
BuildRequires:	boost-devel
BuildRequires:	librote-devel
BuildRequires:	mailcap

Requires:	openssl
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper

%description
This is the Anyterm daemon terminal emulator.

%prep
%setup -q -n anyterm-%{version}-%{svn}
%patch0 -p0

cp %{SOURCE1} anytermd.init
cp %{SOURCE2} anytermd.sysconfig

%build
%serverbuild
%make GCC_FLAGS="%{optflags} -pthread -fPIC -D_REENTRANT" LDFLAGS="%{ldflags}"

%install
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

%files
%doc CHANGELOG LICENSE README
%attr(0755,root,root) %{_initrddir}/anytermd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/anytermd
%attr(0755,root,root) %{_sbindir}/anytermd
%attr(0755,anytermd,anytermd) %dir /var/lib/anytermd

