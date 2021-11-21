# SPDX-License-Identifier: ISC

ENV["VAGRANT_DEFAULT_PROVIDER"] = "libvirt"
ENV["VAGRANT_NO_PARALLEL"] = "yes"

Vagrant.configure("2") do |config|
  config.vagrant.plugins = "vagrant-hostmanager"

  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true

  config.nfs.verify_installed = false
  config.ssh.verify_host_key = false
  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.vm.box = "generic/openbsd7"
  config.vm.box_version = "3.5.2"
  config.vm.provider "libvirt" do |v|
    v.cpus = 2
    v.memory = 4096
  end

  #
  # Boxes
  #

  config.vm.define "openbsd-1" do |c|
    c.vm.hostname = "openbsd-1"
  end
end
