provider "oci" {}

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_id
}

locals {
  # Gather a list of availability domains for use in configuring placement_configs
  azs = data.oci_identity_availability_domains.ads.availability_domains[*].name
}


data "oci_core_subnets" "private_subnets" {
	compartment_id = var.compartment_id
    filter {
        name="display_name"
        values=["k8s-private-subnet"]
        regex=false
        }    
}

resource "oci_file_storage_file_system" "searchagent_freelance-fs" {
	availability_domain = local.azs[0]
	compartment_id = var.compartment_id
	display_name = "searchagent_freelance-fs"
}

resource "oci_file_storage_mount_target" "searchagent_freelance-mt" {
	availability_domain = local.azs[0]
	compartment_id = var.compartment_id
	display_name = "searchagent_freelance-mt"
	subnet_id = data.oci_core_subnets.private_subnets.subnets[0].id
}

resource "oci_file_storage_export" "searchagent_freelance-export" {
	export_set_id = "${oci_file_storage_mount_target.searchagent_freelance-mt.export_set_id}"
	file_system_id = "${oci_file_storage_file_system.searchagent_freelance-fs.id}"
	path = "/searchagentfreelance-fs"
}



