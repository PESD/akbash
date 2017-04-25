# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VisionsModel(models.Model):
    class Meta:
        managed = False


class Viwpremployees(VisionsModel):
    jobtitle = models.CharField(db_column='JobTitle', max_length=25, blank=True, null=True)  # Field name made lowercase.
    departmentdescription = models.CharField(db_column='DepartmentDescription', max_length=75, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=99)  # Field name made lowercase.
    # employeessn = models.CharField(db_column='EmployeeSSN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    # ethnicity = models.CharField(db_column='Ethnicity', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.
    employeeid = models.CharField(db_column='EmployeeID', max_length=10)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=25)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=25)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=25)  # Field name made lowercase.
    jobid = models.IntegerField(db_column='JobID')  # Field name made lowercase.
    # employeeaddress1 = models.CharField(db_column='EmployeeAddress1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    # employeeaddress2 = models.CharField(db_column='EmployeeAddress2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    # employeecity = models.CharField(db_column='EmployeeCity', max_length=30, blank=True, null=True)  # Field name made lowercase.
    # employeestate = models.CharField(db_column='EmployeeState', max_length=2)  # Field name made lowercase.
    # employeezipcode = models.CharField(db_column='EmployeeZipCode', max_length=10)  # Field name made lowercase.
    # employeehomephone = models.CharField(db_column='EmployeeHomePhone', max_length=15)  # Field name made lowercase.
    payrollstatus = models.SmallIntegerField(db_column='PayrollStatus')  # Field name made lowercase.
    # gender = models.SmallIntegerField(db_column='Gender')  # Field name made lowercase.
    departmentid = models.SmallIntegerField(db_column='DepartmentID')  # Field name made lowercase.
    # birthdate = models.DateTimeField(db_column='BirthDate', blank=True, null=True)  # Field name made lowercase.
    hiredate = models.DateTimeField(db_column='HireDate', blank=True, null=True)  # Field name made lowercase.
    termdate = models.DateTimeField(db_column='TermDate', blank=True, null=True)  # Field name made lowercase.
    # endprobationdate = models.DateTimeField(db_column='EndProbationDate', blank=True, null=True)  # Field name made lowercase.
    # leavebankstartdate = models.DateTimeField(db_column='LeaveBankStartDate', blank=True, null=True)  # Field name made lowercase.
    # benefitseligdate = models.DateTimeField(db_column='BenefitsEligDate', blank=True, null=True)  # Field name made lowercase.
    # senioritydate = models.DateTimeField(db_column='SeniorityDate', blank=True, null=True)  # Field name made lowercase.
    rehiredate = models.DateTimeField(db_column='ReHireDate', blank=True, null=True)  # Field name made lowercase.
    # emergencycontactphone = models.CharField(db_column='EmergencyContactPhone', max_length=12, blank=True, null=True)  # Field name made lowercase.
    # useremployeeid = models.CharField(db_column='UserEmployeeID', max_length=20)  # Field name made lowercase.
    # yearsexperience = models.FloatField(db_column='YearsExperience')  # Field name made lowercase.
    # comments = models.TextField(db_column='Comments')  # Field name made lowercase. This field type is a guess.
    nameprefix = models.CharField(db_column='NamePrefix', max_length=4)  # Field name made lowercase.
    # generationid = models.CharField(db_column='GenerationID', max_length=20)  # Field name made lowercase.
    # workphone = models.CharField(db_column='WorkPhone', max_length=15)  # Field name made lowercase.
    # workphoneext = models.IntegerField(db_column='WorkPhoneExt')  # Field name made lowercase.
    # tblhrmasterethnicityid = models.IntegerField(db_column='tblHRMasterEthnicityID')  # Field name made lowercase.
    # married = models.SmallIntegerField(db_column='Married', blank=True, null=True)  # Field name made lowercase.
    # previousname = models.CharField(db_column='PreviousName', max_length=25)  # Field name made lowercase.
    # yearsexpprevious = models.FloatField(db_column='YearsExpPrevious')  # Field name made lowercase.
    # yearsexpdistrict = models.FloatField(db_column='YearsExpDistrict')  # Field name made lowercase.
    # familiarname = models.CharField(db_column='FamiliarName', max_length=25)  # Field name made lowercase.
    # hrnewemployee = models.BooleanField(db_column='HRNewEmployee')  # Field name made lowercase.
    newhire = models.BooleanField(db_column='NewHire')  # Field name made lowercase.
    employeeemail = models.CharField(db_column='EmployeeEmail', max_length=255)  # Field name made lowercase.
    # supressphone = models.BooleanField(db_column='SupressPhone')  # Field name made lowercase.
    # tblprclassificationid = models.IntegerField(db_column='tblPRClassificationID')  # Field name made lowercase.
    # emergencyaddress1 = models.CharField(db_column='EmergencyAddress1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    # emergencyaddress2 = models.CharField(db_column='EmergencyAddress2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    # emergencycity = models.CharField(db_column='EmergencyCity', max_length=30)  # Field name made lowercase.
    # emergencystate = models.CharField(db_column='EmergencyState', max_length=2)  # Field name made lowercase.
    # emergencyzipcode = models.CharField(db_column='EmergencyZipCode', max_length=10)  # Field name made lowercase.
    # concurrencyid = models.IntegerField(db_column='ConcurrencyID')  # Field name made lowercase.
    # tblprterminationcodeid = models.IntegerField(db_column='tblPRTerminationCodeID')  # Field name made lowercase.
    # participatesleavebank = models.BooleanField(db_column='ParticipatesLeaveBank')  # Field name made lowercase.
    # tblprstatusid = models.IntegerField(db_column='tblPRStatusID')  # Field name made lowercase.
    # issubstitute = models.BooleanField(db_column='IsSubstitute')  # Field name made lowercase.
    # tblprinsclassid = models.IntegerField(db_column='tblPRInsClassID')  # Field name made lowercase.
    # tblprleavebankid = models.IntegerField(db_column='tblPRLeaveBankID')  # Field name made lowercase.
    # ethnicityid = models.IntegerField(db_column='EthnicityID', blank=True, null=True)  # Field name made lowercase.
    classification = models.CharField(db_column='Classification', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # status = models.CharField(db_column='Status', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # insuranceclass = models.CharField(db_column='InsuranceClass', max_length=15)  # Field name made lowercase.
    # leavebankplan = models.CharField(db_column='LeaveBankPlan', max_length=15)  # Field name made lowercase.
    # terminationcode = models.CharField(db_column='TerminationCode', max_length=15)  # Field name made lowercase.
    # tblhrapplicantsid = models.IntegerField(db_column='tblHRApplicantsID')  # Field name made lowercase.
    # hrnewhire = models.CharField(db_column='HRNewHire', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # csz = models.CharField(db_column='CSZ', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dobmonth = models.IntegerField(db_column='DOBMonth', blank=True, null=True)  # Field name made lowercase.
    dobday = models.IntegerField(db_column='DOBDay', blank=True, null=True)  # Field name made lowercase.
    dobmonthname = models.CharField(db_column='DOBMonthName', max_length=30)  # Field name made lowercase.
    # tblprtemplateid = models.IntegerField(db_column='tblPRTemplateID')  # Field name made lowercase.
    # templatename = models.CharField(db_column='TemplateName', max_length=50)  # Field name made lowercase.
    # prgender = models.CharField(db_column='PRGender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # issuepaycheck = models.NullBooleanField(db_column='IssuePayCheck')  # Field name made lowercase.
    # statecode = models.CharField(db_column='StateCode', max_length=75, blank=True, null=True)  # Field name made lowercase.
    # eeocclass = models.CharField(db_column='EEOCClass', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # tenuredate = models.DateTimeField(db_column='TenureDate', blank=True, null=True)  # Field name made lowercase.
    # leaveaccrualdate = models.DateTimeField(db_column='LeaveAccrualDate', blank=True, null=True)  # Field name made lowercase.
    # totalyears = models.FloatField(db_column='TotalYears')  # Field name made lowercase.
    # issuepaychecktext = models.CharField(db_column='IssuePayCheckText', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # tblhrmastereeocclassificationid = models.IntegerField(db_column='tblHRMasterEEOCClassificationID')  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=75, blank=True, null=True)  # Field name made lowercase.
    # sifethnicitycode = models.CharField(db_column='SIFEthnicityCode', max_length=75, blank=True, null=True)  # Field name made lowercase.
    # eeoccode = models.IntegerField(db_column='EEOCCode', blank=True, null=True)  # Field name made lowercase.
    # maskssn = models.CharField(db_column='MaskSSN', max_length=11)  # Field name made lowercase.
    # employeeinternetaccess = models.BooleanField(db_column='EmployeeInternetAccess')  # Field name made lowercase.
    # cellphone = models.CharField(db_column='CellPhone', max_length=15)  # Field name made lowercase.
    stateid = models.CharField(db_column='StateID', max_length=50)  # Field name made lowercase.
    # userdata1 = models.CharField(db_column='UserData1', max_length=50)  # Field name made lowercase.
    # userdata2 = models.CharField(db_column='UserData2', max_length=50)  # Field name made lowercase.
    # userdata3 = models.CharField(db_column='UserData3', max_length=50)  # Field name made lowercase.
    # userdata4 = models.CharField(db_column='UserData4', max_length=50)  # Field name made lowercase.
    # userdata5 = models.CharField(db_column='UserData5', max_length=50)  # Field name made lowercase.
    # userdata6 = models.CharField(db_column='UserData6', max_length=50)  # Field name made lowercase.
    # userdata7 = models.CharField(db_column='UserData7', max_length=50)  # Field name made lowercase.
    # userdata8 = models.CharField(db_column='UserData8', max_length=50)  # Field name made lowercase.
    # userdata9 = models.CharField(db_column='UserData9', max_length=50)  # Field name made lowercase.
    # userdata10 = models.CharField(db_column='UserData10', max_length=50)  # Field name made lowercase.
    # userdata11 = models.CharField(db_column='UserData11', max_length=50)  # Field name made lowercase.
    # userdata12 = models.CharField(db_column='UserData12', max_length=50)  # Field name made lowercase.
    # userdata13 = models.CharField(db_column='UserData13', max_length=50)  # Field name made lowercase.
    # userdata14 = models.CharField(db_column='UserData14', max_length=50)  # Field name made lowercase.
    # userdata15 = models.CharField(db_column='UserData15', max_length=50)  # Field name made lowercase.
    # userdata16 = models.CharField(db_column='UserData16', max_length=50)  # Field name made lowercase.
    # userdata17 = models.CharField(db_column='UserData17', max_length=50)  # Field name made lowercase.
    # userdata18 = models.CharField(db_column='UserData18', max_length=50)  # Field name made lowercase.
    # userdata19 = models.CharField(db_column='UserData19', max_length=50)  # Field name made lowercase.
    # userdata20 = models.CharField(db_column='UserData20', max_length=50)  # Field name made lowercase.
    # class_field = models.CharField(db_column='Class', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    # tblglmedicaidclassid = models.IntegerField(db_column='tblGLMedicaidClassID')  # Field name made lowercase.
    # portalusername = models.CharField(db_column='PortalUserName', max_length=100)  # Field name made lowercase.
    # prmarried = models.CharField(db_column='PRMarried', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # tblpremployeesid = models.IntegerField(db_column='tblPREmployeesID')  # Field name made lowercase.
    # insfrequency = models.IntegerField(db_column='InsFrequency')  # Field name made lowercase.
    # insbenefitallowance = models.DecimalField(db_column='InsBenefitAllowance', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # insbenefitallowanceny = models.DecimalField(db_column='InsBenefitAllowanceNY', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # insclassdescription = models.CharField(db_column='InsClassDescription', max_length=50)  # Field name made lowercase.
    # creditedservice = models.FloatField(db_column='CreditedService')  # Field name made lowercase.
    # frequency = models.IntegerField(db_column='Frequency')  # Field name made lowercase.
    # tpafrequency = models.IntegerField(db_column='TPAFrequency')  # Field name made lowercase.
    # startperiod = models.IntegerField(db_column='StartPeriod', blank=True, null=True)  # Field name made lowercase.
    # planbegin = models.DateTimeField(db_column='PlanBegin', blank=True, null=True)  # Field name made lowercase.
    # planend = models.DateTimeField(db_column='PlanEnd', blank=True, null=True)  # Field name made lowercase.
    # tblprmasterinsuranceclassid = models.IntegerField(db_column='tblPRMasterInsuranceClassID', blank=True, null=True)  # Field name made lowercase.
    # archive = models.NullBooleanField(db_column='Archive')  # Field name made lowercase.
    # nmtribe = models.CharField(db_column='NMTribe', max_length=2)  # Field name made lowercase.
    # nmhqpdteachers = models.CharField(db_column='NMHQPDTeachers', max_length=1)  # Field name made lowercase.
    # nmhqmsbegteacher = models.CharField(db_column='NMHQMSBegTeacher', max_length=1)  # Field name made lowercase.
    # nmhqpdadmins = models.CharField(db_column='NMHQPDAdmins', max_length=1)  # Field name made lowercase.
    # nmbdi = models.CharField(db_column='NMBDI', max_length=2)  # Field name made lowercase.
    # nmhd = models.CharField(db_column='NMHD', max_length=1)  # Field name made lowercase.
    # nmhdi = models.CharField(db_column='NMHDI', max_length=2)  # Field name made lowercase.
    # nmtitleiafte = models.CharField(db_column='NMTitleIAFTE', max_length=3)  # Field name made lowercase.
    # nmtitleivfte = models.CharField(db_column='NMTitleIVFTE', max_length=3)  # Field name made lowercase.
    # nmstatus = models.CharField(db_column='NMStatus', max_length=1)  # Field name made lowercase.
    # locationaddress1 = models.CharField(db_column='LocationAddress1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # locationaddress2 = models.CharField(db_column='LocationAddress2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # locationcity = models.CharField(db_column='LocationCity', max_length=30, blank=True, null=True)  # Field name made lowercase.
    # locationstate = models.CharField(db_column='LocationState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    # locationzipcode = models.CharField(db_column='LocationZipCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    # locationcode = models.CharField(db_column='LocationCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    # empfte = models.FloatField(db_column='EmpFTE')  # Field name made lowercase.
    # primaryworksite = models.CharField(db_column='PrimaryWorksite', max_length=100)  # Field name made lowercase.
    # emaildd = models.BooleanField(db_column='EmailDD')  # Field name made lowercase.
    # tblprprimaryworksitesid = models.IntegerField(db_column='tblPRPrimaryWorksitesID')  # Field name made lowercase.
    # coyrsteachinginstate = models.IntegerField(db_column='COYrsTeachingInState')  # Field name made lowercase.
    # coyrsteachingoutstate = models.IntegerField(db_column='COYrsTeachingOutState')  # Field name made lowercase.
    # coyrseduinstate = models.IntegerField(db_column='COYrsEduInState')  # Field name made lowercase.
    # coyrseduoutstate = models.IntegerField(db_column='COYrsEduOutState')  # Field name made lowercase.
    # coyrsprincipalany = models.IntegerField(db_column='COYrsPrincipalAny')  # Field name made lowercase.
    # codistrictresidence = models.CharField(db_column='CODistrictResidence', max_length=4)  # Field name made lowercase.
    # copassparatest = models.CharField(db_column='COPassParaTest', max_length=2)  # Field name made lowercase.
    # copasscoretest = models.CharField(db_column='COPassCoreTest', max_length=2)  # Field name made lowercase.
    # cotenure = models.CharField(db_column='COTenure', max_length=2)  # Field name made lowercase.
    # costateadmincore = models.CharField(db_column='COStateAdminCore', max_length=2)  # Field name made lowercase.
    # orperswagecode = models.CharField(db_column='ORPERSWageCode', max_length=2)  # Field name made lowercase.
    # ilworkerscompclass = models.CharField(db_column='ILWorkersCompClass', max_length=4)  # Field name made lowercase.
    # daysexperience = models.IntegerField(db_column='DaysExperience')  # Field name made lowercase.
    # daysexpprevious = models.IntegerField(db_column='DaysExpPrevious')  # Field name made lowercase.
    # daysexpdistrict = models.IntegerField(db_column='DaysExpDistrict')  # Field name made lowercase.
    # creditedservicedays = models.IntegerField(db_column='CreditedServiceDays')  # Field name made lowercase.
    # totaldays = models.IntegerField(db_column='TotalDays', blank=True, null=True)  # Field name made lowercase.
    # lastpaiddate = models.DateTimeField(db_column='LastPaidDate', blank=True, null=True)  # Field name made lowercase.
    # certified = models.NullBooleanField(db_column='Certified')  # Field name made lowercase.
    # illocationstatus = models.CharField(db_column='ILLocationStatus', max_length=1)  # Field name made lowercase.
    # ilmonthsemployed = models.SmallIntegerField(db_column='ILMonthsEmployed')  # Field name made lowercase.
    # ilpercenttimeadmin = models.SmallIntegerField(db_column='ILPercentTimeAdmin')  # Field name made lowercase.
    # neuscitizen = models.BooleanField(db_column='NEUSCitizen')  # Field name made lowercase.
    # castrsmembershiperror = models.BooleanField(db_column='CASTRSMembershipError')  # Field name made lowercase.
    # castrsbirthdateerror = models.BooleanField(db_column='CASTRSBirthDateError')  # Field name made lowercase.
    # necontractdate = models.DateTimeField(db_column='NEContractDate', blank=True, null=True)  # Field name made lowercase.
    # needucationattained = models.CharField(db_column='NEEducationAttained', max_length=2)  # Field name made lowercase.
    # nepassparatest = models.CharField(db_column='NEPassParaTest', max_length=1)  # Field name made lowercase.
    # necontractorg = models.CharField(db_column='NEContractOrg', max_length=8)  # Field name made lowercase.
    # nelocalcontract = models.BooleanField(db_column='NELocalContract')  # Field name made lowercase.
    # neexcludefromnssrs = models.BooleanField(db_column='NEExcludeFromNSSRS')  # Field name made lowercase.
    # ortspcid = models.IntegerField(db_column='ORTSPCID')  # Field name made lowercase.
    # nmtblhrmasterethnicityid2 = models.IntegerField(db_column='NMtblHRMasterEthnicityID2')  # Field name made lowercase.
    # nmtblhrmasterethnicityid3 = models.IntegerField(db_column='NMtblHRMasterEthnicityID3')  # Field name made lowercase.
    # nmtblhrmasterethnicityid4 = models.IntegerField(db_column='NMtblHRMasterEthnicityID4')  # Field name made lowercase.
    # nmtblhrmasterethnicityid5 = models.IntegerField(db_column='NMtblHRMasterEthnicityID5')  # Field name made lowercase.
    # cotechproficiencylevel = models.CharField(db_column='COTechProficiencyLevel', max_length=2)  # Field name made lowercase.
    # cotechassessmenttype = models.CharField(db_column='COTechAssessmentType', max_length=2)  # Field name made lowercase.
    # cotechassessmentdate = models.CharField(db_column='COTechAssessmentDate', max_length=8)  # Field name made lowercase.
    # ilemploymenttype = models.CharField(db_column='ILEmploymentType', max_length=1)  # Field name made lowercase.
    # illowestgrade = models.CharField(db_column='ILLowestGrade', max_length=2)  # Field name made lowercase.
    # ilhighestgrade = models.CharField(db_column='ILHighestGrade', max_length=2)  # Field name made lowercase.
    # ilteachassignment1 = models.CharField(db_column='ILTeachAssignment1', max_length=3)  # Field name made lowercase.
    # ilteachassignment2 = models.CharField(db_column='ILTeachAssignment2', max_length=3)  # Field name made lowercase.
    # ilteachassignment3 = models.CharField(db_column='ILTeachAssignment3', max_length=3)  # Field name made lowercase.
    # ilteachassignment4 = models.CharField(db_column='ILTeachAssignment4', max_length=3)  # Field name made lowercase.
    # ilteachassignment5 = models.CharField(db_column='ILTeachAssignment5', max_length=3)  # Field name made lowercase.
    # ilteachassignment6 = models.CharField(db_column='ILTeachAssignment6', max_length=3)  # Field name made lowercase.
    # ilteachassignment7 = models.CharField(db_column='ILTeachAssignment7', max_length=3)  # Field name made lowercase.
    # ilclassestaught1 = models.SmallIntegerField(db_column='ILClassesTaught1')  # Field name made lowercase.
    # ilclassestaught2 = models.SmallIntegerField(db_column='ILClassesTaught2')  # Field name made lowercase.
    # ilclassestaught3 = models.SmallIntegerField(db_column='ILClassesTaught3')  # Field name made lowercase.
    # ilclassestaught4 = models.SmallIntegerField(db_column='ILClassesTaught4')  # Field name made lowercase.
    # ilclassestaught5 = models.SmallIntegerField(db_column='ILClassesTaught5')  # Field name made lowercase.
    # ilclassestaught6 = models.SmallIntegerField(db_column='ILClassesTaught6')  # Field name made lowercase.
    # ilclassestaught7 = models.SmallIntegerField(db_column='ILClassesTaught7')  # Field name made lowercase.
    # ilpercenttimeemployed = models.SmallIntegerField(db_column='ILPercentTimeEmployed')  # Field name made lowercase.
    # hasdocs = models.CharField(db_column='HasDocs', max_length=3)  # Field name made lowercase.
    # tblnmteclassificationid = models.IntegerField(db_column='tblNMTEClassificationID')  # Field name made lowercase.
    # caarsmemberstatus = models.CharField(db_column='CAARSMemberStatus', max_length=1)  # Field name made lowercase.
    # caarsretirementdate = models.DateTimeField(db_column='CAARSRetirementDate', blank=True, null=True)  # Field name made lowercase.
    # caarsactivedate = models.DateTimeField(db_column='CAARSActiveDate', blank=True, null=True)  # Field name made lowercase.
    # capersmemberstatus = models.CharField(db_column='CAPERSMemberStatus', max_length=1)  # Field name made lowercase.
    # capersmembertype = models.CharField(db_column='CAPERSMemberType', max_length=1)  # Field name made lowercase.
    # capersretirementdate = models.DateTimeField(db_column='CAPERSRetirementDate', blank=True, null=True)  # Field name made lowercase.
    # capersactivedate = models.DateTimeField(db_column='CAPERSActiveDate', blank=True, null=True)  # Field name made lowercase.
    # capersmembershipnumber = models.CharField(db_column='CAPERSMembershipNumber', max_length=10)  # Field name made lowercase.
    # castrsmemberstatus = models.CharField(db_column='CASTRSMemberStatus', max_length=1)  # Field name made lowercase.
    # castrsmembertype = models.CharField(db_column='CASTRSMemberType', max_length=1)  # Field name made lowercase.
    # castrsretirementdate = models.DateTimeField(db_column='CASTRSRetirementDate', blank=True, null=True)  # Field name made lowercase.
    # castrsactivedate = models.DateTimeField(db_column='CASTRSActiveDate', blank=True, null=True)  # Field name made lowercase.
    # primaryworksitecode = models.CharField(db_column='PrimaryWorksiteCode', max_length=50)  # Field name made lowercase.
    # ethnicorigin = models.CharField(db_column='EthnicOrigin', max_length=1)  # Field name made lowercase.
    # tblprndprevemptypeid = models.IntegerField(db_column='tblPRNDPrevEmpTypeID')  # Field name made lowercase.
    # ndyrsadminexp = models.IntegerField(db_column='NDYrsAdminExp')  # Field name made lowercase.
    # coteacherprobationarystatus = models.CharField(db_column='COTeacherProbationaryStatus', max_length=2)  # Field name made lowercase.
    # coformalperformanceevaluationdate = models.DateTimeField(db_column='COFormalPerformanceEvaluationDate')  # Field name made lowercase.
    # coteacherperformance = models.CharField(db_column='COTeacherPerformance', max_length=2)  # Field name made lowercase.
    # colaedid = models.CharField(db_column='COLAEDID', max_length=14)  # Field name made lowercase.
    # coprincipalperformance = models.CharField(db_column='COPrincipalPerformance', max_length=2)  # Field name made lowercase.
    # okspryrsexpoutstate = models.IntegerField(db_column='OKSPRYrsExpOutState')  # Field name made lowercase.
    # okspryrsexpmilitary = models.IntegerField(db_column='OKSPRYrsExpMilitary')  # Field name made lowercase.
    # okspryrsexpinstate = models.IntegerField(db_column='OKSPRYrsExpInState')  # Field name made lowercase.
    # okspryrsexpdistrict = models.IntegerField(db_column='OKSPRYrsExpDistrict')  # Field name made lowercase.
    # oktrsyrsexp = models.IntegerField(db_column='OKTRSYrsExp')  # Field name made lowercase.
    # smoker = models.BooleanField(db_column='Smoker')  # Field name made lowercase.
    # benefitseligenddate = models.DateTimeField(db_column='BenefitsEligEndDate', blank=True, null=True)  # Field name made lowercase.
    # oksprretired = models.CharField(db_column='OKSPRRetired', max_length=1)  # Field name made lowercase.
    # oksprresidency = models.CharField(db_column='OKSPRResidency', max_length=1)  # Field name made lowercase.
    # oksprmentor = models.CharField(db_column='OKSPRMentor', max_length=1)  # Field name made lowercase.
    # prethnicorigin = models.CharField(db_column='PREthnicOrigin', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # uniquename = models.CharField(db_column='UniqueName', max_length=110)  # Field name made lowercase.
    # termstatecode = models.CharField(db_column='TermStateCode', max_length=10)  # Field name made lowercase.
    # nmyrsexpteachindist = models.FloatField(db_column='NMYrsExpTeachInDist')  # Field name made lowercase.
    # nmyrsexpteachoutdist = models.FloatField(db_column='NMYrsExpTeachOutDist')  # Field name made lowercase.
    # nmyrsexpprinindist = models.FloatField(db_column='NMYrsExpPrinInDist')  # Field name made lowercase.
    # nmyrsexpprinoutdist = models.FloatField(db_column='NMYrsExpPrinOutDist')  # Field name made lowercase.
    # nmyrsexpteachtotal = models.FloatField(db_column='NMYrsExpTeachTotal')  # Field name made lowercase.
    # nmyrsexpprintotal = models.FloatField(db_column='NMYrsExpPrinTotal')  # Field name made lowercase.
    # bargainingunit = models.CharField(db_column='BargainingUnit', max_length=20)  # Field name made lowercase.
    # unioncode = models.CharField(db_column='UnionCode', max_length=20)  # Field name made lowercase.
    # tblprmasterbargainingunitid = models.IntegerField(db_column='tblPRMasterBargainingUnitID')  # Field name made lowercase.
    # tblprmasterunioncodeid = models.IntegerField(db_column='tblPRMasterUnionCodeID')  # Field name made lowercase.
    # ileisexcludefromeis = models.BooleanField(db_column='ILEISExcludeFromEIS')  # Field name made lowercase.
    # ileisretired = models.BooleanField(db_column='ILEISRetired')  # Field name made lowercase.
    # gashbpeligible = models.BooleanField(db_column='GASHBPEligible')  # Field name made lowercase.
    # reimbursementrequests = models.BooleanField(db_column='ReimbursementRequests')  # Field name made lowercase.
    # gashbpweeklyhours = models.FloatField(db_column='GASHBPWeeklyHours')  # Field name made lowercase.
    # classificationtype = models.CharField(db_column='ClassificationType', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # wyrainid = models.CharField(db_column='WYRAINID', max_length=15)  # Field name made lowercase.
    # retired = models.BooleanField(db_column='Retired')  # Field name made lowercase.
    # idexcludefromisee = models.BooleanField(db_column='IDExcludeFromISEE')  # Field name made lowercase.
    # idyrsexpindist = models.IntegerField(db_column='IDYrsExpInDist')  # Field name made lowercase.
    # idyrsexpinstate = models.IntegerField(db_column='IDYrsExpInState')  # Field name made lowercase.
    # idyrsexpoutstate = models.IntegerField(db_column='IDYrsExpOutState')  # Field name made lowercase.
    # idyrsexpnonpublic = models.IntegerField(db_column='IDYrsExpNonPublic')  # Field name made lowercase.
    # idyrsexphigheredinstate = models.IntegerField(db_column='IDYrsExpHigherEdInState')  # Field name made lowercase.
    # idyrsexphigheredoutstate = models.IntegerField(db_column='IDYrsExpHigherEdOutState')  # Field name made lowercase.
    # idpara = models.BooleanField(db_column='IDPara')  # Field name made lowercase.
    # idtitleipara = models.BooleanField(db_column='IDTitleIPara')  # Field name made lowercase.
    # personalemail = models.CharField(db_column='PersonalEmail', max_length=255)  # Field name made lowercase.
    # preferredemail = models.IntegerField(db_column='PreferredEmail')  # Field name made lowercase.
    # email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # preferredemailtext = models.CharField(db_column='PreferredEmailText', max_length=22)  # Field name made lowercase.
    # coteachquality1 = models.CharField(db_column='COTeachQuality1', max_length=2)  # Field name made lowercase.
    # coteachquality2 = models.CharField(db_column='COTeachQuality2', max_length=2)  # Field name made lowercase.
    # coteachquality3 = models.CharField(db_column='COTeachQuality3', max_length=2)  # Field name made lowercase.
    # coteachquality4 = models.CharField(db_column='COTeachQuality4', max_length=2)  # Field name made lowercase.
    # coteachquality5 = models.CharField(db_column='COTeachQuality5', max_length=2)  # Field name made lowercase.
    # coteachquality6 = models.CharField(db_column='COTeachQuality6', max_length=2)  # Field name made lowercase.
    # coprinquality2 = models.CharField(db_column='COPrinQuality2', max_length=2)  # Field name made lowercase.
    # coprinquality1 = models.CharField(db_column='COPrinQuality1', max_length=2)  # Field name made lowercase.
    # coprinquality3 = models.CharField(db_column='COPrinQuality3', max_length=2)  # Field name made lowercase.
    # coprinquality4 = models.CharField(db_column='COPrinQuality4', max_length=2)  # Field name made lowercase.
    # coprinquality5 = models.CharField(db_column='COPrinQuality5', max_length=2)  # Field name made lowercase.
    # coprinquality6 = models.CharField(db_column='COPrinQuality6', max_length=2)  # Field name made lowercase.
    # coprinquality7 = models.CharField(db_column='COPrinQuality7', max_length=2)  # Field name made lowercase.
    # gaplanparticipation = models.CharField(db_column='GAPlanParticipation', max_length=50)  # Field name made lowercase.
    # gaemployeetype = models.CharField(db_column='GAEmployeeType', max_length=50)  # Field name made lowercase.
    # acastatus = models.CharField(db_column='ACAStatus', max_length=50)  # Field name made lowercase.
    # nyethnicity2 = models.IntegerField(db_column='NYEthnicity2')  # Field name made lowercase.
    # nyethnicity3 = models.IntegerField(db_column='NYEthnicity3')  # Field name made lowercase.
    # nyethnicity4 = models.IntegerField(db_column='NYEthnicity4')  # Field name made lowercase.
    # nyethnicity5 = models.IntegerField(db_column='NYEthnicity5')  # Field name made lowercase.
    # nyprofessionaldevelopment = models.CharField(db_column='NYProfessionalDevelopment', max_length=2)  # Field name made lowercase.
    # nyprincipalhiredate = models.DateTimeField(db_column='NYPrincipalHireDate', blank=True, null=True)  # Field name made lowercase.
    # exporttosis = models.BooleanField(db_column='ExporttoSIS')  # Field name made lowercase.
    # neprimarysubjectarea = models.CharField(db_column='NEPrimarySubjectArea', max_length=2)  # Field name made lowercase.
    # privateemployee = models.BooleanField(db_column='PrivateEmployee')  # Field name made lowercase.
    # temporaryprivateemployee = models.BooleanField(db_column='TemporaryPrivateEmployee')  # Field name made lowercase.
    # nystaffsnapshot = models.CharField(db_column='NYStaffSnapshot', max_length=50)  # Field name made lowercase.
    # coeducatorprepprogram = models.CharField(db_column='COEducatorPrepProgram', max_length=5)  # Field name made lowercase.
    # azemptype = models.SmallIntegerField(db_column='AZEmpType')  # Field name made lowercase.
    # gaprcjobclassification = models.CharField(db_column='GAPRCJobClassification', max_length=5)  # Field name made lowercase.
    # gaprcjobstatus = models.CharField(db_column='GAPRCJobStatus', max_length=1)  # Field name made lowercase.
    # gaprcnoenrollmentreason = models.CharField(db_column='GAPRCNoEnrollmentReason', max_length=5)  # Field name made lowercase.
    # akhiredforspecialed = models.CharField(db_column='AKHiredForSpecialEd', max_length=1)  # Field name made lowercase.
    # aktitleihiredate = models.DateTimeField(db_column='AKTitleIHireDate', blank=True, null=True)  # Field name made lowercase.
    # aktitleihsdiploma = models.CharField(db_column='AKTitleIHSDiploma', max_length=1)  # Field name made lowercase.
    # akspedaide = models.CharField(db_column='AKSPEDAide', max_length=1)  # Field name made lowercase.
    # akspedaide3_5 = models.CharField(db_column='AKSPEDAide3_5', max_length=1)  # Field name made lowercase.
    # akminquals = models.CharField(db_column='AKMinQuals', max_length=1)  # Field name made lowercase.
    # aklimitedcertificate = models.CharField(db_column='AKLimitedCertificate', max_length=1)  # Field name made lowercase.
    # aknewtostate = models.CharField(db_column='AKNewToState', max_length=1)  # Field name made lowercase.
    # aknewtoprofession = models.CharField(db_column='AKNewToProfession', max_length=1)  # Field name made lowercase.
    # aklongtermsub = models.CharField(db_column='AKLongTermSub', max_length=1)  # Field name made lowercase.
    # akhighlyqualified = models.CharField(db_column='AKHighlyQualified', max_length=1)  # Field name made lowercase.
    # akhqmethod = models.CharField(db_column='AKHQMethod', max_length=1)  # Field name made lowercase.
    # aknothqreason = models.CharField(db_column='AKNotHQReason', max_length=2)  # Field name made lowercase.
    # aknothqplan = models.CharField(db_column='AKNotHQPlan', max_length=2)  # Field name made lowercase.
    # akhiredforsped = models.CharField(db_column='AKHiredForSPED', max_length=1)  # Field name made lowercase.
    # printw2 = models.BooleanField(db_column='PrintW2')  # Field name made lowercase.
    # acaofferinggroup = models.CharField(db_column='ACAOfferingGroup', max_length=25)  # Field name made lowercase.
    # papimsstafftype = models.CharField(db_column='PAPIMSStaffType', max_length=50)  # Field name made lowercase.
    # papimsempstatus = models.CharField(db_column='PAPIMSEmpStatus', max_length=10)  # Field name made lowercase.
    # meseasonal = models.BooleanField(db_column='MESeasonal')  # Field name made lowercase.
    # gaaca = models.BooleanField(db_column='GAACA')  # Field name made lowercase.
    # idincludeoniseeform8 = models.BooleanField(db_column='IDIncludeOnISEEForm8')  # Field name made lowercase.
    # iddateoflastk12exp = models.CharField(db_column='IDDateOfLastK12Exp', max_length=9)  # Field name made lowercase.
    # idplaceoflastk12exp = models.CharField(db_column='IDPlaceOfLastK12Exp', max_length=2)  # Field name made lowercase.
    # idprofperfcriteriamet = models.BooleanField(db_column='IDProfPerfCriteriaMet')  # Field name made lowercase.
    # riedattend = models.CharField(db_column='RIEdAttend', max_length=1)  # Field name made lowercase.
    # nyitinerantteacher = models.BooleanField(db_column='NYItinerantTeacher')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'viwPREmployees'


class Viwprpositions(VisionsModel):
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.
    positionid = models.CharField(db_column='PositionID', max_length=25)  # Field name made lowercase.
    # tblapreqlocationsid = models.IntegerField(db_column='tblAPReqLocationsID')  # Field name made lowercase.
    dac = models.CharField(db_column='DAC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tblprdacbudgetedpositionsid = models.IntegerField(db_column='tblPRDACBudgetedPositionsID')  # Field name made lowercase.
    postype = models.CharField(db_column='PosType', max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50)  # Field name made lowercase.
    # positionftes = models.FloatField(db_column='PositionFTEs')  # Field name made lowercase.
    # budgetamt = models.DecimalField(db_column='BudgetAmt', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # schedule = models.CharField(db_column='Schedule', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # workcalendar = models.CharField(db_column='WorkCalendar', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # tblprmastersalaryschedulecellsid = models.IntegerField(db_column='tblPRMasterSalaryScheduleCellsID')  # Field name made lowercase.
    # tblprworkcalendarsid = models.IntegerField(db_column='tblPRWorkCalendarsID', blank=True, null=True)  # Field name made lowercase.
    # concurrencyid = models.IntegerField(db_column='ConcurrencyID')  # Field name made lowercase.
    # status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    # employeeid = models.CharField(db_column='EmployeeID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=99, blank=True, null=True)  # Field name made lowercase.
    # employeessn = models.CharField(db_column='EmployeeSSN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    # tblpremployeesid = models.IntegerField(db_column='tblPREmployeesID')  # Field name made lowercase.
    # prioryearamt = models.DecimalField(db_column='PriorYearAmt', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # classification = models.SmallIntegerField(db_column='Classification')  # Field name made lowercase.
    # paymethod = models.SmallIntegerField(db_column='PayMethod')  # Field name made lowercase.
    # paybasis = models.SmallIntegerField(db_column='PayBasis')  # Field name made lowercase.
    # rate = models.DecimalField(db_column='Rate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # hrsday = models.FloatField(db_column='HrsDay')  # Field name made lowercase.
    # isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    # startdate = models.DateTimeField(db_column='StartDate')  # Field name made lowercase.
    # enddate = models.DateTimeField(db_column='EndDate')  # Field name made lowercase.
    # positiondays = models.FloatField(db_column='PositionDays')  # Field name made lowercase.
    # positionamount = models.DecimalField(db_column='PositionAmount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # statecode = models.CharField(db_column='StateCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # sderpcode = models.CharField(db_column='SDERPCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    # classcode = models.CharField(db_column='ClassCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # category = models.CharField(db_column='Category', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # tblprpositioncategoryid = models.IntegerField(db_column='tblPRPositionCategoryID')  # Field name made lowercase.
    # tblprmasterpositioncodesid = models.IntegerField(db_column='tblPRMasterPositionCodesID')  # Field name made lowercase.
    # tblprmasterworkerscompclasscodesid = models.IntegerField(db_column='tblPRMasterWorkersCompClassCodesID')  # Field name made lowercase.
    # leaveaccrualfactor = models.FloatField(db_column='LeaveAccrualFactor')  # Field name made lowercase.
    # salaryscheduletype = models.SmallIntegerField(db_column='SalaryScheduleType')  # Field name made lowercase.
    # nextyearsalaryschedulecellsid = models.IntegerField(db_column='NextYearSalaryScheduleCellsID')  # Field name made lowercase.
    # nextyearrow = models.SmallIntegerField(db_column='NextYearRow', blank=True, null=True)  # Field name made lowercase.
    # nextyearcol = models.SmallIntegerField(db_column='NextYearCol', blank=True, null=True)  # Field name made lowercase.
    # nextyearscheduleamt = models.DecimalField(db_column='NextYearScheduleAmt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    # projection = models.CharField(db_column='Projection', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # nextyearscheduletype = models.SmallIntegerField(db_column='NextYearScheduleType', blank=True, null=True)  # Field name made lowercase.
    # salaryschedulerow = models.SmallIntegerField(db_column='SalaryScheduleRow', blank=True, null=True)  # Field name made lowercase.
    # salaryschedulecol = models.SmallIntegerField(db_column='SalaryScheduleCol', blank=True, null=True)  # Field name made lowercase.
    # salaryscheduleamt = models.DecimalField(db_column='SalaryScheduleAmt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    # nextyearamt = models.DecimalField(db_column='NextYearAmt', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # nextyearrate = models.DecimalField(db_column='NextYearRate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # nextyearfte = models.FloatField(db_column='NextYearFTE')  # Field name made lowercase.
    # numberfilled = models.IntegerField(db_column='NumberFilled')  # Field name made lowercase.
    # positionrankingid = models.IntegerField(db_column='PositionRankingID')  # Field name made lowercase.
    # positionrankingtype = models.CharField(db_column='PositionRankingType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # tblhrmastercontractsid = models.IntegerField(db_column='tblHRMasterContractsID')  # Field name made lowercase.
    # contractname = models.CharField(db_column='ContractName', max_length=100)  # Field name made lowercase.
    # type = models.CharField(db_column='Type', max_length=100)  # Field name made lowercase.
    # supervisorid = models.IntegerField(db_column='SupervisorID')  # Field name made lowercase.
    # nextevaluationdate = models.DateTimeField(db_column='NextEvaluationDate', blank=True, null=True)  # Field name made lowercase.
    # fundingstatus = models.CharField(db_column='FundingStatus', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # tblhrmasterdepartmentsid = models.IntegerField(db_column='tblHRMasterDepartmentsID')  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=25)  # Field name made lowercase.
    # paycycle = models.CharField(db_column='PayCycle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # assignmentstatus = models.CharField(db_column='AssignmentStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # trscategorydescription = models.CharField(db_column='TRSCategoryDescription', max_length=50)  # Field name made lowercase.
    # trscategory = models.CharField(db_column='TRSCategory', max_length=2)  # Field name made lowercase.
    # trspayunit = models.SmallIntegerField(db_column='TRSPayUnit')  # Field name made lowercase.
    # trsyearroundtflg = models.SmallIntegerField(db_column='TRSYearRoundTFlg')  # Field name made lowercase.
    # trsnonstdconflg = models.SmallIntegerField(db_column='TRSNonStdConFlg')  # Field name made lowercase.
    # startpayperiod = models.FloatField(db_column='StartPayPeriod')  # Field name made lowercase.
    # endpayperiod = models.FloatField(db_column='EndPayPeriod')  # Field name made lowercase.
    # tblprpayperiodsid_startpayperiod = models.IntegerField(db_column='tblPRPayPeriodsID_StartPayPeriod')  # Field name made lowercase.
    # tblprpayperiodsid_endpayperiod = models.IntegerField(db_column='tblPRPayPeriodsID_EndPayPeriod')  # Field name made lowercase.
    # schoolcode = models.CharField(db_column='SchoolCode', max_length=25)  # Field name made lowercase.
    # employeeaddress1 = models.CharField(db_column='EmployeeAddress1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    # employeeaddress2 = models.CharField(db_column='EmployeeAddress2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    # employeecity = models.CharField(db_column='EmployeeCity', max_length=30, blank=True, null=True)  # Field name made lowercase.
    # employeestate = models.CharField(db_column='EmployeeState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    # employeezipcode = models.CharField(db_column='EmployeeZipCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    # departmentdescription = models.CharField(db_column='DepartmentDescription', max_length=75, blank=True, null=True)  # Field name made lowercase.
    # departmentid = models.SmallIntegerField(db_column='DepartmentID', blank=True, null=True)  # Field name made lowercase.
    # excludefromads = models.BooleanField(db_column='ExcludeFromADS')  # Field name made lowercase.
    # useremployeeid = models.CharField(db_column='UserEmployeeID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # readytogenerate = models.NullBooleanField(db_column='ReadyToGenerate')  # Field name made lowercase.
    # recordtype = models.CharField(db_column='RecordType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # lumpsumperiods = models.FloatField(db_column='LumpSumPeriods', blank=True, null=True)  # Field name made lowercase.
    # issuepaycheck = models.NullBooleanField(db_column='IssuePayCheck')  # Field name made lowercase.
    # sdergradelevel = models.CharField(db_column='SDERGradeLevel', max_length=50)  # Field name made lowercase.
    # dailyamount = models.FloatField(db_column='DailyAmount', blank=True, null=True)  # Field name made lowercase.
    # paybasisstring = models.CharField(db_column='PayBasisString', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # paymethodstring = models.CharField(db_column='PayMethodString', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # distributiontype = models.SmallIntegerField(db_column='DistributionType', blank=True, null=True)  # Field name made lowercase.
    # jobtitle = models.CharField(db_column='JobTitle', max_length=25)  # Field name made lowercase.
    # contractadjustment = models.DecimalField(db_column='ContractAdjustment', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # nvperscontractdate = models.BooleanField(db_column='NVPERSContractDate')  # Field name made lowercase.
    # nvpersparttime = models.BooleanField(db_column='NVPERSPartTime')  # Field name made lowercase.
    # mthourstype = models.CharField(db_column='MTHoursType', max_length=50)  # Field name made lowercase.
    # mtearningstype = models.CharField(db_column='MTEarningsType', max_length=50)  # Field name made lowercase.
    # issuepaychecktext = models.CharField(db_column='IssuePayCheckText', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # nyemploymentbase = models.IntegerField(db_column='NYEmploymentBase')  # Field name made lowercase.
    # nypayrate = models.DecimalField(db_column='NYPayRate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # nypositiontype = models.IntegerField(db_column='NYPositionType')  # Field name made lowercase.
    # nyindicator = models.IntegerField(db_column='NYIndicator')  # Field name made lowercase.
    # tblprnybasehoursid = models.IntegerField(db_column='tblPRNYBaseHoursID')  # Field name made lowercase.
    # nybasehourscode = models.CharField(db_column='NYBaseHoursCode', max_length=50)  # Field name made lowercase.
    # nyretro = models.IntegerField(db_column='NYRetro')  # Field name made lowercase.
    # nyretroyear = models.IntegerField(db_column='NYRetroYear')  # Field name made lowercase.
    # rowhead = models.CharField(db_column='RowHead', max_length=50)  # Field name made lowercase.
    # colhead = models.CharField(db_column='ColHead', max_length=50)  # Field name made lowercase.
    # rowheadny = models.CharField(db_column='RowHeadNY', max_length=50)  # Field name made lowercase.
    # colheadny = models.CharField(db_column='ColHeadNY', max_length=50)  # Field name made lowercase.
    # paemploymenttype = models.CharField(db_column='PAEmploymentType', max_length=2)  # Field name made lowercase.
    # pawagetype = models.CharField(db_column='PAWageType', max_length=2)  # Field name made lowercase.
    # tblprpaworkstatusid = models.IntegerField(db_column='tblPRPAWorkStatusID')  # Field name made lowercase.
    # paworkstatuscode = models.CharField(db_column='PAWorkStatusCode', max_length=6)  # Field name made lowercase.
    # paworkstatusdescription = models.CharField(db_column='PAWorkStatusDescription', max_length=50)  # Field name made lowercase.
    # paworkstatusstartdate = models.DateTimeField(db_column='PAWorkStatusStartDate', blank=True, null=True)  # Field name made lowercase.
    # paworkstatusenddate = models.DateTimeField(db_column='PAWorkStatusEndDate', blank=True, null=True)  # Field name made lowercase.
    # paexpectedmonths = models.CharField(db_column='PAExpectedMonths', max_length=2)  # Field name made lowercase.
    # paexpectedunits = models.CharField(db_column='PAExpectedUnits', max_length=4)  # Field name made lowercase.
    # pavotingstatus = models.CharField(db_column='PAVotingStatus', max_length=1)  # Field name made lowercase.
    # pabocflag = models.CharField(db_column='PABocFlag', max_length=1)  # Field name made lowercase.
    # paoutstandingcredit = models.CharField(db_column='PAOutstandingCredit', max_length=1)  # Field name made lowercase.
    # pabocsvcenddate = models.DateTimeField(db_column='PABocSvcEndDate', blank=True, null=True)  # Field name made lowercase.
    # classificationtext = models.CharField(db_column='ClassificationText', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # orreportablehours = models.FloatField(db_column='ORReportableHours', blank=True, null=True)  # Field name made lowercase.
    # orperspaytype = models.CharField(db_column='ORPERSPayType', max_length=50)  # Field name made lowercase.
    # tblprstatusid = models.IntegerField(db_column='tblPRStatusID', blank=True, null=True)  # Field name made lowercase.
    # employeestatus = models.CharField(db_column='EmployeeStatus', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # pareportannually = models.BooleanField(db_column='PAReportAnnually')  # Field name made lowercase.
    # orperswagecode = models.CharField(db_column='ORPERSWageCode', max_length=2)  # Field name made lowercase.
    # nycivilservice = models.BooleanField(db_column='NYCivilService')  # Field name made lowercase.
    # txpopcode = models.CharField(db_column='TXPopCode', max_length=2)  # Field name made lowercase.
    # txactivitycode = models.CharField(db_column='TXActivityCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    # txservicecode = models.CharField(db_column='TXServiceCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    # maskssn = models.CharField(db_column='MaskSSN', max_length=11, blank=True, null=True)  # Field name made lowercase.
    # positiontype = models.CharField(db_column='PositionType', max_length=50)  # Field name made lowercase.
    # issubstitute = models.NullBooleanField(db_column='IsSubstitute')  # Field name made lowercase.
    # insuranceclass = models.CharField(db_column='InsuranceClass', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # tblprpositiontypesid = models.IntegerField(db_column='tblPRPositionTypesID')  # Field name made lowercase.
    # supervisor = models.CharField(db_column='Supervisor', max_length=99, blank=True, null=True)  # Field name made lowercase.
    # amountftd = models.DecimalField(db_column='AmountFTD', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # nmperawagecode = models.CharField(db_column='NMPERAWageCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    # nmperaexcludedreason = models.CharField(db_column='NMPERAExcludedReason', max_length=2, blank=True, null=True)  # Field name made lowercase.
    # tblhpparapprovaltemplateid = models.IntegerField(db_column='tblHPPARApprovalTemplateID', blank=True, null=True)  # Field name made lowercase.
    # templatename = models.CharField(db_column='TemplateName', max_length=25)  # Field name made lowercase.
    # employeeclassification = models.CharField(db_column='EmployeeClassification', max_length=15, blank=True, null=True)  # Field name made lowercase.
    # excludedretro = models.DecimalField(db_column='ExcludedRetro', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # onetimepay = models.BooleanField(db_column='OneTimePay')  # Field name made lowercase.
    # tblprempleaveplansid = models.IntegerField(db_column='tblPREmpLeavePlansID')  # Field name made lowercase.
    # leaveplan = models.CharField(db_column='LeavePlan', max_length=45)  # Field name made lowercase.
    # workcalendarname = models.CharField(db_column='WorkCalendarName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # nynonabs = models.BooleanField(db_column='NYNonABS')  # Field name made lowercase.
    # expr1 = models.CharField(db_column='Expr1', max_length=99, blank=True, null=True)  # Field name made lowercase.
    # autostep = models.BooleanField(db_column='AutoStep')  # Field name made lowercase.
    # tblprmastersalaryscheduleid = models.IntegerField(db_column='tblPRMasterSalaryScheduleID', blank=True, null=True)  # Field name made lowercase.
    # ndrateclassification = models.CharField(db_column='NDRateClassification', max_length=255)  # Field name made lowercase.
    # scheduledays = models.IntegerField(db_column='ScheduleDays')  # Field name made lowercase.
    # comments = models.TextField(db_column='Comments')  # Field name made lowercase. This field type is a guess.
    # nextyearscheduledays = models.IntegerField(db_column='NextYearScheduleDays')  # Field name made lowercase.
    # scheduleny = models.CharField(db_column='ScheduleNY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # archive = models.NullBooleanField(db_column='Archive')  # Field name made lowercase.
    # desctype = models.CharField(db_column='DescType', max_length=151, blank=True, null=True)  # Field name made lowercase.
    # assignedbyhr = models.IntegerField(db_column='AssignedByHR', blank=True, null=True)  # Field name made lowercase.
    # excludeinsurance = models.BooleanField(db_column='ExcludeInsurance')  # Field name made lowercase.
    # excludefromuc = models.BooleanField(db_column='ExcludeFromUC')  # Field name made lowercase.
    # papimsreportable = models.BooleanField(db_column='PAPIMSReportable')  # Field name made lowercase.
    # workdays = models.FloatField(db_column='WorkDays', blank=True, null=True)  # Field name made lowercase.
    # tcip = models.BooleanField(db_column='TCIP')  # Field name made lowercase.
    # tcijob = models.BigIntegerField(db_column='TCIJob')  # Field name made lowercase.
    # tcidept = models.IntegerField(db_column='TCIDept')  # Field name made lowercase.
    # supplementaltemplateid = models.IntegerField(db_column='SupplementalTemplateID')  # Field name made lowercase.
    # papsersprioryear = models.BooleanField(db_column='PAPSERSPriorYear')  # Field name made lowercase.
    # advancedate = models.DateTimeField(db_column='AdvanceDate', blank=True, null=True)  # Field name made lowercase.
    # tblprpositionsid = models.IntegerField(db_column='tblPRPositionsID')  # Field name made lowercase.
    # coyrsprincipalschool = models.IntegerField(db_column='COYrsPrincipalSchool')  # Field name made lowercase.
    # coclassesinsubject = models.IntegerField(db_column='COClassesInSubject')  # Field name made lowercase.
    # cotwentyfoursemesterhours = models.CharField(db_column='COTwentyFourSemesterHours', max_length=50)  # Field name made lowercase.
    # cogradelevelinfant = models.BooleanField(db_column='COGradeLevelInfant')  # Field name made lowercase.
    # cogradelevelprek = models.BooleanField(db_column='COGradeLevelPreK')  # Field name made lowercase.
    # cogradelevelk = models.BooleanField(db_column='COGradeLevelK')  # Field name made lowercase.
    # cogradelevel1 = models.BooleanField(db_column='COGradeLevel1')  # Field name made lowercase.
    # cogradelevel2 = models.BooleanField(db_column='COGradeLevel2')  # Field name made lowercase.
    # cogradelevel3 = models.BooleanField(db_column='COGradeLevel3')  # Field name made lowercase.
    # cogradelevel4 = models.BooleanField(db_column='COGradeLevel4')  # Field name made lowercase.
    # cogradelevel5 = models.BooleanField(db_column='COGradeLevel5')  # Field name made lowercase.
    # cogradelevel6 = models.BooleanField(db_column='COGradeLevel6')  # Field name made lowercase.
    # cogradelevel7 = models.BooleanField(db_column='COGradeLevel7')  # Field name made lowercase.
    # cogradelevel8 = models.BooleanField(db_column='COGradeLevel8')  # Field name made lowercase.
    # cogradelevel9 = models.BooleanField(db_column='COGradeLevel9')  # Field name made lowercase.
    # cogradelevel10 = models.BooleanField(db_column='COGradeLevel10')  # Field name made lowercase.
    # cogradelevel11 = models.BooleanField(db_column='COGradeLevel11')  # Field name made lowercase.
    # cogradelevel12 = models.BooleanField(db_column='COGradeLevel12')  # Field name made lowercase.
    # cogradelevelpg = models.BooleanField(db_column='COGradeLevelPG')  # Field name made lowercase.
    # excludefromcde = models.BooleanField(db_column='ExcludeFromCDE')  # Field name made lowercase.
    # coempstatuscode = models.CharField(db_column='COEmpStatusCode', max_length=50)  # Field name made lowercase.
    # coadminareacode = models.CharField(db_column='COAdminAreaCode', max_length=50)  # Field name made lowercase.
    # coteachingsubjectcode = models.CharField(db_column='COTeachingSubjectCode', max_length=50)  # Field name made lowercase.
    # hourlytcpreenc = models.DecimalField(db_column='HourlyTCPreEnc', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # tblcajobclassid = models.IntegerField(db_column='tblCAJobClassID')  # Field name made lowercase.
    # tblcabargainingunitid = models.IntegerField(db_column='tblCABargainingUnitID')  # Field name made lowercase.
    # seniority = models.BooleanField(db_column='Seniority')  # Field name made lowercase.
    # rollintoid = models.IntegerField(db_column='RollIntoID')  # Field name made lowercase.
    # latestfilled = models.IntegerField(db_column='LatestFilled')  # Field name made lowercase.
    # cacountyid = models.CharField(db_column='CACountyID', max_length=25)  # Field name made lowercase.
    # tblhrevaluationgroupid = models.IntegerField(db_column='tblHREvaluationGroupID')  # Field name made lowercase.
    # evaluationgroup = models.CharField(db_column='EvaluationGroup', max_length=50)  # Field name made lowercase.
    # tblnvhqtcodesid = models.IntegerField(db_column='tblNVHQTCodesID', blank=True, null=True)  # Field name made lowercase.
    # basedonid = models.IntegerField(db_column='BasedOnID')  # Field name made lowercase.
    # pctofpos = models.FloatField(db_column='PctOfPos')  # Field name made lowercase.
    # imputedincome = models.BooleanField(db_column='ImputedIncome')  # Field name made lowercase.
    # hasdocs = models.CharField(db_column='HasDocs', max_length=3)  # Field name made lowercase.
    # vacancystatus = models.CharField(db_column='VacancyStatus', max_length=6)  # Field name made lowercase.
    hqtcode = models.CharField(db_column='HQTCode', max_length=2)  # Field name made lowercase.
    # illowestgrade = models.CharField(db_column='ILLowestGrade', max_length=2, blank=True, null=True)  # Field name made lowercase.
    # ilhighestgrade = models.CharField(db_column='ILHighestGrade', max_length=2, blank=True, null=True)  # Field name made lowercase.
    # ilpaidwithtitlei = models.CharField(db_column='ILPaidWithTitleI', max_length=2)  # Field name made lowercase.
    # ilteachassignment1 = models.CharField(db_column='ILTeachAssignment1', max_length=3, blank=True, null=True)  # Field name made lowercase.
    # ilteachassignment2 = models.CharField(db_column='ILTeachAssignment2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    # ilteachassignment3 = models.CharField(db_column='ILTeachAssignment3', max_length=3, blank=True, null=True)  # Field name made lowercase.
    # ilteachassignment4 = models.CharField(db_column='ILTeachAssignment4', max_length=3, blank=True, null=True)  # Field name made lowercase.
    # ilteachassignment7 = models.CharField(db_column='ILTeachAssignment7', max_length=3, blank=True, null=True)  # Field name made lowercase.
    # ilteachassignment6 = models.CharField(db_column='ILTeachAssignment6', max_length=3, blank=True, null=True)  # Field name made lowercase.
    # ilteachassignment5 = models.CharField(db_column='ILTeachAssignment5', max_length=3, blank=True, null=True)  # Field name made lowercase.
    # ilclassestaught1 = models.SmallIntegerField(db_column='ILClassesTaught1', blank=True, null=True)  # Field name made lowercase.
    # ilclassestaught2 = models.SmallIntegerField(db_column='ILClassesTaught2', blank=True, null=True)  # Field name made lowercase.
    # ilclassestaught3 = models.SmallIntegerField(db_column='ILClassesTaught3', blank=True, null=True)  # Field name made lowercase.
    # ilclassestaught4 = models.SmallIntegerField(db_column='ILClassesTaught4', blank=True, null=True)  # Field name made lowercase.
    # ilclassestaught5 = models.SmallIntegerField(db_column='ILClassesTaught5', blank=True, null=True)  # Field name made lowercase.
    # ilclassestaught6 = models.SmallIntegerField(db_column='ILClassesTaught6', blank=True, null=True)  # Field name made lowercase.
    # ilclassestaught7 = models.SmallIntegerField(db_column='ILClassesTaught7', blank=True, null=True)  # Field name made lowercase.
    # postemplatename = models.CharField(db_column='PosTemplateName', max_length=50)  # Field name made lowercase.
    # tblglpositionbudgettemplateid = models.IntegerField(db_column='tblGLPositionBudgetTemplateID')  # Field name made lowercase.
    # orexpertype = models.CharField(db_column='ORExperType', max_length=20)  # Field name made lowercase.
    # orpositiontype = models.CharField(db_column='ORPositionType', max_length=30)  # Field name made lowercase.
    # neexcludefromnssrs = models.BooleanField(db_column='NEExcludeFromNSSRS')  # Field name made lowercase.
    # nesalarytype = models.IntegerField(db_column='NESalaryType')  # Field name made lowercase.
    # dailyrate = models.DecimalField(db_column='DailyRate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # periodicrate = models.DecimalField(db_column='PeriodicRate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # nextyeardailyrate = models.DecimalField(db_column='NextYearDailyRate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # nextyearperiodicrate = models.DecimalField(db_column='NextYearPeriodicRate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # tblcapaymatrixid = models.IntegerField(db_column='tblCAPayMatrixID')  # Field name made lowercase.
    # zeropay = models.BooleanField(db_column='ZeroPay')  # Field name made lowercase.
    # expr2 = models.BooleanField(db_column='Expr2')  # Field name made lowercase.
    # nmhd = models.CharField(db_column='NMHD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    # workedperiods = models.IntegerField(db_column='WorkedPeriods', blank=True, null=True)  # Field name made lowercase.
    # paidperiods = models.IntegerField(db_column='PaidPeriods', blank=True, null=True)  # Field name made lowercase.
    # was275adjust = models.NullBooleanField(db_column='WAS275Adjust')  # Field name made lowercase.
    # was275exclude = models.NullBooleanField(db_column='WAS275Exclude')  # Field name made lowercase.
    # was275report = models.NullBooleanField(db_column='WAS275Report')  # Field name made lowercase.
    # tblprwagradegroupid = models.IntegerField(db_column='tblPRWAGradeGroupID', blank=True, null=True)  # Field name made lowercase.
    # baserate = models.DecimalField(db_column='BaseRate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # tbliabedspaytypesid = models.IntegerField(db_column='tblIABEDSPayTypesID')  # Field name made lowercase.
    # tblprpaycyclesid = models.IntegerField(db_column='tblPRPayCyclesID', blank=True, null=True)  # Field name made lowercase.
    # nmstatus = models.CharField(db_column='NMStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    # iddescription = models.CharField(db_column='IDDescription', max_length=81, blank=True, null=True)  # Field name made lowercase.
    # mtcontracttype = models.CharField(db_column='MTContractType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    # mtpositiontype = models.CharField(db_column='MTPositionType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    # mtextrapaytype = models.CharField(db_column='MTExtraPayType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # mttcsreportable = models.CharField(db_column='MTTCSReportable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    # mtteacherduty = models.CharField(db_column='MTTeacherDuty', max_length=3, blank=True, null=True)  # Field name made lowercase.
    # compositeratefactor = models.FloatField(db_column='CompositeRateFactor')  # Field name made lowercase.
    # exemptcompositerate = models.BooleanField(db_column='ExemptCompositeRate')  # Field name made lowercase.
    # otfactor = models.FloatField(db_column='OTFactor')  # Field name made lowercase.
    # workcalendarstartdate = models.DateTimeField(db_column='WorkCalendarStartDate', blank=True, null=True)  # Field name made lowercase.
    # workcalendarenddate = models.DateTimeField(db_column='WorkCalendarEndDate', blank=True, null=True)  # Field name made lowercase.
    # accountmask = models.CharField(db_column='AccountMask', max_length=100)  # Field name made lowercase.
    # salaryschedulefullannual = models.BooleanField(db_column='SalaryScheduleFullAnnual')  # Field name made lowercase.
    # parid = models.IntegerField(db_column='PARID', blank=True, null=True)  # Field name made lowercase.
    # tblnyersreportcodesid = models.IntegerField(db_column='tblNYERSReportCodesID')  # Field name made lowercase.
    # mttrsfte = models.FloatField(db_column='MTTRSFTE', blank=True, null=True)  # Field name made lowercase.
    # nyersreportcode = models.CharField(db_column='NYERSReportCode', max_length=5, blank=True, null=True)  # Field name made lowercase.
    # lastname = models.CharField(db_column='LastName', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # firstname = models.CharField(db_column='FirstName', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # middlename = models.CharField(db_column='MiddleName', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # generationid = models.CharField(db_column='GenerationID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # stateid = models.CharField(db_column='StateID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # gatrspaymentreason = models.CharField(db_column='GATRSPaymentReason', max_length=2)  # Field name made lowercase.
    # gatrsproratedsummerpay = models.BooleanField(db_column='GATRSProratedSummerPay')  # Field name made lowercase.
    # gatrssummeremploymentpay = models.BooleanField(db_column='GATRSSummerEmploymentPay')  # Field name made lowercase.
    # gapserspaymentreason = models.CharField(db_column='GAPSERSPaymentReason', max_length=2)  # Field name made lowercase.
    # nvincludeincontractamt = models.BooleanField(db_column='NVIncludeInContractAmt')  # Field name made lowercase.
    # idpersiearningtype = models.CharField(db_column='IDPERSIEarningType', max_length=1)  # Field name made lowercase.
    # firstperiodpayamount = models.DecimalField(db_column='FirstPeriodPayAmount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # tblwyxtrasalreasonsid = models.IntegerField(db_column='tblWYXtraSalReasonsID', blank=True, null=True)  # Field name made lowercase.
    # ileisexcludefromeis = models.BooleanField(db_column='ILEISExcludeFromEIS')  # Field name made lowercase.
    # ileisfirstyear = models.BooleanField(db_column='ILEISFirstYear')  # Field name made lowercase.
    # ileispositiontimeframe = models.CharField(db_column='ILEISPositionTimeFrame', max_length=2)  # Field name made lowercase.
    # ileisbilinguallanguage = models.CharField(db_column='ILEISBilingualLanguage', max_length=3)  # Field name made lowercase.
    # nvpersstatuscode = models.CharField(db_column='NVPERSStatusCode', max_length=2)  # Field name made lowercase.
    # wawcplanid = models.IntegerField(db_column='WAWCPlanID', blank=True, null=True)  # Field name made lowercase.
    # ileisoverridefte = models.FloatField(db_column='ILEISOverrideFTE')  # Field name made lowercase.
    # ileisoverridercdts = models.CharField(db_column='ILEISOverrideRCDTS', max_length=15)  # Field name made lowercase.
    # salaryschedule = models.CharField(db_column='SalarySchedule', max_length=165, blank=True, null=True)  # Field name made lowercase.
    # excludeeeoc4 = models.BooleanField(db_column='ExcludeEEOC4')  # Field name made lowercase.
    # sijobcode = models.CharField(db_column='SIJobCode', max_length=20)  # Field name made lowercase.
    # wastatefte = models.FloatField(db_column='WAStateFTE', blank=True, null=True)  # Field name made lowercase.
    # excludefrompar = models.BooleanField(db_column='ExcludeFromPAR')  # Field name made lowercase.
    # acahrsperunit = models.FloatField(db_column='ACAHrsPerUnit')  # Field name made lowercase.
    # acaexclude = models.CharField(db_column='ACAExclude', max_length=5)  # Field name made lowercase.
    # acaannualsalary = models.FloatField(db_column='ACAAnnualSalary', blank=True, null=True)  # Field name made lowercase.
    # maannualsalary = models.DecimalField(db_column='MAAnnualSalary', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # copassedhousse = models.CharField(db_column='COPassedHOUSSE', max_length=2)  # Field name made lowercase.
    # cohighlyqualified = models.CharField(db_column='COHighlyQualified', max_length=2)  # Field name made lowercase.
    # vtoccupationaltitle = models.CharField(db_column='VTOccupationalTitle', max_length=10)  # Field name made lowercase.
    # mtpaytypecode = models.CharField(db_column='MTPayTypeCode', max_length=10)  # Field name made lowercase.
    # ndcertstatus = models.CharField(db_column='NDCertStatus', max_length=1)  # Field name made lowercase.
    # ndspecedparaage = models.CharField(db_column='NDSpecEdParaAge', max_length=1)  # Field name made lowercase.
    # ndspecedparainst = models.CharField(db_column='NDSpecEdParaInst', max_length=1)  # Field name made lowercase.
    # ndpercentspedpk = models.FloatField(db_column='NDPercentSPEDPK')  # Field name made lowercase.
    # ndpercentkg = models.FloatField(db_column='NDPercentKG')  # Field name made lowercase.
    # ndpercent1to6 = models.FloatField(db_column='NDPercent1to6')  # Field name made lowercase.
    # ndpercent7to8 = models.FloatField(db_column='NDPercent7to8')  # Field name made lowercase.
    # ndpercent9to12 = models.FloatField(db_column='NDPercent9to12')  # Field name made lowercase.
    # tblprpositionsid_bridge = models.IntegerField(db_column='tblPRPositionsID_Bridge', blank=True, null=True)  # Field name made lowercase.
    # althrrate = models.DecimalField(db_column='AltHrRate', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    # retcontrol = models.CharField(db_column='RetControl', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # reportabledays = models.FloatField(db_column='ReportableDays', blank=True, null=True)  # Field name made lowercase.
    # reportablehours = models.FloatField(db_column='ReportableHours', blank=True, null=True)  # Field name made lowercase.
    # oebbreportable = models.NullBooleanField(db_column='OEBBReportable')  # Field name made lowercase.
    # gradelevel = models.CharField(db_column='GradeLevel', max_length=2)  # Field name made lowercase.
    # primaryworklocation = models.CharField(db_column='PrimaryWorkLocation', max_length=1)  # Field name made lowercase.
    # azemppaytype = models.SmallIntegerField(db_column='AZEmpPayType')  # Field name made lowercase.
    # statuscodeoverride = models.CharField(db_column='StatusCodeOverride', max_length=1, blank=True, null=True)  # Field name made lowercase.
    # gaprcinclude = models.BooleanField(db_column='GAPRCInclude')  # Field name made lowercase.
    # akexcludefromclassified = models.BooleanField(db_column='AKExcludeFromClassified')  # Field name made lowercase.
    # akexcludefromcertified = models.BooleanField(db_column='AKExcludeFromCertified')  # Field name made lowercase.
    # akeslendorsement = models.CharField(db_column='AKESLEndorsement', max_length=1)  # Field name made lowercase.
    # akspedendorsement = models.CharField(db_column='AKSPEDEndorsement', max_length=2)  # Field name made lowercase.
    # aklowestgrade = models.CharField(db_column='AKLowestGrade', max_length=2)  # Field name made lowercase.
    # akhighestgrade = models.CharField(db_column='AKHighestGrade', max_length=2)  # Field name made lowercase.
    # wafuturebridge = models.NullBooleanField(db_column='WAFutureBridge')  # Field name made lowercase.
    # copassedsecondarytest = models.BooleanField(db_column='COPassedSecondaryTest')  # Field name made lowercase.
    # mascheduledhours = models.FloatField(db_column='MAScheduledHours')  # Field name made lowercase.
    # maadditionalincomereason = models.CharField(db_column='MAAdditionalIncomeReason', max_length=3)  # Field name made lowercase.
    # manontaxablereason = models.CharField(db_column='MANonTaxableReason', max_length=5)  # Field name made lowercase.
    # iacontractdaysoverride = models.IntegerField(db_column='IAContractDaysOverride', blank=True, null=True)  # Field name made lowercase.
    # lowgradecode = models.IntegerField(db_column='LowGradeCode')  # Field name made lowercase.
    # highgradecode = models.IntegerField(db_column='HighGradeCode')  # Field name made lowercase.
    # specialeducation = models.BooleanField(db_column='SpecialEducation')  # Field name made lowercase.
    # distancelearning = models.BooleanField(db_column='DistanceLearning')  # Field name made lowercase.
    # copassednclbhqapproved = models.BooleanField(db_column='COPassedNCLBHQApproved')  # Field name made lowercase.
    # approvedtimeactive = models.BooleanField(db_column='ApprovedTimeActive')  # Field name made lowercase.
    # approvedtimehours = models.FloatField(db_column='ApprovedTimeHours')  # Field name made lowercase.
    # approvedtimeperiodlimit = models.FloatField(db_column='ApprovedTimePeriodLimit')  # Field name made lowercase.
    # approvedtimemaintainhours = models.BooleanField(db_column='ApprovedTimeMaintainHours')  # Field name made lowercase.
    # gacpisubmattercode = models.CharField(db_column='GACPISubMatterCode', max_length=4)  # Field name made lowercase.
    # gacpifieldstatus = models.CharField(db_column='GACPIFieldStatus', max_length=1)  # Field name made lowercase.
    # mtwcplanid = models.IntegerField(db_column='MTWCPlanID')  # Field name made lowercase.
    # azhqreportable = models.BooleanField(db_column='AZHQReportable')  # Field name made lowercase.
    # azhqcore = models.BooleanField(db_column='AZHQCore')  # Field name made lowercase.
    # azhqteacherofrecord = models.BooleanField(db_column='AZHQTeacherOfRecord')  # Field name made lowercase.
    # azhqps = models.BooleanField(db_column='AZHQPS')  # Field name made lowercase.
    # azhqkg = models.BooleanField(db_column='AZHQKG')  # Field name made lowercase.
    # azhqg1 = models.BooleanField(db_column='AZHQG1')  # Field name made lowercase.
    # azhqg2 = models.BooleanField(db_column='AZHQG2')  # Field name made lowercase.
    # azhqg3 = models.BooleanField(db_column='AZHQG3')  # Field name made lowercase.
    # azhqg4 = models.BooleanField(db_column='AZHQG4')  # Field name made lowercase.
    # azhqg5 = models.BooleanField(db_column='AZHQG5')  # Field name made lowercase.
    # azhqg6 = models.BooleanField(db_column='AZHQG6')  # Field name made lowercase.
    # azhqg7 = models.BooleanField(db_column='AZHQG7')  # Field name made lowercase.
    # azhqg8 = models.BooleanField(db_column='AZHQG8')  # Field name made lowercase.
    # azhqg9 = models.BooleanField(db_column='AZHQG9')  # Field name made lowercase.
    # azhqg10 = models.BooleanField(db_column='AZHQG10')  # Field name made lowercase.
    # azhqg11 = models.BooleanField(db_column='AZHQG11')  # Field name made lowercase.
    # azhqg12 = models.BooleanField(db_column='AZHQG12')  # Field name made lowercase.
    # tblprhqcontentareaid = models.IntegerField(db_column='tblPRHQContentAreaID')  # Field name made lowercase.
    # tblprhqcriteriaid = models.IntegerField(db_column='tblPRHQCriteriaID')  # Field name made lowercase.
    # tblprhqpositionid = models.IntegerField(db_column='tblPRHQPositionID')  # Field name made lowercase.
    # tblprhqstatuslookupid = models.IntegerField(db_column='tblPRHQStatusLookupID')  # Field name made lowercase.
    # azhqstartdate = models.DateTimeField(db_column='AZHQStartDate', blank=True, null=True)  # Field name made lowercase.
    # azhqcontentarea = models.CharField(db_column='AZHQContentArea', max_length=10)  # Field name made lowercase.
    # azhqcriteria = models.CharField(db_column='AZHQCriteria', max_length=10)  # Field name made lowercase.
    # azhqposition = models.CharField(db_column='AZHQPosition', max_length=10)  # Field name made lowercase.
    # azhqstatus = models.CharField(db_column='AZHQStatus', max_length=10)  # Field name made lowercase.
    # azhqperiods = models.CharField(db_column='AZHQPeriods', max_length=2)  # Field name made lowercase.
    # azhqsitenumber = models.CharField(db_column='AZHQSiteNumber', max_length=10)  # Field name made lowercase.
    # azhqschoolname = models.CharField(db_column='AZHQSchoolName', max_length=100)  # Field name made lowercase.
    # azhqstatusdesc = models.CharField(db_column='AZHQStatusDesc', max_length=50)  # Field name made lowercase.
    # azhqcriteriadesc = models.CharField(db_column='AZHQCriteriaDesc', max_length=50)  # Field name made lowercase.
    # azhqpositiondesc = models.CharField(db_column='AZHQPositionDesc', max_length=50)  # Field name made lowercase.
    # azhqcontentareadesc = models.CharField(db_column='AZHQContentAreaDesc', max_length=50)  # Field name made lowercase.
    # tblprhqschoolsid = models.IntegerField(db_column='tblPRHQSchoolsID')  # Field name made lowercase.
    # meyrlycontractamt = models.DecimalField(db_column='MEYrlyContractAmt', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # mepersnlstatuscd = models.CharField(db_column='MEPersnlStatusCd', max_length=2)  # Field name made lowercase.
    # meretplanstatuscd = models.CharField(db_column='MERetPlanStatusCd', max_length=1)  # Field name made lowercase.
    # metimeunitcd = models.CharField(db_column='METimeUnitCd', max_length=1)  # Field name made lowercase.
    # meexpctdfulltimewk = models.FloatField(db_column='MEExpctdFullTimeWk')  # Field name made lowercase.
    # meexpctdweeksyr = models.SmallIntegerField(db_column='MEExpctdWeeksYr')  # Field name made lowercase.
    # mebenplancd = models.CharField(db_column='MEBenPlanCd', max_length=5)  # Field name made lowercase.
    # merateschedno = models.CharField(db_column='MERateSchedNo', max_length=6)  # Field name made lowercase.
    # meemployercd = models.CharField(db_column='MEEmployerCd', max_length=6)  # Field name made lowercase.
    # merateofpay = models.DecimalField(db_column='MERateOfPay', max_digits=19, decimal_places=4)  # Field name made lowercase.
    # metimepaid = models.IntegerField(db_column='METimePaid')  # Field name made lowercase.
    # meposclasscd = models.CharField(db_column='MEPosClassCd', max_length=6)  # Field name made lowercase.
    # meincludepayrate = models.BooleanField(db_column='MEIncludePayRate')  # Field name made lowercase.
    # excludefromtransparency = models.BooleanField(db_column='ExcludeFromTransparency')  # Field name made lowercase.
    # mtratetype = models.CharField(db_column='MTRateType', max_length=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'viwPRPositions'
