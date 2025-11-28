class ClinkeyCli < Formula
	include Language::Python::Virtualenv
  
	desc "Command-line generator for secure passwords and secret keys"
	homepage "https://github.com/dim-gggl/clinkey-cli"
	license "MIT"
  
	# URL qui pointe vers l'archive .tar.gz de votre release sur GitHub
	url "https://files.pythonhosted.org/packages/c7/53/7c3cd257928a4f3a1bce4780de9737efaf423bf897f92ae277a71d513f41/clinkey_cli-2.0.0.tar.gz"
  
	# Le hash de sécurité que vous avez calculé
	sha256 "690dd846b97240f23bbe037afe0096d01ca25418e6dc1c664595ba802b762d4c"
  
	depends_on "python@3.12"

	resource "anyio" do
  	  url "https://files.pythonhosted.org/packages/c6/78/7d432127c41b50bccba979505f272c16cbcadcc33645d5fa3a738110ae75/anyio-4.11.0.tar.gz"
  	  sha256 "82a8d0b81e318cc5ce71a5f1f8b5c4e63619620b63141ef8c995fa0db95a57c4"
    end
  
    resource "certifi" do
  	  url "https://files.pythonhosted.org/packages/a2/8c/58f469717fa48465e4a50c014a0400602d3c437d7c0c468e17ada824da3a/certifi-2025.11.12.tar.gz"
  	  sha256 "d8ab5478f2ecd78af242878415affce761ca6bc54a22a27e026d7c25357c3316"
    end
  
    resource "click" do
  	  url "https://files.pythonhosted.org/packages/3d/fa/656b739db8587d7b5dfa22e22ed02566950fbfbcdc20311993483657a5c0/click-8.3.1.tar.gz"
  	  sha256 "12ff4785d337a1bb490bb7e9c2b1ee5da3112e94a8622f26a6c77f5d2fc6842a"
    end
  
    resource "h11" do
  	  url "https://files.pythonhosted.org/packages/01/ee/02a2c011bdab74c6fb3c75474d40b3052059d95df7e73351460c8588d963/h11-0.16.0.tar.gz"
  	  sha256 "4e35b956cf45792e4caa5885e69fba00bdbc6ffafbfa020300e549b208ee5ff1"
    end
  
    resource "httpcore" do
  	  url "https://files.pythonhosted.org/packages/06/94/82699a10bca87a5556c9c59b5963f2d039dbd239f25bc2a63907a05a14cb/httpcore-1.0.9.tar.gz"
  	  sha256 "6e34463af53fd2ab5d807f399a9b45ea31c3dfa2276f15a2c3f00afff6e176e8"
    end
  
    resource "httpx" do
  	  url "https://files.pythonhosted.org/packages/b1/df/48c586a5fe32a0f01324ee087459e112ebb7224f646c0b5023f5e79e9956/httpx-0.28.1.tar.gz"
  	  sha256 "75e98c5f16b0f35b567856f597f06ff2270a374470a5c2392242528e3e3e42fc"
    end
  
    resource "idna" do
  	  url "https://files.pythonhosted.org/packages/6f/6d/0703ccc57f3a7233505399edb88de3cbd678da106337b9fcde432b65ed60/idna-3.11.tar.gz"
  	  sha256 "795dafcc9c04ed0c1fb032c2aa73654d8e8c5023a7df64a53f39190ada629902"
    end
  
    resource "markdown-it-py" do
  	  url "https://files.pythonhosted.org/packages/5b/f5/4ec618ed16cc4f8fb3b701563655a69816155e79e24a17b651541804721d/markdown_it_py-4.0.0.tar.gz"
  	  sha256 "cb0a2b4aa34f932c007117b194e945bd74e0ec24133ceb5bac59009cda1cb9f3"
    end
  
    resource "mdurl" do
  	  url "https://files.pythonhosted.org/packages/d6/54/cfe61301667036ec958cb99bd3efefba235e65cdeb9c84d24a8293ba1d90/mdurl-0.1.2.tar.gz"
  	  sha256 "bb413d29f5eea38f31dd4754dd7377d4465116fb207585f97bf925588687c1ba"
    end
  
    resource "Pygments" do
  	  url "https://files.pythonhosted.org/packages/b0/77/a5b8c569bf593b0140bde72ea885a803b82086995367bf2037de0159d924/pygments-2.19.2.tar.gz"
  	  sha256 "636cb2477cec7f8952536970bc533bc43743542f70392ae026374600add5b887"
    end
  
    resource "rich" do
  	  url "https://files.pythonhosted.org/packages/fb/d2/8920e102050a0de7bfabeb4c4614a49248cf8d5d7a8d01885fbb24dc767a/rich-14.2.0.tar.gz"
  	  sha256 "73ff50c7c0c1c77c8243079283f4edb376f0f6442433aecb8ce7e6d0b92d1fe4"
    end
  
    resource "rich-click" do
  	  url "https://files.pythonhosted.org/packages/bf/d8/f2c1b7e9a645ba40f756d7a5b195fc104729bc6b19061ba3ab385f342931/rich_click-1.9.4.tar.gz"
  	  sha256 "af73dc68e85f3bebb80ce302a642b9fe3b65f3df0ceb42eb9a27c467c1b678c8"
    end
  
    resource "sniffio" do
  	  url "https://files.pythonhosted.org/packages/a2/87/a6771e1546d97e7e041b6ae58d80074f81b7d5121207425c964ddf5cfdbd/sniffio-1.3.1.tar.gz"
  	  sha256 "f4324edc670a0f49750a81b895f35c3adb843cca46f0530f79fc1babb23789dc"
    end
  
	def install
	  virtualenv_install_with_resources
	end
  
	test do
	  output = shell_output("#{bin}/clinkey --length 12 --type strong --no-sep")
	  assert_operator output.strip.length, :>, 0
	end
  end
  