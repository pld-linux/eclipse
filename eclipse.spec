#
%define		_buildid	200406251208
%define		_ver_major	3.0
%define		_ver_minor	0
%define		_ver		%{_ver_major}.%{_ver_minor}
#
Summary:	Eclipse - an open extensible IDE
Summary(pl):	Eclipse - otwarte, rozszerzalne ¶rodowisko programistyczne
Name:		eclipse
Version:	%{_ver_major}
Release:	1.2
License:	CPL v1.0
Group:		Development/Tools
Source0:	http://download2.eclipse.org/downloads/drops/R-%{_ver_major}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_ver_major}.zip
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
JAVA_HOME=%{_prefix}/lib/java
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
%{_datadir}/%{name}/.eclipseproduct
%{_datadir}/%{name}/configuration
%{_datadir}/%{name}/icon.xpm
%{_datadir}/%{name}/notice.html
%{_datadir}/%{name}/readme
%{_datadir}/%{name}/startup.jar

# features
%{_datadir}/%{name}/features/org.eclipse.jdt_%{_ver}
%{_datadir}/%{name}/features/org.eclipse.jdt.source_%{_ver}
%{_datadir}/%{name}/features/org.eclipse.pde_%{_ver}
%{_datadir}/%{name}/features/org.eclipse.pde.source_%{_ver}
%{_datadir}/%{name}/features/org.eclipse.platform_%{_ver}
%{_datadir}/%{name}/features/org.eclipse.platform.source_%{_ver}
%{_datadir}/%{name}/features/org.eclipse.sdk_%{_ver}

# plugins
%{_datadir}/%{name}/plugins/org.apache.ant_1.6.1
%{_datadir}/%{name}/plugins/org.apache.lucene_1.3.0
%{_datadir}/%{name}/plugins/org.eclipse.ant.core_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ant.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.compare_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.core.boot_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.core.expressions_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.core.filebuffers_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.core.resources_%{_ver}

%dir %{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux_%{_ver}/fragment.xml
# todo: native version
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux_%{_ver}/os/linux/%{_eclipse_arch}/libcore_2_1_0b.so

%{_datadir}/%{name}/plugins/org.eclipse.core.runtime_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.core.runtime.compatibility_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.core.variables_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.debug.core_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.debug.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.help_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.help.appserver_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.help.base_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.help.ide_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.help.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.help.webapp_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.core_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.debug_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.debug.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.doc.isv_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.doc.user_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.junit_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.junit.runtime_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.launching_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.source_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jdt.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jface_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.jface.text_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ltk.core.refactoring_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ltk.ui.refactoring_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.osgi_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.osgi.services_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.osgi.util_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.pde_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.pde.build_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.pde.core_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.pde.doc.user_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.pde.junit.runtime_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.pde.runtime_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.pde.source_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.pde.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.platform_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.platform.doc.isv_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.platform.doc.user_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.platform.source_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.platform.source.linux.gtk.%{_eclipse_arch}_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.sdk_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.search_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.swt_%{_ver}

%dir %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/META-INF/MANIFEST.MF
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/about.html
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/cpl-v10.html
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/fragment.properties
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/fragment.xml
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/lgpl-v21.txt
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/mpl-v11.txt
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/os/linux/%{_eclipse_arch}/libswt-atk-gtk-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/os/linux/%{_eclipse_arch}/libswt-awt-gtk-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/os/linux/%{_eclipse_arch}/libswt-gnome-gtk-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/os/linux/%{_eclipse_arch}/libswt-gtk-*.so
%ifnarch amd64
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/os/linux/%{_eclipse_arch}/libswt-mozilla-gtk-*.so
%endif
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/os/linux/%{_eclipse_arch}/libswt-pi-gtk-*.so
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/ws/gtk/swt-mozilla.jar
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/ws/gtk/swt-pi.jar
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_%{_ver}/ws/gtk/swt.jar

%{_datadir}/%{name}/plugins/org.eclipse.team.core_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.core_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.ssh2_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.ssh_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.team.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.text_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.tomcat_4.1.30
%{_datadir}/%{name}/plugins/org.eclipse.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.cheatsheets_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.console_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.editors_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.externaltools_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.forms_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.ide_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.intro_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.presentations.r21_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.views_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.workbench_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.workbench.compatibility_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.ui.workbench.texteditor_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.update.configurator_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.update.core_%{_ver}

%dir %{_datadir}/%{name}/plugins/org.eclipse.update.core.linux_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.update.core.linux_%{_ver}/about.html
%{_datadir}/%{name}/plugins/org.eclipse.update.core.linux_%{_ver}/fragment.xml
# todo: native version
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.update.core.linux_%{_ver}/os/linux/%{_eclipse_arch}/libupdate.so

%{_datadir}/%{name}/plugins/org.eclipse.update.scheduler_%{_ver}
%{_datadir}/%{name}/plugins/org.eclipse.update.ui_%{_ver}
%{_datadir}/%{name}/plugins/org.junit_3.8.1
