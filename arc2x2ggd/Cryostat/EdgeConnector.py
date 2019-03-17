#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class EdgeConnectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dx=None, dy=None, dz=None, corner1=None, corner2=None, material=None, **kwds ):
        self.dx, self.dy, self.dz = ( dx, dy, dz )
        self.corner1 = corner1
        self.corner2 = corner2
        self.material = material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct the middle of the plate
        mid_shape = geom.shapes.Box( self.name+'MidComp', dx=self.dx, dy=self.dy, dz=self.dz)
        # construct corners
        corner1dx = 0.5*( self.corner1*self.corner1*2 )**(0.5)
        corner2dx = 0.5*( self.corner2*self.corner2*2 )**(0.5)
        corner1_shape = geom.shapes.Box( self.name+'Corner1Comp', dx=self.corner1, dy=self.corner1, dz=self.dz)
        corner2_shape = geom.shapes.Box( self.name+'Corner2Comp', dx=self.corner2, dy=self.corner2, dz=self.dz)
        corner3_shape = geom.shapes.Box( self.name+'Corner3Comp', dx=self.corner2, dy=self.dy/2., dz=self.dz)

        # first do the far edge
        relpos1 = geom.structure.Position(self.name+'Corner1Rel_pos', Q('0m'), mid_shape.dy, Q('0m'))
        relrot = geom.structure.Rotation(self.name+'CornerRel_rot', Q('0deg'), Q('0deg'), Q('45deg'))
        # union
        boolean_shape1 = geom.shapes.Boolean( self.name+'Union1', type='union', first=mid_shape, second=corner1_shape, pos=relpos1, rot=relrot)

        # now do the other edge
        relpos2 = geom.structure.Position(self.name+'Corner2Rel_pos', Q('0m'), -1*mid_shape.dy, Q('0m'))
        boolean_shape2 = geom.shapes.Boolean( self.name+'Union2', type='union', first=boolean_shape1, second=corner2_shape, pos=relpos2, rot=relrot)

        relpos3 = geom.structure.Position(self.name+'Corner3Rel_pos', -1*corner3_shape.dy, -1*mid_shape.dy, Q('0m'))
        boolean_shape3 = geom.shapes.Boolean( self.name+'Union3', type='union', first=boolean_shape2, second=corner3_shape, pos=relpos3)

        boolean_lv = geom.structure.Volume('vol'+boolean_shape3.name, material=self.material, shape=boolean_shape3)
        self.add_volume( boolean_lv )
