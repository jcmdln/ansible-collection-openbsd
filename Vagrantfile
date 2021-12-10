# SPDX-License-Identifier: ISC

ENV["VAGRANT_DEFAULT_PROVIDER"] = "libvirt"
ENV["VAGRANT_NO_PARALLEL"] = "yes"

Vagrant.configure("2") do |config|
  config.vagrant.plugins = ["vagrant-libvirt"]

  config.vm.box = "openbsd-run/openbsd"
  config.vm.define "openbsd"
  config.vm.provider "libvirt" do |v|
    v.cpus = 2
    v.memory = 2048
  end

  config.ssh.shell = "/bin/ksh -l"
  config.ssh.sudo_command = "doas %c"

  config.nfs.verify_installed = false
  config.vm.synced_folder '.', '/vagrant', disabled: true
end
