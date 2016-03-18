%global service group-based-policy

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:		openstack-neutron-gbp
Version:	XXX
Release:	XXX
Summary:	Group Based Policy service plugin for OpenStack Networking Service

License:	ASL 2.0
URL:		https://launchpad.net/group-based-policy

Source0:	http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-pbr
BuildRequires:	python-setuptools

Requires:	openstack-neutron >= 7.0
Requires:	python-pbr


%description
Group Based Policy (GBP) provides declarative abstractions for
achieving scalable intent-based infrastructure automation. GBP
complements the OpenStack networking model with the notion of policies
that can be applied between groups of network endpoints.


%prep
%setup -qn group-based-policy-%{upstream_version}

find gbpservice -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

rm -f requirements.txt


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python2_sitelib}/gbpservice/neutron/tests
rm -rf %{buildroot}%{python2_sitelib}/gbpservice/tests

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron
mv %{buildroot}/usr/etc/group-based-policy %{buildroot}%{_sysconfdir}/neutron
mv %{buildroot}%{_sysconfdir}/neutron/group-based-policy/policy.d/policy.json %{buildroot}%{_sysconfdir}/neutron/group-based-policy
rm -rf %{buildroot}%{_sysconfdir}/neutron/group-based-policy/policy.d
mv %{buildroot}/usr/etc/servicechain %{buildroot}%{_sysconfdir}/neutron
chmod 640  %{buildroot}%{_sysconfdir}/neutron/group-based-policy/*.ini
chmod 640  %{buildroot}%{_sysconfdir}/neutron/group-based-policy/policy.json
chmod 640  %{buildroot}%{_sysconfdir}/neutron/group-based-policy/*/*.ini
chmod 640  %{buildroot}%{_sysconfdir}/neutron/servicechain/*/*/*.ini


%files
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/neutron/group-based-policy
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/group-based-policy/*.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/group-based-policy/policy.json
%dir %{_sysconfdir}/neutron/group-based-policy/drivers
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/group-based-policy/drivers/*.ini
%dir %{_sysconfdir}/neutron/servicechain
%dir %{_sysconfdir}/neutron/servicechain/plugins
%dir %{_sysconfdir}/neutron/servicechain/plugins/msc
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/servicechain/plugins/msc/*.ini
%{_bindir}/gbp-db-manage
%{python2_sitelib}/gbpservice
%{python2_sitelib}/group_based_policy-*.egg-info


%changelog
