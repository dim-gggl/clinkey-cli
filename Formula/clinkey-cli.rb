class ClinkeyCli < Formula
	include Language::Python::Virtualenv
  
	desc "Command-line generator for secure passwords and secret keys"
	homepage "https://github.com/dim-gggl/clinkey-cli"
	license "MIT"
  
	# URL qui pointe vers l'archive .tar.gz de votre release sur GitHub
	url "https://github.com/dim-gggl/clinkey-cli/archive/refs/tags/v1.0.1.tar.gz"
  
	# Le hash de sécurité que vous avez calculé
	sha256 "c3022aae431d6978b7895768a65da13dbc2d6aace4ce7a2dbf748e83dc0c207f"
  
	depends_on "python@3.12"
  
	def install
	  virtualenv_install_with_resources
	end
  
	test do
	  output = shell_output("#{bin}/clinkey --length 12 --type strong")
	  assert_equal 12, output.strip.delete("-_").length
	end
  end
  