class ClinkeyCli < Formula
	include Language::Python::Virtualenv
  
	desc "Command-line generator for secure passwords and secret keys"
	homepage "https://github.com/dim-gggl/clinkey-cli"
	license "MIT"
  
	# URL qui pointe vers l'archive .tar.gz de votre release sur GitHub
	url "https://github.com/dim-gggl/clinkey-cli/archive/refs/tags/v1.0.2.tar.gz"
  
	# Le hash de sécurité que vous avez calculé
	sha256 "62650e850423f5305ac93cd3f6701ea65707e72f0762929f6fc58af4f565f03b"
  
	depends_on "python@3.12"
  
	def install
	  virtualenv_install_with_resources
	end
  
	test do
	  output = shell_output("#{bin}/clinkey --length 12 --type strong")
	  assert_equal 12, output.strip.delete("-_").length
	end
  end
  