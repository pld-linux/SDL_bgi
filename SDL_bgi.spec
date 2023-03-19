#
# TODO python3, static libs
Summary:	The SDL_bgi Library
Summary(pl.UTF-8):	Biblioteka SDL_bgi
Name:		SDL_bgi
Version:	3.0.0
Release:	1
License:	Zlib (BSD-like)
Group:		Libraries
Source0:	https://sourceforge.net/projects/sdl-bgi/files/%{name}-%{version}.tar.gz
# Source0-md5:	2a0300d89891d3bac47911394645e00d
URL:		https://sdl-bgi.sourceforge.io/
BuildRequires:	SDL2-devel
BuildRequires:	cmake
BuildRequires:	ninja
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SDL_bgi is a Borland Graphics Interface ('GRAPHICS.H') implementation
based on SDL2. This library strictly emulates BGI functions, making it
possible to compile SDL2 versions of programs written for Turbo
C/Borland C++. ARGB colours, vector fonts, mouse support, and multiple
windows are also implemented; further, native SDL2 functions may be
used in SDL_bgi programs. SDL_bgi also supports Wasm, via Emscripten,
and Python bindings.

%description -l pl.UTF-8
SDL_bgi jest implementacją Borland Graphics Interface ('GRAPHICS.H')
opartą na SDL2. Ta biblioteka dokładnie emuluje funkcje BGI
umożliwiając kompilację wersji SDL2 programów napisanych z
użyciem Turbo C/Borlanf C++. Kolory ARGB, fonty wektorowe, obsługa
myszy oraz wielu okien są także zaimplementowane. Dodatkowo funkcje
natywne SDL2 mogą być użyte w programach SDL_bgi. Biblioteka
wspiera także Wasm, używając do tego Ecmscripten i ma dowiązania
do Pythona.

%package devel
Summary:	SDL_bgi - Header files
Summary(pl.UTF-8):	SDL_bgi - Pliki nagłówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
SDL_bgi - Header files.

%description devel -l pl.UTF-8
SDL_bgi - Pliki nagłówkowe.

%package static
Summary:	SDL_bgi - static libraries
Summary(pl.UTF-8):	SDL_bgi - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
SDL_bgi - static libraries.

%description static -l pl.UTF-8
SDL_bgi - biblioteki statyczne.

%package examples
Summary:	SDL_bgi - example programs
Summary(pl.UTF-8):	SDL_bgi - programy przykładowe
License:	Public Domain
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
BuildArch:	noarch

%description examples
SDL_bgi - example programs.

%description examples -l pl.UTF-8
SDL_bgi - przykładowe programy.

%prep
%setup -q

%build
install -d build
cd build
%cmake -G Ninja \
	../
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%ninja_install -C build
cp -a demo $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/
cp -a test $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/
sed -i -e 's|/usr/bin/env python3|%{_bindir}/python3|g' $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/demo/*.py
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog INSTALL_Emscripten.md INSTALL_GNU-Linux.md INSTALL_Python.md INSTALL_Windows.md INSTALL_macOS.md TODO
%attr(755,root,root) %{_libdir}/libSDL_bgi.so

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_includedir}/SDL2/SDL_bgi.h
%{_includedir}/graphics.h
%{_mandir}/man3/graphics*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
