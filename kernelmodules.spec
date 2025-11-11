%global module1 linuwu_sense
%global module2 evdi
%global kernel_ver_real %(uname -r)
%global kernel_ver_base %(uname -r | sed 's/\\.x86_64$//' | sed 's/\\.aarch64$//')
%global kernel_ver_sanitized %(echo %{kernel_ver_base} | tr - _)

Name:             kernel-modules-collection
Version:          1.0
Release:          %{kernel_ver_sanitized}
Summary:          Custom kernel modules for kernel %{kernel_ver_real}
License:          GPLv2
URL:              https://github.com/SoloSaravanan

BuildRequires:    make gcc kernel-devel
Requires(post):   kmod
Requires(postun): kmod

Provides:         kmod(%{module1}) = %{version}-%{release}
Provides:         kmod(%{module2}) = %{version}-%{release}
Provides:         kernel-modules-for-kernel = %{kernel_ver_real}

Obsoletes:        kernel-modules-collection < %{version}-%{release}
Conflicts:        kernel-modules-collection < %{version}-%{release}

%description
This package provides collection of kernel modules built for kernel %{kernel_ver_real}.

%prep
cp -a %{_sourcedir}/Linuwu-Sense .
cp -a %{_sourcedir}/evdi .

%build
make KVER=%{kernel_ver_real} -C Linuwu-Sense
make KVER=%{kernel_ver_real} -C evdi

%install
# linuwu_sense
mkdir -p %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86
install -m 644 Linuwu-Sense/%{module1}.ko \
    %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86/

# evdi
mkdir -p %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/gpu/drm/evdi
install -m 644 evdi/%{module2}.ko \
    %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/gpu/drm/evdi/

%post
/sbin/depmod -a %{kernel_ver_real} || true

%postun
/sbin/depmod -a %{kernel_ver_real} || true

%files
/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86/%{module1}.ko
/lib/modules/%{kernel_ver_real}/kernel/drivers/gpu/drm/evdi/%{module2}.ko
