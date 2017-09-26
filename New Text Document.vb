' Quality Center Sub to allow for changing fields dependent on another
' Useful for autopopulation or setting required fields based off other field values
Bug_FieldChange(FieldName)
  On Error Resume Next
    
	Select Case FieldName  
	  Case "BG_STATUS"
	    If Bug_Fields("BG_STATUS").Value = "Closed" Then
		  Bug_Fields("BG_EXAMPLE_USER_FIELD").IsRequired = True
		  Bug_Fields("BG_EXAMPLE_USER_FIELD_2").IsReadOnly = True
		
		End If
	End Select
  On Error GoTo 0
End Sub


' Sub to determine if bug can post or not
Function Bug_CanPost
  On Error Resume Next
  
  If Bug_Fields("BG_EXAMPLE_USER_FIELD_3").Value = "An initial value to check" and Bug_Fields("BG_EXAMPLE_USER_FIELD_4").Value = "A second, conflicting value" Then
    msgbox "You cannot have 'An initial value to check' in field 3, and 'A second, conflicting value' in field 4"
	Bug_CanPost = False
  
  Else
    Bug_CanPost = True
  
  End If
  On Error GoTo 0
End Function

