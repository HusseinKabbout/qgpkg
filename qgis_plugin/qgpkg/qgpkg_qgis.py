# DO NOT EDIT THIS FILE in the QGIS plugin directory.
# Edit the original library file in the qgpkg directory and
# execute `make` to update the QGIS plugin files.
from __future__ import print_function
import sys
import os
import sqlite3
import tempfile
import mimetypes
import logging
from PyQt4.QtCore import QFileInfo

from xml.etree import ElementTree as ET

from qgpkg import QGpkg

logger = logging.getLogger('qgpkg_qgis')

# Debug code for Pycharm
#sys.path.append('/home/joana/Downloads/pycharm-2016.3.3/debug-eggs/pycharm-debug.egg')
#import pydevd

#pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)

class QGpkg_qgis(QGpkg):
    """Read and write QGIS mapping information in a GeoPackage database file, using this spec:
    https://github.com/pka/qgpkg/blob/master/qgis_geopackage_extension.md
    """

    def write(self, project_path):
        ''' Store QGIS project '''
        xmltree = self.read_project(project_path)
        # If something is messed up with the file, the Method will stop
        if not xmltree:
            self.log(logging.ERROR, u"Couldn't read project (wrong file format)")
            return

        root = xmltree.getroot()
        projectlayers = root.find("projectlayers")

        # Search for layersources
        sources = []
        for layer in projectlayers:
            layer_path = self.make_path_absolute(layer.find(
                "datasource").text.split("|")[0], project_path)
            if layer_path not in sources:
                self.log(logging.DEBUG, u"Found datasource: %s" % layer_path)
                sources.append(layer_path)

        # If there are more than just one different datasource check from where
        # they are from
        gpkg_found = False
        if len(sources) >= 1:
            for path in sources:
                if self.database_connect(path):
                    if self.check_gpkg(path) and not gpkg_found:
                        gpkg_found = True
                        gpkg_path = path
                    elif self.check_gpkg(path) and gpkg_found:
                        # If a project has layer from more than just one
                        #  GeoPackage it can't be written
                        self.log(logging.ERROR, u"The project uses layers "
                                                "from different GeoPackage databases.")
                        return
            if gpkg_found and len(sources) > 1:
                self.log(
                    logging.WARNING,
                    u"Some layers aren't in the GeoPackage. It can't be "
                    "garanteed that all layers will be shown properly.")

        if not gpkg_found:
            self.log(logging.ERROR, u"There is no GeoPackage layer "
                                    "in the project.")
            return

        # Check for images in the composer of the project
        composer_list = root.findall("Composer")
        images = []
        for composer in composer_list:
            for comp in composer:
                img = comp.find("ComposerPicture").attrib['file']
                if img not in images:
                    self.log(logging.DEBUG, u"Image found: %s" % img)
                    images.append(img)

        # Write data in database
        project_name = os.path.basename(project_path)
        project_xml = ET.tostring(root)

        self.database_connect(gpkg_path)

        # Create tables
        self.c.execute('CREATE TABLE IF NOT EXISTS qgis_projects (name TEXT PRIMARY KEY, xml TEXT NOT NULL)')
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS qgis_resources
             (name TEXT PRIMARY KEY, mime_type TEXT NOT NULL, content BLOB NOT NULL)""")
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS gpkg_extensions (table_name TEXT,column_name TEXT,extension_name TEXT NOT NULL,definition TEXT NOT NULL,scope TEXT NOT NULL,CONSTRAINT ge_tce UNIQUE (table_name, column_name, extension_name))')
        extension_record = (None, None, 'qgis',
                            'http://github.com/pka/qgpkg/blob/master/'
                            'qgis_geopackage_extension.md',
                            'read-write')
        self.c.execute('SELECT count(1) FROM gpkg_extensions WHERE extension_name=?', (extension_record[2],))
        if self.c.fetchone()[0] == 0:
            self.c.execute(
                'INSERT INTO gpkg_extensions VALUES (?,?,?,?,?)', extension_record)

        self.c.execute('SELECT count(1) FROM qgis_projects WHERE name=?', (project_name,))
        if self.c.fetchone()[0] == 0:
            self.c.execute('INSERT INTO qgis_projects VALUES (?,?)', (project_name, project_xml))
            self.log(logging.DEBUG, u"Project %s saved." % project_name)
        else:
            # Overwrite existing project (DELETE gives locking problems)
            self.c.execute('UPDATE qgis_projects SET xml=? WHERE name=?',
                           (project_xml, project_name))
            self.log(logging.INFO, u"Project overwritten.")

        if images:
            for image in images:
                img = self.make_path_absolute(image, project_path)
                with open(img, 'rb') as input_file:
                    blob = input_file.read()
                    mime_type = mimetypes.MimeTypes().guess_type(image)[0]
                    self.c.execute('SELECT count(1) FROM qgis_resources WHERE name=?', (image,))
                    if self.c.fetchone()[0] == 0:
                        self.conn.execute(
                            """INSERT INTO qgis_resources \
                            VALUES(?, ?, ?)""", (image, mime_type, sqlite3.Binary(blob)))
                    # TODO: forced overwrite
                    self.log(logging.DEBUG, u"Image %s was saved" % image)
        self.conn.commit()

    def read(self, gpkg_path):
        ''' Read QGIS project from GeoPackage '''
        # Check if it's a GeoPackage Database
        self.database_connect(gpkg_path)
        if not self.check_gpkg(gpkg_path):
            self.log(logging.ERROR, u"No valid GeoPackage selected.")
            return

        # Read xml from the project in the Database
        try:
            self.c.execute('SELECT name, xml FROM qgis_projects')
        except sqlite3.OperationalError:
            self.log(logging.ERROR, u"There is no Project file "
                                    "in the database.")
            return
        file_name, xml = self.c.fetchone()
        try:
            xml_tree = ET.ElementTree()
            root = ET.fromstring(xml)
        except:
            self.log(logging.ERROR, u"The xml code is corrupted.")
            return
        self.log(logging.DEBUG, u"Xml successfully read.")
        xml_tree._setroot(root)
        projectlayers = root.find("projectlayers")

        # Layerpath in xml adjusted
        tmp_folder = tempfile.mkdtemp()
        project_path = os.path.join(tmp_folder, file_name)
        for layer in projectlayers:
            layer_element = layer.find("datasource")
            layer_info = layer_element.text.split("|")
            layer_path = self.make_path_absolute(gpkg_path, layer_info[0])
            if layer_path.endswith('.gpkg'):
                if len(layer_info) >= 2:
                    for i in range(len(layer_info)):
                        if i == 0:
                            layer_element.text = layer_path
                        else:
                            layer_element.text += "|" + layer_info[i]
                elif len(layer_info) == 1:
                    layer_element.text = layer_path
                self.log(logging.DEBUG,
                         u"Layerpath from layer %s was adjusted." %
                         layer.find("layername").text)

        # Check if an image is available
        composer_list = root.findall("Composer")
        images = []
        for composer in composer_list:
            for comp in composer:
                composer_picture = comp.find("ComposerPicture")
                img = self.make_path_absolute(
                    composer_picture.attrib['file'], project_path)
                # If yes, the path will be adjusted
                composer_picture.set('file', './' + os.path.basename(img))
                self.log(logging.DEBUG,
                         u"External image %s found." % os.path.basename(img))
                images.append(img)

        # and the image will be saved in the same folder as the project
        if images:
            self.c.execute("SELECT name, mime_type, content FROM qgis_resources")
            images = self.c.fetchall()
            for img in images:
                img_name, mime_type, blob = img
                img_path = os.path.join(tmp_folder, img_name)
                with open(img_path, 'wb') as file:
                    file.write(blob)
                self.log(logging.DEBUG, u"Image saved: %s" % img_name)

        # Project is saved and started
        xml_tree.write(project_path)
        self.log(logging.DEBUG, u"Temporary project written: %s" % project_path)
        return project_path

    def read_project(self, path):
        ''' Check if it's a file and give ElementTree object back '''
        if not os.path.isfile(path):
            return False

        return ET.parse(path)