%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           libkml
Version:        0.6.1
Release:        2%{?dist}
Summary:        A KML library written in C++ with bindings to other languagues

Group:          Development/Libraries
License:        BSD
URL:            http://code.google.com/p/%{name}/
Source0:        http://%{name}.googlecode.com/files/%{name}-%{version}.tar.gz
#Patch0:         libkml-string.patch
Patch1:         libkml-third_party_removal.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# requires swig >= 1.3.35
BuildRequires:  cppunit, swig >= 1.3.35
BuildRequires:  java-devel, libcurl-devel
BuildRequires:  expat-devel, python-devel, chrpath
BuildRequires:  minizip-devel, uriparser-devel, zlib-devel
BuildRequires:  boost-devel
BuildRequires:  autoconf, libtool
Requires:       python, java

%description
Libkml is an implementation of the OGC KML 2.2 standard. is written in
C++ and bindings are available via SWIG to other languages. It can be
used in applications that want to parse, generate and operate on KML.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
rm -rf third_party
%patch1 -p0 -b .third_party
#%patch0 -p1 -b .string

%build
autoreconf -fi
%configure --disable-static \
           --with-java-include-dir=%{_jvmdir}/java
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# remove compiled examples
cd examples; make clean;cd ..

# remove x permssion from examples folder files
find examples -type f -print | xargs chmod a-x

# move libs to kml (for keeping third party libs away)
mkdir -p $RPM_BUILD_ROOT%{_libdir}/libkml/
mv $RPM_BUILD_ROOT%{_libdir}/*.so* $RPM_BUILD_ROOT%{_libdir}/libkml/

#removing rpaths with chrpath
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libkml/libkmldom_swig_java.so.0.0.0
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libkml/libkmlengine_swig_python.so.0.0.0
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libkml/libkmlengine.so.0.0.0
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libkml/libkmldom_swig_python.so.0.0.0
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libkml/libkmlengine_swig_java.so.0.0.0
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/_kmlengine.so
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/_kmldom.so
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/_kmlbase.so

# remove .libs and .deps directories
find . -name '.libs'  -type d -print | xargs rm -rf
find . -name '.deps'  -type d -print | xargs rm -rf

# fix unstripping-binary-or-object warning
chmod a+x $RPM_BUILD_ROOT%{python_sitearch}/_kmlengine.so
chmod a+x $RPM_BUILD_ROOT%{python_sitearch}/_kmldom.so

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%doc AUTHORS
%doc README
%doc ChangeLog
%dir %{_libdir}/libkml
%{_libdir}/libkml/*.so.*
%{python_sitearch}/*.so
%{python_sitearch}/*.py
%{python_sitearch}/*.pyc
%{python_sitearch}/*.pyo

%files devel
%defattr(-,root,root,-)
%doc examples
%{_includedir}/*
%dir %{_libdir}/libkml
%{_libdir}/libkml/*.so

%changelog
* Sat Mar 07 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-2
- updated to 0.6.1
- libkml-third_party_removal.diff Removes third part dependency
- (provided by Peter Lemenkov)

* Fri Jan 16 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-1
- Updated to 0.6.1

* Mon Oct 05 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-2
- Added >= 1.3.35 for swing

* Sat Aug 09 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-1
- Initial package
