%undefine _missing_build_ids_terminate_build

Name: jitsi
Summary: Open Source Video Calls and Chat
Summary(de): Open Source Anrufe und Chat
Version: 2.4.4997
Release: 4.2
Group: Applications/Internet
License: GNU Lesser General Public License
URL: https://www.jitsi.org
Source0: https://download.jitsi.org/jitsi/src/%{name}-src-%{version}.zip
Source1: jitsi.sh
BuildRequires: java-devel-openjdk, ant
BuildRequires: desktop-file-utils
Requires: jre
BuildRoot: %{_tmppath}/%{name}-%{version}-build    

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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/jitsi
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/share/pixmaps
mkdir -p $RPM_BUILD_ROOT/usr/lib/jitsi
mkdir -p $RPM_BUILD_ROOT/usr/lib/jitsi/lib
mkdir -p $RPM_BUILD_ROOT/usr/lib/jitsi/lib/bundle
mkdir -p $RPM_BUILD_ROOT/usr/lib/jitsi/lib/native
mkdir -p $RPM_BUILD_ROOT/usr/lib/jitsi/sc-bundles

# copy the documentation
cp resources/install/debian/jitsi.1.tmpl $RPM_BUILD_ROOT/usr/share/man/man1/jitsi.1
sed -i -e "s/_PACKAGE_NAME_/jitsi/"  $RPM_BUILD_ROOT/usr/share/man/man1/jitsi.1
sed -i -e "s/_APP_NAME_/Jitsi/"  $RPM_BUILD_ROOT/usr/share/man/man1/jitsi.1
gzip $RPM_BUILD_ROOT/usr/share/man/man1/jitsi.1

# copy the launcher script
cp -r %{SOURCE1} %{buildroot}%{_bindir}/jitsi
sed -i -e "s/_PACKAGE_NAME_/jitsi/" %{buildroot}%{_bindir}/jitsi

# no more libaoss
chmod a+x $RPM_BUILD_ROOT/usr/bin/jitsi

# copy the menu icons
cp resources/install/debian/jitsi-32.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/jitsi-32.xpm
cp resources/install/debian/jitsi-16.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/jitsi-16.xpm
cp resources/install/debian/jitsi.svg $RPM_BUILD_ROOT/usr/share/pixmaps/jitsi.svg

# copy the menu entry
cp resources/install/debian/jitsi.desktop.tmpl $RPM_BUILD_ROOT/usr/share/applications/jitsi.desktop
sed -i -e "s/_PACKAGE_NAME_/jitsi/"  $RPM_BUILD_ROOT/usr/share/applications/jitsi.desktop
sed -i -e "s/_APP_NAME_/Jitsi/"      $RPM_BUILD_ROOT/usr/share/applications/jitsi.desktop

# copy the sc-bundles
cp sc-bundles/*.jar $RPM_BUILD_ROOT/usr/lib/jitsi/sc-bundles/
# remove all slicks
rm -rf $RPM_BUILD_ROOT/usr/lib/jitsi/sc-bundles/*-slick.jar

# copy the os-specific sc-bundles
cp sc-bundles/os-specific/linux/*.jar $RPM_BUILD_ROOT/usr/lib/jitsi/sc-bundles/

# copy the lib jars
cp lib/*.jar $RPM_BUILD_ROOT/usr/lib/jitsi/lib/
cp lib/bundle/* $RPM_BUILD_ROOT/usr/lib/jitsi/lib/bundle/
rm $RPM_BUILD_ROOT/usr/lib/jitsi/lib/bundle/junit.jar
##cp lib/os-specific/linux/*.jar $RPM_BUILD_ROOT/usr/lib/jitsi/lib/

# copy the native libs
%ifarch x86_64
cp lib/native/linux-64/* $RPM_BUILD_ROOT/usr/lib/jitsi/lib/native/
%else
cp lib/native/linux/* $RPM_BUILD_ROOT/usr/lib/jitsi/lib/native/
%endif

# copy the resources
cp resources/install/logging.properties $RPM_BUILD_ROOT/usr/lib/jitsi/lib/
cp lib/felix.client.run.properties $RPM_BUILD_ROOT/usr/lib/jitsi/lib/

# Make felix deploy its bundles in ~/.felix/sip-communicator.bin
sed -i -e "s/felix.cache.profiledir=jitsi.bin/felix.cache.profile=jitsi.bin/" $RPM_BUILD_ROOT/usr/lib/jitsi/lib/felix.client.run.properties

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
/usr/lib/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/pixmaps/%{name}-16.xpm
%{_datadir}/pixmaps/%{name}-32.xpm
%{_datadir}/pixmaps/%{name}.svg

%changelog
* Fri Dec 13 2013 Huaren Zhong <huaren.zhong@gmail.com> - 2.3.4978
- Rebuild for Fedora
* Mon Mar 11 2013 Pavel Tankov <ptankov@bluejimp.com>
- Now depends on java >= 0:1.5.0.
* Thu Jan 31 2013 Damian Minkov <damencho@jitsi.org>
- Fixed startup script. 
- Add felix.framework and felix.main dependencies.
- Fix warning about conflicting folders with filesystem package.
* Wed Mar 23 2011 Pavel Tankov <tankov_pavel@yahoo.com>
- Renamed to the new project name -jitsi
* Mon Apr 19 2010 Pavel Tankov <tankov_pavel@yahoo.com>
- Now depends on java >= 1:1.5.0.
* Wed Mar 31 2010 Pavel Tankov <tankov_pavel@yahoo.com>
- Handled the manpages.
* Tue Mar 30 2010 Pavel Tankov <tankov_pavel@yahoo.com>
- Migrated the build process on a Fedora 12 x86_64 machine. It used to be a
  Debian which, after a distupgrade, couldn't run rpmbuild properly anymore.
- Took out the svn update and ant rebuild actions and put them in the external
  script that calls rpmbuild with this spec.
- Updated the description section.
* Tue Dec 18 2007 Pavel Tankov <tankov_pavel@yahoo.com>
- Put SC bundles and libraries under /usr/lib instead of /usr/share
- Changed BuildPrereq to subversion instead of cvs
- Changed the "Source:" tag to reflect the new location of the last nightly build
- Patched the launcher script so that LD_PRELOAD points to /usr/lib/libaoss.so.0
  instead of /usr/lib/libaoss.so
* Fri Feb 23 2007 Pavel Tankov <tankov_pavel@yahoo.com>
- Fixed to reflect the new guidelines for the layout
  on http://www.sip-communicator.org/index.php/Documentation/HowToBuildAnInstaller
- Removed the folder /usr/share/sip-communicator/lib/os-cpecific
  because it was not needed.
- Added stuff from sc-bundles/os-specific/linux/ because it was missing.
- This fix resulted in the systray icon showing now.
* Thu Feb 15 2007 Pavel Tankov <tankov_pavel@yahoo.com>
- Fixed to reflect the new images in $RPM_BUILD_ROOT/usr/share/pixmaps/
- TODO: incorporate the systray icon.
* Sat Jan 27 2007 Pavel Tankov <tankov_pavel@yahoo.com>
- Removed /usr/share/menu because it was not needed.
- Fixed to reflect the new directory structure with the "os-specific"
  and "installer-exclude" folders in mind.
- TODO: handle manpages.
- TODO: check whether user has java installed.
* Mon Jan 08 2007 Pavel Tankov <tankov_pavel@yahoo.com>
- Initial RPM release.

