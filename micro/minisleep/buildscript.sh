#!/bin/sh
set -e
builder=$(buildah from registry.redhat.io/ubi9/ubi)
container=$(buildah from registry.redhat.io/ubi9-micro)
mountpoint=$(buildah mount ${container})


buildah run ${builder} -- touch /hello

# Install dependencies into the runtime container
buildah run ${builder} --volume $mountpoint:/hello:z -- bash -C <<EOF
    yum remove -y --installroot /hello --releasever 9 \
        --setopt install_weak_deps=false \
        --nodocs \
        bash
    yum clean all --installroot /hello
EOF

buildah commit --format docker ${container} microsleep
buildah unmount ${container}

