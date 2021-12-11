# SPDX-License-Identifier: ISC

variable "os_arch" {
    type = string
    default = "amd64"
}

variable "os_mirror" {
    type = string
    default = "https://cdn.openbsd.org/pub/OpenBSD"
}

variable "os_version" {
    type = string
    default = "7.0"
}

locals {
    version_flat = replace("${var.os_version}", ".", "")
    image_name = "openbsd-${local.version_flat}-${var.os_arch}"
    iso_name = "cd${local.version_flat}.iso"
    mirror_path = "${var.os_mirror}/${var.os_version}/${var.os_arch}"
}

source "qemu" "openbsd" {
    accelerator = "kvm"
    boot_command = [
        "a<enter><wait2>",
        "http://{{ .HTTPIP }}:{{ .HTTPPort }}/install.conf<enter><wait2>",
        "i<enter>",
    ]
    boot_wait = "30s"
    cpus = 2
    disk_compression = true
    disk_interface = "virtio-scsi"
    disk_size = "20G"
    format = "qcow2"
    headless = true
    http_directory = "./"
    iso_checksum = "file:${local.mirror_path}/SHA256"
    iso_url = "${local.mirror_path}/${local.iso_name}"
    memory = 2048
    net_device = "virtio-net"
    output_directory = "./build"
    shutdown_command = "shutdown -h -p now"
    ssh_agent_auth = false
    ssh_password = "vagrant"
    ssh_timeout = "15m"
    ssh_username = "root"
    vm_name = "${local.image_name}.qcow2"
}

build {
    sources = ["sources.qemu.openbsd"]

    provisioner "shell" {
        inline = [
            "cp /etc/examples/doas.conf /etc/doas.conf",
            "echo 'permit nopass vagrant' >> /etc/doas.conf",
            "doas -C /etc/doas.conf",
        ]
    }

    post-processor "vagrant" {
        compression_level = 9
        keep_input_artifact = true
        output = "./build/${local.image_name}.box"
        provider_override = "libvirt"
    }
}
