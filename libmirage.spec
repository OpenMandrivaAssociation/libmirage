%define version 1.5.0
%define rel	1

%define major	6
%define libname	%mklibname mirage %major
%define devname	%mklibname mirage -d

Name:		libmirage
Version:	%version
Summary:	CD-ROM image access library
Release:	%rel
Source0:	http://downloads.sourceforge.net/cdemu/%name-%version.tar.bz2
Group:		System/Libraries
License:	GPLv2+
URL:		http://cdemu.sourceforge.net/

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

%package common
Summary:	CD-ROM image access library - common files
Group:		System/Libraries
Obsoletes:	%{_lib}mirage-plugins < 1.3.0
# to ease upgrades (old libmirageX depend on this):
Provides:	%{_lib}mirage-plugins = %{version}

%description common
Image access plugins for libMirage.

%package -n %libname
Summary:	CD-ROM image access library - shared library
Group:		System/Libraries
Requires:	%{name}-common >= %{version}-%{release}

%description -n %libname
Shared libraries of libMirage for software using it.

%package -n %devname
Summary:	CD-ROM image access library - development headers
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	mirage-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
# to ease upgrade - in reality the static lib was dropped
Obsoletes:	%{_lib}mirage-static-devel

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

%prep
%setup -q
# See bug #58086
# The mirage defined mime types shadow the fd.o mimetypes, defining an alias
# to the standard name. For example, *.iso files get classified as
# "application/libmirage-iso". The mirage .xml file does define an alias
# "application/x-cd-image". However, the fd.o shared-mime-info specification
# forbids having aliases that conflict with mimetypes defined elsewhere. 
# Therefore at least KDE ignores such aliases, causing .iso and .cue pointing
# to the libmirage mime types only.
# For now, lessen the priorities and weights of libmirage definitions so that
# fd.o provided mimetype definitions take priority. - Anssi 04/2010
sed -i -e 's,priority="50",priority="48",' -e 's,glob pattern,glob weight="48" pattern,' src/parsers/*/libmirage-image-*.xml

%build
autoreconf -fi
%configure2_5x --with-plugin-dir=%{_libdir}/%{name}-%{major} --disable-static
%make

%install
%makeinstall_std

rm -f %{buildroot}/%{_libdir}/%{name}*/{*.la,*.a}

%files common
%{_datadir}/mime/packages/libmirage-image*.xml

%files -n %libname
%{_libdir}/%{name}-%{major}
%{_libdir}/libmirage.so.%{major}*

%files -n %devname
%doc README AUTHORS
%{_includedir}/libmirage
%{_libdir}/libmirage.so
%{_libdir}/pkgconfig/libmirage.pc
%{_datadir}/gtk-doc/html/libmirage



%changelog
* Mon Jan 23 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.5.0-1
+ Revision: 767431
- version update 1.5.0

* Wed Nov 23 2011 Alexander Khrukin <akhrukin@mandriva.org> 1.4.0-1
+ Revision: 732831
- version update to 1.4.0

* Sat Sep 04 2010 Anssi Hannula <anssi@mandriva.org> 1.3.0-1mdv2011.0
+ Revision: 575728
- new version
- drop static library
- move plugins to main library package, to a major-specific directory
- add common subpackage for mimetype files
- remove old compatibility cruft

* Sat Apr 17 2010 Anssi Hannula <anssi@mandriva.org> 1.2.0-2mdv2010.1
+ Revision: 536052
- lower the priorities and weights of mimetype definitions, preferring
  the fd.o defined types over libmirage ones (fixes #58086)

* Thu Dec 03 2009 Funda Wang <fwang@mandriva.org> 1.2.0-1mdv2010.1
+ Revision: 472891
- really rediff patch
- New version 1.2.0

  + Ahmad Samir <ahmadsamir@mandriva.org>
    - rediff patch1

* Sun Sep 13 2009 Thierry Vignaud <tv@mandriva.org> 1.1.1-3mdv2010.0
+ Revision: 438712
- rebuild

* Tue Jan 27 2009 Guillaume Bedot <littletux@mandriva.org> 1.1.1-2mdv2009.1
+ Revision: 334081
- bump rel, re-submit
- move mime types to the plugins' package
- Release 1.1.1

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Apr 23 2008 Anssi Hannula <anssi@mandriva.org> 1.0.0-1.svn302.1mdv2009.0
+ Revision: 196922
- initial Mandriva release

