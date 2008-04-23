
%define version 1.0.0
%define snapshot 302
%define rel	1

%define major	1
%define libname	%mklibname mirage %major
%define pluname	%mklibname mirage-plugins
%define devname	%mklibname mirage -d
%define staname	%mklibname mirage -d -s

%if 0
# Update commands:
REV=$(svn info https://cdemu.svn.sourceforge.net/svnroot/cdemu/trunk/libmirage| sed -ne 's/^Last Changed Rev: //p')
svn export -r $REV https://cdemu.svn.sourceforge.net/svnroot/cdemu/trunk/libmirage libmirage-$REV
tar -cjf libmirage-$REV.tar.bz2 libmirage-$REV
%endif

Name:		libmirage
Version:	%version
Summary:	CD-ROM image access library
%if %snapshot
Release:	%mkrel 1.svn%snapshot.%rel
Source:		%name-%snapshot.tar.bz2
%else
Release:	%mkrel %rel
Source:		http://downloads.sourceforge.net/cdemu/%name-%version.tar.bz2
%endif
Group:		System/Libraries
License:	GPLv2+
URL:		http://cdemu.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	gtk-doc
BuildRequires:	bison
BuildRequires:	sndfile-devel
BuildRequires:	glib2-devel
BuildRequires:	zlib-devel

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
%if %snapshot
%setup -q -n %name-%snapshot
%else
%setup -q
%endif

%build
%if %snapshot
./autogen.sh
%endif
%configure2_5x
%make

%install
rm -rf %buildroot
%makeinstall_std

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %pluname
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libmirage.so.%{major}*

%files -n %devname
%defattr(-,root,root)
%doc README AUTHORS
%{_includedir}/libmirage*
%{_libdir}/libmirage.so
%{_libdir}/libmirage.la
%{_libdir}/pkgconfig/libmirage.pc

%files -n %staname
%defattr(-,root,root)
%{_libdir}/libmirage.a
%{_libdir}/%{name}/*.a
%{_libdir}/%{name}/*.la
