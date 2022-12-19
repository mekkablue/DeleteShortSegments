# encoding: utf-8

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

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

def bezier(p1, p2, p3, p4, t):
	"""
	Returns coordinates for t (=0.0...1.0) on curve segment.
	x1,y1 and x4,y4: coordinates of on-curve nodes
	x2,y2 and x3,y3: coordinates of BCPs
	"""
	x1, y1 = p1.x, p1.y
	x2, y2 = p2.x, p2.y
	x3, y3 = p3.x, p3.y
	x4, y4 = p4.x, p4.y
	
	x = x1*(1-t)**3 + x2*3*t*(1-t)**2 + x3*3*t**2*(1-t) + x4*t**3
	y = y1*(1-t)**3 + y2*3*t*(1-t)**2 + y3*3*t**2*(1-t) + y4*t**3

	return x, y

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

	@objc.python_method
	def segmentLength(self, segment, precision=25):
		if len(segment) == 2:
			p0,p1 = segment
			return distance(p0,p1) # this is Glyphs convenience method
		elif len(segment) == 4:
			p0,p1,p2,p3 = segment
			previousPoint = p0
			length = 0
			for i in range(precision):
				t = (i+1.0)/precision
				currentPoint = bezier( p0,p1,p2,p3, t )
				length += distance(previousPoint,currentPoint)
				previousPoint = currentPoint
			return length
			
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
							if self.segmentLength((thisNode.position, nextNode.position)) < maxLength:
								if (not inEditView) or (nextNode in thisLayer.selection or thisNode in thisLayer.selection) or (not thisLayer.selection):
									thisPath.removeNodeCheckKeepShape_( thisNode )
									hasRemovedSegments = True # OK to start another pass
						elif thisNode.type == OFFCURVE and nextNode.type == OFFCURVE and nextNode.nextNode.type == CURVE:
							if self.segmentLength((thisNode.prevNode.position, thisNode.position, nextNode.position, nextNode.nextNode.position)) < maxLength:
								if (not inEditView) or (nextNode in thisLayer.selection or thisNode in thisLayer.selection) or (not thisLayer.selection):
									del thisPath.nodes[i:i+2]
									hasRemovedSegments = True # OK to start another pass
									
		thisLayer.cleanUpPaths()
	
	@objc.python_method
	def generateCustomParameter( self ):
		return "%s; maxLength:%.1f; passes:%i" % (
			self.__class__.__name__,
			float(Glyphs.defaults['com.mekkablue.DeleteShortSegments.maxLength']),
			int(Glyphs.defaults['com.mekkablue.DeleteShortSegments.passes']),
		)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
