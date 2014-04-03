# spec file for package jitsi





%define libdir_name jitsi


%define disablegost --disable-gost

%ifarch x86_64 amd64
  %define folder linux-64
%else
  %define folder linux
%endif

Name:           jitsi
Version:        2.4
Release:        4997
Summary:        Multiprotocol (SIP, XMPP/Jabber, ecc.) VoIP and instant messaging software
Group:          Productivity/Networking/Instant Messenger
License:        LGPL-2.1+
Url:            http://www.jitsi.org
Source0:        http://download.jitsi.org/jitsi/src/jitsi-src-%{version}.%{release}.zip
Source1:        jitsi-32.sh
Source2:        jitsi-64.sh
Source3:        Jitsi.desktop
Source4:        jitsi_100x100.png
Source5:        jdic_misc.tar.xz
Source6:        ldns-1.6.11.tar.xz
Source7:        unbound-1.4.14.tar.xz

BuildRequires:  java >= 1.6.0 java-devel >= 1.6.0 xalan-j2 ant
BuildRequires:  gcc-c++ dbus-devel xz unzip autoconf automake
BuildRequires:  speex speex-devel pulseaudio-libs alsa-lib-devel libvpx-devel
BuildRequires:  xorg-x11-proto-devel xorg-x11-server-devel
BuildRequires:  glib2-devel gtk2-devel gnome-vfs2-devel libgnome-devel
BuildRequires:  xml-commons-apis  
BuildRequires:  libXScrnSaver-devel libX11-devel libXt-devel libXtst-devel libXv-devel 
BuildRequires:  libmatthew-java desktop-file-utils
BuildRequires:  sane-backends-libs expat expat-devel openssl-devel
BuildRequires:  opus-devel pulseaudio-libs-devel
BuildRequires:  ldns-devel >= 1.6.11
BuildRequires:  unbound-devel >= 1.4.14

Requires:       java >= 1.6.0
Requires:       libmatthew-java

%description
Jitsi is an audio/video and chat communicator that supports protocols
such as SIP, XMPP/Jabber, AIM/ICQ, Windows Live, Yahoo!, Bonjour and many other
useful features such as voice and chat encryption.

%prep
%setup -T -q -b 0 -n jitsi


%build

export CFLAGS="%{optflags} $CFLAGS"
export CXXFLAGS="%{optflags} $CXXFLAGS"
export CPPFLAGS="%{optflags} $CPPFLAGS"

################################
#         BUILD JITSI          #
################################

#Build main program
%ant rebuild

#Build screencapture
%ant screencapture

#Build hid
%ant hid

#Build speex
%ant speex -Dspeex.dynamic=true

#Build g722
%ant g722

#Build hwaddressretriever
%ant hwaddressretriever

#Build galagonotification
#Hidden dbus header
export CPATH="%{_libdir}/dbus-1.0/include"
%ant galagonotification

#Build sysactivity
%ant sysactivity

#Build globalshortcut
%ant globalshortcut

#Build jdic_misc
cd jdic_misc
gcc %{optflags} -c -fPIC -I%{_libdir}/jvm/java/include -I%{_libdir}/jvm/java/include/linux \
  -I/usr/lib/jvm/java/include -I/usr/lib/jvm/java/include/linux -o alerter.o alerter.c
gcc -shared -o libjdic_misc.so alerter.o
%ifarch x86_64 amd64
  cp libjdic_misc.so ../lib/native/linux-64
%else
  cp libjdic_misc.so ../lib/native/linux
%endif
cd ..

%configure
make
make install

%install

#Install bundles
mkdir -p %{buildroot}%{_libdir}/%{libdir_name}
rm -f sc-bundles/*-slick.jar
mkdir -p %{buildroot}%{_libdir}/%{libdir_name}/sc-bundles
cp -r sc-bundles/os-specific/linux/* %{buildroot}%{_libdir}/%{libdir_name}/sc-bundles/
rm -f -r sc-bundles/os-specific
cp -r sc-bundles/* %{buildroot}%{_libdir}/%{libdir_name}/sc-bundles/

#Install other bundles and libs
mkdir -p %{buildroot}%{_libdir}/%{libdir_name}/lib
cp -r lib/bundle %{buildroot}%{_libdir}/%{libdir_name}/lib/
rm -r -f lib/bundle

#Install native libraries
mkdir -p %{buildroot}%{_libdir}/%{libdir_name}/lib/native
%ifarch x86_64 amd64
    rm -r -f lib/native/linux-64/*exclude
    cp lib/native/linux-64/* %{buildroot}%{_libdir}/%{libdir_name}/lib/native/
%else
    rm -r -f lib/native/linux/*exclude
    cp lib/native/linux/* %{buildroot}%{_libdir}/%{libdir_name}/lib/native/
%endif
rm -r -f lib/native
rm -r -f lib/*exclude
rm -r -f lib/os-specific
cp -r lib/* %{buildroot}%{_libdir}/%{libdir_name}/lib/
rm -f %{buildroot}%{_libdir}/%{libdir_name}/lib/native/libunix-java.so
ln --symbolic %{_libdir}/libunix-java.so %{buildroot}%{_libdir}/%{libdir_name}/lib/native/libunix-java.so

#Install executable start script
mkdir -p %{buildroot}%{_bindir}
%ifarch x86_64 amd64
    cp -r %{SOURCE2} %{buildroot}%{_bindir}/jitsi
%else
    cp -r %{SOURCE1} %{buildroot}%{_bindir}/jitsi
%endif
sed -i -e "s;_JAVA_HOME_DIR_;%{java_home};"  %{buildroot}%{_bindir}/jitsi

#Install icons
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp resources/images/logo/sc_logo_45x45.png %{buildroot}%{_datadir}/pixmaps/
cp %{SOURCE4} %{buildroot}%{_datadir}/pixmaps/

#Install desktop file
mkdir -p %{buildroot}%{_datadir}/applications/
cp %{SOURCE3} %{buildroot}%{_datadir}/applications/
%if 0%{?suse_version}
  %suse_update_desktop_file Jitsi Network Telephony InstantMessaging
%else
  desktop-file-install --add-category="Network;Telephony" --dir=%{buildroot}%{_datadir}/applications %{SOURCE3}
%endif



%files
%defattr(-,root,root,-)
%{_libdir}/%{libdir_name}
%{_datadir}/pixmaps/sc_logo_45x45.png
%{_datadir}/pixmaps/jitsi_100x100.png
%{_datadir}/applications/Jitsi.desktop
%attr(0755,root,root) %{_bindir}/jitsi


%changelog
