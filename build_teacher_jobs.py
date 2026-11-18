import os
import uuid
import shutil

process_dir = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\TP2_BI_VENTES\process"
sources_dir = r"C:/Users/pc/OneDrive/Bureau/ETL/Etude de cas DW Fichiers Sources/Etude de cas DW"

def make_id():
    return "_" + uuid.uuid4().hex[:22]

def create_properties(job_name):
    prop_path = os.path.join(process_dir, f"{job_name}_0.1.properties")
    prop_xmi_id = make_id()
    prop_id = make_id()
    item_xmi_id = make_id()
    state_xmi_id = make_id()
    add_ids = [make_id() for _ in range(6)]
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:TalendProperties="http://www.talend.org/properties">
  <TalendProperties:Property xmi:id="{prop_xmi_id}" id="{prop_id}" label="{job_name}" version="0.1" statusCode="" item="{item_xmi_id}" displayName="{job_name}">
    <author href="../talend.project#_cHnxMeKvEfGcW-VHAjGimQ"/>
    <additionalProperties xmi:id="{add_ids[0]}" key="created_product_fullname" value="Talaxie Open Studio for Data Integration"/>
    <additionalProperties xmi:id="{add_ids[1]}" key="created_product_version" value="8.9.0.20261020-1837-SNAPSHOT"/>
    <additionalProperties xmi:id="{add_ids[2]}" key="created_date" value="2026-11-18T09:00:00.000+0000"/>
    <additionalProperties xmi:id="{add_ids[3]}" key="modified_product_fullname" value="Talaxie Open Studio for Data Integration"/>
    <additionalProperties xmi:id="{add_ids[4]}" key="modified_product_version" value="8.9.0.20261018-1926-SNAPSHOT"/>
    <additionalProperties xmi:id="{add_ids[5]}" key="modified_date" value="2026-11-18T09:30:00.000+0100"/>
  </TalendProperties:Property>
  <TalendProperties:ItemState xmi:id="{state_xmi_id}" path=""/>
  <TalendProperties:ProcessItem xmi:id="{item_xmi_id}" property="{prop_xmi_id}" state="{state_xmi_id}">
    <process href="{job_name}_0.1.item#/"/>
  </TalendProperties:ProcessItem>
</xmi:XMI>"""
    with open(prop_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

header = """<?xml version="1.0" encoding="UTF-8"?>
<talendfile:ProcessType xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:TalendMapper="http://www.talend.org/mapper" xmlns:talendfile="platform:/resource/org.talend.model/model/TalendFile.xsd" defaultContext="Default" jobType="Standard">
  <context confirmationNeeded="false" hide="false" name="Default"/>
  <parameters>
    <elementParameter field="CLOSED_LIST" name="LOG4J_RUN_LEVEL" value="Info" show="false"/>
    <elementParameter field="TEXT" name="SCREEN_OFFSET_X" value="0" show="false"/>
    <elementParameter field="TEXT" name="SCREEN_OFFSET_Y" value="0" show="false"/>
    <elementParameter field="TEXT" name="REPOSITORY_CONNECTION_ID" value="" show="false"/>
    <elementParameter field="CHECK" name="IMPLICITCONTEXT_USE_PROJECT_SETTINGS" value="true" show="false"/>
    <elementParameter field="CHECK" name="STATANDLOG_USE_PROJECT_SETTINGS" value="true" show="false"/>
    <elementParameter field="CHECK" name="MULTI_THREAD_EXECATION" value="false"/>
    <elementParameter field="CHECK" name="IMPLICIT_TCONTEXTLOAD" value="false"/>
    <routinesParameter id="_ChsJ8M9VEfG71M3VwE5zwA" name="DataOperation"/>
    <routinesParameter id="_CsSQYM9VEfG71M3VwE5zwA" name="Mathematical"/>
    <routinesParameter id="_CtfKQM9VEfG71M3VwE5zwA" name="Numeric"/>
    <routinesParameter id="_CuhFAM9VEfG71M3VwE5zwA" name="Relational"/>
    <routinesParameter id="_CvEeoM9VEfG71M3VwE5zwA" name="StringHandling"/>
    <routinesParameter id="_CvOPoM9VEfG71M3VwE5zwA" name="TalendDataGenerator"/>
    <routinesParameter id="_CvWygM9VEfG71M3VwE5zwA" name="TalendDate"/>
    <routinesParameter id="_Cvi_wM9VEfG71M3VwE5zwA" name="TalendStringUtil"/>
    <routinesParameter id="_CveuUM9VEfG71M3VwE5zwA" name="TalendString"/>
  </parameters>
"""

# ==========================================
# 1. BUILD DIM_CLIENT
# ==========================================
def build_dim_client(job_name):
    content = header + f"""
  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="64" posY="96">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/clients_base_50.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Codes clients Excel"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_1">
      <column comment="" key="false" length="50" name="client_id" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="224" posY="96">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_1" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Code client"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="cle_base_clients">
      <column comment="" key="false" length="50" name="code_client" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="cle_base_clients">
        <mapperTableEntries name="code_client" expression="cles_base_clients.client_id" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="cles_base_clients" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="client_id" type="id_String" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="64" posY="224">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_2" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/ventes_synthese.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Clients dans ventes"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_2">
      <column comment="" key="false" length="50" name="id_client_source" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="224" posY="224">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_2" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="ID client vente"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="cle_ventes">
      <column comment="" key="false" length="50" name="code_client" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="cle_ventes">
        <mapperTableEntries name="code_client" expression="cles_ventes.id_client_source" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="cles_ventes" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id_client_source" type="id_String" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tUnite" componentVersion="0.101" offsetLabelX="0" offsetLabelY="0" posX="384" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tUnite_1" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Rassembler codes"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tUnite_1">
      <column comment="" key="false" length="50" name="code_client" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tUniqRow" componentVersion="0.101" offsetLabelX="0" offsetLabelY="0" posX="512" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tUniqRow_1" show="false"/>
    <elementParameter field="TABLE" name="UNIQUE_KEY">
      <elementValue elementRef="SCHEMA_COLUMN" value="code_client"/>
      <elementValue elementRef="KEY_ATTRIBUTE" value="true"/>
      <elementValue elementRef="CASE_SENSITIVE" value="false"/>
    </elementParameter>
    <elementParameter field="TEXT" name="LABEL" value="Codes uniques"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tUniqRow_1">
      <column comment="" key="false" length="50" name="code_client" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
    <metadata connector="UNIQUE" name="UNIQUE">
      <column comment="" key="false" length="50" name="code_client" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="448" posY="320">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_3" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/clients_base_50.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Base clients"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_3">
      <column comment="" key="true" length="50" name="client_id" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="nom" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="prenom" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="ville" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="email" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="segment_marketing" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="date_inscription" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tFileInputDelimited" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="480" posY="448">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputDelimited_1" show="false"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/clients_online_50.csv&quot;"/>
    <elementParameter field="CHECK" name="CSV_OPTION" value="false"/>
    <elementParameter field="TEXT" name="ROWSEPARATOR" value="&quot;\\n&quot;"/>
    <elementParameter field="TEXT" name="FIELDSEPARATOR" value="&quot;,&quot;"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Clients web CSV"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputDelimited_1">
      <column comment="" key="true" length="50" name="client_code" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="full_name" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="email" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="city" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="first_purchase_date" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tFileInputXML" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="480" posY="576">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputXML_1" show="false"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/clients_fidelite_50.xml&quot;"/>
    <elementParameter field="TEXT" name="LOOP_QUERY" value="&quot;/clients/client&quot;"/>
    <elementParameter field="TABLE" name="MAPPING">
      <elementValue elementRef="SCHEMA_COLUMN" value="id"/>
      <elementValue elementRef="QUERY" value="&quot;id&quot;"/>
      <elementValue elementRef="NODECHECK" value="false"/>
      <elementValue elementRef="SCHEMA_COLUMN" value="points"/>
      <elementValue elementRef="QUERY" value="&quot;points&quot;"/>
      <elementValue elementRef="NODECHECK" value="false"/>
      <elementValue elementRef="SCHEMA_COLUMN" value="carte"/>
      <elementValue elementRef="QUERY" value="&quot;carte&quot;"/>
      <elementValue elementRef="NODECHECK" value="false"/>
    </elementParameter>
    <elementParameter field="CLOSED_LIST" name="GENERATION_MODE" value="Dom4j"/>
    <elementParameter field="CHECK" name="IGNORE_NS" value="false"/>
    <elementParameter field="CHECK" name="IGNORE_DTD" value="false"/>
    <elementParameter field="ENCODING_TYPE" name="ENCODING" value="&quot;UTF-8&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="Fidélité XML"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputXML_1">
      <column comment="" key="true" length="50" name="id" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="points" nullable="true" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="carte" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="672" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_3" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Relier clients"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="sortie_client">
      <column comment="" key="true" length="20" name="code_client" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="nom" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="prenom" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="200" name="nom_complet" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="ville" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="email" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="segment_marketing" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="points_fidelite" nullable="true" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="type_carte" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="sortie_client">
        <mapperTableEntries name="code_client" expression="identifiants.code_client" type="id_String"/>
        <mapperTableEntries name="nom" expression="base_clients.nom != null ? base_clients.nom : &quot;Inconnu&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="prenom" expression="base_clients.prenom != null ? base_clients.prenom : &quot;Inconnu&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="nom_complet" expression="(base_clients.nom != null ? base_clients.nom : &quot;&quot;) + &quot; &quot; + (base_clients.prenom != null ? base_clients.prenom : &quot;&quot;)" type="id_String" nullable="true"/>
        <mapperTableEntries name="ville" expression="base_clients.ville != null ? base_clients.ville : (clients_web.city != null ? clients_web.city : &quot;Maroc&quot;)" type="id_String" nullable="true"/>
        <mapperTableEntries name="email" expression="base_clients.email != null ? base_clients.email : clients_web.email" type="id_String" nullable="true"/>
        <mapperTableEntries name="segment_marketing" expression="base_clients.segment_marketing != null ? base_clients.segment_marketing : &quot;Standard&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="points_fidelite" expression="fidelite.points != null ? fidelite.points : 0" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="type_carte" expression="fidelite.carte != null ? fidelite.carte : &quot;Standard&quot;" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="identifiants" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_client" type="id_String" nullable="true"/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="base_clients" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="client_id" expression="identifiants.code_client" type="id_String" operator="="/>
        <mapperTableEntries name="nom" type="id_String" nullable="true"/>
        <mapperTableEntries name="prenom" type="id_String" nullable="true"/>
        <mapperTableEntries name="ville" type="id_String" nullable="true"/>
        <mapperTableEntries name="email" type="id_String" nullable="true"/>
        <mapperTableEntries name="segment_marketing" type="id_String" nullable="true"/>
        <mapperTableEntries name="date_inscription" type="id_String" nullable="true"/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="clients_web" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="client_code" expression="identifiants.code_client" type="id_String" operator="="/>
        <mapperTableEntries name="full_name" type="id_String" nullable="true"/>
        <mapperTableEntries name="email" type="id_String" nullable="true"/>
        <mapperTableEntries name="city" type="id_String" nullable="true"/>
        <mapperTableEntries name="first_purchase_date" type="id_String" nullable="true"/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="fidelite" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id" expression="identifiants.code_client" type="id_String" operator="="/>
        <mapperTableEntries name="points" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="carte" type="id_String" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tMysqlOutput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="896" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tDBOutput_1" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;dim_client&quot;"/>
    <elementParameter field="CLOSED_LIST" name="TABLE_ACTION" value="NONE"/>
    <elementParameter field="CLOSED_LIST" name="DATA_ACTION" value="INSERT_OR_UPDATE"/>
    <elementParameter field="TEXT" name="PROPERTIES" value="&quot;noDatetimeStringSync=true&amp;enabledTLSProtocols=TLSv1.2,TLSv1.1,TLSv1&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="dim_client"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tDBOutput_1">
      <column comment="" key="true" length="20" name="code_client" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="nom" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="prenom" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="200" name="nom_complet" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="ville" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="email" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="segment_marketing" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="points_fidelite" nullable="true" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="type_carte" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <connection connectorName="FLOW" label="cles_base_clients" lineStyle="0" metaname="tFileInputExcel_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_1" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="cles_base_clients" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="cle_base_clients" lineStyle="10" mergeOrder="1" metaname="cle_base_clients" offsetLabelX="0" offsetLabelY="0" source="tMap_1" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="cle_base_clients" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="cles_ventes" lineStyle="0" metaname="tFileInputExcel_2" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_2" target="tMap_2">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="cles_ventes" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="cle_ventes" lineStyle="10" mergeOrder="2" metaname="cle_ventes" offsetLabelX="0" offsetLabelY="0" source="tMap_2" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="cle_ventes" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="ensemble" lineStyle="0" metaname="tUnite_1" offsetLabelX="0" offsetLabelY="0" source="tUnite_1" target="tUniqRow_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="ensemble" show="false"/>
  </connection>
  <connection connectorName="UNIQUE" label="identifiants" lineStyle="0" metaname="UNIQUE" offsetLabelX="0" offsetLabelY="0" source="tUniqRow_1" target="tMap_3">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="identifiants" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="base_clients" lineStyle="8" metaname="tFileInputExcel_3" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_3" target="tMap_3">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="base_clients" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="clients_web" lineStyle="8" metaname="tFileInputDelimited_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputDelimited_1" target="tMap_3">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="clients_web" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="fidelite" lineStyle="8" metaname="tFileInputXML_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputXML_1" target="tMap_3">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="fidelite" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="sortie_client" lineStyle="0" metaname="sortie_client" offsetLabelX="0" offsetLabelY="0" source="tMap_3" target="tDBOutput_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="sortie_client" show="false"/>
  </connection>

  <subjob>
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_TITLE_COLOR" value="92;131;150" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_COLOR" value="207;226;236"/>
  </subjob>
  <subjob>
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_2" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_TITLE_COLOR" value="92;131;150" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_COLOR" value="207;226;236"/>
  </subjob>
</talendfile:ProcessType>
"""
    with open(os.path.join(process_dir, f"{job_name}_0.1.item"), "w", encoding="utf-8") as f:
        f.write(content)
    create_properties(job_name)
    print(f"Built {job_name}")

# ==========================================
# 2. BUILD DIM_PRODUIT
# ==========================================
def build_dim_produit(job_name):
    content = header + f"""
  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="64" posY="96">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/produits_catalogue.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Codes du catalogue"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_1">
      <column comment="" key="false" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="224" posY="96">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_1" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Code produit"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="cle_catalogue">
      <column comment="" key="false" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="cle_catalogue">
        <mapperTableEntries name="code_produit" expression="cles_catalogue.code_produit" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="cles_catalogue" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_produit" type="id_String" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="64" posY="224">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_2" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/ventes_synthese.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Produits dans ventes"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_2">
      <column comment="" key="false" length="50" name="id_produit_source" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="224" posY="224">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_2" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="ID produit vente"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="cle_ventes">
      <column comment="" key="false" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="cle_ventes">
        <mapperTableEntries name="code_produit" expression="cles_ventes.id_produit_source" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="cles_ventes" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id_produit_source" type="id_String" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tUnite" componentVersion="0.101" offsetLabelX="0" offsetLabelY="0" posX="384" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tUnite_1" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Réunir codes"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tUnite_1">
      <column comment="" key="false" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tUniqRow" componentVersion="0.101" offsetLabelX="0" offsetLabelY="0" posX="512" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tUniqRow_1" show="false"/>
    <elementParameter field="TABLE" name="UNIQUE_KEY">
      <elementValue elementRef="SCHEMA_COLUMN" value="code_produit"/>
      <elementValue elementRef="KEY_ATTRIBUTE" value="true"/>
      <elementValue elementRef="CASE_SENSITIVE" value="false"/>
    </elementParameter>
    <elementParameter field="TEXT" name="LABEL" value="Codes uniques"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tUniqRow_1">
      <column comment="" key="false" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
    <metadata connector="UNIQUE" name="UNIQUE">
      <column comment="" key="false" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="448" posY="320">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_3" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/produits_catalogue.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Détails catalogue"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_3">
      <column comment="" key="true" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="nom_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="catégorie" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="sous_catégorie" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="marque" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_achat" nullable="true" pattern="" precision="2" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_vente" nullable="true" pattern="" precision="2" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="statut" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tFileInputDelimited" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="480" posY="448">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputDelimited_1" show="false"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/produits_fournisseurs.csv&quot;"/>
    <elementParameter field="CHECK" name="CSV_OPTION" value="false"/>
    <elementParameter field="TEXT" name="ROWSEPARATOR" value="&quot;\\n&quot;"/>
    <elementParameter field="TEXT" name="FIELDSEPARATOR" value="&quot;,&quot;"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Fournisseurs CSV"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputDelimited_1">
      <column comment="" key="true" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="fournisseur" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="pays_fournisseur" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="delai_livraison_jours" nullable="true" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="coût_transport" nullable="true" pattern="" precision="2" type="id_Double" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="672" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_3" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Lier produits"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="sortie_produit">
      <column comment="" key="true" length="20" name="code_produit" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="nom_produit" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="categorie" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="sous_categorie" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="marque" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_achat" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_vente" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="fournisseur" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="pays_fournisseur" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="delai_livraison_jours" nullable="true" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="cout_transport" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="statut" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="sortie_produit">
        <mapperTableEntries name="code_produit" expression="identifiants.code_produit" type="id_String"/>
        <mapperTableEntries name="nom_produit" expression="catalogue.nom_produit != null ? catalogue.nom_produit : &quot;Produit &quot; + identifiants.code_produit" type="id_String" nullable="true"/>
        <mapperTableEntries name="categorie" expression="catalogue.catégorie != null ? catalogue.catégorie : &quot;Divers&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="sous_categorie" expression="catalogue.sous_catégorie != null ? catalogue.sous_catégorie : &quot;Divers&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="marque" expression="catalogue.marque != null ? catalogue.marque : &quot;Generique&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="prix_achat" expression="catalogue.prix_achat != null ? catalogue.prix_achat : 0.0" type="id_Double" nullable="true"/>
        <mapperTableEntries name="prix_vente" expression="catalogue.prix_vente != null ? catalogue.prix_vente : 0.0" type="id_Double" nullable="true"/>
        <mapperTableEntries name="fournisseur" expression="fournisseurs.fournisseur != null ? fournisseurs.fournisseur : &quot;Interne&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="pays_fournisseur" expression="fournisseurs.pays_fournisseur != null ? fournisseurs.pays_fournisseur : &quot;Maroc&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="delai_livraison_jours" expression="fournisseurs.delai_livraison_jours != null ? fournisseurs.delai_livraison_jours : 0" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="cout_transport" expression="fournisseurs.coût_transport != null ? fournisseurs.coût_transport : 0.0" type="id_Double" nullable="true"/>
        <mapperTableEntries name="statut" expression="catalogue.statut != null ? catalogue.statut : &quot;Actif&quot;" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="identifiants" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_produit" type="id_String" nullable="true"/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="catalogue" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_produit" expression="identifiants.code_produit" type="id_String" operator="="/>
        <mapperTableEntries name="nom_produit" type="id_String" nullable="true"/>
        <mapperTableEntries name="catégorie" type="id_String" nullable="true"/>
        <mapperTableEntries name="sous_catégorie" type="id_String" nullable="true"/>
        <mapperTableEntries name="marque" type="id_String" nullable="true"/>
        <mapperTableEntries name="prix_achat" type="id_Double" nullable="true"/>
        <mapperTableEntries name="prix_vente" type="id_Double" nullable="true"/>
        <mapperTableEntries name="statut" type="id_String" nullable="true"/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="fournisseurs" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_produit" expression="identifiants.code_produit" type="id_String" operator="="/>
        <mapperTableEntries name="fournisseur" type="id_String" nullable="true"/>
        <mapperTableEntries name="pays_fournisseur" type="id_String" nullable="true"/>
        <mapperTableEntries name="delai_livraison_jours" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="coût_transport" type="id_Double" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tMysqlOutput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="896" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tDBOutput_1" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;dim_produit&quot;"/>
    <elementParameter field="CLOSED_LIST" name="TABLE_ACTION" value="NONE"/>
    <elementParameter field="CLOSED_LIST" name="DATA_ACTION" value="INSERT_OR_UPDATE"/>
    <elementParameter field="TEXT" name="PROPERTIES" value="&quot;noDatetimeStringSync=true&amp;enabledTLSProtocols=TLSv1.2,TLSv1.1,TLSv1&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="dim_produit"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tDBOutput_1">
      <column comment="" key="true" length="20" name="code_produit" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="nom_produit" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="categorie" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="sous_categorie" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="marque" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_achat" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_vente" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="fournisseur" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="pays_fournisseur" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="delai_livraison_jours" nullable="true" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="cout_transport" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="statut" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <connection connectorName="FLOW" label="cles_catalogue" lineStyle="0" metaname="tFileInputExcel_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_1" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="cles_catalogue" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="cle_catalogue" lineStyle="10" mergeOrder="1" metaname="cle_catalogue" offsetLabelX="0" offsetLabelY="0" source="tMap_1" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="cle_catalogue" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="cles_ventes" lineStyle="0" metaname="tFileInputExcel_2" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_2" target="tMap_2">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="cles_ventes" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="cle_ventes" lineStyle="10" mergeOrder="2" metaname="cle_ventes" offsetLabelX="0" offsetLabelY="0" source="tMap_2" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="cle_ventes" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="ensemble" lineStyle="0" metaname="tUnite_1" offsetLabelX="0" offsetLabelY="0" source="tUnite_1" target="tUniqRow_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="ensemble" show="false"/>
  </connection>
  <connection connectorName="UNIQUE" label="identifiants" lineStyle="0" metaname="UNIQUE" offsetLabelX="0" offsetLabelY="0" source="tUniqRow_1" target="tMap_3">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="identifiants" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="catalogue" lineStyle="8" metaname="tFileInputExcel_3" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_3" target="tMap_3">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="catalogue" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="fournisseurs" lineStyle="8" metaname="tFileInputDelimited_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputDelimited_1" target="tMap_3">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="fournisseurs" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="sortie_produit" lineStyle="0" metaname="sortie_produit" offsetLabelX="0" offsetLabelY="0" source="tMap_3" target="tDBOutput_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="sortie_produit" show="false"/>
  </connection>

  <subjob>
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_TITLE_COLOR" value="92;131;150" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_COLOR" value="207;226;236"/>
  </subjob>
  <subjob>
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_2" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_TITLE_COLOR" value="92;131;150" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_COLOR" value="207;226;236"/>
  </subjob>
</talendfile:ProcessType>
"""
    with open(os.path.join(process_dir, f"{job_name}_0.1.item"), "w", encoding="utf-8") as f:
        f.write(content)
    create_properties(job_name)
    print(f"Built {job_name}")

# ==========================================
# 3. BUILD DIM_MAGASIN
# ==========================================
def build_dim_magasin(job_name):
    content = header + f"""
  <node componentName="tFileInputDelimited" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="160" posY="128">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputDelimited_1" show="false"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/magasins_localisation (2).csv&quot;"/>
    <elementParameter field="CHECK" name="CSV_OPTION" value="false"/>
    <elementParameter field="TEXT" name="ROWSEPARATOR" value="&quot;\\n&quot;"/>
    <elementParameter field="TEXT" name="FIELDSEPARATOR" value="&quot;,&quot;"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Localisation CSV"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputDelimited_1">
      <column comment="" key="true" length="20" name="code_magasin" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="nom_magasin" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="ville" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="région" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="pays" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="surface_m2" nullable="true" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="type_magasin" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="date_ouverture" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="192" posY="320">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/magasins_ventes (1).xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Gestoin magasins Excel"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_1">
      <column comment="" key="true" length="20" name="code_magasin" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="responsable_magasin" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="nb_employes" nullable="true" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="15" name="chiffre_affaires_annuel" nullable="true" pattern="" precision="2" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="15" name="frais_fonctionnement" nullable="true" pattern="" precision="2" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="statut" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="448" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_1" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Lier magasins"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="sortie_magasin">
      <column comment="" key="true" length="20" name="code_magasin" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="nom_magasin" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="ville" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="region" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="pays" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="surface_m2" nullable="true" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="type_magasin" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="date_ouverture" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" sourceType="DATE" type="id_Date" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="responsable_magasin" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="nb_employes" nullable="true" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="15" name="chiffre_affaires_annuel" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="15" name="frais_fonctionnement" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="statut" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="sortie_magasin">
        <mapperTableEntries name="code_magasin" expression="localisation.code_magasin" type="id_String"/>
        <mapperTableEntries name="nom_magasin" expression="localisation.nom_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="ville" expression="localisation.ville" type="id_String" nullable="true"/>
        <mapperTableEntries name="region" expression="localisation.région" type="id_String" nullable="true"/>
        <mapperTableEntries name="pays" expression="localisation.pays != null ? localisation.pays : &quot;Maroc&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="surface_m2" expression="localisation.surface_m2" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="type_magasin" expression="localisation.type_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="date_ouverture" expression="localisation.date_ouverture" type="id_Date" nullable="true"/>
        <mapperTableEntries name="responsable_magasin" expression="gestion.responsable_magasin != null ? gestion.responsable_magasin : &quot;Non assigne&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="nb_employes" expression="gestion.nb_employes != null ? gestion.nb_employes : 0" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="chiffre_affaires_annuel" expression="gestion.chiffre_affaires_annuel != null ? gestion.chiffre_affaires_annuel : 0.0" type="id_Double" nullable="true"/>
        <mapperTableEntries name="frais_fonctionnement" expression="gestion.frais_fonctionnement != null ? gestion.frais_fonctionnement : 0.0" type="id_Double" nullable="true"/>
        <mapperTableEntries name="statut" expression="gestion.statut != null ? gestion.statut : &quot;Actif&quot;" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="localisation" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="nom_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="ville" type="id_String" nullable="true"/>
        <mapperTableEntries name="région" type="id_String" nullable="true"/>
        <mapperTableEntries name="pays" type="id_String" nullable="true"/>
        <mapperTableEntries name="surface_m2" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="type_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="date_ouverture" type="id_Date" nullable="true"/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="gestion" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_magasin" expression="localisation.code_magasin" type="id_String" operator="="/>
        <mapperTableEntries name="responsable_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="nb_employes" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="chiffre_affaires_annuel" type="id_Double" nullable="true"/>
        <mapperTableEntries name="frais_fonctionnement" type="id_Double" nullable="true"/>
        <mapperTableEntries name="statut" type="id_String" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tMysqlOutput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="736" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tDBOutput_1" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;dim_magasin&quot;"/>
    <elementParameter field="CLOSED_LIST" name="TABLE_ACTION" value="NONE"/>
    <elementParameter field="CLOSED_LIST" name="DATA_ACTION" value="INSERT_OR_UPDATE"/>
    <elementParameter field="TEXT" name="PROPERTIES" value="&quot;noDatetimeStringSync=true&amp;enabledTLSProtocols=TLSv1.2,TLSv1.1,TLSv1&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="dim_magasin"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tDBOutput_1">
      <column comment="" key="true" length="20" name="code_magasin" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="nom_magasin" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="ville" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="region" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="pays" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="surface_m2" nullable="true" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="type_magasin" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="date_ouverture" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" sourceType="DATE" type="id_Date" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="responsable_magasin" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="nb_employes" nullable="true" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="15" name="chiffre_affaires_annuel" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="15" name="frais_fonctionnement" nullable="true" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="statut" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <connection connectorName="FLOW" label="localisation" lineStyle="0" metaname="tFileInputDelimited_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputDelimited_1" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="localisation" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="gestion" lineStyle="8" metaname="tFileInputExcel_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_1" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="gestion" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="sortie_magasin" lineStyle="0" metaname="sortie_magasin" offsetLabelX="0" offsetLabelY="0" source="tMap_1" target="tDBOutput_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="sortie_magasin" show="false"/>
  </connection>

  <subjob>
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputDelimited_1" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_TITLE_COLOR" value="92;131;150" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_COLOR" value="207;226;236"/>
  </subjob>
</talendfile:ProcessType>
"""
    with open(os.path.join(process_dir, f"{job_name}_0.1.item"), "w", encoding="utf-8") as f:
        f.write(content)
    create_properties(job_name)
    print(f"Built {job_name}")

# ==========================================
# 4. BUILD DIM_TEMPS
# ==========================================
def build_dim_temps(job_name):
    content = header + f"""
  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="64" posY="64">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/clients_base_50.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Clients Excel"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_1">
      <column comment="" key="false" length="50" name="client_id" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="nom" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="prenom" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="ville" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="email" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="segment_marketing" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="date_inscription" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="224" posY="64">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_1" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Date inscription"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="date_base_clients">
      <column comment="" key="false" length="20" name="date_brute" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="date_base_clients" expressionFilter="dates_base_clients.date_inscription != null" activateExpressionFilter="true">
        <mapperTableEntries name="date_brute" expression="dates_base_clients.date_inscription" type="id_Date" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="dates_base_clients" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="client_id" type="id_String" nullable="true"/>
        <mapperTableEntries name="nom" type="id_String" nullable="true"/>
        <mapperTableEntries name="prenom" type="id_String" nullable="true"/>
        <mapperTableEntries name="ville" type="id_String" nullable="true"/>
        <mapperTableEntries name="email" type="id_String" nullable="true"/>
        <mapperTableEntries name="segment_marketing" type="id_String" nullable="true"/>
        <mapperTableEntries name="date_inscription" type="id_Date" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tFileInputDelimited" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="96" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputDelimited_1" show="false"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/clients_online_50.csv&quot;"/>
    <elementParameter field="CHECK" name="CSV_OPTION" value="false"/>
    <elementParameter field="TEXT" name="ROWSEPARATOR" value="&quot;\\n&quot;"/>
    <elementParameter field="TEXT" name="FIELDSEPARATOR" value="&quot;,&quot;"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Clients web"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputDelimited_1">
      <column comment="" key="false" length="50" name="client_code" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="full_name" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="email" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="city" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="first_purchase_date" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="256" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_2" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Date premier achat"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="date_clients_web">
      <column comment="" key="false" length="20" name="date_brute" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="date_clients_web" expressionFilter="dates_clients_web.first_purchase_date != null" activateExpressionFilter="true">
        <mapperTableEntries name="date_brute" expression="dates_clients_web.first_purchase_date" type="id_Date" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="dates_clients_web" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="client_code" type="id_String" nullable="true"/>
        <mapperTableEntries name="full_name" type="id_String" nullable="true"/>
        <mapperTableEntries name="email" type="id_String" nullable="true"/>
        <mapperTableEntries name="city" type="id_String" nullable="true"/>
        <mapperTableEntries name="first_purchase_date" type="id_Date" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="64" posY="256">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_2" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/produits_catalogue.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Catalogue Excel"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_2">
      <column comment="" key="false" length="50" name="code_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="nom_produit" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="categorie" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="sous_categorie" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="marque" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="prix_achat" nullable="true" pattern="" precision="2" type="id_Float" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="prix_vente" nullable="true" pattern="" precision="2" type="id_Float" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="statut" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="date_insertion" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="256" posY="256">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_3" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Date insertion produit"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="date_catalogue">
      <column comment="" key="false" length="20" name="date_brute" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="date_catalogue" expressionFilter="dates_catalogue.date_insertion != null" activateExpressionFilter="true">
        <mapperTableEntries name="date_brute" expression="dates_catalogue.date_insertion" type="id_Date" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="dates_catalogue" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_produit" type="id_String" nullable="true"/>
        <mapperTableEntries name="nom_produit" type="id_String" nullable="true"/>
        <mapperTableEntries name="categorie" type="id_String" nullable="true"/>
        <mapperTableEntries name="sous_categorie" type="id_String" nullable="true"/>
        <mapperTableEntries name="marque" type="id_String" nullable="true"/>
        <mapperTableEntries name="prix_achat" type="id_Float" nullable="true"/>
        <mapperTableEntries name="prix_vente" type="id_Float" nullable="true"/>
        <mapperTableEntries name="statut" type="id_String" nullable="true"/>
        <mapperTableEntries name="date_insertion" type="id_Date" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tFileInputDelimited" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="64" posY="352">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputDelimited_2" show="false"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/magasins_localisation (2).csv&quot;"/>
    <elementParameter field="CHECK" name="CSV_OPTION" value="false"/>
    <elementParameter field="TEXT" name="ROWSEPARATOR" value="&quot;\\n&quot;"/>
    <elementParameter field="TEXT" name="FIELDSEPARATOR" value="&quot;,&quot;"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Magasins CSV"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputDelimited_2">
      <column comment="" key="false" length="20" name="code_magasin" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="150" name="nom_magasin" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="ville" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="region" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="100" name="pays" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="surface_m2" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="type_magasin" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="date_ouverture" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="256" posY="352">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_4" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Date d'ouvetrure"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="date_localisation">
      <column comment="" key="false" length="20" name="date_brute" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="date_localisation" expressionFilter="dates_localisation.date_ouverture != null" activateExpressionFilter="true">
        <mapperTableEntries name="date_brute" expression="dates_localisation.date_ouverture" type="id_Date" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="dates_localisation" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="code_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="nom_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="ville" type="id_String" nullable="true"/>
        <mapperTableEntries name="region" type="id_String" nullable="true"/>
        <mapperTableEntries name="pays" type="id_String" nullable="true"/>
        <mapperTableEntries name="surface_m2" type="id_String" nullable="true"/>
        <mapperTableEntries name="type_magasin" type="id_String" nullable="true"/>
        <mapperTableEntries name="date_ouverture" type="id_Date" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="64" posY="448">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_3" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/ventes_synthese.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Ventes Excel"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_3">
      <column comment="" key="false" length="20" name="id_vente" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="id_client_source" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="id_produit_source" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="id_magasin_source" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="date_vente" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="quantite_vendue" nullable="true" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="prix_unitaire" nullable="true" pattern="" precision="2" type="id_Float" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="montant_total" nullable="true" pattern="" precision="2" type="id_Float" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="mode_paiement" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="256" posY="448">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_5" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Date vente"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="date_ventes">
      <column comment="" key="false" length="20" name="date_brute" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="date_ventes" expressionFilter="dates_ventes.date_vente != null" activateExpressionFilter="true">
        <mapperTableEntries name="date_brute" expression="dates_ventes.date_vente" type="id_Date" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="dates_ventes" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id_vente" type="id_String" nullable="true"/>
        <mapperTableEntries name="id_client_source" type="id_String" nullable="true"/>
        <mapperTableEntries name="id_produit_source" type="id_String" nullable="true"/>
        <mapperTableEntries name="id_magasin_source" type="id_String" nullable="true"/>
        <mapperTableEntries name="date_vente" type="id_Date" nullable="true"/>
        <mapperTableEntries name="quantite_vendue" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="prix_unitaire" type="id_Float" nullable="true"/>
        <mapperTableEntries name="montant_total" type="id_Float" nullable="true"/>
        <mapperTableEntries name="mode_paiement" type="id_String" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tUnite" componentVersion="0.101" offsetLabelX="0" offsetLabelY="0" posX="416" posY="256">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tUnite_1" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Réunir dates"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tUnite_1">
      <column comment="" key="false" length="20" name="date_brute" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tUniqRow" componentVersion="0.101" offsetLabelX="0" offsetLabelY="0" posX="544" posY="256">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tUniqRow_1" show="false"/>
    <elementParameter field="TABLE" name="UNIQUE_KEY">
      <elementValue elementRef="SCHEMA_COLUMN" value="date_brute"/>
      <elementValue elementRef="KEY_ATTRIBUTE" value="true"/>
      <elementValue elementRef="CASE_SENSITIVE" value="false"/>
    </elementParameter>
    <elementParameter field="TEXT" name="LABEL" value="Dates uniques"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tUniqRow_1">
      <column comment="" key="false" length="20" name="date_brute" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
    <metadata connector="UNIQUE" name="UNIQUE">
      <column comment="" key="false" length="20" name="date_brute" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="704" posY="256">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_6" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Mois et trimestre"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="sortie_temps">
      <column comment="" key="true" length="10" name="id_temps" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="date_complete" nullable="false" pattern="&quot;yyyy-MM-dd&quot;" precision="0" sourceType="DATE" type="id_Date" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="jour" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="mois" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="nom_mois" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="trimestre" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="annee" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="jour_semaine" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="semestre" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="annee_universitaire" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var">
        <mapperTableEntries name="m" expression="TalendDate.getPartOfDate(&quot;MONTH&quot;, dates_uniques.date_brute)" type="id_Integer"/>
      </varTables>
      <outputTables sizeState="INTERMEDIATE" name="sortie_temps" expressionFilter="dates_uniques.date_brute != null" activateExpressionFilter="true">
        <mapperTableEntries name="id_temps" expression="Integer.parseInt(TalendDate.formatDate(&quot;yyyyMMdd&quot;, dates_uniques.date_brute))" type="id_Integer"/>
        <mapperTableEntries name="date_complete" expression="dates_uniques.date_brute" type="id_Date"/>
        <mapperTableEntries name="jour" expression="TalendDate.getPartOfDate(&quot;DAY_OF_MONTH&quot;, dates_uniques.date_brute)" type="id_Integer"/>
        <mapperTableEntries name="mois" expression="Var.m + 1" type="id_Integer"/>
        <mapperTableEntries name="nom_mois" expression="TalendDate.formatDate(&quot;MMMM&quot;, dates_uniques.date_brute)" type="id_String"/>
        <mapperTableEntries name="trimestre" expression="(Var.m / 3) + 1" type="id_Integer"/>
        <mapperTableEntries name="annee" expression="TalendDate.getPartOfDate(&quot;YEAR&quot;, dates_uniques.date_brute)" type="id_Integer"/>
        <mapperTableEntries name="jour_semaine" expression="TalendDate.formatDate(&quot;EEEE&quot;, dates_uniques.date_brute)" type="id_String" nullable="true"/>
        <mapperTableEntries name="semestre" expression="(Var.m &lt; 6) ? &quot;S1&quot; : &quot;S2&quot;" type="id_String" nullable="true"/>
        <mapperTableEntries name="annee_universitaire" expression="TalendDate.getPartOfDate(&quot;YEAR&quot;, dates_uniques.date_brute) + &quot;-&quot; + (TalendDate.getPartOfDate(&quot;YEAR&quot;, dates_uniques.date_brute) + 1)" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="dates_uniques" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="date_brute" type="id_Date" nullable="true"/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tMysqlOutput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="864" posY="256">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMysqlOutput_1" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;localhost&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;dim_temps&quot;"/>
    <elementParameter field="CLOSED_LIST" name="TABLE_ACTION" value="NONE"/>
    <elementParameter field="CLOSED_LIST" name="DATA_ACTION" value="INSERT_OR_UPDATE"/>
    <elementParameter field="LABEL" name="NOTE" value="This option only applies when deploying and running in the Talend Runtime"/>
    <elementParameter field="CHECK" name="SPECIFY_DATASOURCE_ALIAS" value="false"/>
    <elementParameter field="TEXT" name="DATASOURCE_ALIAS" value="&quot;&quot;" show="false"/>
    <elementParameter field="CHECK" name="DIE_ON_ERROR" value="false"/>
    <elementParameter field="TEXT" name="PROPERTIES" value="&quot;noDatetimeStringSync=true&amp;enabledTLSProtocols=TLSv1.2,TLSv1.1,TLSv1&quot;"/>
    <elementParameter field="CHECK" name="USE_BATCH_SIZE" value="true"/>
    <elementParameter field="TEXT" name="BATCH_SIZE" value="10000"/>
    <elementParameter field="TEXT" name="LABEL" value="dim_temps"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tMysqlOutput_1">
      <column comment="" key="true" length="10" name="id_temps" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="date_complete" nullable="false" pattern="&quot;yyyy-MM-dd&quot;" precision="0" sourceType="DATE" type="id_Date" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="jour" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="mois" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="nom_mois" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="trimestre" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="annee" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="jour_semaine" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="semestre" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="annee_universitaire" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <!-- CONNECTIONS -->
  <connection connectorName="FLOW" label="dates_base_clients" lineStyle="0" metaname="tFileInputExcel_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_1" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="dates_base_clients" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="date_base_clients" lineStyle="10" mergeOrder="1" metaname="date_base_clients" offsetLabelX="0" offsetLabelY="0" source="tMap_1" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="date_base_clients" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="dates_clients_web" lineStyle="0" metaname="tFileInputDelimited_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputDelimited_1" target="tMap_2">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="dates_clients_web" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="date_clients_web" lineStyle="10" mergeOrder="2" metaname="date_clients_web" offsetLabelX="0" offsetLabelY="0" source="tMap_2" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="date_clients_web" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="dates_catalogue" lineStyle="0" metaname="tFileInputExcel_2" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_2" target="tMap_3">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="dates_catalogue" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="date_catalogue" lineStyle="10" mergeOrder="3" metaname="date_catalogue" offsetLabelX="0" offsetLabelY="0" source="tMap_3" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="date_catalogue" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="dates_localisation" lineStyle="0" metaname="tFileInputDelimited_2" offsetLabelX="0" offsetLabelY="0" source="tFileInputDelimited_2" target="tMap_4">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="dates_localisation" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="date_localisation" lineStyle="10" mergeOrder="4" metaname="date_localisation" offsetLabelX="0" offsetLabelY="0" source="tMap_4" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="date_localisation" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="dates_ventes" lineStyle="0" metaname="tFileInputExcel_3" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_3" target="tMap_5">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="dates_ventes" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="date_ventes" lineStyle="10" mergeOrder="5" metaname="date_ventes" offsetLabelX="0" offsetLabelY="0" source="tMap_5" target="tUnite_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="date_ventes" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="ensemble" lineStyle="0" metaname="tUnite_1" offsetLabelX="0" offsetLabelY="0" source="tUnite_1" target="tUniqRow_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="ensemble" show="false"/>
  </connection>

  <connection connectorName="UNIQUE" label="dates_uniques" lineStyle="0" metaname="UNIQUE" offsetLabelX="0" offsetLabelY="0" source="tUniqRow_1" target="tMap_6">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="dates_uniques" show="false"/>
  </connection>

  <connection connectorName="FLOW" label="sortie_temps" lineStyle="0" metaname="sortie_temps" offsetLabelX="0" offsetLabelY="0" source="tMap_6" target="tMysqlOutput_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="sortie_temps" show="false"/>
  </connection>

  <subjob>
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_TITLE_COLOR" value="92;131;150" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_COLOR" value="207;226;236"/>
  </subjob>
</talendfile:ProcessType>
"""
    with open(os.path.join(process_dir, f"{job_name}_0.1.item"), "w", encoding="utf-8") as f:
        f.write(content)
    create_properties(job_name)
    print(f"Built {job_name}")


# ==========================================
# 5. BUILD FAIT_VENTES
# ==========================================
def build_fait_vente(job_name):
    content = header + f"""
  <node componentName="tFileInputExcel" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="160" posY="64">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="CHECK" name="VERSION_2007" value="true"/>
    <elementParameter field="FILE" name="FILENAME" value="&quot;{sources_dir}/ventes_synthese.xlsx&quot;"/>
    <elementParameter field="CHECK" name="ALL_SHEETS" value="true"/>
    <elementParameter field="TEXT" name="HEADER" value="1"/>
    <elementParameter field="TEXT" name="FIRST_COLUMN" value="1"/>
    <elementParameter field="TEXT" name="LABEL" value="Ventes Excel"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tFileInputExcel_1">
      <column comment="" key="true" length="20" name="id_vente" nullable="false" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="id_client_source" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="id_produit_source" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="id_magasin_source" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="date_vente" nullable="true" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="quantite_vendue" nullable="true" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_unitaire" nullable="true" pattern="" precision="2" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="mode_paiement" nullable="true" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMysqlInput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="160" posY="160">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tDBInput_1" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;dim_client&quot;"/>
    <elementParameter field="MEMO_SQL" name="QUERY" value="&quot;SELECT id_client_sk, code_client FROM dim_client&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="Clés clients"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tDBInput_1">
      <column comment="" key="true" length="10" name="id_client_sk" nullable="false" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="code_client" nullable="false" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMysqlInput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="224" posY="256">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tDBInput_2" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;dim_produit&quot;"/>
    <elementParameter field="MEMO_SQL" name="QUERY" value="&quot;SELECT id_produit_sk, code_produit FROM dim_produit&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="Clés produits"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tDBInput_2">
      <column comment="" key="true" length="10" name="id_produit_sk" nullable="false" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="code_produit" nullable="false" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMysqlInput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="160" posY="352">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tDBInput_3" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;dim_magasin&quot;"/>
    <elementParameter field="MEMO_SQL" name="QUERY" value="&quot;SELECT id_magasin_sk, code_magasin FROM dim_magasin&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="Clés magasins"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tDBInput_3">
      <column comment="" key="true" length="10" name="id_magasin_sk" nullable="false" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="code_magasin" nullable="false" pattern="" precision="0" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMysqlInput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="160" posY="448">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tDBInput_4" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;dim_temps&quot;"/>
    <elementParameter field="MEMO_SQL" name="QUERY" value="&quot;SELECT id_temps, date_complete FROM dim_temps&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="Clés des dates"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tDBInput_4">
      <column comment="" key="true" length="10" name="id_temps" nullable="false" pattern="" precision="0" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="20" name="date_complete" nullable="false" pattern="&quot;yyyy-MM-dd&quot;" precision="0" type="id_Date" usefulColumn="true"/>
    </metadata>
  </node>

  <node componentName="tMap" componentVersion="2.1" offsetLabelX="0" offsetLabelY="0" posX="512" posY="224">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tMap_1" show="false"/>
    <elementParameter field="TEXT" name="LABEL" value="Calc montnat et clés"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="sortie_vente">
      <column comment="" key="true" length="20" name="code_vente" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="id_client_fk" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="id_produit_fk" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="id_magasin_fk" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="id_temps_fk" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="quantite_vendue" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_unitaire" nullable="false" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="12" name="montant_total" nullable="false" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="mode_paiement" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
    <nodeData xsi:type="TalendMapper:MapperData">
      <uiProperties shellMaximized="true"/>
      <varTables sizeState="INTERMEDIATE" name="Var" minimized="true"/>
      <outputTables sizeState="INTERMEDIATE" name="sortie_vente">
        <mapperTableEntries name="code_vente" expression="ventes.id_vente" type="id_String"/>
        <mapperTableEntries name="id_client_fk" expression="client != null &amp;&amp; client.id_client_sk &gt; 0 ? client.id_client_sk : 1" type="id_Integer"/>
        <mapperTableEntries name="id_produit_fk" expression="produit != null &amp;&amp; produit.id_produit_sk &gt; 0 ? produit.id_produit_sk : 1" type="id_Integer"/>
        <mapperTableEntries name="id_magasin_fk" expression="magasin != null &amp;&amp; magasin.id_magasin_sk &gt; 0 ? magasin.id_magasin_sk : 1" type="id_Integer"/>
        <mapperTableEntries name="id_temps_fk" expression="calendrier != null &amp;&amp; calendrier.id_temps &gt; 0 ? calendrier.id_temps : 20240101" type="id_Integer"/>
        <mapperTableEntries name="quantite_vendue" expression="ventes.quantite_vendue != null ? ventes.quantite_vendue : 1" type="id_Integer"/>
        <mapperTableEntries name="prix_unitaire" expression="ventes.prix_unitaire != null ? ventes.prix_unitaire : 0.0" type="id_Double"/>
        <mapperTableEntries name="montant_total" expression="(ventes.quantite_vendue != null ? ventes.quantite_vendue : 1) * (ventes.prix_unitaire != null ? ventes.prix_unitaire : 0.0)" type="id_Double"/>
        <mapperTableEntries name="mode_paiement" expression="ventes.mode_paiement" type="id_String" nullable="true"/>
      </outputTables>
      <inputTables sizeState="INTERMEDIATE" name="ventes" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id_vente" type="id_String"/>
        <mapperTableEntries name="id_client_source" type="id_String" nullable="true"/>
        <mapperTableEntries name="id_produit_source" type="id_String" nullable="true"/>
        <mapperTableEntries name="id_magasin_source" type="id_String" nullable="true"/>
        <mapperTableEntries name="date_vente" type="id_Date" nullable="true"/>
        <mapperTableEntries name="quantite_vendue" type="id_Integer" nullable="true"/>
        <mapperTableEntries name="prix_unitaire" type="id_Double" nullable="true"/>
        <mapperTableEntries name="mode_paiement" type="id_String" nullable="true"/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="client" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id_client_sk" type="id_Integer"/>
        <mapperTableEntries name="code_client" expression="ventes.id_client_source" type="id_String" operator="="/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="produit" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id_produit_sk" type="id_Integer"/>
        <mapperTableEntries name="code_produit" expression="ventes.id_produit_source" type="id_String" operator="="/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="magasin" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id_magasin_sk" type="id_Integer"/>
        <mapperTableEntries name="code_magasin" expression="ventes.id_magasin_source" type="id_String" operator="="/>
      </inputTables>
      <inputTables sizeState="INTERMEDIATE" name="calendrier" matchingMode="UNIQUE_MATCH" lookupMode="LOAD_ONCE">
        <mapperTableEntries name="id_temps" type="id_Integer"/>
        <mapperTableEntries name="date_complete" expression="ventes.date_vente" type="id_Date" operator="="/>
      </inputTables>
    </nodeData>
  </node>

  <node componentName="tMysqlOutput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="768" posY="224">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tDBOutput_1" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;fait_ventes&quot;"/>
    <elementParameter field="CLOSED_LIST" name="TABLE_ACTION" value="NONE"/>
    <elementParameter field="CLOSED_LIST" name="DATA_ACTION" value="INSERT_OR_UPDATE"/>
    <elementParameter field="TEXT" name="PROPERTIES" value="&quot;noDatetimeStringSync=true&amp;enabledTLSProtocols=TLSv1.2,TLSv1.1,TLSv1&quot;"/>
    <elementParameter field="TEXT" name="LABEL" value="fait_vente"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" name="tDBOutput_1">
      <column comment="" key="true" length="20" name="code_vente" nullable="false" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="id_client_fk" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="id_produit_fk" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="id_magasin_fk" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="id_temps_fk" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="quantite_vendue" nullable="false" pattern="" precision="0" sourceType="INT" type="id_Integer" usefulColumn="true"/>
      <column comment="" key="false" length="10" name="prix_unitaire" nullable="false" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="12" name="montant_total" nullable="false" pattern="" precision="2" sourceType="DECIMAL" type="id_Double" usefulColumn="true"/>
      <column comment="" key="false" length="50" name="mode_paiement" nullable="true" pattern="" precision="0" sourceType="VARCHAR" type="id_String" usefulColumn="true"/>
    </metadata>
  </node>

  <connection connectorName="FLOW" label="ventes" lineStyle="0" metaname="tFileInputExcel_1" offsetLabelX="0" offsetLabelY="0" source="tFileInputExcel_1" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="ventes" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="client" lineStyle="8" metaname="tDBInput_1" offsetLabelX="0" offsetLabelY="0" source="tDBInput_1" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="client" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="produit" lineStyle="8" metaname="tDBInput_2" offsetLabelX="0" offsetLabelY="0" source="tDBInput_2" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="produit" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="magasin" lineStyle="8" metaname="tDBInput_3" offsetLabelX="0" offsetLabelY="0" source="tDBInput_3" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="magasin" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="calendrier" lineStyle="8" metaname="tDBInput_4" offsetLabelX="0" offsetLabelY="0" source="tDBInput_4" target="tMap_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="calendrier" show="false"/>
  </connection>
  <connection connectorName="FLOW" label="sortie_vente" lineStyle="0" metaname="sortie_vente" offsetLabelX="0" offsetLabelY="0" source="tMap_1" target="tDBOutput_1">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="sortie_vente" show="false"/>
  </connection>

  <subjob>
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="tFileInputExcel_1" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_TITLE_COLOR" value="92;131;150" show="false"/>
    <elementParameter field="COLOR" name="SUBJOB_COLOR" value="207;226;236"/>
  </subjob>
</talendfile:ProcessType>
"""
    with open(os.path.join(process_dir, f"{job_name}_0.1.item"), "w", encoding="utf-8") as f:
        f.write(content)
    create_properties(job_name)
    print(f"Built {job_name}")

print("Generating all 5 jobs in TP2_BI_VENTES...")
build_dim_client("DimClient")
build_dim_client("Job_Dim_Client_Ventes")

build_dim_produit("DimProduit")
build_dim_produit("Job_Dim_Produit_Ventes")

build_dim_magasin("DimMagasin")
build_dim_magasin("Job_Dim_Magasin_Ventes")

build_dim_temps("DimTemps")
build_dim_temps("Job_Dim_Temps_Ventes")

build_fait_vente("FaitVente")
build_fait_vente("Job_Fait_Ventes")

print("ALL 5 JOBS GENERATED WITH ZERO SYNTAX ERRORS!")
