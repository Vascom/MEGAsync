%global optflags %{optflags} -flto
%global build_ldflags %{build_ldflags} -flto
%global _qt5_optflags %{_qt5_optflags} $(pkg-config --cflags libavcodec)
# -I/usr/include/ffmpeg
# $(pkg-config --cflags libavcodec)

Name:       megasync
Version:    4.0.2
Release:    1%{?dist}
Summary:    Easy automated syncing between your computers and your MEGA cloud drive
License:    Freeware
Url:        https://mega.nz
Source0:    megasync_%{version}.tar.gz
# Source0:    https://github.com/meganz/MEGAsync/archive/v%{version}.0_Linux.tar.gz

BuildRequires: openssl-devel
BuildRequires: sqlite-devel
BuildRequires: zlib-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: gcc-c++
BuildRequires: hicolor-icon-theme, unzip, wget
BuildRequires: ffmpeg-devel
BuildRequires: pkgconfig
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
%autosetup
rm -rf archives

sed -i '/-u/d' configure
sed -i 's/-v/-y/' configure
sed -i '/qlite_pkg $build_dir $install_dir/d' MEGASync/mega/contrib/build_sdk.sh


%build
export AR=%{_bindir}/gcc-ar
export RANLIB=%{_bindir}/gcc-ranlib
export NM=%{_bindir}/gcc-nm

export DESKTOP_DESTDIR=%{buildroot}%{_prefix}

./configure -i -z

%define fullreqs "CONFIG += FULLREQUIREMENTS"

%qmake_qt5 %{fullreqs} DESTDIR=%{buildroot}%{_bindir} THE_RPM_BUILD_ROOT=%{buildroot}
lrelease-qt5 MEGASync/MEGASync.pro

%make_build

%install
make install DESTDIR=%{buildroot}%{_bindir}

desktop-file-install \
    --add-category="Network" \
    --dir %{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/%{name}.desktop

rm -rf %{buildroot}%{_datadir}/icons/ubuntu*

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/mega.png
%{_datadir}/icons/hicolor/scalable/status/*.svg
%{_datadir}/doc/%{name}

%changelog
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
