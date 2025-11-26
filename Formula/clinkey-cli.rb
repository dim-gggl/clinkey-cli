class ClinkeyCli < Formula
	include Language::Python::Virtualenv
  
	desc "Command-line generator for secure passwords and secret keys"
	homepage "https://github.com/dim-gggl/clinkey-cli"
	license "MIT"
  
	# URL qui pointe vers l'archive .tar.gz de votre release sur GitHub
	url "https://files.pythonhosted.org/packages/3e/a7/b62c63a25a94808caa6d1779b51fe6c5cf7bdffc9c6391e451d02fe45e5a/clinkey_cli-1.2.0.tar.gz"
  
	# Le hash de sécurité que vous avez calculé
	sha256 "63457efd9231c23b3e64f9bd422b7c880fcfcb4491e5104932ff33b3a6e5ce32"
  
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
	  output = shell_output("#{bin}/clinkey --length 12 --type strong --no-sep")
	  assert_operator output.strip.length, :>, 0
	end
  end
  