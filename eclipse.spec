#
%define		_buildid	200408122000
%define		_ver_major	3.1
%define		_ver_minor	0
%define		_ver		%{_ver_major}.%{_ver_minor}
#
Summary:	Eclipse - an open extensible IDE
Summary(pl):	Eclipse - otwarte, rozszerzalne ¶rodowisko programistyczne
Name:		eclipse
Version:	%{_ver_major}
Release:	0.M1_%{_buildid}.1
License:	CPL v1.0
Group:		Development/Tools
Source0:	http://download.eclipse.org/downloads/drops/S-%{_ver_major}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_ver_major}M1.zip
# Source0-md5:	e2ed08cb88adc0262086a77c96ffa2b2
Source1:	%{name}.desktop
Patch0:		%{name}-swt-makefile.patch
Patch1:		%{name}-core_resources-makefile.patch
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
Requires:	jdk >= 1.4
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
%patch1 -p1

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
cd -

JAVA_INC="-I$JAVA_HOME/include -I$JAVA_HOME/include/linux"

%{__make} -C plugins/org.eclipse.core.resources.linux/src \
    CFLAGS="%{rpmcflags}" \
    LDFLAGS="%{rpmldflags}" \
    INC_PATH="$JAVA_INC"
mv plugins/org.eclipse.core.resources.linux/{src/libcore*.so,os/linux/%{_eclipse_arch}}

cd plugins/org.eclipse.update.core.linux/src
%{__cc} %{rpmcflags} %{rpmldflags} -I. $JAVA_INC update.c -o libupdate.so -shared
mv libupdate.so ../os/linux/%{_eclipse_arch}
cd -

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
%ifnarch amd64
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
%{_datadir}/%{name}/features/org.eclipse.jdt_*.*.*
%{_datadir}/%{name}/features/org.eclipse.jdt.source_*.*.*
%{_datadir}/%{name}/features/org.eclipse.pde_*.*.*
%{_datadir}/%{name}/features/org.eclipse.pde.source_*.*.*
%{_datadir}/%{name}/features/org.eclipse.platform_*.*.*
%{_datadir}/%{name}/features/org.eclipse.platform.source_*.*.*
%{_datadir}/%{name}/features/org.eclipse.sdk_*.*.*

# plugins
%{_datadir}/%{name}/plugins/org.apache.ant_*.*.*
%{_datadir}/%{name}/plugins/org.apache.lucene_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ant.core_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ant.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.compare_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.core.boot_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.core.expressions_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.core.filebuffers_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.core.resources_*.*.*

%dir %{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*/fragment.xml
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*/os/linux/%{_eclipse_arch}/libcore_2_1_0b.so
%{_datadir}/%{name}/plugins/org.eclipse.core.runtime_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.core.runtime.compatibility_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.core.variables_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.debug.core_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.debug.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.help_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.help.appserver_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.help.base_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.help.ide_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.help.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.help.webapp_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.core_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.debug_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.debug.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.doc.isv_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.doc.user_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.junit_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.junit.runtime_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.launching_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.source_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jdt.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jface_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.jface.text_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ltk.core.refactoring_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ltk.ui.refactoring_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.osgi_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.osgi.services_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.osgi.util_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.pde_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.pde.build_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.pde.core_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.pde.doc.user_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.pde.junit.runtime_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.pde.runtime_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.pde.source_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.pde.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.platform_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.platform.doc.isv_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.platform.doc.user_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.platform.source_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.platform.source.linux.gtk.%{_eclipse_arch}_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.sdk_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.search_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.swt_*.*.*

%dir %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/META-INF/MANIFEST.MF
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/about.html
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/cpl-v10.html
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/fragment.properties
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/fragment.xml
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/lgpl-v21.txt
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/mpl-v11.txt
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/os/linux/%{_eclipse_arch}/libswt-atk-gtk-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/os/linux/%{_eclipse_arch}/libswt-awt-gtk-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/os/linux/%{_eclipse_arch}/libswt-gnome-gtk-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/os/linux/%{_eclipse_arch}/libswt-gtk-*.so
%ifnarch amd64
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/os/linux/%{_eclipse_arch}/libswt-mozilla-gtk-*.so
%endif
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/os/linux/%{_eclipse_arch}/libswt-pi-gtk-*.so
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/ws/gtk/swt-mozilla.jar
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/ws/gtk/swt-pi.jar
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk_*.*.*/ws/gtk/swt.jar

%{_datadir}/%{name}/plugins/org.eclipse.team.core_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.core_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.ssh2_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.ssh_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.team.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.text_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.tomcat_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.cheatsheets_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.console_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.editors_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.externaltools_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.forms_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.ide_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.intro_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.presentations.r21_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.views_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.workbench_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.workbench.compatibility_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.ui.workbench.texteditor_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.update.configurator_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.update.core_*.*.*

%dir %{_datadir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/about.html
%{_datadir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/fragment.xml
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/os/linux/%{_eclipse_arch}/libupdate.so
%{_datadir}/%{name}/plugins/org.eclipse.update.scheduler_*.*.*
%{_datadir}/%{name}/plugins/org.eclipse.update.ui_*.*.*
%{_datadir}/%{name}/plugins/org.junit_*.*.*
