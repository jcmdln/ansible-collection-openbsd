# SPDX-License-Identifier: ISC
#
# Copyright (c) 2022 Johnathan C. Maudlin <jcmdln@gmail.com>

Vagrant.configure("2") do |config|
  config.vagrant.plugins = ["vagrant-hostmanager", "vagrant-libvirt"]

  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true

  config.nfs.verify_installed = false
  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.vm.box = "jcmdln/openbsd"
  config.vm.box_version = "7.2"
  config.vm.define "openbsd"

  config.vm.provider "libvirt" do |v|
    v.cpus = 2
    v.memory = 2048
  end
end
