#!/bin/sh
set -e
builder=$(buildah from registry.redhat.io/ubi9/ubi)
container=$(buildah from registry.redhat.io/ubi9-micro)
mountpoint=$(buildah mount ${container})


# --installroot ${mountpoint}
# Install dependencies into the runtime container
buildah run ${builder} -- bash -C <<EOF
    yum list  --installroot ${mountpoint}
    yum remove --installroot ${mountpoint} bash sh
    yum clean all --installroot ${mountpoint}
EOF

echo "hello" > ${mountpoint}/hello.txt

buildah commit --format docker ${container} microsleep
buildah unmount ${container}

