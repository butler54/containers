#!/bin/sh
set -e
builder=$(buildah from registry.access.redhat.com/ubi9/ubi@sha256:25a147defd01e19674714f55d17538c8dbe55d8c305fa157ecc3f9c8977b05b6)
container=$(buildah from registry.access.redhat.com/ubi9-micro@sha256:f332c99eb8f798a8486821c91937f10ad64ee83d7e739303be2df051040918f6)
mountpoint=$(buildah mount ${container})


# --installroot ${mountpoint}
# Install dependencies into the runtime container
buildah run ${builder} -- bash -C <<EOF
    yum list  --installroot ${mountpoint}
    yum remove -y --installroot ${mountpoint} --releasever 9 bash
    yum clean all --installroot ${mountpoint}
EOF

ls -l ${mountpoint}/usr/bin

## Remove all the uneeded binaries
rm ${mountpoint}/usr/bin/bash
rm ${mountpoint}/usr/bin/sh
rm ${mountpoint}/usr/bin/less
rm ${mountpoint}/usr/bin/more
rm ${mountpoint}/usr/bin/cat

buildah unmount ${container}
buildah commit --format docker ${container} hardenedsleep