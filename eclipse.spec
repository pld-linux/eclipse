# TODO:
# 	- conditional build with motif
#	- .so binaries should be removed and linked with PLD one...
#	  (we really need them here?)

%define		_buildid	200405211200
%define		_ver		3.0
%define		_milestone	M9
%define		_buildname	%{_ver}%{_milestone}

Summary:	eclipse - an open extensible IDE
Summary(pl):	eclipse - otwarte, rozszerzalne ¶rodowisko programistyczne
Name:		eclipse
Version:	%{_ver}
Release:	0.%{_milestone}.1
License:	Common Public Licence
Group:		Development/Tools
Source0:	http://download2.eclipse.org/downloads/drops/S-%{_buildname}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_buildname}.zip
# Source0-md5:	8213743eaa68db847019f88a5b441c40
Source1:	%{name}.desktop
URL:		http://www.eclipse.org/
BuildRequires:	jdk
BuildRequires:	unzip
BuildRequires:	zip
BuildRequires:	jakarta-ant >= 1.4
BuildRequires:	gtk+2-devel
Requires:	jdk
Requires:	jakarta-ant
Obsoletes:	eclipse-SDK
#BuildArch:	noarch
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	/usr/share/java

%description
Eclipse is a kind of universal tool platform - an open extensible IDE
for anything and nothing in particular.

%description -l pl
Eclipse to rodzaj uniwersalnej platformy narzêdziowej - otwarte,
rozszerzalne IDE (zintegrowane ¶rodowisko programistyczne) do
wszystkiego i niczego w szczególno¶ci.

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
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

#wrapper
install -d $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/eclipse << EOF
#!/bin/sh
exec %{_datadir}/%{name}/eclipse \$*
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eclipse
%attr(755,root,root) %{_datadir}/%{name}/eclipse
%{_desktopdir}/eclipse.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/.[!.]*
%{_datadir}/%{name}/[!e]*
