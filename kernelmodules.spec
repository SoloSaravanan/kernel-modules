%global module1 linuwu_sense
%global module2 evdi
%global module3 xpad
%global kernel_ver_real %(rpm -q kernel-devel --qf '%{VERSION}-%{RELEASE}.%{ARCH}' | head -n1)
%global kver_upstream %(rpm -q kernel-devel --qf '%{VERSION}' | head -n1)
%global kver_release %(rpm -q kernel-devel --qf '%{RELEASE}' | head -n1)

Name:             kernel-modules-collection
Version:          %{kver_upstream}
Release:          %{kver_release}
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
cp -a %{_sourcedir}/xpad .

%build
# Set up kernel build directory symlink
KVER_SHORT=$(echo %{kernel_ver_real} | sed 's/\.x86_64$//' | sed 's/\.aarch64$//')
echo "Kernel version: %{kernel_ver_real}"
echo "Kernel short version: $KVER_SHORT"
echo "Available kernel sources:"
ls -la /usr/src/kernels/ || echo "No /usr/src/kernels directory"

# Find the actual kernel source directory
KERNEL_SRC=$(ls -1d /usr/src/kernels/* 2>/dev/null | head -n1)
if [ -z "$KERNEL_SRC" ]; then
    echo "ERROR: No kernel sources found in /usr/src/kernels/"
    exit 1
fi
echo "Using kernel source: $KERNEL_SRC"

# Create symlink
if [ ! -e /lib/modules/%{kernel_ver_real}/build ]; then
    mkdir -p /lib/modules/%{kernel_ver_real}
    ln -sf "$KERNEL_SRC" /lib/modules/%{kernel_ver_real}/build
fi
echo "Symlink created:"
ls -la /lib/modules/%{kernel_ver_real}/build

make KVER=%{kernel_ver_real} -C Linuwu-Sense
make KVER=%{kernel_ver_real} -C evdi
make KVER=%{kernel_ver_real} -C xpad

%install
# linuwu_sense
mkdir -p %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86
install -m 644 Linuwu-Sense/%{module1}.ko \
    %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86/

# evdi
mkdir -p %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/gpu/drm/evdi
install -m 644 evdi/%{module2}.ko \
    %{buildroot}/lib/modules/%{kernel_ver_real}/kernel/drivers/gpu/drm/evdi/

# xpad
mkdir -p %{buildroot}/lib/modules/%{kernel_ver_real}/extra
install -m 644 xpad/%{module2}.ko \
    %{buildroot}/lib/modules/%{kernel_ver_real}/extra/

%post
/sbin/depmod -a %{kernel_ver_real} || true

%postun
/sbin/depmod -a %{kernel_ver_real} || true

%files
/lib/modules/%{kernel_ver_real}/kernel/drivers/platform/x86/%{module1}.ko
/lib/modules/%{kernel_ver_real}/kernel/drivers/gpu/drm/evdi/%{module2}.ko
/lib/modules/%{kernel_ver_real}/extra/%{module3}.ko
