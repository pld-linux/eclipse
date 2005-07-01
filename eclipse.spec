#
# TODO:
#			- separate SWT (there are separate tarballs at http://www.eclipse.org/swt/)
#			  and add proper provides, obsoletes, conflicts etc. where needed.
#			  This will make building such things like Azureus possible without having
#			  whole Eclipse suite installed.
#
%define		_buildid	200506271435
#define		_mver		M6
%define		_ver_major	3.1
%define		_ver_minor	0
#
Summary:	Eclipse - an open extensible IDE
Summary(pl):	Eclipse - otwarte, rozszerzalne środowisko programistyczne
Name:		eclipse
Version:	%{_ver_major}
#Release:	0.%{_mver}_%{_buildid}.1
Release:	0.1
License:	EPL v1.0
Group:		Development/Tools
#Source0:	http://download.eclipse.org/downloads/drops/S-%{_ver_major}%{_mver}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_ver_major}%{_mver}.zip
Source0:	http://download.eclipse.org/eclipse/downloads/drops/R-%{_ver_major}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_ver_major}.zip
# Source0-md5:	19ad65d52005da5eaa1d3687b3a50de2
Source1:	%{name}.desktop
Patch0:		%{name}-core_resources-makefile.patch
Patch1:		%{name}-jikesbuild.patch
URL:		http://www.eclipse.org/
BuildRequires:	jakarta-ant >= 1.6.1
BuildRequires:	jdk >= 1.4
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	unzip
BuildRequires:	zip
Requires:	jakarta-ant
Requires:	jdk >= 1.4
Obsoletes:	eclipse-SDK
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_eclipse_arch	%(echo %{_target_cpu} | sed 's/i.86/x86/;s/athlon/x86/;s/pentium./x86/')
%define		no_install_post_chrpath		1
%ifarch %{x8664}
%define         _noautostrip	.*\\.so
%endif

%description
Eclipse is a kind of universal tool platform - an open extensible IDE
for anything and nothing in particular.

%description -l pl
Eclipse to rodzaj uniwersalnej platformy narzędziowej - otwarte,
rozszerzalne IDE (zintegrowane środowisko programistyczne) do
wszystkiego i niczego w szczególności.

%prep
%setup -q -c
%patch0 -p0
%patch1 -p1

%build
export JAVA_HOME=%{_libdir}/java

./build -os linux -ws gtk -arch %{_eclipse_arch} -target compile

export JAVA_INC="-I$JAVA_HOME/include -I$JAVA_HOME/include/linux"

%{__make} -C plugins/org.eclipse.core.resources.linux/src \
    CFLAGS="%{rpmcflags} $JAVA_INC" \
    LDFLAGS="%{rpmldflags}"
mv plugins/org.eclipse.core.resources.linux/{src/libcore*.so,os/linux/%{_eclipse_arch}}

%ifarch %{x8664}
mkdir plugins/org.eclipse.update.core.linux/os/linux/%{_eclipse_arch}
%endif

cd plugins/org.eclipse.update.core.linux/src
%{__cc} %{rpmcflags} -fPIC %{rpmldflags} -I. $JAVA_INC update.c -o libupdate.so -shared
mv libupdate.so ../os/linux/%{_eclipse_arch}
cd -

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_bindir},%{_libdir}/%{name}}

./build -os linux -ws gtk -arch %{_eclipse_arch} -target install

tar xfz result/linux-gtk-%{_eclipse_arch}-sdk.tar.gz -C $RPM_BUILD_ROOT%{_libdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

#wrapper
install -d $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/eclipse << EOF
#!/bin/sh
exec %{_libdir}/%{name}/eclipse \$*
EOF

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
%{_libdir}/%{name}/eclipse.ini
%{_libdir}/%{name}/epl-v10.html
%{_libdir}/%{name}/icon.xpm
%{_libdir}/%{name}/notice.html
%{_libdir}/%{name}/readme
%{_libdir}/%{name}/startup.jar
%dir %{_libdir}/%{name}/features
%{_libdir}/%{name}/features/org.eclipse.jdt_*.*.*
%{_libdir}/%{name}/features/org.eclipse.jdt.source_*.*.*
%{_libdir}/%{name}/features/org.eclipse.pde_*.*.*
%{_libdir}/%{name}/features/org.eclipse.pde.source_*.*.*
%{_libdir}/%{name}/features/org.eclipse.platform_*.*.*
%{_libdir}/%{name}/features/org.eclipse.platform.source_*.*.*
%{_libdir}/%{name}/features/org.eclipse.rcp_*.*.*
%{_libdir}/%{name}/features/org.eclipse.rcp.source_*.*.*
%{_libdir}/%{name}/features/org.eclipse.sdk_*.*.*
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/org.apache.ant_*.*.*
%{_libdir}/%{name}/plugins/org.apache.lucene_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ant.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ant.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.compare_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.boot_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.commands_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.expressions_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.filebuffers_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.resources_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.resources.compatibility_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.resources.linux_*.*.*.jar
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime.compatibility_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.variables_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.debug.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.debug.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.appserver_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.base_*.*.*
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
%{_libdir}/%{name}/plugins/org.eclipse.rcp_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.rcp.source_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.rcp.source.linux.gtk.%{_eclipse_arch}_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.sdk_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.swt.gtk.linux.%{_eclipse_arch}_*.*.*.jar
%{_libdir}/%{name}/plugins/org.eclipse.search_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.swt_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.browser_*.*.*
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
%{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*.jar
%{_libdir}/%{name}/plugins/org.eclipse.update.scheduler_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.ui_*.*.*
%{_libdir}/%{name}/plugins/org.junit_*.*.*
