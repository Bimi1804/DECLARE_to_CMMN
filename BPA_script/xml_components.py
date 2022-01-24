p = "TEST"

CMMN_outer_start = """<?xml version="1.0" encoding="UTF-8"?>
<cmmn:definitions xmlns:dc="http://www.omg.org/spec/CMMN/20151109/DC" xmlns:cmmndi="http://www.omg.org/spec/CMMN/20151109/CMMNDI" xmlns:cmmn="http://www.omg.org/spec/CMMN/20151109/MODEL" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:di="http://www.omg.org/spec/CMMN/20151109/DI" id="Definitions_1s3pa6b" targetNamespace="http://bpmn.io/schema/cmmn" exporter="Camunda Modeler" exporterVersion="3.0.0">
"""


CMMN_case_start = """<cmmn:case id="Case_1"><cmmn:casePlanModel id="CasePlanModel_1" name="A CasePlanModel">"""
CMMN_case_end = """</cmmn:casePlanModel></cmmn:case>"""

CMMN_cmmndi_start = """<cmmndi:CMMNDI><cmmndi:CMMNDiagram id="CMMNDiagram_1"> <cmmndi:Size width="500" height="500" /> """

CMMN_end = """</cmmndi:CMMNDiagram> </cmmndi:CMMNDI> </cmmn:definitions>"""
