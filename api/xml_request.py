import requests

post_vars = {
    "sStartDate": "20170101000000",
    "sEndDate": "20170320000000",
    "sKey": "680iv19L72ta1SN47t00888iG26L1H3I",
}
r = requests.post("https://phxschools.tedk12.com/hire/nfIntegration/srApplicantExport.asmx/RetrieveHiresXML", data=post_vars)

xml_file = open("test.xml", "w")
xml_file.truncate()
xml_file.write(r.text)
xml_file.close()
