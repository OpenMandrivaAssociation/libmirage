%define version 1.2.0
%define rel	1

%define major	2
%define libname	%mklibname mirage %major
%define pluname	%mklibname mirage-plugins
%define devname	%mklibname mirage -d
%define staname	%mklibname mirage -d -s

Name:		libmirage
Version:	%version
Summary:	CD-ROM image access library
Release:	%mkrel %rel
Source:		http://downloads.sourceforge.net/cdemu/%name-%version.tar.bz2
Patch0:		libmirage-1.2.0-mdv-format-security.patch
Patch1:		libmirage-1.2.0-linkage.patch
Group:		System/Libraries
License:	GPLv2+
URL:		http://cdemu.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-root

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	sndfile-devel
BuildRequires:	glib2-devel
BuildRequires:	zlib-devel
BuildRequires:	gtk-doc

%description
The aim of libMirage is to provide uniform access to the data stored in
different image formats, by creating a representation of disc stored in image
file, which is based on GObjects. There are various objects that represent
different parts of the disc; disc, session, track, sector, etc. In addition to
providing access to data provided by the image file, libMirage is also capable
of generating some of the data that might not be present in image file. For
instance, ISO image provides only user data from sector, without sync pattern,
header, ECC/EDC codes or subchannel. When this missing data is requested,
libMirage will transparently generate it.

%package -n %pluname
Summary:	CD-ROM image access library - shared plugins
Group:		System/Libraries

%description -n %pluname
Image access plugins for libMirage.

%package -n %libname
Summary:	CD-ROM image access library - shared library
Group:		System/Libraries
Requires:	%pluname >= %{version}-%{release}

%description -n %libname
Shared libraries of libMirage for software using it.

%package -n %devname
Summary:	CD-ROM image access library - development headers
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	mirage-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %devname
Development headers for developing software using libMirage.

The aim of libMirage is to provide uniform access to the data stored in
different image formats, by creating a representation of disc stored in image
file, which is based on GObjects. There are various objects that represent
different parts of the disc; disc, session, track, sector, etc. In addition to
providing access to data provided by the image file, libMirage is also capable
of generating some of the data that might not be present in image file. For
instance, ISO image provides only user data from sector, without sync pattern,
header, ECC/EDC codes or subchannel. When this missing data is requested,
libMirage will transparently generate it.

%package -n %staname
Summary:	CD-ROM image access library - static libraries
Group:		Development/C
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	mirage-static-devel = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}

%description -n %staname
Static libraries for developing static programs using libMirage.

%prep
%setup -q
%patch0 -p0 -b .format-security
%patch1 -p0 -b .link

%build
autoreconf -fi
%configure2_5x
%make

%install
rm -rf %buildroot
%makeinstall_std

rm -f %{buildroot}/%{_libdir}/%{name}*/{*.la,*.a}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post -n %pluname
%update_mime_database

%postun -n %pluname
%clean_mime_database

%files -n %pluname
%defattr(-,root,root)
%{_libdir}/%{name}-1.2
%{_datadir}/mime/packages/libmirage-image*.xml

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libmirage.so.%{major}*

%files -n %devname
%defattr(-,root,root)
%doc README AUTHORS
%{_includedir}/libmirage
%{_libdir}/libmirage.so
%{_libdir}/libmirage.la
%{_libdir}/pkgconfig/libmirage.pc
%{_datadir}/gtk-doc/html/libmirage

%files -n %staname
%defattr(-,root,root)
%{_libdir}/libmirage.a
