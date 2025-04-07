# TODO: emscripten?
#
# Conditional build:
%bcond_without	python	# Python 3.x module
Summary:	The SDL_bgi Library
Summary(pl.UTF-8):	Biblioteka SDL_bgi
Name:		SDL_bgi
Version:	3.0.3
Release:	1
License:	Zlib (BSD-like)
Group:		Libraries
Source0:	https://downloads.sourceforge.net/sdl-bgi/%{name}-%{version}.tar.gz
# Source0-md5:	29941283a8508e8bdf1654a71e4ba4f7
Patch0:		%{name}-no-strip.patch
URL:		https://sdl-bgi.sourceforge.io/
BuildRequires:	SDL2-devel >= 2.0
BuildRequires:	cmake >= 3.5.0
BuildRequires:	ninja
%if %{with python}
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-build
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.045
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
użyciem Turbo C/Borland C++. Kolory ARGB, fonty wektorowe, obsługa
myszy oraz wielu okien są także zaimplementowane. Dodatkowo funkcje
natywne SDL2 mogą być użyte w programach SDL_bgi. Biblioteka
wspiera także Wasm, używając do tego Ecmscripten i ma dowiązania
do Pythona.

%package devel
Summary:	SDL_bgi - header files
Summary(pl.UTF-8):	SDL_bgi - pliki nagłówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL2-devel >= 2.0

%description devel
Header files for SDL_bgi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SDL_bgi.

%package apidocs
Summary:	API documentation for SDL_bgi library
Summary(pl.UTF-8):	Dokumentacja API biblioteki SDL_bgi
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for SDL_bgi library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SDL_bgi.

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

%package -n python3-sdl_bgi
Summary:	Python bindings for SDL_bgi library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki SDL_bgi
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-sdl_bgi
SDL_bgi is a graphics library (GRAPHICS.H) for C, C++, WebAssembly,
and Python. It's based on SDL2 and it's portable on many platforms.

%description -n python3-sdl_bgi -l pl.UTF-8
SDL_bgi to biblioteka graficzna (GRAPHICS.H) dla C, C++, WebAssembly
oraz Pythona. Jest oparta na SDL2 i przenośna na wiele platform.

%prep
%setup -q
%patch -P0 -p1

%build
install -d build
cd build
%cmake -G Ninja \
	..

%ninja_build

%if %{with python}
cd ../pypi
%py3_build_pyproject
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%ninja_install -C build

%if %{with python}
cd pypi
%py3_install_pyproject
cd ..
%endif

cp -a demo test $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__sed} -i -e '1s|/usr/bin/env python3|%{__python3}|' $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/demo/*.py

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog LICENSE README.md TODO
%attr(755,root,root) %{_libdir}/libSDL_bgi.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/SDL2/SDL_bgi.h
%{_includedir}/graphics.h
%{_mandir}/man3/graphics.3*

%files apidocs
%defattr(644,root,root,755)
%doc doc/*.{css,html,png} doc/{sdl_bgi-quickref,turtlegraphics}.pdf

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%if %{with python}
%files -n python3-sdl_bgi
%defattr(644,root,root,755)
%doc pypi/{LICENSE,README.md}
%{py3_sitescriptdir}/sdl_bgi-3.0.2.dist-info
%{py3_sitescriptdir}/sdl_bgi
%endif
