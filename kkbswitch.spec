%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kkbswitch
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.4.3
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:		Keyboard layout indicator for TDE
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/settings/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

# XKBFILES support
BuildRequires:  pkgconfig(xkbfile)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
KKBSwitch displays an icon in the system tray that indicates which layout is 
currently active and enables you to switch layouts by clicking the icon or by 
selecting from the menu. It works with all desktop environments.

Features include:
- Configurable icons for the keyboard layouts.
- The "toggle mode" to toggle between the two most recently-used keyboard 
  layouts.
- Choose to use a global layout or per-application or per-window layouts.
- Configurable keyboard shortcuts.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}

# Fix desktop icon location
if [ -d "%{?buildroot}%{tde_prefix}/share/applnk" ]; then
  %__mkdir_p "%{?buildroot}%{tde_prefix}/share/applications/tde"
  %__mv -f "%{?buildroot}%{tde_prefix}/share/applnk/"*"/%{tde_pkg}.desktop" "%{?buildroot}%{tde_prefix}/share/applications/tde"
  %__rm -r "%{buildroot}%{tde_prefix}/share/applnk"
fi


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README.md TODO
%{tde_prefix}/bin/kkbswitch
%{tde_prefix}/share/applications/tde/kkbswitch.desktop
%{tde_prefix}/share/apps/kkbswitch/
%{tde_prefix}/share/apps/tdeconf_update/kkbswitch.upd
%{tde_prefix}/share/apps/tdeconf_update/kkbswitch_update_14_icons
%{tde_prefix}/share/apps/tdeconf_update/kkbswitch_update_14_options
%{tde_prefix}/share/autostart/kkbswitch.desktop
%{tde_prefix}/share/X11/xkb/symbols/ru_ua
%{tde_prefix}/share/doc/tde/HTML/en/kkbswitch/
%{tde_prefix}/share/man/man1/kkbswitch.1
%{tde_prefix}/share/icons/hicolor/*/apps/kkbswitch.png

