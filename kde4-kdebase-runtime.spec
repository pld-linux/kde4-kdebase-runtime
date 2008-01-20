# Conditional build:
%bcond_without	apidocs		# do not prepare API documentation
%bcond_without	hidden_visibility	# pass '--fvisibility=hidden'
					# & '--fvisibility-inlines-hidden'
					# to g++

%define		_state		stable
%define		_minlibsevr	9:%{version}
%define		_minbaseevr	9:%{version}

Summary:	KDE4 runtime
%define	orgname	kdebase-runtime
Name:		kdebase4-runtime
Version:	4.0.0
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/latest/src/%{orgname}-%{version}.tar.bz2
# Source0-md5:	da93f59497ff90ad01bd4ab9b458f6cb
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_hidden_visibility:BuildRequires:	gcc-c++ >= 5:4.1.0-0.20051206r108118.1}
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	kdelibs4-devel >= %{_minlibsevr}
%{?with_apidocs:BuildRequires:	qt4-doc}
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	xine-lib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreq      libtool(.*)

%description

%package devel
Summary:	Development files for KDE4 runtime
Summary(pl.UTF-8):	Pliki nagłówkowe do KDE pim
Summary(ru.UTF-8):	Файлы разработки для kdepim
Summary(uk.UTF-8):	Файли розробки для kdepim
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	kdelibs4-devel >= %{_minlibsevr}

%description devel

%prep
%setup -q -n %{orgname}-%{version}

%build
export QTDIR=%{_prefix}
mkdir build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post		-p /sbin/ldconfig
%postun		-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/kde4/*.so
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/kde4/libexec/*
%attr(755,root,root) %{_libdir}/kde4/plugins/styles/*.so
%{_iconsdir}/oxygen
%{_datadir}/applications/kde4/*
# this should be probably a separate package
%{_datadir}/apps/khelpcenter
#
%{_datadir}/emoticons/kde4
%{_datadir}/kde4/services


%files devel
%defattr(644,root,root,755)
