from math import sin, cos, radians

layer_in = QgsProject.instance().mapLayersByName('zagadka')[0] #warstwa z punktami
layer_out = QgsProject.instance().mapLayersByName('BBB')[0] #warstwa z liniami
layer_out.dataProvider().addAttributes([QgsField("azim", QVariant.Int, "int", 100), QgsField("name", QVariant.String, "string", 100)])
layer_out.updateFields()
c = 100 #promien wewnetrzny
d = 75 #promien zewnetrzny
theta_min = 0 #kąt początkowy
theta_max = 360 #kąt końcowy
theta_step = 45 #krok (w stopniach)
features_in = layer_in.getFeatures()
features_out = layer_out.getFeatures()
for f in features_in:
    geom = f.geometry()
    nameOfCenter = f['ID'] #nazwa pola w warstwie punktowej
    print(nameOfCenter)
    type(nameOfCenter)
    x = geom.asPoint().x()
    y = geom.asPoint().y()
    layer_out.startEditing()
    for theta in range(theta_min, theta_max, theta_step):
        x1 = x + c * cos(radians(theta))
        y1 = y + c * sin(radians(theta))
        x2 = x + (c+d) * cos(radians(theta))
        y2 = y + (c+d) * sin(radians(theta))
        seg = QgsFeature(layer_out.fields())
        seg.setGeometry(QgsGeometry.fromPolyline([QgsPoint(x1, y1), QgsPoint(x2, y2)]))
        azimuth = round(QgsPoint(x1, y1).azimuth(QgsPoint(x2, y2)))
        if azimuth < 0:
            azimuth = 360 + azimuth
        seg["azim"] = azimuth
        seg["name"] = nameOfCenter
        layer_out.addFeatures([seg])
    layer_out.commitChanges()