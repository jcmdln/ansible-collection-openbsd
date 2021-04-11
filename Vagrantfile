# Vagrantfile

Vagrant.configure("2") do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true
  config.nfs.verify_installed = false
  config.ssh.verify_host_key = false
  config.vm.box = "generic/openbsd6"
  config.vm.provider "libvirt" do |v|
    v.cpus = 1
    v.memory = 1024
  end
  config.vm.synced_folder '.', '/vagrant', disabled: true

  #
  # Boxes
  #

  config.vm.define :openbsd_1 do |c|
    c.vm.hostname = "openbsd-1"
  end

end
