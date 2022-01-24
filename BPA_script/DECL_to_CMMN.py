#Script for convering .decl into .cmmn
import math
import xml_components

input_file = open('input.decl','r')
input_text = input_file.read()
input_file.close()
output = ""
activities = []
precedence = []
init = None

#Save init Task if there is one
if input_text.find("Init[") != -1:
    start_marker = input_text.find("Init[") + len("Init[")
    end_marker = input_text.find("\n",start_marker)
    init = input_text[start_marker:end_marker]
    init = init[:init.find("]")]

#Loop over input_text as long as there is "activity " in it to get all activities ( Tasks)
while input_text.find("activity ") != -1:
    #This is where the name of an activity starts (after "activity ")
    start_marker = 9
    #in the .decl there is a new line after every activity or constraint
    end_marker = input_text.find("\n")
    #append the name of the activity to the activities List
    activities.append(input_text[start_marker:end_marker])
    #Delete the current activity from the input text
    input_text = input_text[end_marker+1:]

#Get all precedence constraints and store them in precedence-List
while input_text.find("Precedence[") != -1:
    start_marker = input_text.find("Precedence[") + len("Precedence[")
    end_marker = input_text.find("\n",start_marker)
    mid = input_text[start_marker:end_marker]
    marker = mid.find(",")
    src = mid[:marker]
    mid = mid[marker+2:]
    marker = mid.find("]")
    dest = mid[:marker]
    insert = [src, dest]
    precedence.append(insert)
    input_text = input_text[end_marker+1:]


#Remove all Precedence constraints that have the Init Task as Source
def removeInits(list):
    for element in list:
        if element[0] == init:
            list.remove(element)
            return removeInits(list)
    return list
precedence = removeInits(precedence)


#create activity-ID Translation
activity_translator = []
id_counter = 0
for act in activities:
    id = "act_" + str(id_counter)
    activity_translator.append([act,id])
    id_counter += 1

#change activity-names to activity-IDs
for act in activities:
    for id in activity_translator:
        if act == id[0]:
            activities[activities.index(act)] = id[1]

#change activity-names in precedence to activity-IDs
translated_precedence = []
for constraint in precedence:
    new_cons = [constraint[0], constraint[1]]
    for act in constraint:
        for id in activity_translator:
            if act == id[0]:
                new_cons[new_cons.index(act)] = id[1]
    translated_precedence.append(new_cons)
precedence = translated_precedence

#change init-name to ID:
for id in activity_translator:
    if init == id[0]:
        init = id[1]




#----------------------------------------------


# determine how many rows we will need in the CMMN model
CMMN_rows = math.ceil(len(activities) / 4)

#Add start xml components
output = xml_components.CMMN_outer_start + xml_components.CMMN_case_start

#Add Init Task
if init is not None:
    cmmn_planitem_task = """ <cmmn:planItem id="Planitem_""" + init + '''"'''
    cmmn_planitem_task += """ definitionRef="Task_""" + init + """" >"""
    for element in precedence:
        if init is element[1]:
            sentry = """<cmmn:entryCriterion id="EntryCriterion_""" + element[0] + element[1] + '''"'''
            sentry += """ sentryRef="Sentry_""" + element[0] + element[1] + """" />"""
            cmmn_planitem_task += sentry
    cmmn_planitem_task += "</cmmn:planItem>"
    output += cmmn_planitem_task

#Add activities to output xml-string as "PlanItems"
#This defines the task-element-structure that can also hold sentrys and other elements
for x in activities:
    if x is not init:
        cmmn_planitem_task = """ <cmmn:planItem id="Planitem_""" + x + '''"'''
        cmmn_planitem_task += """ definitionRef="Task_""" + x + """" >"""
        for element in precedence:
            if x is element[1]:
                sentry = """<cmmn:entryCriterion id="EntryCriterion_""" + element[0] + element[1] + '''"'''
                sentry += """ sentryRef="Sentry_""" + element[0] + element[1] + """" />"""
                cmmn_planitem_task += sentry
        cmmn_planitem_task += "</cmmn:planItem>"
        output += cmmn_planitem_task


#add sentries as elements
for element in precedence:
    for id in activity_translator:
        if element[0] == id[1]:
            el_0_name = id[0]
        if element[1] == id[1]:
            el_1_name = id[0]
    sentry = """<cmmn:sentry id="Sentry_""" + element[0] + element[1] + """"> """
    sentry += """<cmmn:planItemOnPart id="PlanItemOnPart_""" + element[0] + element[1]
    sentry += """" sourceRef="Planitem_""" + element[0] + """"> """
    sentry += "<cmmn:standardEvent>" + "Precedence[" + el_0_name + "," + el_1_name +"]"
    sentry += "</cmmn:standardEvent>"
    sentry += "</cmmn:planItemOnPart> </cmmn:sentry>"
    output += sentry

#add activities as Tasks
#This defines the pure Task elements in .cmmn
for x in activities:
    for id in activity_translator:
        if x == id[1]:
            x_name = id[0]
    if x == init:
        cmmn_task = """ <cmmn:task id="Task_""" + x + '''"''' + ' name="Init_' + x_name + '" />'
        output += cmmn_task
    else:
        cmmn_task = """ <cmmn:task id="Task_""" + x + '''"''' + ' name="' + x_name + '" />'
        output += cmmn_task

#Close cmmn:case and start cmmndi:CMMNDI
output += xml_components.CMMN_case_end + xml_components.CMMN_cmmndi_start

#Define position and size of the model:
#position is always: x100, y100
#width is always: 900 (for 4 columns of tasks)
output += """<cmmndi:CMMNShape id="DI_CasePlanModel_1" cmmnElementRef="CasePlanModel_1"> <dc:Bounds x="150" y="100" width="900" """
height = (150 * CMMN_rows)
output += ''' height="''' + str(height) + '''" /> <cmmndi:CMMNLabel /> </cmmndi:CMMNShape>'''

#add activity position and size
#size is always 100x80
#position is based on row and column - which are based on the length of the activity list
for act in activities:
    counter = activities.index(act)+1
    row = math.ceil(counter/4)
    if row > 1:
        column = counter - (4 * (row-1))
    else:
        column = counter
    x = (column * 200)
    y = (row * 135)
    output += """<cmmndi:CMMNShape id="PlanItem_""" + act + """_di" """ + """cmmnElementRef="Planitem_""" + act + '''"> <dc:Bounds '''
    output += '''x="''' + str(x) + '''" y="''' + str(y) + """" width="100" height="80" /> <cmmndi:CMMNLabel /> </cmmndi:CMMNShape> """

#Sentry shapes
for element in precedence:
    sentry = """<cmmndi:CMMNShape id="EntryCriterion_""" + element[0] + element[1]
    sentry += """_di" cmmnElementRef="EntryCriterion_""" + element[0] + element[1] + """">"""
    for act in activities:
        if act is element[1]:
            counter = activities.index(act)+1
            row = math.ceil(counter/4)
            if row > 1:
                column = counter - (4 * (row-1))
            else:
                column = counter
            x = (column * 200) -10
            y = 160 + ((row -1)*135)
    sentry += """ <dc:Bounds x=" """ + str(x) + '''" y="''' + str(y) + """ " width="20" height="28" />"""
    sentry += "<cmmndi:CMMNLabel /> </cmmndi:CMMNShape>"
    output += sentry

#print(activities)
#print(precedence)

#Edge shapes:
for element in precedence:
    edge = """<cmmndi:CMMNEdge id="PlanItemOnPart_""" + element[0] + element[1]
    edge += """_di" cmmnElementRef="PlanItemOnPart_""" + element[0] + element[1]
    edge += """" targetCMMNElementRef="EntryCriterion_""" + element[0] + element[1]
    edge += """" isStandardEventVisible="true">"""
    for act in activities:
        if act == element[0]:
            counter = activities.index(act)+1
            row = math.ceil(counter/4)

            if row > 1:
                column = counter - (4 * (row-1))
            else:
                column = counter
            x0 = (column * 200) +100
            y0 = 175 + ((row -1)*135)
        if act == element[1]:
            counter = activities.index(act)+1
            row = math.ceil(counter/4)
            if row > 1:
                column = counter - (4 * (row-1))
            else:
                column = counter
            x1 = (column * 200) -10
            y1 = 175 + ((row -1)*135)
    edge += """<di:waypoint x=" """ + str(x0) + """ " y=" """ + str(y0) + """ " />"""
    edge += """<di:waypoint x=" """ + str(x1) + """ " y=" """ + str(y1) + """ " />"""
    edge += """<cmmndi:CMMNLabel> <dc:Bounds x=" """ + str(x0) + """ " y=" """ + str(y0)
    edge += """ " width="51" height="12" /> </cmmndi:CMMNLabel> </cmmndi:CMMNEdge>"""
    output += edge

#Add end-xml-components
output += xml_components.CMMN_end

#print(input_text)
#print(output)


#Write output to output.cmmn file
output_file = open('output.cmmn','w')
output_file.write(output)
output_file.close()
