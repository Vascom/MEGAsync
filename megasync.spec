%global sdk_version 3.4.7

Name:       megasync
Version:    4.0.2
Release:    2%{?dist}
Summary:    Easy automated syncing between your computers and your MEGA cloud drive
License:    BSD
URL:        https://mega.nz
Source0:    https://github.com/meganz/MEGAsync/archive/v%{version}.0_Linux.tar.gz
Source1:    https://github.com/meganz/sdk/archive/v%{sdk_version}.tar.gz

BuildRequires: openssl-devel
BuildRequires: sqlite-devel
BuildRequires: zlib-devel
BuildRequires: automake
BuildRequires: libtool
BuildRequires: gcc-c++
BuildRequires: unzip
BuildRequires: wget
BuildRequires: ffmpeg-devel
BuildRequires: bzip2-devel
BuildRequires: libzen-devel
BuildRequires: libmediainfo-devel
BuildRequires: c-ares-devel
BuildRequires: cryptopp-devel >= 5.6.5
BuildRequires: desktop-file-utils
BuildRequires: qt5-qtbase-devel >= 5.6
BuildRequires: qt5-qttools-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: terminus-fonts
BuildRequires: fontpackages-filesystem
BuildRequires: LibRaw-devel
BuildRequires: libsodium-devel
BuildRequires: libuv-devel
BuildRequires: sqlite-devel

Requires:       hicolor-icon-theme

%description
Secure:
Your data is encrypted end to end. Nobody can intercept it while in storage or
in transit.

Flexible:
Sync any folder from your PC to any folder in the cloud. Sync any number of
folders in parallel.

Fast:
Take advantage of MEGA's high-powered infrastructure and multi-connection
transfers.

Generous:
Store up to 50 GB for free!

%prep
%autosetup -n MEGAsync-%{version}.0_Linux

#Move Mega SDK to it's place
tar -xvf %{SOURCE1} -C src/MEGASync/mega
mv src/MEGASync/mega/sdk-%{sdk_version}/* src/MEGASync/mega/

#Disable all bundling
sed -i '/-u/d' src/configure
sed -i 's/-v/-y/' src/configure
sed -i '/qlite_pkg $build_dir $install_dir/d' src/MEGASync/mega/contrib/build_sdk.sh


%build
#Enable LTO optimisation and FFMPEG
echo "CONFIG += link_pkgconfig
PKGCONFIG += libavcodec
QMAKE_CXXFLAGS += -flto
QMAKE_CFLAGS += -flto
QMAKE_LFLAGS_RELEASE += -flto" >> src/MEGASync/MEGASync.pro

export DESKTOP_DESTDIR=%{buildroot}%{_prefix}

pushd src
    ./configure -i -z

    %qmake_qt5 \
        "CONFIG += FULLREQUIREMENTS" \
        DESTDIR=%{buildroot}%{_bindir} \
        THE_RPM_BUILD_ROOT=%{buildroot}
    lrelease-qt5 MEGASync/MEGASync.pro

    %make_build
popd

%install
pushd src
    %make_install DESTDIR=%{buildroot}%{_bindir}
popd

desktop-file-install \
    --add-category="Network" \
    --dir %{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/%{name}.desktop

#Remove ubuntu specific themes
rm -rf %{buildroot}%{_datadir}/icons/ubuntu*


%files
%license LICENCE.md src/MEGASync/mega/LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/mega.png
%{_datadir}/icons/hicolor/scalable/status/*.svg
%{_datadir}/doc/%{name}

%changelog
* Mon Apr 22 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 4.0.2-2
- Correct spec
- Add license files

* Fri Apr 19 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 4.0.2-1
- Clean spec for fedora

* Mon Feb  4 2019 linux@mega.co.nz
- Update to version 4.0.2:
  * Fix bug with selection of transfer manager items
  * Fix bug of context menu not shown over transfer manager items
  * New design for the main dialog
  * Improved setup assistant
  * Support to show Public Service Announcements
  * Modern notifications
  * Updated third-party libraries
  * Other minor bug fixes and improvements
