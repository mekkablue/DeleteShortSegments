# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class DeleteShortSegments(FilterWithDialog):
	
	# Definitions of IBOutlets
	dialog = objc.IBOutlet()
	maxLengthField = objc.IBOutlet()
	passesField = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Delete Short Segments',
			'de': 'Kurze Segmente löschen',
			'es': 'Borrar segmentos cortos',
			'fr': 'Supprimer segments courts',
		})

		self.actionButtonLabel = Glyphs.localize({
			'en': u'Delete',
			'de': u'Löschen',
			'es': u'Borrar',
			'fr': u'Supprimer',
		})

		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)
	
	# On dialog show
	@objc.python_method
	def start(self):
		Glyphs.registerDefault( "com.mekkablue.DeleteShortSegments.maxLength", 1.0 )
		Glyphs.registerDefault( "com.mekkablue.DeleteShortSegments.passes", 2 )
				
		# Set value of fields:
		self.maxLengthField.setStringValue_( Glyphs.defaults['com.mekkablue.DeleteShortSegments.maxLength'] )
		self.passesField.setStringValue_( Glyphs.defaults['com.mekkablue.DeleteShortSegments.passes'] )
		
		# Set focus to 1st field:
		self.maxLengthField.becomeFirstResponder()
		
	# Actions triggered by UI:
	@objc.IBAction
	def setMaxLength_( self, sender ):
		Glyphs.defaults['com.mekkablue.DeleteShortSegments.maxLength'] = sender.floatValue()
		self.update()
	
	@objc.IBAction
	def setPasses_( self, sender ):
		Glyphs.defaults['com.mekkablue.DeleteShortSegments.passes'] = sender.intValue()
		self.update()
	
	# Actual filter
	@objc.python_method
	def filter(self, thisLayer, inEditView, customParameters):
		# Called on font export:
		if not inEditView:
			if 'maxLength' in customParameters:
				maxLength = float(customParameters['maxLength'])
			elif 'maxlength' in customParameters: # potential misspelling (lowercase l)
				maxLength = float(customParameters['maxlength'])
			else:
				maxLength = 1.0 # fallback
				
			if 'passes' in customParameters:
				passes = int(customParameters['passes'])
			else:
				passes = 2 # fallback
		
		# Called by the user in the UI:
		else:
			maxLength = float(Glyphs.defaults['com.mekkablue.DeleteShortSegments.maxLength'])
			passes = int(Glyphs.defaults['com.mekkablue.DeleteShortSegments.passes'])
		
		# safeguards:
		passes = max( 1, passes )
		maxLength = max( 0.1, maxLength )
		
		hasRemovedSegments = True
		for x in range(passes):
			if hasRemovedSegments: 
				# if no segments were removed in pass 2, do nothing in passes 3+
				# (faster if user enters too many passes)
				hasRemovedSegments = False
				for thisPath in thisLayer.paths:
					for i in range(len(thisPath.nodes))[::-1]: # go backwards through nodes, so i remains correct
						thisNode = thisPath.nodes[i]
						nextNode = thisNode.nextNode
						if nextNode.type != OFFCURVE and thisNode.type != OFFCURVE:
							xDistance = thisNode.x-nextNode.x
							yDistance = thisNode.y-nextNode.y
							distance = ( xDistance**2 + yDistance**2 ) ** 0.5 # Hypotenuse
							if distance < maxLength:
								if (not inEditView) or (nextNode in thisLayer.selection or thisNode in thisLayer.selection) or (not thisLayer.selection):
									thisPath.removeNodeCheckKeepShape_( thisNode )
									hasRemovedSegments = True # OK to start another pass
	
	@objc.python_method
	def generateCustomParameter( self ):
		return "%s; maxLength:%.1f; passes:%i" % (
			self.__class__.__name__,
			Glyphs.defaults['com.mekkablue.DeleteShortSegments.maxLength'],
			Glyphs.defaults['com.mekkablue.DeleteShortSegments.passes'],
		)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
