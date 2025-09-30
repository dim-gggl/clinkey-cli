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
  
	def install
	  virtualenv_install_with_resources
	end
  
	test do
	  output = shell_output("#{bin}/clinkey --length 12 --type strong")
	  assert_equal 12, output.strip.delete("-_").length
	end
  end
  