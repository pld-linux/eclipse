#
%define		_buildid	200409240800
%define		_ver_major	3.1
%define		_ver_minor	0
%define		_ver		%{_ver_major}.%{_ver_minor}
#
Summary:	Eclipse - an open extensible IDE
Summary(pl):	Eclipse - otwarte, rozszerzalne ¶rodowisko programistyczne
Name:		eclipse
Version:	%{_ver_major}
Release:	0.M2_%{_buildid}.2
License:	CPL v1.0
Group:		Development/Tools
Source0:	http://download.eclipse.org/downloads/drops/S-%{_ver_major}M2-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_ver_major}M2.zip
# Source0-md5:	a10fc8b23fd7c6783d55d795168879f0
# Source0-size:	56139196
Source1:	%{name}.desktop
Patch0:		%{name}-swt-makefile.patch
Patch1:		%{name}-core_resources-makefile.patch
URL:		http://www.eclipse.org/
BuildRequires:	jakarta-ant >= 1.6.1
BuildRequires:	jdk >= 1.4
BuildRequires:	kdelibs-devel
BuildRequires:	libgnomeui-devel
#BuildRequires:	mozilla-devel
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
JAVA_HOME=%{_libdir}/java
export JAVA_HOME
./build -os linux -ws gtk -arch %{_eclipse_arch} -target compile

%ifarch amd64
%define	_swtsrcdir	plugins/org.eclipse.swt.gtk64/ws/gtk
%define	_swtgtkdir	plugins/org.eclipse.swt.gtk64
%else
%define	_swtsrcdir	plugins/org.eclipse.swt.gtk/ws/gtk
%define	_swtgtkdir	plugins/org.eclipse.swt.gtk
%endif

rm -rf swt
mkdir swt && cd swt

unzip -x %{_builddir}/%{name}-%{version}/%{_swtsrcdir}/swtsrc.zip
unzip -x %{_builddir}/%{name}-%{version}/%{_swtsrcdir}/swt-pisrc.zip
#unzip -x %{_builddir}/%{name}-%{version}/%{_swtsrcdir}/swt-mozillasrc.zip

export JAVA_INC="-I$JAVA_HOME/include -I$JAVA_HOME/include/linux"

patch -p0 < %{PATCH0}
%{__make} -f make_linux.mak all \
    XTEST_LIB_PATH=%{_prefix}/X11R6/%{_lib} \
    OPT="%{rpmcflags}"
#cp library/* .
#{__make} -f make_linux.mak make_mozilla \
#    OPT="%{rpmcflags}"
cd -

mkdir plugins/org.eclipse.core.resources.linux/os/linux/%{_eclipse_arch}
%{__make} -C plugins/org.eclipse.core.resources.linux/src \
    CFLAGS="%{rpmcflags} $JAVA_INC" \
    LDFLAGS="%{rpmldflags}"
mv plugins/org.eclipse.core.resources.linux/{src/libcore*.so,os/linux/%{_eclipse_arch}}

mkdir plugins/org.eclipse.update.core.linux/os/linux/%{_eclipse_arch}
cd plugins/org.eclipse.update.core.linux/src
%{__cc} %{rpmcflags} -fPIC %{rpmldflags} -I. $JAVA_INC update.c -o libupdate.so -shared
mv libupdate.so ../os/linux/%{_eclipse_arch}
cd -

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_bindir},%{_libdir}/%{name}}
install -d $RPM_BUILD_ROOT%{_libdir}/eclipse/%{_swtgtkdir}_3.1.0/os/linux/amd64

./build -os linux -ws gtk -arch %{_eclipse_arch} -target install

unzip result/linux-gtk-%{_eclipse_arch}-sdk.zip -d $RPM_BUILD_ROOT%{_libdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

#wrapper
install -d $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/eclipse << EOF
#!/bin/sh
exec %{_libdir}/%{name}/eclipse \$*
EOF

cd swt
install libswt-{atk-gtk,awt-gtk,gnome-gtk,gtk,kde,pi-gtk}-*.so \
    $RPM_BUILD_ROOT%{_libdir}/eclipse/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}
#install libswt-mozilla-gtk-*.so \
#    $RPM_BUILD_ROOT%{_datadir}/eclipse/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eclipse
%attr(755,root,root) %{_libdir}/%{name}/eclipse
%{_desktopdir}/eclipse.desktop
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/.eclipseproduct
%{_libdir}/%{name}/configuration
%{_libdir}/%{name}/icon.xpm
%{_libdir}/%{name}/notice.html
%{_libdir}/%{name}/readme
%{_libdir}/%{name}/startup.jar

# features
%dir %{_libdir}/%{name}/features
%{_libdir}/%{name}/features/org.eclipse.jdt_*.*.*
%{_libdir}/%{name}/features/org.eclipse.jdt.source_*.*.*
%{_libdir}/%{name}/features/org.eclipse.pde_*.*.*
%{_libdir}/%{name}/features/org.eclipse.pde.source_*.*.*
%{_libdir}/%{name}/features/org.eclipse.platform_*.*.*
%{_libdir}/%{name}/features/org.eclipse.platform.source_*.*.*
%{_libdir}/%{name}/features/org.eclipse.sdk_*.*.*

# plugins
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/org.apache.ant_*.*.*
%{_libdir}/%{name}/plugins/org.apache.lucene_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ant.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ant.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.compare_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.boot_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.expressions_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.filebuffers_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.resources_*.*.*

%dir %{_libdir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*
%dir %{_libdir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*/os
%dir %{_libdir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*/os/linux
%dir %{_libdir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*/os/linux/%{_eclipse_arch}
%attr(755,root,root) %{_libdir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*/os/linux/%{_eclipse_arch}/libcore_2_1_0b.so
%{_libdir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*/fragment.xml

%{_libdir}/%{name}/plugins/org.eclipse.core.runtime_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime.compatibility_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.variables_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.debug.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.debug.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.appserver_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.base_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.ide_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.webapp_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.debug_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.debug.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.doc.isv_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.doc.user_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.junit_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.junit.runtime_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.launching_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.source_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jface_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jface.text_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ltk.core.refactoring_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ltk.ui.refactoring_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.osgi_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.osgi.services_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.osgi.util_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde.build_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde.doc.user_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde.junit.runtime_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde.runtime_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde.source_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.platform_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.platform.doc.isv_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.platform.doc.user_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.platform.source_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.platform.source.linux.gtk.%{_eclipse_arch}_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.sdk_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.search_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.swt_*.*.*

%dir %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*
%dir %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os
%dir %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux
%dir %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}
%attr(755,root,root) %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-atk-gtk-*.so
%attr(755,root,root) %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-awt-gtk-*.so
%attr(755,root,root) %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-gnome-gtk-*.so
%attr(755,root,root) %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-gtk-*.so
%attr(755,root,root) %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-kde-gtk*.so
#attr(755,root,root) %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-mozilla-gtk-*.so
%attr(755,root,root) %{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-pi-gtk-*.so
%{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/ws
%{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/META-INF
%{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/about.html
%{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/cpl-v10.html
%{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/fragment.properties
%{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/fragment.xml
%{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/lgpl-v21.txt
%{_libdir}/%{name}/%{_swtgtkdir}_*.*.*/mpl-v11.txt

%{_libdir}/%{name}/plugins/org.eclipse.team.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ssh2_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ssh_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.text_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.tomcat_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.cheatsheets_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.console_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.editors_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.externaltools_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.forms_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.ide_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.intro_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.presentations.r21_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.views_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench.compatibility_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench.texteditor_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.configurator_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.core_*.*.*

%dir %{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*
%dir %{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/os
%dir %{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/os/linux
%dir %{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/os/linux/%{_eclipse_arch}
%attr(755,root,root) %{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/os/linux/%{_eclipse_arch}/libupdate.so
%{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/about.html
%{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*/fragment.xml

%{_libdir}/%{name}/plugins/org.eclipse.update.scheduler_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.ui_*.*.*
%{_libdir}/%{name}/plugins/org.junit_*.*.*
