import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

mysystem = chrono.ChSystemNSC()

# Create a fixed rigid body

mbody1 = chrono.ChBody()
mbody1.SetBodyFixed(True)
mbody1.SetPos(chrono.ChVectorD(0, 0, -0.2))
mysystem.Add(mbody1)

mboxasset = chrono.ChBoxShape()
mboxasset.GetBoxGeometry().Size = chrono.ChVectorD(0.2, 0.5, 0.1)
mbody1.AddAsset(mboxasset)


# Create a swinging rigid body

mbody2 = chrono.ChBody()
mbody2.SetBodyFixed(False)
mysystem.Add(mbody2)

mboxasset = chrono.ChBoxShape()
mboxasset.GetBoxGeometry().Size = chrono.ChVectorD(0.2, 0.5, 0.1)
mbody2.AddAsset(mboxasset)

mboxtexture = chrono.ChTexture()
mbody2.GetAssets().push_back(mboxtexture)


# Create a revolute constraint

mlink = chrono.ChLinkRevolute()

# the coordinate system of the constraint reference in abs. space:
mframe = chrono.ChFrameD(chrono.ChVectorD(0.1, 0.5, 0))

# initialize the constraint telling which part must be connected, and where:
mlink.Initialize(mbody1, mbody2, mframe)

mysystem.Add(mlink)

myapplication = chronoirr.ChIrrApp(
    mysystem, "PyChrono example", chronoirr.dimension2du(1024, 768)
)

myapplication.AddTypicalSky()
myapplication.AddTypicalLogo()
myapplication.AddTypicalCamera(chronoirr.vector3df(0.6, 0.6, 0.8))
myapplication.AddTypicalLights()

myapplication.AssetBindAll()
myapplication.AssetUpdateAll()

myapplication.SetTimestep(0.005)


while myapplication.GetDevice().run():
    myapplication.BeginScene()
    myapplication.DrawAll()
    myapplication.DoStep()
    myapplication.EndScene()

