# TODO:
# 	- conditional build with motiff
#	- .so binaries should be removed and linked with PLD one...
#	  (we really need them here?)

%define		_buildid	200307181617
%define		_ver		3.0
%define		_milestone	M2
%define		_buildname	%{_ver}%{_milestone}

Summary:	eclipse
Summary(pl):	eclipse
Name:		eclipse
Version:	%{_ver}
Release:	0.%{_milestone}.1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.eclipse.ps.pl/downloads/drops/S-%{_buildname}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_buildname}.zip
# Source0-md5:	12c9b31cf8605e58cf857715ac6ff5c3
Source1:	%{name}.desktop
URL:		http://www.eclipse.org/
Obsoletes:	eclipse-SDK
BuildRequires:	jdk
BuildRequires:	unzip
BuildRequires:	jakarta-ant >= 1.4
BuildRequires:	gtk+2-devel
Requires:	jdk
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	/usr/share/java

%description

%description -l pl

%prep
%setup -q -c

%build
JAVA_HOME=/usr/lib/java
export JAVA_HOME
./build -os linux -ws gtk -arch x86 -target compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_bindir},%{_datadir}/%{name}}

./build -os linux -ws gtk -arch x86 -target install

unzip result/linux-gtk-x86-sdk.zip -d $RPM_BUILD_ROOT%{_datadir}
install %{SOURCE1} %{_desktopdir}

#wrapper
install -d $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/eclipse << EOF
#!/bin/sh
%{_datadir}/%{name}/eclipse 
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eclipse
%attr(755,root,root) %{_datadir}/%{name}/eclipse
%{_desktopdir}/eclipse.desktop
%{_datadir}/%{name}
