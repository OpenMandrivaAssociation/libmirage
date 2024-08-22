%define		major 11
%define		api_version 3.2
%define		gir_major 3.2
%define		libname %mklibname mirage %{major}
%define		devname %mklibname mirage -d
%define		girname %mklibname mirage-gir %{gir_major}

Summary:	CD-ROM image access library
Name:		libmirage
Version:	3.2.8
Release:	1
License:	GPLv2+
Group:		System/Libraries
Source0:	http://downloads.sourceforge.net/cdemu/%{name}-%{version}.tar.xz
Url:		http://cdemu.sourceforge.net/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	cmake
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	intltool

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

#----------------------------------------------------------------------------

%package common
Summary:	CD-ROM image access library - common files
Group:		System/Libraries

%description common
Image access plugins for libMirage.

%files common
%{_datadir}/mime/packages/libmirage-*.xml
%{_datadir}/locale/*/LC_MESSAGES/libmirage.mo

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	CD-ROM image access library - shared library
Group:		System/Libraries
Requires:	%{name}-common >= %{EVRD}

%description -n %{libname}
Shared libraries of libMirage for software using it.

%files -n %{libname}
%{_libdir}/%{name}-%{api_version}
%{_libdir}/libmirage.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	CD-ROM image access library - development headers
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{girname} = %{EVRD}

%description -n %{devname}
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

%files -n %{devname}
%doc README AUTHORS
%{_includedir}/%{name}-%{api_version}
%{_libdir}/libmirage.so
%{_libdir}/pkgconfig/libmirage.pc
%{_datadir}/gir-1.0/Mirage-%{gir_major}.gir
%{_datadir}/gtk-doc/html/libmirage

#----------------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/Mirage-%{gir_major}.typelib

#----------------------------------------------------------------------------

%prep
%autosetup -p1

# See Mandriva bug #58086
# The mirage defined mime types shadow the fd.o mimetypes, defining an alias
# to the standard name. For example, *.iso files get classified as
# "application/libmirage-iso". The mirage .xml file does define an alias
# "application/x-cd-image". However, the fd.o shared-mime-info specification
# forbids having aliases that conflict with mimetypes defined elsewhere. 
# Therefore at least KDE ignores such aliases, causing .iso and .cue pointing
# to the libmirage mime types only.
# For now, lessen the priorities and weights of libmirage definitions so that
# fd.o provided mimetype definitions take priority. - Anssi 04/2010
#sed -i -e 's,priority="50",priority="48",' -e 's,glob pattern,glob weight="48" pattern,' %{buildroot}%{_datadir}/mime/packages/libmirage-*.xml

%build
%cmake -DPOST_INSTALL_HOOKS:BOOL=OFF
%make_build

%install
%make_install -C build

