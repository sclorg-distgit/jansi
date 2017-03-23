%global pkg_name jansi
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

Name:             %{?scl_prefix}%{pkg_name}
Version:          1.9
Release:          7.14%{?dist}
Summary:          Jansi is a java library for generating and interpreting ANSI escape sequences
License:          ASL 2.0
URL:              http://jansi.fusesource.org/

# git clone git://github.com/fusesource/jansi.git
# cd jansi && git archive --format=tar --prefix=jansi-1.9/ jansi-project-1.9 | xz > jansi-1.9.tar.xz
Source0:          jansi-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    %{?scl_prefix}javapackages-tools
BuildRequires:    %{?scl_prefix}maven-local
BuildRequires:    %{?scl_prefix_maven}maven-release-plugin
BuildRequires:    %{?scl_prefix}jansi-native
BuildRequires:    %{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:    %{?scl_prefix_maven}fusesource-pom


%description
Jansi is a small java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences.

%package javadoc
Summary:          Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x

%pom_disable_module jansi-website
%pom_xpath_remove "pom:build/pom:extensions"

# No org.fusesource.mvnplugins:fuse-javadoc-skin available
%pom_remove_plugin "org.apache.maven.plugins:maven-dependency-plugin"

# No maven-uberize-plugin
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-uberize-plugin']" jansi/pom.xml

%mvn_file org.fusesource.jansi:jansi %{pkg_name}

# Remove unnecessary deps for jansi-native builds
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:artifactId = 'jansi-native' and pom:classifier != '']" jansi/pom.xml
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_mavenpomdir}/%{pkg_name}
%doc readme.md license.txt changelog.md

%files javadoc -f .mfiles-javadoc
%doc license.txt

%changelog
* Mon Jan 16 2017 Michael Simacek <msimacek@redhat.com> - 1.9-7.14
- Rebuild to regenerate requires on java-headless
- Resolves: rhbz#1413545

* Wed Jan 14 2015 Michal Srb <msrb@redhat.com> - 1.9-7.13
- Fix directory ownership

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.9-7.12
- Mass rebuild 2015-01-13

* Fri Jan 09 2015 Michal Srb <msrb@redhat.com> - 1.9-7.11
- Mass rebuild 2015-01-09

* Tue Dec 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.10
- Migrate requires and build-requires to rh-java-common

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.9
- Mass rebuild 2014-12-15

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.8
- Rebuild for rh-java-common collection

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-7.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.9-7
- Mass rebuild 2013-12-27

* Mon Nov 11 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.9-6
- Rebuild for jansi-native changes
- Resolves: rhbz#1028540

* Thu Aug 15 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.9-5
- Migrate away from mvn-rpmbuild (#997431)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-4
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.9-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Oct 09 2012 Marek Goldmann <mgoldman@redhat.com> - 1.9-1
- Upstream release 1.9, RHBZ#864490

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 04 2012 Tomas Radej <tradej@redhat.com> - 1.6-3
- Removed maven-license-plugin BR

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Marek Goldmann <mgoldman@redhat.com> 1.6-1
- Upstream release 1.6
- Spec file cleanup

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.5-1
- Initial packaging
