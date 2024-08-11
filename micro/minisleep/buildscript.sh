#!/bin/sh
set -e
builder=$(buildah from registry.redhat.io/ubi9/ubi)
container=$(buildah from registry.redhat.io/ubi9-micro)
mountpoint=$(buildah mount ${container})


buildah run ${builder} -- touch /hello

# --installroot ${mountpoint}
# Install dependencies into the runtime container
buildah run ${builder} -- bash -C <<EOF
    yum list
    yum remove -y --installroot ${mountpoint} --releasever 9 bash
    yum clean all --installroot ${mountpoint}
EOF

buildah commit --format docker ${container} microsleep
buildah unmount ${container}

