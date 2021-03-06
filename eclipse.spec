# TODO:
# - make use of eclipse-swt package
# - this shit needs jetty(!) to build
#
%define		ebuildver	0.6.1

Summary:	Eclipse - an open extensible IDE
Summary(pl.UTF-8):	Eclipse - otwarte, rozszerzalne środowisko programistyczne
Name:		eclipse
Version:	3.6.1
Release:	0.1
License:	EPL v1.0
Group:		Development/Tools
Source0:	http://download.eclipse.org/technology/linuxtools/eclipse-build/3.6.x_Helios/%{name}-build-%{ebuildver}.tar.bz2
# Source0-md5:	dac006a81d45f366ecbf3f78f7fa9424
Source1:	http://download.eclipse.org/technology/linuxtools/eclipse-build/3.6.x_Helios/%{name}-%{version}-src.tar.bz2
# Source1-md5:	306f8bf4ec2b0bf6f3f8329608cb15dd
Source2:	%{name}.desktop
Patch0:		%{name}-launcher-set-install-dir-and-shared-config.patch
URL:		http://www.eclipse.org/
BuildRequires:	ant >= 1.6.1
BuildRequires:	ant-apache-regexp
BuildRequires:	ant-nodeps
BuildRequires:	java-commons-el >= 1.0-5
BuildRequires:	java-commons-httpclient >= 3.1-4
BuildRequires:	java-sat4j
BuildRequires:	jdk >= 1.6
BuildRequires:	jetty
BuildRequires:	jpackage-utils
BuildRequires:	pkgconfig
BuildRequires:	rpm-javaprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	zip
Requires:	ant
Provides:	eclipse-jdt = %{version}-%{release}
Obsoletes:	eclipse-SDK
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		eclipse_arch	%(echo %{_target_cpu} | sed 's/i.86\\|athlon\\|pentium/x86/;s/amd64/x86_64/')
%define		no_install_post_chrpath		1

# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov			libcairo.so.2

%description
Eclipse is a kind of universal tool platform - an open extensible IDE
for anything and nothing in particular.

%description -l pl.UTF-8
Eclipse to rodzaj uniwersalnej platformy narzędziowej - otwarte,
rozszerzalne IDE (zintegrowane środowisko programistyczne) do
wszystkiego i niczego w szczególności.

%prep
%setup -q -n %{name}-build-%{ebuildver}
cp %{SOURCE1} .
ant -Dlabel=%{version} -DbuildArch=%{eclipse_arch} applyPatches

# Build Id - it's visible in couple places in GUI
%{__sed} -i -e 's,buildId=.*,& (PLD Linux %{name}-%{version}-%{release}),' build/%{name}-%{version}-src/label.properties

%build
unset CLASSPATH || :
export JAVA_HOME=%{java_home}

#-./build -os linux -ws gtk -arch %{eclipse_arch} -target compile
%ant -Dlabel=%{version} -DbuildArch=%{eclipse_arch}
%ant insertBuildId

%install
if [ ! -f makeinstall.stamp -o ! -d $RPM_BUILD_ROOT ]; then
	rm -rf makeinstall.stamp installed.stamp $RPM_BUILD_ROOT

	install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_bindir},%{_libdir}/%{name}}
	# place for arch independent plugins
	install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{features,plugins}

	unset JAVA_HOME || :
	export JAVA_HOME=%{java_home}
	./build -os linux -ws gtk -arch %{eclipse_arch} -target install

	tar xfz result/linux-gtk-%{eclipse_arch}-sdk.tar.gz -C $RPM_BUILD_ROOT%{_libdir}
	touch makeinstall.stamp
fi

if [ ! -f installed.stamp ]; then
	install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

	install -p plugins/org.eclipse.core.filesystem/natives/unix/linux/lib*.so $RPM_BUILD_ROOT%{_libdir}/%{name}
	install -p plugins/org.eclipse.update.core.linux/src/lib*.so $RPM_BUILD_ROOT%{_libdir}/%{name}

	# wrapper
	install -d $RPM_BUILD_ROOT%{_bindir}
	cat > $RPM_BUILD_ROOT%{_bindir}/eclipse <<-'EOF'
	#!/bin/sh
	exec %{_libdir}/%{name}/eclipse ${1:+"$@"}
	EOF

	cat <<-'EOF'> $RPM_BUILD_ROOT%{_datadir}/%{name}/.eclipseextension
	id=org.eclipse.platform name=Eclipse Platform
	version=%{version}
	EOF

	if [ ! -f $RPM_BUILD_ROOT%{_libdir}/%{name}/icon.xpm ]; then
		install -p features/org.eclipse.equinox.executable/bin/gtk/linux/x86/icon.xpm $RPM_BUILD_ROOT%{_libdir}/%{name}/icon.xpm
	fi
	install -Dp features/org.eclipse.equinox.executable/bin/gtk/linux/x86/icon.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/eclipse-icon.xpm

	# not packaged -- remove
	%if 0
	# if we're removing source bundles, we should adjust manifests as well, but
	# were not doing that, so don't break packaging
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/features/org.eclipse.cvs.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/features/org.eclipse.jdt.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/features/org.eclipse.pde.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/features/org.eclipse.platform.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/features/org.eclipse.rcp.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/javax.servlet.jsp.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/javax.servlet.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.apache.ant.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.apache.commons.el.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.apache.commons.logging.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.apache.jasper.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.apache.lucene.analysis.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.apache.lucene.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.eclipse.cvs.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.eclipse.jdt.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.eclipse.pde.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.eclipse.platform.source.linux.gtk.*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.eclipse.platform.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.eclipse.rcp.source.linux.gtk.*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.eclipse.rcp.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.junit.source_*
	rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/org.mortbay.jetty.source_*
	%endif

	touch installed.stamp
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eclipse
%attr(755,root,root) %{_libdir}/%{name}/eclipse
%attr(755,root,root) %{_libdir}/%{name}/lib*.so
%{_desktopdir}/eclipse.desktop
%{_pixmapsdir}/eclipse-icon.xpm
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/.eclipseproduct
%{_libdir}/%{name}/configuration
%{_libdir}/%{name}/eclipse.ini
%{_libdir}/%{name}/epl-v10.html
%{_libdir}/%{name}/icon.xpm
%{_libdir}/%{name}/notice.html
%{_libdir}/%{name}/readme
%{_libdir}/%{name}/about.html
#%dir %{_libdir}/%{name}/about_files
#%{_libdir}/%{name}/about_files/mpl-v11.txt
%dir %{_libdir}/%{name}/features
%{_libdir}/%{name}/features/org.eclipse.cvs_*.*.*
%{_libdir}/%{name}/features/org.eclipse.jdt_*.*.*
%{_libdir}/%{name}/features/org.eclipse.pde_*.*.*
%{_libdir}/%{name}/features/org.eclipse.platform_*.*.*
%{_libdir}/%{name}/features/org.eclipse.rcp_*.*.*
%{_libdir}/%{name}/features/org.eclipse.sdk_*.*.*
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/org.eclipse.swt.gtk.linux.%{eclipse_arch}_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.launcher.gtk.linux.%{eclipse_arch}_*.*.*
%{_libdir}/%{name}/plugins/javax.servlet.jsp_*.*.*
%{_libdir}/%{name}/plugins/javax.servlet_*.*.*
%{_libdir}/%{name}/plugins/com.ibm.icu_*.*.*
%{_libdir}/%{name}/plugins/com.jcraft.jsch_*.*.*
%{_libdir}/%{name}/plugins/org.apache.ant_*.*.*
%{_libdir}/%{name}/plugins/org.apache.commons.el_*.*.*
%{_libdir}/%{name}/plugins/org.apache.commons.logging_*.*.*
%{_libdir}/%{name}/plugins/org.apache.jasper_*.*.*
%{_libdir}/%{name}/plugins/org.apache.lucene_*.*.*
%{_libdir}/%{name}/plugins/org.apache.lucene.analysis_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ant.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ant.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.compare_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.boot_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.commands_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.contenttype_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.databinding_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.databinding.beans_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.expressions_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.filebuffers_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.filesystem_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.filesystem.linux.*_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.jobs_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.net_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.resources_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.resources.compatibility_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime.compatibility_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime.compatibility.auth_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime.compatibility.registry_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.core.variables_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.cvs_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.debug.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.debug.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.app_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.common_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.http.jetty_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.http.registry_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.http.servlet_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.jsp.jasper.registry_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.jsp.jasper_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.launcher_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.preferences_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.registry_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.appserver_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.base_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.help.webapp_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.apt.*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.core.manipulation*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.debug_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.debug.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.doc.isv_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.doc.user_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.junit_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.junit.runtime_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.junit4.runtime_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.launching_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.compiler.apt_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.compiler.tool_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jface_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jface.databinding_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jface.text_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jsch.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.jsch.ui_*.*.*
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
%{_libdir}/%{name}/plugins/org.eclipse.pde.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.pde.ui.templates_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.platform_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.platform.doc.isv_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.platform.doc.user_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.rcp_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.sdk_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.swt_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.search_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ssh2_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ssh_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.team.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.text_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.tomcat_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.browser_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.cheatsheets_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.console_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.editors_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.externaltools_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.forms_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.ide_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.ide.application_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.intro_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.intro.universal_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.navigator_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.navigator.resources_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.net_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.presentations.r21_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.views_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.views.properties.tabbed_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench.compatibility_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench.texteditor_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.configurator_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.core_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.scheduler_*.*.*
%{_libdir}/%{name}/plugins/org.eclipse.update.ui_*.*.*
%{_libdir}/%{name}/plugins/org.junit_*.*.*
%{_libdir}/%{name}/plugins/org.junit4_*.*.*
%{_libdir}/%{name}/plugins/org.mortbay.jetty_*.*.*

%if 1
%{_libdir}/%{name}/features/org.eclipse.cvs.source_*
%{_libdir}/%{name}/features/org.eclipse.jdt.source_*
%{_libdir}/%{name}/features/org.eclipse.pde.source_*
%{_libdir}/%{name}/features/org.eclipse.platform.source_*
%{_libdir}/%{name}/features/org.eclipse.rcp.source_*
%{_libdir}/%{name}/plugins/javax.servlet.jsp.source_*
%{_libdir}/%{name}/plugins/javax.servlet.source_*
%{_libdir}/%{name}/plugins/org.apache.ant.source_*
%{_libdir}/%{name}/plugins/org.apache.commons.el.source_*
%{_libdir}/%{name}/plugins/org.apache.commons.logging.source_*
%{_libdir}/%{name}/plugins/org.apache.jasper.source_*
%{_libdir}/%{name}/plugins/org.apache.lucene.analysis.source_*
%{_libdir}/%{name}/plugins/org.apache.lucene.source_*
%{_libdir}/%{name}/plugins/org.eclipse.cvs.source_*
%{_libdir}/%{name}/plugins/org.eclipse.jdt.source_*
%{_libdir}/%{name}/plugins/org.eclipse.pde.source_*
%{_libdir}/%{name}/plugins/org.eclipse.platform.source.linux.gtk.*
%{_libdir}/%{name}/plugins/org.eclipse.platform.source_*
%{_libdir}/%{name}/plugins/org.eclipse.rcp.source.linux.gtk.*
%{_libdir}/%{name}/plugins/org.eclipse.rcp.source_*
%{_libdir}/%{name}/plugins/org.junit.source_*
%{_libdir}/%{name}/plugins/org.mortbay.jetty.source_*
%endif

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/features
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/.eclipseextension
