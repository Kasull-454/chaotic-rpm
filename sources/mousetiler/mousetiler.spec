%define debug_package %{nil}

Name:           MouseTiler
# renovate: datasource=github-releases depName=rxappdev/MouseTiler extractVersion=true
Version:        6.5.0
Release:        1%{?dist}
Summary:        The fastest, simplest tiler for KDE Plasma 6+ that gives you full freedom at your fingertip. No need to remember dozens of keyboard shortcuts or be limited by a fixed tile layout.
License:        GPL-3.0-or-later
URL:            https://github.com/rxappdev/%{name}
Source0:	    %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch: noarch

Requires: kwin

%description

%prep
%autosetup -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_datadir}/kwin-wayland/scripts/mousetiler
cp src/metadata.json %{buildroot}%{_datadir}/kwin-wayland/scripts/mousetiler/
cp -r src/contents %{buildroot}%{_datadir}/kwin-wayland/scripts/mousetiler/

%files
%license LICENSE
%doc README.md AUTOTILERGUIDE.md
%{_datadir}/kwin-wayland/scripts/mousetiler

%changelog
%autochangelog
