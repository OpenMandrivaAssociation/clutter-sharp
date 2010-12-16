#gw it could even become a noarch package, but it has a dep
#on the clutter library packages
%define debug_package %{nil}
%define cluttergtklibname %mklibname clutter-gtk 0.10 0
#gw it ships a patched version of glib-sharp
%define _provides_exceptions mono.glib-sharp

%define gitdate 20090817
Summary: C#/.NET bindings to Clutter
Name: clutter-sharp
Version: 0
Release: %mkrel -c %{gitdate} 1
URL: http://www.clutter-project.org
Source0: %{name}-%{gitdate}.tar.xz
Patch0: clutter-sharp-20090817-ilasm-build.patch
Patch1: clutter-sharp-20090828-initialization-fix.patch
License: MIT
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-
BuildRequires: mono-devel
BuildRequires: gtk-sharp2-devel
BuildRequires: gtk-sharp2
BuildRequires: glib-sharp2
BuildRequires: clutter-gtk-devel 
ExcludeArch: sparc64
Requires: %cluttergtklibname

%description
Clutter-sharp offers C#/.NET bindings to Clutter

%package devel
Summary: Development files for %{name}
Group: Development/Other
Requires: %name = %{version}-%{release}

%description devel
This package contains the development files for the C#/.NET bindings
to clutter.

%package doc
Summary: Development documentation for %name
Group: Development/Other
Requires(post): mono-tools >= 1.1.9
Requires(postun): mono-tools >= 1.1.9 
BuildArch: noarch

%description doc
This package contains the API documentation for the %name in
Monodoc format. 

%prep
%setup -q -n %{name}
%apply_patches
sed -i -e 's!$(prefix)/lib!%{_libdir}/!' glib/Makefile.am
sed -i -e 's!$(prefix)/lib!%{_libdir}/!' clutter/Makefile.am
sed -i -e 's!$(prefix)/lib!%{_libdir}/!' build/assembly.mk
sed -i -e 's!libdir=${exec_prefix}/lib!libdir=%{_libdir}!' clutter/clutter-sharp.pc.in
sed -i -e 's!libdir=${exec_prefix}/lib!libdir=%{_libdir}!' clutter-gtk/clutter-gtk-sharp.pc.in
./autogen.sh

%build
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
%configure2_5x
#gw parallel make broken
make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%post doc 
%_bindir/monodoc --make-index > /dev/null

%postun doc
if [ "$1" = "0" -a -x %_bindir/monodoc ]; then %_bindir/monodoc --make-index > /dev/null
fi

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/clutter-sharp/

%files devel
%defattr(-,root,root,-)
%{_datadir}/gapi-2.0/*
%{_libdir}/pkgconfig/clutter-sharp.pc
%{_libdir}/pkgconfig/clutter-gtk-sharp.pc

%files doc
%defattr(-,root,root,-)
%{_prefix}/lib/monodoc/sources/*

