# Define variables
%global module_name linuwu_sense
# Replace hyphens (-) with underscores (_) to make it RPM-safe
%global kernel_ver_real %(uname -r)
%global kernel_ver_sanitized %(uname -r | tr - _)

Name:             kernel-modules-collection
Version:          1.0
Release:          %{kernel_ver_sanitized}%{?dist}
Summary:          Kernel modules for %{kernel_ver_real}
License:          GPLv2
URL:              https://github.com/SoloSaravanan

BuildRequires:    make gcc kernel-devel
Requires(post):   kmod
Requires(postun): kmod
Provides:         kmod(%{module_name})

Obsoletes:        kernel-modules-collection < %{version}-%{release}
Conflicts:        kernel-modules-collection < %{version}-%{release}

%description
Kernel module %{module_name} built for kernel %{kernel_ver_real}.

%prep
cp -a %{_sourcedir}/Linuwu-Sense .

%build
make KVER=%{kernel_ver_real} -C Linuwu-Sense

%install
mkdir -p %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86
install -m 644 Linuwu-Sense/linuwu_sense.ko \
    %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86/

%post
/sbin/depmod -a %{kernel_ver_real} || true

%postun
/sbin/depmod -a %{kernel_ver_real} || true

%files
/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86/%{module_name}.ko

