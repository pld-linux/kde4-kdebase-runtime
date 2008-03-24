#
# Conditional build:
%bcond_without	apidocs		# do not prepare API documentation
#
%define		_state		unstable
%define		orgname		kdebase-runtime
Summary:	KDE 4 base runtime components
Summary(pl.UTF-8):	Komponenty uruchomieniowe podstawowej części KDE 4
Name:		kde4-kdebase-runtime
Version:	4.0.66
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/%{version}/src/%{orgname}-%{version}.tar.bz2
# Source0-md5:	bbc7ba68ce96e8ad2201f01c7d336da1
URL:		http://www.kde.org/
BuildRequires:	cmake
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	kde4-kdelibs-devel >= %{version}
BuildRequires:	kde4-kdepimlibs-devel >= %{version}
BuildRequires:	libsmbclient-devel
%{?with_apidocs:BuildRequires:	qt4-doc >= 4.3.0}
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	soprano-devel
BuildRequires:	strigi-devel >= 0.5.5
BuildRequires:	xine-lib-devel
Obsoletes:	kdebase4-runtime
Conflicts:	kdebase4-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE 4 runtime components.

%description -l pl.UTF-8
Komponenty uruchomieniowe podstawowej części KDE 4.

%package devel
Summary:	Development files for KDE 4 runtime components
Summary(pl.UTF-8):	Pliki programistyczne komponentów uruchomieniowych KDE 4
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kde4-kdelibs-devel >= %{version}

%description devel
Development files for KDE 4 runtime components.

%description devel -l pl.UTF-8
Pliki programistyczne komponentów uruchomieniowych KDE 4.

%package -n kde4-phonon-xine
Summary:	Xine backend to Phonon
Summary(pl.UTF-8):	Backend Xine dla Phonona
Group:		X11/Applications

%description -n kde4-phonon-xine
Xine backend to Phonon.

%description -n kde4-phonon-xine -l pl.UTF-8
Backend Xine dla Phonona.

%package -n kde4-icons-oxygen
Summary:	KDE icons - oxygen
Summary(pl.UTF-8):	Motyw ikon do KDE - oxygen
Group:		Themes
Obsoletes:	kde-icons-oxygen

%description -n kde4-icons-oxygen
KDE icons - oxygen.

%description -n kde4-icons-oxygen -l pl.UTF-8
Motyw ikon do KDE - oxygen.

%package -n kde4-style-oxygen
Summary:	KDE Oxygen Style
Summary(pl.UTF-8):	Styl Oxygen dla KDE
Group:		Themes
Obsoletes:	kde-style-oxygen

%description -n kde4-style-oxygen
KDE Oxygen Style.

%description -n kde4-style-oxygen -l pl.UTF-8
Styl Oxygen dla KDE.

%prep
%setup -q -n %{orgname}-%{version}

%build
export QTDIR=%{_prefix}
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

rm -f %{name}-files
WORKDIR=`pwd`
cd $RPM_BUILD_ROOT%{_datadir}/locale/l10n
for DIR in *
do
	if [ -d $DIR ] ; then
		echo "%lang($DIR) %{_datadir}/locale/l10n/$DIR" >> $WORKDIR/%{name}-files
	fi
done
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}-files
%defattr(644,root,root,755)
%{_sysconfdir}/xdg/menus/kde-information.menu
%attr(755,root,root) %{_bindir}/kcmshell4
%attr(755,root,root) %{_bindir}/kde-cp
%attr(755,root,root) %{_bindir}/kde-mv
%attr(755,root,root) %{_bindir}/kde-open
%attr(755,root,root) %{_bindir}/kde4-menu
%attr(755,root,root) %{_bindir}/kdebugdialog
%attr(755,root,root) %{_bindir}/kfile4
%attr(755,root,root) %{_bindir}/khelpcenter
%attr(755,root,root) %{_bindir}/khotnewstuff4
%attr(755,root,root) %{_bindir}/kioclient
%attr(755,root,root) %{_bindir}/kmimetypefinder
%attr(755,root,root) %{_bindir}/knotify4
%attr(755,root,root) %{_bindir}/kquitapp
%attr(755,root,root) %{_bindir}/kreadconfig
%attr(755,root,root) %{_bindir}/kstart
# conflict with kde3
#%attr(755,root,root) %{_bindir}/ksvgtopng
%attr(755,root,root) %{_bindir}/ktraderclient
%attr(755,root,root) %{_bindir}/ktrash
%attr(755,root,root) %{_bindir}/kuiserver
%attr(755,root,root) %{_bindir}/kwriteconfig
%attr(755,root,root) %{_libdir}/libkdeinit4_kcmshell4.so
%attr(755,root,root) %{_libdir}/libkdeinit4_khelpcenter.so
%attr(755,root,root) %{_libdir}/libkdeinit4_kuiserver.so
%attr(755,root,root) %{_libdir}/kde4/cursorthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/djvuthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/exrthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/htmlthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/imagethumbnail.so
%attr(755,root,root) %{_libdir}/kde4/kcm_cgi.so
%attr(755,root,root) %{_libdir}/kde4/kcm_componentchooser.so
%attr(755,root,root) %{_libdir}/kde4/kcm_icons.so
%attr(755,root,root) %{_libdir}/kde4/kcm_ioslaveinfo.so
%attr(755,root,root) %{_libdir}/kde4/kcm_kded.so
%attr(755,root,root) %{_libdir}/kde4/kcm_kdnssd.so
%attr(755,root,root) %{_libdir}/kde4/kcm_knotify.so
%attr(755,root,root) %{_libdir}/kde4/kcm_locale.so
%attr(755,root,root) %{_libdir}/kde4/kcm_samba.so
%attr(755,root,root) %{_libdir}/kde4/kded_kpasswdserver.so
%attr(755,root,root) %{_libdir}/kde4/kded_ktimezoned.so
%attr(755,root,root) %{_libdir}/kde4/kded_remotedirnotify.so
%attr(755,root,root) %{_libdir}/kde4/kded_soliduiserver.so
%attr(755,root,root) %{_libdir}/kde4/kio_about.so
%attr(755,root,root) %{_libdir}/kde4/kio_archive.so
%attr(755,root,root) %{_libdir}/kde4/kio_cgi.so
%attr(755,root,root) %{_libdir}/kde4/kio_filter.so
%attr(755,root,root) %{_libdir}/kde4/kio_finger.so
%attr(755,root,root) %{_libdir}/kde4/kio_fish.so
%attr(755,root,root) %{_libdir}/kde4/kio_floppy.so
%attr(755,root,root) %{_libdir}/kde4/kio_info.so
%attr(755,root,root) %{_libdir}/kde4/kio_man.so
%attr(755,root,root) %{_libdir}/kde4/kio_nfs.so
%attr(755,root,root) %{_libdir}/kde4/kio_remote.so
%attr(755,root,root) %{_libdir}/kde4/kio_settings.so
%attr(755,root,root) %{_libdir}/kde4/kio_sftp.so
%attr(755,root,root) %{_libdir}/kde4/kio_smb.so
%attr(755,root,root) %{_libdir}/kde4/kio_thumbnail.so
%attr(755,root,root) %{_libdir}/kde4/kio_trash.so
%attr(755,root,root) %{_libdir}/kde4/libfixhosturifilter.so
%attr(755,root,root) %{_libdir}/kde4/libkmanpart.so
%attr(755,root,root) %{_libdir}/kde4/libkshorturifilter.so
%attr(755,root,root) %{_libdir}/kde4/libkuriikwsfilter.so
%attr(755,root,root) %{_libdir}/kde4/libkurisearchfilter.so
%attr(755,root,root) %{_libdir}/kde4/liblocaldomainurifilter.so
%attr(755,root,root) %{_libdir}/kde4/librenaudioplugin.so
%attr(755,root,root) %{_libdir}/kde4/librenimageplugin.so
%attr(755,root,root) %{_libdir}/kde4/svgthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/textthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/kcm_nepomuk.so
%attr(755,root,root) %{_libdir}/kde4/kded_nepomukserver.so
%attr(755,root,root) %{_libdir}/kde4/libexec/drkonqi
%attr(755,root,root) %{_libdir}/kde4/libexec/kdeeject
%attr(755,root,root) %{_libdir}/kde4/libexec/kdesu
%attr(755,root,root) %{_libdir}/kde4/libexec/kdesud
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_docbookdig.pl
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_htdig.pl
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_htsearch.pl
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_indexbuilder
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_mansearch.pl
%attr(755,root,root) %{_libdir}/kde4/libexec/kioexec
%attr(755,root,root) %{_libdir}/kde4/libexec/klocaldomainurifilterhelper
%attr(755,root,root) %{_libdir}/kde4/libexec/knetattach
%dir %{_libdir}/kde4/plugins/styles
#%attr(755,root,root) %{_libdir}/strigi/strigiindex_sopranobackend.so
%{_datadir}/apps/drkonqi
%{_datadir}/apps/kcm_componentchooser/kcm_browser.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_kemail.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_terminal.desktop
%{_datadir}/apps/kcmlocale
%{_datadir}/apps/kconf_update/kuriikwsfilter.upd
%{_datadir}/apps/kde/kde.notifyrc
%{_datadir}/apps/khelpcenter
%{_datadir}/apps/kio_finger
%{_datadir}/apps/kio_info
%{_datadir}/apps/kio_man
%{_datadir}/apps/kio_thumbnail
%dir %{_datadir}/apps/konqueror/dirtree
%dir %{_datadir}/apps/konqueror/dirtree/remote
%{_datadir}/apps/konqueror/dirtree/remote/smb-network.desktop
%dir %{_datadir}/apps/remoteview
%{_datadir}/apps/remoteview/smb-network.desktop
%{_datadir}/config.kcfg/khelpcenter.kcfg
%{_datadir}/config/khotnewstuff.knsrc
%{_datadir}/config/kshorturifilterrc
%{_datadir}/dbus-1/interfaces/org.kde.KTimeZoned.xml
%{_datadir}/dbus-1/interfaces/org.kde.khelpcenter.kcmhelpcenter.xml
%{_datadir}/dbus-1/services/org.kde.knotify.service
%{_datadir}/desktop-directories/kde-information.directory
%{_datadir}/emoticons/kde4
%{_datadir}/kde4/services/about.protocol
%{_datadir}/kde4/services/applications.protocol
%{_datadir}/kde4/services/ar.protocol
%{_datadir}/kde4/services/bzip.protocol
%{_datadir}/kde4/services/bzip2.protocol
%{_datadir}/kde4/services/cgi.protocol
%{_datadir}/kde4/services/componentchooser.desktop
%{_datadir}/kde4/services/cursorthumbnail.desktop
%{_datadir}/kde4/services/djvuthumbnail.desktop
%{_datadir}/kde4/services/exrthumbnail.desktop
%{_datadir}/kde4/services/finger.protocol
%{_datadir}/kde4/services/fish.protocol
%{_datadir}/kde4/services/fixhosturifilter.desktop
%{_datadir}/kde4/services/floppy.protocol
%{_datadir}/kde4/services/gzip.protocol
%{_datadir}/kde4/services/htmlthumbnail.desktop
%{_datadir}/kde4/services/icons.desktop
%{_datadir}/kde4/services/imagethumbnail.desktop
%{_datadir}/kde4/services/info.protocol
%{_datadir}/kde4/services/ioslaveinfo.desktop
%{_datadir}/kde4/services/kcm_kdnssd.desktop
%{_datadir}/kde4/services/kcmcgi.desktop
%{_datadir}/kde4/services/kcmkded.desktop
%{_datadir}/kde4/services/kcmnotify.desktop
%{_datadir}/kde4/services/kcm_nepomuk.desktop
%{_datadir}/kde4/services/kded/nepomukserver.desktop
%{_datadir}/kde4/services/kded/kpasswdserver.desktop
%{_datadir}/kde4/services/kded/ktimezoned.desktop
%{_datadir}/kde4/services/kded/remotedirnotify.desktop
%{_datadir}/kde4/services/kded/soliduiserver.desktop
%{_datadir}/kde4/services/khelpcenter.desktop
%{_datadir}/kde4/services/kmanpart.desktop
%{_datadir}/kde4/services/knotify4.desktop
%{_datadir}/kde4/services/kshorturifilter.desktop
%{_datadir}/kde4/services/kuiserver.desktop
%{_datadir}/kde4/services/kuriikwsfilter.desktop
%{_datadir}/kde4/services/kurisearchfilter.desktop
%{_datadir}/kde4/services/language.desktop
%{_datadir}/kde4/services/localdomainurifilter.desktop
%{_datadir}/kde4/services/man.protocol
%{_datadir}/kde4/services/nfs.protocol
%{_datadir}/kde4/services/programs.protocol
%{_datadir}/kde4/services/remote.protocol
%{_datadir}/kde4/services/renaudiodlg.desktop
%{_datadir}/kde4/services/renimagedlg.desktop
%{_datadir}/kde4/services/searchproviders
%{_datadir}/kde4/services/settings.protocol
%{_datadir}/kde4/services/sftp.protocol
%{_datadir}/kde4/services/smb.protocol
%{_datadir}/kde4/services/smbstatus.desktop
%{_datadir}/kde4/services/svgthumbnail.desktop
%{_datadir}/kde4/services/tar.protocol
%{_datadir}/kde4/services/textthumbnail.desktop
%{_datadir}/kde4/services/thumbnail.protocol
%{_datadir}/kde4/services/trash.protocol
%{_datadir}/kde4/services/zip.protocol
%{_datadir}/kde4/servicetypes/searchprovider.desktop
%{_datadir}/kde4/servicetypes/thumbcreator.desktop
%{_datadir}/locale/en_US/*
%dir %{_datadir}/locale/l10n
%{_datadir}/locale/l10n/caribbean.desktop
%{_datadir}/locale/l10n/centralafrica.desktop
%{_datadir}/locale/l10n/centralamerica.desktop
%{_datadir}/locale/l10n/centralasia.desktop
%{_datadir}/locale/l10n/centraleurope.desktop
%{_datadir}/locale/l10n/eastasia.desktop
%{_datadir}/locale/l10n/easteurope.desktop
%{_datadir}/locale/l10n/middleeast.desktop
%{_datadir}/locale/l10n/northafrica.desktop
%{_datadir}/locale/l10n/northamerica.desktop
%{_datadir}/locale/l10n/northeurope.desktop
%{_datadir}/locale/l10n/oceania.desktop
%{_datadir}/locale/l10n/southafrica.desktop
%{_datadir}/locale/l10n/southamerica.desktop
%{_datadir}/locale/l10n/southasia.desktop
%{_datadir}/locale/l10n/southeastasia.desktop
%{_datadir}/locale/l10n/southeurope.desktop
%{_datadir}/locale/l10n/westafrica.desktop
%{_datadir}/locale/l10n/westeurope.desktop
%{_desktopdir}/kde4/Help.desktop
%{_desktopdir}/kde4/knetattach.desktop
%{_kdedocdir}/en/kcontrol
%{_kdedocdir}/en/kdebugdialog
%{_kdedocdir}/en/kdesu
%{_kdedocdir}/en/khelpcenter
%{_kdedocdir}/en/kioslave
%{_kdedocdir}/en/knetattach
%lang(en) %{_mandir}/man1/kdesu.1*
%{_datadir}/sounds/*
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/scalable/apps/*.svgz
# conflicts with hicolor-icon-theme
#%{_iconsdir}/hicolor/index.theme

%files devel
%defattr(644,root,root,755)
%{_datadir}/apps/cmake/modules/FindCLucene.cmake
%{_datadir}/apps/cmake/modules/FindXCB.cmake
#%{_datadir}/apps/cmake/modules/FindXine.cmake

%files -n kde4-phonon-xine
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde4/phonon_xine.so
%attr(755,root,root) %{_libdir}/kde4/kcm_phononxine.so
%{_datadir}/kde4/services/kcm_phononxine.desktop
%dir %{_datadir}/kde4/services/phononbackends
%{_datadir}/kde4/services/phononbackends/xine.desktop

%files -n kde4-icons-oxygen
%defattr(644,root,root,755)
%dir %{_iconsdir}/oxygen
%dir %{_iconsdir}/oxygen/8x8
%{_iconsdir}/oxygen/*x*/actions
%{_iconsdir}/oxygen/*x*/apps
%{_iconsdir}/oxygen/*x*/categories
%{_iconsdir}/oxygen/*x*/devices
%{_iconsdir}/oxygen/*x*/mimetypes
%{_iconsdir}/oxygen/*x*/places
%{_iconsdir}/oxygen/*x*/status
%{_iconsdir}/oxygen/*x*/animations
%{_iconsdir}/oxygen/*x*/emblems
%{_iconsdir}/oxygen/*x*/emotes
%{_iconsdir}/oxygen/index.theme
%dir %{_iconsdir}/oxygen/scalable
%{_iconsdir}/oxygen/scalable/actions
%{_iconsdir}/oxygen/scalable/apps
%{_iconsdir}/oxygen/scalable/categories
%{_iconsdir}/oxygen/scalable/devices
%{_iconsdir}/oxygen/scalable/emblems
%{_iconsdir}/oxygen/scalable/emotes
%{_iconsdir}/oxygen/scalable/export_pngs.sh
%{_iconsdir}/oxygen/scalable/mimetypes
%{_iconsdir}/oxygen/scalable/places
%{_iconsdir}/oxygen/scalable/status

%files -n kde4-style-oxygen
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde4/kstyle_oxygen_config.so
%attr(755,root,root) %{_libdir}/kde4/plugins/styles/oxygen.so
%{_datadir}/apps/kstyle/themes/oxygen.themerc
