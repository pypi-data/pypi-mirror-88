import requests
import asyncio

class Akaneko():
	def __get(params):
		res = requests.__get(f"https://akaneko-api.herokuapp.com/api/{params}")
		json = res.json()
		url = json["url"]
		return url

	@staticmethod
	def neko():
		return Akaneko().__get("neko")

	@staticmethod
	def sfwfoxes():
		return Akaneko().__get("sfwfoxes")

	@staticmethod
	def wallpaper():
		return Akaneko().__get("wallpaper")

	@staticmethod
	def mobileWallpapers():
		return Akaneko().__get("mobileWallpapers")

	class Nsfw:

		@staticmethod
		def bdsm():
			return Akaneko().__get("bdsm")

		@staticmethod
		def cum():
			return Akaneko().__get("cum")

		@staticmethod
		def doujin():
			return Akaneko().__get("doujin")

		@staticmethod
		def femdom():
			return Akaneko().__get("femdom")

		@staticmethod
		def hentai():
			return Akaneko().__get("hentai")

		@staticmethod
		def maid():
			return Akaneko().__get("maid")

		@staticmethod
		def orgy():
			return Akaneko().__get("orgy")

		@staticmethod
		def panties():
			return Akaneko().__get("panties")

		@staticmethod
		def wallpaper():
			return Akaneko().__get("wallpaper")

		@staticmethod
		def mobilewallpapers():
			return Akaneko().__get("mobilewallpapers")

		@staticmethod
		def cuckhold():
			return Akaneko().__get("netorare")

		@staticmethod
		def netorare():
			return Akaneko().__get("netorare")

		@staticmethod
		def gifs():
			return Akaneko().__get("gif")

		@staticmethod
		def gif():
			return Akaneko().__get("gif")

		@staticmethod
		def blowjob():
			return Akaneko().__get("blowjob")

		@staticmethod
		def feet():
			return Akaneko().__get("feet")

		@staticmethod
		def pussy():
			return Akaneko().__get("feet")

		@staticmethod
		def uglyBastard():
			return Akaneko().__get("uglybastard")

		@staticmethod
		def uniform():
			return Akaneko().__get("uniform")

		@staticmethod
		def gangbang():
			return Akaneko().__get("gangbang")

		@staticmethod
		def foxgirl():
			return Akaneko().__get("foxgirl")

		@staticmethod
		def cumslut():
			return Akaneko().__get("cumslut")

		@staticmethod
		def glasses():
			return Akaneko().__get("glasses")

		@staticmethod
		def thighs():
			return Akaneko().__get("thighs")

		@staticmethod
		def tentacles():
			return Akaneko().__get("tentacles")

		@staticmethod
		def loli():
			return Akaneko().__get("loli")

		@staticmethod
		def masturbation():
			return Akaneko().__get("masturbation")

		@staticmethod
		def school():
			return Akaneko().__get("school")

		@staticmethod
		def yuri():
			return Akaneko().__get("yuri")

		@staticmethod
		def zettaiRyouiki():
			return Akaneko().__get("zettai-ryouiki")

akaneko = Akaneko()
akaneko.nsfw = Akaneko().Nsfw()