# SPDX-License-Identifier: ISC
#
# Copyright (c) 2022 Johnathan C. Maudlin <jcmdln@gmail.com>

Vagrant.configure("2") do |config|
  config.vagrant.plugins = ["vagrant-libvirt"]
  config.vm.box = "jcmdln/openbsd"
  config.vm.box_version = "7.2-20221124T164941"
  config.vm.define "ac-openbsd"
  config.vm.provider "libvirt" do |v|
    v.cpus = 2
    v.memory = 2048
  end
end
