







在所需 kernel module 的文件夹里新建`dkms.conf`：
```
MAKE="make -C src/ KERNELDIR=/lib/modules/${kernelver}/build"
CLEAN="make -C src/ clean"
BUILT_MODULE_NAME=awesome
BUILT_MODULE_LOCATION=src/
PACKAGE_NAME=awesome
PACKAGE_VERSION=1.1
REMAKE_INITRD=yes
```

