# encoding: utf-8

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


from GlyphsApp.plugins import *

class DeleteShortSegments(FilterWithoutDialog):
	
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Delete Short Segments', 'de': u'Kurze Segmente löschen'})
		self.keyboardShortcut = None # With Cmd+Shift

	def filter(self, thisLayer, inEditView, customParameters):
		maxLength = 1.0
		passes = 2
		
		try:
			maxLength = float(customParameters["maxlength"])
		except:
			try:
				maxLength = float(customParameters["maxLength"])
			except:
				pass

		try:
			passes = float(customParameters["passes"])
		except:
			try:
				passes = float(customParameters["passes"])
			except:
				pass
		
		for x in range(passes):
			for thisPath in thisLayer.paths:
				for i in range(len(thisPath.nodes))[::-1]:
					thisNode = thisPath.nodes[i]
					nextNode = thisNode.nextNode
					if nextNode.type != OFFCURVE and thisNode.type != OFFCURVE:
						xDistance = thisNode.x-nextNode.x
						yDistance = thisNode.y-nextNode.y
						if abs(xDistance) < maxLength and abs(yDistance) < maxLength:
							if (not inEditView) or (nextNode in thisLayer.selection or thisNode in thisLayer.selection) or (not thisLayer.selection):
								thisPath.removeNodeCheckKeepShape_( thisNode )
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	