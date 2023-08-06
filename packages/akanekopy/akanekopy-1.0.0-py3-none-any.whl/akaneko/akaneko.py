import requests
import asyncio

class Akaneko():
	@staticmethod
	def get(params):
		res = requests.get(f"https://akaneko-api.herokuapp.com/api/{params}")
		json = res.json()
		url = json["url"]
		return url

	@staticmethod
	def neko():
		return Akaneko().get("neko")

	@staticmethod
	def sfwfoxes():
		return Akaneko().get("sfwfoxes")

	@staticmethod
	def wallpaper():
		return Akaneko().get("wallpaper")

	@staticmethod
	def mobileWallpapers():

		@staticmethod
		def bdsm():
			return Akaneko().get("bdsm")

		@staticmethod
		def cum():
			return Akaneko().get("cum")

		@staticmethod
		def doujin():
			return Akaneko().get("doujin")

		@staticmethod
		def femdom():
			return Akaneko().get("femdom")

		@staticmethod
		def hentai():
			return Akaneko().get("hentai")

		@staticmethod
		def maid():
			return Akaneko().get("maid")

		@staticmethod
		def orgy():
			return Akaneko().get("orgy")

		@staticmethod
		def panties():
			return Akaneko().get("panties")

		@staticmethod
		def wallpaper():
			return Akaneko().get("wallpaper")

		@staticmethod
		def mobilewallpapers():
			return Akaneko().get("mobilewallpapers")

		@staticmethod
		def cuckhold():
			return Akaneko().get("netorare")

		@staticmethod
		def netorare():
			return Akaneko().get("netorare")

		@staticmethod
		def gifs():
			return Akaneko().get("gif")

		@staticmethod
		def gif():
			return Akaneko().get("gif")

		@staticmethod
		def blowjob():
			return Akaneko().get("blowjob")

		@staticmethod
		def feet():
			return Akaneko().get("feet")

		@staticmethod
		def pussy():
			return Akaneko().get("feet")

		@staticmethod
		def uglyBastard():
			return Akaneko().get("uglybastard")

		@staticmethod
		def uniform():
			return Akaneko().get("uniform")

		@staticmethod
		def gangbang():
			return Akaneko().get("gangbang")

		@staticmethod
		def foxgirl():
			return Akaneko().get("foxgirl")

		@staticmethod
		def cumslut():
			return Akaneko().get("cumslut")

		@staticmethod
		def glasses():
			return Akaneko().get("glasses")

		@staticmethod
		def thighs():
			return Akaneko().get("thighs")

		@staticmethod
		def tentacles():
			return Akaneko().get("tentacles")

		@staticmethod
		def loli():
			return Akaneko().get("loli")

		@staticmethod
		def masturbation():
			return Akaneko().get("masturbation")

		@staticmethod
		def school():
			return Akaneko().get("school")

		@staticmethod
		def yuri():
			return Akaneko().get("yuri")

		@staticmethod
		def zettaiRyouiki():
			return Akaneko().get("zettai-ryouiki")

akaneko = Akaneko()
akaneko.nsfw = akaneko.Nsfw()