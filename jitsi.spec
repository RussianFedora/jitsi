Name: jitsi
Summary: Open Source Video Calls and Chat
Summary(de): Open Source Anrufe und Chat
Version: 2.4.4997
Release: 1%{?dist}
Group: Applications/Internet
License: LGPLv2+
URL: https://www.jitsi.org
Source0: https://download.jitsi.org/jitsi/src/%{name}-src-%{version}.zip
Source1: jitsi.sh
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
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}/usr
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/doc/jitsi
mkdir -p %{buildroot}/usr/share/man/man1
mkdir -p %{buildroot}/usr/share/pixmaps
mkdir -p %{buildroot}/usr/lib/jitsi
mkdir -p %{buildroot}/usr/lib/jitsi/lib
mkdir -p %{buildroot}/usr/lib/jitsi/lib/bundle
mkdir -p %{buildroot}/usr/lib/jitsi/lib/native
mkdir -p %{buildroot}/usr/lib/jitsi/sc-bundles

# copy the documentation
cp resources/install/debian/jitsi.1.tmpl %{buildroot}/usr/share/man/man1/jitsi.1
sed -i -e "s/_PACKAGE_NAME_/jitsi/"  %{buildroot}/usr/share/man/man1/jitsi.1
sed -i -e "s/_APP_NAME_/Jitsi/"  %{buildroot}/usr/share/man/man1/jitsi.1
gzip %{buildroot}/usr/share/man/man1/jitsi.1

# copy the launcher script
cp -r %{SOURCE1} %{buildroot}%{_bindir}/jitsi
sed -i -e "s/_PACKAGE_NAME_/jitsi/" %{buildroot}%{_bindir}/jitsi

# no more libaoss
chmod a+x %{buildroot}/usr/bin/jitsi

# copy the menu icons
cp resources/install/debian/jitsi-32.xpm %{buildroot}/usr/share/pixmaps/jitsi-32.xpm
cp resources/install/debian/jitsi-16.xpm %{buildroot}/usr/share/pixmaps/jitsi-16.xpm
cp resources/install/debian/jitsi.svg %{buildroot}/usr/share/pixmaps/jitsi.svg

# copy the menu entry
cp resources/install/debian/jitsi.desktop.tmpl %{buildroot}/usr/share/applications/jitsi.desktop
sed -i -e "s/_PACKAGE_NAME_/jitsi/"  %{buildroot}/usr/share/applications/jitsi.desktop
sed -i -e "s/_APP_NAME_/Jitsi/"      %{buildroot}/usr/share/applications/jitsi.desktop

# copy the sc-bundles
cp sc-bundles/*.jar %{buildroot}/usr/lib/jitsi/sc-bundles/
# remove all slicks
rm -rf %{buildroot}/usr/lib/jitsi/sc-bundles/*-slick.jar

# copy the os-specific sc-bundles
cp sc-bundles/os-specific/linux/*.jar %{buildroot}/usr/lib/jitsi/sc-bundles/

# copy the lib jars
cp lib/*.jar %{buildroot}/usr/lib/jitsi/lib/
cp lib/bundle/* %{buildroot}/usr/lib/jitsi/lib/bundle/
rm %{buildroot}/usr/lib/jitsi/lib/bundle/junit.jar
##cp lib/os-specific/linux/*.jar $RPM_BUILD_ROOT/usr/lib/jitsi/lib/

# copy the native libs
%ifarch x86_64
cp lib/native/linux-64/* %{buildroot}/usr/lib/jitsi/lib/native/
%else
cp lib/native/linux/* %{buildroot}/usr/lib/jitsi/lib/native/
%endif

# copy the resources
cp resources/install/logging.properties %{buildroot}/usr/lib/jitsi/lib/
cp lib/felix.client.run.properties %{buildroot}/usr/lib/jitsi/lib/

# Make felix deploy its bundles in ~/.felix/sip-communicator.bin
sed -i -e "s/felix.cache.profiledir=jitsi.bin/felix.cache.profile=jitsi.bin/" %{buildroot}/usr/lib/jitsi/lib/felix.client.run.properties

#%clean
#rm -rf %{buildroot}

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
/usr/lib/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/pixmaps/%{name}-16.xpm
%{_datadir}/pixmaps/%{name}-32.xpm
%{_datadir}/pixmaps/%{name}.svg

%changelog

Thu, Apr 03 2014 Kishinskiy Oleg <legunt@yandex.ru>
-add this to RussianFedora reposytories
