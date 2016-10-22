%{?scl:%thermostat_find_provides_and_requires}      

%{?scl:%scl_package jansi}
%{!?scl:%global pkg_name %{name}}

Name:             %{?scl_prefix}jansi
Version:          1.9
Release:          11%{?dist}
Summary:          Jansi is a java library for generating and interpreting ANSI escape sequences
License:          ASL 2.0
URL:              http://jansi.fusesource.org/

# git clone git://github.com/fusesource/jansi.git
# cd jansi && git archive --format=tar --prefix=jansi-1.9/ jansi-project-1.9 | xz > jansi-1.9.tar.xz
Source0:          jansi-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    maven30-maven-local
BuildRequires:    maven30-maven-release-plugin
BuildRequires:    maven30-maven-plugin-bundle
BuildRequires:    maven30-fusesource-pom
# 1.4-9 jansi-native has classifier fixes
BuildRequires:    %{?scl_prefix}jansi-native >= 1.4-9


%description
Jansi is a small java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences.

%package javadoc
Summary:          Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%{?scl:scl enable maven30 %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{version}

%pom_disable_module jansi-website
%pom_xpath_remove "pom:build/pom:extensions"

# No org.fusesource.mvnplugins:fuse-javadoc-skin available
%pom_remove_plugin "org.apache.maven.plugins:maven-dependency-plugin"

# No maven-uberize-plugin
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-uberize-plugin']" jansi/pom.xml

# Remove unnecessary deps for jansi-native builds
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:artifactId = 'jansi-native' and pom:classifier != '']" jansi/pom.xml

%mvn_file org.fusesource.jansi:jansi %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc readme.md license.txt changelog.md

%files javadoc -f .mfiles-javadoc
%doc license.txt

%changelog
* Wed Jun 18 2014 Severin Gehwolf <sgehwolf@redhat.com>  - 1.9-11
- Build using maven30 collection.

* Mon Jan 20 2014 Severin Gehwolf <sgehwolf@redhat.com>  - 1.9-10
- Rebuild in order to fix osgi()-style provides.
- Resolves: RHBZ#1054813

* Wed Nov 27 2013 Omair Majid <omajid@redhat.com>  - 1.9-9
- Properly enable SCL.

* Mon Nov 18 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.9-8
- Add macro for java auto-requires/provides.

* Mon Nov 11 2013 Severin Gehwolf <sgehwolf@redhat.com> - 1.9-7
- Rebuild for jansi-native changes.

* Fri Nov 08 2013 Severin Gehwolf <sgehwolf@redhat.com> - 1.9-6
- SCL-ize package.

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
