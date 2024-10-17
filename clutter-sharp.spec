#gw it could even become a noarch package, but it has a dep
#on the clutter library packages
%define debug_package %{nil}

%define cluttergtklibname %mklibname clutter-gtk 1.0 0

%define gitdate 20090817

Summary:	C#/.NET bindings to Clutter
Name:		clutter-sharp
Version:	0
Release:	0.%{gitdate}.5
License:	MIT
Group:		System/Libraries
Url:		https://www.clutter-project.org
Source0:	%{name}-%{gitdate}.tar.xz
Patch0:		clutter-sharp-20090817-ilasm-build.patch
Patch1:		clutter-sharp-20090828-initialization-fix.patch
BuildRequires:	gtk-sharp2
BuildRequires:	glib-sharp2
BuildRequires:	pkgconfig(clutter-gtk-1.0)
BuildRequires:	pkgconfig(gapi-2.0)
BuildRequires:	pkgconfig(mono)
Requires:	%{cluttergtklibname} = %{EVRD}

%description
Clutter-sharp offers C#/.NET bindings to Clutter.

%files
%doc COPYING README
%{_libdir}/clutter-sharp/

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development files for the C#/.NET bindings
to clutter.

%files devel
%{_datadir}/gapi-2.0/*
%{_libdir}/pkgconfig/clutter-sharp.pc
%{_libdir}/pkgconfig/clutter-gtk-sharp.pc

#----------------------------------------------------------------------------

%package doc
Summary:	Development documentation for %{name}
Group:		Development/Other
Requires(post,postun):	mono-tools >= 1.1.9
BuildArch:	noarch

%description doc
This package contains the API documentation for the %{name} in
Monodoc format.

%files doc
%{_prefix}/lib/monodoc/sources/*

%post doc
%{_bindir}/monodoc --make-index > /dev/null

%postun doc
if [ "$1" = "0" -a -x %{_bindir}/monodoc ]; then
  %{_bindir}/monodoc --make-index > /dev/null
fi

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}
%autopatch -p1
sed -i -e 's!$(prefix)/lib!%{_libdir}/!' glib/Makefile.am
sed -i -e 's!$(prefix)/lib!%{_libdir}/!' clutter/Makefile.am
sed -i -e 's!$(prefix)/lib!%{_libdir}/!' build/assembly.mk
sed -i -e 's!libdir=${exec_prefix}/lib!libdir=%{_libdir}!' clutter/clutter-sharp.pc.in
sed -i -e 's!libdir=${exec_prefix}/lib!libdir=%{_libdir}!' clutter-gtk/clutter-gtk-sharp.pc.in

#build with new clutter-gtk
sed -i -e 's,clutter-gtk-0.10,clutter-gtk-1.0,g' configure.ac

%build
autoreconf -vfi
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
%configure2_5x
#gw parallel make broken
make

%install
%makeinstall_std

