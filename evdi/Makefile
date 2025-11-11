KVER ?= $(shell uname -r)
KERNELDIR ?= /lib/modules/$(KVER)/build
PWD := $(shell pwd)

KBUILD_CFLAGS += -fno-pic -fno-pie -no-pie
KBUILD_AFLAGS += -fno-pic -fno-pie -no-pie

# Object list
obj-m := evdi.o
evdi-y := \
	evdi_platform_drv.o \
	evdi_platform_dev.o \
	evdi_painter.o \
	evdi_params.o \
	evdi_encoder.o \
	evdi_modeset.o \
	evdi_connector.o \
	evdi_cursor.o \
	evdi_fb.o \
	evdi_gem.o \
	evdi_i2c.o \
	evdi_drm_drv.o \
	evdi_debug.o \
	evdi_sysfs.o \
	evdi_ioc32.o

all:
	@echo "Building EVDI for kernel: $(KVER)"
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) clean
	rm -f modules.order

install:
	@echo "Installing EVDI into /lib/modules/$(KVER)/extra/"
	mkdir -p /lib/modules/$(KVER)/extra
	install -m 644 evdi.ko /lib/modules/$(KVER)/extra/
	depmod -a $(KVER)

.PHONY: all clean install
