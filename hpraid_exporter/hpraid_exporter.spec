%define debug_package %{nil}

Name:    hpraid_exporter
Version: 0.1
Release: 1%{?dist}
BuildArch: x86_64
Summary: Prometheus exporter for HP RAID error stats
License: ASL 2.0
URL:     https://github.com/prometheus/%{name}

Source0: https://github.com/ProdriveTechnologies/hpraid_exporter/archive/v%{version}.tar.gz
Source1: %{name}.service
Source2: %{name}.default

Requires: ssacli

%description

Prometheus exporter for the HP RAID utility 'ssacli'

%prep
%setup -q -c -n v%{version}.tar.gz

%build
cd %{_builddir}/v%{version}.tar.gz/%{name}-%{version}
./build_static.sh

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/%{name}
install -D -m 755 %{_builddir}/v%{version}.tar.gz/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %{_sharedstatedir}/%{name}
