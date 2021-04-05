# Vagrantfile

Vagrant.configure("2") do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  config.nfs.verify_installed = false
  config.ssh.verify_host_key = false
  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.vm.box = "generic/openbsd6"
  config.vm.provider "libvirt" do |v|
    v.cpus = 1
    v.memory = 1024
  end
end
