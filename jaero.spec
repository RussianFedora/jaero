Name:           jaero
Version:        1.0.4.11
Release:        1%{?dist}
Summary:        A SatCom ACARS demodulator and decoder for the Aero standard

# Bundled qcustomplot is GPLv3+
License:        MIT AND GPLv3+
URL:            http://jontio.zapto.org/hda1/jaero.html
Source:         https://github.com/jontio/JAERO/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.xz
Patch0:         bcb5b78c74f06cc878cb347b9f99b08cddfafef4.patch
Patch1:         fe604fb7e221fc615c0526a48f1f73954d6e70bb.patch

BuildRequires:  gcc-c++
BuildRequires:  libcorrect-devel
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5PrintSupport)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(libacars)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  kiss-fft-static
BuildRequires:  qcustomplot-qt5-devel

Requires:       hicolor-icon-theme
Requires:       unzip

%description
JAERO is a program that demodulates and decodes Classic Aero ACARS (Aircraft
Communications Addressing and Reporting System) messages sent from satellites to
aeroplanes (SatCom ACARS), commonly used when planes are beyond VHF range.

Demodulation is performed using the soundcard.

Such signals are typically around 1.5Ghz and can be received with a
low-gain antenna that can be home-brewed in conjunction with an
RTL-SDR dongle.

%prep
%autosetup -p1 -n JAERO-%{version}
## remove bundled libs
# rm -rf kiss_fft130
rm -rf kiss_fft130/kiss_fft*
rm -rf libacars-*
rm -rf libcorrect
rm -rf libogg-*
rm -rf libvorbis-*
rm -rf qcustomplot

# Unbundle kiss-fft
%global TYPE double
echo "INCLUDEPATH += %{_includedir}/kissfft" >> JAERO/JAERO.pro
echo "LIBS += -lkiss_fft_%{TYPE} -lkiss_fftnd_%{TYPE} -lkiss_fftndr_%{TYPE} -lkiss_fftr_%{TYPE} -lkiss_kfc_%{TYPE}" >> JAERO/JAERO.pro
sed -i '/kiss_fft130\/kiss_fft/d' JAERO/JAERO.pro
sed -i 's|../kiss_fft130/kiss_fft|kiss_fft|' JAERO/fftwrapper.h
sed -i 's|../kiss_fft130/kiss_fft|kiss_fft|' JAERO/fftrwrapper.h
sed -i 's|../kiss_fft130/kiss_fft|kiss_fft|' JAERO/DSP.h

# Unbundle libacars
sed -i '/QMAKE_CXXFLAGS_RELEASE/d' JAERO/JAERO.pro
sed -i '/VORBIS_PATH/d' JAERO/JAERO.pro
sed -i '/OGG_PATH/d' JAERO/JAERO.pro
sed -i '/LIBACARS_PATH/d' JAERO/JAERO.pro

# Unbundle libcorrect
sed -i 's|../libcorrect/include/||' JAERO/jconvolutionalcodec.h

# Use prope qcustomplot Qt5 lib
sed -i 's|lqcustomplot|lqcustomplot-qt5|' JAERO/JAERO.pro

# Correct desktop-file
mv JAERO/JAERO.desktop JAERO/%{name}.desktop
sed -i "s|/opt/jaero/JAERO|%{_bindir}/%{name}|" JAERO/%{name}.desktop
sed -i "s|/opt/jaero/jaero.ico|%{name}|" JAERO/%{name}.desktop

# Enable LTO
echo "QMAKE_CXXFLAGS += -flto
QMAKE_LFLAGS_RELEASE += -flto" >> JAERO/JAERO.pro

%build
mkdir JAERO/build
cd JAERO/build
%{qmake_qt5} ..
%make_build

%install
install -Dpm 0755 JAERO/build/JAERO  %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 JAERO/images/primary-modem.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
desktop-file-install JAERO/%{name}.desktop

%files
%license JAERO/LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Thu Oct 24 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 1.0.4.11-1
- Initial release for Fedora
