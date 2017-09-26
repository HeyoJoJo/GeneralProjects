' Script to update lists in quality center admin console easily and remotely
Sub List_Add()

Server = "http://QCurl.com:8080"
User = "username"
Domain = "target_domain_name"
Project = InputBox("YourProject:")
ListName = "target_listname"
Password = "user password"
    
	' Create the connection and the excel file object
    Set tdc = CreateObject("tdapiole80.tdconnection")
    tdc.InitConnection Server, Domain
    tdc.ConnectProject Project, User, Password
    Set objXL = CreateObject("Excel.Application")
    matrisPath = "C:/path/to/file.xlsx"
    objXL.Visible = False
    objXL.Workbooks.Open matrisPath
    Set origin = objXL.Cells(1, 1)
    
	' Open customization
	Set cust = tdc.Customization
    cust.Load
    Set listRoot = cust.Lists.List(CStr(ListName)).RootNode
    i = 0
    Do While 1 = 1
        listItem = origin.Offset(i, 0).Text
        If listItem = "" Then
            Exit Do
        End If
        'Avoid an error if an item already exists
        On Error Resume Next
        listRoot.AddChild (listItem)
        On Error GoTo 0
        i = i + 1
    Loop
    listRoot.Updated = True
    cust.Commit
    objXL.Quit
    Set listRoot = Nothing
    Set origin = Nothing
    Set cust = Nothing
    tdc.Disconnect
    tdc.ReleaseConnection
    MsgBox "Done!!!"

End Sub