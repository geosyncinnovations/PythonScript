from arcgis.gis import GIS
import arcpy
import os
import xml.dom.minidom as DOM
######################
wrkspc = 'D:/Work/ArcMap/ARCGIS_projects/newmap/'
prj_name = 'newmap.aprx'
sd_name = 'PublishMap'
map_name = 'PublishMap'
fs_name = 'PublishMapTest'
folder = 'vinay'
portal = arcpy.GetActivePortalURL() # Can also reference a local portal
user = 'sriramakrishna@Geo'
password = '@Geosync#123'
#connection portal
arcpy.SignInToPortal(portal, user, password)
gis = GIS(portal, user, password)
#Set output file names
aprx = arcpy.mp.ArcGISProject(wrkspc + prj_name)
m = aprx.listMaps(map_name)[0]
print(m)
sharing_draft = m.getWebLayerSharingDraft("HOSTING_SERVER", "FEATURE", sd_name)
sharing_draft.summary = "Test Service"
sharing_draft.tags = "GeoSync"
sharing_draft.description = "Publishing service using python"
print('sharing draft')
#Create Service Definition Draft file
sharing_draft.exportToSDDraft(wrkspc + sd_name +'.sddraft')
##arcpy.mp.CreateWebLayerSDDraft(m, wrkspc + service +'.sddraft', fs_name , 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS', folder, True)
searchItem = gis.content.search("{} AND owner:{}".format(fs_name, user), item_type="Service Definition")
#print(len(searchItem))
#Updating Service Definition Draft file
if len(searchItem) > 0:
    print("Replacing existing service")
    newType = 'esriServiceDefinitionType_Replacement'
    xml = wrkspc + sd_name +'.sddraft'
    doc = DOM.parse(xml)
    descriptions = doc.getElementsByTagName('Type')
    for desc in descriptions:
           if desc.parentNode.tagName == 'SVCManifest':
               if desc.hasChildNodes():
                   desc.firstChild.data = newType
    outXml = xml
    f = open(outXml, 'w')
    doc.writexml( f )
    f.close()
else:
  print("Creating new service")
#verifying file already exists
sd_file = wrkspc +  sd_name +'.sd'
isFile = os.path.isfile(sd_file)
if isFile:
   os.remove(sd_file)
#Execute StageService
arcpy.StageService_server(wrkspc + sd_name +'.sddraft', sd_file)
print("Uploading Service Definition...")
arcpy.UploadServiceDefinition_server(sd_file, 'My Hosted Services',fs_name,'', 'EXISTING', 'vinay', '', 'OVERRIDE_DEFINITION' )
print("Successfully Uploaded service.")
