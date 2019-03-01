#
# Conditional build:
%bcond_without	ntrack		# network status tracking

%define		_state		stable
%define		orgname		kde-runtime
%define		qt_ver		4.8.3
%define		attica_ver	0.4.0
%define		kactivities_ver	4.13.0

Summary:	KDE 4 base runtime components
Summary(pl.UTF-8):	Komponenty uruchomieniowe podstawowej części KDE 4
Name:		kde4-kdebase-runtime
Version:	4.14.3
Release:	10
License:	GPL v2+
Group:		X11/Applications
Source0:	http://download.kde.org/%{_state}/%{version}/src/%{orgname}-%{version}.tar.xz
# Source0-md5:	fbba547e4446b51702e5de8bcae078d5
Source1:	kdebase-searchproviders.tar.bz2
# Source1-md5:	126c3524b5367f5096a628acbf9dc86f
Source2:	l10n-iso639-1
Patch100:	%{name}-branch.diff
Patch0:		%{name}-rpc.patch
Patch1:		moc.patch
Patch2:		%{name}-exiv2.patch
URL:		http://www.kde.org/
BuildRequires:	NetworkManager-devel >= 0.7.0
BuildRequires:	OpenEXR-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	attica-devel >= %{attica_ver}
BuildRequires:	automoc4 >= 0.9.88
BuildRequires:	bzip2-devel
BuildRequires:	clucene-core-devel >= 0.9.21
BuildRequires:	cmake >= 2.8.0
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	exiv2-devel >= 0.18.2
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gpgme-devel
BuildRequires:	kde4-kactivities-devel >= %{kactivities_ver}
BuildRequires:	kde4-kdelibs-devel >= %{version}
BuildRequires:	kde4-kdepimlibs-devel >= %{version}
BuildRequires:	kde4-nepomuk-core-devel >= %{version}
BuildRequires:	libcanberra-devel
BuildRequires:	libgcrypt-devel >= 1.5.0
BuildRequires:	libjpeg-devel
BuildRequires:	libsmbclient-devel
BuildRequires:	libssh-devel >= 1:0.6.0
BuildRequires:	libtirpc-devel
BuildRequires:	libwebp-devel
%{?with_ntrack:BuildRequires:	ntrack-qt4-devel}
BuildRequires:	openslp-devel
BuildRequires:	phonon-devel >= 4.4.57
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel >= 0.9.16
BuildRequires:	qca-devel >= 2.0.0
BuildRequires:	qt4-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	shared-desktop-ontologies-devel >= 0.7.1
BuildRequires:	shared-mime-info
BuildRequires:	soprano-devel >= 2.6.51
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xz
BuildRequires:	xz-devel
Requires:	attica >= %{attica_ver}
Requires:	exiv2-libs >= 0.18.2
Requires:	kde4-kactivities >= %{kactivities_ver}
Requires:	kde4-kdelibs >= %{version}
Requires:	kde4-kdepimlibs >= %{version}
Requires:	kde4-nepomuk-core >= %{version}
Requires:	libgcrypt >= 1.5.0
Requires:	libssh >= 1:0.6.0
Requires:	phonon >= 4.4.57
Requires:	pulseaudio-libs >= 0.9.16
Provides:	dbus(org.freedesktop.Notifications)
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
Requires:	phonon >= 4.4.57

%description -n kde4-phonon
KDE 4 Phonon plugins.

%description -n kde4-phonon -l pl.UTF-8
Wtyczki KDE 4 dla Phonona.

%prep
%setup -q -n %{orgname}-%{version} -a1
#%patch100 -p1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake \
	%{!?with_ntrack:-DQNTRACK=BOOL:FALSE} \
	-DLIBEXEC_INSTALL_DIR=%{_libdir}/kde4/libexec \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

install -d $RPM_BUILD_ROOT%{_datadir}/kde4/services/searchproviders/pld
cp -a kdebase-searchproviders/*.desktop $RPM_BUILD_ROOT%{_datadir}/kde4/services/searchproviders/pld

# l10n dir contains per-country (ISO-3166 alpha2 indexed) localization; rpm uses per-language (ISO-639 alpha2 or alpha3) tags
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
%attr(755,root,root) %{_bindir}/khotnewstuff-upload
%attr(755,root,root) %{_bindir}/kioclient
%attr(755,root,root) %{_bindir}/kmimetypefinder
%attr(755,root,root) %{_bindir}/knotify4
%attr(755,root,root) %{_bindir}/kquitapp
%attr(755,root,root) %{_bindir}/kreadconfig
%attr(755,root,root) %{_bindir}/kstart
%attr(755,root,root) %{_bindir}/kde4
%attr(755,root,root) %{_bindir}/kwalletd
%attr(755,root,root) %{_bindir}/ksvgtopng
%attr(755,root,root) %{_bindir}/keditfiletype
%attr(755,root,root) %{_bindir}/kglobalaccel
%attr(755,root,root) %{_bindir}/ktraderclient
%attr(755,root,root) %{_bindir}/ktrash
%attr(755,root,root) %{_bindir}/kuiserver
%attr(755,root,root) %{_bindir}/kwriteconfig
%attr(755,root,root) %{_bindir}/solid-hardware
%attr(755,root,root) %{_bindir}/plasma-remote-helper
%attr(755,root,root) %{_bindir}/plasmapkg
%attr(755,root,root) %{_libdir}/attica_kde.so
%attr(755,root,root) %{_libdir}/libkdeinit4_kcmshell4.so
%attr(755,root,root) %{_libdir}/libkdeinit4_khelpcenter.so
%attr(755,root,root) %{_libdir}/libkdeinit4_kuiserver.so
%attr(755,root,root) %{_libdir}/libkdeinit4_kwalletd.so
%attr(755,root,root) %{_libdir}/libkdeinit4_kglobalaccel.so
%attr(755,root,root) %{_libdir}/libknotifyplugin.so
# Is it ok to add those files to main package?
%attr(755,root,root) %ghost %{_libdir}/libkwalletbackend.so.4
%attr(755,root,root) %{_libdir}/libkwalletbackend.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmolletnetwork.so.4
%attr(755,root,root) %{_libdir}/libmolletnetwork.so.4.*.*
%attr(755,root,root) %{_libdir}/kde4/comicbookthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/cursorthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/djvuthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/exrthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/htmlthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/imagethumbnail.so
%attr(755,root,root) %{_libdir}/kde4/jpegthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/kcm_cgi.so
%attr(755,root,root) %{_libdir}/kde4/kcm_componentchooser.so
%attr(755,root,root) %{_libdir}/kde4/kcm_device_automounter.so
%attr(755,root,root) %{_libdir}/kde4/kcm_emoticons.so
%attr(755,root,root) %{_libdir}/kde4/kcm_filetypes.so
%attr(755,root,root) %{_libdir}/kde4/kcm_icons.so
%attr(755,root,root) %{_libdir}/kde4/kcm_kded.so
%attr(755,root,root) %{_libdir}/kde4/kcm_kdnssd.so
%attr(755,root,root) %{_libdir}/kde4/kcm_knotify.so
%attr(755,root,root) %{_libdir}/kde4/kcm_locale.so
%attr(755,root,root) %{_libdir}/kde4/kcm_trash.so
%attr(755,root,root) %{_libdir}/kde4/kded_device_automounter.so
%attr(755,root,root) %{_libdir}/kde4/kded_kpasswdserver.so
%attr(755,root,root) %{_libdir}/kde4/kded_ktimezoned.so
%attr(755,root,root) %{_libdir}/kde4/kded_remotedirnotify.so
%attr(755,root,root) %{_libdir}/kde4/kded_soliduiserver.so
%attr(755,root,root) %{_libdir}/kde4/kded_desktopnotifier.so
%attr(755,root,root) %{_libdir}/kde4/kded_networkstatus.so
%attr(755,root,root) %{_libdir}/kde4/kded_networkwatcher.so
%attr(755,root,root) %{_libdir}/kde4/kded_recentdocumentsnotifier.so
%attr(755,root,root) %{_libdir}/kde4/kded_solidautoeject.so
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
%attr(755,root,root) %{_libdir}/kde4/kio_network.so
%attr(755,root,root) %{_libdir}/kde4/kio_nfs.so
%attr(755,root,root) %{_libdir}/kde4/kio_recentdocuments.so
%attr(755,root,root) %{_libdir}/kde4/kio_remote.so
%attr(755,root,root) %{_libdir}/kde4/kio_settings.so
%attr(755,root,root) %{_libdir}/kde4/kio_sftp.so
%attr(755,root,root) %{_libdir}/kde4/kio_smb.so
%attr(755,root,root) %{_libdir}/kde4/kio_thumbnail.so
%attr(755,root,root) %{_libdir}/kde4/kio_trash.so
%attr(755,root,root) %{_libdir}/kde4/libkmanpart.so
%attr(755,root,root) %{_libdir}/kde4/fixhosturifilter.so
%attr(755,root,root) %{_libdir}/kde4/kcm_attica.so
%attr(755,root,root) %{_libdir}/kde4/kcm_phonon.so
%attr(755,root,root) %{_libdir}/kde4/kcmspellchecking.so
%attr(755,root,root) %{_libdir}/kde4/kshorturifilter.so
%attr(755,root,root) %{_libdir}/kde4/kuriikwsfilter.so
%attr(755,root,root) %{_libdir}/kde4/kurisearchfilter.so
%attr(755,root,root) %{_libdir}/kde4/localdomainurifilter.so
%attr(755,root,root) %{_libdir}/kde4/librenaudioplugin.so
%attr(755,root,root) %{_libdir}/kde4/librenimageplugin.so
%attr(755,root,root) %{_libdir}/kde4/plasma-kpart.so
%attr(755,root,root) %{_libdir}/kde4/plasma_appletscript_declarative.so
%attr(755,root,root) %{_libdir}/kde4/plasma_appletscript_simple_javascript.so
%attr(755,root,root) %{_libdir}/kde4/plasma_containment_newspaper.so
%attr(755,root,root) %{_libdir}/kde4/plasma_dataenginescript_javascript.so
%attr(755,root,root) %{_libdir}/kde4/plasma_packagestructure_javascriptaddon.so
%attr(755,root,root) %{_libdir}/kde4/plasma_runnerscript_javascript.so
%attr(755,root,root) %{_libdir}/kde4/svgthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/textthumbnail.so
%attr(755,root,root) %{_libdir}/kde4/windowsexethumbnail.so
%attr(755,root,root) %{_libdir}/kde4/windowsimagethumbnail.so

%attr(755,root,root) %{_libdir}/kde4/imports

%attr(755,root,root) %{_libdir}/kde4/plugins/imageformats/kimg_webp.so

%attr(755,root,root) %{_libdir}/kde4/libexec/drkonqi
#%attr(755,root,root) %{_libdir}/kde4/libexec/installdbgsymbols.sh
%attr(755,root,root) %{_libdir}/kde4/libexec/kdeeject
%attr(755,root,root) %{_libdir}/kde4/libexec/kdesu
%attr(755,root,root) %{_libdir}/kde4/libexec/kdesud
%attr(755,root,root) %{_libdir}/kde4/libexec/kdontchangethehostname
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_docbookdig.pl
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_htdig.pl
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_htsearch.pl
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_indexbuilder
%attr(755,root,root) %{_libdir}/kde4/libexec/khc_mansearch.pl
%attr(755,root,root) %{_libdir}/kde4/libexec/kioexec
%attr(755,root,root) %{_libdir}/kde4/libexec/knetattach
%attr(755,root,root) %{_libdir}/kde4/libexec/kcmremotewidgetshelper
%{_libdir}/kde4/platformimports
%{_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmremotewidgets.conf
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmremotewidgets.policy
%{_datadir}/apps/drkonqi
%{_datadir}/apps/hardwarenotifications
%dir %{_datadir}/apps/kcm_componentchooser
%{_datadir}/apps/kcm_componentchooser/kcm_browser.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_filemanager.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_kemail.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_terminal.desktop
%{_datadir}/apps/kcm_componentchooser/kcm_wm.desktop
%{_datadir}/apps/kcmlocale
%{_datadir}/apps/kconf_update/kuriikwsfilter.upd
%{_datadir}/apps/kconf_update/kwallet-4.13.upd
%{_datadir}/apps/kconf_update/drkonqi-rename-config-section.upd
%{_datadir}/apps/kde/kde.notifyrc
%dir %{_datadir}/apps/kglobalaccel
%{_datadir}/apps/kglobalaccel/kglobalaccel.notifyrc
%{_datadir}/apps/khelpcenter
%{_datadir}/apps/kio_bookmarks
%{_datadir}/apps/kio_finger
%{_datadir}/apps/kio_info
#%{_datadir}/apps/kio_thumbnail
%dir %{_datadir}/apps/konqueror/dirtree
%dir %{_datadir}/apps/konqueror/dirtree/remote
%{_datadir}/apps/konqueror/dirtree/remote/smb-network.desktop
%dir %{_datadir}/apps/remoteview
%{_datadir}/apps/remoteview/smb-network.desktop
%{_datadir}/config.kcfg/khelpcenter.kcfg
%{_datadir}/config.kcfg/jpegcreatorsettings.kcfg
%{_datadir}/config/khotnewstuff.knsrc
%{_datadir}/config/icons.knsrc
%{_datadir}/config/emoticons.knsrc
%{_datadir}/config/kshorturifilterrc
%{_datadir}/config/khotnewstuff_upload.knsrc
%{_datadir}/dbus-1/services/org.kde.knotify.service
%{_datadir}/dbus-1/services/org.kde.kuiserver.service
# xml files to -devel (or have some runtime users?)
%{_datadir}/dbus-1/interfaces/org.kde.KTimeZoned.xml
%{_datadir}/dbus-1/interfaces/org.kde.khelpcenter.kcmhelpcenter.xml
%{_datadir}/dbus-1/interfaces/org.kde.network.kioslavenotifier.xml
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmremotewidgets.service
%{_datadir}/emoticons/kde4
%{_datadir}/kde4/services/qimageioplugins/webp.desktop
%{_datadir}/kde4/services/about.protocol
%{_datadir}/kde4/services/applications.protocol
%{_datadir}/kde4/services/ar.protocol
%{_datadir}/kde4/services/kcm_attica.desktop
%{_datadir}/kde4/services/bookmarks.protocol
%{_datadir}/kde4/services/bzip.protocol
%{_datadir}/kde4/services/bzip2.protocol
%{_datadir}/kde4/services/cgi.protocol
%{_datadir}/kde4/services/comicbookthumbnail.desktop
%{_datadir}/kde4/services/componentchooser.desktop
%{_datadir}/kde4/services/cursorthumbnail.desktop
%{_datadir}/kde4/services/device_automounter_kcm.desktop
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
%{_datadir}/kde4/services/kcmtrash.desktop
%{_datadir}/kde4/services/kded/device_automounter.desktop
%{_datadir}/kde4/services/kded/kpasswdserver.desktop
%{_datadir}/kde4/services/kded/ktimezoned.desktop
%{_datadir}/kde4/services/kded/networkstatus.desktop
%{_datadir}/kde4/services/kded/remotedirnotify.desktop
%{_datadir}/kde4/services/kded/soliduiserver.desktop
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
%{_datadir}/kde4/services/lzma.protocol
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
%{_datadir}/kde4/services/svgthumbnail.desktop
%{_datadir}/kde4/services/tar.protocol
%{_datadir}/kde4/services/textthumbnail.desktop
%{_datadir}/kde4/services/thumbnail.protocol
%{_datadir}/kde4/services/trash.protocol
%{_datadir}/kde4/services/zip.protocol
%{_datadir}/kde4/services/xz.protocol
%{_datadir}/kde4/services/desktop.protocol
%{_datadir}/kde4/services/kded/desktopnotifier.desktop
%{_datadir}/kde4/services/desktopthumbnail.desktop
%{_datadir}/kde4/services/directorythumbnail.desktop
%{_datadir}/kde4/services/filetypes.desktop
%{_datadir}/kde4/services/kded/networkwatcher.desktop
%{_datadir}/kde4/services/kded/solidautoeject.desktop
%{_datadir}/kde4/services/kded/recentdocumentsnotifier.desktop
%{_datadir}/kde4/services/kglobalaccel.desktop
%{_datadir}/kde4/services/network.protocol
%{_datadir}/kde4/services/plasma-containment-newspaper.desktop
%{_datadir}/kde4/services/plasma-kpart.desktop
%{_datadir}/kde4/services/plasma-packagestructure-javascript-addon.desktop
%{_datadir}/kde4/services/plasma-scriptengine-applet-declarative.desktop
%{_datadir}/kde4/services/plasma-scriptengine-applet-simple-javascript.desktop
%{_datadir}/kde4/services/plasma-scriptengine-dataengine-javascript.desktop
%{_datadir}/kde4/services/plasma-scriptengine-runner-javascript.desktop
%{_datadir}/kde4/services/recentdocuments.protocol
%{_datadir}/kde4/services/windowsexethumbnail.desktop
%{_datadir}/kde4/services/windowsimagethumbnail.desktop
%{_datadir}/kde4/servicetypes/knotifynotifymethod.desktop
%{_datadir}/kde4/servicetypes/plasma-javascriptaddon.desktop
%{_datadir}/kde4/servicetypes/searchprovider.desktop
%{_datadir}/kde4/servicetypes/thumbcreator.desktop
%{_datadir}/desktop-directories
%{_datadir}/mime/packages/network.xml
%{_datadir}/mime/packages/webp.xml

#%{_datadir}/locale/en_US/*
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
# really?
%{_datadir}/locale/currency

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
%{_mandir}/man1/kdesu.1*
%{_mandir}/man1/plasmapkg.1*

%{_datadir}/sounds/KDE-*.ogg
%{_iconsdir}/hicolor/*x*/apps/knetattach.png
%dir %{_datadir}/apps/ksmserver
%dir %{_datadir}/apps/ksmserver/windowmanagers
%{_datadir}/apps/ksmserver/windowmanagers/compiz-custom.desktop
%{_datadir}/apps/ksmserver/windowmanagers/compiz.desktop
%{_datadir}/apps/ksmserver/windowmanagers/metacity.desktop
%{_datadir}/apps/ksmserver/windowmanagers/openbox.desktop
%{_datadir}/apps/kio_docfilter
%dir %{_datadir}/apps/konqsidebartng
%dir %{_datadir}/apps/konqsidebartng/virtual_folders
%dir %{_datadir}/apps/konqsidebartng/virtual_folders/remote
%{_datadir}/apps/konqsidebartng/virtual_folders/remote/virtualfolder_network.desktop
%{_datadir}/apps/kwalletd
%{_datadir}/apps/remoteview/network.desktop

# dir owned by kdelibs
%{_datadir}/apps/desktoptheme/default/dialogs
%{_datadir}/apps/desktoptheme/default/icons
%{_datadir}/apps/desktoptheme/default/opaque
%{_datadir}/apps/desktoptheme/default/toolbar-icons
%{_datadir}/apps/desktoptheme/default/translucent
%{_datadir}/apps/desktoptheme/default/widgets
%{_datadir}/apps/desktoptheme/default/colors
%{_datadir}/apps/desktoptheme/default/metadata.desktop
%{_datadir}/apps/desktoptheme/oxygen
%{_datadir}/apps/desktoptheme/appdashboard

%files devel
%defattr(644,root,root,755)
%{_includedir}/knotify*.h
%attr(755,root,root) %{_libdir}/libkwalletbackend.so
%attr(755,root,root) %{_libdir}/libmolletnetwork.so
%{_datadir}/apps/cmake/modules/FindCLucene.cmake
%{_datadir}/apps/cmake/modules/FindSLP.cmake

%files -n kde4-phonon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kconf_update_bin/phonon_devicepreference_update
%attr(755,root,root) %{_libdir}/kconf_update_bin/phonon_deviceuids_update
%attr(755,root,root) %{_libdir}/kde4/kded_phononserver.so
%{_datadir}/kde4/services/kcm_phonon.desktop
%{_datadir}/kde4/services/spellchecking.desktop
%{_datadir}/kde4/servicetypes/phononbackend.desktop

%dir %{_libdir}/kde4/plugins/phonon_platform
%attr(755,root,root) %{_libdir}/kde4/plugins/phonon_platform/kde.so
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
