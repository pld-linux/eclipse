#
%define		_buildid	200406251208
%define		_ver_major	3.0
%define		_ver_minor	0
%define		_buildname	%{_ver_major}
#
Summary:	Eclipse - an open extensible IDE
Summary(pl):	Eclipse - otwarte, rozszerzalne ¶rodowisko programistyczne
Name:		eclipse
Version:	%{_ver_major}
Release:	1.1
License:	Common Public Licence
Group:		Development/Tools
Source0:	http://download2.eclipse.org/downloads/drops/R-%{_buildname}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_buildname}.zip
# Source0-md5:	962a41fe062f0ddc809ca956687c7e01
Source1:	%{name}.desktop
Patch0:		%{name}-swt-makefile.patch
URL:		http://www.eclipse.org/
BuildRequires:	jakarta-ant >= 1.6.1
BuildRequires:	jdk >= 1.4
BuildRequires:	libgnomeui-devel
%ifnarch amd64
BuildRequires:	mozilla-devel
%endif
BuildRequires:	unzip
BuildRequires:	zip
Requires:	jakarta-ant
Requires:	jdk
Obsoletes:	eclipse-SDK
ExclusiveArch:	%{ix86} ppc amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	/usr/share/java
%define		_eclipse_arch	%(echo %{_target_cpu} | sed 's/i.86/x86/;s/athlon/x86/;s/pentium./x86/')

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
./build -os linux -ws gtk -arch %{_eclipse_arch} -target compile

%ifarch amd64
%define	_swtsrcdir	plugins/org.eclipse.swt.gtk64/ws/gtk
%else
%define	_swtsrcdir	plugins/org.eclipse.swt.gtk/ws/gtk
%endif
rm -rf swt
mkdir swt && cd swt
unzip -x %{_builddir}/%{name}-%{version}/%{_swtsrcdir}/swtsrc.zip
unzip -x %{_builddir}/%{name}-%{version}/%{_swtsrcdir}/swt-pisrc.zip
unzip -x %{_builddir}/%{name}-%{version}/%{_swtsrcdir}/swt-mozillasrc.zip
ln -sf library/xpcom.cpp xpcom.cpp
patch -p0 < %{PATCH0}
%ifnarch amd64
%{__make} -f make_gtk.mak all \
%else
# amd64: mozilla disabled
%{__make} -f make_gtk.mak all64 \
%endif
    OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_bindir},%{_datadir}/%{name}}

./build -os linux -ws gtk -arch %{_eclipse_arch} -target install

unzip result/linux-gtk-%{_eclipse_arch}-sdk.zip -d $RPM_BUILD_ROOT%{_datadir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

#wrapper
install -d $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/eclipse << EOF
#!/bin/sh
exec %{_datadir}/%{name}/eclipse \$*
EOF

cd swt
install libswt-{atk-gtk,awt-gtk,gnome-gtk,gtk,pi-gtk}-*.so \
    $RPM_BUILD_ROOT%{_datadir}/eclipse/plugins/org.eclipse.swt.gtk_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}
%ifnarch
install libswt-mozilla-gtk-*.so \
    $RPM_BUILD_ROOT%{_datadir}/eclipse/plugins/org.eclipse.swt.gtk_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}
%endif

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
