# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Filter without dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class ShowCharacter(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Character',
			'de': u'Zeichen',
			'fr': u'caractère',
			'zh': u'👩‍🏫参考字',
		})
	
	@objc.python_method
	def drawMultipleTextAtPoint(self, text, textPosition, fontSize=10.0, fontColor=NSColor.blackColor(), align='left', fontNames=() ):
		try:
			alignment = {
				'topleft': 6, 'topcenter': 7, 'topright': 8,
				'left': 3, 'center': 4, 'right': 5,
				'bottomleft': 0, 'bottomcenter': 1, 'bottomright': 2,
			}
			
			textAlignment = alignment[align]
			currentZoom = self.getScale()
			
			# see if the font names are among the installed fonts:
			verifiedFonts = []
			for fontName in fontNames:
				font = NSFont.fontWithName_size_(fontName, fontSize / currentZoom)
				if font:
					verifiedFonts.append(font)
			
			# if not, use system font as fallback:
			if not verifiedFonts:
				systemFont = NSFont.labelFontOfSize_(fontSize / currentZoom)
				verifiedFonts.append(systemFont)
			
			for font in verifiedFonts:
				fontAttributes = {
					NSFontAttributeName: font,
					NSForegroundColorAttributeName: fontColor,
				}
				displayText = NSAttributedString.alloc().initWithString_attributes_("%s"%text, fontAttributes)
				displayText.drawAtPoint_alignment_(textPosition, textAlignment)
				advanceWidth = displayText.size().width
				x,y = textPosition
				textPosition = (x+advanceWidth, y)
		except Exception as e:
			print(e)
			import traceback
			print(traceback.format_exc())
	
	@objc.python_method
	def foreground(self, layer):
		glyph = layer.parent
		character = glyph.glyphInfo.unicharString()
		
		# try again if glyph has no unicode character associated with it:
		if not character and "." in glyph.name:
			nameWithoutSuffix = glyph.name[:glyph.name.find(".")]
			glyphInfo = Glyphs.glyphInfoForName(nameWithoutSuffix)
			character = glyphInfo.unicharString()
			
		if character:
			font = Glyphs.font
			tab = font.currentTab
			if tab.scale > 0.1999:
				master = layer.associatedFontMaster()
				y = max(master.ascender, layer.bounds.origin.y+layer.bounds.size.height+50.0)
		
				fontSize = 100.0
				fontNames = []
				extraFontNames = font.customParameters["Sample Fonts"]
				if extraFontNames:
					if ";" in extraFontNames:
						# there is a fontsize passed as well:
						parsedParameter = extraFontNames.split(";")
						extraFontNames = parsedParameter[0].strip()
						try:
							parsedFontSize = float(parsedParameter[1].strip())
							if parsedFontSize > 0.0:
								fontSize = parsedFontSize
						except:
							pass
				
					fontNames += [name.strip() for name in extraFontNames.split(",") if name]
			
				self.drawMultipleTextAtPoint(
					character, NSPoint(0,y), 
					fontSize=fontSize, 
					fontColor=NSColor.colorWithRed_green_blue_alpha_(0.1, 0.4, 0.8, 0.6),
					fontNames=fontNames,
					align="bottomleft",
					)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
