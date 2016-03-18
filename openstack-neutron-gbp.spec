%global service group-based-policy

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:		openstack-neutron-gbp
Version:	2015.2.0
Release:	1%{?dist}
Summary:	Group Based Policy service plugin for OpenStack Networking Service

License:	ASL 2.0
URL:		https://launchpad.net/group-based-policy

Source0:	http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-pbr
BuildRequires:	python-setuptools

Requires:	openstack-neutron >= 2015.1
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
* Fri Feb 12 2016 Alan Pevec <alan.pevec@redhat.com> 2015.2.0-1
- Update to 2015.2.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2015.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct  5 2015 Robert Kukura <rk@theep.net> - 2015.1.1-1
- Update to upstream 2015.1.1
- Package config files
- Remove precompiled egg-info

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan  7 2015 Robert Kukura <rk@theep.net> - 2014.2-1
- Update to upstream 2014.2

* Mon Jan  5 2015 Robert Kukura <rk@theep.net> - 2014.2-0.6.rc3
- Update to rc3

* Mon Jan  5 2015 Robert Kukura <rk@theep.net> - 2014.2-0.5.rc2
- Update to rc2
- Updates for renamed top-level python module

* Tue Dec 30 2014 Robert Kukura <rk@theep.net> - 2014.2-0.4.rc1
- Update to rc1
- Remove Group tag
- Use python2_sitelib instead of python_sitelib
- Package sample config file fragment

* Mon Dec 15 2014 Robert Kukura <rk@theep.net> - 2014.2-0.3.acb85f0git
- Don't require specific neutron stable version
- Update to latest upstream commit

* Thu Dec  4 2014 Robert Kukura <rk@theep.net> - 2014.2-0.2.acb85f0git
- Update to commmit with renamed resources

* Mon Nov 17 2014 Robert Kukura <rk@theep.net> - 2014.2-0.1.b3be657git
- Initial package for Fedora
