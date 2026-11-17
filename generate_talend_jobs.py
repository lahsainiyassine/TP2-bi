import os
import uuid

talaxie_process_dir = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\MINI_PROJET\process"
backup_process_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\jobs_talaxie"
os.makedirs(backup_process_dir, exist_ok=True)

def make_id():
    return "_" + uuid.uuid4().hex[:22]

def create_properties_content(job_name):
    prop_xmi_id = make_id()
    prop_id = make_id()
    item_xmi_id = make_id()
    state_xmi_id = make_id()
    add_ids = [make_id() for _ in range(6)]
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:TalendProperties="http://www.talend.org/properties">
  <TalendProperties:Property xmi:id="{prop_xmi_id}" id="{prop_id}" label="{job_name}" version="0.1" statusCode="" item="{item_xmi_id}" displayName="{job_name}">
    <author href="../talend.project#_9EEDoM9UEfG71M3VwE5zwA"/>
    <additionalProperties xmi:id="{add_ids[0]}" key="created_product_fullname" value="Talaxie Open Studio for Data Integration"/>
    <additionalProperties xmi:id="{add_ids[1]}" key="created_product_version" value="8.9.0.20261020-1837-SNAPSHOT"/>
    <additionalProperties xmi:id="{add_ids[2]}" key="created_date" value="2026-11-17T17:00:00.000+0000"/>
    <additionalProperties xmi:id="{add_ids[3]}" key="modified_product_fullname" value="Talaxie Open Studio for Data Integration"/>
    <additionalProperties xmi:id="{add_ids[4]}" key="modified_product_version" value="8.9.0.20261018-1926-SNAPSHOT"/>
    <additionalProperties xmi:id="{add_ids[5]}" key="modified_date" value="2026-11-17T17:30:00.000+0100"/>
  </TalendProperties:Property>
  <TalendProperties:ItemState xmi:id="{state_xmi_id}" path=""/>
  <TalendProperties:ProcessItem xmi:id="{item_xmi_id}" property="{prop_xmi_id}" state="{state_xmi_id}">
    <process href="{job_name}_0.1.item#/"/>
  </TalendProperties:ProcessItem>
</xmi:XMI>"""

# Load template parameters from existing Job_Dim_Temps_0.1.item
ref_item_path = os.path.join(talaxie_process_dir, "Job_Dim_Temps_0.1.item")
with open(ref_item_path, 'r', encoding='utf-8') as f:
    ref_content = f.read()

# Extract parameters block
p_start = ref_content.find("<parameters>")
p_end = ref_content.find("</parameters>") + len("</parameters>")
parameters_block = ref_content[p_start:p_end]

# Common MySQL connection snippet
def mysql_output_node(unique_name, table_name, pos_x, pos_y, columns_xml, field_options_xml):
    return f"""  <node componentName="tMysqlOutput" componentVersion="0.102" offsetLabelX="0" offsetLabelY="0" posX="{pos_x}" posY="{pos_y}">
    <elementParameter field="TEXT" name="UNIQUE_NAME" value="{unique_name}" show="false"/>
    <elementParameter field="CLOSED_LIST" name="DB_VERSION" value="MYSQL_8"/>
    <elementParameter field="CHECK" name="USE_EXISTING_CONNECTION" value="false"/>
    <elementParameter field="COMPONENT_LIST" name="CONNECTION" value="" show="false"/>
    <elementParameter field="TEXT" name="TYPE" value="MYSQL" show="false"/>
    <elementParameter field="TEXT" name="HOST" value="&quot;127.0.0.1&quot;"/>
    <elementParameter field="TEXT" name="PORT" value="&quot;3306&quot;"/>
    <elementParameter field="TEXT" name="DBNAME" value="&quot;dwh_ventes&quot;"/>
    <elementParameter field="TEXT" name="USER" value="&quot;root&quot;"/>
    <elementParameter field="PASSWORD" name="PASS" value="enc:system.encryption.key.v1:Qpev7D0jsvqce+aBXvgu1gqggEzChTPb5m1P0Q6/"/>
    <elementParameter field="DBTABLE" name="TABLE" value="&quot;{table_name}&quot;"/>
    <elementParameter field="CLOSED_LIST" name="TABLE_ACTION" value="NONE"/>
    <elementParameter field="CLOSED_LIST" name="DATA_ACTION" value="INSERT"/>
    <elementParameter field="CHECK" name="DIE_ON_ERROR" value="false"/>
    <elementParameter field="MAPPING_TYPE" name="MAPPING" value="mysql_id" show="false"/>
    <elementParameter field="TEXT" name="PROPERTIES" value="&quot;noDatetimeStringSync=true&amp;enabledTLSProtocols=TLSv1.2,TLSv1.1,TLSv1&quot;"/>
    <elementParameter field="CHECK" name="EXTENDINSERT" value="true"/>
    <elementParameter field="TEXT" name="NB_ROWS_PER_INSERT" value="100"/>
    <elementParameter field="TEXT" name="COMMIT_EVERY" value="10000"/>
    <elementParameter field="TABLE" name="ADD_COLS"/>
    <elementParameter field="CHECK" name="USE_FIELD_OPTIONS" value="false"/>
    <elementParameter field="TABLE" name="FIELD_OPTIONS" show="false">
{field_options_xml}
    </elementParameter>
    <elementParameter field="CHECK" name="USE_HINT_OPTIONS" value="false"/>
    <elementParameter field="CHECK" name="ENABLE_DEBUG_MODE" value="false"/>
    <elementParameter field="TEXT" name="LABEL" value="{table_name}"/>
    <elementParameter field="TEXT" name="CONNECTION_FORMAT" value="row"/>
    <metadata connector="FLOW" label="{table_name}" name="{unique_name}">
{columns_xml}
    </metadata>
    <metadata connector="REJECT" label="{table_name}" name="REJECT">
{columns_xml}
      <column defaultValue="" key="false" length="255" name="errorCode" nullable="true" precision="0" sourceType="VARCHAR" type="id_String" originalLength="-1" usefulColumn="true"/>
      <column defaultValue="" key="false" length="255" name="errorMessage" nullable="true" precision="0" sourceType="VARCHAR" type="id_String" originalLength="-1" usefulColumn="true"/>
    </metadata>
  </node>"""

print("Setup completed successfully.")
