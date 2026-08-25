%global appid   io.github.thezupzup.linthra
%global commit  main

Name:           linthra
Version:        0.1.15
Release:        1%{?dist}
Summary:        Local-first music player with Jellyfin/Navidrome/Plex streaming

License:        # TODO: verifica la licenza reale nel repo (es. GPL-3.0-or-later)
URL:            https://github.com/TheZupZup/Linthra
# Sorgente da un tag di release; per una build da main usa invece:
# Source0:      https://github.com/TheZupZup/Linthra/archive/refs/heads/%{commit}/%{name}-%{commit}.tar.gz
Source0:        https://github.com/TheZupZup/Linthra/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

# Il target Linux di Linthra è solo desktop x86_64 (Flutter Linux embedder)
ExclusiveArch:  x86_64

BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  gtk3-devel
BuildRequires:  xz-devel
BuildRequires:  libsecret-devel
BuildRequires:  mpv-libs
BuildRequires:  mpv-devel
BuildRequires:  desktop-file-utils
# Il toolchain Flutter è scaricato dallo script del progetto (non pacchettizzato in Fedora):
# richiede accesso di rete abilitato per questa build COPR.
BuildRequires:  curl
BuildRequires:  unzip
BuildRequires:  git

Requires:       gtk3
Requires:       libsecret
Requires:       mpv-libs
# Serve un provider Secret Service a runtime (uno dei due, non hard-dep):
Requires:       (gnome-keyring or kwallet5)

%description
Linthra è un lettore musicale open-source e local-first, con scansione della
libreria locale, streaming da Jellyfin/Navidrome/Plex, cache offline esplicita
e riproduzione controllata dall'utente. Questo pacchetto contiene la build
nativa del target desktop Linux (Flutter), non lo pseudo-pacchetto Flatpak.

Nota: il target Linux non è ancora considerato production-ready dal progetto
(vedi docs/linux-desktop.md, milestone #376). Media session/MPRIS non sono
ancora supportati.

%prep
%autosetup -n %{name}-%{version}

%build
# Flutter pinnato dal progetto stesso, non presente nei repo Fedora
./scripts/setup_flutter.sh
export PATH="%{_builddir}/%{name}-%{version}/.tool/flutter/bin:$PATH"

flutter config --enable-linux-desktop
flutter pub get --enforce-lockfile

# Evita il download CMake di SQLite durante il build isolato di mock/COPR:
# scommenta e imposta se hai vendorizzato l'amalgamation SQLite come sorgente aggiuntiva.
# export LINTHRA_SQLITE3_SOURCE_DIR=%{_builddir}/sqlite-amalgamation

flutter build linux --release

%install
set -eu

# Bundle applicativo
install -d %{buildroot}%{_libdir}/%{name}
cp -a build/linux/x64/release/bundle/. %{buildroot}%{_libdir}/%{name}/

# Wrapper in /usr/bin
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/bin/sh
exec %{_libdir}/%{name}/linthra "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Desktop entry e icona, come indicato in docs/linux-desktop.md
install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  linux/packaging/%{appid}.desktop

install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 \
  linux/packaging/icons/%{appid}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg

%changelog
* Tue Aug 25 2026 Package Maintainer <maintainer@example.com> - 0.1.15-1
- Build iniziale del target Linux desktop nativo di Linthra
