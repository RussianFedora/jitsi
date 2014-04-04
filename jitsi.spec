%undefine _missing_build_ids_terminate_build

Name: jitsi
Summary: Open Source Video Calls and Chat
Summary(de): Open Source Anrufe und Chat
Version: 2.4.4997
Release: 1%{?dist}
License: LGPLv2+
URL: https://www.jitsi.org
Source0: https://download.jitsi.org/jitsi/src/%{name}-src-%{version}.zip
Source1:        jitsi-32.sh
Source2:        jitsi-64.sh
Source3:	jitsi.desktop
BuildRequires: java-devel-openjdk, ant
BuildRequires: desktop-file-utils
Requires: jre


%description
Jitsi is an audio/video Internet phone and instant messenger that
supports some of the most popular instant messaging and telephony protocols
such as SIP, Jabber, AIM/ICQ, MSN, Yahoo! Messenger, Bonjour, RSS and
counting.

%description -l de
Jitsi ist ein Audio-/Video- Internettelefon und Sofortnachrichtenklient, der
einige der meist bekannten Protokolle unterstützt, wie SIP, Jabber, AIM/ICQ,
MSN, Yahoo! Messenger, Bonjure, RSS und counting.

%prep
%setup -q -n %{name}

%build
ant -Dlabel=build.%{buildversion} rebuild

%install
#Install bundles
mkdir -p %{buildroot}%{_libdir}/%{name}
rm -f sc-bundles/*-slick.jar
mkdir -p %{buildroot}%{_libdir}/%{name}/sc-bundles
cp -r sc-bundles/os-specific/linux/* %{buildroot}%{_libdir}/%{name}/sc-bundles/
rm -f -r sc-bundles/os-specific
cp -r sc-bundles/* %{buildroot}%{_libdir}/%{name}/sc-bundles/

#Install other bundles and libs
mkdir -p %{buildroot}%{_libdir}/%{name}/lib
cp -r lib/bundle %{buildroot}%{_libdir}/%{name}/lib/
rm -r -f lib/bundle

#Install native libraries
mkdir -p %{buildroot}%{_libdir}/%{name}/lib/native
%ifarch x86_64 amd64
    rm -r -f lib/native/linux-64/*exclude
    cp lib/native/linux-64/* %{buildroot}%{_libdir}/%{name}/lib/native/
%else
    rm -r -f lib/native/linux/*exclude
    cp lib/native/linux/* %{buildroot}%{_libdir}/%{name}/lib/native/
%endif
rm -r -f lib/native
rm -r -f lib/*exclude
rm -r -f lib/os-specific
cp -r lib/* %{buildroot}%{_libdir}/%{name}/lib/
rm -f %{buildroot}%{_libdir}/%{name}/lib/native/libunix-java.so
ln --symbolic %{_libdir}/libunix-java.so %{buildroot}%{_libdir}/%{name}/lib/native/libunix-java.so

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
cp resources/images/logo/sc_logo_45x45.png %{buildroot}%{_datadir}/pixmaps/jitsi.png


#Install desktop file
mkdir -p %{buildroot}%{_datadir}/applications/
cp %{SOURCE3} %{buildroot}%{_datadir}/applications/jitsi.desktop

%files
%{_libdir}/%{name}
%{_datadir}/pixmaps/sc_logo_45x45.png
%{_datadir}/pixmaps/jitsi.png
%{_datadir}/applications/jitsi.desktop
%attr(0755,root,root) %{_bindir}/jitsi

%changelog

* Thu Apr 03 2014 Kishinskiy Oleg <legunt@yandex.ru>
 -add this to RussianFedora reposytories
