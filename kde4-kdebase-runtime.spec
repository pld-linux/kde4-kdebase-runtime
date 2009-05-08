# TODO
# - l10n != %lang glibc locales (et = etiopia not estonia!)
#
# Conditional build:
%bcond_without	apidocs		# do not prepare API documentation
#
%define		_state		stable
%define		orgname		kdebase-runtime
%define		qtver		4.5.0

Summary:	KDE 4 base runtime components
Summary(pl.UTF-8):	Komponenty uruchomieniowe podstawowej części KDE 4
Name:		kde4-kdebase-runtime
Version:	4.2.3
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/%{version}/src/%{orgname}-%{version}.tar.bz2
# Source0-md5:	7ca748e533e3d19f933f9b45f1b1a547
Source1:	kdebase-searchproviders.tar.bz2
# Source1-md5:	126c3524b5367f5096a628acbf9dc86f
Source2:	l10n-iso639-1
Patch100:	%{name}-branch.diff
URL:		http://www.kde.org/
BuildRequires:	QtOpenGL-devel >= %{qtver}
BuildRequires:	QtSvg-devel >= %{qtver}
BuildRequires:	QtTest-devel >= %{qtver}
BuildRequires:	automoc4 >= 0.9.88
BuildRequires:	clucene-core-devel
BuildRequires:	cmake >= 2.6.3
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	kde4-kdelibs-devel >= %{version}
BuildRequires:	kde4-kdepimlibs-devel >= %{version}
BuildRequires:	libsmbclient-devel
BuildRequires:	phonon-devel >= 4.3.1
BuildRequires:	pulseaudio-devel
%{?with_apidocs:BuildRequires:	qt4-doc >= %{qtver}}
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	soprano-devel >= 2.1.64
BuildRequires:	strigi-devel >= 0.6.3
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

%package -n kde4-phonon
Summary:	KDE 4 Phonon plugins
Summary(pl.UTF-8):	Wtyczki KDE 4 dla Phonona
Group:		X11/Applications

%description -n kde4-phonon
KDE 4 Phonon plugins.

%description -n kde4-phonon -l pl.UTF-8
Wtyczki KDE 4 dla Phonona.

%package -n kde4-icons-oxygen
Summary:	KDE icons - oxygen
Summary(pl.UTF-8):	Motyw ikon do KDE - oxygen
Group:		Themes
Obsoletes:	kde-icons-oxygen
Provides:	kde4-icons

%description -n kde4-icons-oxygen
KDE icons - oxygen.

%description -n kde4-icons-oxygen -l pl.UTF-8
Motyw ikon do KDE - oxygen.

%package -n kde4-icons-oxygen-svg
Summary:	KDE SVG icons - oxygen
Summary(pl.UTF-8):	Motyw ikon SVG do KDE - oxygen
Group:		Themes
Provides:	kde4-icons

%description -n kde4-icons-oxygen-svg
KDE icons - oxygen. This package contains SVG icons.

%description -n kde4-icons-oxygen-svg -l pl.UTF-8
Motyw ikon do KDE - oxygen. Ten pakiet zawiera ikony SVG.

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
%setup -q -n %{orgname}-%{version} -a1
#%patch100 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=%{!?debug:release}%{?debug:debug} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

install -d $RPM_BUILD_ROOT%{_datadir}/kde4/services/searchproviders/pld
cp -a kdebase-searchproviders/*.desktop $RPM_BUILD_ROOT%{_datadir}/kde4/services/searchproviders/pld

collect_l10n_files() {
	while read country language comment; do
		[ "$country" != "#" ] || continue
		if [ "$language" = "-" ]; then
			# no mapping. just add for now
			echo >&2 "No mapping for $country $comment, adding without %%lang tag"
			echo "%{_datadir}/locale/l10n/$country"
		else
			echo "%lang($language) %{_datadir}/locale/l10n/$country"
		fi
	done
} < %{SOURCE2}
collect_l10n_files > %{name}.files

rm -f $RPM_BUILD_ROOT%{_datadir}/icons/default.kde4
# provided (conflicts) by hicolor-icon-theme
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/index.theme

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.files
%defattr(644,root,root,755)
%{_sysconfdir}/xdg/menus/kde-information.menu
%attr(755,root,root) %{_bindir}/kcmshell4
%attr(755,root,root) %{_bindir}/kde-cp
%attr(755,root,root) %{_bindir}/kde-mv
%attr(755,root,root) %{_bindir}/kde-open
%attr(755,root,root) %{_bindir}/kde4-menu
%attr(755,root,root) %{_bindir}/kdebugdialog
%attr(755,root,root) %{_bindir}/kfile4
%attr(755,root,root) %{_bindir}/kiconfinder
%attr(755,root,root) %{_bindir}/khelpcenter
%attr(755,root,root) %{_bindir}/khotnewstuff4
%attr(755,root,root) %{_bindir}/kioclient
%attr(755,root,root) %{_bindir}/kmimetypefinder
%attr(755,root,root) %{_bindir}/knotify4
%attr(755,root,root) %{_bindir}/kquitapp
%attr(755,root,root) %{_bindir}/kreadconfig
%attr(755,root,root) %{_bindir}/kstart
%attr(755,root,root) %{_bindir}/kde4
%attr(755,root,root) %{_bindir}/kwalletd
%attr(755,root,root) %{_bindir}/nepomukserver
%attr(755,root,root) %{_bindir}/nepomukservicestub
%attr(755,root,root) %{_bindir}/ksvgtopng
# conflict with kde3
#%attr(755,root,root) %{_bindir}/ksvgtopng
%attr(755,root,root) %{_bindir}/ktraderclient
%attr(755,root,root) %{_bindir}/ktrash
%attr(755,root,root) %{_bindir}/kuiserver
%attr(755,root,root) %{_bindir}/kwriteconfig
%attr(755,root,root) %{_bindir}/solid-hardware
%attr(755,root,root) %{_libdir}/libkdeinit4_kcmshell4.so
%attr(755,root,root) %{_libdir}/libkdeinit4_khelpcenter.so
%attr(755,root,root) %{_libdir}/libkdeinit4_kuiserver.so
%attr(755,root,root) %{_libdir}/libkdeinit4_kwalletd.so
# Is it ok to add those files to main package?
%attr(755,root,root) %{_libdir}/libkwalletbackend.so.?
%attr(755,root,root) %{_libdir}/libkwalletbackend.so.*.*.*
#
%attr(755,root,root) %{_libdir}/libkdeinit4_nepomukserver.so
%attr(755,root,root) %{_libdir}/kde4/cursorthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/djvuthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/exrthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/htmlthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/imagethumbnail.so
%attr(755,root,root) %{_libdir}/kde4/jpegthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/kcm_cgi.so
%attr(755,root,root) %{_libdir}/kde4/kcm_componentchooser.so
%attr(755,root,root) %{_libdir}/kde4/kcm_emoticons.so
%attr(755,root,root) %{_libdir}/kde4/kcm_icons.so
%attr(755,root,root) %{_libdir}/kde4/kcm_kded.so
%attr(755,root,root) %{_libdir}/kde4/kcm_kdnssd.so
%attr(755,root,root) %{_libdir}/kde4/kcm_knotify.so
%attr(755,root,root) %{_libdir}/kde4/kcm_locale.so
%attr(755,root,root) %{_libdir}/kde4/kcm_trash.so
%attr(755,root,root) %{_libdir}/kde4/kded_kpasswdserver.so
%attr(755,root,root) %{_libdir}/kde4/kded_ktimezoned.so
%attr(755,root,root) %{_libdir}/kde4/kded_remotedirnotify.so
%attr(755,root,root) %{_libdir}/kde4/kded_soliduiserver.so
%attr(755,root,root) %{_libdir}/kde4/kded_desktopnotifier.so
%attr(755,root,root) %{_libdir}/kde4/kded_globalaccel.so
%attr(755,root,root) %{_libdir}/kde4/kio_applications.so
%attr(755,root,root) %{_libdir}/kde4/kio_bookmarks.so
%attr(755,root,root) %{_libdir}/kde4/kio_desktop.so
%attr(755,root,root) %{_libdir}/kde4/kio_about.so
%attr(755,root,root) %{_libdir}/kde4/kio_archive.so
%attr(755,root,root) %{_libdir}/kde4/kio_cgi.so
%attr(755,root,root) %{_libdir}/kde4/kio_filter.so
%attr(755,root,root) %{_libdir}/kde4/kio_finger.so
%attr(755,root,root) %{_libdir}/kde4/kio_fish.so
%attr(755,root,root) %{_libdir}/kde4/kio_floppy.so
%attr(755,root,root) %{_libdir}/kde4/kio_info.so
%attr(755,root,root) %{_libdir}/kde4/kio_man.so
%attr(755,root,root) %{_libdir}/kde4/kio_nepomuksearch.so
%attr(755,root,root) %{_libdir}/kde4/kio_nfs.so
%attr(755,root,root) %{_libdir}/kde4/kio_remote.so
%attr(755,root,root) %{_libdir}/kde4/kio_settings.so
%attr(755,root,root) %{_libdir}/kde4/kio_sftp.so
%attr(755,root,root) %{_libdir}/kde4/kio_smb.so
%attr(755,root,root) %{_libdir}/kde4/kio_thumbnail.so
%attr(755,root,root) %{_libdir}/kde4/kio_trash.so
%attr(755,root,root) %{_libdir}/kde4/libkmanpart.so
%attr(755,root,root) %{_libdir}/kde4/fixhosturifilter.so
%attr(755,root,root) %{_libdir}/kde4/kcm_phonon.so
%attr(755,root,root) %{_libdir}/kde4/kcmspellchecking.so
%attr(755,root,root) %{_libdir}/kde4/kshorturifilter.so
%attr(755,root,root) %{_libdir}/kde4/kuriikwsfilter.so
%attr(755,root,root) %{_libdir}/kde4/kurisearchfilter.so
%attr(755,root,root) %{_libdir}/kde4/localdomainurifilter.so
%attr(755,root,root) %{_libdir}/kde4/librenaudioplugin.so
%attr(755,root,root) %{_libdir}/kde4/librenimageplugin.so
%attr(755,root,root) %{_libdir}/kde4/svgthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/textthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/kcm_nepomuk.so
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
%attr(755,root,root) %{_libdir}/kde4/nepomukfilewatch.so
%attr(755,root,root) %{_libdir}/kde4/nepomukmigration1.so
%attr(755,root,root) %{_libdir}/kde4/nepomukontologyloader.so
%attr(755,root,root) %{_libdir}/kde4/nepomukstorage.so
%attr(755,root,root) %{_libdir}/kde4/nepomukstrigiservice.so
%attr(755,root,root) %{_libdir}/kde4/nepomukqueryservice.so
%dir %{_libdir}/kde4/plugins/styles
%attr(755,root,root) %{_libdir}/strigi/strigiindex_sopranobackend.so
%{_datadir}/apps/drkonqi
%dir %{_datadir}/apps/kcm_componentchooser
%{_datadir}/apps/kcm_componentchooser/kcm_browser.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_filemanager.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_kemail.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_terminal.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_wm.desktop
%{_datadir}/apps/kcmlocale
%{_datadir}/apps/kconf_update/kdedglobalaccel_kde42.upd
%{_datadir}/apps/kconf_update/kuriikwsfilter.upd
%{_datadir}/apps/kde/kde.notifyrc
%{_datadir}/apps/khelpcenter
%{_datadir}/apps/kio_bookmarks
%{_datadir}/apps/kio_finger
%{_datadir}/apps/kio_info
%{_datadir}/apps/kio_man
%{_datadir}/apps/kio_thumbnail
%dir %{_datadir}/apps/konqueror/dirtree
%dir %{_datadir}/apps/konqueror/dirtree/remote
%{_datadir}/apps/konqueror/dirtree/remote/smb-network.desktop
%dir %{_datadir}/apps/remoteview
%{_datadir}/apps/remoteview/smb-network.desktop
%dir %{_datadir}/apps/nepomukstrigiservice
%{_datadir}/apps/nepomukstrigiservice/nepomukstrigiservice.notifyrc
%dir %{_datadir}/apps/nepomukstorage
%{_datadir}/apps/nepomukstorage/nepomukstorage.notifyrc
%dir %{_datadir}/apps/nepomuk
%dir %{_datadir}/apps/nepomuk/ontologies
%{_datadir}/apps/nepomuk/ontologies/*.desktop
%{_datadir}/apps/nepomuk/ontologies/*.rdf*
%{_datadir}/apps/nepomuk/ontologies/*.trig
%{_datadir}/autostart/nepomukserver.desktop
%{_datadir}/config.kcfg/khelpcenter.kcfg
%{_datadir}/config/khotnewstuff.knsrc
%{_datadir}/config/icons.knsrc
%{_datadir}/config/emoticons.knsrc
%{_datadir}/config/kshorturifilterrc
%{_datadir}/dbus-1/interfaces/org.kde.KTimeZoned.xml
%{_datadir}/dbus-1/interfaces/org.kde.khelpcenter.kcmhelpcenter.xml
%{_datadir}/dbus-1/services/org.kde.knotify.service
%{_datadir}/dbus-1/interfaces/org.kde.NepomukServer.xml
%{_datadir}/dbus-1/interfaces/org.kde.nepomuk.ServiceControl.xml
%{_datadir}/dbus-1/interfaces/org.kde.nepomuk.ServiceManager.xml
%{_datadir}/dbus-1/interfaces/org.kde.nepomuk.OntologyManager.xml
%{_datadir}/dbus-1/interfaces/org.kde.nepomuk.Strigi.xml
%{_datadir}/dbus-1/interfaces/org.kde.nepomuk.Storage.xml
%{_datadir}/dbus-1/interfaces/org.kde.nepomuk.Query.xml
%{_datadir}/dbus-1/interfaces/org.kde.nepomuk.QueryService.xml
%{_datadir}/emoticons/kde4
%{_datadir}/kde4/services/about.protocol
%{_datadir}/kde4/services/applications.protocol
%{_datadir}/kde4/services/ar.protocol
%{_datadir}/kde4/services/bookmarks.protocol
%{_datadir}/kde4/services/bzip.protocol
%{_datadir}/kde4/services/bzip2.protocol
%{_datadir}/kde4/services/cgi.protocol
%{_datadir}/kde4/services/componentchooser.desktop
%{_datadir}/kde4/services/cursorthumbnail.desktop
%{_datadir}/kde4/services/djvuthumbnail.desktop
%{_datadir}/kde4/services/emoticons.desktop
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
%{_datadir}/kde4/services/jpegthumbnail.desktop
%{_datadir}/kde4/services/kcm_kdnssd.desktop
%{_datadir}/kde4/services/kcmcgi.desktop
%{_datadir}/kde4/services/kcmkded.desktop
%{_datadir}/kde4/services/kcmnotify.desktop
%{_datadir}/kde4/services/kcm_nepomuk.desktop
%{_datadir}/kde4/services/kcmtrash.desktop
%{_datadir}/kde4/services/kded/kpasswdserver.desktop
%{_datadir}/kde4/services/kded/ktimezoned.desktop
%{_datadir}/kde4/services/kded/remotedirnotify.desktop
%{_datadir}/kde4/services/kded/soliduiserver.desktop
%{_datadir}/kde4/services/kded/kdedglobalaccel.desktop
%{_datadir}/kde4/services/khelpcenter.desktop
%{_datadir}/kde4/services/kmanpart.desktop
%{_datadir}/kde4/services/knotify4.desktop
%{_datadir}/kde4/services/kshorturifilter.desktop
%{_datadir}/kde4/services/kuiserver.desktop
%{_datadir}/kde4/services/kuriikwsfilter.desktop
%{_datadir}/kde4/services/kurisearchfilter.desktop
%{_datadir}/kde4/services/kwalletd.desktop
%{_datadir}/kde4/services/language.desktop
%{_datadir}/kde4/services/localdomainurifilter.desktop
%{_datadir}/kde4/services/man.protocol
%{_datadir}/kde4/services/nepomuksearch.protocol
%{_datadir}/kde4/services/nfs.protocol
%{_datadir}/kde4/services/programs.protocol
%{_datadir}/kde4/services/remote.protocol
%{_datadir}/kde4/services/renaudiodlg.desktop
%{_datadir}/kde4/services/renimagedlg.desktop
%{_datadir}/kde4/services/searchproviders
%{_datadir}/kde4/services/settings.protocol
%{_datadir}/kde4/services/sftp.protocol
%{_datadir}/kde4/services/smb.protocol
%{_datadir}/kde4/services/svgthumbnail.desktop
%{_datadir}/kde4/services/tar.protocol
%{_datadir}/kde4/services/textthumbnail.desktop
%{_datadir}/kde4/services/thumbnail.protocol
%{_datadir}/kde4/services/trash.protocol
%{_datadir}/kde4/services/zip.protocol
%{_datadir}/kde4/services/nepomukfilewatch.desktop
%{_datadir}/kde4/services/nepomukmigration1.desktop
%{_datadir}/kde4/services/nepomukontologyloader.desktop
%{_datadir}/kde4/services/nepomukstorage.desktop
%{_datadir}/kde4/services/nepomukstrigiservice.desktop
%{_datadir}/kde4/services/nepomukqueryservice.desktop
%{_datadir}/kde4/services/desktop.protocol
%{_datadir}/kde4/services/kded/desktopnotifier.desktop
%{_datadir}/kde4/servicetypes/nepomukservice.desktop
%{_datadir}/kde4/servicetypes/searchprovider.desktop
%{_datadir}/kde4/servicetypes/thumbcreator.desktop
%{_datadir}/desktop-directories

%{_datadir}/locale/en_US/*
%dir %{_datadir}/locale/l10n
%{_datadir}/locale/l10n/C
%{_datadir}/locale/l10n/caribbean.desktop
%{_datadir}/locale/l10n/centralafrica.desktop
%{_datadir}/locale/l10n/centralamerica.desktop
%{_datadir}/locale/l10n/centralasia.desktop
%{_datadir}/locale/l10n/centraleurope.desktop
%{_datadir}/locale/l10n/eastafrica.desktop
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
%lang(en) %{_kdedocdir}/en/kcontrol/*
%lang(en) %{_kdedocdir}/en/kdebugdialog
%lang(en) %{_kdedocdir}/en/kdesu
%lang(en) %{_kdedocdir}/en/khelpcenter
%lang(en) %{_kdedocdir}/en/kioslave/bzip2
%lang(en) %{_kdedocdir}/en/kioslave/bookmarks
%lang(en) %{_kdedocdir}/en/kioslave/cgi
%lang(en) %{_kdedocdir}/en/kioslave/finger
%lang(en) %{_kdedocdir}/en/kioslave/fish
%lang(en) %{_kdedocdir}/en/kioslave/floppy
%lang(en) %{_kdedocdir}/en/kioslave/gzip
%lang(en) %{_kdedocdir}/en/kioslave/info
%lang(en) %{_kdedocdir}/en/kioslave/man
%lang(en) %{_kdedocdir}/en/kioslave/nfs
%lang(en) %{_kdedocdir}/en/kioslave/sftp
%lang(en) %{_kdedocdir}/en/kioslave/smb
%lang(en) %{_kdedocdir}/en/kioslave/tar
%lang(en) %{_kdedocdir}/en/kioslave/thumbnail
%lang(en) %{_kdedocdir}/en/knetattach
%lang(en) %{_mandir}/man1/kdesu.1*

%{_datadir}/sounds/*
%{_iconsdir}/hicolor/*/*/*.png
%dir %{_datadir}/apps/ksmserver
%dir %{_datadir}/apps/ksmserver/windowmanagers
%{_datadir}/apps/ksmserver/windowmanagers/compiz-custom.desktop
%{_datadir}/apps/ksmserver/windowmanagers/compiz.desktop
%{_datadir}/apps/ksmserver/windowmanagers/metacity.desktop
%{_datadir}/apps/ksmserver/windowmanagers/openbox.desktop

# dir owned by kdelibs
%{_datadir}/apps/desktoptheme/default/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libkwalletbackend.so
#%{_libdir}/libkaudiodevicelist.so
%{_datadir}/apps/cmake/modules/FindCLucene.cmake
%{_datadir}/apps/cmake/modules/FindPulseAudio.cmake

%files -n kde4-phonon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kconf_update_bin/phonon_devicepreference_update
%attr(755,root,root) %{_libdir}/kconf_update_bin/phonon_deviceuids_update
%attr(755,root,root) %{_libdir}/kde4/kded_phononserver.so
%attr(755,root,root) %{_libdir}/kde4/kcm_phononxine.so
%{_datadir}/kde4/services/kcm_phonon.desktop
%{_datadir}/kde4/services/spellchecking.desktop
%{_datadir}/kde4/servicetypes/phononbackend.desktop
%{_datadir}/kde4/services/kcm_phononxine.desktop

%dir %{_libdir}/kde4/plugins/phonon_platform
%{_libdir}/kde4/plugins/phonon_platform/kde.so
%dir %{_datadir}/apps/kcm_phonon
%{_datadir}/apps/kcm_phonon/listview-background.png
%{_datadir}/apps/kconf_update/devicepreference.upd
%dir %{_datadir}/apps/libphonon
%{_datadir}/apps/libphonon/hardwaredatabase
%dir %{_datadir}/apps/phonon
%{_datadir}/apps/phonon/phonon.notifyrc
%dir %{_datadir}/apps/kio_desktop
%dir %{_datadir}/apps/kio_desktop/DesktopLinks
%{_datadir}/apps/kio_desktop/DesktopLinks/Home.desktop
%{_datadir}/apps/kio_desktop/directory.desktop
%{_datadir}/apps/kio_desktop/directory.trash
%{_datadir}/kde4/services/kded/phononserver.desktop

%files -n kde4-icons-oxygen
%defattr(644,root,root,755)
# digikam has it's own icon in digikam.spec
%exclude %{_iconsdir}/oxygen/*x*/apps/digikam.*
%exclude %{_iconsdir}/oxygen/*x*/apps/showfoto.*
%{_iconsdir}/oxygen/*x*/actions/*
%{_iconsdir}/oxygen/*x*/apps/*
%{_iconsdir}/oxygen/*x*/categories/*
%{_iconsdir}/oxygen/*x*/devices/*
%{_iconsdir}/oxygen/*x*/mimetypes/*
%{_iconsdir}/oxygen/*x*/places/*
%{_iconsdir}/oxygen/*x*/status/*
%{_iconsdir}/oxygen/*x*/animations/*
%{_iconsdir}/oxygen/*x*/emblems/*
%{_iconsdir}/oxygen/*x*/emotes/*
%{_iconsdir}/oxygen/index.theme

%files -n kde4-icons-oxygen-svg
%defattr(644,root,root,755)
%dir %{_iconsdir}/oxygen/scalable
# digikam has it's own icon in digikam.spec
%exclude %{_iconsdir}/oxygen/scalable/apps/digikam.*
%{_iconsdir}/oxygen/scalable/text-formatting.svg
%{_iconsdir}/oxygen/scalable/actions
%{_iconsdir}/oxygen/scalable/apps
%{_iconsdir}/oxygen/scalable/categories
%{_iconsdir}/oxygen/scalable/devices
%{_iconsdir}/oxygen/scalable/emblems
%{_iconsdir}/oxygen/scalable/emotes
%{_iconsdir}/oxygen/scalable/mimetypes
%{_iconsdir}/oxygen/scalable/places
%{_iconsdir}/oxygen/scalable/status
%{_iconsdir}/hicolor/scalable/apps/*.svgz

%files -n kde4-style-oxygen
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde4/kstyle_oxygen_config.so
%attr(755,root,root) %{_libdir}/kde4/plugins/styles/oxygen.so
%{_datadir}/apps/kstyle/themes/oxygen.themerc
