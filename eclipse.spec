
# TODO:
# 	- conditional build with motiff
#	- .so binaries should be removed and linked with PLD one... 
#         (we really need them here?)

%define		_buildid	200303272130

Summary:	eclipse
Summary(pl):	eclipse
Name:		eclipse-SDK
Version:	2.1.0
Release:	1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://download2.eclipse.org/downloads/drops/R-2.1-%{_buildid}/eclipse-sourceBuild-srcIncluded-2.1.zip
URL:		http://www.eclipse.org
BuildRequires:	jdk
BuildRequires:	jakarta-ant >= 1.4
BuildRequires:	gtk+2-devel
Requires:	jdk
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	/usr/share/java

%define		_noautoreq	libc.so.2 libdb.so.2 libkdecore.so.4 libkdecore.so.3 libksycoca.so.3 libphexlib.so.2 libphrender.so.2 libph.so.2 libqt.so.2 libqt-mt.so.3

%description

%description -l pl

%prep
%setup -q -c -n %{name}-%{version}


%build
./build -os linux -ws gtk -target compile
./build -os linux -ws gtk -target buildDoc

%install
rm -rf $RPM_BUILD_ROOT

./build -os linux -ws gtk -target install

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}

find $RPM_BUILD_ROOT%{_datadir}/%{name} -type d -name src -exec rm -rf {} \; ||:
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type d -name temp.folder -exec rm -rf {} \; ||:
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name build.xml -exec rm -f {} \; ||:
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name build.properties -exec rm -f {} \; ||:
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name ".*" -exec rm -f {} \; ||: 
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name "*src.zip" -exec rm -f {} \; ||: 
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type  d -name "*solaris*" -exec rm -rf {} \; ||: 
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type  d -name "*hpux*" -exec rm -rf {} \; ||: 
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type  d -name "*macosx*" -exec rm -rf {} \; ||: 
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type  d -name "*aix*" -exec rm -rf {} \; ||: 
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type  d -name "*win32*" -exec rm -rf {} \; ||: 
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type  d -name "*qnx*" -exec rm -rf {} \; ||: 

# I'm not so sure about that:
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name "*.java" -exec rm -f {} \; ||: 

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/{build.bat,compilelog.txt,instructions.html,build}

#desktop file
install -d $RPM_BUILD_ROOT%{_desktopdir}
cat > $RPM_BUILD_ROOT%{_desktopdir}/eclipse.desktop << EOF
[Desktop Entry]
Name=Eclipse
Comment=Eclipse
Comment[pl]=Eclipse
Exec=eclipse
Icon=
Terminal=false
MultipleArgs=false
Type=Application
Categories=Application;Development;
# vi: encoding=utf-8
EOF

#wrapper
install -d $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/eclipse << EOF
#!/bin/sh
%{_datadir}/%{name}/eclipse -nosplash -data \$HOME/eclipse
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eclipse
%attr(755,root,root) %{_datadir}/%{name}/eclipse
%{_desktopdir}/eclipse.desktop

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/plugins

%{_datadir}/%{name}/plugins/org.eclipse.jdt.source

%dir %{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk/plugin.properties
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk/eclipse32.gif
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk/about.ini
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk/about.html
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk/libXm.so.2.1
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk/about.properties
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk/plugin.xml
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk/about.mappings

%{_datadir}/%{name}/plugins/org.eclipse.webdav
%{_datadir}/%{name}/plugins/org.eclipse.ui.workbench
%{_datadir}/%{name}/plugins/org.eclipse.core.runtime
%{_datadir}/%{name}/plugins/org.eclipse.platform.doc.isv
%{_datadir}/%{name}/plugins/org.eclipse.update.core
%{_datadir}/%{name}/plugins/org.eclipse.jface
%{_datadir}/%{name}/plugins/org.eclipse.ui
%{_datadir}/%{name}/plugins/org.eclipse.debug.core
%{_datadir}/%{name}/plugins/org.eclipse.jdt.launching
%{_datadir}/%{name}/plugins/org.eclipse.jdt.core
%{_datadir}/%{name}/plugins/org.eclipse.help
%{_datadir}/%{name}/plugins/org.eclipse.help.webapp
%{_datadir}/%{name}/plugins/org.eclipse.core.resources
%{_datadir}/%{name}/plugins/org.eclipse.ant.optional.junit
%{_datadir}/%{name}/plugins/org.eclipse.update.ui.forms
%{_datadir}/%{name}/plugins/org.eclipse.ui.workbench.texteditor
%{_datadir}/%{name}/plugins/org.eclipse.ui.editors
%{_datadir}/%{name}/plugins/org.eclipse.team.extras
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.core
%{_datadir}/%{name}/plugins/org.eclipse.sdk.linux.gtk
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.gtk.source
%{_datadir}/%{name}/plugins/org.eclipse.pde
%{_datadir}/%{name}/plugins/org.eclipse.jdt.junit
%{_datadir}/%{name}/plugins/org.eclipse.jdt.doc.user

%dir %{_datadir}/%{name}/plugins/org.eclipse.update.core.linux
%{_datadir}/%{name}/plugins/org.eclipse.update.core.linux/about.html
%{_datadir}/%{name}/plugins/org.eclipse.update.core.linux/fragment.xml

%{_datadir}/%{name}/plugins/org.eclipse.pde.runtime

%dir %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/os/linux/x86/libswt-pi-gtk-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/os/linux/x86/libswt-gtk-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/os/linux/x86/libswt-gnome-gtk-*.so
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/lgpl-v21.txt
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/cpl-v10.html
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/fragment.xml
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/about.html
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/fragment.properties
%{_datadir}/%{name}/plugins/org.eclipse.swt.gtk/ws

%{_datadir}/%{name}/plugins/org.eclipse.help.ui
%{_datadir}/%{name}/plugins/org.eclipse.jdt.ui
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif.source
%{_datadir}/%{name}/plugins/org.eclipse.ui.externaltools
%{_datadir}/%{name}/plugins/org.eclipse.tomcat
%{_datadir}/%{name}/plugins/org.eclipse.platform
%{_datadir}/%{name}/plugins/org.eclipse.platform.doc.user

%dir %{_datadir}/%{name}/plugins/org.eclipse.swt.motif
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.motif/os/linux/x86/libswt-kde-motif-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.motif/os/linux/x86/libswt-gnome-motif-*.so
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.swt.motif/os/linux/x86/libswt-motif-*.so
%{_datadir}/%{name}/plugins/org.eclipse.swt.motif/fragment.xml
%{_datadir}/%{name}/plugins/org.eclipse.swt.motif/about.html
%{_datadir}/%{name}/plugins/org.eclipse.swt.motif/fragment.properties
%{_datadir}/%{name}/plugins/org.eclipse.swt.motif/permissions.properties

%{_datadir}/%{name}/plugins/org.eclipse.team.core
%{_datadir}/%{name}/plugins/org.eclipse.pde.source
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.ssh
%{_datadir}/%{name}/plugins/org.eclipse.pde.ui
%{_datadir}/%{name}/plugins/org.eclipse.text
%{_datadir}/%{name}/plugins/org.junit
%{_datadir}/%{name}/plugins/org.eclipse.jdt.debug
%{_datadir}/%{name}/plugins/org.eclipse.team.ui
%{_datadir}/%{name}/plugins/org.eclipse.debug.ui
%{_datadir}/%{name}/plugins/org.eclipse.swt.carbon
%{_datadir}/%{name}/plugins/org.eclipse.pde.doc.user
%{_datadir}/%{name}/plugins/org.eclipse.pde.core
%{_datadir}/%{name}/plugins/org.eclipse.jdt.debug.ui
%{_datadir}/%{name}/plugins/org.eclipse.swt.photon
%{_datadir}/%{name}/plugins/org.eclipse.jdt
%{_datadir}/%{name}/plugins/org.eclipse.pde.build
%{_datadir}/%{name}/plugins/org.eclipse.platform.source
%{_datadir}/%{name}/plugins/org.eclipse.compare
%{_datadir}/%{name}/plugins/org.apache.lucene
%{_datadir}/%{name}/plugins/org.eclipse.ui.views
%{_datadir}/%{name}/plugins/org.eclipse.sdk.linux.motif

%dir %{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux/os/linux/x86/libcore_2_1_0a.so
%{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux/fragment.xml
%{_datadir}/%{name}/plugins/org.eclipse.core.resources.linux/about.html

%{_datadir}/%{name}/plugins/org.eclipse.jdt.doc.isv
%{_datadir}/%{name}/plugins/org.eclipse.help.appserver
%{_datadir}/%{name}/plugins/org.apache.xerces
%{_datadir}/%{name}/plugins/org.eclipse.team.cvs.ui
%{_datadir}/%{name}/plugins/org.eclipse.team.webdav
%{_datadir}/%{name}/plugins/org.eclipse.update.ui
%{_datadir}/%{name}/plugins/org.eclipse.team.ftp
%{_datadir}/%{name}/plugins/org.eclipse.jface.text

%dir %{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/plugin.xml
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/about.mappings
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/os/linux/x86/libXm.so.2.1
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/plugin.properties
%attr(755,root,root) %{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/libXm.so.2.1
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/eclipse32.gif
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/about.ini
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/about.properties
%{_datadir}/%{name}/plugins/org.eclipse.platform.linux.motif/about.html

%{_datadir}/%{name}/plugins/org.eclipse.search
%{_datadir}/%{name}/plugins/org.eclipse.core.boot
%{_datadir}/%{name}/plugins/org.apache.ant
%{_datadir}/%{name}/plugins/org.eclipse.swt
%{_datadir}/%{name}/plugins/org.eclipse.ant.core
%{_datadir}/%{name}/plugins/platform-launcher

%{_datadir}/%{name}/features
%{_datadir}/%{name}/startup.jar
%{_datadir}/%{name}/splash.bmp
%{_datadir}/%{name}/icon.xpm
