class ClinkeyCli < Formula
	include Language::Python::Virtualenv
  
	desc "Command-line generator for secure passwords and secret keys"
	homepage "https://github.com/dim-gggl/clinkey-cli"
	license "MIT"
  
	# URL qui pointe vers l'archive .tar.gz de votre release sur GitHub
	url "https://github.com/dim-gggl/clinkey-cli/archive/refs/tags/v1.1.0.tar.gz"
  
	# Le hash de sécurité que vous avez calculé
	sha256 "85443a3ca90a461455c8f448eb645802d5e6abda6cdc3ee8b3743ed04183b255"
  
	depends_on "python@3.12"

	resource "click" do
		url "https://files.pythonhosted.org/packages/source/c/click/click-8.1.7.tar.gz"
		sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de"
	end

	resource "rich" do
		url "https://files.pythonhosted.org/packages/source/r/rich/rich-14.1.0.tar.gz"
		sha256 "e497a48b844b0320d45007cdebfeaeed8db2a4f4bcf49f15e455cfc4af11eaa8"
	end
  
	def install
	  inreplace "pyproject.toml", "click>=8.3.0", "click>=8.1.7"
	  virtualenv_install_with_resources
	end
  
	test do
	  output = shell_output("#{bin}/clinkey --length 12 --type strong")
	  assert_equal 12, output.strip.delete("-_").length
	end
  end
  