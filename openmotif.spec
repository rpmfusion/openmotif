Summary:	Open Motif runtime libraries and executables
Name:		openmotif
Version:	2.3.4
Release:	1%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
Source: 	http://prdownloads.sourceforge.net/motif/motif-%{version}-src.tgz
Source1:	xmbind
Source2:	README.Fedora
URL:		http://www.motifzone.net/

Buildrequires:	automake autoconf texinfo
BuildRequires:	flex
BuildRequires:	byacc
BuildRequires:	libjpeg-devel libpng-devel
BuildRequires:	libXft-devel libXmu-devel libXp-devel libXt-devel libXext-devel
BuildRequires:	xorg-x11-xbitmaps
BuildRequires:	perl
BuildRequires:	flex-static
BuildRequires:  libtool

Patch1:		openMotif-2.2.3-uil_lib.patch
Patch2:		openMotif-2.3.0-rgbtxt.patch
Patch3: 	openmotif-2.3.3-paths.patch

# Conflicts:	lesstif

%description
This is the Open Motif %{version} runtime environment. It includes the
Motif shared libraries, needed to run applications which are dynamically
linked against Motif, and the Motif Window Manager "mwm".

%package devel
Summary:	Open Motif development libraries and header files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libjpeg-devel libpng-devel
Requires:	libXft-devel libXmu-devel libXp-devel libXt-devel libXext-devel
Provides:	motif-devel = %{version}-%{release}

%description devel
This is the Open Motif %{version} development environment. It includes the
static libraries and header files necessary to build Motif applications.

%package clients
Summary:	Command line utilities for openmotif
Group:		Applications/System
Conflicts:	lesstif-clients
Requires:	%{name} = %{version}-%{release}

%description clients
Commandline utilities for openmotif

* xmbind configure the vitual key bindings of openmotif applications.
* uil is a user interface language compiler.

%package mwm
Summary:	Open Motif window manager
Group:		User Interface/Desktops
Conflicts:	lesstif-mwm
Requires:	%{name} = %{version}-%{release}

%description mwm
"mwm" window manager that adheres largely to the Motif mwm specification.

%package demos
Summary:    Open Motif example code and demo programs
Group:      Development/Libraries
Requires:   openmotif-devel = %{version}-%{release}

%description demos
This is the Open Motif %{version} example code and demo programs.

%package docs
Summary:    Open Motif Additional Documentation
Group:      Development/Libraries
Conflicts:  lesstif-devel
Requires:   openmotif-devel = %{version}-%{release}
# BuildArch:  noarch

%description docs
This is the Open Motif %{version} additional documentation

%prep
%setup -q -n motif-%{version} 
%patch1 -p1 -b .uil_lib
%patch2 -p1 -b .rgbtxt
%patch3 -p1 -b .paths

cp %{SOURCE2} .

%build
./autogen.sh
%configure \
	--enable-xft \
	--enable-jpeg --enable-png

export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make clean

# SMP build doesn't works
make # %{?_smp_mflags}

%install
export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xinit/xinitrc.d

mkdir -p $RPM_BUILD_ROOT/%{_includedir}/openmotif
mv $RPM_BUILD_ROOT/%{_includedir}/[Mu]* $RPM_BUILD_ROOT/%{_includedir}/openmotif
mv $RPM_BUILD_ROOT/%{_includedir}/Xm $RPM_BUILD_ROOT/%{_includedir}/openmotif

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la 
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a 

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/openmotif/
mv $RPM_BUILD_ROOT/%{_libdir}/lib* ${RPM_BUILD_ROOT}/%{_libdir}/openmotif/

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d
%if "%{_lib}" == "lib64"
cat <<EOF >$RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/openmotif-64.conf
%{_libdir}/openmotif
EOF
%else
cat <<EOF >$RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/openmotif.conf
%{_libdir}/openmotif
EOF
%endif

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/xmbind.sh

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la 
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a 

mv -f  $RPM_BUILD_ROOT%{_datadir}/Xm $RPM_BUILD_ROOT%{_libdir}/Xm

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README RELEASE RELNOTES
%{_includedir}/X11/bitmaps/*
%dir %{_libdir}/openmotif
%{_libdir}/openmotif/lib*.so.*
%{_libdir}/X11/bindings/
%{_sysconfdir}/ld.so.conf.d/*

%files mwm
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/X11/mwm/system.mwmrc
%{_bindir}/mwm
%{_mandir}/man1/mwm*
%{_mandir}/man4/mwm*
%doc README.Fedora

%files clients
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/X11/xinit/xinitrc.d/xmbind.sh
%{_bindir}/uil
%{_bindir}/xmbind
%{_mandir}/man1/xmb*
%{_mandir}/man1/uil*

%files devel
%defattr(-,root,root,-)
%{_includedir}/openmotif/
%{_libdir}/openmotif/lib*.so
%{_mandir}/man5/*

%files demos
%defattr(-,root,root,-)
%{_libdir}/Xm/
%{_mandir}/manm/*

%files docs
%defattr(-,root,root,-)
%{_mandir}/man3/*

%changelog
* Thu Oct 25 2012 Jochen Schmitt <Jochen herr-schmitt de> - 2.3.4-1
- New upstream release
- Package clean up
- Licens changed to LGPL

* Tue Jun  5 2012 Jochen Schmitt <Jochen herr-schmitt de> - 2.3.3-3
- Add a BR to flex-static to fix a FTBFS

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 31 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.3.3-1
- New upstream releasee
- Make an unhappy RH employee happy

* Wed Sep 16 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.3.2-5
- Remove req. to /usr/share/X11/XKeysymDB

* Tue Jul 14 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.3.2-4
- Change Destination for libs to %%{_libdir}/openmotif
- Remove rpatch stuff
- Remove utf-8 stuff

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.3.2-3
- Changes to solve file confilicts

* Thu Mar 26 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.3.2-2
- Try to fix conflict with lesstif-devel

* Wed Mar 25 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.3.2-1
- Initional Package for rpmfusion.org (Based on the original RH release)

