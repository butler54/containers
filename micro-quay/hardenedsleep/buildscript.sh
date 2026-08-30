#!/bin/sh
set -e
builder=$(buildah from registry.redhat.io/ubi9/ubi)
container=$(buildah from registry.redhat.io/ubi9-micro)
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